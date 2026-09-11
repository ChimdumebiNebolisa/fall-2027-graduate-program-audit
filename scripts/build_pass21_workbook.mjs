import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";


const root = path.resolve(process.cwd());
const outputDir = path.join(root, "outputs", "20260911-pass21-final");
const dataPath = path.join(root, "data", "processed", "pass21", "workbook_data.json");
const workbookPath = path.join(outputDir, "graduate_program_audit_pass21_20260911.xlsx");
const renderDir = path.join(outputDir, "renders");
const qaPath = path.join(outputDir, "workbook_qa.json");
const data = JSON.parse(await fs.readFile(dataPath, "utf8"));
const artifactRenderEnabled = process.env.PASS21_ENABLE_ARTIFACT_RENDER === "1";

const COLORS = {
  navy: "#17365D",
  blue: "#2F75B5",
  lightBlue: "#D9EAF7",
  lightGray: "#F2F2F2",
  rule: "#8EA9C1",
  white: "#FFFFFF",
  amber: "#FFF2CC",
  red: "#FCE4D6",
  green: "#E2F0D9",
  text: "#222222",
};

function columnName(index) {
  let value = index + 1;
  let output = "";
  while (value) {
    value -= 1;
    output = String.fromCharCode(65 + (value % 26)) + output;
    value = Math.floor(value / 26);
  }
  return output;
}

function safeFormulaText(value) {
  return String(value).replaceAll('"', '""');
}

function tableName(name) {
  return `P21${name.replace(/[^A-Za-z0-9]/g, "").slice(0, 20)}`;
}

function addSheet(workbook, { name, title, context, rows, headers, linkHeaders = [], statusHeader = "" }) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.tabColor = name === "FINAL RANKING" ? COLORS.navy : COLORS.blue;
  const lastCol = columnName(headers.length - 1);

  sheet.getRange("A2").values = [[title]];
  sheet.getRange(`A2:${lastCol}2`).format = {
    font: { name: "Arial", size: 14, bold: true, color: COLORS.navy },
    verticalAlignment: "center",
    rowHeight: 25,
    borders: { bottom: { style: "thin", color: COLORS.rule } },
  };
  sheet.getRange("A3").values = [[context]];
  sheet.getRange(`A3:${lastCol}3`).format = {
    font: { name: "Arial", size: 9, italic: true, color: "#595959" },
    rowHeight: 20,
  };

  const matrix = [headers, ...rows.map((row) => headers.map((header) => row[header] ?? ""))];
  sheet.getRangeByIndexes(3, 0, matrix.length, headers.length).values = matrix;
  sheet.getRange(`A4:${lastCol}4`).format = {
    fill: COLORS.navy,
    font: { name: "Arial", size: 10, bold: true, color: COLORS.white },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
    rowHeight: 42,
    borders: { insideVertical: { style: "thin", color: COLORS.white } },
  };

  if (rows.length) {
    const body = sheet.getRangeByIndexes(4, 0, rows.length, headers.length);
    body.format = {
      font: { name: "Arial", size: 9, color: COLORS.text },
      wrapText: true,
      verticalAlignment: "top",
      rowHeight: name === "FINAL RANKING" ? 58 : 46,
      borders: { insideHorizontal: { style: "thin", color: "#D9E2F3" } },
    };
    sheet.tables.add(`A4:${lastCol}${rows.length + 4}`, true, tableName(name));
  }

  for (const header of linkHeaders) {
    const col = headers.indexOf(header);
    if (col < 0) continue;
    rows.forEach((row, index) => {
      const url = String(row[header] ?? "");
      if (!url.startsWith("http")) return;
      const cell = sheet.getRangeByIndexes(index + 4, col, 1, 1);
      cell.formulas = [[`=HYPERLINK("${safeFormulaText(url)}","Open official source")`]];
      cell.format.font = { name: "Arial", size: 9, color: "#0563C1", underline: true };
    });
  }

  headers.forEach((header, index) => {
    let width = 14;
    if (/rank|priority|fee$/i.test(header)) width = 11;
    else if (/university|program|faculty|contact/i.test(header)) width = 24;
    else if (/url/i.test(header)) width = 17;
    else if (/summary|rationale|evidence|fit|positive|risk|question|reason|problem|condition|claim|uncertainty|matters|decision/i.test(header)) width = 34;
    else if (/deadline|cycle|classification|position|tier|status/i.test(header)) width = 20;
    sheet.getRangeByIndexes(3, index, rows.length + 1, 1).format.columnWidth = width;
  });

  if (statusHeader) {
    const col = headers.indexOf(statusHeader);
    if (col >= 0 && rows.length) {
      const range = sheet.getRangeByIndexes(4, col, rows.length, 1);
      range.conditionalFormats.add("containsText", { text: "Conditional", format: { fill: COLORS.amber } });
      range.conditionalFormats.add("containsText", { text: "Do Not Apply", format: { fill: COLORS.red } });
      range.conditionalFormats.add("containsText", { text: "Strongest", format: { fill: COLORS.green } });
    }
  }

  sheet.freezePanes.freezeRows(4);
  sheet.freezePanes.freezeColumns(name === "FINAL RANKING" ? 3 : 2);
  return sheet;
}

