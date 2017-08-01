#Created by Dylan Randall
# / = NOT; . = AND; + = OR; ( = (; )= ); XOR = @

global AND, NOT, OR, BRACKET_OPEN, BRACKET_CLOSED, XOR
BRACKET_OPEN = -2
BRACKET_CLOSED = -1
NOT = 2
AND = 3
OR = 4
XOR = 5
#EXAMPLE INPUT: /A+/B

def errorCheck(string): #basic check for input error
    oBC = 0 #open bracket count
    cBC = 0 #closed bracket count

    for c in string:
        if ord(c) > 47 and ord(c) < 58:
            return [False, "Numbers are not valid identifiers!"]
        if c == "(":
            oBC += 1
        elif c == ")":
            cBC += 1

    if oBC != cBC:
        return [False, "Brackets are missing/invalid!"]
    else:
        return[True,-1]
    
def inputAnalysis(string): #Returns analysis of input
    valid = errorCheck(string) #error checks
    if valid[0] == False:
        print("INPUT| "+valid[1])
        return -1 #return of -1 = function failure
    
    res = []
    priority = 0
    for c in string:
        if c == "(":
            priority += 1
            res.append([BRACKET_OPEN,priority])
        elif c == ")":
            res.append([BRACKET_CLOSED,priority])
            priority -= 1
        elif c == "/":
            res.append([NOT,priority])
        elif c == ".":
            res.append([AND,priority])
        elif c == "+":
            res.append([OR,priority])
        elif c == "@":
            res.append([XOR,priority])
        elif (ord(c) > 64 and ord(c) < 91) or (ord(c) > 96 and ord(c) < 123):
            res.append([c,-1]) #-1 priority = variable

    return res

def printAnalysis(analysis):
    if analysis == -1:
        print ("printAnanlysis| Cannot print invalid algebra analysis!")
        return
    
    print("Analysis output: ")
    
    for r in analysis:
        msg = ""
        logic = r[0]
        priority = r[1]

        if logic == BRACKET_OPEN:
            msg = "( | "+str(priority)
        elif logic == BRACKET_CLOSED:
            msg = "( | "+str(priority)
        elif logic == NOT:
            msg = "NOT | "+str(priority)
        elif logic == AND:
            msg = "AND | "+str(priority)
        elif logic == OR:
            msg = "OR | "+str(priority)
        elif logic == XOR:
            msg = "XOR | "+str(priority)
        else:
            msg = r[0]+" | "+str(priority)

        print(msg)

def getVarValues(analysis): #Gets the variable(s) value(s)
    if analysis == -1:
        print("getVarValues| Cannot compute invalid algebra!")
        return
    
    vrs = [] #variables
    for r in analysis:
        if r[1] == -1:
            add = True
            for v in vrs:
                if v[0] == r[0]:
                    add = False
            if add == True:
                vrs.append([r[0],0])

    for i in range(len(vrs)):
        v = vrs[i]
        val = input("Enter value of "+str(v[0])+": ")
        val = int(val)
        if val != 0 and val != 1:
            print("Defaulted "+str(v[0])+" to 0 as no valid input was given!")
        else:
            vrs[i] = [v[0],int(val)]
    return vrs

def getVarValuesNoInput(analysis): #Gets the variable(s)
    if analysis == -1:
        print("getVarValues| Cannot compute invalid algebra!")
        return
    
    vrs = [] #variables
    for r in analysis:
        if r[1] == -1:
            add = True
            for v in vrs:
                if v[0] == r[0]:
                    add = False
            if add == True:
                vrs.append([r[0],0])
    return vrs

def printVarValues(variables):
    print("Variable | value")
    for v in variables:
        print(v[0]+" | "+str(v[1]))

def getResult(analysis, vals):
    output = -1

    calculated = analysis

    for itm in calculated:
        if itm[1] == -1:
            vl = 0
            for val in vals:
                if itm[0] == val[0]:
                    vl = val[1]
            itm[0] = vl

    equation = []
    for itm in calculated:
        if itm[0] == NOT:
            equation.append([NOT,itm[1]])
        elif itm[0] == AND:
            equation.append([AND,itm[1]])
        elif itm[0] == OR:
            equation.append([OR,itm[1]])
        elif itm[0] == XOR:
            equation.append([XOR,itm[1]])
        elif itm[0] != BRACKET_OPEN and itm[0] != BRACKET_CLOSED:
            equation.append([itm[0],-1])

    run = True
    rv = 0 #resultantValue
    while run == True:
        print(str(equation))
        maxPR = [0,-1] #Max Priority
        objIndex = 0
        index = 0
        for itm in equation:
            if itm[1] > maxPR[1]:
                maxPR = itm
                objIndex = index
            elif itm[1] == maxPR[1] and itm[1] != -1:
                if itm[0] < maxPR[0]:
                    maxPR = itm
                    objIndex = index
            index += 1

        if maxPR[0] == NOT:
            v = equation[objIndex+1]
            if v[0] == maxPR[0]:
                run = False
                print("CALCULATION| Error invalid algebra!")
                return -1
            v = int(v[0])
            if v == 0:
                v = 1
            elif v == 1:
                v = 0
                
            equation.insert(objIndex,[v,-1])
            del equation[objIndex+2]
            del equation[objIndex+1]
        elif maxPR[0] == AND:
            v1 = equation[objIndex-1]
            v2 = equation[objIndex+1]
            if v1[0] == maxPR[0] or v2[0] == maxPR[0]:
                run = False
                print("CALCULATION| Error invalid algebra!")
                return -1
            v1 = v1[0]
            v2 = v2[0]
            v = int(v1)*int(v2)
            
            if v == -2: #This should not occur here but check here just in case
                v = -1
            elif v == 2:
                v = 1

            equation.insert(objIndex,[v,-1])
            del equation[objIndex+2]
            del equation[objIndex+1]
            del equation[objIndex-1]
        elif maxPR[0] == OR:
            v1 = equation[objIndex-1]
            v2 = equation[objIndex+1]
            if v1[0] == maxPR[0] or v2[0] == maxPR[0]:
                run = False
                print("CALCULATION| Error invalid algebra!")
                return -1
            v1 = int(v1[0])
            v2 = int(v2[0])
            v = v1+v2
            
            if v == -2:
                v = -1
            elif v == 2:
                v = 1

            equation.insert(objIndex,[v,-1])
            del equation[objIndex+2]
            del equation[objIndex+1]
            del equation[objIndex-1]
        elif maxPR[0] == XOR:
            v1 = equation[objIndex-1]
            v2 = equation[objIndex+1]
            if v1[0] == maxPR[0] or v2[0] == maxPR[0]:
                run = False
                print("CALCULATION| Error invalid algebra!")
                return -1
            v1 = int(v1[0])
            v2 = int(v2[0])
            v = v1+v2
            
            if v == -2 or v == 2:
                v = 0

            equation.insert(objIndex,[v,-1])
            del equation[objIndex+2]
            del equation[objIndex+1]
            del equation[objIndex-1]

        if len(equation) == 1:
            run = False
    print(str(equation))
    rv = equation[0]
    return rv[0]
        
def driver():
    run = True
    while(run == True):
        inp = input("Enter boolean algebra: ")
        res = inputAnalysis(inp)
        vals = getVarValues(res)
        r = getResult(res,vals)
        print("Result: "+str(r)+"\n")
            
        run = input("Calculate another? [y/n]: ")
        if run == "y" or run == "Y" or run == "Yes" or run == "yes":
            run = True
        else:
            run = False
            print("")

driver()
