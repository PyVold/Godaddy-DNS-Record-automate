##########################################################################                                                                                                                                                       
################################## PyVOLD ################################
########################### osama@ipdevops.com ###########################
##########################################################################
 
import requests
import json, os
from requests.auth import HTTPBasicAuth  #don't remove
 
api_key=""
api_secret=""
domains = ['domain2.com', 'domain2.com'] 

here = os.path.dirname(__file__)

def check_ip_address():
  # Option#1 CHECK Current IP address for the DNS RECORD FROM GODADDY
  '''
  DNS_A = requests.get(url, headers=headers)
  current_ip=DNS_A.json()[0]['data']
  '''
  
  # Option#2 Check DNS record from a file - to avoid many API requestes
  current_ip = open(os.path.join(here, '.newip'), 'r').readline()
  # Get the servers public IP address
  ipresponse = requests.get("http://ipv4bot.whatismyipaddress.com")
  public_ip = ipresponse.text

  return public_ip, current_ip

def compare_ips(public_ip, current_ip):
  if current_ip == public_ip:
      print("IP was not changed")
      data = []
  else:
      data = [
    {
      "data": public_ip,
      "name":"@",
      "ttl": 600,
      "type": "A"
    }
  ]
  return data

def update_dns_record(url, public_ip, current_ip, data):
    headers = {"Authorization" : "sso-key {}:{}".format(api_key, api_secret), 'Content-type':'application/json', 'Accept':'application/json'}
    post_address = requests.put(url, data=json.dumps(data), headers=headers)
    if post_address.status_code == 200:
        print("IP was changed from {} to {} for {}".format(current_ip, public_ip, url))
        # Write the update in the hidden file
        file = open(os.path.join(here, '.newip'),'w')
        file.write(public_ip)
        file.close()
    else:
        print('Error Occured')
        print(post_address.status_code)

def main():
  public_ip, current_ip = check_ip_address()
  data = compare_ips(public_ip, current_ip)
  if len(data) != 0:
    for domain in domains:
      url="https://api.godaddy.com/v1/domains/{}/records/A/%40".format(domain)
      update_dns_record(url, public_ip, current_ip, data)


# Run the script from here!
main()