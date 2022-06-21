class Player:

    def __init__(self):
        self.id = ""
        self.rank = ""
        self.name = ""
        self.state = ""
        self.ratePre = ""
        self.ratePost = ""
        self.rounds = list()
        self.total = ""
        
    def massageName(self):
        result = ""
        cnc = True
        rawName = list(self.name.lower())
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

    def parse(self, elements, numRounds):
        length = len(elements)
        idx = length - 1
        for i in range(numRounds):
            self.rounds.insert(0, elements[idx - i])
        
        self.ratePost = elements[length - 6]
        self.ratePre = elements[length - 7]
        self.state = elements[length - 8]
        
        self.id = elements[0]
        self.rank = elements[1]
        
        if length == 11:
            self.name = elements[2] + " " + elements[3]
        elif length == 12:
            self.name = elements[2] + " " + elements[3]
            self.state = elements[4]
        elif length == 13: 
            self.name = elements[2] + " " + elements[3] + " " + elements[4]
            self.state = elements[5]
        elif length < 11:
            print("ERROR - less than 11 elements in array!\n\n")
        else:
            print("ERROR - more than 13 elements in array!\n\n")
        self.name = self.massageName()
            

    def fixRound(self, round):
        rnd = round.replace("-", "")
        if len(rnd) == 2 and rnd[-1] == '0':
            rnd = rnd[:-1]
        return rnd
        
    def printHtml(self):
        print("<tr>")

        print("\t<td>" + self.rank + "</td>")
        print("\t<td>" + self.name + "</td>")
        print("\t<td>" + self.state + "</td>")
        print("\t<td>" + self.id + "</td>")
        print("\t<td>" + self.ratePre + "</td>")
        print("\t<td>" + self.ratePost + "</td>")
        for r in self.rounds:
            round = self.fixRound(r)
            print("\t<td>" + round + "</td>")
        print("</tr>")
