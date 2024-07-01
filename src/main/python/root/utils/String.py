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


def printPriorEventPageHeader():
    print("<html><head> \n\
    <meta http-equiv=Content-Type content=\"text/html\" charset=\"utf-8\"> \n\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"css/wcc.css\"/>  \n\
    <script type='text/javascript' language='javascript' src='js/jquery-3.4.1.min.js'> \n\
        <!-- yes, this comment is here on purpose -->  \n\
    </script>  \n\
    <title>Waukesha Chess Club</title>  \n\
</head>  \n\
    \n\
<body>  \n\
<div id=\"main-container\">  \n\
    <div id=\"divHeader\">  \n\
        <span class=\"wccTitle\">WAUKESHA CHESS CLUB</span>  \n\
        <div id=\"divMenu\">  \n\
            <hr class=\"menuLine menuLineTop\"/>  \n\
            <span class=\"wccMenuItemFirst\"><a class=\"wccMenuLink\" href=\"index.html\">Home</a></span>  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"schedule.html\">Schedule</a></span>  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"club_champions.html\">Club Champions</a></span>  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"waukmem.html\">Waukesha Memorial</a></span>  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"boardmembers.html\">WCC Board</a></span>  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"past_tournaments.html\">Past Tournaments</a></span>  \n\
            <!-- <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"games.html\">Games</a></span> -->  \n\
            <span class=\"wccMenuItem\"><a class=\"wccMenuLink\" href=\"links.html\">Links</a></span>  \n\
            <span class=\"wccMenuImage\"><a class=\"wccMenuLink\" href=\"http://waukeshachessclub.blogspot.com/\" target=\"_blank\"><img class=\"wccMenuLinkImage\" src=\"images/blogger-logo.png\" alt=\"Blog\" height=\"17\" width=\"17\"/></a></span>  \n\
            <hr class=\"menuLine menuLineBottom\"/>  \n\
        </div>  \n\
    </div>  \n\
    \n\
    <div id=\"divContent\">  \n\
        <div id=\"pageTitle\"><span>PAST TOURNAMENTS</span><br/></div>\n")


def printPriorEventTableHeader():
    print("<table class='wccPast' width=\"90%\">\n" +
          "<tr><th class =\"thPast\">Year</th><th class=\"thPast\">Tournament</th></tr>\n")


def printPriorEventRow(new_year, name, link, color):
    aggregate_from_year = 1991

    if new_year > 0 and new_year >= aggregate_from_year:
        print("<tr>	<td></td> <td></td> </tr>")
        print("<tr><td colspan=\"2\"><hr width=\"100%\" /></td></tr>\n")
        print("<tr>\n")
        if new_year > aggregate_from_year:
            print("<td class=\"year\">"+str(new_year)+"</td>")
        else:
            print("<td class=\"year\">" + str(new_year) + " (and earlier)</td>")
    else:
        print("<tr>\n")
        print("<td></td>")
    print("<td><a target=\"_blank\" href=\""+link+"\" style=\"color:"+color+"\">"+name+"</a></br></td>\n")
    print("</tr>\n")

# for WinTD Text Formatting
def printBlankLine():
    print("<tr><td></td></tr>")

def printPageClose():
    print("</body>")
    print("</html>")


def printDivClose():
    print("</div>")


def printTableClose():
    print("</tbody>")
    print("</table>")
    print("<br/>")
