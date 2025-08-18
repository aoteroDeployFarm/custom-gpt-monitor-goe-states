# 🚀 preflight.md – Local Setup & Run Instructions (macOS)

    This guide ensures your environment is ready to run the GOE Regulatory Monitor project locally on macOS.

## ✅ Prerequisites
* macOS system with terminal access
* Python 3.7+ installed (python3 --version)
* Git installed
* A clone of this repo on your machine

1. 🧱 Project Structure
    This assumes the repository is cloned and looks like:
```
custom-gpt-monitor-goe-states/
├── app/
│   ├── scraper.py        # Scraper CLI/logic
│   └── api.py            # Optional FastAPI server
├── config/
│   └── state_urls.json   # Regulatory links for all 50 states
├── requirements.txt
└── ...
```

2. 🐍 Set Up Python Environment
Option A — Use system Python (simplest)
Run:
```
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Option B — Use a virtual environment (recommended)
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. ✅ Make scraper.py Executable
Ensure the first line of app/scraper.py contains:
```
#!/usr/bin/env python3
```

Then run:
```
chmod +x app/scraper.py
```

Now you can run it directly:
```
./app/scraper.py
```

4. 🔍 Run the Scraper
Run with default URL in script:
```
./app/scraper.py
```

OR check a specific URL:
```
python3 app/scraper.py https://www.commerce.alaska.gov/web/aogcc/
```

This will:
* Fetch the page
* Hash the content
* Compare it to the last saved version
* Return a result (whether it changed or not)
* Cache the hash in .cache/
* Optionally write results to .csv or .md

```
uvicorn app.api:app --reload
```

Then visit:
* Swagger UI: http://localhost:8000/docs
* Check example:
```
curl "http://localhost:8000/check?url=https://www.commerce.alaska.gov/web/aogcc/"
```

If using token protection:
```
export API_KEY=your_secret_key
```

Then add ?token=your_secret_key to each request.

6. 📄 Generate Tree Structure (Optional)
If you want to verify the directory structure:
```
tree -I '__pycache__|.venv' > tree.md
```

7. 🐳 Docker Option (Optional)
Build and run with Docker:
```
docker-compose up --build
```