#!/usr/bin/env python3
import os
import json
from collections import defaultdict

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/state_urls.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../results/tag_summary.md")

def generate_tag_summary():
    if not os.path.exists(CONFIG_PATH):
        print("❌ state_urls.json not found.")
        return

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    tag_counts = defaultdict(lambda: defaultdict(int))  # tag_counts[state][tag] = count

    for state, entries in data.items():
        for entry in entries:
            tags = entry.get("tags", []) if isinstance(entry, dict) else []
            for tag in tags:
                tag_counts[state][tag] += 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🏷️ Tag Usage Summary\n\n")
        f.write("This report shows how many URLs are tagged with each keyword per state.\n\n")

        for state in sorted(tag_counts):
            f.write(f"## {state}\n\n")
            f.write("| Tag | Count |\n")
            f.write("|-----|-------|\n")
            for tag, count in sorted(tag_counts[state].items(), key=lambda x: x[0]):
                f.write(f"| {tag} | {count} |\n")
            f.write("\n")

    print(f"✅ Tag summary written to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_tag_summary()
