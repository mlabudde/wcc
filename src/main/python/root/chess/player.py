from root.utils import anchor
from root.utils import String


class Player:

    def __init__(self):
        self.id = ""
        self.rank = ""
        self.name = ""
        self.state = ""
        self.ratePre = ""
        self.ratePost = ""
        self.rounds = list()
        self.total = ""

    @classmethod
    def createPlayer(cls, line1, line2):
        aPlayer = Player()
        cls.parseLineOne(aPlayer, line1)
        cls.parseLineTwo(aPlayer, line2)
        # aPlayer.printHtml()
        # print("")
        return aPlayer

    @classmethod
    def parseLineOne(cls, thePlayer, theLine):
        # TODO:
        #   player.rank, player.name, player.total, player.rounds
        #     <a href=XtblPlr.php?202207138352-001-14279562>5</a> | <a href=MbrDtlMain.php?14279562>JASON MICHAEL MARKOWSKI</a>         |2.5  |W  16|W   4|L   3|D   6|
        line = theLine.strip()
        items = line.split("|")
        if len(items) >= 2:
            rank = anchor.getText(items[0])
            thePlayer.rank = rank

            name = anchor.getText(items[1])
            thePlayer.name = String.massageName(name)

        if len(items) > 2:
            thePlayer.total = items[2]
            for i in range(3, len(items) - 1):
                rnd = items[i]
                thePlayer.rounds.append(rnd)
        return thePlayer

    @classmethod
    def parseLineTwo(cls, thePlayer, theLine):
        line = theLine.strip()
        thePlayer.state = line[0:2]
        thePlayer.id = line[5:13]
        rating = line[19:35]
        pos = rating.index("->")
        pre = rating[0:pos]
        post = rating[pos + 2:]
        thePlayer.ratePre = pre.strip()
        thePlayer.ratePost = post.strip()
        # TODO: the colors for each round!
        return thePlayer

    def parse(self, elements, numRounds):
        length = len(elements)
        idx = length - 1
        for i in range(numRounds):
            rnd = self.fixRound(elements[idx - i])
            self.rounds.insert(0, rnd)

        self.ratePost = elements[length - numRounds - 1]
        self.ratePre = elements[length - numRounds - 2]
        self.state = elements[length - numRounds - 3]

        self.id = elements[0]
        self.rank = elements[1]
        self.name = elements[2]
        self.state = elements[3]

        # if length == (6 + numRounds):
        #     self.name = elements[2] + " " + elements[3]
        # elif length == (7 + numRounds):
        #     self.name = elements[2] + " " + elements[3]
        #     self.state = elements[4]
        # elif length == (8 + numRounds):
        #     self.name = elements[2] + " " + elements[3] + " " + elements[4]
        #     self.state = elements[5]
        # elif length < (6 + numRounds):
        #     print("ERROR - less than 11 elements in array!\n\n")
        # elif length > (8 + numRounds):
        #     print("ERROR - more than 13 elements in array!\n\n")

        self.name = String.massageName(self.name)  # self.massageName()

    def fixRound(self, aRound):
        rnd = aRound.replace("-", "")
        if len(rnd) == 2 and rnd[1] == '0':
            rnd = rnd[0]
        return rnd

    # def getHtml(self):
    #     return self.toHtmlString()

    def printHtml(self):
        print(self.toHtml())

    def toHtml(self):
        buffer = ""
        buffer += ("<tr>\n")
        buffer += ("\t<td>" + self.rank + "</td>\n")
        buffer += ("\t<td>" + self.name + "</td>\n")
        buffer += ("\t<td>" + self.state + "</td>\n")
        buffer += ("\t<td>" + self.id + "</td>\n")
        buffer += ("\t<td>" + self.ratePre + "</td>\n")
        buffer += ("\t<td>" + self.ratePost + "</td>\n")
        for r in self.rounds:
            buffer += ("\t<td>" + r + "</td>\n")
        buffer += ("\t<td>" + self.total + "</td>\n")
        buffer += "</tr>\n"
        return buffer
