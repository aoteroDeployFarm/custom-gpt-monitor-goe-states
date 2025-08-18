#!/usr/bin/env python3

import os
import sys
import json
import requests
import hashlib
import argparse
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config", "state_urls.json")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "last_run.json")

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

def get_cache_file(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.txt")

def load_last_hash(url):
    cache_file = get_cache_file(url)
    if not os.path.exists(cache_file):
        return None
    with open(cache_file, "r") as f:
        return f.read().strip()

def save_hash(url, hash_val):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = get_cache_file(url)
    with open(cache_file, "w") as f:
        f.write(hash_val)

def check_url(state, url):
    try:
        html = fetch_html(url)
        content = extract_content(html)
        new_hash = compute_hash(content)
        old_hash = load_last_hash(url)
        updated = new_hash != old_hash
        if updated:
            save_hash(url, new_hash)
        return {
            "state": state,
            "url": url,
            "updated": updated,
            "checkedAt": datetime.utcnow().isoformat() + "Z",
            "summary": "Change detected" if updated else "No change"
        }
    except Exception as e:
        return {
            "state": state,
            "url": url,
            "error": str(e),
            "updated": False,
            "checkedAt": datetime.utcnow().isoformat() + "Z"
        }

def run_all(config):
    results = []
    for state, urls in config.items():
        for url in urls:
            result = check_url(state, url)
            print(f"[{state}] {url} - {result.get('summary', 'Error')}")
            results.append(result)
    return results

def run_single(state_name, config):
    if state_name not in config:
        print(f"❌ State '{state_name}' not found in config.")
        sys.exit(1)

    results = []
    for url in config[state_name]:
        result = check_url(state_name, url)
        print(f"[{state_name}] {url} - {result.get('summary', 'Error')}")
        results.append(result)
    return results

def run_single_url(state, url):
    result = check_url(state or "Custom", url)
    print(f"[{result['state']}] {url} - {result.get('summary', 'Error')}")
    return [result]

def save_results(results):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Regulatory Monitor Scraper")
    parser.add_argument("--state", help="Run scraper only for a specific state (e.g., 'Alaska')")
    parser.add_argument("--url", help="Run scraper for a specific URL only")
    args = parser.parse_args()

    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    if args.url:
        results = run_single_url(args.state, args.url)
    elif args.state:
        results = run_single(args.state, config)
    else:
        results = run_all(config)

    save_results(results)

if __name__ == "__main__":
    main()
