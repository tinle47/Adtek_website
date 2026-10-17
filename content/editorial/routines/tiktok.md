# Routine: Video TikTok Adtek (đăng qua Zernio)

Anh Tin chọn ngày 17/10/2026: đăng tự động qua Zernio (zernio.com, gói miễn phí cho 2 tài khoản). Script tải video lên Zernio và hẹn giờ; đến giờ Zernio đăng công khai lên TikTok Adtek, gắn nhãn "Nội dung do AI tạo" (giọng đọc nhân bản bằng ElevenLabs). Không dùng Direct Post bằng ứng dụng TikTok riêng: Content Sharing Guidelines của TikTok không duyệt công cụ chỉ đăng lên tài khoản do chính mình quản lý. Phương án dự phòng B (đẩy vào hộp nháp, anh Tin tự bấm Đăng) vẫn có trong script: lệnh `auth`, `upload`, `inbox-status`.

Lịch video: danh sách `tiktok` trong `calendar.json` (3 video/tuần, phiên Adtek - Marketing lập, không tự đổi date, time). Kịch bản `video/scripts/<slug bài blog>/<part>.json`, giọng `video/tools/voice.mjs`, dựng `video/tools/render.mjs` (xem `video/README.md`). Công cụ: `tools/tiktok_post.py`.

Cài đặt đăng mặc định (`TIKTOK_SETTINGS` trong script): công khai, cho bình luận, Duet, Stitch (tự tắt mục nào tài khoản đã tắt trong app), nhãn AI bật, không bật nhãn quảng cáo. Caption = `caption` + `hashtags` của kịch bản, không link (link để ở bio).

## Cài đặt một lần (anh Tin)

1. Tài khoản TikTok Adtek để chế độ công khai; nên là tài khoản doanh nghiệp (Business).
2. Tạo tài khoản Zernio, kết nối TikTok Adtek trong trang quản trị (đăng nhập TikTok, bấm Cho phép).
3. Tạo API key trong Zernio, lưu vào cài đặt môi trường cloud với tên `ZERNIO_API_KEY` (Network secrets hoặc biến môi trường). Không dán vào chat.
4. Mở phiên mới, chạy `python3 tools/tiktok_post.py check`: phải ra đúng tên tài khoản TikTok Adtek, có `PUBLIC_TO_EVERYONE`.
5. Đăng thử một video: hẹn một mục tiktok bằng `schedule`, kiểm tra trên TikTok sau giờ đăng, rồi mới bật lịch tự động.

## Mỗi video

1. Trước ngày đăng: kịch bản, giọng, dựng video (`show <id>` liệt kê việc còn thiếu). `video/out/` không nằm trong git, phiên hẹn đăng phải dựng lại nếu chưa có file.
2. Báo trước và hẹn giờ (trong 24 giờ trước giờ đăng): `schedule <id>`. Gửi anh Tin video (SendUserFile), caption, push notification "Video TikTok <giờ>: <angle>. Không nhắn hủy thì Zernio đăng đúng giờ."
3. Anh Tin nhắn "hủy <id>": `cancel <id>` (xóa lịch trên Zernio). Sửa caption: sửa kịch bản, `cancel <id>`, đổi status về `planned`, rồi `schedule <id>` lại.
4. Sau giờ đăng khoảng 30 phút: `status <id>`. Đã đăng: push notification kèm `tiktok_url` (TikTok có thể mất vài phút mới trả link, chạy lại `status` sau). `failed`: báo anh Tin nguyên văn `fail_reason`, không thử cách khác.
5. Ghi `logs/changelog.md`, commit, push.

Giới hạn: TikTok tối đa 15 video mỗi 24 giờ cho mỗi tài khoản; Zernio gói miễn phí 60 lượt gọi mỗi phút. Bản tải lên Zernio giữ 7 ngày, nên hẹn trong vòng 7 ngày trước giờ đăng.

Lịch tự động chưa tạo: chờ có `ZERNIO_API_KEY` (bước 3), lần đăng thử (bước 5) và kịch bản video đầu tiên.
