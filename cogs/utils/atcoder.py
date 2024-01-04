from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from cogs.utils.contestdata import ContestData


def get_contest_data():
    res = []
    load_url = "https://atcoder.jp/contests/?lang=ja"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    action = soup.find(id="contest-table-action")
    if action is not None:
        action = action.find_all("tr")
        for data in action[1:]:
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Running"
            contest_data.Platform = "AtCoder"
            contest_data.Platformimage = "https://i.imgur.com/Rhv0H2m.png"
            contest_data.Starttime = datetime.strptime(
                data[0].text, "%Y-%m-%d %H:%M:%S%z"
            )
            contest_data.Url = "https://atcoder.jp" + data[1].find("a").get("href")
            contest_data.ProblemAUrl = contest_data.Url + "/tasks/" + data[1].find("a").get("href").split("/")[-1] + "_a"
            contest_data.StandingsUrl = contest_data.Url + "/standings"
            contest_data.Name = data[1].find("a").text
            contesttype = data[1].find_all("span")[0].get("title")
            if contesttype == "Algorithm":
                if data[1].find_all("span")[1].get("class") == []:
                    contestcolor = None
                else:
                    contestcolor = data[1].find_all("span")[1].get("class")[0]
                if contestcolor == "user-blue":
                    contest_data.Type = "ABC"
                    contest_data.Color = 0x0000FF
                elif contestcolor == "user-orange":
                    contest_data.Type = "ARC"
                    contest_data.Color = 0xFF8000
                elif contestcolor == "user-red":
                    contest_data.Type = "AGC"
                    contest_data.Color = 0xFF0000
                else:
                    contest_data.Type = "Other Algorithm Contest"
                    contest_data.Color = 0x000000
            elif contesttype == "Heuristic":
                if "AtCoder Heuristic Contest" in contest_data.Name:
                    contest_data.Type = "AHC"
                    contest_data.Color = 0x008000
                else:
                    contest_data.Type = "Other Heuristic Contest"
                    contest_data.Color = 0x000000
            else:
                contest_data.Type = "Other AtCoder Contest"
                contest_data.Color = 0x000000
            contest_data.Duration = timedelta(
                seconds=int(data[2].text.split(":")[0]) * 3600
                + int(data[2].text.split(":")[1]) * 60
            )
            contest_data.Endtime = contest_data.Starttime + contest_data.Duration
            contest_data.RatedRange = data[3].text.replace(" ", "")
            if contest_data.RatedRange == "-":
                contest_data.RatedRange = "Unrated"
            res.append(contest_data)

    upcoming = soup.find(id="contest-table-upcoming")
    if upcoming is not None:
        upcoming = upcoming.find_all("tr")
        for data in upcoming[1:]:
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Upcoming"
            contest_data.Platform = "AtCoder"
            contest_data.Platformimage = "https://i.imgur.com/Rhv0H2m.png"
            contest_data.Starttime = datetime.strptime(
                data[0].text, "%Y-%m-%d %H:%M:%S%z"
            )
            contest_data.Url = "https://atcoder.jp" + data[1].find("a").get("href")
            contest_data.ProblemAUrl = contest_data.Url + "/tasks/" + data[1].find("a").get("href").split("/")[-1] + "_a"
            contest_data.StandingsUrl = contest_data.Url + "/standings"
            contest_data.Name = data[1].find("a").text
            contesttype = data[1].find_all("span")[0].get("title")
            if contesttype == "Algorithm":
                if data[1].find_all("span")[1].get("class") == []:
                    contestcolor = None
                else:
                    contestcolor = data[1].find_all("span")[1].get("class")[0]
                if contestcolor == "user-blue":
                    contest_data.Type = "ABC"
                    contest_data.Color = 0x0000FF
                elif contestcolor == "user-orange":
                    contest_data.Type = "ARC"
                    contest_data.Color = 0xFF8000
                elif contestcolor == "user-red":
                    contest_data.Type = "AGC"
                    contest_data.Color = 0xFF0000
                else:
                    contest_data.Type = "Other Algorithm Contest"
                    contest_data.Color = 0x000000
            elif contesttype == "Heuristic":
                if "AtCoder Heuristic Contest" in contest_data.Name:
                    contest_data.Type = "AHC"
                    contest_data.Color = 0x008000
                else:
                    contest_data.Type = "Other Heuristic Contest"
                    contest_data.Color = 0x000000
            else:
                contest_data.Type = "Other Contest"
                contest_data.Color = 0x000000
            contest_data.Duration = timedelta(
                seconds=int(data[2].text.split(":")[0]) * 3600
                + int(data[2].text.split(":")[1]) * 60
            )
            contest_data.Endtime = contest_data.Starttime + contest_data.Duration
            contest_data.RatedRange = data[3].text.replace(" ", "")
            if contest_data.RatedRange == "-":
                contest_data.RatedRange = "Unrated"
            res.append(contest_data)
    recent = soup.find(id="contest-table-recent")
    if recent is not None:
        recent = recent.find_all("tr")
        for data in recent[1:]:
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Finished"
            contest_data.Platform = "AtCoder"
            contest_data.Platformimage = "https://i.imgur.com/Rhv0H2m.png"
            contest_data.Starttime = datetime.strptime(
                data[0].text, "%Y-%m-%d %H:%M:%S%z"
            )
            contest_data.Url = "https://atcoder.jp" + data[1].find("a").get("href")
            contest_data.StandingsUrl = contest_data.Url + "/standings"
            contest_data.Name = data[1].find("a").text
            contesttype = data[1].find_all("span")[0].get("title")
            if contesttype == "Algorithm":
                if data[1].find_all("span")[1].get("class") == []:
                    contestcolor = None
                else:
                    contestcolor = data[1].find_all("span")[1].get("class")[0]
                if contestcolor == "user-blue":
                    contest_data.Type = "ABC"
                    contest_data.Color = 0x0000FF
                elif contestcolor == "user-orange":
                    contest_data.Type = "ARC"
                    contest_data.Color = 0xFF8000
                elif contestcolor == "user-red":
                    contest_data.Type = "AGC"
                    contest_data.Color = 0xFF0000
                else:
                    contest_data.Type = "Other Algorithm Contest"
                    contest_data.Color = 0x000000
            elif contesttype == "Heuristic":
                if "AtCoder Heuristic Contest" in contest_data.Name:
                    contest_data.Type = "AHC"
                    contest_data.Color = 0x008000
                else:
                    contest_data.Type = "Other Heuristic Contest"
                    contest_data.Color = 0x000000
            else:
                contest_data.Type = "Other Contest"
                contest_data.Color = 0x000000
            contest_data.Duration = timedelta(
                seconds=int(data[2].text.split(":")[0]) * 3600
                + int(data[2].text.split(":")[1]) * 60
            )
            contest_data.Endtime = contest_data.Starttime + contest_data.Duration
            contest_data.RatedRange = data[3].text.replace(" ", "")
            if contest_data.RatedRange == "-":
                contest_data.RatedRange = "Unrated"
            res.append(contest_data)
    return res
