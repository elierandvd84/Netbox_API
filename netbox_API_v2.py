import datetime
import json

import nmap
import paramiko
import requests
from urllib3.exceptions import InsecureRequestWarning

# Temporary removed this import
#requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# HI NATI
# SSH configuration for IPAM server
port = "22"
ip = "10.213.17.21"
username = "radware"
password = "radware"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)

# Hi NaTI
# API configuration for IPAM Netbox server

url ='http://10.213.17.21/api/ipam/ip-addresses/?limit=200'

switchuser='maory'
switchpassword='shukizik12'
myheaders={'content-type':'application/json', 'Authorization':'Token  bf15f47d0b65747c8fcf79db6088f98f0b79b82e'}

params = {"token": "bf15f47d0b65747c"
                   ""
                   "8fcf79db6088f98f0b79b82e"}


# #   Getting the current nmap IP's from IPAM server
   # stdin, stdout, stderr = ssh.exec_command("cat /home/radware/netbox_Test/final_ip_list.txt")
   # list_of_nmap_ip = stdout.readlines()
   # #print(list_of_nmap_ip)
   # resp = ''.join(list_of_nmap_ip)
   # #print(resp)

#   Getting the IP's from Netbox server
response = requests.get(url, verify=False, headers=myheaders)
res_json = response.json()
#print(response.text)
   #print(res_json)

   # for x in res_json:
   #     print(x)
   #
   # print(json.dumps(res_json, indent=4))
   # print(res_json["results"])

list_of_ipam_ip = res_json["results"]
ip_list_netbox = [sub['address'] for sub in list_of_ipam_ip]
host_id_list = [sub['id'] for sub in list_of_ipam_ip]
#print(host_id_list)
#print(ip_list_netbox)

# GET ID from Given IP
id = [x['id'] for x in list_of_ipam_ip if x['address'] == "10.213.17.10/24"]
#print(id)


# Filter only 10.213.17.x network from ip_list_netbox

new_ip_list = [ip for ip in ip_list_netbox if "10.213.17" in ip]
# for ip in ip_list_netbox:
#     if "10.213.17" in ip:
#         new_ip_list.append(ip)

nm = nmap.PortScanner()
# If you want to do a pingsweep on network 192.168.1.0/24:
nm.scan(hosts='10.213.17.1-254/24', arguments='-sP -PI')
nmap_host_list = nm.all_hosts()
# for i in range(len(nmap_host_list)):
#    print(nmap_host_list[i])


# new_nmap_list = []
# for ip in new_nmap_list:
#    new_nmap_list.append(ip.replace("\n", "/24"))


print("\nips from Netbox \n")
print("---------------------")
print(new_ip_list)
print("\nips from nmap \n")
print("---------------------")
print(nmap_host_list)

#Compare between 2 list of ip's and find different:

list_to_del = [item for item in new_ip_list if item not in nmap_host_list]
print("differnet between the 2 list to DELETE\n")
print(list_to_del)
print("number of unuiqe ip's {}".format(len(list_to_del)))


list_to_add = [item for item in nmap_host_list if item not in new_ip_list]
print("differnet between the 2 list to ADD \n")
print(list_to_add)
print("number of unuiqe ip's {}".format(len(list_to_add)))

list_add_test = ['10.213.17.12/24', '10.213.17.61/24']

# current_time = datetime.datetime.now()
# print(current_time)

#Adding missing IP's in API:

   # for ip in list_add_test:
   #
   #     current_time = datetime.datetime.now()
   #     current_time =str(current_time)
   #     payload = {
   #
   #                 "id": 47,
   #                 "family": {
   #                     "value": 4,
   #                     "label": "IPv4"
   #                 },
   #                 "address": ip,
   #                 "dns_name": "",
   #                 "description": "Add_by_API",
   #                 "tags": [
   #                     "VDP_Lab"
   #                 ],
   #                 "custom_fields": {},
   #                 "created": "2019-12-05",
   #                 "last_updated": current_time
   #
   #     }
   #     response = requests.post(url, data=json.dumps(payload), verify=False, headers=myheaders)

#Delete ip by ID
# use only the ID with DELETE API no DATA needed.

url='http://10.213.17.21/api/ipam/ip-addresses/72/'

response = requests.delete(url, verify=False, headers=myheaders)



#Old Nmap scan used <--
   #nm.scan(hosts='10.213.17.0/24')
   #hosts_list=[(x, nm[x]['status']['state']) for x in nm.all_hosts()]
   #for host, status in hosts_list:
   #print('{0}:{1}'.host)

print('----------------------------------------------------')

#hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
 # Printing tests:  
   #print(nm.all_hosts())
   #print(type(nm.all_hosts()))
   #print (type(nm))
   # for host, status in hosts_list:
   #   print('{0}:{1}'.format(host, status))
   #print(nm["10.213.17.203"])





