from tokens import Token
from SA import SyntaxAnalyzer
import re

''' Creating a Dictionary of keywords and Operators
    Creating List of Punctuators, considering every entry belongs to itself '''

keyWord = {
    "import":"import", "from":"from", "in":"in", "func":"func", "if":"if", "else":"else", "obj":"obj",
    "while":"while", "for":"for", "continue":"continue", "break":"break", "return":"return", "array":"array",
    "bool":"DT", "int":"DT",  "float":"DT", "char":"DT", "str":"DT", "class":"class", "final":"final",
    "inherits":"inherits", "static":"static", "this":"this", "super":"super", "abstract":"abstract", 
    "construct":"construct"
}

operaTors = {
    ":=": ":=", "!=":"Relational Operator", "==":"Relational Operator", "<":"Relational Operator", "->":".",
    ">":"Relational Operator", ">=":"Relational Operator", "<=":"Relational Operator", "*":"*", "||":"||",
    "&":"&", "+":"Plus/Minus", "-":"Plus/Minus", "*":"Multiply/Divide/Modulus","/":"Multiply/Divide/Modulus",
    "%":"Multiply/Divide/Modulus","++":"Increment/Decrement", "--":"Increment/Decrement",
    "+:=":"Compound Assignment", "-:=":"Compound Assignment", "*:=":"Compound Assignment", "/:=":"Compound Assignment"
    
}
#, "#":"Hash" = Comment
puncTuators = {
    ".":"." , ";":";" , "{":"{" , "}":"}" ,",":",", "[":"[" , "]":"]" , "(":"(" , ")":")" 
}

def isKeyword(input):
    for i in keyWord.keys():
        if (i == input):
            return keyWord[i]

    return None

def isOperator(input):
    for i in operaTors.keys():
        if (i == input):
            return operaTors[i]

    return None

def isPunctuator(input):
    for i in puncTuators.keys():
        if (i == input):
            return puncTuators[i]

    return None

def isCharConst(input):
    is_matched = bool(re.fullmatch("^'[A-Za-z]'$", input))
    return is_matched

def isNumber(input):
    is_matched = bool(re.match('[+-]?\d+[.\d]*', input))
    return is_matched 

def  isDigit( input) :
    is_matched = bool(re.match('^[+-]?[0-9]+$' , input))
    return is_matched

def isAlpha(input):
    is_matched = bool(re.match('^[A-Za-z]+$', input))
    return is_matched

def isIntConst(input):
    is_matched = bool(re.match('^[+-]?[0-9]+$' , input))
    return is_matched

def isFloatConst(input):
    is_matched = bool(re.match('^[+-]?[0-9]*[.][0-9]+$' , input))
    return is_matched

def isStringConst(input):
    if (isCharConst(input) == False):
        is_matched = bool(re.fullmatch('"{1}.*"{1}', input))
        return is_matched

def isBoolConst(input):
    if (input == "True" or input == "False"):
        return True

def isIdentifier(input):
    is_matched = bool(re.fullmatch('^[a-zA-Z][a-zA-Z0-9]*(_[A-Za-z0-9]+)*|[_][A-Za-z0-9]+(_[A-Za-z0-9]+)*$', input))
    return is_matched

