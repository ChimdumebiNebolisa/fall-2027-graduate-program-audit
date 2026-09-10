import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const COLORS = {
  navy: "#17365D",
  blue: "#4F81BD",
  paleBlue: "#DCE6F1",
  gray: "#E7E6E6",
  darkGray: "#595959",
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
  return rows.slice(1).filter(r => r.some(v => v !== "")).map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
}

async function csvRows(filePath) {
  try { return parseCSV(await fs.readFile(filePath, "utf8")); }
  catch (error) { if (error.code === "ENOENT") return []; throw error; }
}

function numberValue(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : value ?? "";
}

function columnName(index) {
  let n = index + 1, result = "";
  while (n > 0) { n -= 1; result = String.fromCharCode(65 + (n % 26)) + result; n = Math.floor(n / 26); }
  return result;
}

function cleanName(name) { return name.replace(/[^A-Za-z0-9]/g, "").slice(0, 24); }

function addTableSheet(workbook, { name, title, subtitle, headers, rows, tableIndex, validations = {}, scoreHeaders = [] }) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.tabColor = COLORS.blue;
  const lastCol = columnName(Math.max(headers.length - 1, 0));
  sheet.getRange(`A1:${lastCol}1`).merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format = { fill: COLORS.navy, font: { name: "Arial", size: 14, bold: true, color: COLORS.white }, rowHeight: 26, verticalAlignment: "center" };
  sheet.getRange(`A2:${lastCol}2`).merge();
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange("A2").format = { fill: COLORS.paleBlue, font: { name: "Arial", size: 10, color: COLORS.darkGray }, wrapText: true, rowHeight: 28, verticalAlignment: "center" };
  const matrix = [headers, ...rows.map(row => headers.map(h => row[h] ?? ""))];
  sheet.getRangeByIndexes(3, 0, matrix.length, headers.length).values = matrix;
  const header = sheet.getRangeByIndexes(3, 0, 1, headers.length);
  header.format = { fill: COLORS.blue, font: { name: "Arial", size: 10, bold: true, color: COLORS.white }, wrapText: true, rowHeight: 30, verticalAlignment: "center" };
  if (rows.length) {
    const data = sheet.getRangeByIndexes(4, 0, rows.length, headers.length);
    data.format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "top", borders: { preset: "all", style: "thin", color: "#D9E2F3" } };
    sheet.tables.add(`A4:${lastCol}${4 + rows.length}`, true, `Audit${String(tableIndex).padStart(2, "0")}${cleanName(name)}`);
  }
  sheet.freezePanes.freezeRows(4);
  sheet.freezePanes.freezeColumns(Math.min(2, headers.length));
  headers.forEach((h, index) => {
    const maxLen = Math.max(h.length, ...rows.slice(0, 250).map(row => String(row[h] ?? "").length));
    let width = Math.min(42, Math.max(11, Math.ceil(maxLen * 0.85)));
    if (/Explanation|Infrastructure|Funding Model|Scholarships|Risk|Question|Notes|Why|Evidence|Research Areas|Draft|Outcome|Rationale|Source/i.test(h)) width = 38;
    if (/URL|Email/i.test(h)) width = 28;
    sheet.getRangeByIndexes(3, index, Math.max(1, rows.length + 1), 1).format.columnWidth = width;
  });
  for (const [headerName, values] of Object.entries(validations)) {
    const index = headers.indexOf(headerName);
    if (index >= 0 && rows.length) sheet.getRangeByIndexes(4, index, rows.length, 1).dataValidation = { rule: { type: "list", values } };
  }
  for (const scoreHeader of scoreHeaders) {
    const index = headers.indexOf(scoreHeader);
    if (index >= 0 && rows.length) sheet.getRangeByIndexes(4, index, rows.length, 1).conditionalFormats.add("colorScale", { minColor: "#F8696B", midColor: "#FFEB84", maxColor: "#63BE7B" });
  }
  return sheet;
}

function project(rows, mapping) {
  return rows.map(row => Object.fromEntries(mapping.map(([label, field, transform]) => [label, transform ? transform(row[field], row) : row[field] ?? ""])));
}

