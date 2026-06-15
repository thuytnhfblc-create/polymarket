# Weekly Prediction Market Literature Monitor

## Overview

This project automatically monitors newly published academic papers related to prediction markets.

### Workflow

1. Search OpenAlex and Crossref for predefined keywords.
2. Remove duplicates.
3. Filter results to high-quality journals and recognized working paper series.
4. Compare results against the existing paper database.
5. Identify newly discovered papers.
6. Fill missing abstracts using Gemini (optional).
7. Update the master database (`data/papers.csv`).
8. Generate a weekly digest report (`reports/`).

---

## Keywords

Current keywords include:

* Prediction Markets
* Prediction Market
* Polymarket
* Kalshi
* Event Contracts
* Forecasting Markets
* Information Aggregation Markets

To modify the search scope, edit:

```text
src/config.py
```

---

## Quality Filters

The script only keeps papers from selected journals and working paper series.

Examples include:

* Journal of Finance
* Journal of Financial Economics
* Review of Financial Studies
* American Economic Review
* Quarterly Journal of Economics
* Econometrica
* NBER Working Papers
* CEPR Discussion Papers
* BIS Working Papers
* SSRN

To modify the filtering rules, edit:

```text
src/database.py
```

---

## Gemini Abstract Completion

If a paper is missing an abstract, the script can use Gemini to retrieve one automatically.

The API key should be stored as:

```text
GEMINI_API_KEY
```

If no API key is provided, the script skips this step and continues normally.

---

## Weekly Automatic Updates

The main script is:

```text
run_weekly.py
```

To run automatically every week, the repository must be hosted on GitHub and include a GitHub Actions workflow (e.g. `.github/workflows/weekly_update.yml`).

The workflow should:

* Run `run_weekly.py` weekly.
* Use the repository secret `GEMINI_API_KEY`.
* Commit updated files (`data/papers.csv` and `reports/`) back to the repository.

Once configured, no manual intervention is required.

---

## Notes

* OpenAlex and Crossref are queried through their public APIs.
* Duplicate detection uses DOI when available and falls back to title matching.
* Gemini usage is optional.
* The paper database grows incrementally over time.
* Reports contain only newly discovered papers from the current run.

---

## Maintenance

Common modifications:

* Add/remove keywords → `src/config.py`
* Change journal filters → `src/database.py`
* Modify report format → `src/report.py`
* Modify data sources → `src/search_sources.py`
