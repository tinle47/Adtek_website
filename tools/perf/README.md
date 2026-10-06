# Đo tốc độ trước/sau cho mu-plugin adtek-performance

Chạy plugin trên HTML thật của website (không cần cài WordPress), phục vụ lại qua một máy chủ HTTPS/HTTP2 giả lập adtek.agency, rồi đo Lighthouse mobile cho bản gốc và bản tối ưu trong cùng điều kiện.

```bash
mkdir -p build/perf && cp tools/perf/* build/perf/ && cd build/perf
npm init -y && npm i lighthouse@12          # Lighthouse + puppeteer-core
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 7 -subj "/CN=adtek.agency"
mkdir -p pages
curl -sS --compressed -o pages/home.orig.html https://adtek.agency/
curl -sS --compressed -o pages/post.orig.html https://adtek.agency/aio-la-gi/
python3 prep.py                              # tải CSS/JS nguồn vào site/
mkdir -p site/wp-content/mu-plugins/adtek-performance site/wp-content/themes
cp -r ../../wordpress/mu-plugins/adtek-performance/fonts site/wp-content/mu-plugins/adtek-performance/
cp -r ../../wordpress/themes/monatheme site/wp-content/themes/
php harness.php home post                    # tạo pages/*.opt.html và file gộp trong site/wp-content/uploads/adtek-perf/
./runlh.sh orig 3 home:/ post:/aio-la-gi/    # bản gốc
./runlh.sh opt 3 home:/ post:/aio-la-gi/     # bản tối ưu
python3 lhsum.py res/opt-home-1.json
node shots.mjs opt home:/                    # ảnh chụp mobile/desktop + lỗi console vào shots/ (cần mkdir shots, chạy máy chủ trước)
```

- Máy chủ cần cổng 443 (chạy bằng root). Trang HTML trả về sau 300 ms, tài nguyên khác sau 40 ms để mô phỏng độ trễ mạng.
- Script bên thứ ba (Google Tag Manager, Crisp) có thể bị chặn trong môi trường thử, nên điểm đo được thường cao hơn PageSpeed thật. Dùng để so sánh trước/sau, không thay cho PageSpeed Insights.
