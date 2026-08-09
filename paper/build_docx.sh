#!/usr/bin/env bash
# build the Word version of the paper from the markdown draft
set -e
cd "$(dirname "$0")"
if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is not installed (see https://pandoc.org/installing.html)" >&2
  exit 1
fi
pandoc paper.md -o paper.docx --resource-path=. --metadata lang=en-US
echo "wrote paper.docx"
