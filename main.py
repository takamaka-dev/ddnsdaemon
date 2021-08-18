import configparser
from http import HTTPStatus

from flask import Flask, json
from flask_restful import Resource, Api

import RipConf
import RipNetInterfaces
import RipRepack
import RipWelcome
import daemon

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
        ip_and_interfaces_conf = {}
        # get local inet configuration
        int_list = rn.list_interfaces()
        gws_list = rn.list_gateways()
        internal_interfaces = rn.descr_interfaces(int_list)
        internal_gateways = rn.descr_gateways(gws_list)
        my_ext_ip = rr.retrieve_my_ip(props_conf['ddns_server']['ip_retrieval_url'])
        # todo finire l'assemblaggio
        # print("Internal interfaces " + str(internal_interfaces))
        # print("Internal gateways " + str(internal_gateways))
        ip_and_interfaces_conf["interfaces"] = internal_interfaces
        ip_and_interfaces_conf["gateways"] = internal_gateways
        # print(my_ext_ip.exploded)
        ip_and_interfaces_conf["ext_ip"] = my_ext_ip.exploded if my_ext_ip is not None else None
        ip_and_interfaces_conf["request-type"] = "update-machine-registration"
        ip_and_interfaces_conf["uuid"] = props_conf['ddns_server']['uuid']
        ip_and_interfaces_conf["nickname"] = props_conf['ddns_server']['nickname']
        ip_and_interfaces_conf["platform"] = rn.get_platform_details()
        ip_and_interfaces_conf["java"] = rn.get_default_java()
        ip_and_interfaces_conf["load"] = rn.get_sys_load()
        print("PLATFORM " + str(ip_and_interfaces_conf["platform"]))
        print("JAVA " + str(ip_and_interfaces_conf["java"]))
        print("LOAD " + str(ip_and_interfaces_conf["load"]))
        res = RipRepack.RipRequest.json_hmac_request(destination_server_url=props_conf['ddns_server']['delivery_url'],
                                                     api_user=props_conf['keys']['api_user'],
                                                     api_key=props_conf['keys']['dns_key'],
                                                     api_key_number=props_conf['keys']['api_key_number'],
                                                     dictionary_payload=ip_and_interfaces_conf,
                                                     submit_method="POST")
        print(res.text)
        # print(str(ip_and_inferfaces_conf))
        # get external ip addr
        # return {"result": "job called", "request": "cronjob", "data": ip_and_inferfaces_conf}, HTTPStatus.OK
        j_data = json.loads(res.text)
        return j_data, res.status_code


api = Api(app)
api.add_resource(RipWelcome.RipWelcome, '/')
api.add_resource(CronJob, '/cronjob')





if __name__ == "__main__":

    print("Mode " + props_conf['app']['debug'])

    print(props_conf['ddns_server']['nickname'])

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


