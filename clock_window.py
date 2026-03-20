import tkinter as tk
import datetime
from config import save_config

class ClockWindow(tk.Toplevel):
    def __init__(self, master, config, update_callback=None):
        super().__init__(master)
        self.master = master
        self.config = config
        self.update_callback = update_callback

        self.overrideredirect(True)
        self.attributes("-topmost", False)
        self.attributes("-transparentcolor", "gray")
        self.configure(bg="gray")
        self.geometry(f"+{config['clock_x']}+{config['clock_y']}")

        self.edit_mode = False
        self.drag_data = {"x": 0, "y": 0}
        self.idle_timer = None

        self.canvas = tk.Canvas(self, bg="gray", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self._create_text_items()

        self.canvas.bind("<Double-Button-1>", self.toggle_edit_mode)
        self.canvas.bind("<Button-3>", self.open_settings)

        self.update_clock()

    def _create_text_items(self):
        self.hour_text_id = self.canvas.create_text(0, 0,
            text="00",
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_hour"],
            anchor="nw")
        self.colon_text_id = self.canvas.create_text(0, 0,
            text=":",
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_minute"],
            anchor="nw")
        self.min_text_id = self.canvas.create_text(0, 0,
            text="00",
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_minute"],
            anchor="nw")
        self.ampm_text_id = self.canvas.create_text(0, 0,
            text="AM",
            font=(self.config["clock_font_family"], self.config["clock_ampm_font_size"]),
            fill=self.config["clock_color_ampm"],
            anchor="nw")
        self.after(10, self._update_text_positions)

    def _update_text_positions(self):
        self.update_idletasks()

        hour_bbox = self.canvas.bbox(self.hour_text_id)
        colon_bbox = self.canvas.bbox(self.colon_text_id)
        min_bbox = self.canvas.bbox(self.min_text_id)
        ampm_bbox = self.canvas.bbox(self.ampm_text_id)

        hour_width = hour_bbox[2] - hour_bbox[0] if hour_bbox else 50
        colon_width = colon_bbox[2] - colon_bbox[0] if colon_bbox else 10
        min_width = min_bbox[2] - min_bbox[0] if min_bbox else 50
        ampm_width = ampm_bbox[2] - ampm_bbox[0] if ampm_bbox else 40
        ampm_height = ampm_bbox[3] - ampm_bbox[1] if ampm_bbox else 30

        self.canvas.coords(self.hour_text_id, 0, 0)
        self.canvas.coords(self.colon_text_id, hour_width, 0)
        self.canvas.coords(self.min_text_id, hour_width + colon_width, 0)

        ampm_state = self.canvas.itemcget(self.ampm_text_id, "state")
        if ampm_state != "hidden":
            ampm_x = hour_width + colon_width + min_width + 5
            ampm_y = self.config["clock_ampm_y_offset"]
            self.canvas.coords(self.ampm_text_id, ampm_x, ampm_y)
            total_width = ampm_x + ampm_width
            total_height = max(
                hour_bbox[3] - hour_bbox[1] if hour_bbox else 50,
                ampm_height + abs(ampm_y)
            )
        else:
            total_width = hour_width + colon_width + min_width
            total_height = hour_bbox[3] - hour_bbox[1] if hour_bbox else 50

        self.canvas.config(width=total_width, height=total_height)

    def update_clock(self):
        now = datetime.datetime.now()
        if self.config["clock_hour_format"] == "12":
            hour = now.strftime("%I").lstrip("0") or "12"
            ampm = now.strftime("%p")
        else:
            hour = now.strftime("%H")
            ampm = ""
        minute = now.strftime("%M")

        self.canvas.itemconfig(self.hour_text_id, text=hour)
        self.canvas.itemconfig(self.min_text_id, text=minute)
        self.canvas.itemconfig(self.ampm_text_id, text=ampm)

        if self.config["clock_hour_format"] == "12" and ampm:
            self.canvas.itemconfig(self.ampm_text_id, state="normal")
        else:
            self.canvas.itemconfig(self.ampm_text_id, state="hidden")
        self.canvas.itemconfig(self.colon_text_id, state="normal")

        self._update_text_positions()
        self.after(1000, self.update_clock)

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
        self.drag_data["x"] = event.x_root - self.winfo_x()
        self.drag_data["y"] = event.y_root - self.winfo_y()
        if self.idle_timer:
            self.after_cancel(self.idle_timer)
            self.idle_timer = None

    def do_drag(self, event):
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        taskbar_height = 40
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height - taskbar_height))
        
        self.geometry(f"+{x}+{y}")
        if self.update_callback:
            self.update_callback()

    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}
        self.idle_timer = self.after(10000, self.on_idle_timeout)
        if self.update_callback:
            self.update_callback()

    def save_position(self):
        self.config["clock_x"] = self.winfo_x()
        self.config["clock_y"] = self.winfo_y()
        save_config(self.config)

    def apply_background(self):
        bg = self.config["bg_color"]
        frame_bg = "gray" if bg == "transparent" else bg
        self.canvas.config(bg=frame_bg)

    def open_settings(self, event=None):
        from settings_window import SettingsWindow
        if hasattr(self.master, 'app'):
            SettingsWindow(self.master.app, initial_tab="clock")
        else:
            SettingsWindow(self.master, initial_tab="clock")

    def refresh_from_config(self):
        self.canvas.itemconfig(self.hour_text_id,
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_hour"])
        self.canvas.itemconfig(self.min_text_id,
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_minute"])
        self.canvas.itemconfig(self.colon_text_id,
            font=(self.config["clock_font_family"], self.config["clock_font_size"]),
            fill=self.config["clock_color_minute"])
        self.canvas.itemconfig(self.ampm_text_id,
            font=(self.config["clock_font_family"], self.config["clock_ampm_font_size"]),
            fill=self.config["clock_color_ampm"])
        self.apply_background()
        self._update_text_positions()
        self.geometry(f"+{self.config['clock_x']}+{self.config['clock_y']}")