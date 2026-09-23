#!/usr/bin/env bash
# Downloads the Open University Learning Analytics Dataset (OULAD) into data/oulad/.
# Source: UCI Machine Learning Repository (mirrors the original analyse.kmi.open.ac.uk release).
# License: CC BY 4.0. Real, anonymised student data — not synthetic.
# Citation: Kuzilek, J., Hlosta, M., Zdrahal, Z. Open University Learning Analytics dataset.
#           Sci Data 4, 170171 (2017). https://doi.org/10.1038/sdata.2017.171
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/oulad"
URL="https://archive.ics.uci.edu/static/public/349/open+university+learning+analytics+dataset.zip"
ZIP_PATH="$SCRIPT_DIR/_oulad.zip"

if [ -f "$OUT_DIR/studentVle.csv" ]; then
  echo "OULAD already present at $OUT_DIR — skipping download."
  exit 0
fi

echo "Downloading OULAD from UCI (about 45 MB zipped)..."
curl -sL -o "$ZIP_PATH" "$URL"

mkdir -p "$OUT_DIR"
unzip -q -o "$ZIP_PATH" -d "$OUT_DIR"
rm "$ZIP_PATH"

echo "Done. Files in $OUT_DIR:"
ls -la "$OUT_DIR"
