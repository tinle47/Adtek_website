// In file HTML thành PDF khổ A4 hoặc chụp ảnh.
// Cách dùng: node tools/render_pdf.js jobs.json
//   jobs.json: mảng {input, output, kind: "pdf"|"jpg", margin?, footer?, width?, height?}
//   pdf: footer là chữ ở chân trang (kèm số trang), bỏ trống thì không in chân trang.
const { chromium } = require("playwright");
const path = require("path");

const FOOT = (text) => `<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5px;color:#6B7280;padding:0 16mm;display:flex;justify-content:space-between">
<span>${text}</span><span><span class="pageNumber"></span></span></div>`;

(async () => {
  const jobs = require(path.resolve(process.argv[2]));
  const browser = await chromium.launch();
  for (const job of jobs) {
    const page = await browser.newPage({ viewport: { width: +(job.width || 794), height: +(job.height || 1123) } });
    await page.goto("file://" + path.resolve(job.input));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    if (job.kind === "jpg") {
      await page.screenshot({ path: job.output, type: "jpeg", quality: 88 });
    } else {
      const m = job.margin || "0";
      await page.pdf({
        path: job.output, format: "A4", printBackground: true, preferCSSPageSize: false,
        margin: { top: m, bottom: job.footer ? "18mm" : m, left: "0", right: "0" },
        displayHeaderFooter: !!job.footer, headerTemplate: "<div></div>",
        footerTemplate: job.footer ? FOOT(job.footer) : "<div></div>",
      });
    }
    await page.close();
  }
  await browser.close();
})();
