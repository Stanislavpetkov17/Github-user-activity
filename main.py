import urllib.request
import json

name = input("Enter github username:")
response = urllib.request.urlopen(f"https://api.github.com/users/{name}/events")
response_list = json.load(response)


for event in response_list:
    if event["type"] == "PushEvent":
        print("Pushed")
    print(event["type"])
    print(event["repo"]["name"])




#print(response_list[0]["repo"]["name"])
#print(response_list[0]["payload"])

