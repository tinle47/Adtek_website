// Chụp ảnh toàn trang (mobile 412px và desktop 1366px) + ghi lỗi console, dùng cùng máy chủ giả lập.
import puppeteer from './lh/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
const [mode, ...pages] = process.argv.slice(2);
const browser = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: 'new',
  args: ['--no-sandbox', '--ignore-certificate-errors', '--host-resolver-rules=MAP adtek.agency 127.0.0.1', `--proxy-server=${process.env.HTTPS_PROXY}`, '--proxy-bypass-list=adtek.agency'] });
for (const spec of pages) {
  const [name, path] = spec.split(':');
  for (const [vw, w, h, mobile] of [['m', 412, 860, true], ['d', 1366, 900, false]]) {
    const page = await browser.newPage(); const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
    await page.setViewport({ width: w, height: h, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1 });
    await page.goto('https://adtek.agency' + path, { waitUntil: 'networkidle0', timeout: 120000 }).catch(e => errors.push('goto: ' + e.message));
    // cuộn hết trang để ảnh lazy và hiệu ứng chạy, rồi về đầu trang
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
    await new Promise(r => setTimeout(r, 2500));
    await page.screenshot({ path: `shots/${mode}-${name}-${vw}-top.png` });
    await page.screenshot({ path: `shots/${mode}-${name}-${vw}-full.png`, fullPage: true });
    const info = await page.evaluate(() => ({ h: document.body.scrollHeight, fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style).join(', '),
      faWidth: (() => { const i = document.querySelector('[class*="fa-"]'); return i ? getComputedStyle(i, '::before').content : 'none'; })() }));
    console.log(mode, name, vw, JSON.stringify(info), errors.length ? '\n   ' + errors.join('\n   ') : '');
    await page.close();
  }
}
await browser.close();
