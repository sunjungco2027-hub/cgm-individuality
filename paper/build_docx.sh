#!/usr/bin/env bash
# build the Word version of the paper from the markdown draft
set -e
cd "$(dirname "$0")"
pandoc paper.md -o paper.docx
echo "wrote paper.docx"
