import sys
from player import Player
from ..utils.String import printPageClose
from ..utils.String import printTableHeader

inputFilename = '../resources/EarlySummer-Reserve.txt'
numRounds = (4 + 1)  # the total points is in the last 'round'

if len(sys.argv) > 1:
    inputFilename = sys.argv[1]
if len(sys.argv) > 2:
    numRounds = 1 + int(sys.argv[2])


# main script starts here
with open(inputFilename) as fin:
    players = []
    numRounds = 0
    index = 0
    line1 = ""
    line2 = ""

    for line in fin:
        if index == 0:
            # nothing to do here
            # clean up
            line1 = ""
            line2 = ""
        elif index == 1:
            line1 = line
        elif index == 2:
            line2 = line
            player = Player.createPlayer(line1.strip(), line2.strip())
            players.append(player)
            if numRounds == 0:
                numRounds = len(player.rounds)

            # clean up
            index = -1
        index = index + 1

    # now let's print out the crosstable
    printTableHeader(numRounds)
    for player in players:
        player.printHtml()
    printPageClose()
