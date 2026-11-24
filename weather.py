import requests

api_key ="264413a399ec47dc8f465851260302"
q=input("Enter the city name: ")
req=input("enter the current forcaste:")
base_url="http://api.weatherapi.com/v1/current.json"

if req=="current":
    complete_url=f"{base_url}/current.json"
    params={
        "key":api_key,
        "q":q
    }
response=requests.get(complete_url,params=params)

import pdb;pdb.set_trace()
