from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup
import re

from cogs.utils.contestdata import ContestData


def get_contest_data():
    JST = timezone(timedelta(hours=+9), "JST")
    res = []
    load_url = "https://yukicoder.me/contests"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    action = soup.find_all("table")[0]
    if action is not None:
        action = action.find_all("tr")
        for data in action[1:]:
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Running"
            contest_data.Platform = "yukicoder"
            contest_data.Platformimage = "https://i.imgur.com/jnamIn1.png"
            start = re.sub("\(.\)", "", data[1].text.split("〜")[0]).strip()
            end = re.sub("\(.\)", "", data[1].text.split("〜")[1]).rstrip()
            contest_data.Starttime = datetime.strptime(
                start + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Endtime = datetime.strptime(
                end + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Url = "https://yukicoder.me" + data[0].find("a").get("href")
            contest_data.StandingsUrl = "https://yukicoder.me" + data[4].find("a").get(
                "href"
            )
            contest_data.Name = data[0].find("a").text
            contest_data.Type = "yukicoder Contest"
            contest_data.Color = 0x3B4250
            contest_data.Duration = contest_data.Endtime - contest_data.Starttime
            contest_data.RatedRange = "Unrated"
            res.append(contest_data)
    upcoming = soup.find_all("table")[1]
    if upcoming is not None:
        upcoming = upcoming.find_all("tr")
        for data in upcoming[1:]:
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Upcoming"
            contest_data.Platform = "yukicoder"
            contest_data.Platformimage = "https://i.imgur.com/jnamIn1.png"
            start = re.sub("\(.\)", "", data[1].text.split("〜")[0]).strip()
            end = re.sub("\(.\)", "", data[1].text.split("〜")[1]).rstrip()
            contest_data.Starttime = datetime.strptime(
                start + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Endtime = datetime.strptime(
                end + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Url = "https://yukicoder.me" + data[0].find("a").get("href")
            contest_data.StandingsUrl = "https://yukicoder.me" + data[4].find("a").get(
                "href"
            )
            contest_data.Name = data[0].find("a").text
            contest_data.Type = "yukicoder Contest"
            contest_data.Color = 0x3B4250
            contest_data.Duration = contest_data.Endtime - contest_data.Starttime
            contest_data.RatedRange = "Unrated"
            res.append(contest_data)
    recent = soup.find_all("table")[2]
    if recent is not None:
        recent = recent.find_all("tr")
        cnt = 0
        for data in recent[1:]:
            cnt += 1
            if cnt > 5:
                break
            data = data.find_all("td")
            contest_data = ContestData()
            contest_data.Status = "Finished"
            contest_data.Platform = "yukicoder"
            contest_data.Platformimage = "https://i.imgur.com/jnamIn1.png"
            start = re.sub("\(.\)", "", data[1].text.split("〜")[0]).strip()
            end = re.sub("\(.\)", "", data[1].text.split("〜")[1]).rstrip()
            contest_data.Starttime = datetime.strptime(
                start + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Endtime = datetime.strptime(
                end + "+0900", "%Y-%m-%d  %H:%M:%S%z"
            )
            contest_data.Url = "https://yukicoder.me" + data[0].find("a").get("href")
            contest_data.StandingsUrl = "https://yukicoder.me" + data[4].find("a").get(
                "href"
            )
            contest_data.Name = data[0].find("a").text
            contest_data.Type = "yukicoder Contest"
            contest_data.Color = 0x3B4250
            contest_data.Duration = contest_data.Endtime - contest_data.Starttime
            contest_data.RatedRange = "Unrated"
            res.append(contest_data)
    return res
