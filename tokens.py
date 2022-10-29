class Token:
    def __init__ (self, cPart, vPart, lNo):
        self.classPart = cPart
        self.valuePart = vPart
        self.lineNo = lNo

    def getClassPart(self):
        return self.classPart

    def setClassPart(self, cPart):
        self.classPart = cPart

    def getValuePart(self):
        return self.valuePart

    def setValuePart(self, vPart):
        self.valuePart = vPart
    
    def setLineNo (self, lNo):
        self.lineNo = lNo

    def getLineNo (self):
        return self.lineNo 

    def printToken(self):
        return "("+self.classPart+","+self.valuePart+","+str(self.lineNo) +")"

