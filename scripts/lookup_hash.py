#!/usr/bin/env python3
import os
import json
import argparse

# Paths
BASE_DIR = os.path.dirname(__file__)
MAPPING_FILE = os.path.join(BASE_DIR, "../.cache/mapping.json")

def main():
    parser = argparse.ArgumentParser(description="🔍 Reverse lookup a SHA256 hash in mapping.json")
    parser.add_argument("hash", help="The SHA256 hash to look up")
    args = parser.parse_args()
    target_hash = args.hash.lower()

    if not os.path.exists(MAPPING_FILE):
        print(f"❌ mapping.json not found at {MAPPING_FILE}")
        exit(1)

    with open(MAPPING_FILE, "r") as f:
        mapping = json.load(f)

    match = mapping.get(target_hash)
    if match:
        print(f"✅ Match found:")
        print(f"  URL   : {match['url']}")
        print(f"  State : {match['state']}")
    else:
        print(f"❌ No match found for hash: {target_hash}")

if __name__ == "__main__":
    main()
