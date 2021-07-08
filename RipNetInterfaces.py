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
    def descr_interfaces(inets: ListString):
        # print(RipNetInterfaces.InetSystemAttr)
        if inets is not None:
            interf_dict = {}
            for inet in inets:
                interface_info = netifaces.ifaddresses(inet)
                print(interface_info)
                interf_dict[str(inet)] = RipNetInterfaces.collect_data_to_dict(interface_info)
            return interf_dict
