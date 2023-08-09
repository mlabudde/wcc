import sys
import reader
from ..utils import String


def getInputFilename():
    if len(sys.argv) >= 3:
        return sys.argv[2]
    return "../../resources/LateSpring-Open.txt"


with open(getInputFilename()) as fin:
    lines = []
    for line in fin:
        lines.append(line)

section1 = reader.getSectionFromLines(lines, "Section 1")
section2 = reader.getSectionFromLines(lines, "Section 2")

String.printPageHeader()
String.printTableHeader(section1.getRoundCount())
print(section1.toHtml())
String.printTableClose()

String.printTableHeader(section2.getRoundCount())
print(section2.toHtml())
String.printTableClose()
String.printPageClose()
