// Máy chủ thử nghiệm: giả lập adtek.agency (HTTP/2 + Brotli), trang HTML lấy từ pages/<tên>.<mode>.html,
// file tối ưu lấy từ site/, còn lại lấy từ website thật (cache vào mirror/).
import http2 from 'node:http2'; import fs from 'node:fs'; import path from 'node:path'; import zlib from 'node:zlib'; import crypto from 'node:crypto'; import { execFileSync } from 'node:child_process';
const S = path.dirname(new URL(import.meta.url).pathname); const MODE = process.argv[2] || 'orig';
const ROUTES = { '/': 'home', '/aio-la-gi/': 'post', '/blog/': 'blog', '/solutions/': 'solutions', '/contact/': 'contact', '/solution/integrated-marketing-communication-imc/': 'imc', '/faq/': 'faq' };
const TYPES = { '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.woff': 'font/woff', '.gif': 'image/gif', '.json': 'application/json', '.ttf': 'font/ttf' };
fs.mkdirSync(S + '/mirror', { recursive: true });
const brCache = new Map();
function send(stream, body, type, cache, accept) {
  const h = { ':status': 200, 'content-type': type, 'cache-control': cache };
  if (/text|javascript|json|svg/.test(type) && /br/.test(accept || '')) {
    const k = crypto.createHash('md5').update(body).digest('hex');
    if (!brCache.has(k)) brCache.set(k, zlib.brotliCompressSync(body, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 5 } }));
    body = brCache.get(k); h['content-encoding'] = 'br';
  }
  stream.respond(h); stream.end(body);
}
const server = http2.createSecureServer({ key: fs.readFileSync(S + '/key.pem'), cert: fs.readFileSync(S + '/cert.pem'), allowHTTP1: true });
server.on('stream', (stream, headers) => { setTimeout(() => handle(stream, headers), DELAY); });
const DELAY = 40;
function handle(stream, headers) {
  const url = new URL(headers[':path'], 'https://adtek.agency'); const p = decodeURIComponent(url.pathname); const accept = headers['accept-encoding'];
  try {
    if (ROUTES[p]) { const f = `${S}/pages/${ROUTES[p]}.${MODE}.html`; return setTimeout(() => send(stream, fs.readFileSync(f), 'text/html; charset=UTF-8', 'no-cache', accept), 300); }
    const local = S + '/site' + p;
    if ((p.startsWith('/wp-content/uploads/adtek-perf/') || p.startsWith('/wp-content/mu-plugins/')) && fs.existsSync(local)) return send(stream, fs.readFileSync(local), TYPES[path.extname(p)] || 'application/octet-stream', 'public, max-age=604800', accept);
    const key = crypto.createHash('md5').update(headers[':path']).digest('hex'); const mf = `${S}/mirror/${key}`;
    if (!fs.existsSync(mf)) {
      try { execFileSync('curl', ['-sS', '-f', '--compressed', '-o', mf, '-H', 'Accept: image/webp,*/*', 'https://adtek.agency' + headers[':path']]); }
      catch { stream.respond({ ':status': 404 }); return stream.end(); }
    }
    send(stream, fs.readFileSync(mf), TYPES[path.extname(p).toLowerCase()] || 'application/octet-stream', 'public, max-age=604800', accept);
  } catch (e) { try { stream.respond({ ':status': 500 }); stream.end(String(e)); } catch {} }
}
server.listen(443, () => console.log('listening', MODE));
