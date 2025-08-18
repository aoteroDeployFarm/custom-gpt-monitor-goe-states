#!/bin/bash

set -e

echo "📁 Creating project directory structure..."

mkdir -p app config results .cache openapi scripts

# Create initial files if they don't already exist
touch app/__init__.py
touch app/scraper.py
touch app/api.py
touch config/state_urls.json
touch results/last_run.json
touch results/last_run.csv
touch results/last_run.md
touch openapi/openapi.yaml
touch scripts/setup.sh
touch requirements.txt
touch .gitignore
touch README.md

echo "✅ Directory structure and placeholder files created."

# Ensure `tree` is available
if ! command -v tree &> /dev/null
then
    echo "❌ 'tree' command not found. Please install it (e.g., brew install tree)."
    exit 1
fi

# Generate directory tree
echo "📦 Generating directory tree..."

TREE_OUTPUT=$(tree -I '__pycache__|.git|*.pyc|.DS_Store' -L 2)

# --- Update README.md ---
echo "📝 Updating README.md..."

# Remove old tree section if it exists
sed -i.bak '/^```/,/^```/d' README.md 2>/dev/null || true

# Append updated tree section to README
{
  echo ""
  echo "## 📁 Project Directory Structure"
  echo ""
  echo '```'
  echo "$TREE_OUTPUT"
  echo '```'
} >> README.md

rm -f README.md.bak
echo "✅ Updated README.md with directory tree."

# --- Create tree.md ---
echo "🗂️  Creating tree.md..."
{
  echo "# 📁 Project Directory Structure"
  echo ""
  echo '```'
  echo "$TREE_OUTPUT"
  echo '```'
} > tree.md

echo "✅ tree.md generated."

echo "🎉 Setup complete!"
