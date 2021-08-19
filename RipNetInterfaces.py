import builtins
import json
import sys

import netifaces
import platform
import subprocess

import psutil as psutil
from psutil import cpu_percent

from RipFunCall import RipFunCall


class RipNetInterfaces:
    ListString = list[str]
    InetSystemAttr = {v: k for k, v in netifaces.address_families.items()}
    # LoadArray = [
    #     psutil.cpu_percent,
    #     psutil.virtual_memory,
    #     psutil.swap_memory,
    #     psutil.cpu_count,
    #     psutil.cpu_freq,
    #     psutil.cpu_stats,
    #     psutil.cpu_times,
    #     psutil.cpu_times_percent,
    #     psutil.disk_io_counters,
    #     (psutil.disk_usage, "/"),
    #     (psutil.disk_usage, "/mnt/linExtra"),
    #     psutil.boot_time,
    #     psutil.users,
    #     # (psutil.sensors_temperatures, False),
    #     (getattr(psutil, "sensors_temperatures"), None, {"fahrenheit": False}),
    #     # (psutil.disk_io_counters, (False, False)),
    #     # (psutil.disk_io_counters, None, {"perdisk": False, "nowrap": False}),
    #     # (psutil.disk_io_counters, True, {"nowrap": False}),
    #
    # ]

    SafeLoadArray = [
        (psutil, "cpu_percent"),
        (psutil, "sensors_temperatures", None, {"fahrenheit": False}),
    ]

    # psutil.cpu_percent,
    # psutil.virtual_memory,
    # psutil.swap_memory,
    # psutil.cpu_count,
    # psutil.cpu_freq,
    # psutil.cpu_stats,
    # psutil.cpu_times,
    # psutil.cpu_times_percent,
    # psutil.disk_io_counters,
    # (psutil.disk_usage, "/"),
    # (psutil.disk_usage, "/mnt/linExtra"),
    # psutil.boot_time,
    # psutil.users,
    # # (psutil.sensors_temperatures, False),
    # (getattr(psutil, "sensors_temperatures"), None, {"fahrenheit": False}),
    # # (psutil.disk_io_counters, (False, False)),
    # # (psutil.disk_io_counters, None, {"perdisk": False, "nowrap": False}),
    # # (psutil.disk_io_counters, True, {"nowrap": False}),
    # ]

    @staticmethod
    def list_interfaces() -> ListString:
        try:
            net_ifcs = netifaces.interfaces()
            # print(type(net_ifcs))
            return net_ifcs
        except Exception as exc:
            print(str(exc))
            return None

    @staticmethod
    def list_gateways() -> ListString:
        # netifaces.gateways()
        try:
            net_ifcs = netifaces.gateways()
            # print(type(net_ifcs))
            return net_ifcs
        except Exception as exc:
            print(str(exc))
            return None

    @staticmethod
    def collect_data_to_dict(interface_info):
        if interface_info is not None:
            d_res = {}
            try:
                for k in RipNetInterfaces.InetSystemAttr.keys():
                    if RipNetInterfaces.InetSystemAttr[k] in interface_info:
                        try:
                            d_res[k] = interface_info[RipNetInterfaces.InetSystemAttr[k]]

                        except Exception as exc:
                            print("error in key access " + str(exc))
            except Exception as exc:
                print(str(exc))
                return None
            return d_res
        else:
            return None

    @staticmethod
    def collect_gw_to_dict(gw_info):
        if gw_info is not None:
            d_res = {}
            print("GW INFO: " + str(gw_info))

            try:
                if "default" in gw_info.keys():
                    try:
                        d_gw = {
                            "addr": gw_info["default"][0] if gw_info["default"][0] is not None else None,
                            "interface": gw_info["default"][1] if gw_info["default"][1] is not None else None
                        }
                        d_res["gw_default"] = d_gw

                    except Exception as exc:
                        print("exception reading default gateway" + str(exc))

                for k in RipNetInterfaces.InetSystemAttr.keys():
                    if RipNetInterfaces.InetSystemAttr[k] in gw_info:
                        try:
                            # d_res[k] = interface_info[RipNetInterfaces.InetSystemAttr[k]]
                            print("key " + str(k))
                            print("val " + str(gw_info[RipNetInterfaces.InetSystemAttr[k]]))
                            gateways = {}
                            i = 0
                            for gw_el in gw_info[RipNetInterfaces.InetSystemAttr[k]]:
                                gateways["gw_" + str(i)] = {
                                    "addr": gw_el[0] if gw_el[0] is not None else None,
                                    "interface": gw_el[1] if gw_el[1] is not None else None,
                                    "default": gw_el[2] if gw_el[2] is not None else None,
                                }
                                i += 1
                            d_res["all_gateways"] = gateways
                        except Exception as exc:
                            print("error in key access " + str(exc))
            except Exception as exc:
                print(str(exc))
                return None
            print("THE WINNER IS " + str(d_res))
            return d_res
        else:
            return None

    @staticmethod
    def descr_interfaces(inets: ListString):
        # print(RipNetInterfaces.InetSystemAttr)
        if inets is not None:
            interf_dict = {}
            for inet in inets:
                interface_info = netifaces.ifaddresses(inet)
                print(interface_info)
                interf_dict[str(inet)] = RipNetInterfaces.collect_data_to_dict(interface_info)
            return interf_dict

    @staticmethod
    def descr_gateways(gws: ListString):
        # print(RipNetInterfaces.InetSystemAttr)
        if gws is not None:
            interf_dict = {}
            # for gw in gws:
            #     # interface_info = netifaces.ifaddresses(inet)
            #     print(gw)

            interf_dict = RipNetInterfaces.collect_gw_to_dict(gws)
            return interf_dict

    @staticmethod
    def get_platform_details() -> dict:
        res = {}
        try:
            res['hostname'] = platform.node()

            res['platform'] = platform.platform()
            res['python-compiler'] = platform.python_compiler()
            res['machine'] = platform.machine()
            res['release'] = platform.release()
            res['architecture'] = platform.architecture()
            res['java_ver'] = platform.java_ver()
            res['libc_ver'] = platform.libc_ver()
            res['system'] = platform.system()
            res['uname'] = platform.uname()
            res['mac-ver'] = platform.mac_ver()
            res['win32-edition'] = platform.win32_edition()
            res['win32-is-iot'] = platform.win32_is_iot()
            res['processor'] = platform.processor()
            res['win32-ver'] = platform.win32_ver()
        except Exception as exc:
            res["platform_check_error"] = str(exc)
        return res

    @staticmethod
    def get_default_java() -> dict:
        res = {}
        try:
            res['java'] = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode(
                sys.stdout.encoding).replace("\n", " | ")
        except Exception as exc:
            res["java_check_error"] = str(exc)
        return res

    @staticmethod
    def get_sys_load() -> dict:
        res = {}
        try:
            # f_a_r = RipFunCall.wrap_fun_array_duplicate_rename(fun_arr=RipNetInterfaces.LoadArray)
            f_a_r = RipFunCall.safe_wrap_fun_array_duplicate_rename(fun_arr=RipNetInterfaces.SafeLoadArray)
            print("FAR: " + json.dumps(f_a_r))
            res["load_check"] = f_a_r
            # res["cpu_percent"] = psutil.cpu_percent()
            # r, e = RipFunCall.wrap_fun(psutil.cpu_percent)
            # print("R: " + str(r) + " E: " + str(e))
            # res["virtual_memory"] = psutil.virtual_memory()
            # res["swap_memory"] = psutil.swap_memory()
            # res["cpu_count"] = psutil.cpu_count()
            # res["cpu_freq"] = psutil.cpu_freq()
            # res["cpu_stats"] = psutil.cpu_stats()
            # res["cpu_times"] = psutil.cpu_times()
            # res["cpu_times_percent"] = psutil.cpu_times_percent()
            # res["disk_io_counters"] = psutil.disk_io_counters()
            # res["disk_usage"] = psutil.disk_usage("/")
            # print("DRY CALL ------------------------------")
            # # compl_call = (psutil.disk_io_counters, None, {"path": "/"})
            # # r, e = RipFunCall.wrap_fun(compl_call[0], compl_call[1:])
            # # print("R: " + str(r) + " E: " + str(e))
            # print("DRY CALL ------------------------------ END")
            # res["boot_time"] = psutil.boot_time()
            # res["users"] = psutil.users()
            # res["sensors_temperatures"] = psutil.sensors_temperatures(fahrenheit=False)
        except Exception as exc:
            res["load_check_errors"] = str(exc)
        return res
