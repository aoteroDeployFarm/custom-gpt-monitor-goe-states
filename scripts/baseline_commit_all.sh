#!/bin/bash

# Path to scraper
SCRAPER="./app/scraper.py"
LOG_FILE=".baseline-progress.log"

# Stop on error
set -e

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
    echo "  📄 Exporting $format (only updated)..."
    output=$($SCRAPER --state "$state" --export "$format" --only-updated)

    if echo "$output" | grep -q '"updated": true'; then
      changes_detected=true
      echo "  ✅ Changes detected in $format. Committing..."
      git add results/state/"$state"/"$format"/*
      git commit -m "baseline $state initial $format export (only updated)"
      git push
    else
      echo "  ℹ️ No changes in $format for $state."
    fi
  done

  if [ "$changes_detected" = true ]; then
    echo "$state" >> "$LOG_FILE"
    echo "✅ Done with $state (changes committed)"
  else
    echo "⚠️ No changes found for $state — not committing"
  fi

  echo "-------------------------------"
done

echo "🎉 All done!"
