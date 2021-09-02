import os
import platform

linux_tempdir = "/tmp"

if __name__ == "__main__":
    curr_platform = platform.system()
    win_appdata = os.getenv('APPDATA')
    pid_file_path = None
    print("I'm launcher running on: " + curr_platform)
    print("APPDATA: " + str(win_appdata))
    if curr_platform == "Windows":
        pid_file_path = os.path.dirname(str(win_appdata)[:len("Roaming")])
        print("APPDATA DIR: " + str(pid_file_path))
