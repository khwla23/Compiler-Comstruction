class SyntaxAnalyzer:
    
    def __init__(self, tokenList):
        self.TList = tokenList
        self.i = 0
    
    def ch(self):
        ind = self.TList[self.i].getClassPart()
        return ind

    def validate (self):
        if (self.S0()):
            if (self.TList[self.i].getClassPart() == "$"):
                print ("Valid")
        else:
            print ("Syntax error at" , self.TList[self.i].getLineNo(), self.TList[self.i].printToken())
  
# SS = import, while, for, return, if, break, continue, static, DT, func, ID, class,abstract , final , this, super==> $ 
# <S0> --> <opFrom> <S>
    def S0(self):
        if (self.ch() == "from" or self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
        self.ch() == "break" or self.ch() == "continue" or self.ch() == "static" or self.ch() == "DT" or
        self.ch() == "ID" or self.ch() == "class" or self.ch() == "abstract" or self.ch() == "final" or self.ch() == "this" or self.ch() == "super"):
            if (self.opFrom()):
                if (self.S()):
                    return True
        else:
            if (self.ch() == '$'):
                return True
        return False

 #First(S) ={while, for, return, if, break, continue, abstract, static, DT, func, ID, class, final, e ,this, super}
#<S> --> <SST> <S>  ==> {while, for, return, if, break, continue, ID, this, super} 
# <S> --> | <f’’> <S2>  ==> { final, class, abstract, static, DT, func}
# <S> -->|e ==> {$}
    def S(self):
        if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or self.ch() == "this" or self.ch() == "super" or
        self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "static" or self.ch() == "DT" or 
        self.ch() == "class" or self.ch() == "abstract" or self.ch() == "final" or self.ch() == "public" or self.ch() == "private"):
            #----
            if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
            self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super" ):
                if (self.SST()):
                    if(self.S()):
                        return True

            else:
                if (self.ch() == "static" or self.ch() == "DT" or self.ch() == "final" or 
                self.ch() == "abstract" or self.ch() == "class" or self.ch() == "public" or self.ch() == "private"):
                    if (self.fdouble()):
                        if(self.S2()):
                            return True
        else:
            if (self.ch() == '$'):
                return True 
        return False

#<opFrom> --> <From> | e
#First = { from, e }
#follow opfrom = first (S)= ={while, for, return, if, break, continue, Id, static, DT, func, abstract, final, class, , this, super }
    def opFrom(self):
        if (self.ch() == 'from'):
            if(self.frm()):
                return True
        else:
            if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
                self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "static" or 
                self.ch() == "DT" or self.ch() == "final" or self.ch() == "abstract" or 
                self.ch() == "class" or self.ch() == "this" or self.ch() == "super" or self.ch() == "$"):
                return True
        return False
#First(S2) = {abstract, private, public,  class, DT, func, Static}
#<S2> --> abstract<anew> 
# | <class_def><S>
# | DT <var_func> 
# | static <Snew>
    def S2(self):
        if (self.ch() == "abstract" or self.ch() == "static" or self.ch() == "DT" or self.ch() == "class" or
            self.ch() == "public" or self.ch() == "private"):
            if (self.ch() == 'abstract'):
                self.i += 1
                if(self.anew()):
                    return(True)
            elif (self.ch() == "class" or self.ch() == "public" or self.ch() == "private"):
                if (self.class_def()):
                    if (self.S()):
                        return True
            elif (self.ch() == "DT"):
                self.i += 1
                if (self.var_func()):
                    return True
            else:
                if (self.ch() == "static"):
                    self.i += 1
                    if (self.Snew()):
                        return True
        return False
#<var_func> --> <fdec><S> | <func_st><S>	{ID, func}    
    def var_func(self):
        if (self.ch() == "ID" or self.ch() == "func"):
            if (self.ch() == "ID"):
                if (self.fdec()):
                    if(self.S()):
                        return True
            else:
                if(self.ch() == "func"):
                    if(self.func_st()):
                        if(self.S()):
                            return True
        return False

# First(Snew) = {DT}
#<Snew> --> DT  <var_func>
    def Snew(self):
        if (self.ch() == "DT"):
            self.i += 1
            if (self.var_func()):
                return True
        return False
    
#<anew> --> <class_def> <S> | Static DT <func_st> <S> | DT <func_st><S>
#First(anew) = {public, private, class, Static, DT}
    def anew(self):
        if (self.ch() == "static" or self.ch() == "DT"or self.ch() == "class" or self.ch() == "public" or self.ch() == "private"):
            if (self.ch() == "class" or self.ch() == "public" or self.ch() == "private"):
                if (self.class_def()):
                    if (self.S()):
                        return True
            elif (self.ch() == "static"):
                self.i += 1
                if (self.ch() == "DT"):
                    self.i += 1
                    if (self.func_st()):
                        if(self.S()):
                            return True
            else:
                if (self.ch() == "DT"):
                    self.i += 1
                    if (self.func_st()):
                        if(self.S()):
                            return True
        return False

#<Dec> --> <init>  <lst> ==> {:=, ; , ‘,’}
    def Dec(self):
        if ((self.ch() == ':=') or (self.ch() == ';') or (self.ch() == ',')):
            if (self.init()):
                if (self.lst()):
                    return True
        return False
# First(lst) = {; , ','} 
#<list> --> ; | , ID <init><list>
    def lst(self):
        #create new main check. then rules check.
        if (self.ch() == ";" or self.ch() == ","):
            if (self.ch() == ";"):
                self.i += 1
                return True
            else:
                if (self.ch() == ","):
                    self.i += 1
                    if (self.ch() == "ID"):
                        self.i += 1
                        if (self.init()):
                            if (self.lst()):
                                return True
        return False
#First (init) = {e, :=}
#Follow(init) = {; , ’,’}                        ctrl"/
#<init> --> := <initE> | e
    def init(self):
        if (self.ch() == ":="):
            self.i += 1
            if(self.initE()):
                return True
        else:
            if(self.ch() == ";" or self.ch() == ","):
                return True
        return False

    def const(self):
        if (self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or self.ch() == "StringConst" or 
        self.ch() == "charConstant" or self.ch() == "boolConstant"):
            self.i += 1
            return True
        else:
            return False
