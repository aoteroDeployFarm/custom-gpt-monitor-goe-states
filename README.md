# 🛢️ Regulatory Monitor Scraper

A modular Python project that tracks and monitors regulatory data across oil, gas, and energy websites in all 50 U.S. states. It supports both **command-line** and **API access**, and is designed to integrate with **OpenAI Custom GPTs** via Actions (OpenAPI 3.1.0).

---

## 🚀 Features

- 🔍 Scrape hundreds of government regulatory URLs by state
- 🧠 Detect changes using SHA256-based content hashing
- 🧾 Export results in JSON, CSV, or Markdown
- 🧪 Run manually, via cron, or as an API
- 🤖 Integrate with GPTs via OpenAPI-defined custom actions

---

## ⚙️ Installation

```bash
git clone https://github.com/aoteroDeployFarm/custom-gpt-monitor-goe-states.git
cd custom-gpt-monitor-goe-states

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
````

---

## 🧪 Usage (CLI)

```bash
python app/scraper.py                         # Check all states
python app/scraper.py --state Texas           # Check one state
python app/scraper.py --url https://... --state Texas
python app/scraper.py --state Texas --export csv
python app/scraper.py --state Texas --export markdown
python app/scraper.py --only-updated          # Only export changed URLs
```

---

## 🌐 API Mode (via FastAPI)

Run the service locally:

```bash
uvicorn app.api:app --reload --port 8000
```

### Example Endpoints

* `GET /api/check`
* `GET /api/check?state=Texas`
* `GET /api/check?url=https://...`

---

## 🤖 GPT Integration (via Actions)

1. Deploy the API (Render, Railway, Fly.io, etc.)
2. Register the OpenAPI spec at `openapi/openapi.yaml` via GPT builder
3. Use prompts like:

   > "Check for updates in Alaska's oil and gas regulations."

---

## 📄 Output Format

Each record looks like this:

```json
{
  "state": "Alaska",
  "url": "https://www.commerce.alaska.gov/web/aogcc/",
  "updated": true,
  "checkedAt": "2025-08-17T18:30:00Z",
  "summary": "Change detected"
}
```

---

## 🧼 Caching

* All scraped content is hashed with SHA256 and stored in `.cache/`
* Reduces unnecessary network requests and false positives
* `.cache/mapping.json` maps hashes to URLs + state

---

## 📅 Automate It (Optional)

Run daily with cron:

```bash
crontab -e
# Run at 2am daily
0 2 * * * /path/to/venv/bin/python /path/to/custom-gpt-monitor-goe-states/app/scraper.py
```

---

## 🐳 Docker Usage (Optional)

### 🔨 Build the Docker image

```bash
docker build -t regulatory-monitor .
```

### ▶️ Run the container

```bash
docker run -p 8000:8000 regulatory-monitor
```

Visit:

* [http://localhost:8000/api/check](http://localhost:8000/api/check)
* [http://localhost:8000/api/check?state=Texas](http://localhost:8000/api/check?state=Texas)

---

## 🧱 Docker Compose

Start the app:

```bash
docker-compose up --build
```

Stop the app:

```bash
docker-compose down
```

### Visit the API:

* 📡 [http://localhost:8000](http://localhost:8000)
* 📡 [http://localhost:8000/api/check?url=https://www.commerce.alaska.gov/web/aogcc/](http://localhost:8000/api/check?url=https://www.commerce.alaska.gov/web/aogcc/)

---

## 📦 .dockerignore (Optional)

```dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.cache/
results/
.env
.venv/
.DS_Store
```

---

## 📁 Project Directory Structure

```text
custom-gpt-monitor-goe-states/
├── app/
│   ├── __init__.py
│   ├── api.py               # FastAPI app
│   └── scraper.py           # Core scraper
├── config/
│   └── state_urls.json      # Source config: all 50 states
├── openapi/
│   └── openapi.yaml         # GPT Action spec
├── results/
│   └── state/
│       └── <State>/
│           ├── json/
│           ├── csv/
│           ├── md/
│           ├── diff/
│           └── content/
├── .cache/                  # Content hashes + mapping.json
│   └── mapping.json
├── scripts/
│   ├── setup.sh
│   ├── generate_mapping.py
│   ├── lookup_hash.py
│   └── baseline_commit_all.sh
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── NOTES.md
```

---

## 📡 API Endpoints Overview

| Endpoint               | Description                   |
| ---------------------- | ----------------------------- |
| `GET /`                | Health check                  |
| `GET /check`           | Run scraper on all URLs       |
| `GET /check?state=...` | Scrape all URLs for a state   |
| `GET /check?url=...`   | Scrape one URL manually       |
| `POST /batch-check`    | Check multiple URLs (planned) |

> See [`docs/api.md`](docs/api.md) for full OpenAPI schema

---

## 🛠️ Roadmap

* [x] Per-state tracking
* [x] JSON/CSV/Markdown exports
* [x] Git-based baseline + commits
* [x] Reverse lookup from SHA → URL
* [ ] Slack/email alerts
* [ ] HTML/text diff viewer
* [ ] Database support (SQLite or Postgres)
* [ ] Frontend dashboard

---

## 👨‍💻 Contributing

Pull requests welcome!
Please fork, branch, and submit a PR.

---

## 📄 License

MIT License © Fabing Productions

---

## 🙋 Questions?

* Open an issue
* Start a discussion on GitHub
