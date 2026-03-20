import os
import json
import sys
import ctypes
from pathlib import Path

APP_NAME = "WidTronic"

def get_config_dir():
    if os.name == 'nt':
        base = os.getenv('APPDATA')
    else:
        base = os.path.expanduser('~')
    config_dir = os.path.join(base, APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_fonts_dir():
    fonts_dir = os.path.join(get_config_dir(), "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    return fonts_dir

CONFIG_FILE = os.path.join(get_config_dir(), "config.json")

_custom_font_families = []

def load_custom_fonts():
    global _custom_font_families
    _custom_font_families = []
    fonts_dir = get_fonts_dir()
    if not os.path.exists(fonts_dir):
        return
    
    try:
        gdi32 = ctypes.windll.gdi32
        FR_PRIVATE = 0x10
    except:
        return
    
    for file in os.listdir(fonts_dir):
        if file.lower().endswith(('.ttf', '.otf')):
            path = os.path.join(fonts_dir, file)
            try:
                gdi32.AddFontResourceExW(ctypes.c_wchar_p(path), FR_PRIVATE, 0)
                family = os.path.splitext(file)[0]
                if family not in _custom_font_families:
                    _custom_font_families.append(family)
            except:
                family = os.path.splitext(file)[0]
                if family not in _custom_font_families:
                    _custom_font_families.append(family)
    
    _custom_font_families.sort()

def copy_bundled_fonts():
    if getattr(sys, 'frozen', False):
        src_fonts = os.path.join(sys._MEIPASS, "fonts")
    else:
        src_fonts = os.path.join(os.path.dirname(__file__), "fonts")
    
    if not os.path.exists(src_fonts):
        return
    
    dst_fonts = get_fonts_dir()
    for file in os.listdir(src_fonts):
        if file.lower().endswith(('.ttf', '.otf')):
            src = os.path.join(src_fonts, file)
            dst = os.path.join(dst_fonts, file)
            if not os.path.exists(dst):
                try:
                    import shutil
                    shutil.copy2(src, dst)
                    family = os.path.splitext(file)[0]
                    if family not in _custom_font_families:
                        _custom_font_families.append(family)
                except:
                    pass

copy_bundled_fonts()
load_custom_fonts()

if not _custom_font_families:
    _custom_font_families = ["No fonts found - add .ttf files to fonts folder"]

DEFAULT_CONFIG = {
    "clock_font_family": _custom_font_families[0] if _custom_font_families and _custom_font_families[0] != "No fonts found - add .ttf files to fonts folder" else "Arial",
    "clock_font_size": 48,
    "clock_color_hour": "#ffffff",
    "clock_color_minute": "#ffffff",
    "clock_color_ampm": "#ffffff",
    "clock_ampm_font_size": 24,
    "clock_ampm_y_offset": 0,
    "clock_hour_format": "24",
    "clock_x": 100,
    "clock_y": 100,
    "day_font_family": _custom_font_families[0] if _custom_font_families and _custom_font_families[0] != "No fonts found - add .ttf files to fonts folder" else "Arial",
    "day_font_size": 24,
    "day_color": "#ffffff",
    "day_x": 100,
    "day_y": 200,
    "day_show": True,
    "day_attach": False,
    "day_attach_position": "below",
    "day_attach_gap": 10,
    "bg_color": "transparent",
    "settings_theme": "light",
    "settings_opacity": 1.0,
    "settings_on_top": False,
    "start_minimized": False,
    "auto_start": False
}

def load_config():
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
            config.update(loaded)
        except:
            pass
    
    custom_fonts = get_font_list()
    if custom_fonts and custom_fonts[0] != "No fonts found - add .ttf files to fonts folder":
        if config["clock_font_family"] not in custom_fonts:
            config["clock_font_family"] = custom_fonts[0]
        if config["day_font_family"] not in custom_fonts:
            config["day_font_family"] = custom_fonts[0]
    
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_font_list():
    global _custom_font_families
    if not _custom_font_families:
        return ["No fonts found - add .ttf files to fonts folder"]
    return _custom_font_families