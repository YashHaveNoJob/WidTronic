import tkinter as tk
import datetime
from config import save_config

class DayWindow(tk.Toplevel):
    def __init__(self, master, config, clock_window=None):
        super().__init__(master)
        self.master = master
        self.config = config
        self.clock_window = clock_window

        self.overrideredirect(True)
        self.attributes("-topmost", False)
        self.attributes("-transparentcolor", "gray")
        self.configure(bg="gray")
        self.geometry(f"+{config['day_x']}+{config['day_y']}")

        self.edit_mode = False
        self.drag_data = {"x": 0, "y": 0}
        self.idle_timer = None

        self.canvas = tk.Canvas(self, bg="gray", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.day_text_id = self.canvas.create_text(
            0, 0,
            text=datetime.datetime.now().strftime("%A"),
            font=(self.config["day_font_family"], self.config["day_font_size"]),
            fill=self.config["day_color"],
            anchor="nw"
        )
        self._update_canvas_size()

        self.canvas.bind("<Double-Button-1>", self.toggle_edit_mode)
        self.canvas.bind("<Button-3>", self.open_settings)

        self.update_day()

        if self.config["day_attach"]:
            self.after(100, self.attach_to_clock)

    def _update_canvas_size(self):
        self.update_idletasks()
        bbox = self.canvas.bbox(self.day_text_id)
        if bbox:
            self.canvas.config(width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])

    def update_day(self):
        self.canvas.itemconfig(self.day_text_id, text=datetime.datetime.now().strftime("%A"))
        self._update_canvas_size()
        self.after(60000, self.update_day)

    def toggle_edit_mode(self, event=None):
        if not self.edit_mode:
            self.enter_edit_mode()
        else:
            self.exit_edit_mode(save_position=True)

    def enter_edit_mode(self):
        self.edit_mode = True
        self.canvas.config(bg="lightgray")
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        if self.idle_timer:
            self.after_cancel(self.idle_timer)
        self.idle_timer = self.after(10000, self.on_idle_timeout)

    def exit_edit_mode(self, save_position=False):
        self.edit_mode = False
        self.apply_background()
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if self.idle_timer:
            self.after_cancel(self.idle_timer)
            self.idle_timer = None
        if save_position:
            self.save_position()

    def on_idle_timeout(self):
        self.exit_edit_mode(save_position=True)

    def start_drag(self, event):
        if self.config["day_attach"]:
            self.config["day_attach"] = False
            save_config(self.config)
        self.drag_data["x"] = event.x_root - self.winfo_x()
        self.drag_data["y"] = event.y_root - self.winfo_y()
        if self.idle_timer:
            self.after_cancel(self.idle_timer)
            self.idle_timer = None

    def do_drag(self, event):
        if self.drag_data["x"] is None:
            return
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        taskbar_height = 40
        
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height - taskbar_height))
        
        self.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}
        self.idle_timer = self.after(10000, self.on_idle_timeout)

    def save_position(self):
        self.config["day_x"] = self.winfo_x()
        self.config["day_y"] = self.winfo_y()
        save_config(self.config)

    def apply_background(self):
        bg = self.config["bg_color"]
        frame_bg = "gray" if bg == "transparent" else bg
        self.canvas.config(bg=frame_bg)

    def open_settings(self, event=None):
        from settings_window import SettingsWindow
        if hasattr(self.master, 'app'):
            SettingsWindow(self.master.app, initial_tab="day")
        else:
            SettingsWindow(self.master, initial_tab="day")

    def refresh_from_config(self):
        self.canvas.itemconfig(self.day_text_id,
            font=(self.config["day_font_family"], self.config["day_font_size"]),
            fill=self.config["day_color"])
        self.apply_background()
        self._update_canvas_size()
        if not self.config["day_attach"]:
            self.geometry(f"+{self.config['day_x']}+{self.config['day_y']}")
        else:
            self.attach_to_clock()

    def attach_to_clock(self):
        if not self.clock_window or not self.config["day_attach"]:
            return
        self.update_idletasks()
        clock_x = self.clock_window.winfo_x()
        clock_y = self.clock_window.winfo_y()
        clock_w = self.clock_window.winfo_width()
        clock_h = self.clock_window.winfo_height()
        day_w = self.winfo_width()
        day_h = self.winfo_height()
        gap = self.config["day_attach_gap"]

        pos = self.config["day_attach_position"]
        if pos == "above":
            new_x = clock_x + (clock_w - day_w) // 2
            new_y = clock_y - day_h - gap
        elif pos == "below":
            new_x = clock_x + (clock_w - day_w) // 2
            new_y = clock_y + clock_h + gap
        elif pos == "left":
            new_x = clock_x - day_w - gap
            new_y = clock_y + (clock_h - day_h) // 2
        elif pos == "right":
            new_x = clock_x + clock_w + gap
            new_y = clock_y + (clock_h - day_h) // 2
        else:
            return
        self.geometry(f"+{new_x}+{new_y}")
        self.config["day_x"] = new_x
        self.config["day_y"] = new_y