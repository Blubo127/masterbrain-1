#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/5] Building frontend"
cd "$ROOT_DIR/src/web"
npm install
npm run build

echo "[2/5] Vendoring OpenCode CLI"
cd "$ROOT_DIR"
python3 scripts/vendor_opencode.py --force

echo "[3/5] Syncing Python packaging dependencies"
cd "$ROOT_DIR"
uv sync --group packaging

echo "[4/5] Building desktop bundle with PyInstaller"
uv run pyinstaller packaging/pyinstaller/masterbrain.spec --noconfirm

echo "[5/5] Done"
echo "Bundle output: $ROOT_DIR/dist/Masterbrain"
