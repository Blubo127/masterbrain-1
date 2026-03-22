#!/usr/bin/env bash

set -euo pipefail

API_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$API_DIR/../.." && pwd)"

echo "[1/5] Building frontend"
cd "$REPO_ROOT/apps/web"
npm install
npm run build

echo "[2/5] Vendoring OpenCode CLI"
cd "$API_DIR"
python3 "$API_DIR/scripts/vendor_opencode.py" --force

echo "[3/5] Syncing Python packaging dependencies"
cd "$API_DIR"
uv sync --group packaging

echo "[4/5] Building desktop bundle with PyInstaller"
uv run pyinstaller packaging/pyinstaller/masterbrain.spec --noconfirm

echo "[5/5] Done"
echo "Bundle output: $API_DIR/dist/Masterbrain"
