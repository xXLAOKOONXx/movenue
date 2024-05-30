# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['movenue\\ui\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('movenue\\ui\\assets\\icons8-sichtbar-50.png', 'movenue\\ui\\assets'),
        ('movenue\\ui\\assets\\polygon.ico', 'movenue\\ui\\assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='movenue',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='movenue\\ui\\assets\\polygon.ico'
)
