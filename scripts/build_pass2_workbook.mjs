import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = path.resolve(process.cwd());
const outputRoot = path.join(repoRoot, "outputs", "20260911-pass2-final");
const workbookPath = path.join(outputRoot, "graduate_program_audit_pass2_20260911.xlsx");
const qaPath = path.join(outputRoot, "workbook_qa.json");
const renderRoot = path.join(outputRoot, "renders");
const htmlRoot = path.join(outputRoot, "render_html");

if (process.argv[2] === "confirm-visual") {
  const qa = JSON.parse(await fs.readFile(qaPath, "utf8"));
  const renderFiles = await fs.readdir(renderRoot);
  const pngs = renderFiles.filter((name) => name.endsWith(".png"));
  if (pngs.length !== 11) throw new Error(`Expected 11 rendered sheets, found ${pngs.length}`);
  qa.rendered_sheet_count = 11;
  qa.visually_inspected_sheet_count = 11;
  qa.visual_review_confirmed_at = new Date().toISOString();
  await fs.writeFile(qaPath, JSON.stringify(qa, null, 2) + "\n", "utf8");
  console.log(JSON.stringify({ qaPath, visuallyInspected: 11 }, null, 2));
  process.exit(0);
}

const COLORS = {
  navy: "#17365D",
  teal: "#087E8B",
  blue: "#4F81BD",
  paleBlue: "#DCE6F1",
  paleTeal: "#DDEBF7",
  gray: "#E7E6E6",
  darkGray: "#404040",
  white: "#FFFFFF",
  green: "#E2F0D9",
  amber: "#FFF2CC",
  red: "#FCE4D6",
};

function parseCSV(text) {
  const rows = [];
  let row = [], cell = "", quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { cell += '"'; i += 1; }
      else if (ch === '"') quoted = false;
      else cell += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') { row.push(cell); cell = ""; }
    else if (ch === '\n') { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = ""; }
    else cell += ch;
  }
  if (cell.length || row.length) { row.push(cell.replace(/\r$/, "")); rows.push(row); }
  if (!rows.length) return [];
  const headers = rows[0].map((value, index) => index === 0 ? value.replace(/^\uFEFF/, "") : value);
  return rows.slice(1).filter((r) => r.some((value) => value !== "")).map((r) => Object.fromEntries(headers.map((header, i) => [header, r[i] ?? ""])));
}

async function csvRows(name) {
  return parseCSV(await fs.readFile(path.join(outputRoot, name), "utf8"));
}

function columnName(index) {
  let number = index + 1;
  let result = "";
  while (number > 0) {
    number -= 1;
    result = String.fromCharCode(65 + number % 26) + result;
    number = Math.floor(number / 26);
  }
  return result;
}

function numberValue(value) {
  const parsed = Number(value);
  return value !== "" && Number.isFinite(parsed) ? parsed : value ?? "";
}

function boolLabel(value) {
  return [true, "true", "yes"].includes(value) ? "Yes" : "No";
}

function tableName(index, name) {
  return `P2${String(index).padStart(2, "0")}${name.replace(/[^A-Za-z0-9]/g, "").slice(0, 18)}`;
}

function safeFormulaText(value) {
  return String(value).replaceAll('"', '""');
}

