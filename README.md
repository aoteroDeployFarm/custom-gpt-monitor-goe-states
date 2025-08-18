# 🛢️ Regulatory Monitor Scraper

A modular Python project that tracks and monitors regulatory data across oil, gas, and energy websites in all 50 U.S. states. It supports both **command-line** and **API access**, and is designed to integrate with **OpenAI Custom GPTs** via Actions (OpenAPI 3.1.0).

---

## 🚀 Features

- 🔍 **Scrape** hundreds of government regulatory URLs by state
- 🧠 **Detect changes** via hash-based comparison
- 🧾 **Export results** in JSON, CSV, or Markdown format
- 🧪 **Run manually**, by cron, or as an API server
- 🤖 **Integrate with GPTs** via OpenAPI-defined action

---

## 🗂️ Project Directory Structure
---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/regulatory-monitor.git
   
   cd regulatory-monitor
   
   python3 -m venv venv
   source venv/bin/activate
   
   pip install -r requirements.txt

## 🧪 Usage
    Run the scraper via command line:
    
    python app/scraper.py                   # Check all states
    python app/scraper.py --state Texas     # Check one state
    python app/scraper.py --url https://... --state Texas
    python app/scraper.py --format csv      # Output CSV
    python app/scraper.py --format md       # Output Markdown

## 🌐 API Mode

    Run as a FastAPI service:
    uvicorn app.api:app --reload --port 8000
    GET /api/check
    GET /api/check?state=Texas
    GET /api/check?url=https://...

## 🤖 GPT Integration (via Actions)
    1. Deploy the API using Render, Railway, Fly.io, etc.
    2. Register the OpenAPI spec in openapi/openapi.yaml via the GPT Builder.
    3. Prompt the GPT like:
       1. "Check for updates in Alaska's oil and gas regulations."

## 📄 Output Format
    Each record looks like:
        {
          "state": "Alaska",
          "url": "https://www.commerce.alaska.gov/web/aogcc/",
          "updated": true,
          "checkedAt": "2025-08-17T18:30:00Z",
          "summary": "Change detected"
        }

## 📅 Automate It (Optional)
    To run daily with cron:

    crontab -e
    # Run at 2am daily
    0 2 * * * /path/to/venv/bin/python /path/to/regulatory-monitor/app/scraper.py

## 🧼 Caching
    * All previously scraped content is hashed (SHA256) and stored in .cache/
    * Prevents false positives on unchanged pages
    * URL content hashes are stored per URL in .cache/
    * This prevents false positives and unnecessary rescanning

## 🛠️ Roadmap
    * Slack/email alert integration
    * HTML/text diff support
    * Docker support for easier deployment
    * Database to track long-term change history
    * Frontend dashboard for monitoring

## 🐳 (Optional) Docker Usage
    Coming soon! A Dockerfile can be added to simplify deployments. Ask if you'd like it now.

## 👨‍💻 Contributing
    Pull requests welcome! Fork the repo, create a branch, and submit a PR.

## 📄 License
    MIT License © Fabing Productions

## 🙋 Questions?
   * Open an issue
   * Start a discussion    
## 📁 Project Directory Structure

```
custom-gpt-monitor-goe-state/
├── app
│   ├── __init__.py
│   ├── api.py
│   └── scraper.py
├── config
│   └── state_urls.json
├── Dockerfile
├── init_project.sh
├── NOTES.md
├── openapi
│   └── openapi.yaml
├── README.md
├── requirements.txt
├── results
│   ├── last_run.csv
│   ├── last_run.json
│   └── last_run.md
├── scripts
│   └── setup.sh
└── setup.sh

6 directories, 15 files
```
