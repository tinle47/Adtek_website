"""Bài Facebook hằng ngày theo danh sách "facebook" trong content/editorial/calendar.json (lịch do phiên Adtek - Marketing lập).

Mỗi bài có id (fb-YYYYMMDD), date, time, format, title (câu hỏi), brief, link_post (số bài blog để Page bình luận link,
null thì không bình luận), caption, hashtags (3 hashtag riêng), images, approval, status.

Ảnh do phiên Adtek - Designer làm: danh sách file trong trường images (đường dẫn tính từ gốc repo), hoặc thư mục
content/facebook/<id>/ (ảnh đơn hoặc carousel đánh số 1.jpg, 2.jpg...; video là video.mp4).

Caption đăng thật (template anh Tin duyệt 16/10/2026):
  TIÊU ĐỀ CÂU HỎI IN HOA
  Xem full bài viết ở bình luận bên dưới.   (chỉ khi bài blog link_post đã lên sóng, Page sẽ bình luận link)
  caption
  #Adtek #GrowthMarketing + 3 hashtag
  Website: adtek.agency / Email: contact@adtek.agency

Cách dùng:
  python3 tools/fb_daily.py due                    bài đã đến giờ mà chưa đăng (JSON)
  python3 tools/fb_daily.py week <YYYY-MM-DD>      7 bài từ ngày đó (JSON tóm tắt)
  python3 tools/fb_daily.py show <id>              caption đăng thật, ảnh, bình luận
  python3 tools/fb_daily.py notify <id...> [--mark | --pending]   in JSON email (kèm ảnh)
        --mark: báo trước, approval = auto (anh không nhắn hủy thì đăng)
        --pending: gửi duyệt theo tuần, approval = pending, hạn 24 giờ (D+1)
  python3 tools/fb_daily.py approve <id...>        anh Tin duyệt: approval = approved
  python3 tools/fb_daily.py auto                   bài pending quá 24 giờ chưa phản hồi: approval = auto (JSON)
  python3 tools/fb_daily.py publish <id> [--dry-run]  đăng (cần approval approved hoặc auto, đủ ảnh)
  python3 tools/fb_daily.py cancel <id>            anh Tin nhắn "hủy": không đăng bài này
  python3 tools/fb_daily.py delete <id>            gỡ bài đã đăng
"""
import base64
import html
import json
import mimetypes
import sys
from datetime import datetime

from datetime import timedelta

from blog_post import APPROVAL_WINDOW, ROOT, VN, find, load, save
from fb_post import CTA, FOOTER, HASHTAGS, check, delete as graph_delete, fail, graph, is_live

TO = "hi@tinle.co"
DAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def item(data, fid):
    try:
        return next(x for x in data["facebook"] if x["id"] == fid)
    except StopIteration:
        sys.exit(f"Không có bài {fid} trong danh sách facebook")


def when(x):
    return datetime.fromisoformat(f"{x['date']}T{x['time']}:00").replace(tzinfo=VN)


def label(x):
    d = when(x)
    return f"{DAYS[d.weekday()]} {d.day}/{d.month}, {x['time']}"


def media(x):
    """Danh sách file ảnh hoặc video của bài, theo thứ tự đăng."""
    if x.get("images"):
        return [ROOT / p for p in x["images"]]
    folder = ROOT / f"content/facebook/{x['id']}"
    if not folder.is_dir():
        return []
    files = [p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".mp4", ".mov")]
    return sorted(files, key=lambda p: (len(p.stem), p.stem))


def blog_link(data, x, live_check=True):
    """(bình luận, url) nếu bài blog link_post đã lên sóng, ngược lại None."""
    if not x.get("link_post"):
        return None
    post = find(data, int(x["link_post"]))
    if not post.get("slug") or (live_check and not is_live(post)):
        return None
    url = f"https://adtek.agency/{post['slug']}/"
    text = post.get("fb_comment") or f"{post['title']}: {url}"
    return (text if url in text else f"{text} {url}"), url


def message(x, with_cta):
    head = x["title"].strip().upper() + ("\n" + CTA if with_cta else "")
    tags = HASHTAGS + [h if h.startswith("#") else "#" + h for h in (x.get("hashtags") or [])][:3]
    return "\n\n".join([head, x["caption"].strip(), " ".join(tags), FOOTER])


