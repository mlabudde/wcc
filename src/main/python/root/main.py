import json
import sys

from root.chess.player import Player as player
from root.chess.reader import Reader as reader
from root.utils import String

class_cycle = ["wccColor1", "wccColor2", "wccColor3", "wccColor4", "wccColor5", "wccColor6"]
# color_cycle = ["#CCFFCC", "#CCFFFF", "#FFCCCC", "#FFCCFF", "#CCCCFF", "#FFFFCC"]

def getInputFilename():
    if len(sys.argv) >= 3:
        return sys.argv[2]
    return "../../resources/LateSpring-Open.txt"

def splitFullPostUpdateFile():
    outLineSet = []
    thisLineSet = []

    inputFilename = getInputFilename()
    with open(inputFilename) as fin:
        for line in fin:
            if len(line) > 1 and line[0] != " " and thisLineSet != []: # start of a new set
                outLineSet.append(thisLineSet)
                thisLineSet = [line]
            else:
                thisLineSet.append(line)
    if thisLineSet != []: # start of a new set
        outLineSet.append(thisLineSet)
    return outLineSet

def fullUpdatePost():
    # print("Split file")
    [openXtbl, openPair, reserveXtbl, reservePair] = splitFullPostUpdateFile()
    print("</br><b>Open Section Crosstable</b></br>")
    processWinTDFile(openXtbl)
    print("</br><b>Open Section Pairings</b></br>")
    processGamesFile(openPair)
    print("</br><b>Reserve Section Crosstable</b></br>")
    processWinTDFile(reserveXtbl)
    print("</br><b>Reserve Section Pairings</b></br>")
    processGamesFile(reservePair)

def processFile():
    inputFilename = getInputFilename()
    numRounds = 4

    if len(sys.argv) >= 4:
        numRounds = int(sys.argv[3])

    String.printTableHeader(numRounds)
    with open(inputFilename) as fin:
        for line in fin:
            elements = splitFixedLine(line.strip(), numRounds)
            player = createPlayer(elements, numRounds)
            player.printHtml()

    print("</tbody>")
    print("</table>")
    String.printPageClose()
    return


def processWinTDFile(inLines = None):
    if inLines is None:
        inputFilename = getInputFilename()
        with open(inputFilename) as fin:
            inLines = fin.readlines()

    numRounds = 4

    if len(sys.argv) >= 4:
        numRounds = int(sys.argv[3])

    String.printCrossTableHeader(numRounds)

    players = 0
    for line in inLines:
        if len(line) > 5 and line[4] == '.' and line[2] != 'N':
            players = players + 1
            thisPlayer = player.createPlayerFromWinTDXtbl(line, numRounds)
            print(thisPlayer.printXtblHtml(players, numRounds, numRounds))
        else:
            if players > 0 and False:
                String.printBlankLine()
                String.printBlankLine()

    print("</tbody>")
    print("</table>")
    return


def processGamesFile(inLines = None):
    if inLines is None:
        inputFilename = getInputFilename()
        with open(inputFilename) as fin:
            inLines = fin.readlines()

    if len(sys.argv) >= 4:
        numRounds = int(sys.argv[3])

    String.printGamesTableHeader()

    players = 0
    for line in inLines:
        if len(line) > 7 and line[6] == '.':
            elements = splitGamesLine(line)
            print(player.printGamesHtml(elements))
            players = players + 1

    print("</tbody>")
    print("</table>")
    return


def processWeb():
    tournamentId = ""
    if len(sys.argv) >= 3:
        tournamentId = sys.argv[2]
    html = reader.getHtml(tournamentId, "0")
    return processWebContent(html)


def processWebFile():
    inputFilename = getInputFilename()
    html = ""
    with open(inputFilename) as fin:
        for line in fin:
            html += line
    return processWebContent(html)


def processWebContent(html: str):
    sections = reader.getSectionsFromHtml(html)
    String.printPageHeader()
    for section in sections:
        print(section.getNameHtml())
        String.printTableHeader(section.getRoundCount())
        print(section.toHtml())
        String.printTableClose()
    String.printPageClose()
    return


def processMSAEvents():
    # should actually divert this output to past_tournaments.html

    # as we determine how we want some events to appear, we can add the updates here...
    f = open('data/event_names.json')
    event_name_overrides = json.load(f)

    fOut = open('../../web/past_tournaments.html', 'w')
    refOut = sys.stdout
    sys.stdout = fOut

    classIndex = -1
    events = reader.getEventHistory()
    current_year = 0
    String.printPageHeader("Past Tournaments", "- results linked to events -")
    String.printEventTableHeader(["Year", "Tournament"])
    for event in events:
        out_name = event["name"]
        if event["event_id"] in event_name_overrides.keys():
            out_name = event_name_overrides[event["event_id"]]

        new_year = 0
        if event["date"].year != current_year:
            current_year = event["date"].year
            new_year = current_year

        classIndex = (classIndex+1) % len(class_cycle)
        # print(event["date"].strftime("%m/%d/%Y") + " - " + event["link"] + " - " + out_name)
        String.printPriorEventRow(new_year, out_name, event["link"], class_cycle[classIndex])

    String.printTableClose()
    String.printDivClose()
    String.printPageClose()
    sys.stdout = refOut


