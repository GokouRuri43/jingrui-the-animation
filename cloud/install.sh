#!/usr/bin/env bash
set -euo pipefail
echo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$echo_root"
if ! command -v apt-get >/dev/null; then
  echo 'Use Ubuntu/Debian, or install Python 3.10+, Blender 3.4+, FFmpeg and Noto CJK manually.' >&2
  exit 1
fi
echo_sudo=()
if [ "$(id -u)" -ne 0 ]; then
  echo_sudo=(sudo -n)
fi
echo_packages=(python3 blender ffmpeg fontconfig fonts-noto-cjk fonts-dejavu-core)
echo_missing=()
for echo_package in "${echo_packages[@]}"; do
  if ! dpkg-query -W -f='${Status}' "$echo_package" 2>/dev/null | grep -q 'install ok installed'; then
    echo_missing+=("$echo_package")
  fi
done
if [ "${#echo_missing[@]}" -gt 0 ]; then
  "${echo_sudo[@]}" apt-get update
  "${echo_sudo[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${echo_missing[@]}"
fi
fc-cache -f
bash cloud/start.sh
python3 tools/render_previs.py --smoke --output outputs/install-smoke