#<initE> --> ID<new>|<TS> ID<LHP><Tdash><Edash>| <const><Tdash><Edash> | !<F> <Tdash><Edash>|(<E>) <Tdash><Edash> 
#First(initE) = {this, super, const, ( , ! , ID}
    def initE(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "boolConstant" or self.ch() == "(" or 
        self.ch() == "!" or self.ch() == "ID"):
            if (self.ch() == "ID"):
                self.i += 1
                if (self.new()):
                    return True
            elif(self.ch() == "this" or self.ch() == "super"):
                if(self.TS()):
                    if (self.ch() == "ID"):
                        self.i += 1
                        if(self.LHP()):
                            if(self.Tdash()):
                                if(self.Edash()):
                                    return True
            elif(self.ch() == "IntegerConstant" or self.ch() == "boolConstant" or self.ch() == "FloatConstant" or self.ch() == "StringConst" or self.ch() == "charConstant"):
                if (self.const()):
                    if (self.Tdash()):
                        if(self.Edash()):
                            return True
            elif (self.ch() == "!"):
                self.i += 1
                if(self.F()):
                    if (self.Tdash()):
                        if(self.Edash()):
                            return True
            else: #(<E> ) <Tdash> <Edash> 
                if (self.ch() == "("):
                    self.i += 1
                    if (self.E()):
                        if(self.ch() == ")"):
                            self.i += 1
                            if(self.Tdash()):
                                if(self.Edash()):
                                    return True
        return False
#First(new) ={ :=, [ , ( , . , e}
# Follow(new) = {; , ,}
# <new> --> <init> | <LHP><TDash><Edash> 
    def new(self):
        if (self.ch() == ":=" or self.ch() == "[" or self.ch() == "(" or self.ch() == "."):
            if (self.ch() == ":="):
                if (self.init()):
                    return True
            else:
                if(self.ch() == "[" or self.ch() == "(" or self.ch() == "."):
                    if(self.LHP()):
                        if(self.Tdash()):
                            if (self.Edash()):
                                return True
        else:
            if (self.ch() == ";" or self.ch() == ","):
                return True
        return False
#<while_st> --> while ( <OE> ) <body>	First(while_st) = {while}
    def while_st(self):
        if(self.ch() == "while"):
            self.i += 1
            if (self.ch() == "("):
                self.i += 1
                if (self.OE()):
                    if (self.ch() == ")"):
                        self.i += 1
                        if(self.body()):
                            return True
        return False
#<break> --> break; 	First(break) = {break}
    def brk(self):
        if (self.ch() == "break"):
            self.i += 1
            if (self.ch() == ";"):
                self.i += 1
                return True
        return False
#<continue> --> continue;	First(continue) = {continue}
    def cont(self):
        if (self.ch() == "continue"):
            self.i += 1
            if (self.ch() == ";"):
                self.i += 1
                return True
        return False
#<for_st> --> for ( <f1> <f2> ; <f3>) <body>	First(for_st) = {for}
    def for_st(self):
        if (self.ch() == "for"):
            self.i += 1
            if (self.ch() == "("):
                self.i += 1
                if (self.f1()):
                    if(self.f2()):
                        if (self.ch() == ";"):
                            self.i += 1
                            if(self.f3()):
                                if self.ch() == ")":
                                    self.i += 1
                                    if(self.body()):
                                        return True
        return False

#First(f1) = {DT, ID, ;}	            
#<f1> --> DT Id <Dec>                   First(f1) = {DT}
#<f1> --> ID <RHP> <asgn_st> ;     First(f1) = {ID}
#<f1> --> ;                    First(f1) = {;}
    def f1(self):
        if (self.ch() == "DT" or self.ch() == "ID" or self.ch() == ";"):
            if self.ch() == "DT":
                self.i += 1
                if(self.ch() == "ID"):
                    self.i += 1
                    if (self.Dec()):
                        return True
            elif(self.ch() == "ID"):
                    self.i += 1
                    if(self.RHP()):
                        if(self.asgn_st()):
                            if (self.ch() == ";"):
                                self.i += 1
                                return True
            else:
                if(self.ch() == ";"):
                    self.i += 1
                    return True
        return False
#<f2> --> <OE> {this, super, const, ( , ! , ID}
#<f2> --> e         Follow(f2) = {;}
    def f2(self):
        if(self.ch() == "this" or self.ch() == "super" or self.ch() == "IntegerConstant" or self.ch() == "boolConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.OE()):
                return True
        else:
            if (self.ch() == ";"):
                return True
        return False
#<f3> --> ID <RHP> <f3d>        First(f3) = {ID}
#<f3> --> inc_dec ID <LHP>      First (f3) = {inc_dec}
#<f3> --> e             First (f3) = {e}     Follow(f3) = { ) } First(f3) = {Id, ++, --, e}
    def f3(self):
        if (self.ch() == "Increment/Decrement" or self.ch() == "ID"):
                if (self.ch() == "ID"):
                    self.i += 1
                    if (self.RHP()):
                        if(self.f3d()):
                            return True
                else:
                    if(self.ch() == "Increment/Decrement"):
                        self.i += 1
                        if(self.ch() == "ID"):
                            self.i += 1
                            if (self.LHP()):
                                return True
        else:
            if (self.ch() == ")"):
                return True
        return False
#<f3d> --> <asgn_st> 
#<f3d> --> inc_dec
#First(f3d) = { ++, --, := , CompAsgnOP }
    def f3d(self):
        if (self.ch() == "Increment/Decrement" or self.ch() == ":=" or self.ch() == "Compound Assignment"):
            if (self.ch() == ":=" or self.ch() == "Compound Assignment"):
                if (self.asgn_st()):
                    return True
            else:
                if(self.ch() == "Increment/Decrement"):
                    self.i += 1
                    return True
        return False

#<asgn_st> --> <asgn_op> <asg>
#First (asgn_st) = {:= , CompAsgnOP }
    def asgn_st(self):
        if (self.ch() == ":=" or self.ch() == "Compound Assignment"):
            if(self.asgn_op()):
                if(self.asg()):
                    return True
        return False

#<asg> --> <E> | <object_call>
#First(asg) = {this, super, const, ( , ! , ID, obj}
    def asg(self):
        if(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or 
        self.ch() == "ID", self.ch() == "obj"):
            if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
            self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
                if(self.E()):
                    return True
            else:
                if(self.ch() == "obj"):
                    if(self.object_call()):
                        return True
        return False
#<asgn_op> --> :=      <asgn_op> --> CompAsgnOp
    def asgn_op(self):
        if (self.ch() == ":=" or self.ch() == "Compound Assignment"):
            if (self.ch() == ":="):
                self.i += 1
                return True
            else:
                if(self.ch() == "Compound Assignment"):
                    self.i += 1
                    return True
        return False
#<if_else_st> --> if ( <cond>) <body> <op_else>
    def if_else_st(self):
        if (self.ch() == "if"):
            self.i += 1
            if (self.ch() == "("):
                self.i += 1
                if (self.cond()):
                    if (self.ch() == ")"):
                        self.i += 1
                        if(self.body()):
                            if (self.op_else()):
                                return True
        return False
#<op_else> --> else <body>| e     #else
# follow = while, for, return, if, break, continue, ID, , static, final, abstract, func, DT
    def op_else(self):
        if (self.ch() == "else"):
            self.i += 1
            if(self.body()):
                return True
        else:
            if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
            self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "}" or
            self.ch() == "static" or self.ch() == "final" or self.ch() == "abstract" or self.ch() == "func" or
            self.ch() == "DT" or self.ch() == "class" or self.ch() == "this" or self.ch() == "super"):
                return True
        return False

