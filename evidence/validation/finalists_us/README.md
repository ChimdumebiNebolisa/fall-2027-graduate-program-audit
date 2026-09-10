# U.S. finalist independent validation

This pass treats `outputs/20260909-fall2027-audit/portfolio.json` as immutable. The file contained 18 current core programs at validation time; Maryland had already been moved to reserve after its official FAQ disclosed that admission does not include a funding guarantee. The audit therefore covers the 18 current core rows plus Maryland as the displaced former-core row, for the requested 19-program comparison.

Each program row compares a primary official program/admissions page with a distinct official university, school, department, catalog, funding, or faculty-hosted page. A `qualified` result preserves a plausible route while explicitly retaining a condition, missing cycle label, offer-specific term, or unresolved coverage detail. A `conflict` identifies an actionable correction. Faculty activity was never treated as recruiting evidence unless an official page explicitly advertised a position.

The five exclusion samples span GPA interpretation, department-wide versus lab-specific funding, advisor dependence, possible unfunded admission, and last-60-hour GPA/funding uncertainty. Search results were used only to locate official pages; the cited official pages were opened and checked on 2026-09-09.

Run:

```powershell
python evidence/validation/finalists_us/build_validation.py
python evidence/validation/finalists_us/verify_validation.py
```