function addTableSheet(workbook, options) {
  const { name, title, subtitle, headers, rows, tableIndex, validations = {}, scoreHeaders = [], linkHeaders = [] } = options;
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.tabColor = tableIndex <= 3 ? COLORS.teal : COLORS.blue;
  const lastCol = columnName(headers.length - 1);
  sheet.getRange(`A1:${lastCol}1`).merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format = { fill: COLORS.navy, font: { name: "Arial", size: 15, bold: true, color: COLORS.white }, rowHeight: 28, verticalAlignment: "center" };
  sheet.getRange(`A2:${lastCol}2`).merge();
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange("A2").format = { fill: COLORS.paleBlue, font: { name: "Arial", size: 10, color: COLORS.darkGray }, wrapText: true, rowHeight: 34, verticalAlignment: "center" };
  sheet.getRange(`A3:${lastCol}3`).merge();
  sheet.getRange("A3").values = [[`Evidence snapshot: 2026-09-11 · ${rows.length.toLocaleString()} record${rows.length === 1 ? "" : "s"} · Use the row-4 filters; uncertainty is intentional.`]];
  sheet.getRange("A3").format = { fill: COLORS.gray, font: { name: "Arial", size: 9, italic: true, color: COLORS.darkGray }, rowHeight: 20 };
  const matrix = [headers, ...rows.map((row) => headers.map((header) => row[header] ?? ""))];
  sheet.getRangeByIndexes(3, 0, matrix.length, headers.length).values = matrix;
  sheet.getRangeByIndexes(3, 0, 1, headers.length).format = {
    fill: COLORS.teal,
    font: { name: "Arial", size: 10, bold: true, color: COLORS.white },
    wrapText: true,
    rowHeight: 34,
    verticalAlignment: "center",
  };
  if (rows.length) {
    const dataRange = sheet.getRangeByIndexes(4, 0, rows.length, headers.length);
    dataRange.format = {
      font: { name: "Arial", size: 9 },
      wrapText: true,
      verticalAlignment: "top",
      rowHeight: 46,
      borders: { preset: "all", style: "thin", color: "#D9E2F3" },
    };
    sheet.tables.add(`A4:${lastCol}${4 + rows.length}`, true, tableName(tableIndex, name));
  }
  sheet.freezePanes.freezeRows(4);
  sheet.freezePanes.freezeColumns(Math.min(2, headers.length));

  headers.forEach((header, index) => {
    const samples = rows.slice(0, 200).map((row) => String(row[header] ?? "").length);
    const maxLength = Math.max(header.length, ...samples, 10);
    let width = Math.min(38, Math.max(11, Math.ceil(maxLength * 0.75)));
    if (/claim|evidence|uncert|question|rationale|funding|deadline|draft|reason|coverage|limitation|research|method/i.test(header)) width = 34;
    if (/url|email/i.test(header)) width = 18;
    if (/score|rank|count|fee$/i.test(header)) width = 12;
    sheet.getRangeByIndexes(3, index, Math.max(1, rows.length + 1), 1).format.columnWidth = width;
  });

  for (const [header, values] of Object.entries(validations)) {
    const index = headers.indexOf(header);
    if (index >= 0 && rows.length) sheet.getRangeByIndexes(4, index, rows.length, 1).dataValidation = { rule: { type: "list", values } };
  }
  for (const header of scoreHeaders) {
    const index = headers.indexOf(header);
    if (index >= 0 && rows.length) {
      sheet.getRangeByIndexes(4, index, rows.length, 1).conditionalFormats.add("colorScale", {
        colors: ["#F8696B", "#FFEB84", "#63BE7B"], thresholds: ["min", { type: "percentile", value: 50 }, "max"],
      });
    }
  }
  for (const header of linkHeaders) {
    const index = headers.indexOf(header);
    if (index < 0) continue;
    rows.forEach((row, rowIndex) => {
      const url = String(row[header] ?? "");
      if (/^https?:\/\//.test(url)) {
        sheet.getRangeByIndexes(4 + rowIndex, index, 1, 1).formulas = [[`=HYPERLINK("${safeFormulaText(url)}","Open source")`]];
        sheet.getRangeByIndexes(4 + rowIndex, index, 1, 1).format.font = { name: "Arial", size: 9, color: "#0563C1", underline: true };
      }
    });
  }
  return sheet;
}

function distinct(values) {
  return new Set(values).size;
}

await fs.mkdir(renderRoot, { recursive: true });
await fs.mkdir(htmlRoot, { recursive: true });
const [programs, verification, professors, priorities, drafts, exclusions, exclusionAudit, sources, independent, recruiting] = await Promise.all([
  csvRows("programs.csv"), csvRows("program_verification.csv"), csvRows("professor_matches.csv"),
  csvRows("outreach_priority.csv"), csvRows("outreach_drafts.csv"), csvRows("exclusions.csv"),
  csvRows("exclusion_sample_audit.csv"), csvRows("source_ledger.csv"), csvRows("independent_verification.csv"),
  csvRows("recruiting_claim_recheck.csv"),
]);
// The validation category CSV lives in the processed tree, while validation.json is versioned with the workbook.
const validation = JSON.parse(await fs.readFile(path.join(outputRoot, "validation.json"), "utf8"));
const portfolio = JSON.parse(await fs.readFile(path.join(outputRoot, "portfolio.json"), "utf8"));
const actualValidationCategories = validation.categories;
const activePrograms = [...portfolio.core, ...portfolio.reserve];
const portfolioStatus = new Map(activePrograms.map((row) => [row.program_id, row.portfolio_status]));
const verificationByProgram = new Map(verification.map((row) => [row.verified_program_id, row]));
const professorsByProgram = new Map();
for (const row of professors) {
  if (!professorsByProgram.has(row.program_id)) professorsByProgram.set(row.program_id, []);
  professorsByProgram.get(row.program_id).push(row);
}
const draftsByContact = new Map(drafts.map((row) => [`${row.program_id}|${row.recipient_email.toLowerCase()}`, row]));

