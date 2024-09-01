import asyncio
import aiohttp
from sys import argv


url = "https://api.github.com/users/{username}/events"
EVENTS = ["issue", "commits"]


def get_repo(activity: dict[str, dict[str, str]]) -> str:
    return activity["repo"]["url"].split("/repos/")[-1]


def categorize(categorized_activities: dict, payload: dict, repo: str) -> dict:
    categorized_activities["others"] = []
    added = False
    for event in EVENTS:
        if event in payload:
            if event not in categorized_activities:
                categorized_activities[event] = {}
            if repo in categorized_activities[event]:
                categorized_activities[event][repo] += 1
                added = True
            else:
                categorized_activities[event][repo] = 1
                added = True
    else:
        if not added:
            categorized_activities["others"].append(payload)
    return categorized_activities


def get_categorized_activities(activities: list[dict[str, dict[str, str]]]):
    categorized_activities = dict()
    for activity in activities:
        payload = activity["payload"]
        repo = get_repo(activity)
        categorized_activities = categorize(
            categorized_activities=categorized_activities, payload=payload, repo=repo
        )
    return categorized_activities


def print_categorized_activities(categorized_activites: dict[str, dict | list]):
    print("Output:")
    for commit in categorized_activites["commits"]:
        print(
            f"- Pushed {categorized_activites["commits"][commit]} commits to {commit}"
        )
    for issue in categorized_activites["issue"]:
        print(f"- Opened {categorized_activites["issue"][issue]} new issue in {issue}")


async def get_activity():
    if len(argv) != 2:
        raise SystemError("Usage: python github_activity <username>")
    username = argv[1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url.format(username=username)) as response:
            activities = await response.json()
    categorized_activities = get_categorized_activities(activities=activities)
    return categorized_activities


if __name__ == "__main__":
    categorized_activites = asyncio.run(get_activity())
    print_categorized_activities(categorized_activites=categorized_activites)
