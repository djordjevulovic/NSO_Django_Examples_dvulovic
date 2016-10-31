from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from nso_helper_dvulovic import NSO_GET
from nso_helper_dvulovic import HTTP_Accept_Types
from nso_helper_dvulovic import Test_NSO_GET
from nso_helper_dvulovic import NSO_Intro_Add_DNS_Service
from nso_helper_dvulovic import NSO_GET_Show_Device_Config
from nso_helper_dvulovic import NSO_GET_Device_NED_ID
from nso_helper_dvulovic import NSO_GET_Show_IOS_Device_Interface_List
from nso_helper_dvulovic import NSO_GET_Show_IOS_Device_Interface_Config
from nso_helper_dvulovic import NSO_GET_Show_IOSXR_Device_Interface_List
from nso_helper_dvulovic import NSO_GET_Show_IOSXR_Device_Interface_Config

import json
import requests

from django.http import HttpResponse
from NSO_Intro_Webdemo import forms

# Create your views here.
def test(request):

    jsonObject = Test_NSO_GET()

    text = str("Devices<br><br>")
    #jsonDump = json.dumps(jsonObject, sort_keys=True, indent=4)
    for device in jsonObject["device"]:
        text += device["name"]
        text += "<br>"

    return HttpResponse(text)

def NSO_Intro_Main_View(request):
    return render(request, 'NSO_Intro_Webdemo/main.html')

def NSO_Intro_Result_View(request, text):
    return render(request, 'NSO_Intro_Webdemo/result.html', {'text': text})

def NSO_Intro_Show_Device_Config_View(request):

    if request.method == 'POST':
        form = forms.NSO_Intro_Show_Device_Config_Form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            device = cd.get('device')

            result = NSO_GET_Show_Device_Config(device)

            return NSO_Intro_Result_View(request, json.dumps(result, sort_keys=True, indent=4))
        else:
            print (form.errors)
    else:
        form = forms.NSO_Intro_Show_Device_Config_Form()

    return render(request, 'NSO_Intro_Webdemo/show_device_config.html', {'form': form})

def NSO_Intro_Show_Interface_Config_View(request):

    if request.method == 'POST':
        form = forms.NSO_Intro_Show_Device_Config_Form(request.POST)

        if form.is_valid():

            cd = form.cleaned_data

            device = cd.get('device')
            ## from some reaosn, intf_type and intf_number are not in the "clean" data; find out why; until, use raw data
            intf_type = request.POST['intf_type']
            intf_number = request.POST['intf_number']

            jsonObject = NSO_GET_Device_NED_ID(device)
            ned_id = jsonObject["ned-id"]

            if ned_id == "ios-id:cisco-ios":
                result = NSO_GET_Show_IOS_Device_Interface_Config(device,intf_type,intf_number)
            if ned_id == "cisco-ios-xr-id:cisco-ios-xr":
                result = NSO_GET_Show_IOSXR_Device_Interface_Config(device,intf_type,intf_number)

            return NSO_Intro_Result_View(request, json.dumps(result, sort_keys=True, indent=4))
        else:
            print (form.errors)
    else:
        form = forms.NSO_Intro_Show_Interface_Config_Form()

    return render(request, 'NSO_Intro_Webdemo/show_interface_config.html', {'form': form})

@csrf_exempt
def NSO_Intro_Show_Interface_Config_View_get_intf_types(request):

    response = []

    device = request.POST['device']

    if device:

        jsonObject = NSO_GET_Device_NED_ID(device)
        ned_id = jsonObject["ned-id"]

        data = []

        if ned_id == "ios-id:cisco-ios":

            jsonObject = NSO_GET_Show_IOS_Device_Interface_List(device)

            for intf_type in jsonObject["tailf-ned-cisco-ios:interface"]:
                data.append({'id': intf_type, 'name': intf_type})

            response = { 'item_list':data }
            return HttpResponse(json.dumps(response))

        if ned_id == "cisco-ios-xr-id:cisco-ios-xr":

            jsonObject = NSO_GET_Show_IOSXR_Device_Interface_List(device)

            for intf_type in jsonObject["tailf-ned-cisco-ios-xr:interface"]:
                data.append({'id': intf_type, 'name': intf_type})

            response = { 'item_list':data }
            return HttpResponse(json.dumps(response))

        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse(json.dumps(response))

@csrf_exempt
def NSO_Intro_Show_Interface_Config_View_get_intf_numbers(request):

    response = []

    jsonargs = json.loads(request.body.decode('utf-8'))

    device = jsonargs['device']
    intf_type = jsonargs['intf-type']

    if device:

        jsonObject = NSO_GET_Device_NED_ID(device)
        ned_id = jsonObject["ned-id"]

        data = [ ]

        if ned_id == "ios-id:cisco-ios":

            jsonObject = NSO_GET_Show_IOS_Device_Interface_List(device)

            for intf_number in jsonObject["tailf-ned-cisco-ios:interface"][intf_type]:
                data.append({'id': intf_number["name"], 'name': intf_number["name"]})

            response = { 'item_list':data }  # We send back the list
            return HttpResponse(json.dumps(response))

        if ned_id == "cisco-ios-xr-id:cisco-ios-xr":

            jsonObject = NSO_GET_Show_IOSXR_Device_Interface_List(device)

            for intf_number in jsonObject["tailf-ned-cisco-ios-xr:interface"][intf_type]:
                data.append({'id': intf_number["id"], 'name': intf_number["id"]})

            response = { 'item_list':data }
            return HttpResponse(json.dumps(response))

        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse(json.dumps(response))

def NSO_Intro_Add_DNS_Service_View(request):

    if request.method == 'POST':
        form = forms.NSO_Intro_Add_DNS_Service_Form(request.POST)

        if form.is_valid():

            cd = form.cleaned_data

            name = cd.get('name')
            device = cd.get('device')
            dns_server_ip = cd.get('DNS_server')

            try:
                NSO_Intro_Add_DNS_Service(name, device, dns_server_ip)
                text = "Service Successfully Created"
            except requests.exceptions.RequestException as e:
                text = "Error: " + e

            return NSO_Intro_Result_View(request, text)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = forms.NSO_Intro_Add_DNS_Service_Form()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'NSO_Intro_Webdemo/add_dns_service.html', {'form': form})