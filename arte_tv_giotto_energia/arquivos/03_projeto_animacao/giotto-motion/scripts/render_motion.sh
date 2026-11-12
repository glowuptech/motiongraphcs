#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
render_tmp=$(mktemp --suffix=.mp4)
trap 'rm -f "$render_tmp"' EXIT
out=../../../videos_finais
mkdir -p "$out"
npx remotion render src/index.ts GiottoBlackFridayMotion "$render_tmp" --browser-executable=/usr/bin/chromium --codec=h264 --crf=16 --concurrency=2
ffmpeg -v error -y -i "$render_tmp" -vf 'scale=in_range=full:out_range=tv,format=yuv420p' -c:v libx264 -preset fast -crf 18 -color_range tv -c:a aac -b:a 192k -t 10 -movflags +faststart "$out/giotto-black-friday-motion-10s.mp4"
ffmpeg -v error -y -i "$out/giotto-black-friday-motion-10s.mp4" -map 0:v:0 -c:v copy -an "$out/giotto-black-friday-motion-muted.mp4"
npx remotion still src/index.ts GiottoBlackFridayMotion "$out/giotto-black-friday-final-frame.png" --frame=299 --browser-executable=/usr/bin/chromium