const workbook = Workbook.create();
console.log("workbook-created");
const rankingHeaders = Object.keys(data.final_ranking[0]);
const evidenceHeaders = Object.keys(data.evidence[0]);
const exclusionHeaders = Object.keys(data.exclusions[0]);
const questionHeaders = Object.keys(data.open_questions[0]);

addSheet(workbook, {
  name: "FINAL RANKING",
  title: "Pass 2.1 Final Ranking",
  context: "Application-ready programs only. Funding certainty is evaluated before admission position, fit, fee, degree structure, and unresolved risk.",
  rows: data.final_ranking,
  headers: rankingHeaders,
  linkHeaders: ["Official Program URL", "Official Funding URL", "Admissions Evidence URL"],
  statusHeader: "Recommendation Tier",
});
console.log("ranking-added");

addSheet(workbook, {
  name: "FUNDING AND ADMISSIONS EVIDENCE",
  title: "Funding and Admissions Evidence",
  context: "One row per recommended or conditional program. Claims were compared with current official source content; HTTP status alone was not treated as validation.",
  rows: data.evidence,
  headers: evidenceHeaders,
  linkHeaders: ["Source URL", "Official Program URL", "Official Funding URL", "Admissions URL", "Fit URL"],
  statusHeader: "Decision Category",
});
console.log("evidence-added");

addSheet(workbook, {
  name: "EXCLUSIONS",
  title: "Exclusions and Conditional Programs",
  context: "Conditional rows need one decision-changing answer. Do Not Apply rows fail a gate or lose on the program-first funding, admission, fit, and cost comparison.",
  rows: data.exclusions,
  headers: exclusionHeaders,
  linkHeaders: ["Evidence URL"],
  statusHeader: "Revised Status",
});
console.log("exclusions-added");

addSheet(workbook, {
  name: "OPEN QUESTIONS",
  title: "Decision-Changing Open Questions",
  context: "Only questions that could change an application decision are listed. No outreach drafts or professor-tracking fields are included.",
  rows: data.open_questions,
  headers: questionHeaders,
  linkHeaders: ["Evidence URL"],
  statusHeader: "Current Decision Without Reply",
});
console.log("questions-added");

workbook.recalculate();
console.log("recalculated");
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });

const inspections = {};
for (const [sheetName, range] of [
  ["FINAL RANKING", "A2:H19"],
  ["FUNDING AND ADMISSIONS EVIDENCE", "A2:H12"],
  ["EXCLUSIONS", "A2:K30"],
  ["OPEN QUESTIONS", "A2:I12"],
]) {
  console.log(`inspecting-${sheetName}`);
  const result = await workbook.inspect({ kind: "table", range: `${sheetName}!${range}`, include: "values,formulas", tableMaxRows: 30, tableMaxCols: 27 });
  inspections[sheetName] = result.ndjson;
}

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "Pass 2.1 formula error scan",
});
console.log("formula-scan-complete");

const output = await SpreadsheetFile.exportXlsx(workbook);
console.log("xlsx-exported");
await output.save(workbookPath);

const renderRanges = [
  ["FINAL RANKING", "A2:H12"],
  ["FUNDING AND ADMISSIONS EVIDENCE", "A2:H12"],
  ["EXCLUSIONS", "A2:H12"],
  ["OPEN QUESTIONS", "A2:I12"],
];
if (artifactRenderEnabled) {
  for (const [sheetName, range] of renderRanges) {
    console.log(`rendering-${sheetName}`);
    const preview = await workbook.render({ sheetName, range, scale: 0.7, format: "png" });
    const filename = sheetName.toLowerCase().replaceAll(" ", "_").replaceAll("&", "and") + ".png";
    await fs.writeFile(path.join(renderDir, filename), new Uint8Array(await preview.arrayBuffer()));
  }
}

const qa = {
  workbook_path: workbookPath,
  sheet_count: 4,
  rendered_sheet_count: artifactRenderEnabled ? 4 : 0,
  sheets: ["FINAL RANKING", "FUNDING AND ADMISSIONS EVIDENCE", "EXCLUSIONS", "OPEN QUESTIONS"],
  expected_rows: {
    "FINAL RANKING": data.final_ranking.length,
    "FUNDING AND ADMISSIONS EVIDENCE": data.evidence.length,
    EXCLUSIONS: data.exclusions.length,
    "OPEN QUESTIONS": data.open_questions.length,
  },
  formula_error_scan: formulaErrors.ndjson,
  inspections,
  visual_review_status: "pending manual inspection",
  renderer_note: !artifactRenderEnabled
    ? "Artifact-tool rendering is disabled by default because its renderer terminates without diagnostics in this Windows runtime; use the local HTML preview for visual QA."
    : "Rendered with artifact-tool.",
};
await fs.writeFile(qaPath, JSON.stringify(qa, null, 2) + "\n", "utf8");
console.log(JSON.stringify({ workbookPath, qaPath, rendered: artifactRenderEnabled ? 4 : 0 }, null, 2));
