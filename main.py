import urllib.request
from urllib.error import HTTPError, URLError
import json

name = input("Enter github username:")
if name == "":
    print("Please enter a valid username")
else:
    try:
        response = urllib.request.urlopen(f"https://api.github.com/users/{name}/events")
        response_list = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            print("Username not found")
        else:
            print(f"Error {error.code}")
    except URLError:
        print("Could not connect to Github")
    else:
        for event in response_list:
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

            elif event["type"] == "DeleteEvent":
                print("Deleted " + event["payload"]["ref_type"] + " " + event["payload"]["ref"] + " in " + event["repo"]["name"])

            elif event["type"] == "ReleaseEvent":
                print("Published release " + event["payload"]["release"]["tag_name"] + " in " + event["repo"]["name"])

            elif event["type"] == "IssuesEvent":
                issueaction = event["payload"]["action"]
                print(issueaction.capitalize() + " an issue in " + event["repo"]["name"])

            elif event["type"] == "IssueCommentEvent":
                comment_type = "issue"
                xtra2 = "an "
                if "pull_request" in event["payload"]["issue"]:
                    comment_type = "pull request"
                    xtra2 = "a "
                print("Commented on " + xtra2 + comment_type + " in " + event["repo"]["name"])

            elif event["type"] == "PullRequestEvent":
                pullaction = event["payload"]["action"]
                if pullaction == "closed" and "merged" in event["payload"]["pull_request"] and event["payload"]["pull_request"]["merged"] is True:
                    pullaction = "Merged"
                print(pullaction.capitalize() + " a pull request" + " in " + event["repo"]["name"])

            elif event["type"] == "PullRequestReviewEvent":
                reviewaction = event["payload"]["action"]
                reviewstate = "unknown"
                if "state" in event["payload"]["review"]:
                    reviewstate = event["payload"]["review"]["state"]
                    reviewstate = reviewstate.lower()
                reviewaction = reviewaction.lower()

                if reviewaction == "created" and reviewstate == "commented":
                    print("Reviewed a pull request in " + event["repo"]["name"])

                elif reviewaction == "created":
                    reviewaction = reviewstate
                    if reviewaction == "changes_requested":
                        reviewaction = "requested changes on"
                    print(reviewaction.capitalize() + " a pull request in " + event["repo"]["name"])

                else:
                    print(reviewaction.capitalize() + " a review on a pull request in " + event["repo"]["name"])

            elif event["type"] == "PullRequestReviewCommentEvent":
                print("Commented on code in a pull request in " + event["repo"]["name"])

            else:
                print("Other activity in " + event["repo"]["name"])