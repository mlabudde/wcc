# String utility functions

def massageName(name):
    result = ""
    cnc = True
    rawName = list(name.lower())
    for c in rawName:
        if cnc:
            # result = result + c.upper()
            result += c.upper()
            cnc = False
        else:
            result += c
        if c == ' ' or c == '\'':
            cnc = True
    if result.startswith('Mcc'):
        result = result.replace('Mcc', 'McC')
    return result


def printPageHeader():
    print("<html><head>")
    print("<link rel='stylesheet' type='text/css' href='http://www.waukeshachessclub.com/css/wcc.css' />")
    print("</head>")
    print("<body style='background-color: white; color: black; font-size: 12pt; text-align: left;'>")


def printTableHeader(numRounds):
    print("<table class='wccCrosstable'>")
    print("<thead>")
    print("<tr>")
    print("\t<th>No.</th>")
    print("\t<th>Player Name</th>")
    print("\t<th>State</th>")
    print("\t<th>USCF ID</th>")
    print("\t<th>Pre</th>")
    print("\t<th>Post</th>")

    for i in range(numRounds):
        print("\t<th>R" + str(i + 1) + "</th>")
    print("\t<th>Total</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")


def printPageClose():
    print("</body>")
    print("</html>")


def printTableClose():
    print("</tbody>")
    print("</table>")
    print("<br/>")
