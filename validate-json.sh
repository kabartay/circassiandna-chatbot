#!/bin/bash
set -e

# Directories/files to check
FILES=( *.json data/**/*.json )

# Loop over JSON files in root and data/
for file in "${FILES[@]}"; do

  # Skip if file does not exist and git ignores
  [ -f "$file" ] || continue
  git check-ignore -q "$file" && continue

  echo "Fixing $file with jq..."
  if jq '.' "$file" >/dev/null 2>&1; then
    # Already valid, just format
    jq '.' "$file" > tmp.json && mv tmp.json "$file"
    git add "$file"
  else
    echo "Error: $file contains invalid JSON that jq cannot parse"
  fi
done