def  wordBreaker( strr,  index_no) :

    arr = [None] * (2)
    i = index_no
    ch = ''
    temp = ""
    while (i < len(strr)) :
        ch = strr[i]

        if(ch == ' ' or ch == '\t' or ch == '\n') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                break
            else :
                i += 1
                continue
        
        elif(ch == '!') :
            if (i + 1 < len(strr) and strr[i + 1] == '=') :
                if (temp != "") :
                    arr[0] = temp
                    arr[1] = str(i)
                    temp = ""
                    break
                else :
                    temp = "!="
                    arr[0] = temp
                    arr[1] =str(i + 2)
                    temp = ""
                    break
            else :
                temp = temp + str(ch)   
        elif(ch == ':') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == '=') :
                temp = ":="
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
        elif(ch == '>') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == '=') :
                temp = ">="
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
        elif(ch == '<') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == '=') :
                temp = "<="
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
        elif(ch == '=') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == '=') :
                temp = "=="
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
        elif(ch == '|') :
            if (i + 1 < len(strr) and strr[i + 1] == '|') :
                if (temp != "") :
                    arr[0] = temp
                    arr[1] = str(i)
                    temp = ""
                    break
                else :
                    temp = "||"
                    arr[0] = temp
                    arr[1] = str(i + 2)
                    temp = ""
                    break
            else :
                temp = temp + str(ch)
        elif(ch == '+'):
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == ':') :
                if(i + 2 < len(strr) and strr[i + 2] == "="):
                    temp = "+:="
                    arr[0] = temp
                    arr[1] = str(i + 3)
                    temp = ""
                    break
            elif(i + 1 < len(strr) and strr[i + 1] == '+'):
                temp = "++"
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
            
        elif(ch == '-'):
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == ':') :
                if(i + 2 < len(strr) and strr[i + 2] == "="):
                    temp = "-:="
                    arr[0] = temp
                    arr[1] = str(i + 3)
                    temp = ""
                    break
            elif (i + 1 < len(strr) and strr[i + 1] == '>'):
                    temp = "->"
                    arr[0] = temp
                    arr[1] =str(i + 2)
                    temp = ""
                    break
            elif(i + 1 < len(strr) and strr[i + 1] == '-'):
                temp = "--"
                arr[0] = temp
                arr[1] = str(i + 2)
                temp = ""
                break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
            
        elif(ch == '/'):
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == ':') :
                if(i + 2 < len(strr) and strr[i + 2] == "="):
                    temp = "/:="
                    arr[0] = temp
                    arr[1] = str(i + 3)
                    temp = ""
                    break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
            
        elif(ch == '*'):
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            if (i + 1 < len(strr) and strr[i + 1] == ':') :
                if(i + 2 < len(strr) and strr[i + 2] == "="):
                    temp = "*:="
                    arr[0] = temp
                    arr[1] = str(i + 3)
                    temp = ""
                    break
            else :
                temp = temp + str(ch)
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break

        elif(ch == '%' or ch == '(' or ch == ')' or ch == '{' or ch == '}' or ch == '[' or 
            ch == ']' or ch == ';' or ch == ','):
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            else :
                temp = temp + ch
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break

        elif(ch == '\''):   
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            temp = temp + str(ch)
            i += 1
            if (i < len(strr)) :
                ch = strr[i]
                temp = temp + str(ch)
                if (ch == '\\') :
                    j = 0
                    while (j < 2) :
                        i += 1
                        if (i < len(strr)) :
                            ch = strr[i]
                            temp = temp + str(ch)
                        j += 1
                    arr[0] = temp
                    arr[1] = str(i + 1)
                    temp = ""
                    break
                else :
                    i += 1
                    if (i < len(strr)) :
                        ch = strr[i]
                        temp = temp + str(ch)
                        arr[0] = temp
                        arr[1] = str(i + 1)
                        temp = ""
                        break
        elif(ch == '"') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            while True :
                ch = strr[i]
                if (ch == '\\' and i + 1 < len(strr)) :
                    temp = temp + str(ch) + strr[i + 1]
                    i += 1
                else :
                    temp = temp + str(ch)
                i += 1
                if((i < len(strr) and strr[i] != '"') == False) :
                    break

            if (i < len(strr) and strr[i] == '"') :
                temp = temp + "\""
                arr[0] = temp
                arr[1] = str(i + 1)
                temp = ""
                break
        elif(ch == '`') :
            if (temp != "") :
                arr[0] = temp
                arr[1] = str(i)
                temp = ""
                break
            i = len(strr)
        elif(ch == '.') :
            if (temp != "") :
                if (isDigit(temp)) :
                    i += 1
                    if (i < len(strr)) :
                        ch = strr[i]
                        if (isDigit(ch)) :
                            temp = temp + "." + ch
                        else :
                            arr[0] = temp
                            arr[1] = str(i)
                            temp = ""
                            break
                    else :
                        i -= 1
                        arr[0] = temp
                        arr[1] = str(i)
                        temp = ""
                        break
                else :
                    arr[0] = temp
                    arr[1] = str(i)
                    temp = ""
                    break
            else :
                temp = temp + "."
                i += 1
                if (i < len(strr)) :
                    ch = strr[i]
                    if (isDigit(ch)) :
                        temp = temp + str(ch)
                    else :
                        arr[0] = temp
                        arr[1] = str(i)
                        temp = ""
                        break
                else :
                    arr[0] = temp
                    arr[1] = str(i)
                    temp = ""
                    break
        else :
            temp = temp + str(ch)
        i += 1
    if (temp != "") :
        arr[0] = temp
        arr[1] = str(i)
        temp = ""
    elif(arr[0] == None and arr[1] == None) :
        arr[0] = "-1"
        arr[1] = str(i + 1)
    return arr