def problems(x, files):
    out = []
    if not x.get("caption"):
        out.append("thiếu caption")
    elif any(s in (x.get("caption") or "") + x["title"] for s in ("http", "adtek.agency")):
        out.append("caption có link")
    if len(x.get("hashtags") or []) < 3:
        out.append("thiếu 3 hashtag")
    if not files:
        out.append(f"thiếu ảnh content/facebook/{x['id']}/ từ phiên Adtek - Designer")
    elif any(not p.exists() for p in files):
        out.append("file ảnh không tồn tại: " + ", ".join(str(p.relative_to(ROOT)) for p in files if not p.exists()))
    return out


def summary(data, x, live_check=False):
    files = media(x)
    link = blog_link(data, x, live_check)
    return {"id": x["id"], "when": label(x), "format": x["format"], "title": x["title"], "status": x.get("status"),
            "approval": x.get("approval"), "media": [str(p.relative_to(ROOT)) for p in files],
            "comment": link[0] if link else None, "problems": problems(x, files)}


def due(data):
    now = datetime.now(VN)
    out = [summary(data, x, live_check=True) for x in data["facebook"]
           if x.get("status") not in ("posted", "cancelled") and when(x) <= now]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def week(data, start):
    d0 = datetime.fromisoformat(start).date()
    out = [summary(data, x) for x in data["facebook"] if 0 <= (datetime.fromisoformat(x["date"]).date() - d0).days < 7]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def show(data, x):
    link = blog_link(data, x, live_check=False)
    print(message(x, with_cta=bool(link)) if x.get("caption") else "(chưa có caption)")
    print("\n---\nBình luận:", link[0] if link else "(không bình luận)")
    print("Ảnh:", [str(p.relative_to(ROOT)) for p in media(x)])


def li_part(data, x):
    """Bản LinkedIn tiếng Anh trong email (caption đăng thật, bình luận, ảnh, vấn đề), None khi đã hủy LinkedIn.
    Duyệt một lần áp dụng cho cả Facebook và LinkedIn."""
    import li_post  # nhập trong hàm vì li_post dùng lại các hàm của file này
    if x.get("li_status") == "cancelled":
        return None
    files = li_post.media(x)
    c = li_post.comment(data, x, live_check=False)
    cap = li_post.message(x, with_cta=bool(c)) if x.get("li_title") and x.get("li_caption") else None
    return cap, c, files, li_post.problems(x, files)