#<cond> --> ID <cond_new> | <TS> ID <LHP> <Tdash> <Edash> <REdash> <AEdash> <OEdash> |
 # ! F <Tdash><Edash> <REdash><AEdash><OEdash> |
# <const> <Tdash><Edash> <REdash> <AEdash> <OEdash> | ( <E> ) <Tdash><Edash> <REdash><AEdash><OEdash>
    def cond(self):
        if(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or 
            self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or self.ch() == "StringConst" or 
            self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.ch() == "ID"):
                self.i += 1
                if (self.cond_new()):
                    return True

            elif (self.ch() == "this" or self.ch() == "super"):
                if (self.TS()):
                    if (self.ch() == "ID"):
                        self.i += 1
                        if (self.LHP()):
                            if(self.Tdash()):
                                if(self.Edash()):
                                    if(self.REdash()):
                                        if (self.AEdash()):
                                            if (self.OEdash()):
                                                return True

            elif (self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
                self.ch() == "StringConst" or self.ch() == "charConstant"):
                if (self.const()):
                    if(self.Tdash()):
                        if(self.Edash()):
                            if(self.REdash()):
                                if (self.AEdash()):
                                    if (self.OEdash()):
                                        return True
            
            elif (self.ch() == "!" ): #! F <Tdash><Edash> <REdash><AEdash><OEdash>
                if(self.F()):
                    if(self.Tdash()):
                        if(self.Edash()):
                            if(self.REdash()):
                                if (self.AEdash()):
                                    if (self.OEdash()):
                                        return True
            
            else: #( <E> ) <Tdash><Edash> <REdash><AEdash><OEdash>
                if(self.ch() == "("):
                    self.i += 1
                    if (self.E()):
                        if(self.ch() == ")"):
                            self.i += 1
                            if(self.Tdash()):
                                if(self.Edash()):
                                    if(self.REdash()):
                                        if (self.AEdash()):
                                            if (self.OEdash()):
                                                return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<cond_new> -> in ID <array> | <LHP> <Tdash> <Edash> <REdash> <AEdash> <OEdash>    
