from urllib.request import urlopen
from ..utils import anchor

BASE_URL = 'http://www.uschess.org/msa/XtblMain.php'


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
        section = cls.createSection(name, "Section " + sn, href)
        return section

    @classmethod
    def getSectionImpl(cls, section, lines, i):
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("<a href="):
                l1 = lines[i]
                l2 = lines[i + 1]
                player = player.createPlayer(l1, l2)
                section.addPlayer(player)
                i = i + 2
            else:
                break
            i = i + 1
        return
