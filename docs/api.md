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

```
GET /check?url=https://www.commerce.alaska.gov/web/aogcc/&export=markdown&token=your_key
```
