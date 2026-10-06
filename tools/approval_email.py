"""Soạn email nhắc anh Tin duyệt bài blog, lấy dữ liệu từ content/editorial/calendar.json.

Mỗi bài cần: wp_id, media_id, summary (2 đến 3 câu), confirm (danh sách điểm cần xác nhận, có thể rỗng).
Cách dùng: python3 tools/approval_email.py [--mark] 3 4  -> in JSON {to, subject, body, htmlBody, deadline} để gửi qua Gmail.
--mark: ghi approval=pending và approval_requested=bây giờ vào calendar.json (dùng khi gửi thật, không dùng cho email mẫu).
"""
import html
import json
import subprocess
import sys
from datetime import date, datetime

from fix_alt import api
from blog_post import APPROVAL_WINDOW, VN, find, load, save

TO = "hi@tinle.co"
DAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
BTN = ("display:inline-block;padding:10px 18px;border-radius:6px;text-decoration:none;"
       "font-weight:600;font-size:14px;")


def when(post):
    d = date.fromisoformat(post["date"])
    return f"{DAYS[d.weekday()]} {d.day}/{d.month}, {post['time']}"


def public_preview(pid, days=7):
    """Link xem trước không cần đăng nhập (mu-plugin adtek-public-preview.php). None nếu plugin chưa cài."""
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-X", "POST",
                        f"https://adtek.agency/wp-json/adtek/v1/preview/{pid}", "-d", f"days={days}"],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get("url")
    except (json.JSONDecodeError, AttributeError):
        return None


PREVIEWS = {}


def links(post):
    pid = post["wp_id"]
    if pid not in PREVIEWS:
        PREVIEWS[pid] = public_preview(pid) or f"https://adtek.agency/?p={pid}&preview=true"
    return PREVIEWS[pid], f"https://adtek.agency/wp-admin/post.php?post={pid}&action=edit"


def card(post):
    e = html.escape
    preview, edit = links(post)
    cover = api("GET", f"media/{post['media_id']}?_fields=source_url").get("source_url", "")
    confirm = "".join(f"<li>{e(c)}</li>" for c in post.get("confirm", []))
    return f"""
<div style="border:1px solid #E3E8F0;border-radius:10px;overflow:hidden;margin:0 0 24px">
  <a href="{preview}"><img src="{cover}" alt="{e(post['title'])}" width="560" style="display:block;width:100%;max-width:560px;height:auto;border:0"></a>
  <div style="padding:18px 20px">
    <div style="color:#FF9014;font-weight:700;font-size:12px;letter-spacing:1px;text-transform:uppercase">Bài {post['no']} · Đăng {e(when(post))}</div>
    <h2 style="margin:6px 0 10px;font-size:19px;line-height:1.35;color:#002D72">{e(post['title'])}</h2>
    <p style="margin:0 0 12px;font-size:14px;line-height:1.6;color:#333">{e(post.get('summary', ''))}</p>
    {f'<p style="margin:0 0 4px;font-size:14px;font-weight:600;color:#333">Cần anh xác nhận:</p><ul style="margin:0 0 14px;padding-left:20px;font-size:14px;line-height:1.6;color:#333">{confirm}</ul>' if confirm else ''}
    <table role="presentation" cellspacing="0" cellpadding="0" border="0"><tr>
      <td bgcolor="#002D72" style="background-color:#002D72;border-radius:6px">
        <a href="{preview}" style="{BTN}color:#ffffff;background-color:#002D72;border:1px solid #002D72">Xem trước bài viết</a></td>
      <td width="10"></td>
      <td bgcolor="#ffffff" style="background-color:#ffffff;border-radius:6px">
        <a href="{edit}" style="{BTN}color:#002D72;background-color:#ffffff;border:1px solid #002D72">Sửa trên WordPress (cần đăng nhập)</a></td>
    </tr></table>
  </div>
</div>"""


def build(nos, mark=False):
    data = load()
    posts = [find(data, n) for n in nos]
    now = datetime.now(VN)
    deadline = now + APPROVAL_WINDOW
    due = f"{deadline.hour}:{deadline.minute:02d} {DAYS[deadline.weekday()]} {deadline.day}/{deadline.month}"
    if mark:
        for p in posts:
            p["approval"], p["approval_requested"] = "pending", now.isoformat(timespec="seconds")
        save(data)
    subject = ("[Adtek Blog] Cần duyệt bài " + " và ".join(str(p["no"]) for p in posts)
               + ": đăng " + ", ".join(f"{date.fromisoformat(p['date']).day}/{date.fromisoformat(p['date']).month}" for p in posts))
    howto = ("Cách duyệt: trả lời trong phiên Claude Code \"duyệt bài X\", hoặc ghi chỗ cần sửa. "
             f"Nếu anh chưa phản hồi trước {due}, bài sẽ tự đặt lịch đăng theo kế hoạch; "
             "sau đó anh vẫn hủy được trước giờ đăng bằng cách nhắn \"hủy bài X\". "
             + ("Link xem trước mở được không cần đăng nhập, hết hạn sau 7 ngày."
                if all("adtek_preview=" in links(p)[0] for p in posts)
                else "Link xem trước cần đăng nhập WordPress."))
    htmlbody = f"""<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#333">
<p style="font-size:15px;line-height:1.6">Chào anh Tin,</p>
<p style="font-size:15px;line-height:1.6">{len(posts)} bài blog mới đã lên WordPress ở dạng nháp và đang chờ anh duyệt.</p>
<p style="font-size:14px;line-height:1.6;padding:10px 14px;background-color:#FFF4E8;border-left:3px solid #FF9014">Hạn duyệt: <strong>{due}</strong>. Quá hạn mà chưa có phản hồi, bài sẽ tự đặt lịch đăng theo kế hoạch.</p>
{''.join(card(p) for p in posts)}
<p style="font-size:13px;line-height:1.6;color:#666">{html.escape(howto)}</p>
</div>"""
    text = "Chào anh Tin,\n\n" + "\n\n".join(
        f"Bài {p['no']}: {p['title']}\nĐăng: {when(p)}\nXem trước: {links(p)[0]}\nSửa (cần đăng nhập): {links(p)[1]}\n{p.get('summary', '')}"
        + ("\nCần anh xác nhận:\n" + "\n".join(f"- {c}" for c in p["confirm"]) if p.get("confirm") else "")
        for p in posts) + "\n\n" + howto
    return {"to": [TO], "subject": subject, "body": text, "htmlBody": htmlbody, "deadline": deadline.isoformat(timespec="minutes")}


if __name__ == "__main__":
    args = sys.argv[1:]
    print(json.dumps(build([int(x) for x in args if x != "--mark"], mark="--mark" in args), ensure_ascii=False))
