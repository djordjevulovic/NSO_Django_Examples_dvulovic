"""NSO_Django_Examples_dvulovic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from NSO_Intro_Webdemo import views;
from django.http import HttpResponse

urlpatterns = [
    url(r'^test/', views.test, name='NSO Test'),
    url(r'^nso_intro/$', views.NSO_Intro_Main_View, name='NSO Intro Webdemo'),
    url(r'^nso_intro/show_device_config/$', views.NSO_Intro_Show_Device_Config_View, name='Show Device Config'),
    url(r'^nso_intro/show_interface_config/$', views.NSO_Intro_Show_Interface_Config_View, name='Show Interface Config'),
    url(r'^a/get/intf_type/?$', views.NSO_Intro_Show_Interface_Config_View_get_intf_types, name='get_intf_types'),
    url(r'^a/get/intf_number/?$', views.NSO_Intro_Show_Interface_Config_View_get_intf_numbers, name='get_intf_numbers'),
    url(r'^nso_intro/add_dns_service/$', views.NSO_Intro_Add_DNS_Service_View, name='Add DNS Service'),
]
