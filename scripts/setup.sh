#!/bin/bash
set -e

mkdir -p config results .cache
touch config/state_urls.json
echo "[]" > results/last_run.json
echo "Created subdirectories and placeholder files."
