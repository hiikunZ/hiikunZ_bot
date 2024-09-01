from datetime import datetime, timedelta, timezone
import requests

from cogs.utils.contestdata import ContestData


def get_contest_data():
    JST = timezone(timedelta(hours=+9), "JST")
    res = []
    load_url = "https://alpacahack.com/ctfs?_data=routes%2F_root.ctfs"
    contest_list = requests.get(load_url, headers={"User-Agent": "Bot"}).json()
    contest_list = contest_list["ctfs"]
    for data in contest_list:
        if data["isMirror"]:
            continue

        contest_data = ContestData()
        contest_data.Status = data["status"].capitalize()
        contest_data.Platform = "AlpacaHack"
        contest_data.Platformimage = "https://i.imgur.com/QjP1KSh.png"
        contest_data.Starttime = datetime.fromtimestamp(
            data["startAt"]["value"] // 1000
        ).astimezone(JST)
        contest_data.Endtime = datetime.fromtimestamp(
            data["endAt"]["value"] // 1000
        ).astimezone(JST)
        contest_data.Duration = contest_data.Endtime - contest_data.Starttime
        contest_data.Url = "https://alpacahack.com/ctfs/" + data["canonicalName"]
        contest_data.StandingsUrl = contest_data.Url + "/scoreboard"
        contest_data.Name = data["name"]
        contest_data.Type = "AlpacaHack Contest"
        contest_data.Color = 0xF04328
        contest_data.RatedRange = "No data"
        res.append(contest_data)
    return res
