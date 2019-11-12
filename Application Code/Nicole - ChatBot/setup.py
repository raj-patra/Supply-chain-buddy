import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("chat_room.py", base=base)]

cx_Freeze.setup(
    name="Nicole",
    options={"build_exe": {"packages": ["tkinter", "aiml"]}},
    version="0.01",
    description="An Intelligent Chat Bot",
    executables=executables
)
