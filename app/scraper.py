#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import json
import csv
from datetime import datetime
from pathlib import Path
import difflib

# === Constants ===
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / ".cache"
CONFIG_PATH = BASE_DIR / "config" / "state_urls.json"
RESULTS_DIR = BASE_DIR / "results"
URL_MAP_FILE = CACHE_DIR / "urlmap.json"

# === Setup cache directory and URL map ===
os.makedirs(CACHE_DIR, exist_ok=True)
if not URL_MAP_FILE.exists():
    with open(URL_MAP_FILE, "w") as f:
        json.dump({}, f)

# === Utility Functions ===

def fetch_html(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def extract_content(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("main") or soup.find("div", id="content") or soup.find("div", class_="row")
    return content.get_text(strip=True) if content else soup.get_text()

def compute_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_url_hash(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()

def get_last_content(url_hash, content_dir):
    content_path = content_dir / f"{url_hash}.txt"
    return content_path.read_text(encoding="utf-8") if content_path.exists() else None

def save_content(url_hash, content, content_dir):
    os.makedirs(content_dir, exist_ok=True)
    with open(content_dir / f"{url_hash}.txt", "w", encoding="utf-8") as f:
        f.write(content)

def save_diff(url_hash, old_content, new_content, diff_dir):
    os.makedirs(diff_dir, exist_ok=True)
    diff = list(difflib.unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        fromfile='before.txt',
        tofile='after.txt',
        lineterm=""
    ))
    if diff:
        with open(diff_dir / f"{url_hash}.diff", "w", encoding="utf-8") as f:
            f.write("\n".join(diff))
        return "\n".join(diff[:5]) + ("\n..." if len(diff) > 5 else "")
    return "No significant differences."

def update_url_map(url_hash, url):
    with open(URL_MAP_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if url_hash not in data:
            data[url_hash] = url
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def get_all_state_urls():
    with open(CONFIG_PATH) as f:
        return json.load(f)

# === Main Logic ===

def check_for_update(url, state=None):
    url_hash = get_url_hash(url)
    update_url_map(url_hash, url)

    state_folder = state.lower().replace(" ", "_") if state else "general"
    content_dir = RESULTS_DIR / state_folder / "content"
    diff_dir = RESULTS_DIR / state_folder / "diff"

    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(diff_dir, exist_ok=True)

    try:
        html = fetch_html(url)
        content = extract_content(html)
        old_content = get_last_content(url_hash, content_dir)
        diff_summary = None

        if old_content:
            if old_content != content:
                diff_summary = save_diff(url_hash, old_content, content, diff_dir)
                updated = True
            else:
                updated = False
                diff_summary = "No change detected"
        else:
            updated = True
            diff_summary = "Initial snapshot (no previous content)"

        save_content(url_hash, content, content_dir)

        return {
            "url": url,
            "state": state,
            "updated": updated,
            "lastChecked": datetime.utcnow().isoformat() + "Z",
            "diffSummary": diff_summary
        }

    except Exception as e:
        return {
            "url": url,
            "state": state,
            "updated": False,
            "lastChecked": datetime.utcnow().isoformat() + "Z",
            "error": str(e)
        }

def export_results(results, export_format="json", state=None, url=None):
    now = datetime.utcnow().strftime("%Y-%m-%d")
    state_folder = (state or "general").lower().replace(" ", "_")
    export_dir = RESULTS_DIR / state_folder / export_format.lower()
    os.makedirs(export_dir, exist_ok=True)

    if state and not url:
        filename = f"{state_folder}-{now}.{export_format}"
    elif state and url:
        filename = f"all_websites-{now}.{export_format}"
    else:
        filename = f"{now}.{export_format}"

    filepath = export_dir / filename

    if export_format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    elif export_format == "csv":
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            keys = {k for result in results for k in result.keys()}
            writer = csv.DictWriter(f, fieldnames=sorted(keys))
            writer.writeheader()
            writer.writerows(results)
    elif export_format in ["markdown", "md"]:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("| URL | Updated | Last Checked | State | Summary |\n")
            f.write("|-----|---------|---------------|--------|---------|\n")
            for r in results:
                f.write(
                    f"| {r.get('url')} | {'✅ Yes' if r.get('updated') else '❌ No'} "
                    f"| {r.get('lastChecked')} | {r.get('state') or ''} "
                    f"| {r.get('diffSummary', '')[:60]}... |\n"
                )
    print(f"📁 Exported: {filepath}")

# === CLI ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor regulatory site changes.")
    parser.add_argument("--state", help="State to check (e.g. Texas)")
    parser.add_argument("--url", help="Single URL to check")
    parser.add_argument("--export", choices=["json", "csv", "markdown", "md"], default="json", help="Export format")
    parser.add_argument("--only-updated", action="store_true", help="Export only updated results")
    args = parser.parse_args()

    export_format = args.export.lower()

    results = []

    if args.url:
        results.append(check_for_update(args.url, state=args.state))
        export_results(results, export_format=export_format, state=args.state, url=args.url)
    elif args.state:
        print(f"🔎 Checking all URLs for {args.state}...")
        all_states = get_all_state_urls()
        state_urls = all_states.get(args.state)
        if not state_urls:
            print(f"❌ No URLs found for state: {args.state}")
        else:
            for url in state_urls:
                results.append(check_for_update(url, state=args.state))
            if args.only_updated:
                results = [r for r in results if r.get("updated")]
            export_results(results, export_format=export_format, state=args.state)
    else:
        print("🔁 Scanning all states...")
        all_states = get_all_state_urls()
        for state, urls in all_states.items():
            print(f"📡 {state} ({len(urls)} URLs)...")
            state_results = [check_for_update(url, state=state) for url in urls]
            if args.only_updated:
                state_results = [r for r in state_results if r.get("updated")]
            if state_results:
                export_results(state_results, export_format=export_format, state=state)
