import sys
import reader
from utils import String

inputFilename = "../../resources/EarlySummer-uscf.html"
sectionName = "Section 1"

if len(sys.argv) > 1:
    inputFilename = sys.argv[1]
if len(sys.argv) > 2:
    sectionName = sys.argv[2]

with open(inputFilename) as fin:
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
