import os
import uuid
from configparser import ConfigParser


class RipConf:
    @staticmethod
    def load_app_conf(props_conf: ConfigParser, conf_file_name: str):

        print("---------------- result:" + str(conf_file_name))
        print("---------------- result:" + str(os.path.isfile(conf_file_name)))
        if not os.path.isfile(conf_file_name):
            # init new config file
            print("creating... " + conf_file_name)
            props_conf['keys'] = {
                'dns_key': "aaaa-bbbb-eeee-ffff-rrrr-qqqq",
                'api_key_number': '1',
                'api_user': 'test',
                'requested_domain': 'testdomain2',
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
            props_conf['ddns_server'] = {
                'delivery_url': "http://localhost:6000/update-registration",
                'ip_retrieval_url': 'https://supportlink.ch/myip.php',
                'uuid': uuid.uuid4()
            }
            with open(conf_file_name, 'w') as configfile:
                props_conf.write(configfile)
        else:
            # load from config file
            print("loading... " + conf_file_name)
            props_conf.read(conf_file_name)
