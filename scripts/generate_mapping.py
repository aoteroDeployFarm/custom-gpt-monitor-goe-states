#!/usr/bin/env python3
import os
import json
import hashlib

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/state_urls.json")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "../.cache")
MAPPING_FILE = os.path.join(CACHE_DIR, "mapping.json")

def hash_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def main():
    # Load state_urls.json
    with open(CONFIG_PATH, "r") as f:
        state_urls = json.load(f)

    # Create mapping
    mapping = {}
    for state, urls in state_urls.items():
        for url in urls:
            mapping[hash_url(url)] = url

    # Save to .cache/mapping.json
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

    print(f"✅ Generated mapping.json with {len(mapping)} entries.")

if __name__ == "__main__":
    main()
