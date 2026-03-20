WidTronic - Floating Desktop Clock
https://img.shields.io/badge/python-3.13-blue.svg
https://img.shields.io/badge/license-GPLv3-green.svg
https://img.shields.io/badge/platform-Windows-lightgrey.svg
https://img.shields.io/github/downloads/yourusername/widtronic/total.svg

<div align="center"> <img src="screenshot.png" alt="WidTronic Screenshot" width="600"> <p><i>A beautiful, customizable floating clock for your Windows desktop</i></p> </div>
---------------------------------------------------------------------------------------------
Features
Dual Windows – Separate clock and day displays that can work independently or together

Customizable Appearance – Choose fonts, colors, sizes for every element

Edit Mode – Double‑click any window to drag and reposition (auto‑saves after 10 seconds)

System Tray – Minimal tray icon with quick controls

Auto‑Start – Option to launch with Windows

Custom Fonts – Use your own .ttf/.otf fonts from %APPDATA%\WidTronic\fonts

Light/Dark Theme – Settings window adapts to your preference

Screen Boundary Protection – Windows stay within visible screen area (above taskbar)
------------------------------------------------------------------------------------

📦 Installation
Method 1: Download Pre‑built EXE (Recommended for Users)
Go to the Releases page

Download WidTronic.exe

Place it anywhere and run – no installation needed!

Configuration is saved in %APPDATA%\WidTronic\config.json

Method 2: Run from Source (For Developers)
Prerequisites
Python 3.13 or higher

pip (Python package manager)

Clone the Repository
bash
git clone https://github.com/yourusername/widtronic.git
cd widtronic
Install Dependencies
bash
pip install -r requirements.txt
Run the Application
bash
python main.py
Run with Hidden Console (Windows)
bash
pythonw main.py
=================================================================

Development Setup
Required Libraries
Library	Version	Purpose
pystray	≥0.19.0	System tray icon and menu
Pillow	≥10.0.0	Image handling for tray icon
pywin32	≥305	Windows registry access for auto‑start
tkinter	Built-in	GUI framework
Install All Dependencies
bash
pip install pystray pillow pywin32
Create requirements.txt
txt
pystray>=0.19.0
Pillow>=10.0.0
pywin32>=305
🚀 Building the EXE
Using PyInstaller
Install PyInstaller:

bash
pip install pyinstaller
Create the executable:

bash
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --add-data "fonts;fonts" --hidden-import=pystray --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=winreg main.py
The EXE will be in the dist folder

Using the Spec File (Recommended for Advanced Users)
Create widtronic.spec (included in repository) and run:

bash
pyinstaller widtronic.spec
📁 Project Structure
text
widtronic/
├── main.py              # Entry point – creates windows and tray
├── clock_window.py      # Clock display (hours, minutes, AM/PM)
├── day_window.py        # Day of week display
├── settings_window.py   # Unified settings (5 tabs)
├── config.py            # Config management (AppData path)
├── icon.ico             # Application icon
├── fonts/               # Bundled custom fonts (optional)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── LICENSE              # GPLv3 license

========================================================
 How to Use
Basic Controls
Double‑click any window → Enter edit mode (gray background)

Drag while in edit mode → Move window

Right‑click any window → Open settings

System Tray → Right‑click for quick controls

Settings Tabs
Tab	Description
Clock	Font, size, colors, AM/PM size & offset, hour format
Day	Show/hide, font, size, color, attach options
Menu	Theme, opacity, always on top, auto‑start
Help	User guide and tips
About	Version info and credits
Custom Fonts
Click "Open Font Folder" in Clock or Day tab

Copy your .ttf/.otf files into the folder

Fonts appear instantly in the dropdown lists

⚙️ Configuration File
All settings are saved in %APPDATA%\WidTronic\config.json:

json
{
    "clock_font_family": "Arial",
    "clock_font_size": 48,
    "clock_color_hour": "#ffffff",
    "clock_color_minute": "#ffffff",
    "clock_color_ampm": "#ffffff",
    "clock_ampm_font_size": 24,
    "clock_ampm_y_offset": 0,
    "clock_hour_format": "24",
    "clock_x": 100,
    "clock_y": 100,
    "day_font_family": "Arial",
    "day_font_size": 24,
    "day_color": "#ffffff",
    "day_x": 100,
    "day_y": 200,
    "day_show": true,
    "day_attach": false,
    "day_attach_position": "below",
    "day_attach_gap": 10,
    "bg_color": "transparent",
    "settings_theme": "light",
    "settings_opacity": 1.0,
    "settings_on_top": false,
    "start_minimized": false,
    "auto_start": false
}
🧪 Testing
Run the test suite:

bash
python -m unittest discover tests
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/amazing)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing)

Open a Pull Request

Coding Guidelines
Follow PEP 8 style guide

Add comments for complex logic

Update documentation for new features

Test your changes thoroughly

📝 License
This project is licensed under the GNU General Public License v3.0 – see the LICENSE file for details.

🙏 Credits
Developed by Yash © 2025

Built With
Python – Core programming language

Tkinter – GUI framework

PyStray – System tray integration

Pillow – Image handling

PyInstaller – Application packaging

Special Thanks
The open‑source community for amazing libraries

All contributors and users who provide feedback

📬 Contact
GitHub Issues: Report a bug

Email: your.email@example.com

Twitter: @yourhandle

💖 Support
If you find this project useful, consider:

Starring the repository ⭐

Sharing it with friends

Buying me a coffee

