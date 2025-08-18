#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import argparse
import json
from datetime import datetime
import csv
from difflib import unified_diff
from urllib.parse import urlparse

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/state_urls.json")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "../.cache")

def fetch_html(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"[ERROR] {str(e)}"

def extract_content(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("main") or soup.find("div", id="content") or soup.find("div", class_="row")
    return content.get_text(strip=True) if content else soup.get_text()

def compute_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_cache_path(url):
    hashed = compute_hash(url)
    return os.path.join(CACHE_DIR, f"{hashed}.txt")

def load_last_content(url):
    path = get_cache_path(url)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_current_content(url, content):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = get_cache_path(url)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def slugify_url(url):
    parsed = urlparse(url)
    return parsed.netloc.replace(".", "_") + parsed.path.replace("/", "_")

def export_results(results, export_format="json", state=None, url=None):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    base_dir = os.path.join("results", "state", state or "general")
    format_dir = os.path.join(base_dir, export_format)
    os.makedirs(format_dir, exist_ok=True)

    if state and url:
        filename = f"{slugify_url(url)}_{now}.{export_format}"
    elif state:
        filename = f"{state}_{now}.{export_format}"
    else:
        filename = f"all_websites_{now}.{export_format}"

    filepath = os.path.join(format_dir, filename)

    if export_format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    elif export_format == "markdown":
        with open(filepath, "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"## {r.get('url')}\n")
                f.write(f"- Updated: {r.get('updated')}\n")
                f.write(f"- Last Checked: {r.get('lastChecked')}\n")
                f.write(f"- Summary: {r.get('diffSummary')}\n\n")
    elif export_format == "csv":
        keys = ["url", "updated", "lastChecked", "diffSummary"]
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)

def check_url(url, state=None):
    html = fetch_html(url)
    if html.startswith("[ERROR]"):
        return {
            "url": url,
            "updated": False,
            "lastChecked": datetime.utcnow().isoformat() + "Z",
            "error": html
        }

    content = extract_content(html)
    prev_content = load_last_content(url)

    updated = content != prev_content
    if updated:
        save_current_content(url, content)

    diff_summary = "Updated" if updated else "No change detected"
    result = {
        "url": url,
        "updated": updated,
        "lastChecked": datetime.utcnow().isoformat() + "Z",
        "diffSummary": diff_summary
    }

    # Save diff and content per-state
    if updated and state:
        base_state_path = os.path.join("results", "state", state)
        diff_dir = os.path.join(base_state_path, "diff")
        content_dir = os.path.join(base_state_path, "content")
        os.makedirs(diff_dir, exist_ok=True)
        os.makedirs(content_dir, exist_ok=True)

        slug = slugify_url(url)
        diff_path = os.path.join(diff_dir, f"{slug}.diff")
        content_path = os.path.join(content_dir, f"{slug}.txt")

        if prev_content:
            diff = unified_diff(
                prev_content.splitlines(),
                content.splitlines(),
                fromfile="before",
                tofile="after",
                lineterm=""
            )
            with open(diff_path, "w", encoding="utf-8") as f:
                f.write("\n".join(diff))

        with open(content_path, "w", encoding="utf-8") as f:
            f.write(content)

    return result

def check_state(state, urls, only_updated=False):
    state_results = []
    for url in urls:
        result = check_url(url, state)
        if not only_updated or result.get("updated"):
            state_results.append(result)
    return state_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", help="Run check for a specific state")
    parser.add_argument("--url", help="Run check for a specific URL")
    parser.add_argument("--export", help="Export format: json|csv|markdown")
    parser.add_argument("--only-updated", action="store_true", help="Export only updated results")

    args = parser.parse_args()

    if args.state and args.url:
        results = [check_url(args.url, args.state)]
    elif args.state:
        with open(CONFIG_PATH, "r") as f:
            all_data = json.load(f)
        urls = all_data.get(args.state)
        if not urls:
            print(f"[ERROR] No URLs found for state: {args.state}")
            exit(1)
        results = check_state(args.state, urls, args.only_updated)
    else:
        with open(CONFIG_PATH, "r") as f:
            all_data = json.load(f)
        results = []
        for state, urls in all_data.items():
            state_results = check_state(state, urls, args.only_updated)
            results.extend(state_results)

    if args.export:
        export_results(results, args.export, state=args.state, url=args.url)
    else:
        print(json.dumps(results, indent=2))