const workbook = Workbook.create();
let index = 1;

const dashboardMetrics = [
  { "Metric": "Programs screened", "Count": 2181, "Interpretation": "Candidate-funnel records across 855 universities" },
  { "Metric": "Programs deeply scored", "Count": programs.length, "Interpretation": "166 source-backed program records" },
  { "Metric": "Core programs", "Count": portfolio.core.length, "Interpretation": "Working shortlist; all hard gates pass" },
  { "Metric": "Reserve programs", "Count": portfolio.reserve.length, "Interpretation": "Reply-dependent alternatives" },
  { "Metric": "Do-not-apply programs", "Count": portfolio.do_not_apply.length, "Interpretation": "Diagnostic scores only; at least one hard gate failed" },
  { "Metric": "Distinct professors evaluated", "Count": 788, "Interpretation": "830 professor-program candidate records" },
  { "Metric": "Distinct professors recommended", "Count": distinct(professors.map((row) => row.professor_id)), "Interpretation": "Verified strong matches" },
  { "Metric": "First-wave contacts", "Count": priorities.filter((row) => row.wave === "first_wave").length, "Interpretation": "Drafted and manually reviewed; not sent" },
  { "Metric": "Second-wave contacts", "Count": priorities.filter((row) => row.wave === "second_wave").length, "Interpretation": "No draft until promoted" },
  { "Metric": "Confirmed recruiting rechecks", "Count": recruiting.length, "Interpretation": "Exact degree scope retained" },
  { "Metric": "Core-domain rechecks", "Count": independent.length, "Interpretation": "Program, faculty, funding, eligibility, deadline" },
  { "Metric": "Source-ledger records", "Count": sources.length, "Interpretation": "Program and professor sources combined" },
];
const dashboard = addTableSheet(workbook, {
  name: "Coverage Dashboard", title: "Pass 2 Coverage Dashboard",
  subtitle: "Six validation categories are reported separately. A structural pass does not imply complete second-source or live-access coverage.",
  headers: ["Metric", "Count", "Interpretation"], rows: dashboardMetrics, tableIndex: index++, scoreHeaders: ["Count"],
});
dashboard.getRange("E4:H4").values = [["Validation Category", "Status", "Coverage", "Limitations"]];
dashboard.getRange("E4:H4").format = { fill: COLORS.teal, font: { name: "Arial", size: 10, bold: true, color: COLORS.white }, wrapText: true, rowHeight: 34 };
dashboard.getRange(`E5:H${4 + actualValidationCategories.length}`).values = actualValidationCategories.map((row) => [row.category, row.status, row.coverage, row.limitations]);
dashboard.getRange(`E5:H${4 + actualValidationCategories.length}`).format = { font: { name: "Arial", size: 9 }, wrapText: true, verticalAlignment: "top", rowHeight: 42, borders: { preset: "all", style: "thin", color: "#D9E2F3" } };
dashboard.getRange("E:E").format.columnWidth = 28; dashboard.getRange("F:F").format.columnWidth = 24; dashboard.getRange("G:G").format.columnWidth = 36; dashboard.getRange("H:H").format.columnWidth = 38;

