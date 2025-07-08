import sys
import os
from cx_Freeze import setup, Executable

script_name = "run_washer_main.py"

include_files = []

include_files += ["emp_name.txt", "wash_profiles.py", "Washer_Log.txt", "washerGUI.kv", "washerAbortScreen.py",
                      "washerAddBoardsScreen.py", "washerBarcodeScreen.py", "washerCompleteScreen.py",
                      "washerConfirmationScreen.py", "washerGlobals.py", "washerOptionsScreen.py",
                      "washerScreenCountdown.py", "washerUseConfigScreen.py", "fonts/Nexa-ExtraLight.ttf", "fonts/Nexa-Heavy.ttf"]

build_exe_options = {
    "packages": ["pip", "kivymd", "datetime", "pyodbc", "kivy"],
    "excludes": ["kivy_deps.angle"],
    "include_files": include_files
}


'''
# MUST MANUALLY ADD THESE:
- glew32.dll
- SDL2_ttf.dll
- SDL2.dll
- SDL2_image.dll
- SDL2_mixer.dll
'''

base = None

setup (
    name = "WasherGUI",
    version="0.1",
    description="GUI for Washer, with barcode scanner functionality, washtype selection, and board loading.",
    options={"build_exe": build_exe_options},
    executables=[Executable(script_name, base=base)]
)