def generateWinnersPage():
    # should actually divert this output to champions.html

    # as we determine how we want some events to appear, we can add the updates here...
    f = open('data/event_names.json')
    event_name_overrides = json.load(f)

    fOut = open('../../web/champions.html', 'w')
    refOut = sys.stdout
    sys.stdout = fOut

    classIndex = -1
    winnersByYear = reader.getWinners() # this should be updated - not all affiliate, but by ids in winners.json
    current_year = 0
    String.printPageHeader("Past Champions", "- honoring our club history -")
    String.printEventTableHeader(["Year", "Club Champion", "Waukesha Memorial Champion"])

    for winner in winnersByYear:
        ccWinner = winner["ccWinner"]
        memWinner = winner["memWinner"]
        year = winner["year"]
        classIndex = (classIndex+1) % len(class_cycle)
        String.printWinnersRow(year, ccWinner, winner["ccLink"], memWinner, winner["memLink"], class_cycle[classIndex])

    String.printTableClose()
    String.printDivClose()
    String.printPageClose()
    sys.stdout = refOut


def createPlayer(attributes, rounds):
    return player().parse(attributes, rounds)


#          1         2         3         4         5         6         7
# 012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
# 30289677    1 KLINKNER, PATRICK WI  927/24  921*   W---7 L---5 W---3 W---2 W---2 3.0
#
def splitFixedLine(line, aNumRounds):
    elements = list()
    if (line):
        elements.append(line[0:9].strip())
        elements.append(line[9:13].strip())
        elements.append(line[14:31].strip())
        elements.append(line[32:34].strip())
        elements.append(line[35:43].strip())
        elements.append(line[43:51].strip())

        for i in range(aNumRounds):
            start = 51 + (6 * i)
            end = start + 6
            elements.append(line[start:end].strip())

    return elements




#           1         2         3         4         5         6         7         8
# 012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#    101.  ___  Templin, Aethe (2.0,Templi,1960)  ___  Coons, James Jay (2.0,1724)
#
def splitGamesLine(line):
    elements = list()
    if (line):
        elements.append(line[3:7].strip())
        elements.append(line[14:47].strip())
        elements.append(line[53:90].strip())

    return elements

def processTSV():
    processTSVXtbl('data/xtbl-open.tsv')
    processTSVXtbl('data/xtbl-reserve.tsv')
    processTSVPairing('data/pair-open.tsv')
    processTSVPairing('data/pair-reserve.tsv')

def processTSVXtbl(fn):
    f = open(fn)
    xtbl = f.readlines()
    players = []
    for line in xtbl[1:]:
        players.append(player.createPlayerFromTSV(line.strip().split('\t')))
    String.printCrossTableHeader(4)
    for i in range(len(players)):
        print(players[i].printXtblHtml(i+1,4,1))
    print("</tbody>")
    print("</table>")

def processTSVPairing(fn):
    f = open(fn)
    xtbl = f.readlines()
    players = []
    String.printGamesTableHeader()
    for i in range(len(xtbl[2:])):
        elts = xtbl[2+i].strip().split('\t')
        print(player.printGamesHtml([elts[0],elts[1],elts[3]]))
    print("</tbody>")
    print("</table>")


def main():
    #
    # Possible values for argv[1] are:
    #   file, web, webfile
    #
    arg1 = None

    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
    if "file" == arg1:
        processFile()
    elif "web" == arg1:
        processWeb()
    elif "webfile" == arg1:
        processWebFile()
    elif "winTD" == arg1:
        processWinTDFile()
    elif "pairings" == arg1:
        processGamesFile()
    elif "updatePost" == arg1:
        fullUpdatePost()
    elif "clubEvents" == arg1:
        processMSAEvents()
    elif "winnersPage" == arg1:
        generateWinnersPage()
    elif "fromTSV" == arg1:
        processTSV()
    else:
        print(
            "arg1 must be one of: 'file', 'web', 'webfile', 'clubEvents', 'winnersPage', 'fromTSV', 'winTD' or 'pairings' (last 3 take text output from a file - needs manual preprocessing)")
        sys.exit(1)


if __name__ == "__main__":
    main()
