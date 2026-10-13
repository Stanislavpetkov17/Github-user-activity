import urllib.request
import json

name = input("Enter github username:")
response = urllib.request.urlopen(f"https://api.github.com/users/{name}/events")
response_list = json.load(response)

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
        if "state" in event["payload"]["review"]:
            reviewstate = event["payload"]["review"]["state"]
        reviewaction = reviewaction.lower()
        reviewstate = reviewstate.lower()

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
        print("Did unknown event in " + event["repo"]["name"])