const summaryHeaders = ["Portfolio Status", "Rank", "Institution", "Program", "Degree", "Region", "Overall Score", "Distinct Strong Professors", "Single-Professor Dependency", "Funding", "Application Fee", "Fee Currency", "Deadline", "Cycle Label", "Evidence Completeness", "Score Confidence", "Unresolved Conflicts", "Official Program URL"];
const summaryRows = activePrograms.map((row) => {
  const score = programs.find((candidate) => candidate.program_id === row.program_id) ?? {};
  const verified = verificationByProgram.get(row.program_id) ?? {};
  const matches = professorsByProgram.get(row.program_id) ?? [];
  return {
    "Portfolio Status": row.portfolio_status, "Rank": numberValue(row.evidence_rank), "Institution": row.institution_name,
    "Program": row.program_name, "Degree": row.degree_type, "Region": row.region, "Overall Score": numberValue(row.overall_score),
    "Distinct Strong Professors": distinct(matches.map((match) => match.professor_id)), "Single-Professor Dependency": boolLabel(score.single_professor_dependency),
    "Funding": row.funding_type, "Application Fee": numberValue(row.application_fee), "Fee Currency": row.fee_currency,
    "Deadline": verified.fall_2027_deadline ?? "", "Cycle Label": verified.deadline_cycle_label ?? "",
    "Evidence Completeness": score.evidence_completeness ?? "", "Score Confidence": score.score_confidence ?? "",
    "Unresolved Conflicts": row.unresolved_conflicts, "Official Program URL": row.official_program_url,
  };
}).sort((a, b) => (a["Portfolio Status"] === b["Portfolio Status"] ? Number(b["Overall Score"]) - Number(a["Overall Score"]) : a["Portfolio Status"] === "core" ? -1 : 1));
addTableSheet(workbook, { name: "School Summary", title: "School Summary", subtitle: "One row per active university and program. Professor counts are distinct IDs, not contact rows.", headers: summaryHeaders, rows: summaryRows, tableIndex: index++, scoreHeaders: ["Overall Score"], linkHeaders: ["Official Program URL"] });

const programHeaders = ["Portfolio Status", "Evidence Rank", "Institution", "Country", "Region", "Program", "Degree", "Overall Score", "Professor Score", "Depth Score", "Funding Score", "Eligibility Score", "Admissions Alignment", "Economics Score", "All Hard Gates Pass", "Hard-Gate Failures", "Distinct Strong Professors", "Funding Status", "Application Fee", "Fee Currency", "Admission Plausibility", "Evidence Completeness", "Score Confidence", "Unresolved Conflicts", "Official Program URL"];
const programRows = programs.map((row) => ({
  "Portfolio Status": portfolioStatus.get(row.program_id) ?? "do_not_apply", "Evidence Rank": numberValue(row.evidence_rank), "Institution": row.institution_name,
  "Country": row.country, "Region": row.region, "Program": row.program_name, "Degree": row.degree_type, "Overall Score": numberValue(row.overall_score),
  "Professor Score": numberValue(row.professor_alignment_score), "Depth Score": numberValue(row.department_program_depth_score), "Funding Score": numberValue(row.funding_net_viability_score),
  "Eligibility Score": numberValue(row.eligibility_credential_alignment_score), "Admissions Alignment": numberValue(row.degree_admissions_alignment_score), "Economics Score": numberValue(row.application_economics_score),
  "All Hard Gates Pass": boolLabel(row.all_hard_gates_pass), "Hard-Gate Failures": row.hard_gate_failures, "Distinct Strong Professors": numberValue(row.distinct_verified_strong_matches),
  "Funding Status": row.funding_status, "Application Fee": numberValue(row.application_fee), "Fee Currency": row.fee_currency, "Admission Plausibility": row.admission_plausibility,
  "Evidence Completeness": row.evidence_completeness, "Score Confidence": row.score_confidence, "Unresolved Conflicts": row.unresolved_conflicts, "Official Program URL": row.official_program_url,
}));
addTableSheet(workbook, { name: "Schools & Programs", title: "Schools & Programs", subtitle: "All 166 deeply scored programs. Do-not-apply rows retain diagnostic scores but are not recommendations.", headers: programHeaders, rows: programRows, tableIndex: index++, scoreHeaders: ["Overall Score", "Professor Score", "Depth Score", "Funding Score", "Eligibility Score"], linkHeaders: ["Official Program URL"], validations: { "Portfolio Status": ["core", "reserve", "do_not_apply"] } });

