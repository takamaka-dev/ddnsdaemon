import netifaces


class RipNetInterfaces:
    ListString = list[str]
    InetSystemAttr = {v: k for k, v in netifaces.address_families.items()}

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
                    d_res["gw_default"] = gw_info["default"]

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
                                    "dafault": gw_el[2] if gw_el[2] is not None else None,
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
