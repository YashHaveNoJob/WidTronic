# WidTronic 

<div align="center">
   <img width="87" height="87" alt="icon" src="https://github.com/user-attachments/assets/ffbc87bf-f094-43be-94d3-b9a07b6a43a2" />
<p><i>A light, customizable clock widget for your Windows desktop</i></p> </div>

**WidTronic** is a modern, minimalist Windows desktop widget suite designed pyhtonw. It features a highly customizable floating clock and date widget with performance in mind

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

PreView<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/13b3b01e-a224-4f6f-8429-c3caaa19b1d7" />


## Features
* **Dual Windows:** Separate clock and day displays that can work independently or together
* **Customizable Appearance:**  Choose fonts, colors, sizes for every element
* **System Tray:** Minimal tray icon with quick controls
* **Auto‑Start**  Option to launch with Windows
* **Custom Fonts**  Use your own .ttf/.otf fonts from %APPDATA%\WidTronic\fonts
* **Light/Dark Theme**  Settings window adapts to your preference
* **Performance Focused:** Low CPU/RAM footprint using optimized Tkinter and Win32 API calls.
* Takes Less memory than ur Base apps
<img width="916" height="214" alt="image" src="https://github.com/user-attachments/assets/1baa6b64-b4d5-48b3-a736-f59030ace659" />

## Getting Started

### Prerequisites
* **Windows 10 or 11** (Required for Acrylic effects).
* **Python 3.10 or higher**.

### Installation
**Method 1: Download Pre‑built EXE (Recommended for Users)**

Go to the Releases page

Download WidTronic.exe

Place it anywhere and run – no installation needed!

Configuration is saved in %APPDATA%\WidTronic\config.json

**Method 2: Run from Source (For Developers, who know how it works)**
Prerequisites
Python 3.13 or higher

pip (Python package manager)
*Required Libraries*
Library	Version	Purpose
pystray	≥0.19.0	System tray icon and menu
Pillow	≥10.0.0	Image handling for tray icon
pywin32	≥305	Windows registry access for auto‑start
tkinter	Built-in	GUI framework

**One Line CMD**
```bash
 pip install pystray pillow pywin32 pyinstaller
```
1. **Clone the repository:**
   ```bash
   https://github.com/YOUR_USERNAME/WidTronic.git
   ```

2. **Usage**


   for using use the BAT file "[Clock.bat](https://github.com/YashHaveNoJob/WidTronic/blob/main/clock.bat)" or the cmd
   ```python main.py```



   # License
      This project is licensed under the GNU General Public License v3.0 – see the LICENSE file for details.
   # Credits
   Developed by Yash © 2026

   
   Contact
GitHub Issues: Report a bug