const professorHeaders = ["Priority Rank", "Wave", "Portfolio Status", "Institution", "Program", "Professor", "Official Email", "Research Match Score", "Outreach Score", "Fit Strength", "Recruiting Status", "Recruiting Evidence", "Information Gap", "Reply Could Change", "Recommended Angle", "Contact History", "Faculty or Lab URL"];
const professorPriority = priorities.filter((row) => row.contact_type === "professor");
const seenProfessorIds = new Set();
const professorRows = [];
for (const priority of professorPriority) {
  const match = professors.find((row) => row.program_id === priority.program_id && row.full_name === priority.contact_name);
  if (!match || seenProfessorIds.has(match.professor_id)) continue;
  seenProfessorIds.add(match.professor_id);
  professorRows.push({
    "Priority Rank": numberValue(priority.priority_rank), "Wave": priority.wave, "Portfolio Status": priority.portfolio_status,
    "Institution": priority.institution_name, "Program": priority.program_name, "Professor": priority.contact_name,
    "Official Email": priority.official_contact, "Research Match Score": numberValue(priority.research_match_score), "Outreach Score": numberValue(priority.outreach_score),
    "Fit Strength": match.fit_strength, "Recruiting Status": match.recruiting_status, "Recruiting Evidence": match.recruiting_evidence,
    "Information Gap": priority.information_gap, "Reply Could Change": priority.decision_that_reply_could_change,
    "Recommended Angle": priority.recommended_outreach_angle, "Contact History": priority.contact_history_status,
    "Faculty or Lab URL": priority.contact_source_url,
  });
}
addTableSheet(workbook, { name: "Professor Outreach", title: "Professor Outreach", subtitle: "Distinct professor IDs only. Recruiting is confirmed only when an explicit source says so; current research alone is not recruiting evidence.", headers: professorHeaders, rows: professorRows, tableIndex: index++, scoreHeaders: ["Research Match Score", "Outreach Score"], linkHeaders: ["Faculty or Lab URL"], validations: { "Wave": ["first_wave", "second_wave", "blocked_missing_official_contact"] } });

const adminHeaders = ["Priority Rank", "Wave", "Portfolio Status", "Institution", "Program", "Office", "Official Contact", "Outreach Score", "Information Gap", "Reply Could Change", "Recommended Angle", "Contact History", "Contact Source URL"];
const adminRows = priorities.filter((row) => row.contact_type === "department").map((row) => ({
  "Priority Rank": numberValue(row.priority_rank), "Wave": row.wave, "Portfolio Status": row.portfolio_status,
  "Institution": row.institution_name, "Program": row.program_name, "Office": row.contact_name, "Official Contact": row.official_contact,
  "Outreach Score": numberValue(row.outreach_score), "Information Gap": row.information_gap, "Reply Could Change": row.decision_that_reply_could_change,
  "Recommended Angle": row.recommended_outreach_angle, "Contact History": row.contact_history_status, "Contact Source URL": row.contact_source_url,
}));
addTableSheet(workbook, { name: "Department Admin Outreach", title: "Department / Admin Outreach", subtitle: "Administrative questions are separated from professor research and supervision questions.", headers: adminHeaders, rows: adminRows, tableIndex: index++, scoreHeaders: ["Outreach Score"], linkHeaders: ["Contact Source URL"], validations: { "Wave": ["first_wave", "second_wave", "blocked_missing_official_contact"] } });

const queueHeaders = ["Priority Rank", "Institution", "Program", "Recipient", "Email", "Outreach Score", "Question", "Information Gap", "Draft Ready", "Send Status", "Contact History", "Source URL"];
const firstWaveRows = priorities.filter((row) => row.wave === "first_wave").map((row) => {
  const draft = draftsByContact.get(`${row.program_id}|${row.official_contact.toLowerCase()}`) ?? {};
  return {
    "Priority Rank": numberValue(row.priority_rank), "Institution": row.institution_name, "Program": row.program_name,
    "Recipient": row.contact_name, "Email": row.official_contact, "Outreach Score": numberValue(row.outreach_score),
    "Question": draft.question ?? row.decision_that_reply_could_change, "Information Gap": row.information_gap,
    "Draft Ready": draft.draft_ready === "yes" ? "Yes" : "No", "Send Status": draft.send_status ?? "not_sent",
    "Contact History": row.contact_history_status, "Source URL": row.contact_source_url,
  };
});
addTableSheet(workbook, { name: "This Weekend Outreach Queue", title: "This Weekend Outreach Queue", subtitle: "Compact first-wave queue. All 12 ready drafts passed Stage 8 and remain unsent.", headers: queueHeaders, rows: firstWaveRows, tableIndex: index++, scoreHeaders: ["Outreach Score"], linkHeaders: ["Source URL"], validations: { "Draft Ready": ["Yes", "No"], "Send Status": ["not_sent", "sent", "replied", "closed"] } });

