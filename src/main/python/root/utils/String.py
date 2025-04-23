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
    print("\t<th>Norm</th>")

    for i in range(numRounds):
        print("\t<th>R" + str(i + 1) + "</th>")
    print("\t<th>Total</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")


# for WinTD Text Formatting
def printCrossTableHeader(numRounds):
    print("<table class='wccCrosstable'>")
    print("<thead>")
    print("<tr>")
    print("\t<th>No.</th>")
    print("\t<th>Player Name</th>")
    print("\t<th>Rating</th>")

    for i in range(numRounds):
        print("\t<th>R" + str(i + 1) + "</th>")
    print("\t<th>Total</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")


# for WinTD Text Formatting
def printGamesTableHeader():
    print("<table class='wccCrosstable'>")
    print("<thead>")
    print("<tr>")
    print("\t<th>No.</th>")
    print("\t<th>White</th>")
    print("\t<th>Black</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")


def printPageHeader(title, subtitle):
    print("<! DOCTYPE html> \n\
    <html><head> \n\
    <meta http-equiv=Content-Type content=\"text/html\" charset=\"utf-8\"> \n\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"css/wcc.css\"/>  \n\
    <script type=\"text/javascript\" language=\"javascript\" src=\"js/jquery-3.4.1.min.js\"> \n\
        <!-- yes, this comment is here on purpose -->  \n\
    </script>  \n\
    <title>Waukesha Chess Club</title>  \n\
    </head>  \n\
        \n\
    <body>  \n\
    <div id=\"main-container\"> \n\
    <script> \n\
        const isDarkMode = window.matchMedia(\"(prefers-color-scheme: dark)\").matches; \n\
        $(function() { \n\
            if (isDarkMode) \n\
            { \n\
                $(\"#title\").load(\"headerw.html\"); \n\
            } else { \n\
              $(\"#title\").load(\"headerb.html\"); \n\
            } \n\
            $(\"#menu\").load(\"menu.html\"); \n\
            $(\"#footer\").load(\"footer.html\"); \n\
        }); \n\
    </script> \n\
    <div id=\"title\"> </div> \n\
    <div id=\"menu\"></div> \n\
    <div id=\"divContent\"> \n\
    <div id=\"pageTitle\"> \n\
    <span>" + title + "</br></span> \n\
    <span id=\"divSubtitle\">" + subtitle + "</span></div>\n")

def printEventTableHeader(headerList):
    print("<table class='wccPast' width=\"90%\">\n<tr>")
    for hdr in headerList:
        print("<th style=\"width: " + str(int(80 / len(headerList))) + "%\" class =\"thPast\">" + hdr + "</th>\n")
    print("</tr>")


def printPriorEventRow(new_year, name, link, className):
    aggregate_from_year = 1991
    if new_year > 0 and new_year >= aggregate_from_year:
        print("<tr>	<td></td> <td></td> </tr>")
        print("<tr><td colspan=\"2\"><hr width=\"100%\" /></td></tr>\n")
        print("<tr>\n")
        if new_year > aggregate_from_year:
            print("<td class=\"year\">" + str(new_year) + "</td>")
        else:
            print("<td class=\"year\">" + str(new_year) + " (and earlier)</td>")
    else:
        print("<tr>\n")
        print("<td></td>")
    print("<td class='" + className + "'><a class='" + className + "' target=\"_blank\" href=\"" + link + "\" >" + name + "</a></br></td>\n")
    print("</tr>\n")


def printWinnersRow(new_year, name1, link1, name2, link2, className):
    if new_year > 0:
        print("<tr>	<td></td> <td></td> </tr>")
        print("<tr><td colspan=\"3\"><hr width=\"100%\" /></td></tr>\n")
        print("<tr>\n")
        print("<td class=\"year\">" + str(new_year) + "</td>")
    else:
        print("<tr>\n")
        print("<td></td>")
    if link1 == "":
        print("<td class='" + className + "'>" + name1 + "</br></td>\n")
    else:
        print(
            "<td class='" + className + "'><a class='" + className + "' target=\"_blank\" href=\"" + link1 + "\">" + name1 + "</a></br></td>\n")
    if link2 == "":
        print("<td class='" + className + "'>" + name2 + "</br></td>\n")
    else:
        print("<td class='" + className + "'><a class='" + className + "' target=\"_blank\" href=\"" + link2 + "\">" + name2 + "</a></br></td>\n")
    print("</tr>\n")


# for WinTD Text Formatting
def printBlankLine():
    print("<tr><td></td></tr>")


def printPageClose():
    print("</div>")
    print("<div id=\"footer\"></div>")
    print("</body>")
    print("</html>")


def printDivClose():
    print("</div>")


def printTableClose():
    print("</table>")
    print("<br/>")
