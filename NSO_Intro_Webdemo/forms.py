from django import forms
from nso_helper_dvulovic import NSO_GET_Device_List

def get_device_list():

    jsonObject = NSO_GET_Device_List()

    device_list = []

    for device_entry in jsonObject["device"]:
        device_list.append([device_entry["name"], device_entry["name"]])

    return device_list

class NSO_Intro_Show_Device_Config_Form(forms.Form):

    device = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['device'] = forms.ChoiceField(choices=get_device_list(),help_text="Device:");

class NSO_Intro_Show_Interface_Config_Form(forms.Form):

    device = forms.ChoiceField()

    intf_type = forms.ChoiceField()

    intf_number = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        device_list = get_device_list()

        self.fields['device'] = forms.ChoiceField(choices=device_list,help_text="Device:", widget=forms.Select(attrs={'id': 'id_device'}))

        self.fields['intf_type'] = forms.ChoiceField(choices=[], help_text="Interface Type:", widget=forms.Select(attrs={'id': 'id_intf_type'}))

        self.fields['intf_number'] = forms.ChoiceField(choices=[], help_text="Interface Number:", widget=forms.Select(attrs={'id': 'id_intf_number'}))

class NSO_Intro_Add_DNS_Service_Form(forms.Form):

    name = forms.CharField()

    device = forms.ChoiceField()

    DNS_server = forms.CharField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(max_length=128, help_text="Name:")

        self.fields['device'] = forms.ChoiceField(choices=get_device_list(),help_text="Device:")

        self.fields['DNS_server'] = forms.CharField(max_length=128, help_text="DNS server:")
