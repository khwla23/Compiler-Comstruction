# Compiler-Construction
## Lexical Analyzer
This Repository includes the Lexical Analyzer.
LA.py file reads the input file "f.txt" breaks it using wordbreaker function and creates the token using "Token.py" file then write these token into output.txt file.
I have also used Regex to find the match of words.

Its important for a wordbreaker to ignore the comments and not convert them into tokens. Here, i have used "#" symbol for comments.

***Token ==> (classPart, valuePart, LineNo)***
These are the keywords, operators and punctuators that i have used in my language.
'''
**keyWord = {
    "import":"import", "from":"from", "in":"in", "func":"func", "if":"if", "else":"else", "obj":"obj",
    "while":"while", "for":"for", "continue":"continue", "break":"break", "return":"return", "array":"array",
    "bool":"DT", "int":"DT",  "float":"DT", "char":"DT", "str":"DT", "class":"class", "final":"final",
    "inherits":"inherits", "static":"static", "this":"this", "super":"super", "abstract":"abstract", 
    "construct":"construct"
}**

**operaTors = {
    ":=": ":=", "!=":"Relational Operator", "==":"Relational Operator", "<":"Relational Operator", "->":".",
    ">":"Relational Operator", ">=":"Relational Operator", "<=":"Relational Operator", "*":"*", "||":"||",
    "&":"&", "+":"Plus/Minus", "-":"Plus/Minus", "*":"Multiply/Divide/Modulus","/":"Multiply/Divide/Modulus",
    "%":"Multiply/Divide/Modulus","++":"Increment/Decrement", "--":"Increment/Decrement",
    "+:=":"Compound Assignment", "-:=":"Compound Assignment", "*:=":"Compound Assignment", "/:=":"Compound Assignment"
 }**

**puncTuators = {
    ".":"." , ";":";" , "{":"{" , "}":"}" ,",":",", "[":"[" , "]":"]" , "(":"(" , ")":")" 
}**
'''
To run the code, download this repository and open it in VScode then simply press F5.

_Right now i am working on Syntax Analyzer so when its done i will inclue the file in this Repository._
