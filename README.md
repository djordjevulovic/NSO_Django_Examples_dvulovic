# Example Django Web application for Cisco Network Services Orchestrator (NSO)

## Introduction

[Cisco Network Services Orchestrator (NSO) enabled by Tail-f®] (http://www.cisco.com/c/en/us/solutions/service-provider/solutions-cloud-providers/network-services-orchestrator-solutions.html) is an industry-leading orchestration platform for hybrid networks. One of the main advantaes of NSO is comprehensive set of northbound APIs, rendered from the models. With those APIs, NSO can be easily integrated with northbound systems such as operation support systems (OSSs) and self-service portals.

In this example, we will provide a demo of the northbond application integrated with Cisco NSO using REST API. Application is created by [Django framework] (https://www.djangoproject.com/), providing easy-to-use Web interface. This simple app has three parts (pages):
- "Show Devices Configuration" will show full configuration of a device in JSON format. Input form contains combo-box for choosing device, which will be pre-propulated with evices available to NSO.
- "Show Interface Configuration" will configuration of a device interface in JSON format. Input form contains combo-boxes for available device and then available interface types and interface numbers for this specific device. When changing device, interface type/number boxes will automatically change.
- "Add New DNS Service" will deploy instance of a simple service for puting new DNS server configuration. Input form conatins text box for service name, combo box for device, and text box for IP address for DNS server.

## Instructions

To run the application, use the following steps (skip the ones which you have already performed):
- This application is designed to use NSO instance from [Cisco dCloud] (https://dcloud.cisco.com/) lab ["Cisco NSO Lab - L2VPN Service Design with XML Templates v1"] (https://dcloud2-lon.cisco.com/content/demo/67315). Before running the application, make sure you do the following (all these steps are thoroughly described in the dCloud documentation):
  - Register for Cisco.com account (http://www.cisco.com/web/siteassets/account/index.html)
  - Schedule lab session
  - Connect to VPN using Anyconnect(https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Install Python 3 and Django (https://docs.djangoproject.com/en/1.10/intro/install/)
- Install Git client 
- Clone project from the Github ("git clone https://github.com/djordjevulovic/NSO_Django_Examples_dvulovic")
- Run application on port 8888 ("python manage.py runserver 8888")
- Go to your preferred browser (tested with Chrome) and enter URL of the main page ("http://127.0.0.1:8888/nso_intro/")

## Developer notes
