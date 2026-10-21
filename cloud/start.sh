#!/usr/bin/env bash
set -euo pipefail
echo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$echo_root"
export PYTHONUTF8=1
python3 tools/check_environment.py
