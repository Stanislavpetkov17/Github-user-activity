import urllib.request
import json

name = input("Enter github username:")
response = urllib.request.urlopen(f"https://api.github.com/users/{name}/events")
response_list = json.load(response)

fake_events = [
    {"type": "CreateEvent", "repo": {"name": "a/one"}, "payload": {"ref": "main", "ref_type": "branch"}},
    {"type": "CreateEvent", "repo": {"name": "b/two"}, "payload": {"ref": None, "ref_type": "repository"}},
]

for event in fake_events:
    if event["type"] == "PushEvent":
        print("Pushed to " + event["repo"]["name"])

    elif event["type"] == "WatchEvent":
        print("Starred " + event["repo"]["name"])

    elif event["type"] == "ForkEvent":
        print("Forked " + event["repo"]["name"])

    elif event["type"] == "CreateEvent":
        ref = event["payload"]["ref"]
        xtra = " "
        if ref is None:
            xtra = ""
            ref = ""
        print("Created " + event["payload"]["ref_type"] + xtra + ref + " in " + event["repo"]["name"])

    elif event["type"] == "ForkEvent":
        print("Forked " + event["repo"]["name"])

    elif event["type"] == "ForkEvent":
        print("Forked " + event["repo"]["name"])
