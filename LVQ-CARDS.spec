# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['LVQ-CARDS.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\GAMES\\PY_PROJECTS\\hmm-male.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\collect-points.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\no-with-attitude-3.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\sub-bass-4-seconds.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\joker.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\eh.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\man-intrigued.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\fanfare.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\card-snap.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\cards.ogg', '.'), ('D:\\GAMES\\PY_PROJECTS\\wheel-spin.ogg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LVQ-CARDS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LVQ-CARDS',
)
