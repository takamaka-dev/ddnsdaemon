import configparser
from http import HTTPStatus

from flask import Flask
from flask_restful import Resource, Api

import RipConf
import RipNetInterfaces
import RipRepack
import RipWelcome

rn = RipNetInterfaces.RipNetInterfaces
rr = RipRepack.RipRequest
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


class CronJob(Resource):
    @staticmethod
    def get():
        print("cronjob called")
        internal_inferfaces_conf = {}
        # get local inet configuration
        int_list = rn.list_interfaces()
        gws_list = rn.list_gateways()
        internal_interfaces = rn.descr_interfaces(int_list)
        internal_gateways = rn.descr_gateways(gws_list)
        # todo finire l'assemblaggio
        # print("Internal interfaces " + str(internal_interfaces))
        # print("Internal gateways " + str(internal_gateways))
        internal_inferfaces_conf["interfaces"] = internal_interfaces
        internal_inferfaces_conf["gateways"] = internal_gateways
        print(str(internal_inferfaces_conf))
        # get external ip addr
        my_ext_ip = rr.retrieve_my_ip(props_conf['ddns_server']['ip_retrieval_url'])
        print(my_ext_ip)
        return {"result": "job called", "request": "cronjob"}, HTTPStatus.OK


api = Api(app)
api.add_resource(RipWelcome.RipWelcome, '/')
api.add_resource(CronJob, '/cronjob')

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
            port=props_conf['app']['bind_port'])