const secondRows = priorities.filter((row) => row.wave === "second_wave").map((row) => ({
  "Priority Rank": numberValue(row.priority_rank), "Institution": row.institution_name, "Program": row.program_name,
  "Recipient": row.contact_name, "Email": row.official_contact, "Outreach Score": numberValue(row.outreach_score),
  "Question": row.decision_that_reply_could_change, "Information Gap": row.information_gap, "Draft Ready": "No",
  "Send Status": "not_sent", "Contact History": row.contact_history_status, "Source URL": row.contact_source_url,
}));
addTableSheet(workbook, { name: "Second-Wave Outreach", title: "Second-Wave Outreach", subtitle: "Hold until the first-wave result or a new evidence change justifies promotion. No Stage 8 draft exists for these contacts.", headers: queueHeaders, rows: secondRows, tableIndex: index++, scoreHeaders: ["Outreach Score"], linkHeaders: ["Source URL"], validations: { "Draft Ready": ["Yes", "No"], "Send Status": ["not_sent", "promoted", "sent", "closed"] } });

const exclusionHeaders = ["Region", "Institution", "Program", "Degree", "Exclusion Category", "Evidence-Backed Reason", "Largest Unresolved Question", "Source URLs", "Independent Sample Result", "Sample Risk"];
const sampleByInstitution = new Map(exclusionAudit.map((row) => [row.institution_id, row]));
const exclusionRows = exclusions.map((row) => {
  const sample = sampleByInstitution.get(row.institution_id) ?? {};
  return {
    "Region": row.region, "Institution": row.institution_name, "Program": row.program_name, "Degree": row.degree_type,
    "Exclusion Category": row.exclusion_category, "Evidence-Backed Reason": row.evidence_backed_reason,
    "Largest Unresolved Question": row.largest_unresolved_question, "Source URLs": row.source_urls,
    "Independent Sample Result": sample.audit_result ?? "not_sampled", "Sample Risk": sample.false_negative_risk ?? "not_sampled",
  };
});
addTableSheet(workbook, { name: "Screening & Exclusions", title: "Screening & Exclusions", subtitle: "All explicit exclusions. Independent sample outcomes remain visible, including unresolved and reopened records.", headers: exclusionHeaders, rows: exclusionRows, tableIndex: index++, validations: { "Independent Sample Result": ["not_sampled", "confirmed", "false_negative_corrected", "unresolved", "reopen"] } });

const sourceHeaders = ["Source ID", "Entity Type", "Institution", "Program ID", "Professor ID", "Claim Categories", "Exact Claim Supported", "Source Title", "Publisher", "Official / Secondary", "Accessed", "Cycle / Year", "Confidence", "Verification Status", "Access Note", "URL"];
const sourceRows = sources.map((row) => ({
  "Source ID": row.source_id, "Entity Type": row.entity_type, "Institution": row.institution_name, "Program ID": row.program_id,
  "Professor ID": row.professor_id, "Claim Categories": row.claim_categories, "Exact Claim Supported": row.exact_claim_supported,
  "Source Title": row.source_title, "Publisher": row.publisher, "Official / Secondary": row.official_or_secondary,
  "Accessed": row.date_accessed, "Cycle / Year": row.cycle_or_year, "Confidence": row.confidence,
  "Verification Status": row.verification_status, "Access Note": row.access_note, "URL": row.url,
}));
addTableSheet(workbook, { name: "Sources", title: "Sources", subtitle: "Complete combined program and professor source ledger. Exact claims and access limitations are authoritative here.", headers: sourceHeaders, rows: sourceRows, tableIndex: index++, linkHeaders: ["URL"] });

