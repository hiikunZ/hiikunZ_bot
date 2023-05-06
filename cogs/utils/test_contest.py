from datetime import datetime, timedelta, timezone
import requests

# from cogs.utils.contestdata import ContestData
from contestdata import ContestData


def get_contest_data():
    JST = timezone(timedelta(hours=+9), "JST")
    res = []
    load_url = (
        "https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc"
    )
    contest_list = requests.get(load_url).json()
    action = contest_list["present_contests"]
    for data in action:
        contest_data = ContestData()
        contest_data.Status = "Running"
        contest_data.Platform = "CodeChef"
        contest_data.Platformimage = "https://i.imgur.com/B9oJvqG.png"
        contest_data.Starttime = datetime.strptime(
            data["contest_start_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        if "contest_end_date_iso" not in data:
            continue
        contest_data.Endtime = datetime.strptime(
            data["contest_end_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        contest_data.Duration = contest_data.Endtime - contest_data.Starttime
        contest_data.Url = "https://www.codechef.com/" + data["contest_code"]
        contest_data.StandingsUrl = (
            "https://www.codechef.com/rankings/" + data["contest_code"] + "A"
        )
        contest_data.Name = data["contest_name"].split("(")[0].strip()
        contest_data.Type = "CodeChef Contest"
        contest_data.Color = 0x713C1D
        if "(" in data["contest_name"]:
            contest_data.RatedRange = data["contest_name"].split("(")[1].split(")")[0]
            contest_data.RatedRange = contest_data.RatedRange.replace("Rated for ", "")
        res.append(contest_data)
    upcoming = contest_list["future_contests"]
    for data in upcoming:
        contest_data = ContestData()
        contest_data.Status = "Upcoming"
        contest_data.Platform = "CodeChef"
        contest_data.Platformimage = "https://i.imgur.com/B9oJvqG.png"
        contest_data.Starttime = datetime.strptime(
            data["contest_start_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        if "contest_end_date_iso" not in data:
            continue
        contest_data.Endtime = datetime.strptime(
            data["contest_end_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        contest_data.Duration = contest_data.Endtime - contest_data.Starttime
        contest_data.Url = "https://www.codechef.com/" + data["contest_code"]
        contest_data.StandingsUrl = (
            "https://www.codechef.com/rankings/" + data["contest_code"] + "A"
        )
        contest_data.Name = data["contest_name"].split("(")[0].strip()
        contest_data.Type = "CodeChef Contest"
        contest_data.Color = 0x713C1D
        if "(" in data["contest_name"]:
            contest_data.RatedRange = data["contest_name"].split("(")[1].split(")")[0]
            contest_data.RatedRange = contest_data.RatedRange.replace("Rated for ", "")
        res.append(contest_data)
    cnt = 0
    recent = contest_list["past_contests"]
    for data in recent:
        cnt += 1
        if cnt > 5:
            break
        contest_data = ContestData()
        contest_data.Status = "Finished"
        contest_data.Platform = "CodeChef"
        contest_data.Platformimage = "https://i.imgur.com/B9oJvqG.png"
        contest_data.Starttime = datetime.strptime(
            data["contest_start_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        if "contest_end_date_iso" not in data:
            continue
        contest_data.Endtime = datetime.strptime(
            data["contest_end_date_iso"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(JST)
        contest_data.Duration = contest_data.Endtime - contest_data.Starttime
        contest_data.Url = "https://www.codechef.com/" + data["contest_code"]
        contest_data.StandingsUrl = (
            "https://www.codechef.com/rankings/" + data["contest_code"] + "A"
        )
        contest_data.Name = data["contest_name"].split("(")[0].strip()
        contest_data.Type = "CodeChef Contest"
        contest_data.Color = 0x713C1D
        if "(" in data["contest_name"]:
            contest_data.RatedRange = data["contest_name"].split("(")[1].split(")")[0]
            contest_data.RatedRange = contest_data.RatedRange.replace("Rated for ", "")
        res.append(contest_data)
    return res


r = get_contest_data()
for i in r:
    print(i.Name)
    print(i.Starttime)
    print(i.Endtime)
    print(i.Duration)
    print(i.Url)
    print(i.StandingsUrl)
    print(i.RatedRange)
    print(i.Type)
    print(i.Color)
    print(i.Platform)
    print(i.Platformimage)
    print(i.Status)
