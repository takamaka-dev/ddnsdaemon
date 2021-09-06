import asyncio
import os
from pathlib import Path
import platform
from typing import Union

import RipFileHelper


class RipProcHelper:
    @staticmethod
    def check_pid_running(pid: int) -> Union[None, bool]:
        try:
            os.kill(pid, 0)
            return True
        except OSError as exc:
            return False
        except Exception as exc:
            print("unexpected behaviour " + str(exc))
            return None

    @staticmethod
    async def run(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        print("Child pid is:" + str(proc.pid))

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    @staticmethod
    def get_pid_file_path_by_os():
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
            pid_file_path = os.path.join(app_data, "Local", "Temp", RipFileHelper.RipFileHelper.pid_filename)
        elif curr_platform == "Linux":
            pid_file_path = os.path.join(RipFileHelper.RipFileHelper.linux_tempdir,
                                         RipFileHelper.RipFileHelper.pid_filename)
        return pid_file_path

    @staticmethod
    def delete_invalid_pid_file_or_terminate():
        pid_file_path = RipProcHelper.get_pid_file_path_by_os()
        pid_file_exists = RipFileHelper.RipFileHelper.file_exists(pid_file_path)

        print("Pid File is " + str(pid_file_path) + " file exists: " + str(pid_file_exists))

        if pid_file_exists is None:
            print("error in file reading")
            # max 127
            exit(3)

        if pid_file_exists:
            saved_pid = RipFileHelper.RipFileHelper.read_pid_file(pid_file_path)
            print("Pid file value is: " + str(saved_pid))
            if saved_pid is None:
                print("invalid pid file")
                print("deleting pid file")
                del_pid_file = RipFileHelper.RipFileHelper.delete_file(pid_file_path)
                if del_pid_file is None:
                    print("unable to handle pid file")
                    exit(4)
                elif del_pid_file:
                    print("invalid pid file successfully deleted")
                else:
                    print("unhandled exception in file removal ")
                    exit(5)
            else:
                pid_exists = RipProcHelper.check_pid_running(saved_pid)
                print("pid exists and running " + str(pid_exists))
                if pid_exists:
                    print("skip execution")
                    exit(0)
                else:
                    del_pid_file = RipFileHelper.RipFileHelper.delete_file(pid_file_path)
                    if del_pid_file is None:
                        print("unable to handle pid file")
                        exit(4)
                    elif del_pid_file:
                        print("expired pid file successfully deleted")
                    else:
                        print("unhandled exception in file removal ")
                        exit(5)
