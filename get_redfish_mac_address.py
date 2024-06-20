#! /usr/bin/python3

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import argparse
import subprocess
from pprint import pprint



# Arguments parsing
parser = argparse.ArgumentParser(description='tbd')
parser.add_argument('-R', '--url', action="store", help='Redfish Bmc Url, ex : https://<ip>')
parser.add_argument('-U', '--username', action="store", help='Username, ex : admin')
parser.add_argument('-P', '--password', action="store", help='Password, ex: password')
args = parser.parse_args()
url = args.url
username = args.username
password = args.password

# HTTP Header
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# get all installed NIC into the chassis
network_adapters_path = "/redfish/v1/Chassis/Self/NetworkAdapters"
try:
    response = requests.get(url + network_adapters_path, auth=(username, password), headers=headers, verify=False)
    if response.status_code == 200:
        print('--------------------------------------------------------------------------')
        for nic in response.json()['Members']:
            nic_url = nic['@odata.id']
            all_nic_info_response = requests.get(url + nic_url, auth=(username, password), headers=headers, verify=False)                                                                                                                 
            controllers = all_nic_info_response.json()['Controllers']
            pci_model_url = controllers[-1]['Links']['PCIeDevices'][-1]['@odata.id']
            pci_model_response =  requests.get(url + pci_model_url, auth=(username, password), headers=headers, verify=    False)                                                                                                         
            print('Redfish side : ')
            print(pci_model_response.json()['Name'])
            print(nic_url.split('/')[-1])
            print('\nLinux side :')
            ports = ['PORT_0','PORT_1']
            for mac_port in ports:
                mac_port_number = "/NetworkPorts/{}".format(mac_port)
                mac_response = requests.get(url + nic_url + mac_port_number, auth=(username, password), headers=headers, verify=False)                                                                                                    
                if 'ActiveLinkTechnology' in mac_response.json():
                    mac = mac_response.json()['AssociatedNetworkAddresses']
                    #print('BMC Redfish MAC Address: {}'.format(mac[-1].lower()))
                    #ps = subprocess.Popen(('/usr/sbin/ip', '-br', 'link'), stdout=subprocess.PIPE)
                    #output = subprocess.check_output(('grep', mac[-1].lower()), stdin=ps.stdout)
                    #print(output.decode('utf-8'))
                    cmd = "/usr/sbin/ip -br link | grep {}".format(mac[-1].lower())
                    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    output = ps.communicate()[0]

                    print(output.decode('utf8'))
            print('-----------------------------------')
    else:
        print("Erreur : ", response.status_code)
except requests.exceptions.RequestException as e:
    print("Erreur : ", e)
