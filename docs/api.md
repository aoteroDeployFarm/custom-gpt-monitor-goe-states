# 🧠 Regulatory Monitor API – Full Documentation

Track and monitor regulatory page content across all 50 U.S. states for the oil, gas, and energy sectors.

Built with [FastAPI](https://fastapi.tiangolo.com), this API wraps scraper logic into REST endpoints for easy integration with GPT Actions or external systems.

---

## 📡 Endpoints

### 🔹 `GET /` — Health Check

Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "GOE Regulatory Monitor API is running."
}
```

### 🔹 GET /check — Check a Single URL

* Scrape a single regulatory URL and check if its content has changed since the last run.
* Query Parameters:
| Name     | Type   | Required | Description                                         |
| -------- | ------ | -------- | --------------------------------------------------- |
| `url`    | string | ✅ yes    | Full URL to check                                   |
| `export` | string | optional | Format: `json` (default), `csv`, or `markdown`      |
| `token`  | string | optional | API key (required only if `API_KEY` env var is set) |

### Example

```
GET /check?url=https://www.commerce.alaska.gov/web/aogcc/&export=markdown&token=your_key
```

### Response:
```
{
  "url": "https://www.commerce.alaska.gov/web/aogcc/",
  "updated": true,
  "lastChecked": "2025-08-17T17:00:00Z",
  "diffSummary": "AOGCC homepage content changed"
}
```
---

### 🔹 POST /batch-check — Batch Check Multiple URLs
    Send a JSON array of URLs to check multiple regulatory pages in one request.
    Query Parameters:

| Name     | Type   | Required | Description                                         |
| -------- | ------ | -------- | --------------------------------------------------- |
| `export` | string | optional | Format: `json` (default), `csv`, or `markdown`      |
| `token`  | string | optional | API key (required only if `API_KEY` env var is set) |

### Request Body (JSON):
```
{
  "urls": [
    "https://www.commerce.alaska.gov/web/aogcc/",
    "https://www.epa.gov/npdes-permits/alaska-npdes-permits"
  ]
}
```

### Example:
```
curl -X POST "http://localhost:8000/batch-check?export=json&token=your_key" \
     -H "Content-Type: application/json" \
     -d '{"urls": ["https://site1.com", "https://site2.com"]}'
```

### Response:
```
{
  "results": [
    {
      "url": "https://site1.com",
      "updated": false,
      "lastChecked": "2025-08-17T17:00:00Z",
      "diffSummary": "No change detected"
    },
    {
      "url": "https://site2.com",
      "updated": true,
      "lastChecked": "2025-08-17T17:00:00Z",
      "diffSummary": "Content changed"
    }
  ]
}
```
---

### 🔐 Authentication (Optional)
    If you set an environment variable:
```
export API_KEY=your_secret_key
```
Then all endpoints require ?token=your_secret_key as a query parameter.
If API_KEY is not set, authentication is disabled.

---

### ⚙️ Export Formats
  * json: Standard JSON response
  * csv: Also writes to results/last_run.csv
  * markdown: Also writes to results/last_run.md

---

### 🧪 Local Testing
* Start the server:
```
uvicorn app.api:app --reload
```
* Try:
```
curl "http://localhost:8000/check?url=https://www.commerce.alaska.gov/web/aogcc/"
```

* Or:
```
curl -X POST http://localhost:8000/batch-check \
     -H "Content-Type: application/json" \
     -d '{"urls": ["https://site1.com", "https://site2.com"]}'
```

### 🐳 Docker Testing
    Use docker-compose.yml:
```
docker-compose up --build
```

    Then access the API at:
```
http://localhost:8000

```
---

### ✅ Status Summary
| Endpoint       | Method | Description          |
| -------------- | ------ | -------------------- |
| `/`            | GET    | Health check         |
| `/check`       | GET    | Single URL check     |
| `/batch-check` | POST   | Batch check for URLs |

---

### 🧩 Built With
  * FastAPI
  * Uvicorn
  * Requests
  * BeautifulSoup4
