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


def processWebContent(html:str):
    sections = reader.getSectionsFromHtml(html)
    String.printPageHeader()
    for section in sections:
        print(section.getNameHtml())
        String.printTableHeader(section.getRoundCount())
        print(section.toHtml())
        String.printTableClose()
    String.printPageClose()
    return


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
else:
    print("arg1 must be one of: 'file', 'web', or 'webfile'")
    sys.exit(1)
