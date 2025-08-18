#!/usr/bin/env python3

from fastapi import FastAPI, Query, HTTPException, Request, Depends
from typing import Optional, List
from app.scraper import check_for_update
import uvicorn
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("regulatory-monitor")

# Load API key from environment
API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="GOE Regulatory Monitor API",
    description="Track and monitor regulatory data changes across all U.S. states in the energy, oil, and gas sectors.",
    version="1.1.0"
)

# Dependency to enforce optional API key auth
def verify_token(token: Optional[str] = Query(None, alias="token")):
    if API_KEY and token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API token.")
    return True

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response status: {response.status_code}")
    return response

@app.get("/check", summary="Check a URL for content updates")
def check(
    url: str = Query(..., description="The full URL of the regulatory page to check."),
    export: Optional[str] = Query("json", description="Output format: json, csv, or markdown"),
    auth: bool = Depends(verify_token)
):
    logger.info(f"🔍 Checking URL: {url} (format={export})")
    result = check_for_update(url, export)
    logger.info(f"✅ Result: updated={result['updated']}")
    return result

@app.post("/batch-check", summary="Batch check multiple URLs")
def batch_check(
    urls: List[str],
    export: Optional[str] = Query("json", description="Output format: json, csv, or markdown"),
    auth: bool = Depends(verify_token)
):
    logger.info(f"🔍 Batch checking {len(urls)} URLs (format={export})")
    results = []
    for url in urls:
        try:
            result = check_for_update(url, export)
            logger.info(f"✅ {url} => updated={result['updated']}")
            results.append(result)
        except Exception as e:
            logger.error(f"❌ Error checking {url}: {e}")
            results.append({"url": url, "error": str(e)})
    return {"results": results}

@app.get("/", summary="Health check")
def root():
    return {"status": "ok", "message": "GOE Regulatory Monitor API is running."}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
