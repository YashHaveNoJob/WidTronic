import tkinter as tk
from tkinter import ttk, colorchooser
import os
import sys
import webbrowser
from config import save_config, get_font_list, get_fonts_dir
import winreg
import ctypes

class ACCENTPOLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_uint),
        ("AccentFlags", ctypes.c_uint),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_uint)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENTPOLICY)),
        ("SizeOfData", ctypes.c_size_t)
    ]

class SettingsWindow(tk.Toplevel):
    def __init__(self, app, initial_tab="clock"):
        super().__init__(app.root)
        self.app = app
        self.original_config = app.config.copy()
        self.config = app.config.copy()
        self.initial_tab = initial_tab

        self.title("WidTronic Settings")
        self.geometry("400x800")
        self.minsize(400, 800)
        self.transient(app.root)
        self.grab_set()

        self.theme = tk.StringVar(value=self.config.get("settings_theme", "light"))
        self.opacity = tk.DoubleVar(value=self.config.get("settings_opacity", 1.0))
        self.always_on_top = tk.BooleanVar(value=self.config.get("settings_on_top", False))
        self.auto_start = tk.BooleanVar(value=self.config.get("auto_start", False))
        self.acrylic_var = tk.BooleanVar(value=self.config.get("settings_acrylic", False))

        self.attributes("-alpha", self.opacity.get())
        if self.always_on_top.get():
            self.attributes("-topmost", True)

        self._set_icon()
        self._apply_theme(self.theme.get())

        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_clock_tab()
        self.create_day_tab()
        self.create_menu_tab()
        self.create_help_tab()
        self.create_about_tab()

        tab_map = {"clock": 0, "day": 1, "menu": 2, "help": 3, "about": 4}
        self.notebook.select(tab_map.get(initial_tab, 0))

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(btn_frame, text="Apply", command=self.apply_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)

        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.cancel())

        self.theme.trace_add('write', lambda *a: self._on_theme_change())
        self.opacity.trace_add('write', lambda *a: self.attributes("-alpha", self.opacity.get()))
        self.always_on_top.trace_add('write', lambda *a: self.attributes("-topmost", self.always_on_top.get()))
        self.acrylic_var.trace_add('write', lambda *a: self._apply_acrylic())

        self.update_idletasks()
        self._apply_acrylic()

    def _on_theme_change(self):
        self._apply_theme(self.theme.get())
        self._apply_acrylic()

    def _apply_acrylic(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            accent = ACCENTPOLICY()
            
            if self.acrylic_var.get():
                accent.AccentState = 4
                accent.AccentFlags = 2
                
                if self.theme.get() == "dark":
                    accent.GradientColor = 0x99202020
                else:
                    accent.GradientColor = 0x99FAFAFA
            else:
                accent.AccentState = 0
                
            data = WINDOWCOMPOSITIONATTRIBDATA()
            data.Attribute = 19
            data.Data = ctypes.pointer(accent)
            data.SizeOfData = ctypes.sizeof(accent)
            
            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.pointer(data))
        except:
            pass

    def _set_icon(self):
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(__file__)
        for fname in ["icon.ico", "icon.png"]:
            path = os.path.join(base, fname)
            if os.path.exists(path):
                try:
                    if path.endswith(".ico"):
                        self.iconbitmap(path)
                    else:
                        img = tk.PhotoImage(file=path)
                        self.iconphoto(True, img)
                except:
                    pass
                break

    def _apply_theme(self, theme_name):
        style = ttk.Style()
        style.theme_use('clam')
        if theme_name == "dark":
            style.configure('.', background='#2d2d2d', foreground='#ffffff',
                           troughcolor='#3c3c3c', selectbackground='#0078d4')
            style.configure('TLabel', background='#2d2d2d', foreground='#ffffff')
            style.configure('TFrame', background='#2d2d2d')
            style.configure('TNotebook', background='#2d2d2d', tabmargins=0)
            style.configure('TNotebook.Tab', background='#3c3c3c', foreground='#ffffff',
                           padding=[10, 5], focuscolor='none')
            style.map('TNotebook.Tab', background=[('selected', '#0078d4')])
            style.configure('TButton', background='#3c3c3c', foreground='#ffffff')
            style.map('TButton', background=[('active', '#555555')])
            style.configure('TCheckbutton', background='#2d2d2d', foreground='#ffffff')
            style.configure('TRadiobutton', background='#2d2d2d', foreground='#ffffff')
            style.configure('TScale', background='#2d2d2d')
            style.configure('TEntry', fieldbackground='#3c3c3c', foreground='#ffffff')
        else:
            style.configure('.', background='#f0f0f0', foreground='#000000',
                           troughcolor='#d0d0d0', selectbackground='#0078d4')
            style.configure('TLabel', background='#f0f0f0', foreground='#000000')
            style.configure('TFrame', background='#f0f0f0')
            style.configure('TNotebook', background='#f0f0f0')
            style.configure('TNotebook.Tab', background='#e1e1e1', foreground='#000000',
                           padding=[10, 5])
            style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
            style.configure('TButton', background='#e1e1e1', foreground='#000000')
            style.map('TButton', background=[('active', '#d1d1d1')])
            style.configure('TCheckbutton', background='#f0f0f0', foreground='#000000')
            style.configure('TRadiobutton', background='#f0f0f0', foreground='#000000')
            style.configure('TScale', background='#f0f0f0')
            style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')

    def _apply_auto_start(self):
        enable = self.auto_start.get()
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if getattr(sys, 'frozen', False):
                app_path = sys.executable
            else:
                main_path = os.path.join(os.path.dirname(__file__), "main.py")
                app_path = f'"{sys.executable}" "{main_path}"'
            if enable:
                winreg.SetValueEx(key, "WidTronic", 0, winreg.REG_SZ, app_path)
            else:
                try:
                    winreg.DeleteValue(key, "WidTronic")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Auto-start error: {e}")

    def create_clock_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Clock", padding=10)

        ttk.Label(tab, text="Font:").grid(row=0, column=0, sticky='w', pady=(0,5))
        self.clock_font_var = tk.StringVar(value=self.config["clock_font_family"])
        font_combo = ttk.Combobox(tab, textvariable=self.clock_font_var,
                                   values=get_font_list(), state='readonly')
        font_combo.grid(row=0, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        font_combo.bind('<<ComboboxSelected>>', self.preview)

        ttk.Label(tab, text="Font size:").grid(row=1, column=0, sticky='w', pady=(0,5))
        self.clock_size_var = tk.IntVar(value=self.config["clock_font_size"])
        size_scale = ttk.Scale(tab, from_=10, to=120, orient=tk.HORIZONTAL,
                                variable=self.clock_size_var, command=self.preview)
        size_scale.grid(row=1, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        
        self.clock_size_disp = tk.StringVar(value=str(self.clock_size_var.get()))
        self.clock_size_var.trace_add('write', lambda *a: self.clock_size_disp.set(str(self.clock_size_var.get())))
        ttk.Label(tab, textvariable=self.clock_size_disp).grid(row=1, column=2, padx=5)

        ttk.Label(tab, text="AM/PM size:").grid(row=2, column=0, sticky='w', pady=(0,5))
        self.ampm_size_var = tk.IntVar(value=self.config["clock_ampm_font_size"])
        ampm_scale = ttk.Scale(tab, from_=8, to=72, orient=tk.HORIZONTAL,
                                variable=self.ampm_size_var, command=self.preview)
        ampm_scale.grid(row=2, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        
        self.ampm_size_disp = tk.StringVar(value=str(self.ampm_size_var.get()))
        self.ampm_size_var.trace_add('write', lambda *a: self.ampm_size_disp.set(str(self.ampm_size_var.get())))
        ttk.Label(tab, textvariable=self.ampm_size_disp).grid(row=2, column=2, padx=5)

        ttk.Label(tab, text="AM/PM offset:").grid(row=3, column=0, sticky='w', pady=(0,5))
        self.ampm_y_offset_var = tk.IntVar(value=self.config.get("clock_ampm_y_offset", 0))
        offset_scale = ttk.Scale(tab, from_=-15, to=40, orient=tk.HORIZONTAL,
                                  variable=self.ampm_y_offset_var, command=self.preview)
        offset_scale.grid(row=3, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        
        self.ampm_off_disp = tk.StringVar(value=str(self.ampm_y_offset_var.get()))
        self.ampm_y_offset_var.trace_add('write', lambda *a: self.ampm_off_disp.set(str(self.ampm_y_offset_var.get())))
        ttk.Label(tab, textvariable=self.ampm_off_disp).grid(row=3, column=2, padx=5)

        ttk.Label(tab, text="Hour format:").grid(row=4, column=0, sticky='w', pady=(0,5))
        self.hour_format_var = tk.StringVar(value=self.config["clock_hour_format"])
        fmt_frame = ttk.Frame(tab)
        fmt_frame.grid(row=4, column=1, sticky='w', padx=(5,0))
        ttk.Radiobutton(fmt_frame, text="24h", variable=self.hour_format_var,
                        value="24", command=self.preview).pack(side=tk.LEFT, padx=(0,10))
        ttk.Radiobutton(fmt_frame, text="12h", variable=self.hour_format_var,
                        value="12", command=self.preview).pack(side=tk.LEFT)

        ttk.Label(tab, text="Colors:").grid(row=5, column=0, sticky='w', pady=(10,5))
        colors_frame = ttk.Frame(tab)
        colors_frame.grid(row=5, column=1, sticky='w', padx=(5,0))
        self.color_hour_var = tk.StringVar(value=self.config["clock_color_hour"])
        self.color_min_var = tk.StringVar(value=self.config["clock_color_minute"])
        self.color_ampm_var = tk.StringVar(value=self.config["clock_color_ampm"])
        ttk.Button(colors_frame, text="Hour", command=lambda: self.choose_color(self.color_hour_var)).pack(side=tk.LEFT, padx=2)
        ttk.Button(colors_frame, text="Minute", command=lambda: self.choose_color(self.color_min_var)).pack(side=tk.LEFT, padx=2)
        ttk.Button(colors_frame, text="AM/PM", command=lambda: self.choose_color(self.color_ampm_var)).pack(side=tk.LEFT, padx=2)

        ttk.Label(tab, text="Window position:").grid(row=6, column=0, sticky='w', pady=(15,5))
        pos_frame = ttk.Frame(tab)
        pos_frame.grid(row=6, column=1, sticky='w', padx=(5,0))
        ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
        self.clock_x_var = tk.IntVar(value=self.app.clock.winfo_x())
        ttk.Entry(pos_frame, textvariable=self.clock_x_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
        self.clock_y_var = tk.IntVar(value=self.app.clock.winfo_y())
        ttk.Entry(pos_frame, textvariable=self.clock_y_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(pos_frame, text="Current", command=self.use_clock_position).pack(side=tk.LEFT, padx=5)

        ttk.Button(tab, text="Open Font Folder", command=lambda: os.startfile(get_fonts_dir())).grid(row=7, column=0, columnspan=2, pady=15)
        tab.columnconfigure(1, weight=1)

    def create_day_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Day", padding=10)

        self.show_day_var = tk.BooleanVar(value=self.config.get("day_show", True))
        ttk.Checkbutton(tab, text="Show day", variable=self.show_day_var, command=self.preview).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,10))

        ttk.Label(tab, text="Font:").grid(row=1, column=0, sticky='w', pady=(0,5))
        self.day_font_var = tk.StringVar(value=self.config.get("day_font_family", "Arial"))
        font_combo = ttk.Combobox(tab, textvariable=self.day_font_var, values=get_font_list(), state='readonly')
        font_combo.grid(row=1, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        font_combo.bind('<<ComboboxSelected>>', self.preview)

        ttk.Label(tab, text="Font size:").grid(row=2, column=0, sticky='w', pady=(0,5))
        self.day_size_var = tk.IntVar(value=self.config.get("day_font_size", 24))
        size_scale = ttk.Scale(tab, from_=8, to=72, orient=tk.HORIZONTAL, variable=self.day_size_var, command=self.preview)
        size_scale.grid(row=2, column=1, sticky='ew', pady=(0,5), padx=(5,0))
        self.day_size_disp = tk.StringVar(value=str(self.day_size_var.get()))
        self.day_size_var.trace_add('write', lambda *a: self.day_size_disp.set(str(self.day_size_var.get())))
        ttk.Label(tab, textvariable=self.day_size_disp).grid(row=2, column=2, padx=5)

        ttk.Label(tab, text="Color:").grid(row=3, column=0, sticky='w', pady=(0,5))
        self.day_color_var = tk.StringVar(value=self.config.get("day_color", "#ffffff"))
        color_frame = ttk.Frame(tab)
        color_frame.grid(row=3, column=1, sticky='w', padx=(5,0))
        ttk.Button(color_frame, text="Choose", command=lambda: self.choose_color(self.day_color_var)).pack(side=tk.LEFT)
        color_preview = tk.Label(color_frame, bg=self.day_color_var.get(), width=2)
        color_preview.pack(side=tk.LEFT, padx=5)
        self.day_color_var.trace_add('write', lambda *a: color_preview.config(bg=self.day_color_var.get()))

        self.attach_var = tk.BooleanVar(value=self.config.get("day_attach", False))
        ttk.Checkbutton(tab, text="Attach to clock", variable=self.attach_var, command=self.preview).grid(row=4, column=0, columnspan=2, sticky='w', pady=(15,5))

        pos_frame = ttk.Frame(tab)
        pos_frame.grid(row=5, column=0, columnspan=2, sticky='w', pady=(0,5))
        ttk.Label(pos_frame, text="Position:").pack(side=tk.LEFT)
        self.attach_pos_var = tk.StringVar(value=self.config.get("day_attach_position", "below"))
        for p in ["above", "below", "left", "right"]:
            ttk.Radiobutton(pos_frame, text=p, variable=self.attach_pos_var, value=p, command=self.preview).pack(side=tk.LEFT, padx=5)

        ttk.Label(tab, text="Gap:").grid(row=6, column=0, sticky='w')
        self.gap_var = tk.IntVar(value=self.config.get("day_attach_gap", 10))
        gap_scale = ttk.Scale(tab, from_=0, to=50, orient=tk.HORIZONTAL, variable=self.gap_var, command=self.preview)
        gap_scale.grid(row=6, column=1, sticky='ew', padx=(5,0))
        self.gap_disp = tk.StringVar(value=str(self.gap_var.get()))
        self.gap_var.trace_add('write', lambda *a: self.gap_disp.set(str(self.gap_var.get())))
        ttk.Label(tab, textvariable=self.gap_disp).grid(row=6, column=2, padx=5)

        ttk.Label(tab, text="Manual position:").grid(row=7, column=0, sticky='w', pady=(15,5))
        pos_manual = ttk.Frame(tab)
        pos_manual.grid(row=7, column=1, sticky='w', padx=(5,0))
        ttk.Label(pos_manual, text="X:").pack(side=tk.LEFT)
        self.day_x_var = tk.IntVar(value=self.app.day.winfo_x())
        ttk.Entry(pos_manual, textvariable=self.day_x_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Label(pos_manual, text="Y:").pack(side=tk.LEFT)
        self.day_y_var = tk.IntVar(value=self.app.day.winfo_y())
        ttk.Entry(pos_manual, textvariable=self.day_y_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(pos_manual, text="Current", command=self.use_day_position).pack(side=tk.LEFT, padx=5)

        ttk.Label(tab, text="Background:").grid(row=8, column=0, sticky='w', pady=(15,5))
        self.bg_var = tk.StringVar(value=self.config.get("bg_color", "transparent"))
        bg_frame = ttk.Frame(tab)
        bg_frame.grid(row=8, column=1, sticky='w', padx=(5,0))
        ttk.Radiobutton(bg_frame, text="Transparent", variable=self.bg_var, value="transparent", command=self.preview).pack(side=tk.LEFT)
        ttk.Radiobutton(bg_frame, text="Black", variable=self.bg_var, value="black", command=self.preview).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(bg_frame, text="White", variable=self.bg_var, value="white", command=self.preview).pack(side=tk.LEFT)

        ttk.Button(tab, text="Open Font Folder", command=lambda: os.startfile(get_fonts_dir())).grid(row=9, column=0, columnspan=2, pady=15)
        tab.columnconfigure(1, weight=1)

    def create_menu_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Menu", padding=10)

        ttk.Label(tab, text="Theme:").grid(row=0, column=0, sticky='w', pady=(0,5))
        theme_frame = ttk.Frame(tab)
        theme_frame.grid(row=0, column=1, sticky='w', padx=(5,0))
        ttk.Radiobutton(theme_frame, text="Light", variable=self.theme, value="light").pack(side=tk.LEFT)
        ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme, value="dark").pack(side=tk.LEFT, padx=10)

        ttk.Label(tab, text="Window opacity:").grid(row=1, column=0, sticky='w', pady=(15,5))
        opacity_scale = ttk.Scale(tab, from_=0.3, to=1.0, orient=tk.HORIZONTAL, variable=self.opacity)
        opacity_scale.grid(row=1, column=1, sticky='ew', padx=(5,0))
        self.opacity_disp = tk.StringVar(value=f"{int(self.opacity.get()*100)}%")
        self.opacity.trace_add('write', lambda *a: self.opacity_disp.set(f"{int(self.opacity.get()*100)}%"))
        ttk.Label(tab, textvariable=self.opacity_disp).grid(row=1, column=2, padx=5)

        ttk.Checkbutton(tab, text="Keep settings window on top", variable=self.always_on_top).grid(row=2, column=0, columnspan=2, sticky='w', pady=(15,5))

        ttk.Checkbutton(tab, text="Start with Windows", variable=self.auto_start).grid(row=3, column=0, columnspan=2, sticky='w', pady=(15,5))

        ttk.Checkbutton(tab, text="Enable Acrylic Blur (Experiment)", variable=self.acrylic_var).grid(row=4, column=0, columnspan=2, sticky='w', pady=(15,5))

        tab.columnconfigure(1, weight=1)

    def create_help_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Help", padding=10)
        help_text = """
WIDTRONIC – USER GUIDE

Double‑click on any window to enter edit mode (blue border). 
While in edit mode, you can drag the window anywhere on the screen. 
After 10 seconds of inactivity, the window automatically exits edit mode 
and saves its position.

Right‑click on a window to open settings (or use the system tray menu).

CLOCK:
• Choose font, size, and colours for hours, minutes, and AM/PM.
• Adjust AM/PM size and vertical offset (use slider to move up/down).
• Switch between 12‑hour and 24‑hour format.
• Use "Current" to set the window to its current position.

DAY:
• Show/hide the day of the week.
• Customise font, size, and colour.
• Attach the day window to the clock (above, below, left, right) 
  with a configurable gap. When attached, moving the clock also moves 
  the day window.
• If not attached, you can position it manually.

FONTS:
• ONLY fonts placed in %APPDATA%\\WidTronic\\fonts will appear.
• Click "Open Font Folder" and drop .ttf or .otf files into that folder.
• Fonts are loaded automatically when you reopen settings.

MENU:
• Switch between light and dark theme.
• Adjust the opacity of the settings window.
• Keep settings window on top.
• Enable/disable automatic start with Windows.

BUTTONS:
• Apply – preview changes without closing
• Save – save permanently and close
• Cancel – discard all changes and close

TIPS:
• The clock stays above desktop icons but below full‑screen windows.
• All settings are saved in %APPDATA%\\WidTronic\\config.json
"""
        help_label = ttk.Label(tab, text=help_text, justify=tk.LEFT, wraplength=500)
        help_label.pack(fill=tk.BOTH, expand=True)

    def create_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="About", padding=10)
        about_text = """WidTronic
Version 2.0

A customizable, always‑on‑top clock for your desktop.

Developed by Yash
© 2026

Built with:
• Python 3.13
• Tkinter – GUI framework
• PyStray – system tray integration
• Pillow – image handling
• PyInstaller – application packaging

Special thanks to the open‑source community.

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by 
the Free Software Foundation.

For source code and updates, visit:
https://github.com/yourusername/widtronic"""

        def open_github():
            webbrowser.open("https://github.com/YashHaveNoJob/WidTronic")

        ttk.Button(tab, text="Visit GitHub", command=open_github).pack(pady=10)

        ttk.Label(tab, text=about_text, justify=tk.CENTER).pack(expand=True)

    def choose_color(self, var):
        color = colorchooser.askcolor(initialcolor=var.get())[1]
        if color:
            var.set(color)
            self.preview()

    def use_clock_position(self):
        self.clock_x_var.set(self.app.clock.winfo_x())
        self.clock_y_var.set(self.app.clock.winfo_y())

    def use_day_position(self):
        self.day_x_var.set(self.app.day.winfo_x())
        self.day_y_var.set(self.app.day.winfo_y())

    def preview(self, event=None):
        if hasattr(self.app, 'clock'):
            self.app.clock.config["clock_font_family"] = self.clock_font_var.get()
            self.app.clock.config["clock_font_size"] = self.clock_size_var.get()
            self.app.clock.config["clock_ampm_font_size"] = self.ampm_size_var.get()
            self.app.clock.config["clock_ampm_y_offset"] = self.ampm_y_offset_var.get()
            self.app.clock.config["clock_hour_format"] = self.hour_format_var.get()
            self.app.clock.config["clock_color_hour"] = self.color_hour_var.get()
            self.app.clock.config["clock_color_minute"] = self.color_min_var.get()
            self.app.clock.config["clock_color_ampm"] = self.color_ampm_var.get()
            self.app.clock.config["bg_color"] = self.bg_var.get()
            self.app.clock.refresh_from_config()

        if hasattr(self.app, 'day'):
            self.app.day.config["day_font_family"] = self.day_font_var.get()
            self.app.day.config["day_font_size"] = self.day_size_var.get()
            self.app.day.config["day_color"] = self.day_color_var.get()
            self.app.day.config["day_attach"] = self.attach_var.get()
            self.app.day.config["day_attach_position"] = self.attach_pos_var.get()
            self.app.day.config["day_attach_gap"] = self.gap_var.get()
            self.app.day.config["bg_color"] = self.bg_var.get()
            self.app.day.refresh_from_config()
            if self.show_day_var.get(): self.app.day.deiconify()
            else: self.app.day.withdraw()

    def apply_changes(self):
        self.preview()
        self._apply_auto_start()

    def save(self):
        self.config["clock_font_family"] = self.clock_font_var.get()
        self.config["clock_font_size"] = self.clock_size_var.get()
        self.config["clock_ampm_font_size"] = self.ampm_size_var.get()
        self.config["clock_ampm_y_offset"] = self.ampm_y_offset_var.get()
        self.config["clock_hour_format"] = self.hour_format_var.get()
        self.config["clock_color_hour"] = self.color_hour_var.get()
        self.config["clock_color_minute"] = self.color_min_var.get()
        self.config["clock_color_ampm"] = self.color_ampm_var.get()
        self.config["clock_x"] = self.clock_x_var.get()
        self.config["clock_y"] = self.clock_y_var.get()
        self.config["day_font_family"] = self.day_font_var.get()
        self.config["day_font_size"] = self.day_size_var.get()
        self.config["day_color"] = self.day_color_var.get()
        self.config["day_attach"] = self.attach_var.get()
        self.config["day_attach_position"] = self.attach_pos_var.get()
        self.config["day_attach_gap"] = self.gap_var.get()
        self.config["day_show"] = self.show_day_var.get()
        self.config["day_x"] = self.day_x_var.get()
        self.config["day_y"] = self.day_y_var.get()
        self.config["bg_color"] = self.bg_var.get()
        self.config["settings_theme"] = self.theme.get()
        self.config["settings_opacity"] = self.opacity.get()
        self.config["settings_on_top"] = self.always_on_top.get()
        self.config["auto_start"] = self.auto_start.get()
        self.config["settings_acrylic"] = self.acrylic_var.get()

        self._apply_auto_start()
        self.app.clock.config.update(self.config)
        self.app.clock.refresh_from_config()
        self.app.day.config.update(self.config)
        self.app.day.refresh_from_config()
        save_config(self.config)
        self.destroy()

    def cancel(self):
        self.app.clock.config.update(self.original_config)
        self.app.clock.refresh_from_config()
        self.app.day.config.update(self.original_config)
        self.app.day.refresh_from_config()
        self.destroy()