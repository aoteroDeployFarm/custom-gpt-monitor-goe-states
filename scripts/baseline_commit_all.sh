#!/bin/bash

# Path to scraper
SCRAPER="./app/scraper.py"
LOG_FILE=".baseline-progress.log"

# Stop on error
set -e

# Enable recursive globbing
shopt -s globstar nullglob

# Parse optional flag
FULL_MODE=false
if [[ "$1" == "--full" ]]; then
  FULL_MODE=true
  echo "🔁 Running in FULL mode: all sites will be exported, regardless of update status."
else
  echo "🚀 Running in ONLY-UPDATED mode: only updated sites will be exported."
fi

# Create log file if it doesn't exist
touch "$LOG_FILE"

# All 50 U.S. states
states=(
  "Alabama" "Alaska" "Arizona" "Arkansas" "California"
  "Colorado" "Connecticut" "Delaware" "Florida" "Georgia"
  "Hawaii" "Idaho" "Illinois" "Indiana" "Iowa"
  "Kansas" "Kentucky" "Louisiana" "Maine" "Maryland"
  "Massachusetts" "Michigan" "Minnesota" "Mississippi" "Missouri"
  "Montana" "Nebraska" "Nevada" "New Hampshire" "New Jersey"
  "New Mexico" "New York" "North Carolina" "North Dakota" "Ohio"
  "Oklahoma" "Oregon" "Pennsylvania" "Rhode Island" "South Carolina"
  "South Dakota" "Tennessee" "Texas" "Utah" "Vermont"
  "Virginia" "Washington" "West Virginia" "Wisconsin" "Wyoming"
)

# Main loop
for state in "${states[@]}"; do
  if grep -Fxq "$state" "$LOG_FILE"; then
    echo "⏩ Skipping $state (already processed)"
    continue
  fi

  echo "🔍 Processing $state..."
  changes_detected=false

  for format in json csv markdown; do
    echo "  📄 Exporting $format..."

    if [ "$FULL_MODE" = true ]; then
      output=$($SCRAPER --state "$state" --export "$format")
    else
      output=$($SCRAPER --state "$state" --export "$format" --only-updated)
    fi

    if [ "$FULL_MODE" = true ] || echo "$output" | grep -q '"updated": true'; then
      changes_detected=true
    fi
  done

  if [ "$changes_detected" = true ]; then
    echo "  ✅ Committing all updates for $state..."

    git add results/state/"$state"/**/* || true

    if ! git diff --cached --quiet; then
      git commit -m "baseline $state initial export${FULL_MODE:+ (full)}"
      git push
    else
      echo "⚠️  Nothing to commit for $state"
    fi

    echo "$state" >> "$LOG_FILE"
    echo "✅ Done with $state"
  else
    echo "⚠️ No updates for $state — nothing to commit"
  fi

  echo "-------------------------------"

  # ✅ Ask user to continue
  read -rp "❓ Do you wish to continue to the next state? (y/n): " answer
  if [[ "$answer" =~ ^[Nn]$ ]]; then
    echo "🛑 Exiting on user request."
    exit 0
  fi
done

echo "🎉 All done!"
