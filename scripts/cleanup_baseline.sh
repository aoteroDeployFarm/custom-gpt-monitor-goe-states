#!/bin/bash

# Exit immediately on error
set -e

echo "🧹 Cleaning up previous baseline data..."

# Remove results per state
echo "🗑️  Deleting results/state/ directory..."
#rm -rf results/state/
rm -rf results/*

# Remove cache of hashes
echo "🗑️  Deleting .cache/ directory..."
rm -rf .cache/

# Optional: remove tree.md if you use auto-generated structure docs
if [ -f tree.md ]; then
  echo "🗑️  Removing tree.md..."
  rm tree.md
fi

# Optional: reset git (uncomment if you want this behavior)
# echo "🧨 WARNING: This will discard all local changes!"
# git reset --hard
# git clean -fd

echo "✅ Cleanup complete. Ready for fresh baseline."
