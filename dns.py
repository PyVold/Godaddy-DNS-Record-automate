##########################################################################                                                                                                                                                       
################################## PyVOLD ################################
########################### osama@ipdevops.com ###########################
##########################################################################
 
import requests
import json
from requests.auth import HTTPBasicAuth  #don't remove
 
api_key="dKYdWjinTtCF_Kr3mSoyBdZf1gSJJ8HMn3y"
api_secret="7SxTMTHZtaFt4UGoynp1j7"
domain = "packetshow.com"
 
 
headers = {"Authorization" : "sso-key {}:{}".format(api_key, api_secret), 'Content-type':'application/json', 'Accept':'application/json'}
url="https://api.godaddy.com/v1/domains/{}/records/A/%40".format(domain)
 
 
# Option#1 CHECK Current IP address for the DNS RECORD FROM GODADDY
'''
DNS_A = requests.get(url, headers=headers)
current_ip=DNS_A.json()[0]['data']
'''
 
# Option#2 Check DNS record from a file - to avoid many API requestes
current_ip = open('.newip', 'r').readline()
 
# Get the servers public IP address
ipresponse = requests.get("http://ipv4bot.whatismyipaddress.com")
 
public_ip= ipresponse.text
 
if current_ip == public_ip:
    print("IP was not changed")
else:
    data = [
  {
    "data": public_ip,
    "name":"@",
    "ttl": 600,
    "type": "A"
  }
]
    post_address = requests.put(url, data=json.dumps(data), headers=headers)
    if post_address.status_code == 200:
        print("IP was changed from {} to {}".format(current_ip,public_ip))
        # Write the update in the hidden file
        file = open('.newip','w')
        file.write(public_ip)
        file.close()
    else:
        print('Error Occured')
        print(post_address.status_code)
 # EOF
