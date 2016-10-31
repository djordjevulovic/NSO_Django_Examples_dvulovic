import requests
import urllib
from requests.auth import HTTPBasicAuth
import json
import base64
from enum import Enum
import sys;
from collections import OrderedDict

###################################
# These are for NSO instance @ dCloud L2VPN lab
nso_url_prefix = "http://198.18.1.79:8080/api/"
nso_username = 'admin'
nso_password = 'admin'
###################################
class HTTP_Accept_Types(Enum):
    json_data = 1
    json_collection = 2

def NSO_GET(url_suffix, accept_type = HTTP_Accept_Types.json_data):

    url = nso_url_prefix + url_suffix

    # add Accept header
    if accept_type ==  HTTP_Accept_Types.json_data:
        accept_string =  'application/vnd.yang.data+json'
    elif accept_type ==  HTTP_Accept_Types.json_collection:
        accept_string = 'application/vnd.yang.collection+json'

    header = {"Accept": accept_string}

    response = requests.get(url, headers=header, auth=HTTPBasicAuth(nso_username, nso_password),verify=False)

    jsonObject = response.json()

    return jsonObject

def NSO_PUT(url_suffix, json_payload):

    url = nso_url_prefix + url_suffix

    header = {"Content-Type": "application/vnd.yang.data+json"}

    response = requests.put(url, data=json_payload, auth=HTTPBasicAuth(nso_username, nso_password), headers=header, verify=False)

    response.raise_for_status()

    return response.status_code

def Test_NSO_GET():

    return NSO_GET('running/devices/device?shallow', HTTP_Accept_Types.json_data)

def NSO_GET_Show_Device_Config(device):

    suffix = "running/devices/device/" + device + "/config"
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_GET_Device_List():
    return NSO_GET('running/devices/device?shallow', HTTP_Accept_Types.json_data)

def NSO_GET_Device_NED_ID(device):
    suffix = "running/devices/device/" + device + "/device-type/cli/ned-id"
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_GET_Show_IOS_Device_Interface_List(device):

    suffix = "running/devices/device/" + device + "/config/ios:interface?shallow"
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_GET_Show_IOSXR_Device_Interface_List(device):

    suffix = "running/devices/device/" + device + "/config/cisco-ios-xr:interface?shallow"
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_GET_Show_IOS_Device_Interface_Config(device,intf_type,intf_number):
    # intf_number can contain '/' so we must use urllib.parse.quote_plus to replace ti with Unicode character %2F
    suffix = "running/devices/device/" + device + "/config/ios:interface/" + str(intf_type) + "/" + urllib.parse.quote_plus(str(intf_number))
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_GET_Show_IOSXR_Device_Interface_Config(device,intf_type,intf_number):
    # intf_number can contain '/' so we must use urllib.parse.quote_plus to replace ti with Unicode character %2F
    suffix = "running/devices/device/" + device + "/config/cisco-ios-xr:interface/" + str(intf_type) + "/" + urllib.parse.quote_plus(str(intf_number))
    return NSO_GET(suffix, HTTP_Accept_Types.json_data)

def NSO_Intro_Add_DNS_Service(name, device, dns_server_ip):

    # NSO requries that key ("name" in this example) must be first parameter
    # Therefore, unordered dictionary like below might not work
    # payload = {"DNS:DNS": [ { "name": name, "device": [ device ], "dns_server_ip": dns_server_ip} ] }
    # The solution is to use ordered dictionary (OrderedDict)

    args = OrderedDict((("name",name),("device", [device]), ("dns_server_ip",dns_server_ip)))
    payload = json.dumps({"DNS:DNS": args },sort_keys=False)

    suffix = "running/services/DNS/" + name

    return NSO_PUT (suffix, payload)