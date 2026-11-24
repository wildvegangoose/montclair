#!/usr/bin/env bash
# Polite, retrying downloader for Wikimedia Commons thumbnails (Commons rate-limits bursts with HTTP 429).
set -euo pipefail
mkdir -p "$(dirname "$0")/../../img/landmarks"
cd "$(dirname "$0")/../../img/landmarks"
while IFS=$'\t' read -r id name url; do
  [ -z "$id" ] && continue
  [ -s "$name" ] && continue
  for i in 1 2 3 4 5 6 7 8; do
    code=$(curl -sSL -m 90 -A "MontclairThroughTime/0.1 (non-commercial fan history site; https://github.com/wildvegangoose/montclair)" -o "$name.part" -w "%{http_code}" "$url" || echo "000")
    if [ "$code" = "200" ] && file -b --mime-type "$name.part" 2>/dev/null | grep -q '^image/'; then
      mv "$name.part" "$name"
      echo "ok $name ($(stat -c%s "$name") bytes)"
      break
    fi
    rm -f "$name.part"
    echo "retry $name (code=$code, attempt=$i)"
    sleep $((i * 45))
  done
  sleep 25
done < ../../tools/landmarks/photos.tsv
echo "done"
