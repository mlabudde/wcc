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
        connection = urlopen(url)
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
            if line.startswith("<a href="):
                l1 = lines[i]
                l2 = lines[i + 1]
                player = Player.createPlayer(l1, l2)
                section.addPlayer(player)
                i = i + 2
            else:
                break
            i = i + 1
        return

    @classmethod
    def getEventHistory(cls, start_date=datetime.now(), end_date=datetime(day=1, month=1, year=1950)):
        out_set = []
        page = 1
        done = False
        while not done:
            url = BASE_AFFILIATE_URL + "." + str(page)
            connection = urlopen(url)
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
                        link = event.xpath("./td/a")[0].attrib["href"].split("?")[1]
                        out_set.append({"date": date,
                                        "link": BASE_URL + "?" + link,
                                        "name": event.xpath("./td/a")[0].text})
                    done = (date <= end_date)
            else:
                done = True

            page = page + 1

        return out_set
