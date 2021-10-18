import requests
import json
from requests.auth import HTTPBasicAuth  #don't remove

api_key=""
api_secret=""
domain = "mydomain.com"


headers = {"Authorization" : "sso-key {}:{}".format(api_key, api_secret), 'Content-type':'application/json', 'Accept':'application/json'}
url="https://api.godaddy.com/v1/domains/{}/records/A/%40".format(domain)

DNS_A = requests.get(url, headers=headers)

# Get the servers public IP address
ipresponse = requests.get("http://ipv4bot.whatismyipaddress.com")

current_ip=DNS_A.json()[0]['data']
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
    print(post_address.json())
    print("IP was changed from {} to {}".format(current_ip,public_ip)) 
