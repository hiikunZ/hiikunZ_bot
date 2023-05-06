from datetime import datetime, timedelta, timezone
import requests
from cogs.utils.contestdata import ContestData


def get_contest_data():
    JST = timezone(timedelta(hours=+9), "JST")
    res = []
    load_url = "https://codeforces.com/api/contest.list"
    contest_list = requests.get(load_url).json()["result"]
    endcnt = 0
    for data in contest_list:
        contest_data = ContestData()
        if data["phase"] == "BEFORE":
            contest_data.Status = "Upcoming"
        elif data["phase"] == "CODING":
            contest_data.Status = "Running"
        else:
            contest_data.Status = "Finished"
            endcnt += 1
            if endcnt >= 5:
                break
        contest_data.Platform = "Codeforces"
        contest_data.Platformimage = "https://i.imgur.com/CdviAkE.png"
        contest_data.Starttime = datetime.fromtimestamp(
            data["startTimeSeconds"], tz=JST
        )
        contest_data.Url = "https://codeforces.com/contest/" + str(data["id"])
        contest_data.StandingsUrl = contest_data.Url + "/standings"
        contest_data.Name = data["name"].split("(")[0].strip()
        if "Codeforces Global Round" in contest_data.Name:
            contest_data.Type = "Codeforces Global Round"
            contest_data.Color = 0xFFFFFF
            contest_data.RatedRange = "All"
        elif "Educational Codeforces Round" in contest_data.Name:
            contest_data.Type = "Educational Codeforces Round"
        elif "Codeforces Round" in contest_data.Name:
            contest_data.Type = "Codeforces Round"
        else:
            contest_data.Type = "Other Codeforces Contest"
        name = data["name"].replace(". ", ".")
        if "Div.1" in name and "Div.2" in name:
            contest_data.Color = 0xC000C0
            contest_data.RatedRange = "Div.1 & Div.2"
        elif "Div.1" in name:
            contest_data.Color = 0xFF0000
            contest_data.RatedRange = "Div.1"
        elif "Div.2" in name:
            contest_data.Color = 0x0000FF
            contest_data.RatedRange = "Div.2"
        elif "Div.3" in name:
            contest_data.Color = 0xC0C000
            contest_data.RatedRange = "Div.3"
        elif "Div.4" in name:
            contest_data.Color = 0x008000
            contest_data.RatedRange = "Div.4"
        else:
            contest_data.Color = 0x000000

        contest_data.Duration = timedelta(seconds=data["durationSeconds"])
        contest_data.Endtime = contest_data.Starttime + contest_data.Duration
        res.append(contest_data)

    return res
