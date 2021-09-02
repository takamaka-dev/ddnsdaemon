import os
import platform
from pathlib import Path

pid_filename = "ddnsdaemon.pid"
linux_tempdir = "/tmp"

if __name__ == "__main__":
    curr_platform = platform.system()
    win_appdata = os.getenv('APPDATA')
    pid_file_path = None
    print("I'm launcher running on: " + curr_platform)
    print("APPDATA: " + str(win_appdata))
    if curr_platform == "Windows":
        # pid_file_path = os.path.dirname(str(win_appdata)[:-len("Roaming")])
        app_data = Path(win_appdata).resolve().parent
        print("APPDATA DIR: " + str(pid_file_path))
        print("parent: " + str(app_data))
        pid_file_path = os.path.join(app_data, "Temp", pid_filename)
    elif curr_platform == "Linux":
        pid_file_path = os.path.join(linux_tempdir, pid_filename)

    print("Pid File is " + str(pid_file_path))
