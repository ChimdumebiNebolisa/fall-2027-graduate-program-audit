import fs from "node:fs/promises";
import path from "node:path";

const root = path.resolve(process.cwd());
const source = JSON.parse(await fs.readFile(path.join(root, "data", "processed", "pass21", "workbook_data.json"), "utf8"));
const sheets = [
  ["FINAL RANKING", source.final_ranking],
  ["FUNDING AND ADMISSIONS EVIDENCE", source.evidence],
  ["EXCLUSIONS", source.exclusions],
  ["OPEN QUESTIONS", source.open_questions],
];

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

const panels = sheets.map(([name, rows], index) => {
  const headers = Object.keys(rows[0]);
  const visibleRows = name === "OPEN QUESTIONS" ? rows : rows.slice(0, 12);
  return `<section class="sheet" data-index="${index}">
    <h1>${escapeHtml(name)}</h1>
    <p>${visibleRows.length} rows shown of ${rows.length}; visual QA mirrors the workbook's title, header, wrapping, spacing, and status treatment.</p>
    <div class="table-wrap"><table><thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead>
    <tbody>${visibleRows.map((row) => `<tr>${headers.map((header) => {
      const value = row[header];
      const text = String(value ?? "");
      const status = /conditional/i.test(text) ? " conditional" : /do not apply/i.test(text) ? " reject" : /strongest/i.test(text) ? " strong" : "";
      return `<td class="${status}">${escapeHtml(value)}</td>`;
    }).join("")}</tr>`).join("")}</tbody></table></div>
  </section>`;
}).join("");

const html = `<!doctype html><html><head><meta charset="utf-8"><title>Pass 2.1 workbook visual QA</title><style>
  :root{font-family:Arial,sans-serif;color:#222;background:#eef2f6}body{margin:0}.qa{padding:24px}nav{display:flex;gap:8px;margin-bottom:18px;position:sticky;top:0;background:#eef2f6;padding:8px 0;z-index:3}nav a{background:#2f75b5;color:white;text-decoration:none;padding:9px 14px;border-radius:5px;font-size:13px}h1{font-size:23px;color:#17365d;border-bottom:2px solid #8ea9c1;margin:0;padding:6px 0 10px}p{color:#595959;font-size:13px;font-style:italic}.sheet{display:none;background:white;padding:18px;box-shadow:0 2px 12px #1d2d3d22}.table-wrap{overflow:auto;max-height:680px;border:1px solid #d9e2f3}table{border-collapse:collapse;min-width:100%;font-size:12px}th{position:sticky;top:0;background:#17365d;color:white;text-align:center;padding:10px;min-width:130px;max-width:280px}td{vertical-align:top;padding:9px 10px;min-width:130px;max-width:280px;white-space:normal;border-bottom:1px solid #d9e2f3;line-height:1.35}.conditional{background:#fff2cc}.reject{background:#fce4d6}.strong{background:#e2f0d9}
</style></head><body><main class="qa"><nav>${sheets.map(([name], index) => `<a href="?sheet=${index}">${escapeHtml(name)}</a>`).join("")}</nav>${panels}</main><script>
const index=Math.max(0,Math.min(3,Number(new URLSearchParams(location.search).get('sheet')||0)));document.querySelector('[data-index="'+index+'"]').style.display='block';
</script></body></html>`;

const output = path.join(root, "outputs", "20260911-pass21-final", "workbook_visual_qa.html");
await fs.writeFile(output, html, "utf8");
console.log(output);
