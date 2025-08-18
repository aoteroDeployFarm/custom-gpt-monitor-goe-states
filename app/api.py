#!/usr/bin/env python3

from fastapi import FastAPI, Query, HTTPException, Request, Depends
from typing import Optional, List
from app.scraper import check_url, check_state, CONFIG_PATH
import json
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
    version="1.3.0"
)

# Optional API key protection
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

@app.get("/", summary="Health check", tags=["Health"])
def root():
    return {"status": "ok", "message": "GOE Regulatory Monitor API is running."}


@app.get("/api/check", summary="Check a URL, a state, or all URLs", tags=["Scraper"])
def api_check(
    state: Optional[str] = Query(None, description="State to filter by (e.g. Texas)"),
    url: Optional[str] = Query(None, description="Specific URL to check"),
    only_updated: bool = Query(False, description="Only return updated results"),
    export: Optional[str] = Query(None, description="Export format: json, csv, markdown"),
    filter_tag: Optional[str] = Query(None, description="Comma-separated tags to include"),
    exclude_tag: Optional[str] = Query(None, description="Comma-separated tags to exclude"),
    auth: bool = Depends(verify_token)
):
    filter_tags = [t.strip().lower() for t in filter_tag.split(",")] if filter_tag else None
    exclude_tags = [t.strip().lower() for t in exclude_tag.split(",")] if exclude_tag else None

    with open(CONFIG_PATH, "r") as f:
        all_data = json.load(f)

    results = []

    if url and state:
        logger.info(f"🔍 Checking specific URL: {url} in state={state}")
        result = check_url(url, state)
        result["tags"] = []
        results.append(result)
    elif state:
        logger.info(f"🔍 Checking state: {state} (tags={filter_tags}, exclude={exclude_tags})")
        entries = all_data.get(state)
        if not entries:
            raise HTTPException(status_code=404, detail=f"No URLs found for state: {state}")
        results = check_state(state, entries, only_updated, filter_tags, exclude_tags)
    else:
        logger.info(f"🔍 Checking ALL states (tags={filter_tags}, exclude={exclude_tags})")
        for st, entries in all_data.items():
            state_results = check_state(st, entries, only_updated, filter_tags, exclude_tags)
            results.extend(state_results)

    return {
        "count": len(results),
        "results": results
    }


@app.post("/batch-check", summary="Batch check multiple URLs", tags=["Batch"])
def batch_check(
    urls: List[str],
    export: Optional[str] = Query("json", description="Export format: json, csv, or markdown"),
    auth: bool = Depends(verify_token)
):
    logger.info(f"📦 Batch checking {len(urls)} URLs")
    results = []
    for url in urls:
        try:
            result = check_url(url)
            results.append(result)
        except Exception as e:
            logger.error(f"❌ Error checking {url}: {e}")
            results.append({"url": url, "error": str(e)})
    return {"results": results}


@app.get("/api/tags", summary="Get all available tags", tags=["Scraper"])
def get_all_tags(auth: bool = Depends(verify_token)):
    """
    Returns a list of all unique tags currently defined in state_urls.json
    """
    with open(CONFIG_PATH, "r") as f:
        all_data = json.load(f)

    tag_set = set()
    for entries in all_data.values():
        for entry in entries:
            if isinstance(entry, dict) and "tags" in entry:
                tag_set.update([t.lower() for t in entry["tags"]])

    return {"tags": sorted(tag_set)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