async function main() {
  const outputRoot = path.resolve(process.argv[2] ?? "outputs/20260909-fall2027-audit");
  const workbookPath = path.resolve(process.argv[3] ?? path.join(outputRoot, "graduate_program_audit.xlsx"));
  const renderRoot = path.join(outputRoot, "renders");
  await fs.mkdir(renderRoot, { recursive: true });
  const [programs, professors, exclusions, sources, admins, calendar, drafts] = await Promise.all([
    csvRows(path.join(outputRoot, "program_screening.csv")),
    csvRows(path.join(outputRoot, "professor_evidence.csv")),
    csvRows(path.join(outputRoot, "exclusion_log.csv")),
    csvRows(path.join(outputRoot, "source_ledger.csv")),
    csvRows(path.join(outputRoot, "admin_contacts.csv")),
    csvRows(path.join(outputRoot, "calendar_comparison.csv")),
    csvRows(path.join(outputRoot, "outreach_drafts.csv")),
  ]);
  const manifest = JSON.parse(await fs.readFile(path.join(outputRoot, "run_manifest.json"), "utf8"));
  const validation = JSON.parse(await fs.readFile(path.join(outputRoot, "validation.json"), "utf8"));
  const portfolio = JSON.parse(await fs.readFile(path.join(outputRoot, "portfolio.json"), "utf8"));
  const reviewed = programs.filter(row => !["", "mechanical", "preliminary"].includes((row.verification_status ?? "").toLowerCase()));
  const retained = programs.filter(row => (row.screening_decision ?? "").toLowerCase() === "retained");
  const recommended = professors.filter(row => ["first wave", "first-wave", "high"].includes((row.outreach_priority ?? "").toLowerCase()));
  const workbook = Workbook.create();
  let tableIndex = 1;

  const dashboard = workbook.worksheets.add("COVERAGE DASHBOARD");
  dashboard.showGridLines = false;
  dashboard.tabColor = COLORS.navy;
  dashboard.getRange("A1:H1").merge();
  dashboard.getRange("A1").values = [["Fall 2027 Graduate Program Discovery & Fit Audit"]];
  dashboard.getRange("A1").format = { fill: COLORS.navy, font: { name: "Arial", size: 14, bold: true, color: COLORS.white }, rowHeight: 28, verticalAlignment: "center" };
  dashboard.getRange("A2:H2").merge();
  dashboard.getRange("A2").values = [[`Evidence date ${manifest.current_date}; validation ${validation.status}. Mechanical screens and deep reviews are counted separately.`]];
  dashboard.getRange("A2").format = { fill: COLORS.paleBlue, font: { name: "Arial", size: 10, color: COLORS.darkGray }, rowHeight: 24 };
  const counts = manifest.counts ?? {};
  const metrics = [
    ["Coverage metric", "Count"],
    ["Institutions indexed", counts.institutions_indexed ?? 0],
    ["Institutions with relevant fields", Object.entries(counts.by_institution_status ?? {}).filter(([k]) => ["preliminary_fit", "deep_review", "retained"].includes(k)).reduce((s, [,v]) => s + Number(v), 0)],
    ["Programs screened", programs.length],
    ["Programs deeply reviewed", reviewed.length],
    ["Programs retained", retained.length],
    ["Programs excluded", programs.filter(r => ["excluded", "screened_out", "do_not_apply"].includes((r.screening_decision ?? "").toLowerCase())).length],
    ["Professors evaluated", professors.length],
    ["Professors recommended", recommended.length],
    ["First-wave contacts", Math.min(15, recommended.length + admins.filter(r => (r.priority ?? "").toLowerCase().includes("first")).length)],
    ["Source claims", sources.length],
    ["Blocked/unverified institutions", Number((counts.by_institution_status ?? {}).indexed ?? 0) + Number((counts.by_institution_status ?? {}).program_screened_out ?? 0)],
  ];
  dashboard.getRange(`A4:B${3 + metrics.length}`).values = metrics;
  dashboard.getRange("A4:B4").format = { fill: COLORS.blue, font: { name: "Arial", bold: true, color: COLORS.white } };
  dashboard.getRange(`A5:B${3 + metrics.length}`).format = { font: { name: "Arial", size: 10 }, borders: { preset: "all", style: "thin", color: "#D9E2F3" } };
  const regionCounts = [["Region", "Institutions"], ["United States", programs.length ? 2107 : 0], ["Canada", 98], ["Europe/UK", 3628]];
  dashboard.getRange("D4:E7").values = regionCounts;
  dashboard.getRange("D4:E4").format = { fill: COLORS.blue, font: { name: "Arial", bold: true, color: COLORS.white } };
  const reasonCounts = new Map();
  for (const row of exclusions) reasonCounts.set(row.primary_exclusion_reason || "Unspecified", (reasonCounts.get(row.primary_exclusion_reason || "Unspecified") ?? 0) + 1);
  const topReasons = [...reasonCounts.entries()].sort((a,b) => b[1] - a[1]).slice(0, 8);
  dashboard.getRange(`G4:H${4 + topReasons.length}`).values = [["Top exclusion reason", "Count"], ...topReasons];
  dashboard.getRange("G4:H4").format = { fill: COLORS.blue, font: { name: "Arial", bold: true, color: COLORS.white } };
  dashboard.getRange("A18:H18").merge();
  dashboard.getRange("A18").values = [[`Datasets: IPEDS 2024/25 provisional; IRCC/CICIC accessed ${manifest.current_date}; ROR v2.10. Europe ROR API fallback coverage: 81.31%.`]];
  dashboard.getRange("A18").format = { fill: COLORS.gray, font: { name: "Arial", size: 10, italic: true }, wrapText: true, rowHeight: 34 };
  dashboard.freezePanes.freezeRows(2);
  dashboard.getRange("A:H").format.font = { name: "Arial", size: 10 };
  dashboard.getRange("A:A").format.columnWidth = 34; dashboard.getRange("B:B").format.columnWidth = 12;
  dashboard.getRange("D:D").format.columnWidth = 24; dashboard.getRange("E:E").format.columnWidth = 12;
  dashboard.getRange("G:G").format.columnWidth = 44; dashboard.getRange("H:H").format.columnWidth = 12;
  if (metrics.length > 2) { const chart = dashboard.charts.add("bar", dashboard.getRange(`A4:B${3 + metrics.length}`)); chart.title = "Audit funnel"; chart.hasLegend = false; chart.setPosition("J3", "Q18"); }
  if (topReasons.length) { const chart = dashboard.charts.add("bar", dashboard.getRange(`G4:H${4 + topReasons.length}`)); chart.title = "Leading exclusion reasons"; chart.hasLegend = false; chart.setPosition("J20", "Q36"); }

  const schoolHeaders = ["University","Stable Institution ID","Country","Program","Degree Type","Department","Program Priority","Research Fit Score","Professor Fit Score","Faculty Depth Score","Funding Score","Eligibility Score","Overall Score","Research Fit Explanation","Relevant Courses or Research Infrastructure","Direct-from-Bachelor’s Eligible","International Eligible","Minimum GPA","English Requirement or Waiver","Admissions Model","Faculty Contact Expectation","Fall 2027 Deadline","Deadline Cycle Status","Funding Model","Stipend","Funding Duration","Tuition Coverage","Fees and Insurance Coverage","Summer Funding","PhD Funding","Master’s Funding","Scholarships and Fellowships","Application Fee","Fee Waiver Possibility","Multiple Applications Allowed","Official Program URL","Current Status","Recommended Action","Final Decision","Biggest Risk","Unresolved Question","Notes"];
  const schoolMap = [
    ["University","institution_name"],["Stable Institution ID","institution_id"],["Country","country"],["Program","program_name"],["Degree Type","degree_type"],["Department","department"],["Program Priority","recommendation"],
    ["Research Fit Score","research_fit_score",numberValue],["Professor Fit Score","professor_fit_score",numberValue],["Faculty Depth Score","faculty_depth_score",numberValue],["Funding Score","funding_score",numberValue],["Eligibility Score","eligibility_score",numberValue],["Overall Score","overall_score",numberValue],
    ["Research Fit Explanation","preliminary_fit"],["Relevant Courses or Research Infrastructure","research_groups_labs"],["Direct-from-Bachelor’s Eligible","direct_from_bachelors_eligible"],["International Eligible","international_student_eligible"],["Minimum GPA","minimum_gpa"],["English Requirement or Waiver","english_requirement_waiver"],["Admissions Model","admissions_model"],["Faculty Contact Expectation","faculty_contact_expectation"],["Fall 2027 Deadline","fall_2027_deadline"],["Deadline Cycle Status","deadline_cycle_status"],["Funding Model","funding_model"],["Stipend","stipend_amount",(v,r)=>[v,r.stipend_currency].filter(Boolean).join(" ")],["Funding Duration","funding_duration_years"],["Tuition Coverage","tuition_coverage"],["Fees and Insurance Coverage","mandatory_fee_coverage",(v,r)=>[v,r.health_insurance_coverage].filter(Boolean).join("; ")],["Summer Funding","summer_funding"],["PhD Funding","phd_funding"],["Master’s Funding","masters_funding"],["Scholarships and Fellowships","scholarships_fellowships"],["Application Fee","application_fee",(v,r)=>[v,r.fee_currency].filter(Boolean).join(" ")],["Fee Waiver Possibility","fee_waiver_rules"],["Multiple Applications Allowed","multiple_applications_allowed"],["Official Program URL","official_program_url"],["Current Status","verification_status"],["Recommended Action","recommendation"],["Final Decision","final_decision"],["Biggest Risk","biggest_risk"],["Unresolved Question","unresolved_question"],["Notes","notes"]
  ];
  addTableSheet(workbook,{name:"SCHOOLS & PROGRAMS",title:"Schools & Programs",subtitle:"Deeply reviewed programs only. Funding and eligibility are hard gates; older deadlines retain their actual cycle label.",headers:schoolHeaders,rows:project(reviewed,schoolMap),tableIndex:tableIndex++,validations:{"Final Decision":["Apply","Reserve","Monitor","Do Not Apply","Pending"]},scoreHeaders:["Research Fit Score","Professor Fit Score","Faculty Depth Score","Funding Score","Eligibility Score","Overall Score"]});

  const professorHeaders = ["Outreach Priority","University","Program","Professor","Department","Faculty Position","Appointment Status","Can Supervise This Program?","Research Areas","Why They Fit Me","Fit Strength","Relevant Paper or Project","Paper or Project URL","Publication Year","Sustained Research Evidence","Recruiting Evidence","Recruiting Status","Prospective-Student Instructions","Contacting Faculty Appropriate?","Official Email","Faculty or Lab URL","Already Contacted?","Last Contact Date","Previous Outcome","Recommended Outreach Angle","Specific Question or Goal","Date Contacted","Response Status","Follow-Up Date","Outcome","Notes"];
  const professorMap = [["Outreach Priority","outreach_priority"],["University","institution_name"],["Program","program_name"],["Professor","full_name"],["Department","department"],["Faculty Position","faculty_position"],["Appointment Status","appointment_status"],["Can Supervise This Program?","can_supervise_program"],["Research Areas","research_themes"],["Why They Fit Me","fit_explanation"],["Fit Strength","fit_strength"],["Relevant Paper or Project","recent_work_1"],["Paper or Project URL","recent_work_1_url"],["Publication Year","recent_work_1_year"],["Sustained Research Evidence","sustained_research_evidence"],["Recruiting Evidence","recruiting_evidence"],["Recruiting Status","recruiting_status"],["Prospective-Student Instructions","prospective_student_instructions"],["Contacting Faculty Appropriate?","contacting_faculty_appropriate"],["Official Email","official_email"],["Faculty or Lab URL","official_faculty_url"],["Already Contacted?","already_contacted"],["Last Contact Date","last_contact_date"],["Previous Outcome","previous_outcome"],["Recommended Outreach Angle","recommended_outreach_angle"],["Specific Question or Goal","specific_question_goal"],["Date Contacted","date_contacted"],["Response Status","response_status"],["Follow-Up Date","follow_up_date"],["Outcome","outcome"],["Notes","notes"]];
  addTableSheet(workbook,{name:"PROFESSOR MATCHES",title:"Professor Matches",subtitle:"Current appointments and supervision authority are checked; recruiting remains unknown unless a current explicit statement/opening exists.",headers:professorHeaders,rows:project(professors,professorMap),tableIndex:tableIndex++,validations:{"Already Contacted?":["Yes","No"],"Response Status":["Not sent","Sent","Replied","No reply","Closed"]}});

  const adminHeaders = ["Priority","University","Program","Department","Contact Name","Contact Role","Official Email","Question to Resolve","Why It Matters","Already Contacted?","Date Contacted","Response","Follow-Up Date","Outcome","Notes"];
  addTableSheet(workbook,{name:"DEPARTMENT AND ADMIN OUTREACH",title:"Department & Admin Outreach",subtitle:"Administrative questions are kept separate from professor research/supervision questions.",headers:adminHeaders,rows:admins.map(r=>Object.fromEntries(adminHeaders.map(h=>[h,r[h]??r[h.toLowerCase().replaceAll(" ","_")]??""]))),tableIndex:tableIndex++,validations:{"Already Contacted?":["Yes","No"]}});

  const bestByInstitution = new Map();
  for (const row of reviewed) { const prior=bestByInstitution.get(row.institution_id); if (!prior || Number(row.overall_score||0)>Number(prior.overall_score||0)) bestByInstitution.set(row.institution_id,row); }
  const professorByInstitution = new Map();
  for (const row of professors) { if (!professorByInstitution.has(row.institution_id)) professorByInstitution.set(row.institution_id,[]); professorByInstitution.get(row.institution_id).push(row); }
  const summaryHeaders=["University","Best Program","Best Alternative Program","Overall Score","Research Fit","Funding Strength","Admission Plausibility","Best Professor Match","Number of Strong Faculty Matches","Single-Professor Dependency?","Biggest Positive","Biggest Risk","Biggest Unresolved Question","Application Fee","Fee Waiver Potential","Application Deadline","Previous Calendar Status","New Recommendation","Recommendation Rationale"];
  const summaryRows=[...bestByInstitution.values()].sort((a,b)=>Number(b.overall_score||0)-Number(a.overall_score||0)).map(row=>{const faculty=(professorByInstitution.get(row.institution_id)||[]).sort((a,b)=>Number(b.outreach_score||0)-Number(a.outreach_score||0)); const alts=reviewed.filter(r=>r.institution_id===row.institution_id&&r.program_id!==row.program_id); const cal=calendar.find(c=>c.existing_calendar_school===row.institution_name); return {"University":row.institution_name,"Best Program":row.program_name,"Best Alternative Program":alts[0]?.program_name??"","Overall Score":numberValue(row.overall_score),"Research Fit":row.preliminary_fit,"Funding Strength":row.funding_status,"Admission Plausibility":row.admission_plausibility,"Best Professor Match":faculty[0]?.full_name??"","Number of Strong Faculty Matches":faculty.filter(f=>["Direct","Strong","Exceptional"].includes(f.fit_strength)).length,"Single-Professor Dependency?":row.single_professor_dependency,"Biggest Positive":row.notes,"Biggest Risk":row.biggest_risk,"Biggest Unresolved Question":row.unresolved_question,"Application Fee":[row.application_fee,row.fee_currency].filter(Boolean).join(" "),"Fee Waiver Potential":row.fee_waiver_rules,"Application Deadline":row.fall_2027_deadline,"Previous Calendar Status":cal?.previous_category??"Not found in bounded Calendar search","New Recommendation":row.recommendation,"Recommendation Rationale":row.recommendation_rationale??row.preliminary_fit};});
  addTableSheet(workbook,{name:"SCHOOL SUMMARY",title:"School Summary",subtitle:"One row per deeply reviewed university, using its highest-scoring compatible route.",headers:summaryHeaders,rows:summaryRows,tableIndex:tableIndex++,scoreHeaders:["Overall Score"]});

  const queueHeaders=["Rank","Person","University","Program","Professor or Admin","Why Contact Them Now","What This Contact Resolves","Email Address","Prior Contact?","Draft Ready?","Send Status","Date Sent","Follow-Up Date","Result"];
  const queue=[];
  for(const p of recommended){queue.push({"Person":p.full_name,"University":p.institution_name,"Program":p.program_name,"Professor or Admin":"Professor","Why Contact Them Now":p.recommended_outreach_angle,"What This Contact Resolves":p.specific_question_goal,"Email Address":p.official_email,"Prior Contact?":p.already_contacted||"No","Draft Ready?":drafts.some(d=>d.recipient_email===p.official_email)?"Yes":"No","Send Status":"Not sent","Date Sent":"","Follow-Up Date":"","Result":"","_score":Number(p.outreach_score||0)});}
  for(const a of admins){if((a.Priority??a.priority??"").toLowerCase().includes("first")){queue.push({"Person":a["Contact Name"]??a.contact_name??"Graduate program","University":a.University??a.university??"","Program":a.Program??a.program??"","Professor or Admin":"Admin","Why Contact Them Now":a["Why It Matters"]??a.why_it_matters??"","What This Contact Resolves":a["Question to Resolve"]??a.question_to_resolve??"","Email Address":a["Official Email"]??a.official_email??"","Prior Contact?":a["Already Contacted?"]??a.already_contacted??"No","Draft Ready?":drafts.some(d=>d.recipient_email===(a["Official Email"]??a.official_email))?"Yes":"No","Send Status":"Not sent","Date Sent":"","Follow-Up Date":"","Result":"","_score":70});}}
  queue.sort((a,b)=>b._score-a._score); queue.slice(0,15).forEach((row,i)=>row.Rank=i+1);
  addTableSheet(workbook,{name:"THIS WEEKEND OUTREACH QUEUE",title:"This Weekend Outreach Queue",subtitle:"Ranked by information value, research fit, supervisor/funding dependence, uncertainty, and contact appropriateness. Nothing has been sent.",headers:queueHeaders,rows:queue.slice(0,15),tableIndex:tableIndex++,validations:{"Send Status":["Not sent","Ready","Sent","Do not send"]}});

  const draftHeaders=["Rank","University","Program","Recipient","Recipient Email","Subject","Personalization Anchor","Draft"];
  const draftRows=drafts.map((d,i)=>({"Rank":numberValue(d.rank||i+1),"University":d.university,"Program":d.program,"Recipient":d.recipient,"Recipient Email":d.recipient_email,"Subject":d.subject,"Personalization Anchor":d.personalization_anchor,"Draft":d.body||d.draft}));
  addTableSheet(workbook,{name:"OUTREACH DRAFTS",title:"Outreach Drafts",subtitle:"First-wave drafts only. Review and send manually if desired; no Gmail draft was created.",headers:draftHeaders,rows:draftRows,tableIndex:tableIndex++});

  const exclusionHeaders=["Stable Institution ID","Institution","Country","Program","Stage of Exclusion","Primary Exclusion Reason","Supporting Evidence","Source URL","Confidence","Manual Verification","Date Checked"];
  const meaningful=exclusions.filter(r=>r.program_id||["institution universe","program screen","deep review"].includes((r.stage_of_exclusion||"").toLowerCase())).slice(0,1000);
  const exclusionMap=[["Stable Institution ID","institution_id"],["Institution","institution_name"],["Country","country"],["Program","program_name"],["Stage of Exclusion","stage_of_exclusion"],["Primary Exclusion Reason","primary_exclusion_reason"],["Supporting Evidence","supporting_evidence"],["Source URL","source_url"],["Confidence","confidence"],["Manual Verification","manual_verification"],["Date Checked","date_checked"]];
  addTableSheet(workbook,{name:"SCREENING AND EXCLUSIONS",title:"Screening & Exclusions",subtitle:`Meaningful screening rows (up to 1,000) are shown here; the complete ${exclusions.length.toLocaleString()}-row exclusion log is in exclusion_log.csv.`,headers:exclusionHeaders,rows:project(meaningful,exclusionMap),tableIndex:tableIndex++});

  const calendarHeaders=["Existing Calendar School","Previous Category","Survived New Audit?","New Status","Change","Reason","Contradictory Calendar Instructions"];
  const calendarMap=[["Existing Calendar School","existing_calendar_school"],["Previous Category","previous_category"],["Survived New Audit?","survived_new_audit"],["New Status","new_status"],["Change","change"],["Reason","reason"],["Contradictory Calendar Instructions","contradictory_calendar_instructions"]];
  addTableSheet(workbook,{name:"CALENDAR COMPARISON",title:"Calendar Comparison",subtitle:"Read-only comparison. Calendar inclusion was treated as prior context, not as an application decision; no events were modified.",headers:calendarHeaders,rows:project(calendar,calendarMap),tableIndex:tableIndex++});

  const deepIds=new Set(reviewed.map(r=>r.institution_id));
  const sourceRows=sources.filter(r=>deepIds.has(r.institution_id)||["dataset","coverage","registry"].includes((r.claim_type||"").toLowerCase())).slice(0,1500);
  const sourceHeaders=["Source ID","Stable Institution ID","University","Program or Professor","Claim Type","Exact Claim Supported","Source Title","Publisher","Publication Date","URL","Source Type","Official or Secondary","Date Accessed","Admissions Cycle","Confidence","Verification Status","Access Note"];
  const sourceMap=[["Source ID","source_id"],["Stable Institution ID","institution_id"],["University","institution_name"],["Program or Professor","program_or_professor"],["Claim Type","claim_type"],["Exact Claim Supported","exact_claim_supported"],["Source Title","source_title"],["Publisher","publisher"],["Publication Date","publication_date"],["URL","url"],["Source Type","source_type"],["Official or Secondary","official_or_secondary"],["Date Accessed","date_accessed"],["Admissions Cycle","admissions_cycle"],["Confidence","confidence"],["Verification Status","verification_status"],["Access Note","access_note"]];
  addTableSheet(workbook,{name:"SOURCES",title:"Sources",subtitle:`Condensed finalist and registry ledger (${sourceRows.length.toLocaleString()} rows shown); the complete ${sources.length.toLocaleString()}-row source_ledger.csv is authoritative.`,headers:sourceHeaders,rows:project(sourceRows,sourceMap),tableIndex:tableIndex++});

  const methodRows=[
    {Topic:"Geographic scope",Method:"United States; Canada; EU-27 including Ireland; United Kingdom; Norway; Switzerland; Iceland."},
    {Topic:"Structured sources",Method:"IPEDS; IRCC DLI; CICIC; ROR v2.10; national higher-education authorities; official university catalogues/pages."},
    {Topic:"Scholarly discovery",Method:"OpenAlex searches covering 2022 through the evidence date; discovery signals were rechecked on official appointment/program pages."},
    {Topic:"Screening stages",Method:"Registry universe → mechanical field/program screen → research-fit discovery → program/faculty/funding/eligibility verification → hard gates → scoring → independent recheck."},
    {Topic:"Scoring rubric",Method:"Professor fit 30; department depth 15; funding 25; eligibility 15; degree/admissions alignment 10; application economics 5."},
    {Topic:"Hard gates",Method:"Recognized active institution, relevant research program, international eligibility, bachelor's entry or research master's route, verified supervisor, credible funding/full scholarship, compatible degree."},
    {Topic:"Recruiting status",Method:"Confirmed only with a current explicit statement or opening. Active lab/recent paper is not recruiting proof; silence remains unknown."},
    {Topic:"Funding definition",Method:"Assistantships existing is insufficient. Normal funding requires credible tuition and stipend/salary evidence; international-rate gaps remain explicit."},
    {Topic:"Admissions plausibility",Method:"Qualitative categories only; no admission probabilities, ranking inference, or anecdotal-profile comparisons."},
    {Topic:"Deadlines",Method:"Fall 2027 dates are used only when published. Older/current standing dates are labeled by their actual cycle/status."},
    {Topic:"Known gaps",Method:"Europe ROR API fallback captured 81.31% of the reported filtered set; EHESO required authorization; blocked pages and unresolved Canadian crosswalks are manifested."},
    {Topic:"Privacy",Method:"Calendar/Gmail checks were bounded and read-only. No Calendar event changed, no Gmail draft created, and no email sent."},
  ];
  addTableSheet(workbook,{name:"METHODOLOGY",title:"Methodology",subtitle:"Decision rules and evidence limitations for interpreting the audit.",headers:["Topic","Method"],rows:methodRows,tableIndex:tableIndex++});

  workbook.recalculate();
  const inspection = await workbook.inspect({kind:"sheet,table,formula",maxChars:12000,tableMaxRows:4,tableMaxCols:8,tableMaxCellChars:80});
  await fs.writeFile(path.join(outputRoot,"workbook_inspection.ndjson"),inspection.ndjson||"","utf8");
  const errorScan = await workbook.inspect({kind:"match",search:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:500},maxChars:12000});
  await fs.writeFile(path.join(outputRoot,"workbook_formula_error_scan.ndjson"),errorScan.ndjson||"","utf8");
  for (const name of ["COVERAGE DASHBOARD","SCHOOLS & PROGRAMS","PROFESSOR MATCHES","DEPARTMENT AND ADMIN OUTREACH","SCHOOL SUMMARY","THIS WEEKEND OUTREACH QUEUE","OUTREACH DRAFTS","SCREENING AND EXCLUSIONS","CALENDAR COMPARISON","SOURCES","METHODOLOGY"]) {
    const blob = await workbook.render({sheetName:name,autoCrop:"all",scale:0.65,format:"png"});
    await fs.writeFile(path.join(renderRoot,`${name.toLowerCase().replaceAll(" ","_").replaceAll("&","and")}.png`),new Uint8Array(await blob.arrayBuffer()));
  }
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(workbookPath);
  console.log(JSON.stringify({workbookPath,sheets:11,reviewedPrograms:reviewed.length,professors:professors.length,renderRoot},null,2));
}

main().catch(error=>{console.error(error);process.exit(1);});