def notify(data, xs, mark=False, pending=False):
    """Email báo trước: caption đăng thật, bình luận, ảnh đính kèm. Không nhắn hủy thì đăng đúng giờ."""
    e = html.escape
    blocks, texts, attachments = [], [], []
    for x in xs:
        files = media(x)
        link = blog_link(data, x, live_check=False)
        cap = message(x, with_cta=bool(link))
        issues = problems(x, files)
        li = li_part(data, x)
        texts.append(f"{x['id']} · {label(x)} · {x['format']}\n\n{cap}\n\nBình luận đầu tiên: "
                     f"{link[0] if link else '(không bình luận)'}\nẢnh: {', '.join(p.name for p in files) or 'chưa có'}"
                     + (f"\nCẦN XỬ LÝ: {'; '.join(issues)}" if issues else "")
                     + (f"\n\nLinkedIn (tiếng Anh):\n\n{li[0] or '(chưa có bản tiếng Anh)'}\n\nBình luận đầu tiên: "
                        f"{li[1] or '(không bình luận)'}\nẢnh: {', '.join(p.name for p in li[2]) or 'chưa có'}"
                        + (f"\nLINKEDIN CẦN XỬ LÝ: {'; '.join(li[3])}" if li[3] else "") if li else ""))
        blocks.append(
            f'<div style="border:1px solid #E3E8F0;border-radius:10px;padding:16px 18px;margin:0 0 20px">'
            f'<div style="color:#FF9014;font-weight:700;font-size:12px;letter-spacing:1px;text-transform:uppercase">'
            f'{e(x["id"])} · {e(label(x))} · {e(x["format"])}</div>'
            f'<div style="margin:10px 0;padding:10px 12px;background-color:#F4F6FA;border-radius:6px;font-size:13px;'
            f'line-height:1.55;color:#333">{e(cap).replace(chr(10), "<br>")}</div>'
            f'<p style="margin:0 0 6px;font-size:13px;color:#555">Bình luận đầu tiên: {e(link[0]) if link else "(không bình luận)"}</p>'
            f'<p style="margin:0;font-size:13px;color:#555">Ảnh đính kèm: {e(", ".join(p.name for p in files)) or "chưa có"}</p>'
            + (f'<p style="margin:6px 0 0;font-size:13px;color:#B42318">Cần xử lý: {e("; ".join(issues))}</p>' if issues else "")
            + (f'<div style="margin:16px 0 0;color:#002D72;font-weight:700;font-size:12px;letter-spacing:1px;'
               f'text-transform:uppercase">LinkedIn (tiếng Anh)</div>'
               f'<div style="margin:10px 0;padding:10px 12px;background-color:#F4F6FA;border-radius:6px;font-size:13px;'
               f'line-height:1.55;color:#333">{e(li[0]).replace(chr(10), "<br>") if li[0] else "(chưa có bản tiếng Anh)"}</div>'
               f'<p style="margin:0 0 6px;font-size:13px;color:#555">Bình luận đầu tiên: {e(li[1]) if li[1] else "(không bình luận)"}</p>'
               f'<p style="margin:0;font-size:13px;color:#555">Ảnh: {e(", ".join(p.name for p in li[2])) or "chưa có"}'
               f'{" (đính kèm ảnh đầu)" if li[2] else ""}</p>'
               + (f'<p style="margin:6px 0 0;font-size:13px;color:#B42318">LinkedIn cần xử lý: {e("; ".join(li[3]))}</p>'
                  if li[3] else "") if li else "")
            + "</div>")
        for i, p in enumerate(files):
            if p.exists() and p.suffix.lower() in (".jpg", ".jpeg", ".png"):
                attachments.append({"filename": f"{x['id']}-{i + 1}{p.suffix}", "mimeType": mimetypes.guess_type(p.name)[0],
                                    "content": base64.b64encode(p.read_bytes()).decode()})
        if li and li[2] and li[2][0].exists() and li[2][0].suffix.lower() in (".jpg", ".jpeg", ".png"):
            p = li[2][0]  # chỉ đính kèm ảnh đầu bản tiếng Anh để email không quá nặng
            attachments.append({"filename": f"{x['id']}-linkedin-1{p.suffix}", "mimeType": mimetypes.guess_type(p.name)[0],
                                "content": base64.b64encode(p.read_bytes()).decode()})
        if mark or pending:
            x["approval"] = "auto" if mark else "pending"
            x["notified_at"] = datetime.now(VN).isoformat(timespec="seconds")
            x["notified_media"] = len([f for f in files if f.exists()])  # 0: báo khi chưa có ảnh, cần gửi lại khi có ảnh
    if mark or pending:
        save(data)
    deadline = (datetime.now(VN) + APPROVAL_WINDOW).strftime("%H:%M %d/%m")
    first = xs[0]
    subject = f"[Adtek Facebook] {label(first)}: {first['title']}" if len(xs) == 1 else \
        f"[Adtek Facebook] {len(xs)} bài từ {label(first)}"
    both = " Duyệt hoặc hủy áp dụng cho cả bản Facebook và LinkedIn." if any(li_part(data, x) for x in xs) else ""
    note = (f'Hạn duyệt: {deadline}. Nhắn trong phiên Claude Code "Adtek - Facebook post": "duyệt &lt;id&gt;", '
            '"hủy &lt;id&gt;" hoặc ghi chỗ cần sửa. Quá hạn chưa phản hồi, bài tự được duyệt và đăng đúng giờ.') if pending else \
           ('Bài sẽ tự đăng đúng giờ. Muốn hủy hoặc sửa, nhắn trong phiên Claude Code "Adtek - Facebook post": '
            '"hủy &lt;id&gt;" hoặc ghi chỗ cần sửa, trước giờ đăng.')
    note += both
    body = "Chào anh Tin,\n\n" + "\n\n----------\n\n".join(texts) + "\n\n" + html.unescape(note)
    html_body = ('<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#333">'
                 '<p style="font-size:15px;line-height:1.6">Chào anh Tin,</p>' + "".join(blocks) +
                 f'<p style="font-size:13px;line-height:1.6;color:#666">{note}</p></div>')
    print(json.dumps({"to": [TO], "subject": subject, "body": body, "htmlBody": html_body, "attachments": attachments,
                      "deadline": (datetime.now(VN) + APPROVAL_WINDOW).isoformat(timespec="minutes") if pending else None},
                     ensure_ascii=False))


