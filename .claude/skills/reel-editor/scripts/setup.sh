#!/usr/bin/env bash
# Prepares a fresh cloud machine for reel editing and creates a project from the template.
# Usage: setup.sh <work-dir> [project-name]
# Prints the project path on the last line.
set -euo pipefail

WORK="${1:?usage: setup.sh <work-dir> [project-name]}"
NAME="${2:-reel}"
SKILL="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v ffmpeg >/dev/null; then
  apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg >/dev/null
fi

mkdir -p "$WORK" && cd "$WORK"
[ -f package.json ] || echo '{"private":true}' > package.json
npm i -s hyperframes@0.8.106 gsap@3.14.2 @fontsource/karantina @fontsource/heebo >/dev/null 2>&1
npx hyperframes browser ensure >/dev/null 2>&1 || true

if [ ! -d "$NAME" ]; then
  HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "$NAME" --example=blank --resolution=portrait --non-interactive >/dev/null 2>&1
fi
mkdir -p "$NAME/fonts" "$NAME/media"
F=node_modules/@fontsource
cp $F/karantina/files/karantina-hebrew-400-normal.woff2 \
   $F/karantina/files/karantina-hebrew-700-normal.woff2 \
   $F/karantina/files/karantina-latin-700-normal.woff2 \
   $F/heebo/files/heebo-hebrew-200-normal.woff2 \
   $F/heebo/files/heebo-hebrew-300-normal.woff2 \
   $F/heebo/files/heebo-latin-300-normal.woff2 "$NAME/fonts/"
cp node_modules/gsap/dist/gsap.min.js "$NAME/"
cp "$SKILL/template/index.html" "$NAME/index.html"

echo "$WORK/$NAME"
