import configparser

from flask import Flask
from flask_restful import Resource, Api

import RipConf
import RipNetInterfaces
import RipWelcome

rn = RipNetInterfaces.RipNetInterfaces
props_conf = configparser.ConfigParser()
conf_file_name = "config.properties"
app = Flask(__name__)
RipConf.RipConf.load_app_conf(props_conf=props_conf, conf_file_name=conf_file_name)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_interfaces():
    int_list = rn.list_interfaces()
    rn.descr_interfaces(int_list)


api = Api(app)
api.add_resource(RipWelcome.RipWelcome, '/')

if __name__ == "__main__":

    print("Mode " + props_conf['app']['debug'])
    if props_conf['app'].getboolean('debug'):
        print("debug")
        app.run(props_conf['app_debug']['bind_address'], int(props_conf['app_debug']['bind_port']),
                props_conf['app_debug'].getboolean('debug'))
    else:
        from waitress import serve

        serve(
            app,
            host=props_conf['app']['bind_address'],
            port=props_conf['appF']['bind_port'])