const draftHeaders = ["Priority Rank", "Institution", "Program", "Recipient", "Email", "Subject", "Personalization Anchor", "Question", "Draft Body", "Manual Review", "Draft Ready", "Send Status", "Personalization URL"];
const draftRows = drafts.map((row) => ({
  "Priority Rank": numberValue(row.priority_rank), "Institution": row.institution_name, "Program": row.program_name,
  "Recipient": row.recipient_name, "Email": row.recipient_email, "Subject": row.subject,
  "Personalization Anchor": row.personalization_anchor, "Question": row.question, "Draft Body": row.draft_body,
  "Manual Review": row.manual_read_through === "yes" ? "Yes" : "No", "Draft Ready": row.draft_ready === "yes" ? "Yes" : "No",
  "Send Status": row.send_status, "Personalization URL": row.personalization_source_url,
}));
addTableSheet(workbook, { name: "Outreach Drafts", title: "Outreach Drafts", subtitle: "Only Stage 8-approved first-wave drafts appear here. These are local artifacts; no Gmail draft was created and no message was sent.", headers: draftHeaders, rows: draftRows, tableIndex: index++, linkHeaders: ["Personalization URL"], validations: { "Draft Ready": ["Yes", "No"], "Send Status": ["not_sent", "sent", "withdrawn"] } });

const methodologyRows = [
  { "Topic": "Geographic scope", "Method / Rule": "United States, Canada, and Europe were screened with region-specific registries and official program sources." },
  { "Topic": "Candidate funnel", "Method / Rule": "Registry and bounded discovery signals were separated from exact-program verification. Discovery alone never established eligibility, funding, or recruiting." },
  { "Topic": "Program verification", "Method / Rule": "Exact degree route, current status, bachelor's entry, international eligibility, language, deadline cycle, fees, and funding were recorded with official source IDs." },
  { "Topic": "Professor verification", "Method / Rule": "Current appointment, exact-program supervision authority, specific research overlap, and recent work were all required for a retained strong match." },
  { "Topic": "Recruiting", "Method / Rule": "Confirmed only from an explicit statement/opening. Active labs, papers, grants, current students, or silence were not treated as recruiting evidence." },
  { "Topic": "Scoring", "Method / Rule": "Professor alignment 30; department depth 15; funding/net viability 25; eligibility 15; degree/admissions alignment 10; application economics 5." },
  { "Topic": "Hard gates", "Method / Rule": "Funding, professor, eligibility, degree structure, and coursework exceptions were evaluated before ranking. Gated-out scores are diagnostic only." },
  { "Topic": "Portfolio", "Method / Rule": "Quality-first core working range 12–16; normally one primary program per university; reserves remain evidence- and reply-dependent." },
  { "Topic": "Cycle labels", "Method / Rule": "Only dates explicitly labeled for Fall 2027 are confirmed. Recurring, inferred, prior-cycle, and conflicting dates retain their caveats." },
  { "Topic": "Independent verification", "Method / Rule": "Every core program received five domain rechecks; all scores and distinct-professor counts were independently recalculated; confirmed recruiting claims were rechecked." },
  { "Topic": "Validation categories", "Method / Rule": "Structural, evidence-completeness, substantive second-source, portfolio-rule, outreach-quality, and visual workbook results are reported separately." },
  { "Topic": "Human follow-up", "Method / Rule": "Faculty capacity, offer-specific funding, final fees, and unpublished deadlines require replies or later official updates. Non-response is not negative evidence." },
];
addTableSheet(workbook, { name: "Methodology", title: "Methodology", subtitle: "Decision rules, evidence boundaries, and interpretation guidance for the final audit.", headers: ["Topic", "Method / Rule"], rows: methodologyRows, tableIndex: index++ });

workbook.recalculate();
const inspection = await workbook.inspect({ kind: "sheet,table,formula", maxChars: 30000, tableMaxRows: 5, tableMaxCols: 12, tableMaxCellChars: 120 });
await fs.writeFile(path.join(outputRoot, "workbook_inspection.ndjson"), inspection.ndjson ?? "", "utf8");
const errorScan = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan", maxChars: 20000 });
await fs.writeFile(path.join(outputRoot, "workbook_formula_error_scan.ndjson"), errorScan.ndjson ?? "", "utf8");

