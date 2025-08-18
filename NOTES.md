# 📝 Project Notes & Roadmap — Regulatory Monitor

*Custom GPT + API system for tracking regulatory changes across all 50 U.S. states.*

---

## ✅ Completed Milestones

### 🔖 Tagging & Metadata

* ✅ Added support for `tags` in `state_urls.json`
* ✅ Updated `scraper.py` to include `tags` in all output formats
* ✅ Built `auto_tag_urls.py` to infer tags via keyword matching
* ✅ Added `--preserve` flag to avoid overwriting manual tags
* ✅ Implemented error logging in tagging script
* ✅ Confirmed tags flow through CLI + exports
* ✅ Implemented `--filter-tag` and `--exclude-tag` flags for CLI filtering
* ✅ Added tag filtering support in FastAPI `/api/check`

---

### 📊 Reporting & Dashboarding

* ✅ Generated per-tag summary as Markdown: `results/tag_summary.md`
* ✅ Aggregates tag count by state and tag
* ✅ CLI-ready and easy to rerun

---

### 📄 Output, Caching, and Hashing

* ✅ SHA256-based diff detection for each URL
* ✅ `.cache/` structure storing previous content
* ✅ `mapping.json` file tracking hash ➝ URL + state
* ✅ `lookup_hash.py` reverse-lookup CLI tool
* ✅ Clean separation of `results/`:

  * `json`, `csv`, `markdown` per state
  * `diff/`, `content/`, and date-based file naming

---

### 🔧 Baseline & Export Control

* ✅ Full `scraper.py` CLI support:

  * `--state`, `--url`, `--export`, `--only-updated`
  * `--filter-tag`, `--exclude-tag`
* ✅ Git-automated `baseline_commit_all.sh`

  * Auto-commits each state after success
  * Skips completed states via `.baseline-progress.log`
  * Supports `--full` export mode
* ✅ Error-resistant file naming + slug creation
* ✅ Pre-checks for existing dirs, ensures clean structure

---

### 🌐 API / GPT Integration

* ✅ Added `/api/check` with query param support for:

  * `state`, `url`, `only_updated`, `filter_tag`, `exclude_tag`
* ✅ Added `/api/tags` to return all known tags
* ✅ Added `token` support (optional API key)
* ✅ API logs all requests and responses
* ✅ `/batch-check` for POSTing multiple URLs
* ✅ OpenAPI 3.1.0 spec defined in `openapi/openapi.yaml`
* ✅ Grouped endpoints with tags: Health, Scraper, Batch
* ✅ `tags` field included in API and OpenAPI responses

---

## 🛠️ In Progress / Optional Enhancements

### 📊 Tag Summary Enhancements

* [ ] Export tag summary to:

  * [ ] CSV
  * [ ] HTML (for web dashboard)
* [ ] Global view: total tag counts across all states

---

### 📤 Notifications

* [ ] Slack or Discord webhooks on update
* [ ] Email summary (e.g., via SendGrid or Mailgun)
* [ ] Attach `diffSummary` or actual `.diff` files

---

### 📅 Automation

* [ ] Add GitHub Actions `.yml` to run scraper daily
* [ ] Auto-export and auto-commit changes per state
* [ ] Summary report posted to GitHub Discussions or sent via webhook

---

### 📁 Optional Data Enhancements

* [ ] Add `description` field per URL
* [ ] Maintain per-state update history (JSON or DB)
* [ ] Long-term tracking via SQLite or flatfile db
* [ ] Add `/api/states` endpoint to list all configured states

---

## 🧪 Testing (Future Optional)

* [ ] Add unit tests for `check_url()`, `export_results()`, CLI args
* [ ] Mock URL fetches to simulate change/no-change
* [ ] Add test cases for mapping and hashing

---

## 🔁 How to Contribute

* Track new TODOs here
* Fork & PR welcome!
* Ask for help structuring new features

---

📅 Last Updated: **2025-08-18**
