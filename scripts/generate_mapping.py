#!/usr/bin/env python3
import os
import json
import hashlib

# Paths
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "../config/state_urls.json")
CACHE_DIR = os.path.join(BASE_DIR, "../.cache")
MAPPING_FILE = os.path.join(CACHE_DIR, "mapping.json")

def hash_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def main():
    # Load the config
    with open(CONFIG_PATH, "r") as f:
        state_urls = json.load(f)

    mapping = {}

    # Hash each URL and include state info
    for state, urls in state_urls.items():
        for url in urls:
            hashed = hash_url(url)
            mapping[hashed] = {
                "url": url,
                "state": state
            }

    # Save mapping
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

    print(f"✅ Generated mapping.json with {len(mapping)} entries (with state info)")

if __name__ == "__main__":
    main()
