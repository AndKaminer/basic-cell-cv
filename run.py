import easygui
import subprocess

video_file = easygui.fileopenbox()

if video_file:
    subprocess.run(["python", "application.py", "--file", video_file, "--dtype", "0"])
