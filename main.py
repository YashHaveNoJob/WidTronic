import tkinter as tk
import threading
import os
import sys
import socket
import traceback
import winreg

LOCK_PORT = 12346
lock_socket = None

def is_another_instance_running():
    global lock_socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", LOCK_PORT))
        sock.listen(1)
        lock_socket = sock
        return False
    except socket.error:
        return True

def show_error(title, message):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title, message)
    root.destroy()

def set_auto_start(enable):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        exe_path = sys.executable
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
        if enable:
            winreg.SetValueEx(key, "WidTronic", 0, winreg.REG_SZ, app_path)
        else:
            try:
                winreg.DeleteValue(key, "WidTronic")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set auto-start: {e}")

def get_icon_path():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    for fname in ["icon.ico", "icon.png"]:
        path = os.path.join(base, fname)
        if os.path.exists(path):
            return path
    return None

def set_window_icon(window):
    icon_path = get_icon_path()
    if icon_path:
        try:
            if icon_path.endswith(".ico"):
                window.iconbitmap(icon_path)
            else:
                img = tk.PhotoImage(file=icon_path)
                window.iconphoto(True, img)
        except:
            pass

try:
    from pystray import Icon, MenuItem, Menu
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False
    print("pystray or PIL not installed – running without system tray")
    class Icon: pass
    class Menu: pass
    class MenuItem: pass

def create_default_tray_image():
    img = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 56, 56), outline='white', fill='black')
    draw.text((24, 20), "🕒", fill='white')
    return img

class App:
    def __init__(self):
        try:
            if is_another_instance_running():
                show_error("Already Running", "WidTronic is already running.")
                sys.exit(0)

            self.root = tk.Tk()
            self.root.withdraw()
            set_window_icon(self.root)
            self.root.app = self

            from config import load_config
            self.config = load_config()

            from clock_window import ClockWindow
            from day_window import DayWindow

            self.clock = ClockWindow(self.root, self.config, update_callback=self.on_clock_moved)
            self.day = DayWindow(self.root, self.config, clock_window=self.clock)
            set_window_icon(self.clock)
            set_window_icon(self.day)

            self.clock.apply_background()
            self.day.apply_background()

            if not self.config["day_show"]:
                self.day.withdraw()

            if self.config.get("start_minimized", False):
                self.clock.withdraw()
                self.day.withdraw()

            set_auto_start(self.config.get("auto_start", False))

            if HAS_TRAY:
                self.tray_thread = threading.Thread(target=self.setup_tray, daemon=True)
                self.tray_thread.start()
            else:
                print("No system tray – use right-click on windows to open settings.")

            self.root.protocol("WM_DELETE_WINDOW", self.quit)
            self.root.mainloop()

        except Exception as e:
            show_error("Startup Error", f"An error occurred:\n{traceback.format_exc()}")
            sys.exit(1)

    def on_clock_moved(self):
        if self.config["day_attach"] and self.day.winfo_viewable():
            self.day.attach_to_clock()

    def setup_tray(self):
        icon_path = get_icon_path()
        if icon_path:
            try:
                image = Image.open(icon_path)
            except:
                image = create_default_tray_image()
        else:
            image = create_default_tray_image()

        menu = Menu(
            MenuItem("Show/Hide Clock", self.toggle_clock),
            MenuItem("Show/Hide Day", self.toggle_day),
            MenuItem("Settings", self.open_settings),
            MenuItem("Start minimized", self.toggle_start_minimized, checked=lambda item: self.config.get("start_minimized", False)),
            MenuItem("Exit", self.quit)
        )
        self.tray_icon = Icon("widtronic", image, "WidTronic", menu)
        self.tray_icon.run()

    def toggle_clock(self, icon, item):
        if self.clock.winfo_viewable():
            self.clock.withdraw()
        else:
            self.clock.deiconify()

    def toggle_day(self, icon, item):
        if self.day.winfo_viewable():
            self.day.withdraw()
        else:
            self.day.deiconify()
            if self.config["day_attach"]:
                self.day.attach_to_clock()

    def toggle_start_minimized(self, icon, item):
        self.config["start_minimized"] = not self.config.get("start_minimized", False)
        from config import save_config
        save_config(self.config)

    def open_settings(self, icon=None, item=None):
        from settings_window import SettingsWindow
        self.root.after(0, lambda: SettingsWindow(self))

    def quit(self, icon=None, item=None):
        if HAS_TRAY and hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.clock.destroy()
        self.day.destroy()
        self.root.destroy()
        os._exit(0)

if __name__ == "__main__":
    App()