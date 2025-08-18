#!/usr/bin/env python3
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import argparse

# Define common regulatory keywords to detect
TAG_KEYWORDS = {
    "air": ["air quality", "air permit", "emissions", "clean air"],
    "water": ["water quality", "npdes", "stormwater", "drinking water"],
    "permits": ["permit", "licensing", "application"],
    "wells": ["wells", "drilling", "borehole", "oil well"],
    "gas": ["gas pipeline", "gas safety", "natural gas"],
    "oil": ["oil", "crude", "oil and gas"],
    "energy": ["energy", "renewable", "fossil fuel", "solar", "wind"],
    "compliance": ["compliance", "regulations", "code"],
    "enforcement": ["violation", "enforcement", "inspection"],
    "land": ["land", "soil", "remediation"]
}

# Paths
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "../config/state_urls.json")
LOG_PATH = os.path.join(BASE_DIR, "auto_tag_errors.log")

def log_error(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    full_message = f"[{timestamp}] {message}"
    print(f"❌ {full_message}")
    with open(LOG_PATH, "a") as log_file:
        log_file.write(full_message + "\n")

def fetch_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return f"{soup.title.string if soup.title else ''} {soup.get_text()}"
    except Exception as e:
        log_error(f"Failed to fetch {url} — {str(e)}")
        return ""

def infer_tags(text):
    tags_found = set()
    lower_text = text.lower()
    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower_text:
                tags_found.add(tag)
    return sorted(tags_found)

def process(preserve_existing=False):
    if not os.path.exists(CONFIG_PATH):
        log_error("state_urls.json not found.")
        return

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    enriched_data = {}

    for state, entries in data.items():
        print(f"🔍 Processing {state}...")
        enriched_data[state] = []

        for entry in entries:
            if isinstance(entry, dict):
                url = entry.get("url")
                existing_tags = entry.get("tags", [])
            else:
                url = entry
                existing_tags = []

            print(f"  🌐 Scanning {url} ...")

            # Preserve tags if requested and tags already exist
            if preserve_existing and existing_tags:
                tags = existing_tags
                print(f"    ➤ Preserving existing tags: {tags}")
            else:
                content = fetch_text(url)
                tags = infer_tags(content)
                print(f"    ➤ Detected tags: {tags}")

            enriched_data[state].append({
                "url": url,
                "tags": tags
            })

    # Save updated config
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, indent=2)
        print(f"\n✅ Updated config written to {CONFIG_PATH}")
        print(f"📄 Errors (if any) logged in: {LOG_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-tag URLs in state_urls.json using keyword inference.")
    parser.add_argument("--preserve", action="store_true", help="Preserve existing tags instead of overwriting them.")
    args = parser.parse_args()

    process(preserve_existing=args.preserve)