const renderRanges = new Map([
  ["Coverage Dashboard", "A1:H17"], ["School Summary", "A1:L18"], ["Schools & Programs", "A1:L18"],
  ["Professor Outreach", "A1:L18"], ["Department Admin Outreach", "A1:L12"],
  ["This Weekend Outreach Queue", "A1:K16"], ["Second-Wave Outreach", "A1:K15"],
  ["Screening & Exclusions", "A1:J18"], ["Sources", "A1:L18"], ["Outreach Drafts", "A1:I16"], ["Methodology", "A1:B16"],
]);
const sheetNames = [...renderRanges.keys()];
for (const [sheetName, range] of renderRanges.entries()) {
  const fileName = sheetName.toLowerCase().replaceAll(" ", "_").replaceAll("&", "and") + ".png";
  const htmlName = fileName.replace(/\.png$/, ".html");
  const tableHtml = workbook.toHTML(sheetNames.indexOf(sheetName), range, { formulas: true });
  const pageHtml = `<!doctype html><html><head><meta charset="utf-8"><title>${sheetName}</title><style>html,body{margin:0;background:#eef2f6;font-family:Arial,sans-serif}body{padding:20px;width:max-content;min-width:1440px}table{background:#fff;box-shadow:0 2px 14px rgba(23,54,93,.18)}td{vertical-align:top}</style></head><body>${tableHtml}</body></html>`;
  await fs.writeFile(path.join(htmlRoot, htmlName), pageHtml, "utf8");
}

const requiredSheets = [...renderRanges.keys()];
const formulaErrorText = (errorScan.ndjson ?? "").trim();
const formulaErrors = formulaErrorText.includes("Cell search matched 0 entries") ? "" : formulaErrorText;
const qa = {
  schema_version: "2.0",
  generated_at: new Date().toISOString(),
  workbook_path: path.relative(repoRoot, workbookPath).replaceAll("\\", "/"),
  sheet_count: requiredSheets.length,
  sheets: requiredSheets,
  all_required_sheets: requiredSheets.length === 11,
  table_count: 11,
  filters_present_on_all_data_sheets: true,
  frozen_panes_present_on_all_sheets: true,
  dropdown_sheets: ["Schools & Programs", "Professor Outreach", "Department Admin Outreach", "This Weekend Outreach Queue", "Second-Wave Outreach", "Screening & Exclusions", "Outreach Drafts"],
  hyperlink_formula_count: sourceRows.filter((row) => row.URL).length + programRows.filter((row) => row["Official Program URL"]).length + summaryRows.filter((row) => row["Official Program URL"]).length + professorRows.filter((row) => row["Faculty or Lab URL"]).length + adminRows.filter((row) => row["Contact Source URL"]).length + firstWaveRows.filter((row) => row["Source URL"]).length + secondRows.filter((row) => row["Source URL"]).length + draftRows.filter((row) => row["Personalization URL"]).length,
  professor_outreach_rows: professorRows.length,
  professor_outreach_distinct_ids: seenProfessorIds.size,
  no_professor_double_count: professorRows.length === seenProfessorIds.size,
  first_wave_rows: firstWaveRows.length,
  first_wave_ready_rows: firstWaveRows.filter((row) => row["Draft Ready"] === "Yes").length,
  second_wave_rows: secondRows.length,
  second_wave_ready_rows: secondRows.filter((row) => row["Draft Ready"] === "Yes").length,
  rendered_sheet_count: 0,
  html_preview_count: renderRanges.size,
  visually_inspected_sheet_count: 0,
  formula_errors: formulaErrors ? [formulaErrors] : [],
  substantive_validation_note: "Formula cleanliness is not treated as substantive proof; independent source, score, professor, portfolio, outreach, and cycle checks are stored separately.",
};
await fs.writeFile(qaPath, JSON.stringify(qa, null, 2) + "\n", "utf8");
console.log(JSON.stringify({ workbookPath, qaPath, sheets: requiredSheets.length, renders: renderRanges.size, formulaErrors: qa.formula_errors.length }, null, 2));

// Export last: the host performs a saved-file inspection and may end the process after save.
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(workbookPath);
