import os
from configparser import ConfigParser


class RipConf:
    @staticmethod
    def load_app_conf(props_conf: ConfigParser, conf_file_name: str):
        if not os.path.isfile(conf_file_name):
            # init new config file
            print("creating... " + conf_file_name)
            props_conf['keys'] = {
                'dns_key': "replace_with_takamaka_key_for_dns_update",
                'management_key': 'replace_with_takamaka_key_for_management'
            }
            props_conf['app'] = {
                'bind_address': 'localhost',
                'bind_port': '13131',
                'debug': False
            }
            props_conf['app_debug'] = {
                'bind_address': '0.0.0.0',
                'bind_port': '13131'
            }
            with open(conf_file_name, 'w') as configfile:
                props_conf.write(configfile)
        else:
            # load from config file
            print("loading... " + conf_file_name)
            props_conf.read(conf_file_name)
