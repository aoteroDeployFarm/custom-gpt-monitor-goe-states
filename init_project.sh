#!/bin/bash

set -e

PROJECT_DIR="regulatory-monitor"

echo "📁 Creating project: $PROJECT_DIR"

# ----------------------------
# Directory Structure
# ----------------------------
mkdir -p "$PROJECT_DIR"/{app,config,results,.cache,scripts,openapi}

# ----------------------------
# Placeholder Files
# ----------------------------
touch "$PROJECT_DIR"/app/{__init__.py,scraper.py,api.py}
touch "$PROJECT_DIR"/config/state_urls.json
touch "$PROJECT_DIR"/results/last_run.{json,csv,md}
touch "$PROJECT_DIR"/openapi/openapi.yaml
touch "$PROJECT_DIR"/scripts/setup.sh
touch "$PROJECT_DIR"/.gitignore
touch "$PROJECT_DIR"/README.md
touch "$PROJECT_DIR"/requirements.txt

# ----------------------------
# .gitignore
# ----------------------------
cat > "$PROJECT_DIR/.gitignore" <<EOF
.cache/
results/
__pycache__/
*.pyc
.env
EOF

# ----------------------------
# requirements.txt
# ----------------------------
cat > "$PROJECT_DIR/requirements.txt" <<EOF
fastapi
uvicorn
requests
beautifulsoup4
EOF

# ----------------------------
# README.md
# ----------------------------
cat > "$PROJECT_DIR/README.md" <<EOF
# Regulatory Monitor Scraper

Tracks and monitors regulatory data for oil, gas, and energy across all 50 U.S. states.

## Features

- Scrapes and detects changes on government regulatory websites
- Supports CLI and HTTP API usage
- Exports results to JSON, CSV, or Markdown
- Integrates with Custom GPTs via OpenAPI Action

## Structure

- \`app/scraper.py\`: Scraper logic (CLI + importable)
- \`app/api.py\`: FastAPI app for GPT action
- \`config/state_urls.json\`: State/URL map
- \`openapi/openapi.yaml\`: OpenAPI spec for GPTs
EOF

# ----------------------------
# Scripts/setup.sh (nested project scaffold)
# ----------------------------
cat > "$PROJECT_DIR/scripts/setup.sh" <<'EOS'
#!/bin/bash
set -e

mkdir -p config results .cache
touch config/state_urls.json
echo "[]" > results/last_run.json
echo "Created subdirectories and placeholder files."
EOS

chmod +x "$PROJECT_DIR/scripts/setup.sh"

echo "✅ Project initialized in: $PROJECT_DIR"
echo "👉 You can now navigate there and start coding:"
echo "   cd $PROJECT_DIR"