def auto(data):
    now, done = datetime.now(VN), []
    for x in data["facebook"]:
        if x.get("approval") == "pending" and x.get("notified_at") and x.get("status") not in ("posted", "cancelled") \
                and now - datetime.fromisoformat(x["notified_at"]) >= APPROVAL_WINDOW - timedelta(minutes=5):
            x["approval"] = "auto"
            done.append(x["id"])
    save(data)
    print(json.dumps({"auto_approved": done}))


def publish(data, x, dry_run=False):
    if x.get("status") == "posted":
        sys.exit(f"{x['id']}: đã đăng ({x.get('fb_post_id')}), không đăng lại")
    if x.get("status") == "cancelled":
        sys.exit(f"{x['id']}: anh Tin đã hủy, không đăng")
    files = media(x)
    issues = problems(x, files)
    if issues:
        sys.exit(f"{x['id']}: chưa đăng: {'; '.join(issues)}")
    if x.get("approval") not in ("approved", "auto"):
        sys.exit(f"{x['id']}: chưa duyệt (approval = {x.get('approval')}), chưa đăng")
    link = blog_link(data, x)
    msg = message(x, with_cta=bool(link))
    if dry_run:
        print(json.dumps({"id": x["id"], "media": [str(p.relative_to(ROOT)) for p in files], "message": msg,
                          "comment": link[0] if link else None}, ensure_ascii=False, indent=1))
        return
    check()  # token phải đúng Page
    videos = [p for p in files if p.suffix.lower() in (".mp4", ".mov")]
    if videos:
        r = graph("POST", "me/videos", form_strings={"description": msg}, files={"source": videos[0]})
        post_id = r.get("id")
    elif len(files) == 1:
        r = graph("POST", "me/photos", form_strings={"message": msg, "published": "true"}, files={"source": files[0]})
        post_id = r.get("post_id")
    else:  # carousel: tải từng ảnh ở chế độ chưa đăng, rồi gắn vào một bài
        ids = []
        for p in files:
            u = graph("POST", "me/photos", form_strings={"published": "false"}, files={"source": p})
            if "id" not in u:
                fail(f"tải ảnh {p.name}", u)
            ids.append(u["id"])
        form = {"message": msg}
        form.update({f"attached_media[{i}]": json.dumps({"media_fbid": m}) for i, m in enumerate(ids)})
        r = graph("POST", "me/feed", form_strings=form)
        post_id = r.get("id")
    if not post_id:
        fail("đăng bài", r)
    x.update({"fb_post_id": post_id, "status": "posted", "posted_at": datetime.now(VN).isoformat(timespec="seconds")})
    save(data)  # lưu ngay để lần chạy lại không đăng trùng
    if link:
        c = graph("POST", f"{post_id}/comments", form_strings={"message": link[0]})
        if "id" not in c:
            x["comment_error"] = json.dumps(c.get("error", c), ensure_ascii=False)[:300]
            save(data)
            fail("bình luận link (bài đã đăng, chưa có bình luận)", c)
        x["fb_comment_id"] = c["id"]
        save(data)
    print(json.dumps({"id": x["id"], "fb_post_id": post_id, "fb_comment_id": x.get("fb_comment_id"),
                      "url": f"https://www.facebook.com/{post_id}"}, ensure_ascii=False))


if __name__ == "__main__":
    cmd, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    data = load()
    if cmd == "due":
        due(data)
    elif cmd == "week":
        week(data, args[0])
    elif cmd == "show":
        show(data, item(data, args[0]))
    elif cmd == "notify":
        notify(data, [item(data, a) for a in args], mark="--mark" in sys.argv, pending="--pending" in sys.argv)
    elif cmd == "approve":
        for a in args:
            item(data, a)["approval"] = "approved"
        save(data)
        print(json.dumps({"approved": args}))
    elif cmd == "auto":
        auto(data)
    elif cmd == "publish":
        publish(data, item(data, args[0]), dry_run="--dry-run" in sys.argv)
    elif cmd == "cancel":
        x = item(data, args[0])
        x["status"] = "cancelled"
        save(data)
        print(json.dumps({"cancelled": x["id"]}))
    elif cmd == "delete":
        x = item(data, args[0])
        if not x.get("fb_post_id"):
            sys.exit(f"{x['id']}: chưa đăng")
        graph_delete(x["fb_post_id"])
        x.update({"status": "planned", "fb_post_id": None, "fb_comment_id": None})
        save(data)
    else:
        sys.exit(__doc__)