# first = [ , ( , . , MDM, PM, ROP, &&,  || 

    def cond_new(self):
        if (self.ch() == "in" or self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or 
            self.ch() == "&&" or self.ch() == "||" or self.ch() == "." or self.ch() == "Multiply/Divide/Modulus" or
            self.ch() == "(" or self.ch() == "["):
            if (self.ch() == "in"):
                self.i += 1
                if (self.ch() == "ID"):
                    self.i += 1
                    if(self.array()):
                        return True
            else:
                if(self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or 
                self.ch() == "&&" or self.ch() == "||" or self.ch() == "." or 
                self.ch() == "Multiply/Divide/Modulus" or self.ch() == "(" or self.ch() == "["):
                    if (self.LHP()):
                        if(self.Tdash()):
                            if(self.Edash()):
                                if(self.REdash()):
                                    if (self.AEdash()):
                                        if (self.OEdash()):
                                            return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<array> --> [<E>]<array1>      ==>First(array) = {[}
    def array(self):
        if (self.ch() == "["):
            self.i += 1
            if (self.E()):
                if self.ch() == "]":
                    self.i += 1
                    if (self.array1()):
                        return True
        return False
#<array1> --> [<E>] <array2> | e ==> First (array1) = {[, e} ==> Follow(array1) = {)}
    def array1(self):
        if (self.ch() == "["):
            self.i += 1
            if (self.E()):
                if self.ch() == "]":
                    self.i += 1
                    if (self.array2()):
                        return True
        else:
            if(self.ch() == ")" or self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "." or
                self.ch() == "Increment/Decrement" or self.ch() == "Multiply/Divide/Modulus" or 
                self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or self.ch() == "&&" or 
                self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<array2> --> [<E>] | e         ==> First(array2) = {[, e}    ==> Follow(array2) = {)}
    def array2(self):
        if (self.ch() == "["):
            self.i += 1
            if (self.E()):
                if self.ch() == "]":
                    self.i += 1
                    return True
        else:
            if(self.ch() == ")" or self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "." or
                self.ch() == "Increment/Decrement" or self.ch() == "Multiply/Divide/Modulus" or 
                self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or self.ch() == "&&" or 
                self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<OE> --> <AE> <OEDASH> ==> First (OE) = {this, super, const, ( , ! , ID}  
    def OE(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.AE()):
                if(self.OEdash()):
                    return True
        return False

#<OEDASH> --> || <AE> <OEDASH> | e  ==> First (OEDASH) = {||, e}
#Follow (OEDASH) = {‘,’ , ; , ), ] }
    def OEdash(self):
        if (self.ch() == "||"):
            self.i += 1
            if (self.AE()):
                if(self.OEdash()):
                    return True
        else:
            if(self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<AE> --> <RE> <AEDASH> ==> First (AE) = {this, super, const, ( , ! , ID}
    def AE(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.RE()):
                if(self.AEdash()):
                    return True
        return False

#<AEDASH> --> && <RE> <AEDASH> | e ==> First (AEDASH) = {&&, }
#Follow (AEDASH) = {||, ‘,’ , ; , ), ] }
    def AEdash(self):
        if (self.ch() == "&&"):
            self.i += 1
            if (self.RE()):
                if(self.AEdash()):
                    return True
        else:
            if(self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<RE> --> <E> <REDASH>   ==> First (RE) = {this, super, const, ( , ! , ID}
    def RE(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.E()):
                if(self.REdash()):
                    return True
        return False

#<REDASH> --> ROP <E> <REDASH> | e ==> First (REDASH) = {ROP, e}
#Follow (REDASH) ={&&, ||, ‘,’ , ; , ), ] }
    def REdash(self):
        if (self.ch() == "Relational Operator"):
            self.i += 1
            if (self.E()):
                if(self.REdash()):
                    return True
        else:
            if(self.ch() == "&&" or self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<E> --> <T> <EDASH>  ==> First (E) = {this, super, const, ( , ! , ID}
    def E(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.T()):
                if(self.Edash()):
                    return True
        return False

#<EDASH> --> PM <T> <EDASH> | e  ==>First (EDASH) = {PM, }
#Follow(EDASH) ={ROP, &&, ||, ‘,’ , ; , ), ] }
    def Edash(self):
        if (self.ch() == "Plus/Minus"):
            self.i += 1
            if (self.T()):
                if(self.Edash()):
                    return True
        else:
            if(self.ch() == "Relational Operator" or self.ch() == "&&" or self.ch() == "||" or 
            self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<T> --> <F> <TDASH> ==> First (T) = {this, super, const, ( , ! , ID}
    def T(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or 
        self.ch() == "FloatConstant" or self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or 
        self.ch() == "!" or self.ch() == "ID"):
            if (self.F()):
                if(self.Tdash()):
                    return True
        return False

#<TDASH> --> MDM <F> <TDASH> | e   ==> First (TDASH) = {MDM, }
#Follow (TDASH) = {PM, ROP, &&, ||, ‘,’ , ; , ), ]}
    def Tdash(self):
        if (self.ch() == "Multiply/Divide/Modulus"):
            self.i += 1
            if (self.F()):
                if(self.Tdash()):
                    return True
        else:
            if(self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or self.ch() == "&&" or self.ch() == "||" or 
            self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<F> --> <TS> ID <LHP> | <const> | ( <E>)   | ID<LHP> #First(F) = {this, super, const, ( , ! , ID}
    def F(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
        self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or self.ch() == "ID"):
            if (self.ch() == "this" or self.ch() == "super"):
                if (self.TS()):
                    if (self.ch() == "ID"):
                        self.i += 1
                        if (self.LHP()):
                            return True

            elif (self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
                    self.ch() == "StringConst" or self.ch() == "charConstant"):
                if (self.const()):
                    return True

            elif(self.ch() == "("):
                self.i += 1
                if (self.E()):
                    if self.ch() == ")":
                        self.i += 1
                        return True

            else:
                if (self.ch() == "ID"): #ID<LHP>
                    self.i += 1
                    if(self.LHP()):
                        return True
        return False

#<TS>  this. | super.    ==> First(TS) = {this, super}
    def TS(self):
        if (self.ch() == 'this' or self.ch() == "super"):
            if (self.ch() == 'this'):
                self.i += 1
                if (self.ch() == "."):
                    self.i += 1
                    return True
            else:
                if(self.ch() == "super"):
                    self.i += 1
                    if (self.ch() == "."):
                        self.i += 1
                        return True
        return False

#<LHP> First (LHP) = { [ , ( , . , e}
#Follow(LHP) = {:= , CompAsgnOP, ++, --, MDM, PM, ROP, &&, ||, ‘,’ , ; , ), ]}
    def LHP(self):
        if (self.ch() == "[" or self.ch() == "(" or self.ch() == "."):
            if (self.ch() == "["):  #<array> 
                if (self.array()):
                    if (self.LHP3()):
                       return True

            elif(self.ch() == "("): #(<argument>) <LHP3>      
                self.i += 1
                if(self.argument()):
                    if(self.ch() == ")"):
                        self.i += 1
                        if(self.LHP3()):
                            return True
            
            else:
                if(self.ch() == "."): #<LHP1>
                    if(self.LHP1()):
                        return True
        else:
            if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
             self.ch() == "Multiply/Divide/Modulus" or self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or 
             self.ch() == "&&" or self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<LHP3> --> <LHP1> | e
    def LHP3(self):
        if(self.ch() == "."):
            if(self.LHP1()):
                return True
        else:
            if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
             self.ch() == "Multiply/Divide/Modulus" or self.ch() == "Plus/Minus" or self.ch() == "Relational Operator" or 
             self.ch() == "&&" or self.ch() == "||" or self.ch() == "," or self.ch() == ";" or self.ch() == ")" or self.ch() == "]"):
                return True
        return False

#<LHP1> --> .ID <LHP> 
    def LHP1(self):
        if(self.ch() == "."):
            self.i += 1
            if(self.ch() == "ID"):
                self.i += 1
                if(self.LHP()):
                    return True
        return False

#<func_st> --> func ID ( <parameters>) { <MST>} 
    def func_st(self):
        if(self.ch() == "func"):
            self.i += 1
            if (self.ch() == "ID"):
                self.i += 1
                if (self.ch() == "("):
                    self.i += 1
                    if(self.parameters()):
                        if (self.ch() == ")"):
                            self.i += 1
                            if (self.ch() == "{"):
                                self.i += 1
                                if(self.MST()):
                                    if(self.ch() == "}"):
                                        self.i += 1
                                        return True
        return False

#<parameters> --> DT ID <p0> <p1> | ID ID <p0> <p1> | e ===> First (parameters) = {DT,ID e}	Follow (parameters) = { ) }
    def parameters(self):
        if (self.ch() == "DT" or self.ch() == "ID"):
            if (self.ch() == "DT"):
                self.i += 1
                if (self.ch() == "ID"):
                    self.i += 1
                    if(self.p0()):
                        if(self.p1()):
                            return True
            else:
                if(self.ch() == "ID"):
                    self.i += 1
                    if (self.ch() == "ID"):
                        self.i += 1
                        if(self.p0()):
                            if(self.p1()):
                                return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<p0> --> := <E><p1> | <array_dec> | e ==>First(p0) = {:= ,e, [ }	==>Follow (p0) = { ,, ) }
    def p0(self):
        if (self.ch() == ":=" or self.ch() == "["):
            if (self.ch() == ":="):
                self.i += 1
                if(self.E()):
                    if(self.p1()):
                        return True
            else:
                if(self.ch() == "["):
                    self.i += 1
                    if(self.array()):
                        return True
        else:
            if(self.ch() == ")", self.ch() == ","):
                return True
        return False

#<p1> --> ,<parameters> | e ==> First (p1) = {, , }	Follow (p1) = { ) }
    def p1(self):
        if (self.ch() == ","):
            self.i += 1
            if(self.parameters()):
                return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<return_st> --> return <OE>; 	First (return_st) = {return}
    def return_st(self):
        if (self.ch() == "return"):
            self.i += 1
            if (self.OE()):
                if(self.ch() == ";"):
                    self.i += 1
                    return True
        return False

#<argument> --> <OE><A1> |e ==> First (argument) = {this, super, const, ( , ! , ID, e} =>Follow (argument) = { ) }
    def argument(self):
        if (self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or 
        self.ch() == "FloatConstant" or self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or 
        self.ch() == "!" or self.ch() == "ID"):
            if(self.OE()):
                if(self.A1()):
                    return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<A1> --> , <argument> | e ==>First (A1) = {, , }	Follow (A1) = { ) }
    def A1(self):
        if (self.ch() == ","):
            self.i += 1
            if(self.argument()):
                return True
        else:
            if(self.ch() == ")"):
                return True
        return False

#<AM> --> public | private | null    follow() = {class, static, final, abstract, DT}
    def AM(self):
        if (self.ch() == 'public' or self.ch() == 'private'):
            self.i += 1
            return True
        else:
            if (self.ch() == "class" or self.ch() == "static" or self.ch() == "final" or 
                self.ch() == "abstract" or self.ch() == "DT"):
                return True
        return False

#<class_def> --> <AM>class ID <inherits> {<class_body>}	==> First (class_def) = {public, private, class}
    def class_def(self):
        if (self.ch() == "public" or self.ch() == "private" or self.ch() == "class"):
            if(self.AM()):
                if(self.ch() == "class"):
                    self.i += 1
                    if (self.ch() == "ID"):
                        self.i += 1
                        if(self.inherits()):
                            if (self.ch() == "{"):
                                self.i += 1
                                if(self.class_body()):
                                    if(self.ch() == "}"):
                                        self.i += 1
                                        return True
        return False

#<inherits> --> inherits ID | e ==> First (inherits) = {inherits, }	Follow (inherits) = { { }
    def inherits(self):
        if(self.ch() == "inherits"):
            self.i += 1
            if (self.ch() == "ID"):
                self.i += 1
                return True
        else:
            if(self.ch() == "{"):
                return True
        return False

#<class_body>--> <const_st> <class_body> | <AM><SST2><class_body> | e ==>First(class_body) = {construct,static, final, abstract, func, DT},	Follow(class_body) = { } }
    def class_body(self):
        if (self.ch() == "abstract" or self.ch() == "static" or self.ch() == "DT" or 
            self.ch() == "final" or self.ch() == "construct" or self.ch() == "public" or self.ch() == "private"):
            if (self.ch() == "construct"):
                if (self.const_st()):
                    if(self.class_body()):
                        return True
            else:
                if (self.ch() == "abstract" or self.ch() == "static" or self.ch() == "DT" or self.ch() == "public" or 
                self.ch() == "private" or self.ch() == "final"):
                    if (self.AM()):
                        if(self.SST2()):
                            if(self.class_body()):
                                return True
        else:
            if(self.ch() == "}"):
                return True
        return False

#<const_st> -> construct func ID (<parameters>) {<const_body>}
    def const_st(self):
        if (self.ch() == "construct"):
            self.i += 1
            if(self.ch() == "func"):
                self.i += 1
                if (self.ch() == "ID"):
                    self.i += 1
                    if (self.ch() == "("):
                        self.i += 1
                        if(self.parameters()):
                            if (self.ch() == ")"):
                                self.i += 1
                                if (self.ch() == "{"):
                                    self.i += 1
                                    if(self.const_body()):
                                        if(self.ch() == "}"):
                                            self.i += 1
                                            return True
        return False

# <const_body> -> <create> <const_body> |<fdec>
# # self.ch() == "this" or self.ch() == "super" or self.ch() == "DT"
    def const_body(self):
        if (self.ch() == "this" or self.ch() == "super"):
            if (self.create()):
                if (self.const_body()):
                    return True
        elif (self.ch() == "DT"):
            self.i += 1
            if (self.fdec()):
                if (self.const_body()):
                    return True
        else:
            if (self.ch() == "}"):
                return True
        return False

# <create> --> <TS> ID := ID; first(create) = this, super
    def create(self):
        if(self.ch() == "this" or self.ch() == "super"):
            if(self.TS()):
                if(self.ch() == "ID"):
                    self.i+= 1
                    if(self.ch() == ":="):
                        self.i += 1
                        if(self.ch() == "ID"):
                            self.i += 1
                            if(self.ch() == ";"):
                                self.i += 1
                                return True
        return False

#<object_call> -->  obj ID (<argument>)	==>First(object_call) = {obj}
    def object_call(self):
        if(self.ch() == "obj"):
            self.i += 1
            if (self.ch() == "ID"):
                self.i += 1
                if (self.ch() == "("):
                    self.i += 1
                    if(self.argument()):
                        if(self.ch() == ")"):
                            self.i += 1
                            return True
        return False

#<imprt> --> import <something>;   ==> First(imprt) = {import}
    def imprt(self):
        if(self.ch() == "import"):
            #print("import")
            self.i += 1
            if(self.something()):
                if(self.ch() == ";"):
                    #print(";")
                    self.i += 1
                    return True
        return False

#<something> --> ID | *	  ==> First(something) = {ID | *}
    def something(self):
        if(self.ch() == "ID"):
            #print("nxt ID")
            self.i += 1
            return True
        else:
            if(self.ch() == "*"):
                self.i += 1
                return True
        return False

#<frm> --> from ID <imprt>	==> First(frm) = {from}
    def frm(self):
        if(self.ch() == "from"):
            self.i += 1
            if(self.ch() == "ID"):
                #print("ID")
                self.i += 1
                if(self.imprt()):
                    return True
        return False

#<array_dec> -->  [<E>] <dec2>	==> First(array_dec) = {[}
    def array_dec(self):
        if(self.ch() == "["):
            self.i += 1
            if (self.E()):
                if (self.ch() == "]"):
                    self.i += 1
                    if(self.dec2()):
                        return True
        return False

#<dec2> --> <init1><arr> | [<E>] <dec3> ==> {; , ‘,’, :=, [}
    def dec2(self):
        if(self.ch() == ";" or self.ch() == "," or self.ch() == ":=" or self.ch() == "["):
            if (self.ch() == ";" or self.ch() == "," or self.ch() == ":="):
                if(self.init1()):
                    if(self.arr()):
                        return True
            else:
                if(self.ch() == "["):
                    self.i += 1
                    if (self.E()):
                        if (self.ch() == "]"):
                            self.i += 1
                            if(self.dec3()):
                                return True
        return False

#<dec3> --> <init2><arr>|[<E>] <init3><arr> ==> {:=, ; , ‘,’, [}
    def dec3(self):
        if(self.ch() == ";" or self.ch() == "," or self.ch() == ":=" or self.ch() == "["):
            if (self.ch() == ";" or self.ch() == "," or self.ch() == ":="):
                if(self.init2()):
                    if(self.arr()):
                        return True
            else:
                if(self.ch() == "["):
                    self.i += 1
                    if (self.E()):
                        if (self.ch() == "]"):
                            self.i += 1
                            if(self.init3()):
                                if(self.arr()):
                                    return True
        return False

#<arr> --> ; | , ID <array_dec>	==> First (arr) = { ; , ‘,’}
    def arr(self):
        if(self.ch() == ";" or self.ch() == ","):
            if(self.ch() == ";"):
                self.i += 1
                return True
            else:
                if(self.ch() == ","):
                    self.i += 1
                    if (self.ch() == "ID"):
                        self.i += 1
                        if(self.array_dec()):
                            return True
        return False

#<init1> --> := [<Exp>] | e ==>	First(init1) = {:= , e}	==> Follow(init1) = {; , ‘,’} 
    def init1(self):
        if (self.ch() == ":="):
            self.i += 1
            if(self.ch() == "["):
                self.i += 1
                if(self.Exp()):
                    if(self.ch() == "]"):
                        self.i += 1
                        return True
        else:
            if(self.ch() == ";" or self.ch() == ","):
                return True
        return False

#<Exp> --> <E><Exp1> |e ==>	First (Exp) {this, super, const, ( , ! , ID, e } ==> Follow(Exp) = {]}
    def Exp(self):
        if(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or 
        self.ch() == "FloatConstant" or self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or 
        self.ch() == "!" or self.ch() == "ID"):
            if(self.E()):
                if(self.Exp1()):
                    return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<Exp1> --> ,<E><Exp1> | 	First (Exp1) = {, , e}	Follow (Exp1) = {]}
    def Exp1(self):
        if(self.ch() == ","):
            self.i += 1
            if(self.E()):
                if(self.Exp1()):
                    return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<init2> --> := [<init2d>] | e	==>First(init2) = {:=, e}	==>Follow (init2) = {; , ‘,’}
    def init2(self):
        if (self.ch() == ":="):
            self.i += 1
            if(self.ch() == "["):
                self.i += 1
                if(self.init2d()):
                    if(self.ch() == "]"):
                        self.i += 1
                        return True
        else:
            if(self.ch() == ";" or self.ch() == ","):
                return True
        return False

#<init2d> --> [<Exp>]<init2_dash>| e ==> First(init2d) = {[, e}	==> Follow(init2d) = {]}
    def init2d(self):
        if (self.ch() == "["):
                self.i += 1
                if(self.Exp()):
                    if(self.ch() == "]"):
                        self.i += 1
                        if(self.init2_dash()):
                            return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<init2_dash> --> ,<init2d> | e ==>	First(init2_dash) = {‘,’ , e}	==> Follow(init2_dash) = {]}
    def init2_dash(self):
            if(self.ch() == ","):
                self.i += 1
                if(self.init2d()):
                    return True
            else:
                if(self.ch() == "]"):
                    return True
            return False

#<init3> --> := [<init3d>]  | e ==>	First(init3) = {:=, e}	==>Follow(init3) = {; , ‘,’}
    def init3(self):
        if (self.ch() == ":="):
            self.i += 1
            if(self.ch() == "["):
                self.i += 1
                if(self.init3d()):
                    if(self.ch() == "]"):
                        self.i += 1
                        return True
        else:
            if(self.ch() == ";" or self.ch() == ","):
                return True
        return False

#<init3d> --> [<init3_dash>] <callinit3d>| e ==>First(init3d) = {[, e} ==> Follow(init3d) = {]}
    def init3d(self):
        if (self.ch() == "["):
                self.i += 1
                if(self.init3_dash()):
                    if(self.ch() == "]"):
                        self.i += 1
                        if(self.callinit3d()):
                            return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<init3_dash> --> <init2d> | e ==> First (init3_dash) = {[,e} ==> Follow (init3_dash) = {]}
    def init3_dash(self):
        if (self.ch() == "["):
                if(self.init2d()):
                    return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<callinit3d> --> ,<init3d>| e ==>	First(callinit3d) = {‘,’ ,e} ==> Follow(callinit3d) = {]}
    def callinit3d(self):
        if(self.ch() == ","):
            self.i += 1
            if(self.init3d()):
                return True
        else:
            if(self.ch() == "]"):
                return True
        return False

#<SST> --> <while_st> |<for_st>|<return_st> | <if_else_st> | <brk> | <cont> | ID<call>|<create>
# First(SST) = {while, for, return, if, break, continue, ID}
    def SST(self):
        if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
        self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super"):
            if(self.ch()=="while"):
                if(self.while_st()):
                    return True
            elif(self.ch() == "for"):
                if(self.for_st()):
                    return True
            elif(self.ch() =="return"):
                if(self.return_st()):
                    return True
            elif(self.ch()=="if"):
                if(self.if_else_st()):
                    return True
            elif(self.ch() == "break"):
                if(self.brk()):
                    return True
            elif(self.ch() == "continue"):
                if(self.cont()):
                    return True
            elif (self.ch() == "this" or self.ch() == "super"):
                if(self.TS()):
                    if(self.ch() == "ID"):
                        self.i += 1
                        if(self.RHP()):
                            if(self.asgn_op()):
                                if(self.E()):
                                    if (self.ch() == ";"):
                                        self.i += 1
                                        return True
            else:
                if(self.ch() == "ID"):
                    self.i += 1
                    if(self.call()):
                        return True
        return False

#<call>--> (<argument>) <func_call>  | <RHP1> <f3op>; | <f3op>;  | [<E>]<call2> 
# ==> { (, . , ++, --, := , CompAsgnOP, ; , [ }
    def call(self):
        if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
            self.ch() == "[" or self.ch() == "(" or self.ch() == "." or self.ch() == ";"):
            if(self.ch() == "("): #(<argument>) <func_call>     
                self.i += 1
                if(self.argument()):
                    if(self.ch() == ")"):
                        self.i += 1
                        if(self.func_call()):
                            return True 
            elif (self.ch() == "."): #<RHP1> <f3op>;
                if (self.RHP1()):
                    if (self.f3op()):
                        if (self.ch() == ";"):
                                self.i += 1
                                return True
            elif(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
                self.ch() == ";"): #<f3op>;
                if (self.f3op()):
                    if (self.ch() == ";"):
                            self.i += 1
                            return True
            else:
                if(self.ch() == "["): #[<E>]<call2> 
                    self.i += 1
                    if(self.E()):
                        if(self.ch() == "]"):
                            self.i += 1
                            if(self.call2()):
                                return True
        return False

# func_call --> <RHP1> <f3op> ; | ;
    def func_call(self):
        if (self.ch() == "."):
            if(self.RHP1()):
                if(self.f3op()):
                    if (self.ch() == ";"):
                        self.i += 1
                        return True 
        else:
            if(self.ch() == ";"):
                self.i += 1
                return True
        return False
# <call2> --> <RHP1><f3op>; | inc_dec; | compoundAsgnop <asg> ; | [<E>] <call3> | , ID <array_dec> | 
#              := <call2z> | ; <call2y> 
#{.} U { ++, --,} U {CompAsgnOP} U {[} U {,} U {:=} U {;} 
#
    def call2(self):
        if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
            self.ch() == "[" or self.ch() == "(" or self.ch() == "." or self.ch() == ";"):
            if (self.ch() == "."): #<RHP1> <f3op>;
                if (self.RHP1()):
                    if (self.f3op()):
                        if (self.ch() == ";"):
                                self.i += 1
                                return True
            elif (self.ch() == "Increment/Decrement"):
                self.i += 1
                if (self.ch() == ";"):
                    self.i += 1
                    return True
            elif(self.ch() == "Compound Assignment"):
                self.i += 1
                if (self.asg()):
                    if (self.ch() == ";"):
                        self.i += 1
                        return True
            elif(self.ch() == "["):
                self.i += 1
                if(self.E()):
                    if(self.ch() == "]"):
                        self.i += 1
                        if(self.call3()):
                            return True
            elif(self.ch() == ","):
                self.i += 1
                if(self.ch() == "ID"):
                    self.i += 1 
                    if(self.array_dec()):
                        return True
            elif (self.ch() == ":="):
                self.i += 1 
                if(self.call2z()):
                    return True
            else:
                if (self.ch() == ";"):
                    self.i += 1 
                    if(self.call2y()):
                        return True
        else:
            return False
# call2z
    def call2z(self):
        if (self.ch() == "["):
            self.i += 1
            if(self.Exp()):
                if (self.ch() == "]"):
                    self.i += 1
                    if (self.arr()):
                        return True
        elif(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
            self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or 
            self.ch() == "ID", self.ch() == "obj"):
            if(self.asg()):
                if (self.ch() == ";"):
                    self.i += 1
                    return True
        else:
            return False
#call2y
    def call2y(self):
        if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
            self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super" or
            self.ch() == "static" or self.ch() == "final"  or self.ch() == "abstract" or self.ch() == "func" or self.ch() == "DT"):
            return True
#call3
    def call3(self):
        if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
            self.ch() == "[" or self.ch() == "(" or self.ch() == "." or self.ch() == ";"):
            if (self.ch() == "."): #<RHP1> <f3op>;
                if (self.RHP1()):
                    if (self.f3op()):
                        if (self.ch() == ";"):
                                self.i += 1
                                return True
            elif (self.ch() == "Increment/Decrement"):
                self.i += 1
                if (self.ch() == ";"):
                    self.i += 1
                    return True
            elif(self.ch() == "Compound Assignment"):
                self.i += 1
                if (self.asg()):
                    if (self.ch() == ";"):
                        self.i += 1
                        return True
            elif(self.ch() == "["):
                self.i += 1
                if(self.E()):
                    if(self.ch() == "]"):
                        self.i += 1
                        if(self.call4()):
                            return True
            elif(self.ch() == ","):
                self.i += 1
                if(self.ch() == "ID"):
                    self.i += 1 
                    if(self.array_dec()):
                        return True
            elif (self.ch() == ":="):
                self.i += 1 
                if(self.call3z()):
                    return True
            else:
                if (self.ch() == ";"):
                    self.i += 1 
                    if(self.call2y()):
                        return True
        else:
            return False

#call3z
    def call3z(self):
        if (self.ch() == "["):
            self.i += 1
            if(self.init2d()):
                if (self.ch() == "]"):
                    self.i += 1
                    if (self.arr()):
                        return True
        elif(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
            self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or 
            self.ch() == "ID", self.ch() == "obj"):
            if(self.asg()):
                if (self.ch() == ";"):
                    self.i += 1
                    return True
        else:
            return False
#call 4
    def call4(self):
        if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or 
            self.ch() == "[" or self.ch() == "(" or self.ch() == "." or self.ch() == ";"):
            if (self.ch() == "."): #<RHP1> <f3op>;
                if (self.RHP1()):
                    if (self.f3op()):
                        if (self.ch() == ";"):
                                self.i += 1
                                return True
            elif (self.ch() == "Increment/Decrement"):
                self.i += 1
                if (self.ch() == ";"):
                    self.i += 1
                    return True
            elif(self.ch() == "Compound Assignment"):
                self.i += 1
                if (self.asg()):
                    if (self.ch() == ";"):
                        self.i += 1
                        return True
            elif(self.ch() == ","):
                self.i += 1
                if(self.ch() == "ID"):
                    self.i += 1 
                    if(self.array_dec()):
                        return True
            elif (self.ch() == ":="):
                self.i += 1 
                if(self.call4z()):
                    return True
            else:
                if (self.ch() == ";"):
                    self.i += 1 
                    if(self.call2y()):
                        return True
        else:
            return False

#call 4z
    def call4z(self):
        if (self.ch() == "["):
            self.i += 1
            if(self.init3d):
                if (self.ch() == "]"):
                    self.i += 1
                    if (self.arr()):
                        return True
        elif(self.ch() == "this" or self.ch() == "super" or self.ch() == "boolConstant" or self.ch() == "IntegerConstant" or self.ch() == "FloatConstant" or 
            self.ch() == "StringConst" or self.ch() == "charConstant" or self.ch() == "(" or self.ch() == "!" or 
            self.ch() == "ID", self.ch() == "obj"):
            if(self.asg()):
                if (self.ch() == ";"):
                    self.i += 1
                    return True
        else:
            return False
#First(RHP) = {[, (, . , null, }	Follow(RHP) = { ++, --, := , CompAsgnOP}
    def RHP(self):
        if (self.ch() == "[" or self.ch() == "(" or self.ch() == "."):
            if (self.ch() == "["):  #<array>   <RHP3>       
                if (self.array()):
                    if (self.RHP3()):
                       return True

            elif(self.ch() == "("): #(<argument>) <RHP1>      
                self.i += 1
                if(self.argument()):
                    if(self.ch() == ")"):
                        self.i += 1
                        if(self.RHP1()):
                            return True
            
            else:
                if(self.ch() == "."): #<RHP1>
                    if(self.RHP1()):
                        return True
        else:
            if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement" or self.ch() == ";"):
                return True
        return False

#<RHP3> --> <RHP1> | e
    def RHP3(self):
        if(self.ch() == "."):
            if(self.RHP1()):
                return True
        else:
            if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement"):
                return True
        return False

#<RHP1> --> .ID <RHP> 
    def RHP1(self):
        if(self.ch() == "."):
            self.i += 1
            if(self.ch() == "ID"):
                self.i += 1
                if(self.RHP()):
                    return True
        return False

#<f3op> --> <f3d> | e  ==> { ++, --, := , CompAsgnOP, e }
    def f3op(self):
        if(self.ch() == ":=" or self.ch() == "Compound Assignment" or self.ch() == "Increment/Decrement"):
            if (self.f3d()):
                return True
        else:
            if(self.ch() == ";"):
                return True
        return False


#<SST2> --> <sdouble><fdouble><SST3> ==> First(SST2) = {static, final, abstract, DT}
    def SST2(self):
        if (self.ch() == "static" or self.ch() == "final" or self.ch() == "abstract" or self.ch() == "DT"):
            if(self.sdouble()):
                if(self.fdouble()):
                    if(self.SST3()):
                        return True
        return False

#<SST3> --> <adouble> DT <func_st> | DT <fdec> ==> First (SST3) = {abstract, func, DT}
# abstract DT <func_st> | DT <func_st> | DT <fdec>
# --> abstract DT <func_st> | DT <v_func_type>
    def SST3(self):
        if(self.ch() == "abstract" or self.ch() == "DT"):
            if(self.ch() == "abstract"):
                self.i += 1
                if(self.ch() == "DT"):
                    self.i += 1
                    if(self.func_st()):
                        return True
            else:
                if(self.ch() == "DT"):
                    self.i += 1
                    if(self.v_func_type()):
                        return True
        return False

# <v_func_type> --> <func_st> | <fdec>  ==> func, ID
    def v_func_type (self):
        if (self.ch() == "func"):
            if (self.func_st()):
                return True
        else:
            if (self.ch() == "ID"):
                if (self.fdec()):
                    return True
        return False

#<fdec> --> ID <declaration> ==> First(fdec) = {ID}
    def fdec(self):
        if(self.ch() == "ID"):
            self.i += 1
            if(self.declaration()):
                return True
        return False

# <declaration> --> <Dec> | <array_dec> ==> First (declaration) = { ; , ‘,’, :=, [} 
    def declaration(self):
        if(self.ch() == ":=" or self.ch() == "[" or self.ch() == ";" or self.ch() == ","):
            if(self.ch() == ":=" or self.ch() == "," or self.ch() == ";"):
                if(self.Dec()):
                    return True
            else:
                if(self.ch() == "["):
                    if(self.array_dec()):
                        return True
        return False

#<sdouble> -->  static | e  ==> First(sdouble) = {static, } ==>Follow(sdouble)= {abstract, func, DT}
    def sdouble(self):
        if (self.ch() == "static"):
            self.i += 1
            return True
        else:
            if(self.ch() == "abstract" or self.ch() == "func" or self.ch() == "DT" or self.ch() == "final"):
                return True
        return False

#<fdouble> final |e  ==> First(fdouble) = {final, } ==> {static, abstract, func, DT, class}
    def fdouble(self):
        if (self.ch() == "final"):
            self.i += 1
            return True
        else:
            if(self.ch() == "static" or self.ch() == "class"  or self.ch() == "abstract" or self.ch() == "func" or 
            self.ch() == "DT" or self.ch() == "private" or self.ch() == "public"):
                return True
        return False

#<adouble>  abstract | 	==> First (adouble) = {abstract, } ==> func
    def adouble(self):
        if (self.ch() == "abstract"):
            self.i += 1
            return True
        else:
            if(self.ch() == "DT" or self.ch() == "private" or self.ch() == "public" or self.ch() == "class" or self.ch() == "final"):
                return True
        return False

#<body> --> ; | <SST> |<SST2> | {<MST>} 
# ==> First(body) = { { , ; , while, for, return, if, break, continue, ID, static, final, func, abstract, DT }
    def body(self):
        if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or self.ch() == "this" or self.ch() == "super" or
            self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "{" or self.ch() == ";" or
            self.ch() == "static" or self.ch() == "final"  or self.ch() == "abstract" or self.ch() == "DT"):
            if(self.ch() == ";"):
                self.i += 1
                return True
            elif(self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
                self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super"):
                if(self.SST()):
                    return True
            elif (self.ch() == "static" or self.ch() == "final"  or self.ch() == "abstract" or self.ch() == "DT"):
                if(self.SST2()):
                    return True
            else:
                if(self.ch() == "{"):
                    self.i += 1
                    if(self.MST()):
                        if(self.ch() == "}"):
                            self.i += 1
                            return True
        return False
    
#<MST> --> <SST> <MST>|<SST2><MST> |e ==> Follow(MST) = { } }
#==>First(MST) = { while, for, return, if, break, continue, ID, , static, final, abstract, func, DT}
    def MST(self):
        if (self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
            self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super" or
            self.ch() == "static" or self.ch() == "final"  or self.ch() == "abstract" or self.ch() == "DT"):

            if(self.ch()=="while" or self.ch() == "for" or self.ch() =="return" or self.ch()=="if" or
                self.ch() == "break" or self.ch() == "continue" or self.ch() == "ID" or self.ch() == "this" or self.ch() == "super"):
                if(self.SST()):
                    if(self.MST()):
                        return True
                else:
                    if(self.ch() == "static" or self.ch() == "final"  or self.ch() == "abstract" or self.ch() == "DT"):
                        if(self.SST2()):
                            if(self.MST()):
                                return True
        else:
            if(self.ch() == "}"):
                return True
        return False
                    
