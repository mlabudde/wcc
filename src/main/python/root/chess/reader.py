import json
import urllib
from datetime import datetime
from urllib.request import urlopen
from root.chess.player import Player
from root.chess.section import Section
from root.utils import anchor

from lxml import html

BASE_URL = 'http://www.uschess.org/msa/XtblMain.php'
BASE_AFFILIATE_URL = "https://www.uschess.org/msa/AffDtlTnmtHst.php?A5008948"


class Reader:

    # @classmethod
    # def createReader(cls):
    #     aReader = Reader()
    #     return aReader

    @classmethod
    def getHtml(cls, tournamentId: str, section: str):
        url = BASE_URL + "?" + tournamentId + ("" if section is None else ("." + section))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        connection = urlopen(req)
        raw = connection.read()
        return raw.decode("utf-8")

    @classmethod
    def getSectionsFromHtml(cls, html):
        lines = html.splitlines(True)
        return cls.getSectionsFromLines(lines)

    @classmethod
    def getSectionsFromLines(cls, lines):
        links = cls.getSectionLinks(lines)
        sections = cls.getSectionsFromLinks(links)

        if len(sections) == 0:
            sections.append(cls.createSection("<a href=XtblMain.php?202503267692.1><b>Section 1</b></a>"))

        for section in sections:
            search = "<b>" + section.getUscfName()
            seekStart = False
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.startswith(search):
                    seekStart = True
                if seekStart & line.startswith(" Num  | USCF ID"):
                    cls.getSectionImpl(section, lines, (i + 2))
                    break
                i = i + 1

        return sections

    @classmethod
    def getSectionLinks(cls, lines):
        links = []
        for line in lines:
            if line.startswith("<a href=XtblMain.php?"):
                links.append(line)
        return links

    @classmethod
    def getSectionsFromLinks(cls, links):
        sections = []
        for link in links:
            section = cls.createSection(link)
            sections.append(section)
        return sections

    @classmethod
    def createSection(cls, link):
        name = anchor.getText(link)
        href = anchor.getHref(link)
        parts = href.split(".")
        last = len(parts) - 1
        sn = parts[last]
        section = Section.createSection(name, "Section " + sn, href)
        return section

    @classmethod
    def getSectionImpl(cls, section, lines, i):
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Num  | USCF ID"):  # ran over section...
                return

            if line.startswith("<a href="):
                l1 = lines[i]
                l2 = lines[i + 1]
                player = Player.createPlayer(l1, l2)
                section.addPlayer(player)
                i = i + 1
            i = i + 1
        return

    @classmethod
    def getEventHistory(cls, start_date=datetime.now(), end_date=datetime(day=1, month=1, year=1950)):
        out_set = []
        page = 1
        done = False
        while not done:
            url = BASE_AFFILIATE_URL + "." + str(page)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            connection = urlopen(req)
            raw = connection.read()
            event_html = raw.decode("utf-8")
            tree = html.fromstring(event_html)
            events = tree.xpath('//tr[ ./td/a[contains(@href,"XtblMain")]]')
            # events = tree.xpath("//body/table/tbody/tr/td/center/table/tbody/tr/table")
            if len(events) > 0:
                for event in events:
                    parts = event.xpath("./td")[0].text.split('-')
                    date = datetime(month=int(parts[1]), day=int(parts[2]), year=int(parts[0]))
                    if start_date >= date >= end_date:
                        event_id = event.xpath("./td/a")[0].attrib["href"].split("?")[1]
                        out_set.append({"date": date,
                                        "link": BASE_URL + "?" + event_id,
                                        "event_id": event_id,
                                        "name": event.xpath("./td/a")[0].text.
                                       title().replace("Wcc", "WCC").replace("Swcc", "SWCC").replace(" Cc ", " CC ")
                                        })
                    done = (date <= end_date)
            else:
                done = True

            page = page + 1

        return out_set

    @classmethod
    def getEventWinners(cls, eventID):
        section = cls.getSectionsFromHtml(cls.getHtml(eventID, ""))
        winScore = -1
        outName = ""

        if len(section) < 1:
            return ""
        players = section[0].players

        for p in players:
            if winScore == -1:
                winScore = float(p.total)
            thisScore =  float(p.total)
            if thisScore == winScore:
                outName = outName + p.name + ",<br/> "
        return outName[:-7]

    @classmethod
    def getWinners(cls, start_date=datetime.now(), end_date=datetime(day=1, month=1, year=1950)):

        f = open('data/Winners.json')
        winners = json.load(f)

        # return 1 record/year with year, ccLink, ccWinner(s), memLink, memWinner(s) that can be directly printed as html
        #for each year from now year to 1950
        #   for the mem link and cc link
        #       get the 1st section and retreive the winner(s) names
        #       package link and names for return

        out_set = []
        for year in range(datetime.now().year,1950,-1):
            memRef = [w for w in winners["memorial"] if w["eventYear"] == str(year)]
            ccRef = [w for w in winners["clubChp"] if w["eventYear"] == str(year)]

            if memRef == [] and ccRef == []:
                return out_set
            memWinner = ""
            memLink = ""
            if memRef != []:
                if memRef[0]["eventID"] == "x":
                    memWinner = memRef[0]["winner"]
                else:
                    memWinner = cls.getEventWinners(memRef[0]["eventID"])
                    memLink = BASE_URL + "?" + memRef[0]["eventID"] + ".1"
            ccWinner = ""
            ccLink = ""
            if ccRef != []:
                if ccRef[0]["eventID"] == "x":
                    ccWinner = ccRef[0]["winner"]
                else:
                    ccWinner = cls.getEventWinners(ccRef[0]["eventID"])
                    ccLink = BASE_URL + "?" + ccRef[0]["eventID"] + ".1"

            out_set.append({"year": year,
                            "memLink": memLink,
                            "memWinner": memWinner,
                            "ccLink": ccLink,
                            "ccWinner": ccWinner
                            })

        return out_set
