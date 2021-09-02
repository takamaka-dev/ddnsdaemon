import os
import platform

linux_tempdir = "/tmp"


if __name__ == "__main__":
    curr_platform = platform.system()
    print("I'm launcher running on: " + curr_platform)
    print("APPDATA: " + str(os.getenv('APPDATA')))
