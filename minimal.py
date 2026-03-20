import tkinter as tk
import datetime

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-transparentcolor", "gray")
root.configure(bg="gray")
label = tk.Label(root, text="", bg="gray", fg="white", font=("Arial", 48))
label.pack()

def update():
    label.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
    root.after(1000, update)

update()
root.mainloop()
