# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_root = Path(__file__).resolve().parents[2]
web_dist = project_root / "src" / "web" / "dist"
vendored_opencode = project_root / "vendor" / "opencode"

if not web_dist.exists():
    raise SystemExit(
        "Frontend build not found. Run `npm run build` inside `src/web` before packaging."
    )

if not vendored_opencode.exists():
    raise SystemExit(
        "Vendored OpenCode not found. Run `python3 scripts/vendor_opencode.py` before packaging."
    )


a = Analysis(
    [str(project_root / "src" / "masterbrain" / "desktop.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[
        (str(web_dist), "web_dist"),
        (str(vendored_opencode), "vendor/opencode"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Masterbrain",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Masterbrain",
)