if __name__ == '__main__':
    
    tokenList = []
    count = 1
    try:
        file = open('f.txt', 'r')
    except:
        print ("Input file does not exists")

    inps = file.readlines()
    #print(inps)
    #print(len(inps)) #10
    for inp in inps:
        if (inp):
            if not inp.startswith('#'):
                #print(inp)   #func sum(a , b){
                index = 0
                while(index < len(inp)):
                    arr = wordBreaker(inp,index)
                    #print("( " + arr[0] + ", " , arr[1] ," )")
                    index = int(arr[1])
                    temp = arr[0]
                    if temp != "-1":
                        if temp[0] == '_':
                            flag = isIdentifier(temp)
                            if (flag):
                                tok = Token('ID', temp, count)
                                tokenList.append(tok)
                            else:
                                tok = Token('Invalid Lexeme', temp, count)
                                tokenList.append(tok)

                        elif (isNumber(temp)):
                            flag = isIntConst(temp)
                            if (flag):
                                tok = Token('IntegerConstant', temp, count)
                                tokenList.append(tok)
                            else:
                                flag = isFloatConst(temp)
                                if(flag):
                                    tok = Token('FloatConstant', temp, count)
                                    tokenList.append(tok)
                                else:
                                    tok = Token('Invalid Lexeme', temp, count)
                                    tokenList.append(tok)

                        elif temp[0] == '.':
                            if len(temp) > 1:
                                flag = isFloatConst(temp)
                                if (flag):
                                    tok = Token('FloatConstant', temp, count)
                                    tokenList.append(tok)
                                else:
                                    tok = Token('Invalid Lexeme', temp, count)
                                    tokenList.append(tok)
                            else:
                                tok.setClassPart = 'Dot'
                                tok.setValuePart = temp
                                tok.setLineNo = count
                                tokenList.append(tok)

                        elif (isBoolConst(temp)and (isKeyword(temp) == None)):
                            tok = Token('boolConstant', temp, count)
                            tokenList.append(tok)

                        elif (temp[0] == "'"):
                            flag = isCharConst(temp)
                            if (flag):
                                tok = Token('charConstant', temp, count)
                                tokenList.append(tok)
                            else:
                                tok = Token('Invalid Lexeme', temp, count)
                                tokenList.append(tok)

                        elif(isStringConst(temp) and (isKeyword(temp) == None)):
                                tok = Token('StringConst', temp, count)
                                tokenList.append(tok)

                        elif (isAlpha(temp)):
                            flag = isIdentifier(temp)
                            if (flag):
                                classPart = isKeyword(temp)
                                if (classPart != None):
                                    #print(classPart)
                                    tok = Token(classPart, temp, count)
                                    tokenList.append(tok)

                                else:
                                    tok = Token('ID', temp, count)
                                    tokenList.append(tok)
                            else:
                                tok = Token('Invalid Lexeme', temp, count)
                                tokenList.append(tok)

                        else:
                            punc = isPunctuator(temp)
                            op = isOperator(temp)
                            #print("op:",op)
                            if (punc != None):
                                tok = Token(punc, temp, count)
                                tokenList.append(tok)
                            elif (op != None):
                                tok = Token(op, temp, count)
                                tokenList.append(tok)
                            else:
                                tok = Token('Invalid Lexeme', temp, count)
                                tokenList.append(tok)
                count+=1

    tok = Token('$', '$' , count)
    tokenList.append(tok)

    #for loop ends
    #print(tokenList)
    # for i in tokenList:
    #    print(i.printToken())
   
        
    #load tokenList in a file 
    file = open('output.txt', 'w')
    for t in tokenList:
        file.write(t.printToken())
        file.write("\n")

    file.close()

    #print("---Lexical Analyzer---")
    #Syntax

    SyA = SyntaxAnalyzer(tokenList)
    
    SyA.validate()
    #SyA.ch()
 #final int z := 5;