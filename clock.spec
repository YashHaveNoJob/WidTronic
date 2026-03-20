# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('fonts', 'fonts')
    ],
    hiddenimports=[
        'pystray',
        'PIL',
        'PIL._tkinter_finder',
        'winreg',
        'tkinter',
        'tkinter.colorchooser',
        'tkinter.font',
        'datetime',
        'json',
        'os',
        'threading',
        'socket',
        'config',
        'clock_window',
        'day_window',
        'settings_window'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WiDTronic',
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
    icon='icon.ico'
)
