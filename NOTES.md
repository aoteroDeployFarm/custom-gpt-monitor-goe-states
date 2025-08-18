# 📝 Project Notes & Roadmap — Regulatory Monitor

This document tracks next steps, features in progress, and enhancement ideas for the custom GPT-powered state regulatory monitor.

---

## 🚀 Suggested Next Steps

### 🔖 Tagging & Metadata

- [ ] Add support for `tags` or `type` in `state_urls.json`
  - Example: `"tags": ["air", "permits", "drilling"]`
- [ ] Update scraper to include tags in results
- [ ] Use tags to filter or group output in CLI/API

> 💡 Use tags for advanced GPT prompts, dashboard grouping, or selective monitoring.

---

### 📊 Markdown/HTML Dashboard View

- [ ] Generate a per-state summary table:
  - State name
  - Total sites
  - Updated count
  - Last check timestamp
- [ ] Export to `results/dashboard.md` or `results/dashboard.html`
- [ ] Optional: hyperlink to full results or diffs

> 💡 Use this for internal review or stakeholder reports.

---

### 📤 Notification System

- [ ] Integrate email alerts (SMTP or Mailgun)
- [ ] Support Slack/Discord/webhook push notifications
- [ ] Notify only on updates (diff detected)
- [ ] Include `state`, `url`, and diff summary

> 💡 Helpful for real-time regulatory change tracking.

---

### 🧪 Testing & Reliability

- [ ] Add unit tests for:
  - `extract_content()`
  - `check_url()`
  - `export_results()`
- [ ] Add CLI test coverage (arg parsing, dry runs)
- [ ] Add tests for mapping + hash lookups

> 💡 Use `pytest` and `unittest.mock` to simulate fetches.

---

### 📅 Scheduled Automation

- [ ] Create a GitHub Actions workflow:
  - Run daily or hourly
  - Commit results automatically
- [ ] Add cron examples to README
- [ ] Auto-generate status summary on schedule

---

## 🔧 Infrastructure / Enhancements (Future Ideas)

### 🛢️ Database Integration (Optional)

- Store all change history over time
- Allow rollback or diff across date ranges
- SQLite or Postgres recommended

### 📁 Results Index File

- [ ] Maintain a central index of all exports
  - `results/state_index.json`
  - List last update time, exported files, URLs checked

### 🔍 Search CLI Tool

- [ ] CLI command to search for:
  - URLs by tag
  - Most recently updated sites
  - Sites without diffs yet

### 🧠 GPT Prompt Templates (Bonus)

- [ ] Generate templated prompts like:
  - “Summarize changes in environmental permits for Texas”
  - “What changed in air quality rules in California this week?”

---

## ✅ Completed Milestones

- [x] Scraper CLI with full per-state export
- [x] JSON, CSV, and Markdown output support
- [x] Per-state diff + content archiving
- [x] SHA256 caching for change detection
- [x] Git commit + push per state via shell script
- [x] `.cache/mapping.json` with reverse lookup
- [x] Docker + Compose setup
- [x] OpenAPI + GPT Actions integration
- [x] `lookup_hash.py` CLI tool

---

## 🙋 Ideas? Feedback?

If you'd like to brainstorm or prioritize next features:
- Open an issue
- Drop a TODO in this file
- We can work together from here!

