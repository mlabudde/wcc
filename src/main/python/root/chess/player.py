from utils import anchor
from utils import String


class Player:
    normDisp = dict({
        'N:4': '1200',
        'N:3': '1400',
        'N:2': '1600',
        'N:1': '1800',
        'N:CM': '2000',
        'N:LM': '2200',
        'N:SM': '2400',
        'N:C': '2000',
        'N:M': '2200',
        'N:S': '2400',
        '': ''
    })

    def __init__(self):
        self.id = ""
        self.rank = ""
        self.name = ""
        self.state = ""
        self.ratePre = ""
        self.ratePost = ""
        self.rounds = list()
        self.rdScore = list()
        self.rdTotal = list()
        self.norm = ""
        self.total = ""

    #           1         2         3         4         5         6         7         8
    # 012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
    #    1.    Waller, Matt (1) .............  WI     2058 W10   W6    W2    -N-     3.0
    #
    @classmethod
    def createPlayerFromWinTDXtbl(cls, line, aNumRounds):
        aPlayer = Player()
        if line:
            _ = line[0:9].strip()  # row nbr
            aPlayer.name = line[9:38].strip()  # name
            aPlayer.ratePre = line[48:52].strip()  # rating

            last_good = -1
            last_good_tag = ""
            for i in range(aNumRounds + 1):
                start = 53 + (6 * i)
                end = start + 6
                this_tag = line[start:end].strip()
                if len(this_tag) > 0:
                    last_good = i
                    last_good_tag = this_tag
                aPlayer.rounds.append(this_tag)  # round detail
            if last_good != aNumRounds:                     # this means did not get a "total" where we expected (3 rds instead of 4, etc)
                aPlayer.rounds[last_good] = ""              # so clear the total in the wrong spot
                #ements[aNumRounds + 3] = last_good_tag    # and put it in the right spot

            aPlayer.calculateRoundScores()

        return aPlayer

    @classmethod
    def createPlayerFromTSV(self, lineParts):
        aPlayer = Player()
        aPlayer.name = lineParts[1]
        aPlayer.id = lineParts[2]
        aPlayer.ratePre = lineParts[3]
        aPlayer.total = 0
        for rd in lineParts[4:]:
            aPlayer.rounds.append(rd)
        aPlayer.calculateRoundScores()
        return aPlayer


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
        if "->" not in rating:
            rating = "->"
            pre = "0"
            post = "0"
        else:
            pos = rating.index("->")
            pre = rating[0:pos]
            post = rating[pos + 2:]
        thePlayer.ratePre = pre.strip()
        thePlayer.ratePost = post.strip()
        # TODO: the colors for each round!
        items = line.split("|")
        thePlayer.norm = cls.normDisp[items[2].strip()];
        for i in range(len(thePlayer.rounds)):
            if (items[3 + i].strip() != ''):
                thePlayer.rounds[i] = thePlayer.rounds[i] + "/" + items[3 + i].strip()
        return thePlayer

    def calculateRoundScores(self):
        self.rdScore = []
        self.rdTotal = []
        curTotal = 0
        for rd in self.rounds:
            if rd[0] == "W" or rd == "BYE":
                self.rdScore.append(1.0)
                curTotal += 1.0
            elif rd[0] == "D" or rd == "H":
                self.rdScore.append(0.5)
                curTotal += 0.5
            else:
                self.rdScore.append(0.0)
            self.rdTotal.append(curTotal)

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
        buffer += ("\t<td>" + self.norm + "</td>\n")
        for r in self.rounds:
            buffer += ("\t<td>" + r + "</td>\n")
        buffer += ("\t<td>" + self.total + "</td>\n")
        buffer += "</tr>\n"
        return buffer

    def printXtblHtml(self, rowNbr, nbrRounds, scrRound):
        buffer = ""
        buffer += ("<tr>\n")
        buffer += ("\t<td>" + str(rowNbr) + "</td>\n")
        buffer += ("\t<td>" + self.name + "</td>\n")
        buffer += ("\t<td>" + self.ratePre  + "</td>\n")
        for r in range(nbrRounds):
            result = "" if r>=len(self.rounds) else self.rounds[r]
            buffer += ("\t<td>" + result + "</td>\n")
        buffer += ("\t<td>" + str(self.rdTotal[scrRound-1]) + "</td>\n")
        buffer += "</tr>\n"
        return buffer

    @classmethod
    def printGamesHtml(self, elements):
        buffer = ""
        buffer += ("<tr>\n")
        buffer += ("\t<td>" + elements[0] + "</td>\n")
        buffer += ("\t<td>" + elements[1] + "</td>\n")
        buffer += ("\t<td>" + elements[2] + "</td>\n")
        buffer += "</tr>\n"
        return buffer
