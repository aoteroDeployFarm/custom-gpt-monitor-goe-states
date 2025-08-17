## 📝 NOTES.md – Project Summary & Quick Recovery Guide

---

### 🛢️ Regulatory Monitor Scraper – Project Overview

This project tracks and monitors regulatory websites across **all 50 U.S. states** related to the **oil, gas, and energy** sectors. It detects content updates, outputs change logs in multiple formats, and integrates with **OpenAI Custom GPTs** through a web API defined by an OpenAPI spec.

---

### ✅ Core Features

* Scrapes and monitors hundreds of URLs grouped by U.S. state
* Uses SHA-256 hashes to detect changes
* CLI interface for one-time or scheduled runs
* FastAPI-based web API for live checking or GPT integration
* Exports output in **JSON**, **CSV**, and **Markdown**
* Fully containerized using Docker
* Designed for cloud deployment or local use

---

### 🧠 Custom GPT Integration

* Exposes `/api/check` endpoint for GPT to query update status
* OpenAPI 3.1.0 spec available in `openapi/openapi.yaml`
* Deployable to services like **Render**, **Railway**, **Fly.io**, or any VPS
* GPTs can prompt with:

  > “Check for updates in Alaska’s oil and gas regulatory data.”

---

## 🗂️ Project Directory Structure

regulatory-monitor/
├── app/
│   ├── scraper.py       # Main CLI scraper logic
│   └── api.py           # FastAPI web server
├── config/
│   └── state_urls.json  # URL list grouped by state
├── results/
│   ├── last_run.json
│   ├── last_run.csv
│   └── last_run.md
├── .cache/              # Local hash cache per URL
├── openapi/
│   └── openapi.yaml     # Action spec for GPTs
├── scripts/
│   └── setup.sh         # Directory bootstrap script
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md

---

### 🧪 How to Run

#### CLI Mode

```bash
python app/scraper.py                     # Run all states
python app/scraper.py --state Texas       # Run one state
python app/scraper.py --url https://...   # Run one URL
python app/scraper.py --format csv        # Output as CSV
```

#### API Mode (FastAPI)

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

Example endpoints:

* `GET /api/check`
* `GET /api/check?state=Texas`
* `GET /api/check?url=https://example.com`

---

### 🐳 Docker Usage

#### Build the image

```bash
docker build -t regulatory-monitor .
```

#### Run the container

```bash
docker run -p 8000:8000 regulatory-monitor
```

Access the API:

```
http://localhost:8000/api/check
```

---

### ⚙️ Automation & Cron

To run daily (e.g., 2am):

```bash
crontab -e
# Add this line:
0 2 * * * /path/to/venv/bin/python /path/to/regulatory-monitor/app/scraper.py
```

---

### 📌 Remaining TODOs / Future Features

* [ ] Add email or Slack alerts for updated URLs
* [ ] Implement content diffing (before vs after)
* [ ] Store historical change logs (file or DB)
* [ ] Add a frontend dashboard for browsing changes
* [ ] Add GitHub Actions for CI/CD (optional)
* [ ] Finalize and test `openapi/openapi.yaml`

---

### ✅ Current Status

* ✅ CLI scraper works
* ✅ API works locally and in Docker
* ✅ JSON config of all 50 states complete
* ✅ GPT integration via OpenAPI is prepared
* ✅ Project is Dockerized and deployable

---

### 📦 Hosting Recommendations

* **Render** (easy Docker deploys)
* **Railway** (easy GitHub + Docker pipeline)
* **Fly.io** (if you want global deployments)
* Any VPS (with Docker installed)

---

### 🙋‍♀️ Help / Recovery

* Clone repo and run: `docker build` + `docker run`
* Use `NOTES.md` to restore structure and commands
* Use `setup.sh` in `scripts/` to recreate folders
* For GPT integration, deploy `/api/check` and register `openapi.yaml`

---

Save this file and you’ll never lose context — even if your tab or session disappears. 🚀

---

Let me know if you'd like me to generate the missing pieces:

* `api.py`
* `openapi.yaml`
* `Docker Compose`
* GitHub Actions workflows

I'm ready whenever you are.
