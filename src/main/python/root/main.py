import json
import sys
from root.chess.player import Player as player
from root.chess.reader import Reader as reader
from root.utils import String


def getInputFilename():
    if len(sys.argv) >= 3:
        return sys.argv[2]
    return "../../resources/LateSpring-Open.txt"


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


def processWinTDFile():
    inputFilename = getInputFilename()
    numRounds = 4

    if len(sys.argv) >= 4:
        numRounds = int(sys.argv[3])

    String.printCrossTableHeader(numRounds)
    with open(inputFilename) as fin:
        players = 0
        for line in fin:
            if len(line) > 5 and line[4] == '.' and line[2] != 'N':
                elements = splitWinTDXtblLine(line, numRounds)
                print(player().printXtblHtml(elements, numRounds))
                players = players + 1
            else:
                if players > 0:
                    String.printBlankLine()
                    String.printBlankLine()

    print("</tbody>")
    print("</table>")
    String.printPageClose()
    return


def processGamesFile():
    inputFilename = getInputFilename()
    numRounds = 4

    if len(sys.argv) >= 4:
        numRounds = int(sys.argv[3])

    String.printGamesTableHeader()
    with open(inputFilename) as fin:
        players = 0
        for line in fin:
            if len(line) > 7 and line[6] == '.':
                elements = splitGamesLine(line)
                print(player().printGamesHtml(elements))
                players = players + 1

    print("</tbody>")
    print("</table>")
    String.printPageClose()
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
    # as we determine how we want some events to appear, we can add the updates here...
    f = open('data/event_names.json')
    event_name_overrides = json.load(f)
    color_cycle = ["#CCFFCC", "#CCFFFF", "#FFCCCC", "#FFCCFF", "#CCCCFF", "#FFFFCC"]
    current_color = -1
    events = reader.getEventHistory()
    current_year = 0
    String.printPriorEventPageHeader()
    String.printPriorEventTableHeader()
    for event in events:
        out_name = event["name"]
        if event["event_id"] in event_name_overrides.keys():
            out_name = event_name_overrides[event["event_id"]]

        new_year = 0
        if event["date"].year != current_year:
            current_year = event["date"].year
            new_year = current_year
            current_color = (current_color+1) % len(color_cycle)
        # print(event["date"].strftime("%m/%d/%Y") + " - " + event["link"] + " - " + out_name)
        String.printPriorEventRow(new_year, out_name, event["link"], color_cycle[current_color])

    String.printTableClose()
    String.printDivClose()
    String.printPageClose()


def createPlayer(attributes, rounds):
    aPlayer = player.Player()
    aPlayer.parse(attributes, rounds)
    return aPlayer


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
#    1.    Waller, Matt (1) .............  WI     2058 W10   W6    W2    -N-     3.0
#
def splitWinTDXtblLine(line, aNumRounds):
    elements = list()
    if (line):
        elements.append(line[0:9].strip())
        elements.append(line[9:38].strip())
        elements.append(line[48:52].strip())

        for i in range(aNumRounds + 1):
            start = 53 + (6 * i)
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
        elements.append(line[53:80].strip())

    return elements


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
elif "clubEvents" == arg1:
    processMSAEvents()
else:
    print(
        "arg1 must be one of: 'file', 'web', 'webfile', 'winTD', or 'pairings' (last 2 take winTD text output from a file)")
    sys.exit(1)
