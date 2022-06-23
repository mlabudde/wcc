import sys
from player import Player
inputFilename = '../resources/LateSpring-Open.txt'
numRounds = (4 + 1)  # the total points is in the last 'round'

if len(sys.argv) > 1:
    inputFilename = sys.argv[1]
if len(sys.argv) > 2:
    numRounds = 1 + int(sys.argv[2])


def createPlayer(attributes, rounds):
    aPlayer = Player()
    aPlayer.parse(attributes, rounds)
    return aPlayer


def splitLine(line):
    elements = list()
    if (line):
        elements = list(filter(None, line.split(" ")))
    return elements

#          1         2         3         4         5         6         7
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#30289677    1 KLINKNER, PATRICK WI  927/24  921*   W---7 L---5 W---3 W---2 W---2 3.0
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

def printTableHeader():
    print("<html><head>")
    print("<link rel='stylesheet' type='text/css' href='http://www.waukeshachessclub.com/css/wcc.css' />")
    print("</head>")
    print("<body>")
    print("<table class='wccCrosstable'>")
    print("<thead>")
    print("<tr>")
    print("\t<th>No.</th>")
    print("\t<th>Player Name</th>")
    print("\t<th>State</th>")
    print("\t<th>USCF ID</th>")
    print("\t<th>Pre</th>")
    print("\t<th>Post</th>")

    for i in range(numRounds - 1):
        print("\t<th>R " + str(i + 1) + "</th>")
    print("\t<th>Total</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")


def printPageClose():
    print("</body>")
    print("</html>")


# main script starts here
with open(inputFilename) as fin:
    printTableHeader()
    for line in fin:
        elements = splitFixedLine(line.strip(), numRounds)
        player = createPlayer(elements, numRounds)
        player.printHtml()

    print("</tbody>")
    print("</table>")
    printPageClose()
