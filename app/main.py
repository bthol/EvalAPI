# Dependencies
import math
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import copy

# Environment variables
load_dotenv()

# PROGRAMIC PROCESS

# Phase I: Pre-Structural Validation
# Description: Performs validation on string and each character to prevent structuring of inputs whose invalidity is easily determinable from a string of characters.

# Phase II: Entity Structuring and Analysis
# Description: Analyzes problem string to create problem structure from problem string data storing relevant problem data as it goes. The problem string is structured into entities including and limited to multi-digit numbers, negative numbers, decimal numbers, operations, parenthesis, sets, variables and keywords.

# Phase III: Post-structural Validation
# Description: This is the phase in which rules for problem structure syntax are enforced by running various tests to catch inputs that fail to adhere to the rules of problem construction and produce a relevant error.

# Phase IV: Structural Manipulation
# Description: After determining a valid input, the program analyzes the structure to identify remaining program entities and Sets are structured to allow multiple arguments into a single key functon. From the data stored throughout the process of structuring and validation, the program determines the best course of action for how to begin processing the problem structure into a solution. That may be as simple as calulating arithmetic into a single value solution or as complex as indentifyig the first parenthetical section to handle in an algebraic expression.

# Phase V: Calculation
# Description: However the program determines its course for where to begin, the calculate function will ultimately be called, and that function breaks down into three processes which occur in the following order: 1) Key Functions, 2) Arithmetic Operations, and 3) Algebraic Expression Formatting and Simplification. Key functions permit special functions to be called by a key and argument(s), so long as correct syntax is followed. Arithmetic operations are performed in operator precedence one at a time until none are remaining. If an algebraic expression is indentified, its form will be standardized at the level of a term and the level of an expression before being comprehensively tested for cases of simplification until none are remaining.

# Program Information
info = {
    
    "operations": [
        {"name":"Addition", "syntax":"+"},
        {"name":"Subtraction", "syntax":"-"},
        {"name":"Multiplication", "syntax":"*"},
        {"name":"Division", "syntax":"/"},
        {"name":"Exponentiation", "syntax":"^"},
        {"name":"radication", "syntax":"√"}, # alt code 251
        {"name":"negation", "syntax":"(-x)"},
        {"name":"open_parenthesis", "syntax":"("},
        {"name":"close_parenthesis", "syntax":")"},
        {"name":"open_bracket", "syntax":"["},
        {"name":"close_bracket", "syntax":"]"},
    ],

    "constants": [
        {"name":"π", "syntax":"pi"}, # alt code 227
        {"name":"Euler's Number", "syntax":"euler"},
    ],

    # the whole lowercase alphabet may be used as variables (keys are also composed of lowercase letters)
    "variables": ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w"],

    "key_functions": [
        # Trigonomic Module
        [
                
            # Reciprocal
            {"name":"Arcus Cosecant", "key":"acsc", "syntax": "acsc(x)", "about": "Gets the arcus cosecant, i.e. the inverse reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Cosecant", "key":"csc", "syntax": "csc(x)", "about": "Gets the cosecant, i.e. the reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Secant", "key":"asec", "syntax": "asec(x)", "about": "Gets the arcus secant, i.e. the inverse reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Secant", "key":"sec", "syntax": "sec(x)", "about": "Gets the secant, i.e. the reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Cotangent", "key":"acot", "syntax": "acot(x)", "about": "Gets the arcus cotangent, i.e. the inverse reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Cotangent", "key":"cot", "syntax": "cot(x)", "about": "Gets the cotangent, i.e. the reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},

            # Hyperbolic
            {"name":"Arcus Hyperbolic Sine", "key":"asinh", "syntax": "asinh(x)", "about": "Gets the arcus hyperbolic sine, i.e the inverse sine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Hyperbolic Sine", "key":"sinh", "syntax": "sinh(x)", "about": "Gets the hyperbolic sine, i.e the sine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Hyperbolic Cosine", "key":"acosh", "syntax": "acosh(x)", "about": "Gets the arcus hyperbolic cosine, i.e the inverse cosine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Hyperbolic Cosine", "key":"cosh", "syntax": "cosh(x)", "about": "Gets the hyperbolic cosine, i.e the cosine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Hyperbolic Tangent", "key":"atanh", "syntax": "atanh(x)", "about": "Gets the arcus hyperbolic tangent, i.e the inverse tangent of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Hyperbolic Tangent", "key":"tanh", "syntax": "tanh(x)", "about": "Gets the hyperbolic tangent, i.e the tangent of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            # Fundamental
            {"name":"Arcus Sine", "key":"asin", "syntax": "asin(x)", "about": "Gets the arcus sine, i.e. the inverse sine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Sine", "key": "sin", "syntax": "sin(x)", "about": "Gets the sine of x, where x is a value or an expression that evaluates to a value."},

            {"name":"Arcus Cosine", "key": "acos", "syntax": "acos(x)", "about": "Gets the arc cosine, i.e. the inverse of cosine, of x, where x is a value or an expression that evaluates to a value."},

            {"name":"Cosine", "key": "cos", "syntax": "cos(x)", "about": "Gets the cosine of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Tangent", "key": "atan", "syntax": "atan(x)", "about": "Gets the arcus tangent, i.e. the inverse tangent, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Tangent", "key":"tan", "syntax": "tan(x)", "about": "Gets the tangent of x, where x is a value or an expression that evaluates to a value."},
        ],

        # Geometeric Module
        [
            # Triangles
            {"name":"Right Triangle Hypotenuse", "key":"hypot", "syntax": "hypot[a,b]", "about": "Gets the hypotenuse length of a right triangle given leg lengths a and b, where a and b are a value or an expression that evaluates to a value wrapped within square brackets, e.g. hypot[a,[b+x]]."},
            
            {"name":"Heron's Formula", "key":"heron", "syntax": "heron[a,b,c]", "about": "Gets the area of a scalene triangle given side lengths a, b, and c, where a, b, and c are a value or an expression that evaluates to a value wrapped within square brackets, e.g. heron[a,b,[c+x]]."},
        ],

        # Combinatoric Module
        [
            {"name":"Factorial", "key":"fact", "syntax": "fact(x)", "about": "Gets the factorial of x, where x is a value or an expression that evaluates to a value."},

            {"name":"Permutation", "key":"perm", "syntax": "perm[n,r]", "about": "Gets a permutation given n number of objects with r number of objects per permutation, where n and r are values or an expression that evaulates to a value wrapped within square brackets, e.g. perm[n,[r+x]]."},

            {"name":"Combination", "key":"comb", "syntax": "comb[n,r]", "about": "Gets a combination given n number of objects with r number of objects per combination, where n and r are values or an expression that evaulates to a value wrapped within square brackets, e.g. comb[n,[r+x]]."},
            
        # add
        #  - composition
        #  - partition

        ],

        # Statistical Module
        [
            {"name":"Standard Deviation", "key":"sd", "syntax": "sd[a,b]", "about": "Gets the standard deviation of the set of items within square brackets, where that set has at least two comma-demarcated items. An item may be a value or an expression that evaulates to a value wrapped within square brackets, e.g. var[a,[b+x]]."},
            
            {"name":"Variance", "key":"var", "syntax": "var[a,b]", "about": "Gets the variance of the set of items within square brackets, where that set has at least two comma-demarcated items. An item may be a value or an expression that evaulates to a value wrapped within square brackets, e.g. sd[a,[b+x]]."},
                
            # Means
            {"name":"Harmonic Mean", "key":"meanh", "syntax": "meanh[a,b]", "about": "Gets the geometeric mean of the the set of items within square brackets, where that set has at least two comma-demarcated items, and each item is a value or an expression that evaulates to a value wrapped within square brackets, e.g. meang[10,[2+3]]."},

            {"name":"Geometeric Mean", "key":"meang", "syntax": "meang[a,b]", "about": "Gets the harmonic mean of the the set of items within square brackets, where that set has at least two comma-demarcated items, and each item is a value or an expression that evaulates to a value wrapped within square brackets, e.g. meanh[10,[2+3]]."},

            {"name":"Weighted Mean", "key":"meanw", "syntax": "meanw[[a,w1],[b,w2]]", "about": "Gets the weighted mean of the the set of items within square brackets, where that set has at least two comma-demarcated items, and each item is a value and a weight for that value wrapped in square brackets, e.g. meanw[[10,60],[20,40]]."},

            {"name":"Mean", "key":"mean", "syntax": "mean[a,b]", "about": "Gets the mean of the the set of values within square brackets, where that set has at least two comma demarcated items, and each item is a value or an expression that evaluates to a value, e.g. mean[a,[b+x]]."},

            {"name":"Root Mean Square", "key":"rms", "syntax": "rms[a,b]", "about": "Gets the geometeric mean of the the set of items within square brackets, where that set has at least two comma-demarcated items, and each item is a value or an expression that evaulates to a value wrapped within square brackets, e.g. rms[10,[2+3]]."},
                
            # Et Cetera
            {"name":"Greatest Common Factor", "key":"gcf", "syntax": "gcf[a,b]", "about": "Gets the greatest common factor of a and b within square brackets, where a and b are values or expressions that evaluate to values wrapped in square brackets, e.g. gcf[a,[b+x]]."},

            {"name":"Least Common Multiple", "key":"lcm", "syntax": "lcm[a,b]", "about": "Gets the least common multiple of values a and b within square brackets, where a and b are values or expressions that evaluate to values wrapped in square brackets, e.g. lcm[a,[b+x]]."},
            
            {"name":"Logarithm", "key":"log", "syntax": "log[x,b]", "about": "Gets the logarithm of x with base b, where x and b are values or expressions wrapped in square brackets that evaluate to a value, e.g. log[x,[b+2]]."},

            {"name":"Natural Log", "key":"ln", "syntax": "ln(x)", "about": "Gets the natural log of x with base e, where x is a value or an expression that evaluates to a value, e.g. ln(2-1*0)."},
        ],

        # Algebraic
        # note: algebraic module must be at end index of key_functions
        [
            {"name":"Algebraic Exponentiation", "key":"algexp", "syntax":"algexp[[a],x]", "about":"Gets an algebraic exponentiation given a polynomial expression a and power x, where x is a value or an arithmetic expression that evaluates to a positive integer value wrapped within square brackets, e.g. expand[[x+1],[1+1]] = (x+1)*(x+1)"},
            
            {"name":"Polynomial Expansion", "key":"expand", "syntax":"expand[[x][y]]", "about":"Gets a polynomial expansion given a list of at least 2 polynomial expressions x and y, where each expression may have a unique number of any number of terms, e.g. expand[[a][b+c][d+e+f]]"},
        
        # add:
        #  - complete Polynomial Expansion by finishing required cases of simplification
        #  - Polynomial Factorization
        #  - complex conjugate
        ],
    ],
}

def evaluator(input):

    # PROGRAM PARAMETERS
    global info

    # the paren_limit parameter controls the maximum number of levels of parenthesis nesting in any one evaluation
    paren_limit = 10

    # the const_limit parameter controls the maximum number of instances of any one constant allowed in any one evaluation
    const_limit = 1000

    # the key_limit parameter controls the maximum number of the same key function allowed in any one evaluation
    key_limit = 1000

    # the simp_limit parameter constrols the maximum number of simplifications in any one evaluation
    simp_limit = 1000

    # PROGRAM ENTITY REFERENCE

    # operator characters
    operation = {
        "addition": info["operations"][0]["syntax"],
        "subtraction": info["operations"][1]["syntax"],
        "multiplication": info["operations"][2]["syntax"],
        "division": info["operations"][3]["syntax"],
        "exponentiation": info["operations"][4]["syntax"],
        "radication": info["operations"][5]["syntax"],
        "negation": info["operations"][6]["syntax"],
        "open_parenthesis": info["operations"][7]["syntax"],
        "close_parenthesis": info["operations"][8]["syntax"],
        "open_bracket": info["operations"][9]["syntax"],
        "close_bracket": info["operations"][10]["syntax"]
    }

    # key placeholder for subtraction of algebraic terms
    subtract_key = "sub"

    # Operator Precedence is from highest to least in this structure
    operator_precedence = [[operation["subtraction"], operation["addition"]], [operation["division"], operation["multiplication"]], [operation["radication"], operation["exponentiation"]]]
    
    # variable characters
    variables = ""
    for v in info["variables"]:
        variables = variables + v

    # represents a string containing all of the valid non-numeral characters
    valid_chars = " " + "." + "," + variables + operation["addition"] + operation["subtraction"] + operation["multiplication"] + operation["division"] + operation["exponentiation"] + operation["radication"] + operation["open_parenthesis"] + operation["close_parenthesis"] + operation["open_bracket"] + operation["close_bracket"]
    
    # global_bypass is an emergeny brake which prevents the continuation of the program
    # If True, bypasses the whole program 
    global_bypass = False
    
    # is_var indicates if variables in problem structure
    # and controls whether the program solves for an algebraic expression, True, or a single value, False
    is_var = False

    # is_paren indicates whether there are parenthesis, True, or not, False
    # If False, bypasses section function
    is_paren = False

    # is_brack indicates whether there are square brackets, True, or not, False
    # If False, bypasses key_functions function
    is_brack = False

    # is_exp indicates whether there are exponentiations, True, or not, False
    # If False, bypasses exponentiation
    is_exp = False

    # is_root indicates whether there are roots, True, or not, False
    # If False, bypasses roots
    is_root = False

    # is_mult indicates whether there are multiplications, True, or not, False
    # If False, bypasses multiplication
    is_mult = False

    # is_div indicates whether there are divisions, True, or not, False
    # If False, bypasses division
    is_div = False

    # is_add indicates whether there are additions, True, or not, False
    # If False, bypasses additions
    is_add = False

    # is_sub indicates whether there are subtractions, True, or not, False
    # If False, bypasses subtractions
    is_sub = False

    # is_key stores strings for each kind of keyword in problem string
    # If is_key is empty, bypasses key_functions function
    is_key = []

    # key_modules structure represent which key functions modules should be run or be bypassed on call
    key_modules = [
        {"module":"trigonomic", "use":False},
        {"module":"geometric", "use":False},
        {"module":"combinatoric", "use":False},
        {"module":"statistical", "use":False},
        {"module":"algebraic", "use":False},
    ]

    # use_logs indicates whether to use logs, True, or not, False
    # if use_logs is "1", then logging is active, otherwise it remains defaultly inactive
    use_logs = ""

    # process_log is an object literal that stores string values for all process checkpoints during evalution
    process_log = {"0":"no logging"}

    # note: log_process is run on every restructure, run for calculation reference, and run for process labels
    def log_process(log = ""):
        if use_logs == "1":
            new_key = int(list(process_log.keys())[-1]) + 1
            if isinstance(log, list) == True:
                process_log["%s" % new_key] = copy.deepcopy(log)
            else:
                process_log["%s" % new_key] = log
    
    # STRUCTURE START

    def num_cast(str):
        # a single data type converter for all your data type conversion needs!
        try:
            num = float(str)
            if (num % 1 == 0):
                num = int(num)
            return num
        except:
            return False
    
    def restructure(solution, start, end, arr):
        # A single restructure function for all your restructuring needs!
        structure = []
        if start != 0:
            structure = structure + arr[0:start]
        if solution != None:
            if isinstance(solution, list):
                if solution[0] == "[":
                    # remove square brackets from set
                    del(solution[0])
                    del(solution[len(solution) - 1])
                    # remove commas from set
                    sol = []
                    for i in solution:
                        if i != ",":
                            sol.append(i)
                    # append set
                    structure.append(sol)
                else:
                    # concatenate lists
                    structure = structure + solution
            elif solution != "delete":
                structure.append(solution)
        if end != len(arr) - 1:
            structure = structure + arr[end + 1:len(arr)]
        # log new structure
        log_process(structure)
        return structure

    def get_word(word, arr):
        # finds a given keyword within the structure
        wordLen = len(word)
        ref = None
        for i in range(0, len(arr)):
            if (i > len(arr) - wordLen):
                # stop search if remaining indexes of arr is less than length of word
                break
            # test for first and last letter of word
            if arr[i] == word[0] and arr[i + wordLen - 1] == word[wordLen - 1]:
                # get string between first and last letter index
                str = ""
                for l in range(0, wordLen):
                    str = str + arr[i + l]
                # compare string with word
                if str == word:
                    ref = {"first": i, "last": i + wordLen}
                    break
        return ref

    def word_struct(word, arr, module = None):
        # structures a given keyword
        nonlocal is_key
        arrVar = arr
        ref = get_word(word, arrVar)
        s = True
        if module == None:
            while ref is not None:
                # for every word found in arr
                if s == True:
                    # for first word found
                    # add key to is_key structure
                    is_key = [word] + is_key
                    s = False
                # restructure with keyword
                arrVar = restructure(word, ref["first"], ref["last"] - 1, arrVar)
                # find next word or None
                ref = get_word(word, arrVar)
        else:
            # for key function modules
            while ref is not None:
                # for every word found in arr
                if s == True:
                    # for first word found
                    # add key to is_key structure
                    is_key = [word] + is_key
                    # activate key module
                    key_modules[module]["use"] = True
                    s = False
                # restructure with keyword
                arrVar = restructure(word, ref["first"], ref["last"] - 1, arrVar)
                # find next word or None
                ref = get_word(word, arrVar)

        return arrVar
    
    def op_test(str):
        # tests if given str is an operation character
        for i in range(0, len(info["operations"])):
            if info["operations"][i]["syntax"] == str:
                return True
        return False

    def var_test(str):
        # test for variables
        for i in variables:
            if i == str:
                return True
        return False

    def key_test(str):
        # tests if str is key
        for i in range(0, len(info["key_functions"])):
            for j in range(0, len(info["key_functions"][i])):
                if info["key_functions"][i][j]["key"] == str:
                    return True
        return False

    def identify_entities(arr):
        # identify program entities and update program entity reference
        nonlocal operation
        
        # Identify algebraic mode
        nonlocal is_var
        for i in arr:
            if var_test(i):
                is_var = True
                break
        
        # Identify parenthesis
        nonlocal is_paren
        if is_paren == False:
            for i in arr:
                if i == operation["open_parenthesis"] or i == operation["close_parenthesis"]:
                    is_paren = True
                    break
        
        # Identify square brackets
        nonlocal is_brack
        if is_brack == False:
            for i in arr:
                if i == operation["open_bracket"] or i == operation["close_bracket"]:
                    is_brack = True
                    break
        
        # Identify exponentiation
        nonlocal is_exp
        if is_exp == False:
            for i in arr:
                if i == operation["exponentiation"]:
                    is_exp = True
                    break

        # Identify roots
        nonlocal is_root
        if is_root == False:
            for i in arr:
                if i == operation["radication"]:
                    is_root = True
                    break
        
        # Identify multiplication
        nonlocal is_mult
        if is_mult == False:
            for i in arr:
                if i == operation["multiplication"]:
                    is_mult = True
                    break
        
        # Identify division
        nonlocal is_div
        if is_div == False:
            for i in arr:
                if i == operation["division"]:
                    is_div = True
                    break
        
        # Identify addition
        nonlocal is_add
        if is_add == False:
            for i in arr:
                if i == operation["addition"]:
                    is_add = True
                    break
        
        # Identify subtraction
        nonlocal is_sub
        if is_sub == False:
            for i in arr:
                if i == operation["subtraction"]:
                    is_sub = True
                    break
        
        return True
        
    # STRUCTURE END

    # ARITHMETIC OPERATIONS START

    def precedence(op1, op2):
        # returns true if op1 has higher operator precedence than op2
        # larger op value indicates larger operator precedence
        nonlocal operator_precedence
        if op_test(op1) and op_test(op2):
            op1_precedence = 0
            op2_precedence = 0
            for o in range(len(operator_precedence)):
                for i in range(len(operator_precedence[o])):
                    if op1 == operator_precedence[o][i]:
                        op1_precedence = o
                    if op2 == operator_precedence[o][i]:
                        op2_precedence = o
            
            if op1_precedence >= op2_precedence:
                return True
            else:
                return False
        else:
            return None

    def operate(i, arr):
        # returns True if operation at index i in structure arr is operating in operator precedence
        arrVar = arr
        # larger op value indicates larger operator precedence
        op1 = arrVar[i] # operation on current index
        op2 = "" # operation before index
        op3 = "" # operation after index

        if i - 2 > -1 and op_test(arrVar[i - 2]):
            op2 = arr[i  -2]
        if i + 2 < len(arrVar) and op_test(arrVar[i + 2]):
            op3 = arr[i + 2]

        if op2 != "" and op3 != "":
            # test both op2 and op3
            x = precedence(op1, op2)
            y = precedence(op1, op3)
            if x == True and y == True:
                # op1 has higher precedence than op2 and op3
                return True
            else:
                # op1 has lower precedence than either op2 or op3
                return None
        
        elif op2 != "" and op3 == "":
            # only test op2
            x = precedence(op1, op2)
            if x == True:
                # op1 has higher precedence than op2
                return True
            else:
                # op1 has lower precedence than op2
                return None

        elif op2 == "" and op3 != "":
            # only test op3
            y = precedence(op1, op3)
            if y == True:
                # op1 has higher precedence than op3
                return True
            else:
                # op1 has lower precedence than op3
                return None
        
        else: # op2 == "" and op3 == ""
            return True

    def exponentiate(base, exponent):
        base = float(base)
        if base % 1 == 0:
            base = int(base)

        exponent = float(exponent)
        if exponent % 1 == 0:
            exponent = int(exponent)

        power = math.pow(base, exponent)

        return power

    def root(radicand, degree):
        radicand = float(radicand)
        if radicand % 1 == 0:
            radicand = int(radicand)

        degree = float(degree)
        if degree % 1 == 0:
            degree = int(degree)

        root = math.pow(radicand, 1/degree)

        return root

    def multiply(multiplicand, multiplier):
        multiplicand = float(multiplicand)
        if multiplicand % 1 == 0:
            multiplicand = int(multiplicand)

        multiplier = float(multiplier)
        if multiplier % 1 == 0:
            multiplier = int(multiplier)

        product = multiplicand * multiplier

        return product

    def divide(dividend, divisor):
        nonlocal global_bypass
        dividend = float(dividend)
        if dividend % 1 == 0:
            dividend = int(dividend)

        divisor = float(divisor)
        if divisor % 1 == 0:
            divisor = int(divisor)

        if divisor != 0:
            quotient = dividend / divisor
            if quotient % 1 == 0:
                quotient = int(quotient)
            return quotient
        else:
            global_bypass = True
            return "no division by zero"

    def add(augend, addend):
        augend = float(augend)
        if augend % 1 == 0:
            augend = int(augend)

        addend = float(addend)
        if addend % 1 == 0:
            addend = int(addend)

        total = augend + addend

        return total

    def subtract(minuend, subtrahend):
        minuend = float(minuend)
        if minuend % 1 == 0:
            minuend = int(minuend)

        subtrahend = float(subtrahend)
        if subtrahend % 1 == 0:
            subtrahend = int(subtrahend)

        difference = minuend - subtrahend

        return difference

    def monus(a, b):
        # monus; truncated minus; doz (difference or zero)
        a = float(a)
        if a % 1 == 0:
            a = int(a)
        b = float(b)
        if b % 1 == 0:
            b = int(b)
        
        if a >= b:
            return a - b
        else:
            return 0

    def factorial(x):
        if int(x) == x:
            if x == 1:
                return 1
            elif x > 1:
                # accumulate factorial in y
                y = 1
                for i in range(int(x), 1, -1):
                    y = y * i
                
                # return answer
                return y
            
            elif x < 0:
                # accumulate factorial in y
                y = 1
                x = abs(x)
                for i in range(int(x), 1, -1):
                    y = y * i
                
                # test odd number of negative multiplications
                if x % 2 != 0:
                    y = -y

                # return answer
                return y
            
        else:
            # x is not an integer
            nonlocal global_bypass
            global_bypass = True

            # return error
            return 0

    def get_mean(arr):
        # returns the mean of a list of values
        return sum(arr) / len(arr)

    # ARITHMETIC OPERATIONS END

    # ALGEBRAIC OPERATIONS START
    def negate_alg_exp(exp):
        # negates an algebraic expression
        for i in range(len(exp)):
            if exp[i] == operation["addition"]:
                exp.pop(i)
                exp.insert(i, operation["subtraction"])
            elif exp[i] == operation["subtraction"]:
                exp.pop(i)
                exp.insert(i, operation["addition"])
        return exp

    def negate_alg_terms(terms):
        # negates terms in an algebraic expression
        nonlocal subtract_key
        for i in range(len(terms)):
            if terms[i][0] == subtract_key:
                terms[i].pop(0)
            else:
                terms[i].insert(0, subtract_key)
        return terms

    def get_terms(arr):
        nonlocal subtract_key
        terms = []
        buffer = []
        for i in range(len(arr)):
            if arr[i] == operation["addition"]:
                # end of term
                terms.append(buffer)
                buffer = []
            elif arr[i] == operation["subtraction"]:
                # prevent end of term on negation
                if arr[i - 1] != operation["open_parenthesis"]:
                    # non-negative value
                    # end of term
                    terms.append(buffer)
                    buffer = []
                    buffer = [subtract_key]
            else:
                # compile term
                buffer.append(arr[i])
        
        # add last term
        terms.append(buffer)
        
        return terms

    def like_terms(t1, t2):
        # returns True if given terms are like
        # terms are like if:
        #  - same variables
        #  - same exponent for each variable
        t1_len = len(t1)
        t2_len = len(t2)
        t1_dat = []
        t2_dat = []

        # get data for term 1
        for x in range(t1_len):
            if var_test(t1[x]):
                if x + 2 < t1_len and t1[x + 1] == operation["exponentiation"]:
                    # assumes no power expression
                    t1_dat.append({"var": t1[x], "pow": t1[x + 2]})
                else:
                    # no power
                    t1_dat.append({"var": t1[x], "pow": 1})
        
        # get data for term 2
        for x in range(t2_len):
            if var_test(t2[x]):
                if x + 2 < t2_len and t2[x + 1] == operation["exponentiation"]:
                    # assumes no power expression
                    t2_dat.append({"var": t2[x], "pow": t2[x + 2]})
                else:
                    # no power
                    t2_dat.append({"var": t2[x], "pow": 1})
        
        # make comparison using term data
        t1_dat_len = len(t1_dat)
        t2_dat_len = len(t2_dat)
        if t1_dat_len == t2_dat_len:
            # compare term data
            for x in range(t1_dat_len):
                if t1_dat[x]["var"] != t2_dat[x]["var"] or t1_dat[x]["pow"] != t2_dat[x]["pow"]:
                    return False
        else:
            # dissimilar length of main term and term 2
            return False

        # no conditions met for falsification
        return True

    def combine_terms(t1, t2):
        # returns terms combined by addition or subtraction
        # note: for use on terms returning true from like_terms(t1, t2)
        nonlocal subtract_key
        coef_sum = 0
        term = []
        t1_len = len(t1)
        t2_len = len(t2)

        # add coefficient of first term
        if t1_len > 0:

            if t1[0] == subtract_key:
                if len(t1) > 1 and not var_test(t1[1]):
                    coef_sum -= t1[1]
                    term = t1[3:]
                else:
                    coef_sum -= 1
                    term = t1[1:]
                    
            elif not var_test(t1[0]):
                coef_sum += t1[0]
                term = t1[2:]
            else:
                coef_sum += 1
                term = t1
            
        # add coefficient of second term
        if t2_len > 0:

            if t2[0] == subtract_key:
                if len(t2) > 1 and not var_test(t2[1]):
                    coef_sum -= t2[1]
                    if t1_len == 0:
                        term = t2[3:]
                else:
                    coef_sum -= 1
                    if t1_len == 0:
                        term = t2[1:]
                    
            elif not var_test(t2[0]):
                coef_sum += t2[0]
                if t1_len == 0:
                    term = t2[2:]
            else:
                coef_sum += 1
                if t1_len == 0:
                    term = t2

        if t1_len == 0 and t2_len == 0:
            return []

        # test coefficient for special cases
        if coef_sum == 0:
            return [0]
        elif coef_sum == 1:
            return term
        else:
            return [coef_sum, operation["multiplication"]] + term
    
    def product_term(t1, t2):
        # returns the product of t1 and t2
        # note: terms do not have to be like terms to create product term
        nonlocal subtract_key
        t1_len = len(t1)
        t2_len = len(t2)
        # handle empty terms
        if t1_len == 0:
            if t2_len == 0:
                # both terms are empty
                return []
            else:
                # t1 is empty
                return t2
        elif t2_len == 0:
            # t2 is empty
            return t1

        if t1_len > 0 and t2_len > 0:
            # neither terms are empty

            # test for zero product
            if t1[0] == 0 or t2[0] == 0:
                return [0]
            if t1[0] == subtract_key and t1_len > 1 and t1[1] == 0:
                return [0]
            if t2[0] == subtract_key and t2_len > 1 and t2[1] == 0:
                return [0]

            # test for square term product
            if t1_len == t2_len:
                identical = True
                for i in range(t1_len):
                    if t1[i] != t2[i]:
                        identical = False
                        break
                if identical == True:
                    # square term
                    if t1_len == 1:
                        return t1 + [operation["exponentiation"], 2]
                    else:
                        return [operation["open_parenthesis"]] + t1 + [operation["close_parenthesis"], operation["exponentiation"], 2]
            
            # create product term
            return t1 + [operation["multiplication"]] + t2

    def testTermEnds(c1, c2, arr):
        # tests ends of term to ensure that the entire term is identified by condition
        arr_len = len(arr)

        # test both ends
        if c1 - 1 > -1 and c2 + 1 < arr_len:
            if arr[c1 - 1] == operation["addition"] or arr[c1 - 1] == operation["subtraction"]:
                if arr[c2 + 1] == operation["addition"] or arr[c2 + 1] == operation["subtraction"]:
                    return True
        
        # test front end
        elif c1 - 1 > -1:
            if arr[c1 - 1] == operation["addition"] or arr[c1 + 1] == operation["subtraction"]:
                return True
        
        # test back end
        elif c2 + 1 < arr_len:
            if arr[c2 + 1] == operation["addition"] or arr[c2 + 1] == operation["subtraction"]:
                return True
        
        # no ends to test
        elif c1 == 0 and c2 + 1 == arr_len:
            return True
        
        # no true condition reached (e.g. index out of range)
        return False

    def standardize_form(arr):
        # identifies terms in algebraic expression,
        # standardizes term forms, combines like terms,
        # standardizes expression form, returns result
        log_process("Standardizing Format of Algebraic Terms and Expressions")
        log_process(arr)

        # return empty argument
        if len(arr) == 0:
            log_process("Standardization Aborted")
            return arr

        # prevent standardization on parenthetical or bracketed algebraic expressions
        for i in arr:
            if i == operation["open_parenthesis"] or i == operation["close_parenthesis"] or i == operation["open_bracket"] or i == operation["close_bracket"]:
                log_process("Standardization Aborted")
                return arr

        # term standards
        #  - single coefficient at starting index 2*x^2*3*y => 6*x^2*y
        #  - variables in alphabetical order within divisional sections of term b^2*3*a^3/b*a => 3*a^3*b^2/a*b
        #  - 

        # expression standards
        #  - Decremental order of term degree  x^2 + 2*x^3 - 6*x => 2*x^3 + x^2 - 6*x
        #  - arithmetic terms are combined into single constant at end of expression
        #  - like algebraic terms are combined
        #  - non-leading terms subtract instead of add negative coefficient
        
        nonlocal subtract_key
        sect_struct = [] # stores terms as sublists
        term = [] # buffer for sect_struct term appending
        expression = [] # stores terms as sublists in original order but with term standards
        formatted = [] # stores terms concatenated into single list with term and expression standards
        
        for i in range(0, len(arr)):
            if arr[i] == operation["addition"]:
                # end of term
                sect_struct.append(term)
                term = []
            elif arr[i] == operation["subtraction"]:
                # prevent end of term on negation
                if arr[i - 1] != operation["open_parenthesis"]:
                    # non-negative value
                    # end of term
                    sect_struct.append(term)
                    term = [subtract_key]
            else:
                # compile term
                term.append(arr[i])
        
        # append last term
        sect_struct.append(term)

        # print(sect_struct)

        # --- TERM STANDARDS ---
        log_process("Imposition of Term Standards")

        # iterate over each term
        for t in sect_struct:
            # print(t)
            log_process("Term Identified")

            # decalre variables
            is_subtracted = False
            if t[0] == subtract_key:
                # flip key switch
                is_subtracted = True
                # remove subtract key
                t.pop(0)
            length = len(t)
            tdata = []
            var_count = 0
            coef_count = 0
            divisions = [] # stores the numbers for variables after which there is division
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            
            # collect term data
            for j in range(0, length):

                if var_test(t[j]): # is a variable
                    # get alphabetic index of variable for later alphabetization
                    alpha = None
                    for a in range(0, 26):
                        if t[j] == alphabet[a]:
                            alpha = a
                            break
                    var_count += 1
                    tdata.append({"coef": False, "value": t[j], "term_index": j, "alpha_index": alpha})

                else:
                    try: # is a coefficient
                        val = int(t[j])
                        if j + 2 < length and t[j + 1] == operation["multiplication"] and var_test(t[j + 2]):
                            # case: a * x
                            if j - 1 > -1:
                                if t[j - 1] != operation["exponentiation"] and t[j - 1] != operation["radication"]:
                                    # prevent appending non-coefficients
                                    tdata.append({"coef": True, "value": val, "term_index": j, "alpha_index": None})
                                    coef_count += 1
                                else:
                                    # non-coefficient value
                                    tdata.append({"coef": False, "value": val, "term_index": j, "alpha_index": None})
                            else:
                                tdata.append({"coef": True, "value": val, "term_index": j, "alpha_index": None})
                                coef_count += 1

                        elif j - 2 > -1 and t[j - 1] == operation["multiplication"] and var_test(t[j - 2]):
                            # case: x * a
                            if j + 1 < length:
                                if t[j + 1] != operation["exponentiation"] and t[j + 1] != operation["radication"]:
                                    # prevent appending non-coefficients
                                    tdata.append({"coef": True, "value": val, "term_index": j, "alpha_index": None}) 
                                    coef_count += 1
                                else:
                                    # non-coefficient value
                                    tdata.append({"coef": False, "value": val, "term_index": j, "alpha_index": None})
                            else:
                                tdata.append({"coef": True, "value": val, "term_index": j, "alpha_index": None})
                                coef_count += 1
                        else:
                            # non-coefficient value
                            tdata.append({"coef": False, "value": val, "term_index": j, "alpha_index": None})

                    except: # is an operation
                        tdata.append({"coef": False, "value": t[j], "term_index": j, "alpha_index": None})
                        
                        # append variable number before a division
                        if t[j] == operation["division"]:
                            divisions.append({"var_count": var_count, "term_index": j})
            
            # print(tdata)
            # print(divisions)

            # analyze term data
            if var_count > 0:
                log_process("New Divisional Section")
                last = 0 # farthest alphabetic index
                start = 0 # next starting index for alphabetization after division
                end = length # next ending index for alphabetization before division
                divisions_i = 0
                d_length = len(divisions)
                if d_length > 0:
                    end = divisions[divisions_i]["term_index"]

                # store product of coeffients from each section in term
                log_process(" - Coefficient Product Calculated")
                coefficiency = []
                if coef_count > 0:
                    for i in range(0, d_length + 1):
                        # get product of coefficients in divisional section
                        product = 1
                        for j in range(start, end):
                            c = tdata[j]["coef"]
                            x = tdata[j]["value"]
                            if c == True:
                                try:
                                    x = float(x)
                                    product *= x
                                except:
                                    continue
                        
                        # append product to coefficiency
                        try:
                            if product % 1 == 0:
                                product = int(product)
                        except:
                            continue

                        coefficiency.append(product)

                        # move to next divisional section
                        start = end
                        divisions_i += 1
                        if divisions_i < d_length:
                            end = divisions[divisions_i]["term_index"]
                        else:
                            end = length

                # print(coefficiency)
                
                # reinitialize section variables
                divisions_i = 0
                start = 0
                end = length
                if d_length > 0:
                    end = divisions[divisions_i]["term_index"]
                
                # declare alphabetical structure before skipping divisional sections to add placeholders
                alphabetical = []

                # skip divisional sections without variables
                loop_count = 0
                while loop_count < d_length and divisions[divisions_i]["var_count"] == 0:
                    loop_count += 1

                    # append placeholder for divisional section
                    alphabetical.append({"term_index": None})

                    # move to next divisional section
                    start = end
                    divisions_i += 1
                    if divisions_i < d_length:
                        end = divisions[divisions_i]["term_index"]
                    else:
                        end = length

                # sectionally alphabetize variables from term, sectioning by division
                log_process(" - Variable Alphabetization")
                for i in range(0, var_count):

                    # calculate differences ommitting below previous minimum
                    diffs = []
                    for j in range(start, end):
                        d = tdata[j]["alpha_index"]
                        ti = tdata[j]["term_index"]
                        if d != None and d >= last:
                            use = True
                            # test alphabetical for duplicates
                            for a in alphabetical:
                                if ti == a["term_index"]:
                                    use = False
                                    break
                            
                            if use == True:
                                diffs.append({"diff": d - last, "term_index": ti})

                    # print(diffs)

                    # determine smallest difference
                    if len(diffs) > 0:
                        # for divisional sections with variables
                        small = diffs[0]["diff"]
                        for d in diffs:
                            diff = d["diff"]
                            if diff < small:
                                small = diff

                        # use smallest difference to append data in order to section list
                        for d in diffs:
                            if d["diff"] == small:
                                # found matching difference
                                alphabetical.append(tdata[d["term_index"]])
                                last = tdata[d["term_index"]]["alpha_index"]
                                if divisions_i < d_length and i == divisions[divisions_i]["var_count"] - 1 or i == var_count - 1:
                                    # on end of divisional section
                                    last = 0
                                    start = end
                                    divisions_i += 1
                                    if divisions_i < d_length:
                                        end = divisions[divisions_i]["term_index"]
                                    else:
                                        end = length
                                
                                break
                
                # print(alphabetical)

                # append sub-lists of divisional sections from section list to alphabetical list
                divisions_i = 0 # reset to zero
                div_sect = []
                sectional = []
                div_placeholder_count = 0 # stores the number of divisional sections with a placeholder
                for i in range(0, len(alphabetical)):
                    div_sect.append(alphabetical[i])
                    if alphabetical[i]["term_index"] == None:
                        # end of divisional section with placeholder
                        sectional.append(div_sect)
                        div_sect = []
                        divisions_i += 1
                        # count placeholder for divisional section
                        div_placeholder_count += 1
                    elif divisions_i < d_length and i - div_placeholder_count == divisions[divisions_i]["var_count"] - 1:
                        # end of divisional section
                        sectional.append(div_sect)
                        div_sect = []
                        divisions_i += 1
                sectional.append(div_sect)

                # collect non-coefficient values by divisional section
                add_placeholder = True
                noncoef_vals = []
                div_sect = [] # repurpose as buffer for noncoef_vals
                divisions_i = 0 # reset to zero
                end = length
                if d_length > 0:
                    end = divisions[divisions_i]["term_index"]
                
                for i in range(0, length):
                    if i < end:
                        if tdata[i]["coef"] == False and tdata[i]["alpha_index"] == None and not op_test(tdata[i]["value"]):
                            if i - 1 <= -1 or tdata[i - 1]["value"] != operation["exponentiation"] and tdata[i - 1]["value"] != operation["radication"]:
                                # start and middle
                                add_placeholder = False
                                div_sect.append(tdata[i])

                    elif i == length - 1 and len(noncoef_vals) == d_length:
                        if tdata[i]["coef"] == False and tdata[i]["alpha_index"] == None and not op_test(tdata[i]["value"]):
                            # special end case
                            div_sect.append(tdata[i])
                            noncoef_vals.append(div_sect)

                    else:
                        # check at end that at least one value was added in last divisional section
                        if add_placeholder == True:
                            # add placeholder
                            div_sect.append({"term_index": None})
                        else:
                            # setup placeholder for next divisional section
                            add_placeholder = True

                        noncoef_vals.append(div_sect)
                        div_sect = []

                        divisions_i += 1
                        if divisions_i < d_length:
                            end = divisions[divisions_i]["term_index"]
                        else:
                            end = length - 1

                # print(sectional)
                # print(coefficiency)
                # print(noncoef_vals)

                # use sectional and coeffiency data to create expression term structure
                term = []
                coefficiency_len = len(coefficiency)
                sectional_len = len(sectional)
                noncoef_vals_len = len(noncoef_vals)
                for i in range(0, d_length + 1):
                    # iterate over each divisional section
                    # coefficient goes at start of divisional section in term
                    # coefficients are broken down by divisional section to avoid rounding errors frpom division
                    # ommit coefficients of 1
                    if i < coefficiency_len and coefficiency[i] != 1:
                        term.append(coefficiency[i])

                    if i < sectional_len:
                        for obj in sectional[i]:
                            t_i = obj["term_index"]
                            start = t_i
                            end = t_i
                            if t_i != None: # exclude placeholders
                                # test for bounds of variable
                                if t_i + 2 < len(t) and t[t_i + 1] == operation["exponentiation"]:
                                    end += 2
                                if t_i - 1 > -1 and t[t_i - 1] == operation["radication"]:
                                    if t_i - 2 > -1 and not op_test(t[t_i - 2]):
                                        # n-th root, where n != 2
                                        start -= 2
                                    else:
                                        # square root
                                        start -= 1
                            
                                # add data to term
                                if start == end:
                                    # single variable
                                    if len(term) == 0:
                                        # variable at start
                                        term.append(t[t_i])
                                    else:
                                        # intermittent variable
                                        if term[len(term) - 1] != operation["division"]:
                                            # variable in middle of divisional section
                                            term.append(operation["multiplication"])
                                            term.append(t[t_i])
                                        else:
                                            # variable at start of second or later divisional section
                                            term.append(t[t_i])
                                else:
                                    # variable expression
                                    if len(term) > 0:
                                        # intermittent expression
                                        term.append(operation["multiplication"])
                                    exp = t[start:end + 1]
                                    for obj in exp:
                                        term.append(obj)
                                
                    if i < noncoef_vals_len and noncoef_vals[i][0]["term_index"] != None:
                        term.append(noncoef_vals[i][0]["value"])
                    
                    # add divison symbol after each divisional section
                    term.append(operation["division"])

                # remove extra division symbol at end
                if term[len(term) - 1] == operation["division"]:
                    term.pop()

                # if switch is flipped
                if is_subtracted == True:
                    # re-add subtract key
                    term = [subtract_key] + term
                
                # add standardized term to expression structure
                expression.append(term)
                
            else:
                # arithmetic expressions require no formatting

                # if switch is flipped
                if is_subtracted == True:
                    # re-add subtract key
                    t = [subtract_key] + t
                
                # add arithmetic term to expression structure
                expression.append(t)
                
        # --- EXPRESSION STANDARDS ---
        if len(expression) == 1:
            # not an expression of terms; single term
            # return formatted term
            log_process("Standardization Complete")
            log_process(expression[0])
            return expression[0]
        else:
            log_process("Imposition of Expression Standards")
            # print(expression)

            # combine all arithemtic terms into single constant term at end of expression
            log_process(" - Combination of Arithmetic Terms into Constant")
            constant = []
            indexes_removal = []
            expression_len = len(expression)
            for t in range(0, expression_len):
                is_var = False
                e = expression[t]
                for i in range(0, len(e)):
                    ee = e[i]
                    if var_test(ee):
                        # is algebraic term
                        is_var = True
                        break
                    elif isinstance(ee, str) and ee[0] == operation["open_parenthesis"] and len(ee) == 4 and ee[1] == operation["subtraction"] and var_test(ee[2]) and ee[3] == operation["close_parenthesis"]:
                        # handle negative variables
                        is_var = True
                        break

                if is_var == False:
                    # arithmetic term
                    indexes_removal.append(t)
                    # combine arithmetic terms
                    if expression[t][0] == subtract_key:
                        # remove subtract key
                        expression[t].pop(0)
                        # subtract or negate
                        constant_len = len(constant)
                        if constant_len == 0:
                            # negate first value in constant
                            x = num_cast(operation["subtraction"] + str(expression[t][0]))
                            if x:
                                constant = [x]
                                
                        elif constant_len > 0:
                            # replace last addition with subtraction
                            constant.pop()
                            constant += [operation["subtraction"]]
                            constant += expression[t]
                        
                        # add arithmetic terms together
                        constant += [operation["addition"]]
                    else:
                        constant += expression[t]
                        constant += [operation["addition"]]
            
            # if there are arithmetic terms
            if len(constant) > 0:
                # remove last operation symbol
                constant.pop()
            
                # remove arithmetic terms from expression
                indexes_removal = sorted(indexes_removal, reverse=True)
                for i in indexes_removal:
                    expression.pop(i)

                # calculate constant from arithmetic terms
                c = calculate(constant)

                # format constant for handling subtraction
                if int(c) >= 0:
                    constant = [c]
                else:
                    constant = [subtract_key, -c]
                
                # put constant on end of term
                expression.append(constant)

            # print(expression)

            # order expression in decremental order of term degree
            log_process(" - Polynomials in Decremental Order of Term Degree")
            degrees = []
            for i in range(0, len(expression)):
                # append largest exponent in each term to represent term degree
                degree = 0
                trm = expression[i]
                trm_len = len(trm)
                for j in range(0, trm_len):
                    if j + 1 < trm_len and trm[j] == operation["exponentiation"]:
                        # for each exponent in term
                        x = num_cast(trm[j + 1])
                        if x and x > degree:
                            # update as largest
                            degree = x
                # append degree of term (zero for linear terms)
                degrees.append(degree)
            
            # print(degrees)
            
            # store indexes of terms in expression in order from greatest to least degree
            degrees_sorted = sorted(degrees, reverse=True)
            degree_indexes = [] # stores indexes
            degree_order = [] # stores terms ordered by degree
            for d in degrees_sorted:
                for i in range(0, len(degrees)):
                    if d == degrees[i]:
                        if len(degree_indexes + [i]) == len(set(degree_indexes + [i])):
                            # index is unique
                            degree_indexes.append(i)
                            break
            
            # print(degree_indexes)

            # use indexes to create expression structure ordered by degree
            for i in degree_indexes:
                degree_order.append(expression[i])

            log_process(" - Combination of Like Algebraic Terms")
            # print(degree_order)
            
            # combine like terms:
            #  - same degree in both terms
            #  - same variables in both terms
            #  - same exponenets for each variable in both terms

            indexes = list(range(len(degree_order)))

            main_index = 0
            while len(indexes) > 1:

                # print("ran")
                # print(len(indexes))

                # get a main term to make comparisons
                main_term = degree_order[main_index]

                # remove index of main term from reference
                for i in range(len(indexes)):
                    if main_index == indexes[i]:
                        indexes.pop(i)
                        break
                
                like_indexes = []
                for i in range(main_index + 1, len(degree_order)):
                    compare_term = degree_order[i]
                    if like_terms(main_term, compare_term) == True:
                        like_indexes.append(i)

                # print(like_indexes)

                # remove i in like_indexes from reference
                like = []
                for i in like_indexes:
                    # collect like terms
                    like.append(degree_order[i])
                
                # combine like terms
                if len(like) > 0:

                    # use term and like to combine
                    main = []

                    # combine all terms like main 
                    for t in like:
                        main = combine_terms(main, t)

                    # combine with main term
                    main = combine_terms(main, main_term)
                    
                    # restructure degree_order with combined term stored in main
                    if main_index < len(degree_order) - 1:
                        if main_index == 0:
                            # only after
                            degree_order = [main] + degree_order[main_index + 1:]
                        else:
                            # both before and after
                            degree_order = degree_order[:main_index] + [main] + degree_order[main_index + 1:]
                    else:
                        if main_index == 0:
                            # neither before nor after
                            degree_order = [main]
                        else:
                            # only after
                            degree_order = degree_order[:main_index] + [main]

                    # print(degree_order)
                    
                    # remove terms that are alike
                    like_indexes_len = len(like_indexes)
                    if like_indexes_len > 1:
                        for i in range(len(like_indexes) - 1, -1, -1):
                            degree_order.pop(like_indexes[i])
                    elif like_indexes_len == 1:
                        degree_order.pop(like_indexes[0])
                    
                    # remove indexes of like terms from indexes
                    for i in like_indexes:
                        for idx in range(len(indexes)):
                            if i == indexes[idx]:
                                indexes.pop(idx)
                                break

                    # print(degree_order)

                # update modified main term to prevent re-runs
                main_index += 1

            # print(degree_order)

            # remove terms with 0 coefficient
            zero_coef_indexes = []
            for i in range(len(degree_order)):
                first = degree_order[i][0]
                if first == subtract_key:
                    first = degree_order[i][1]
                if not var_test(first):
                    x = num_cast(first)
                    if not isinstance(x, bool) and x == 0:
                        zero_coef_indexes.append(i)
        
            # print(zero_coef_indexes)

            for i in range(len(zero_coef_indexes) - 1, -1, -1):
                degree_order.pop(zero_coef_indexes[i])

            # print(degree_order)

            # concatenate terms into formatted expression
            degree_order_len = len(degree_order)

            # leading term
            if degree_order[0][0] == subtract_key:
                # remove subtract key
                degree_order[0].pop(0)
                # negate term of first divisional section
                a = degree_order[0][0]
                x = num_cast(a)
                if not isinstance(x, bool):
                    # negate coefficient
                    x = -x
                    degree_order[0][0] = x

                elif var_test(a) == True:
                    # negate variable
                    degree_order[0][0] = operation["negation"]
            
            # extend with leading term 
            formatted.extend(degree_order[0])
            
            # append addition symbol 
            formatted.append(operation["addition"])

            # rest of the iterations
            if degree_order_len > 1:
                for i in range(1, degree_order_len):
                    # store coefficient
                    coef = num_cast(degree_order[i][0])
                    # subtract key
                    if degree_order[i][0] == subtract_key:
                        # remove subtract key
                        degree_order[i].pop(0)
                        # remove previous addition
                        formatted.pop()
                        # replace it with subtraction
                        formatted.append(operation["subtraction"])
                    
                    # negative coefficient => subtraction with positive coefficient
                    elif not isinstance(coef, bool) and coef < 0:
                        # handle coefficient
                        if coef == -1:
                            # remove coefficient
                            degree_order[i].pop(0)
                            # remove multiplication symbol
                            degree_order[i].pop(0)
                        else:
                            degree_order[i].pop(0)
                            degree_order[i].insert(0, -coef)
                        
                        # update operation

                        # remove previous addition
                        formatted.pop()
                        # replace it with subtraction
                        formatted.append(operation["subtraction"])

                    
                    # extend with next term 
                    formatted.extend(degree_order[i])
                    
                    # append addition symbol 
                    formatted.append(operation["addition"])

            # remove extra addition symbol at end
            formatted.pop()

            # return formatted algebraic expression
            log_process("Standardization Complete")
            log_process(formatted)
            return formatted
    
    def simplify(arr):
        nonlocal global_bypass
        nonlocal simp_limit

        # simplifies algebraic expressions
        destandardized = False
        
        arrVar = standardize_form(arr)
        
        # log process label
        log_process("Simplification of Algebraic Expression")
        # print(arrVar)

        # define process of simplification
        # 1.) Format expression and terms into standard forms
        # 2.) identify first variable in arr testing from left to right
        # 3.) test for simplifications until one is discovered and run that
        # 4.) repeat step 1 - 2 until no simplifications are discovered during step 2
        # 5.) return result
        
        simplifying = True
        x = 0
        while x < simp_limit and simplifying == True:
            # each while loop interation is one simplification
            x += 1
            
            # get length of arrVar
            length = len(arrVar)

            for c in range(0, length):
                
                # each character
                if var_test(arrVar[c]):
                    # each variable
                    var = arrVar[c]

                    # run simplifications

                    # Operation on current variable
                    if c + 2 < length:

                        # MULTIPLICATION
                        if arrVar[c + 1] == operation["multiplication"]:

                            # SIMP1: multiplication of variables with coefficients

                            # case: a * x * b * x => (a*b) * x ^ 2, where a and b are particular values
                            if c - 2 > -1 and c + 4 < length and testTermEnds(c - 2, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    # switch post-standardization to on
                                    destandardized = True

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(coefficient1, coefficient2), operation["multiplication"], var, operation["exponentiation"], "2"], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break

                            # case: x * a * x => a * x ^ 2, where a is a particular value
                            elif c + 4 < length and testTermEnds(c, c + 4, arrVar):
                                if arrVar[c + 4] == var and not var_test(arrVar[c + 2]):
                                    # switch post-standardization to on
                                    destandardized = True

                                    # get term data
                                    coefficient = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % coefficient, operation["multiplication"], var, operation["exponentiation"], "2"], c, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break

                            # SIMP2: multiply a variable by itself
                            if arrVar[c + 2] == var and operate(c + 1, arrVar) == True:

                                # switch post-standardization to on
                                destandardized = True
                            
                                # any number multiplied by itself is that number to the power of the number of times it is multiplied by itself
                                multiplying = True
                                power = 2
                                place = c + 2

                                # get power and place data
                                while multiplying == True and place + 2 < length:
                                    if arrVar[place + 1] == operation["multiplication"] and arrVar[place + 2] == var:
                                        # consecutive multiplications of variable
                                        power += 1
                                        place = place + 2
                                    else:
                                        # discontinuation of consecutive multiplication
                                        multiplying = False
                                        # stop while loop
                                        break
                                
                                # apply simplification to problem structure
                                arrVar = restructure([var, operation["exponentiation"],'%s' % power], c, place, arrVar)
                                
                                # end current simplification
                                break
                            
                            if c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP3: a * x * b => (a*b) * x

                                if arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(val1, val2), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break

                            # SIMP4: a / x * b => (a*b) / x

                                if arrVar[c - 1] == operation["division"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                        # DIVISION
                        elif arrVar[c + 1] == operation["division"]:

                            # SIMP5: division of variables with coefficients

                            # case: a * x / b * x => a / b, where a and b are particular values
                            if c - 2 > -1 and c + 4 < length and testTermEnds(c - 2, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    quotient = divide(coefficient1, coefficient2)
                                    if global_bypass == False:
                                        arrVar = restructure(['%s' % quotient], c - 2, c + 4, arrVar)
                                    else:
                                        # division by zero
                                        return quotient
                                    
                                    # end current simplification
                                    break
                            
                            # SIMP6: divide a variable by itself
                            if arrVar[c + 2] == var and operate(c + 1, arrVar) == True:

                                # test if next operation after dividing by itself is another division by itself
                                if c + 4 < length and arrVar[c + 3] == operation["division"] and arrVar[c + 4] == var:
                                    # prevent running operation if one of the variables has an operation with higher operator precedence

                                    # any number divided by itself is that number divided by that number to the power of the number of times it is divided by itself
                                    dividing = True
                                    power = 1
                                    place = c + 2

                                    # get power and place data
                                    while dividing == True and place + 2 < length:
                                        if arrVar[place + 1] == operation["division"] and arrVar[place + 2] == var:
                                            # consecutive divisions of variable
                                            power += 1
                                            place = place + 2
                                        else:
                                            # discontinuation of consecutive division
                                            dividing = False
                                            # stop while loop
                                            break
                                    
                                    # any number divided by itself is 1
                                    arrVar = restructure([var, operation["division"], operation["open_parenthesis"], var, operation["exponentiation"], '%s' % power, operation["close_parenthesis"]], c, place, arrVar)
                                    # end current simplification
                                    break

                                elif c - 2 > -1:
                                    # test if operation before cancels out the value 1
                                    if arrVar[c - 1] == operation["multiplication"]:
                                        # any number multiplied by 1 is itself
                                        arrVar = restructure("delete", c - 1, c + 2, arrVar)
                                        # end current simplification
                                        break

                                    elif arrVar[c - 1] == operation["division"]:
                                        
                                        # any number divided by 1 is itself
                                        arrVar = restructure("delete", c - 1, c + 2, arrVar)
                                        # end current simplification
                                        break
                                        
                                else:
                                    # apply simplification to problem structure
                                    arrVar = restructure("1", c, c + 2, arrVar)
                                    # end current simplification
                                    break

                            if c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP7: a * x / b => (a/b) * x

                                if arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    quotient = divide(val1, val2)
                                    if global_bypass == False:
                                        arrVar = restructure(['%s' % quotient, operation["multiplication"], var], c - 2, c + 2, arrVar)
                                    else:
                                        # division by zero
                                        return quotient

                                    # end current simplification
                                    break

                            # SIMP8: a / x / b => (a/b) / x

                                if arrVar[c - 1] == operation["division"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % divide(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)
                                    
                                    # end current simplification
                                    break
                            
                        # ADDITION
                        elif arrVar[c + 1] == operation["addition"]:

                            # SIMP9: add coefficients between terms with no exponents
                            
                            # case: a * x + b * x => (a+b) * x
                            if c - 2 > -1 and c + 4 < length and testTermEnds(c - 2, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break

                            # case: a * x + x => (a + 1) * x, where a is a particular value
                            elif c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):
                                if arrVar[c + 2] == var and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]):
                                    
                                    # get term data
                                    coefficient = arrVar[c - 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([str(int(coefficient) + 1), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # case: x + a * x => (a + 1) * x, where a is a particular value
                            elif c + 4 < length and testTermEnds(c, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c + 2]):

                                    # get term data
                                    coefficient = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([str(int(coefficient) + 1), operation["multiplication"], var], c, c + 4, arrVar)

                                    # end current simplification
                                    break
                                
                            # SIMP10: add a variable to itself
                            
                            if arrVar[c + 2] == var and operate(c + 1, arrVar) == True:
                                
                                # any number added to itself is that number multiplied by the number of times it is added to itself
                                adding = True
                                multiplier = 2
                                place = c + 2

                                # get multiplier and place data
                                while adding == True and place + 2 < length:
                                    if arrVar[place + 1] == operation["addition"] and arrVar[place + 2] == var:
                                        # consecutive additions of variable
                                        multiplier += 1
                                        place = place + 2
                                    else:
                                        # discontinuation of consecutive addition
                                        adding = False
                                        # stop while loop
                                        break
                                
                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % multiplier, operation["multiplication"], var], c, place, arrVar)
                                # end current simplification
                                break
                            
                            if c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):
                            
                            # SIMP11: a + x + b => (a+b) + x

                                if arrVar[c - 1] == operation["addition"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(val1, val2), operation["addition"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP12: a - x + b => (a+b) - x

                                if arrVar[c - 1] == operation["subtraction"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(val1, val2), operation["subtraction"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                        # SUBTRACTION
                        elif arrVar[c + 1] == operation["subtraction"]:

                            # SIMP13: subtract coefficients between terms with no exponents

                            # case: a * x - b * x => (a-b) * x
                            if c - 2 > -1 and c + 4 < length and testTermEnds(c - 2, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % subtract(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break

                            # case: a * x - x => (a - 1) * x, where a is a particular value
                            elif c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):
                                if arrVar[c + 2] == var and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]):
                                    
                                    # get term data
                                    coefficient = arrVar[c - 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([str(int(coefficient) - 1), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # case: x - a * x => (1 - a) * x, where a is a particular value
                            elif c + 4 < length and testTermEnds(c, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c + 2]):

                                    # get term data
                                    coefficient = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([str(1 - int(coefficient)), operation["multiplication"], var], c, c + 4, arrVar)

                                    # end current simplification
                                    break

                            # SIMP14: subtracted from itself

                            if arrVar[c + 2] == var and operate(c + 1, arrVar) == True:
                            
                                # any number subtracted from itself is that number subtracted by the number of times it is subtracted from itself multiplied by itself
                                subtracting = True
                                multiplier = 1
                                place = c + 2

                                # get multiplier and place data
                                while subtracting == True and place + 2 < length:
                                    if arrVar[place + 1] == operation["subtraction"] and arrVar[place + 2] == var:
                                        # consecutive subtractions of variable
                                        multiplier += 1
                                        place = place + 2
                                    else:
                                        # discontinuation of consecutive subtraction
                                        subtracting = False
                                        # stop while loop
                                        break
                                
                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % (1 - multiplier), operation["multiplication"], var], c, place, arrVar)
                                # end current simplification
                                break
                            
                            if c - 2 > -1 and testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP15: a + x - b => x+(a-b)

                                if arrVar[c - 1] == operation["addition"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([var, operation["addition"], '%s' % subtract(val1, val2)], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP16: a - x - b => (-x)+(a-b)

                                if arrVar[c - 1] == operation["subtraction"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                        
                                        # get term data
                                        val1 = arrVar[c - 2]
                                        val2 = arrVar[c + 2]
                                        var = operation["negation"]

                                        # apply simplification to problem structure
                                        arrVar = restructure([var, operation["addition"], '%s' % subtract(val1, val2)], c - 2, c + 2, arrVar)

                                        # end current simplification
                                        break
                            
                # test terminating condition
                if c + 1 == length:
                    # no further simplifications; on end character and no simplifications run
                    simplifying = False

        # log end of simplification
        log_process("Simplification Complete")

        # standardize simplified expression
        if destandardized == True:
            log_process("Standards Broken by Simplification")
            arrVar = standardize_form(arrVar)

        # return simplified expression
        return arrVar

    # ALGEBRAIC OPERATIONS END

    # KEY FUNCTIONS START

    def getIdx(str, arr):
        # gets index of string in structure
        nonlocal global_bypass
        nonlocal operator_precedence

        if global_bypass == False:

            # get length of arr
            length = len(arr)

            # test if string contains an operation
            if op_test(str):

                # operation string
                val = None
                for i in range(0, length):
                    if arr[i] == str:
                        # test for index range of test
                        if i - 1 > -1 and i + 1 < length:
                            a = arr[i - 1]
                            b = arr[i + 1]
                            # test for operation on parenthesis and square brackets
                            if a != operation["open_parenthesis"] and a != operation["close_parenthesis"] and a != operation["open_bracket"] and a != operation["close_bracket"] and b != operation["open_parenthesis"] and b != operation["close_parenthesis"] and b != operation["open_bracket"] and b != operation["close_bracket"]:
                                # test for operation on variables
                                if not var_test(arr[i - 1]) and not var_test(arr[i + 1]):
                                    # test for operation on exponent with algebraic base
                                    if i - 2 <= -1 or arr[i - 2] != operation["exponentiation"]:
                                        # operator precedence on variables
                                        if i - 3 > -1 and var_test(arr[i - 3]) or i + 3 < length and var_test(arr[i + 3]):
                                            if operate(i, arr) == True:
                                                val = i
                                                return val
                                                
                                        else:
                                            # arithmetic operation approved
                                            val = i
                                            return val

                # no operation from string not on variable
                return val
                            
            else:

                # not operation string
                val = None
                for i in range(0, length):
                    if arr[i] == str:
                        val = i
                        break
                return val
        else:
            # globally bypassed
            return None

    def trigonomic(arr):
        # key function module for trigonomic functions
        arrVar = arr
        nonlocal global_bypass

        if key_modules[0]["use"] == True and global_bypass == False:
            log_process("Trigonomic Key Module")

            # fundamental functions

            # perform all sine functions
            ref = getIdx("sin", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.sin(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sin", arrVar)

            # perform all arcus sine functions
            ref = getIdx("asin", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                x = num_cast(arrVar[ref + 1])

                if x >= -1 and x <= 1:
                    y = np.arcsin(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("asin", arrVar)
                else:
                    # invalid arguments
                    global_bypass = True
                    return "invalid argument = x, x < -1 or x > 1"
                
            # perform all cosine functions
            ref = getIdx("cos", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.cos(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("cos", arrVar)
            
            # perform all arcus cosine functions
            ref = getIdx("acos", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                x = num_cast(arrVar[ref + 1])
                if x >= -1 and x <= 1:
                    y = np.arccos(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("acos", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return "invalid argument = x, x < -1 or x > 1"

            # perform all tangent functions
            ref = getIdx("tan", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                
                if x % np.pi != 0 and x <= - 1 or x % np.pi != 0 and x >= 1:
                    y = np.tan(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("tan", arrVar)
                else:
                    # invalid arguments
                    global_bypass = True
                    return "invalid argument = x, -1 < x < 1 or x mod π = 0"
                
            # perform all arcus tangent functions
            ref = getIdx("atan", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.arctan(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("atan", arrVar)

            # reciprocal functions
            
            # perform all cosecant functions
            ref = getIdx("csc", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x != 0:
                    y = 1 / np.sin(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("csc", arrVar)
                else:
                    # x = 0
                    global_bypass = True
                    return 'no zero argument'
                
            # perform all arc cosecant functions
            ref = getIdx("acsc", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x <= -1 or x >= 1:
                    y = np.arcsin(1/x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("acsc", arrVar)
                else:
                    # -1 < x < 1
                    global_bypass = True
                    return "invalid argument = x, -1 < x < 1"

            # perform all secant functions
            ref = getIdx("sec", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x > 0 and x < np.pi:
                    y = 1 / np.cos(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("sec", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return "invalid argument = x, x <= 0 or x >= π"
                
            # perform all arc secant functions
            ref = getIdx("asec", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x <= -1 or x >= 1:
                    y = np.arccos(1/x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("asec", arrVar)
                else:
                    # -1 < x < 1
                    global_bypass = True
                    return 'invalid argument = x, -1 < x < 1'

            # perform all cotangent functions
            ref = getIdx("cot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x != 0 and x % np.pi != 0:
                    y = 1 / np.tan(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("cot", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return "invalid argument = x, x = 0 or x mod π = 0"
            
            # perform all cotangent functions
            ref = getIdx("acot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x != 0:
                    y = np.arctan(1/x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("acot", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return 'no zero argument'

            # hyperbolic functions

            # perform all hyperbolic sine functions
            ref = getIdx("sinh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sinh", arrVar)
            
            # perform all arcus hyperbolic sine functions
            ref = getIdx("asinh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.asinh(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("asinh", arrVar)
            
            # perform all hyperbolic cosine functions
            ref = getIdx("cosh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("cosh", arrVar)
            
            # perform all arcus hyperbolic cosine functions
            ref = getIdx("acosh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x >= 1:
                    y = np.asinh(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("acosh", arrVar)
                else:
                    # invalid arguments
                    global_bypass = True
                    return "invalid argument = x, x < 1"
        
            # perform all hyperbolic tangent functions
            ref = getIdx("tanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("tanh", arrVar)
        
            # perform all arcus hyperbolic tangent functions
            ref = getIdx("atanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                if x <= -1 or x >= 1:
                    y = np.asinh(x)

                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("atanh", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return "invalid argument = x, -1 < x < 1"

        return arrVar

    def geometric(arr):
        # key function module for geometric functions
        arrVar = arr
        nonlocal global_bypass

        if key_modules[1]["use"] == True and global_bypass == False:
            log_process("Geometric Key Module")

            # perform all right triangle hypotenuse functions
            ref = getIdx("hypot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                leg1 = set_2[0]
                leg2 = set_2[1]
                
                if leg1 > 0 and leg2 > 0:
                    y = np.hypot(leg1, leg2)
                    
                    # apply answer and search for new problem
                    arrVar = restructure(y, ref, ref + 1, arrVar)
                    ref = getIdx("hypot", arrVar)
                else:
                    # invalid argument
                    global_bypass = True
                    return "invalid argument = x, x <= 0"

            # perform all Heron's Formula functions
            ref = getIdx("heron", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)
                
                # perform calculation using numeral set
                # side lengths
                a = set_2[0]
                b = set_2[1]
                c = set_2[2]
                
                if a > 0 and b > 0 and c > 0:
                    # semiperimeter
                    s = (a + b + c) / 2
                    
                    # area calculation
                    area = (s * (s - a) * (s - b) * (s - c))**0.5

                    # apply answer and search for new problem
                    arrVar = restructure(area, ref, ref + 1, arrVar)
                    ref = getIdx("heron", arrVar)
                else:
                    # invalid arguments
                    global_bypass = True
                    return "invalid argument = x, x <= 0"

        return arrVar

    def combinatoric(arr):
        # key function module for combinatoric functions
        arrVar = arr
        nonlocal global_bypass

        if key_modules[2]["use"] == True and global_bypass == False:
            log_process("Combinatoric Key Module")

            # perform all Factorial functions
            ref = getIdx("fact", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])
                y = factorial(x)

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("fact", arrVar)

            # perform all Permutation functions
            ref = getIdx("perm", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                n = set_2[0] # number of objects
                r = set_2[1] # number of objects per permutation
                if n == r:
                    perm  = 1
                    # apply answer and search for new problem
                    arrVar = restructure(perm, ref, ref + 1, arrVar)
                    ref = getIdx("perm", arrVar)

                elif n > 0 and r > 0 and n > r:
                    perm = factorial(n) / factorial(n - r)
                    
                    # apply answer and search for new problem
                    arrVar = restructure(perm, ref, ref + 1, arrVar)
                    ref = getIdx("perm", arrVar)

                else:
                    # n cannot be less than r
                    global_bypass = True
                    return "invalid arguments: n <= 0 or r <= 0 or n < r"

            # perform all Combination functions
            ref = getIdx("comb", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # log keyword
                log_process(arrVar[ref])

                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                n = set_2[0]
                r = set_2[1]

                if n > 0 and r > 0 and n > r:
                    comb = factorial(n) / (factorial(r) * factorial(n - r))
                    # apply answer and search for new problem
                    arrVar = restructure(comb, ref, ref + 1, arrVar)
                    ref = getIdx("comb", arrVar)
                else:
                    # n cannot be greater than r
                    global_bypass = True
                    return "invalid arguments: n <= 0 or r <= 0 or n <= r"

        return arrVar

    def statistical(arr):
        # key function module for statistical functions
        arrVar = arr
        nonlocal global_bypass

        if key_modules[3]["use"] == True and global_bypass == False:
            log_process("Statistical Key Module")
            
            # perform all Standard Deviation functions
            ref = getIdx("sd", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)
                    
                # print(set_2)

                # perform calculation using numeral set
                mean = get_mean(set_2)
                set_3 = []
                for i in set_2:
                    set_3.append(math.pow(i - mean, 2))
                sd = math.pow(sum(set_3)/len(set_3), 1/2)

                # apply answer and search for new problem
                arrVar = restructure(sd, ref, ref + 1, arrVar)
                ref = getIdx("sd", arrVar)
                
            # perform all Variance functions
            ref = getIdx("var", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                mean = get_mean(set_2)
                set_3 = []
                for i in set_2:
                    set_3.append(math.pow(i - mean, 2))
                sd = sum(set_3)/len(set_3)

                # apply answer and search for new problem
                arrVar = restructure(sd, ref, ref + 1, arrVar)
                ref = getIdx("var", arrVar)

            # perform all Harmonic Mean functions
            ref = getIdx("meanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        if x != 0:
                            set_2.append(1/x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "no zero argument"
                    else:
                        x = num_cast(section(i))
                        if x != False and x != 0:
                            set_2.append(1/x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "no zero argument"

                # perform calculation using numeral set
                mean = len(set_2) / sum(set_2)

                # apply answer and search for new problem
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meanh", arrVar)
                
            # perform all Geometeric Mean functions
            ref = getIdx("meang", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                set_2 = 1
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        set_2 = set_2 * x
                    else:
                        x = num_cast(section(i))
                        set_2 = set_2 * x

                # perform calculation using numeral set
                mean = math.pow(set_2, 1/len(set_1))

                # apply answer and search for new problem
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meang", arrVar)

            # perform all Weighted Mean functions
            ref = getIdx("meanw", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # get weights and total of weights
                n = 0
                weights = []
                for i in set_1:
                    weight = float(i[1])
                    weights.append(weight)
                    n = n + weight
                
                # get weighted numeral set
                set_2 = []
                iter = 0
                for i in set_1:
                    val = float(i[0])
                    set_2.append(weights[iter] * val)
                    iter = iter + 1

                # perform calculation using numeral set
                mean = sum(set_2) / n

                # apply answer and search for new problem
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meanw", arrVar)

            # perform all Mean functions
            ref = getIdx("mean", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                mean = get_mean(set_2)

                # apply answer and search for new problem
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("mean", arrVar)
            
            # perform all Root Mean Square functions
            ref = getIdx("rms", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = num_cast(section(i))
                        set_2.append(x)

                # perform calculation using numeral set
                square = []
                for i in set_2:
                    square.append(math.pow(i, 2))
                mean = get_mean(square)
                root = math.pow(mean, 1/2)

                # apply answer and search for new problem
                arrVar = restructure(root, ref, ref + 1, arrVar)
                ref = getIdx("rms", arrVar)
            
            # perform all Greatest Common Factor functions
            ref = getIdx("gcf", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"
                    else:
                        x = num_cast(section(i))
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"

                # perform calculation using numeral set
                gcf = 0
                val1 = set_2[0]
                val2 = set_2[1]
                if val1 != val2:
                    facts_1 = []
                    facts_2 = []

                    def factor(x):
                        factors = []
                        for i in range(x, 0, -1):
                            if x / i % 1 == 0:
                                factors.append(i)
                        return factors
                    
                    # account for limiting factor
                    if val1 > val2:
                        # filter extra factors
                        facts = factor(val1)
                        for i in facts:
                            if i < val2:
                                facts_1.append(i)
                        facts_2 = factor(val2)
                    else:
                        # filter extra factors
                        facts = factor(val2)
                        for i in facts:
                            if i < val1:
                                facts_2.append(i)
                        facts_1 = factor(val1)

                    log_process(facts_1)
                    log_process(facts_2)

                    # search for common factors
                    for i in facts_1:
                        for j in facts_2:
                            if i == j:
                                gcf = j
                                break
                        if gcf != 0:
                            break
                else:
                    gcf = set_2[0]
                
                # apply answer and search for new problem
                arrVar = restructure(gcf, ref, ref + 1, arrVar)
                ref = getIdx("gcf", arrVar)
            
            # perform all Least Common Multiple functions
            ref = getIdx("lcm", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"
                    else:
                        x = num_cast(section(i))
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"

                # perform calculation using numeral set
                lcm = 0
                mult_1 = [set_2[0]]
                mult_2 = [set_2[1]]
                same = False
                x = 0
                while x < 100 and same != True:
                    x = x + 1

                    # search for common multiples
                    for i in mult_1:
                        for j in mult_2:
                            if i == j:
                                same = True
                                lcm = i
                                break
                        if same == True:
                            break

                    # if no multiples were found, add next multiple to each list, and test again
                    if same != True:
                        mult_1.append(mult_1[0] * x)
                        mult_2.append(mult_2[0] * x)

                # apply answer and search for new problem
                arrVar = restructure(lcm, ref, ref + 1, arrVar)
                ref = getIdx("lcm", arrVar)
            
            # perform all Logarithm functions
            ref = getIdx("log", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])
                
                # get string string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"
                    else:
                        x = num_cast(section(i))
                        if x > 0:
                            set_2.append(x)
                        else:
                            # invalid argument
                            global_bypass = True
                            return "invalid argument = x, x <= 0"
                
                x = set_2[0]
                b = set_2[1]

                if x > 0:
                    y = np.emath.logn(b, x)
                else:
                    # complex result
                    global_bypass = True
                    y = 0

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("log", arrVar)
            
            # perform all Natural Logarithm functions
            ref = getIdx("ln", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                x = num_cast(arrVar[ref + 1])

                if x > 0:
                    y = np.log(x)
                else:
                    # complex result
                    global_bypass = True
                    return "invalid argument = x, x <= 0"

                # apply answer and search for new problem
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("ln", arrVar)
                
        return arrVar

    def algebraic(arr):
        # key function module for algebraic functions
        # algebraic operations translate to algebraic expressions
        # rather than solving for single value
        arrVar = arr
        nonlocal global_bypass
        nonlocal subtract_key

        if key_modules[4]["use"] == True and global_bypass == False:
            log_process("Algebraic Key Module")

            # performs all algebraic exponentiation
            ref = getIdx("algexp", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # Log keyword
                log_process(arrVar[ref])

                # get arguments
                args = arrVar[ref + 1]

                # handle power
                if isinstance(args[1], str):
                    # convert then append power value
                    x = float(args[1])
                    args[1] = x
                else:
                    # simplify power expression then append power value
                    x = section(args[1])
                    # convert power expression product to integer
                    args[1] = int(x)

                # perform algebraic operation using numeral set
                base = args[0] # base expression
                power = args[1] # power value

                # log values
                log_process("Base expression = %s" % base)
                log_process("Power value = %s" % power)

                # build exponentiation by power value
                if power == 0:
                    # x^0 = 1

                    # restructure with section
                    arrVar = restructure(["1"], ref, ref + 1, arrVar)
                    # get next instance
                    ref = getIdx("algexp", arrVar)

                elif power < 0:
                    # x^-y = 1/(x^y)

                    sect = ["1", "/", "("] + base
                    for j in range(0, abs(power) - 1):
                        sect = sect + ["*"]
                        sect = sect + base
                    sect = sect + [")"]

                    # restructure with section
                    arrVar = restructure(sect, ref, ref + 1, arrVar)
                    # get next instance
                    ref = getIdx("algexp", arrVar)

                else:
                    # general
                    # build section
                    sect = ["("] + base + [")"]
                    for j in range(0, power - 1):
                        sect = sect + ["*"]
                        sect = sect + ["("] + base + [")"]
                    
                    # restructure with section
                    arrVar = restructure(sect, ref, ref + 1, arrVar)
                    # get next instance
                    ref = getIdx("algexp", arrVar)

            # # performs all polynomial expansions
            ref = getIdx("expand", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                # get arguments
                nomials = arrVar[ref + 1]

                # Log keyword
                log_process(arrVar[ref])
                log_process(nomials)

                if len(nomials) == 1 or len(nomials) == 0:
                    # cannot expand a single nomial or no nomial

                    # Log keyword
                    log_process(arrVar[ref])
                    # restructure with product expression
                    arrVar = restructure(nomials, ref, ref + 1, arrVar)
                    # identify further cases of polynomial expansion
                    ref = getIdx("expand", arrVar)

                else:
                    # multiple nomials can be expanded

                    # reference structure for section with distribution
                    sect_struct = []

                    # Use nomials to create sect_struct
                    for nomial in nomials:
                        x = get_terms(nomial)
                        # standardize terms
                        for t in range(len(x)):
                            x[t] = standardize_form(x[t])
                        sect_struct += get_terms(x)

                    # print(sect_struct)

                    # initialize sect_product with the first nomial in sect_struct
                    sect_product = sect_struct[0]

                    # multiply each nomial with the data in the sect_product variable
                    for i in range(1, len(sect_struct)):
                        # each expansion of nomials
                        product = []
                        for x in sect_product:
                            # x = each term in sect_product
                            if x[0] == subtract_key:
                                x.pop(0) # remove subtract key
                                n = num_cast(x[0])
                                if not isinstance(n, bool):
                                    # negate coefficient
                                    x[0] = -n
                                else:
                                    # -1 coefficient
                                    x.insert(0, operation["multiplication"])
                                    x.insert(0, "%s1" % (operation["subtraction"]))

                            for y in sect_struct[i]:
                                # y = each term in the next nomial
                                if y[0] == subtract_key:
                                    y.pop(0) # remove subtract key
                                    n = num_cast(y[0])
                                    if not isinstance(n, bool):
                                        # negate coefficient
                                        y[0] = -n
                                    else:
                                        # -1 coefficient
                                        y.insert(0, operation["multiplication"])
                                        y.insert(0, "%s1" % (operation["subtraction"]))

                                # get product term
                                # print("this")
                                # print(x)
                                # print(y)
                                # print(product_term(x, y))
                                product += product_term(x, y)
                                product.append(operation["addition"])
                        
                            # update sect product with last product for next expansion
                            product.pop() #remove extra addition symbol
                            # print(product)
                            sect_product = get_terms(product)
                            # print(sect_product)
                            product.append(operation["addition"])
                    
                        # print(sect_product)
                    # print(sect_product)
                    log_process(sect_product)

                    expansion = []
                    for i in sect_product:
                        expansion += i
                        expansion += operation["addition"]
                    expansion.pop()

                    # print(expansion)

                    expansion = simplify(expansion)

                    # print(expansion)

                    # restructure with product expression
                    arrVar = restructure(expansion, ref, ref + 1, arrVar)
                    # identify further cases of polynomial expansion
                    ref = getIdx("expand", arrVar)

        return arrVar

    def key_functions(arr):
        # runs key function modules
        nonlocal is_var
        arrVar = arr

        # Log process label for key functions
        log_process("Key Functions")

        if is_var == True:
            # ALGEBRAIC MODULE
            arrVar = algebraic(arrVar)
        else:
            # TRIGONOMIC MODULE
            arrVar = trigonomic(arrVar)
            # GEOMETRIC MODULE
            arrVar = geometric(arrVar)
            # COMBINATORIC MODULE
            arrVar = combinatoric(arrVar)
            # STATISTICAL MODULE
            arrVar = statistical(arrVar)

        log_process("Key Functions Complete")
        return arrVar
    
    # KEY FUNCTIONS END

    def calculate(arr):
        nonlocal global_bypass
        arrVar = arr
        if global_bypass == True:
            return arrVar
        else:
            # scans for operations and calculates then simplifies

            # perform all key functions (in section)

            # if there are identified key functions
            is_key_len = len(is_key)
            if is_key_len > 0:
                # test if there are keys in section
                keys_in_section = False
                for i in range(0, is_key_len):
                    for j in range(0, len(arrVar)):
                        if is_key[i] == arrVar[j]:
                            keys_in_section = True
                            break
                    if keys_in_section == True:
                        break
                if keys_in_section == True:
                    # run key functions on section
                    arrVar = key_functions(arrVar)
            
            if global_bypass == True:
                return arrVar
            else:
                # perform all arithmetic operations accounting for operator precedence
                log_process("Calculating Arithmetic Operations in Operator Precedence")
                log_process(arrVar)

                # perform all exponentiations
                if is_exp == True:
                    ref = getIdx(operation["exponentiation"], arrVar)
                    while ref is not None:
                        x = exponentiate(arrVar[ref - 1], arrVar[ref + 1])
                        arrVar = restructure(x, ref - 1, ref + 1, arrVar)
                        ref = getIdx(operation["exponentiation"], arrVar)

                # Perform all square roots
                if is_root == True:
                    ref = getIdx(operation["radication"], arrVar)
                    while ref is not None:
                        x = 0
                        if ref - 1 > -1 and not op_test(arrVar[ref - 1]):
                            # radication of given degree
                            x = root(arrVar[ref + 1], arrVar[ref - 1])
                            arrVar = restructure(x, ref - 1, ref + 1, arrVar)
                            ref = getIdx(operation["radication"], arrVar)
                        else:
                            # square root
                            x = root(arrVar[ref + 1], 2)
                            arrVar = restructure(x, ref, ref + 1, arrVar)
                            ref = getIdx(operation["radication"], arrVar)

                # perform all Multiplications and Divisions as they appear from left to right
                if is_mult == True and is_div == True:
                    m_ref = getIdx(operation["multiplication"], arrVar)
                    d_ref = getIdx(operation["division"], arrVar)
                    while m_ref is not None or d_ref is not None:
                        if d_ref is None and m_ref is not None:
                            # Only Multiply
                            x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                            arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)
                            m_ref = getIdx(operation["multiplication"], arrVar)

                        elif m_ref is None and d_ref is not None:
                            # Only Divide
                            x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                            if global_bypass == False:
                                arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                                d_ref = getIdx(operation["division"], arrVar)
                            else:
                                # division by zero
                                return x
                                
                        elif m_ref is not None and d_ref is not None and m_ref < d_ref:
                            # Multiply first
                            x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                            arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)

                            d_ref = getIdx(operation["division"], arrVar)
                            y = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                            if global_bypass == False:
                                arrVar = restructure(y, d_ref - 1, d_ref + 1, arrVar)

                                m_ref = getIdx(operation["multiplication"], arrVar)
                                d_ref = getIdx(operation["division"], arrVar)
                            else:
                                # divison by zero
                                return y

                        elif d_ref is not None and m_ref is not None and d_ref < m_ref:
                            # Divide First
                            x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                            if global_bypass == False:
                                arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                                m_ref = getIdx(operation["multiplication"], arrVar)

                                y = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                                arrVar = restructure(y, m_ref - 1, m_ref + 1, arrVar)

                                m_ref = getIdx(operation["multiplication"], arrVar)
                                d_ref = getIdx(operation["division"], arrVar)
                            else:
                                # division by zero
                                return x

                elif is_mult == True:
                    m_ref = getIdx(operation["multiplication"], arrVar)
                    while m_ref is not None:
                        x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                        arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)
                        m_ref = getIdx(operation["multiplication"], arrVar)

                elif is_div == True:
                    d_ref = getIdx(operation["division"], arrVar)
                    while d_ref is not None:
                        x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                        if global_bypass == False:
                            arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                            d_ref = getIdx(operation["division"], arrVar)
                        else:
                            # division by zero
                            return x

                # perform all Additions and Subtractions as they appear from left to right
                if is_add == True and is_sub == True:
                    a_ref = getIdx(operation["addition"], arrVar)
                    s_ref = getIdx(operation["subtraction"], arrVar)
                    while a_ref is not None or s_ref is not None:
                        if s_ref is None and a_ref is not None:
                            # only add
                            x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                            arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                            a_ref = getIdx(operation["addition"], arrVar)

                        elif a_ref is None and s_ref is not None:
                            # only subtract
                            x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                            arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                            s_ref = getIdx(operation["subtraction"], arrVar)

                        elif a_ref is not None and s_ref is not None and a_ref < s_ref:
                            # add first
                            x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                            arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                            a_ref = getIdx(operation["addition"], arrVar)

                            s_ref = getIdx(operation["subtraction"], arrVar)
                            y = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                            arrVar = restructure(y, s_ref - 1, s_ref + 1, arrVar)

                            a_ref = getIdx(operation["addition"], arrVar)
                            s_ref = getIdx(operation["subtraction"], arrVar)

                        elif s_ref is not None and a_ref is not None and s_ref < a_ref:
                            # subtract first
                            x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                            arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                            s_ref = getIdx(operation["subtraction"], arrVar)

                            a_ref = getIdx(operation["addition"], arrVar)
                            y = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                            arrVar = restructure(y, a_ref - 1, a_ref + 1, arrVar)

                            a_ref = getIdx(operation["addition"], arrVar)
                            s_ref = getIdx(operation["subtraction"], arrVar)
                
                elif is_add == True:
                    a_ref = getIdx(operation["addition"], arrVar)
                    while a_ref is not None:
                        x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                        arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                        a_ref = getIdx(operation["addition"], arrVar)
                
                elif is_sub == True:
                    s_ref = getIdx(operation["subtraction"], arrVar)
                    while s_ref is not None:
                        x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                        arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                        s_ref = getIdx(operation["subtraction"], arrVar)
                
                log_process("Calculation Complete")
                
                # test for variables in section
                is_variables = False
                for i in range(0, len(arrVar)):
                    if var_test(arrVar[i]) == True:
                        is_variables = True
                        break
                
                if is_variables == True:
                    # run algebraic simplifications
                    arrVar = simplify(arrVar)
                    # return algebraic expression
                    return arrVar
                else:
                    # return single value
                    return arrVar[0]

    def section(arr):
        # identifies next section of problem structure to process
        # runs calculation on section
        # if algebraic, runs simplification on section
        nonlocal global_bypass
        nonlocal is_paren
        arrVar = arr
        thresh = 0
        while global_bypass == False and is_paren == True and thresh < paren_limit:
            thresh = thresh + 1

            # test for parenthesis
            parens = []
            count = 0

            # build reference structure
            for i in range(0, len(arrVar)):
                if arrVar[i] == "(":
                    count = count + 1
                    parens.append({"index": i, "char": "("})
                elif arrVar[i] == ")":
                    count = count + 1
                    parens.append({"index": i, "char": ")"})
            
            if count == 0:
                is_paren = False
                break
            else:
                log_process("Parenthetical Section")
            
            # get section to be solved
            osme = []
            for i in range(0, len(parens)):
                if parens[i]["char"] == "(" and parens[i + 1]["char"] == ")":
                    arr_sect = arrVar[parens[i]["index"] + 1:parens[i + 1]["index"]]
                    # send to osme for restructing
                    osme.append({"section": arr_sect, "start": parens[i]["index"] + 1, "end": parens[i + 1]["index"]})

            # restructuring
            osme_length = len(osme)
            for i in range(0, osme_length):

                start = osme[osme_length - 1 - i]["start"] - 1
                end = osme[osme_length - 1 - i]["end"] + 1
                section = osme[osme_length - 1 - i]["section"]

                log_process(section)

                if len(section) > 1:

                    # calculate and simplify section
                    section = calculate(section)

                    if global_bypass == False:

                        # test for variables in section
                        # if there are no variables, section should be the single value result of the arithmetic operations of the pre-calculated section
                        # handle parenthetical algebraic expressions
                        if isinstance(section, list):

                            # identify expression operation (distributable operations)
                            # any case which does not remove the parenthesis should be excluded from expression operations
                            terms = get_terms(section)
                            terms_len = len(terms)
                            parens_removed = False

                            if terms_len == 1: # single term expression

                                # exponentation (distributes accross multiplication; only single term expressions)
                                # case 1: ( x * y ) ^ a => x ^ a * y ^ a, where "a" is a value
                                # case 2: ( x * y ) ^ z => x ^ z * y ^ z, where "z" is a variable
                                # case 3: ( x * y ) ^ (a + b) => x ^ c * y ^ c, where "a" and "b" are values whose sum is "c"
                                # case 4 [EXCLUDE]: ( x * y ) ^ (a + z) => x ^ (a + z) * y ^ (a + z), where "a + z" is an algebraic expression

                                if end < len(arrVar) - 1 - 2 and arrVar[end + 1] == operation["exponentiation"]:
                                    if arrVar[end + 2] == operation["open_parenthesis"]:
                                        # power expression
                                        nest = 0
                                        exp = []
                                        for i in range(end + 2, len(arrVar)):
                                            exp.append(arrVar[i])
                                            if var_test(arrVar[i]) == True:
                                                # case 4
                                                return arrVar
                                            if arrVar[i] == operation["open_parenthesis"]:
                                                nest += 1
                                            elif arrVar[i] == operation["close_parenthesis"]:
                                                nest -= 1
                                                if nest == 0:
                                                    # extend the end of setion to reach end of power expression
                                                    end = i
                                                    break
                                        
                                        # case 3: calculate power expression by parenthetical section
                                        exp = section(exp)
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["exponentiation"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()

                                        arrVar = restructure(x, start, end - 1, arrVar)
                                        
                                    elif var_test(arrVar[end + 2]) == True:
                                        # variable power
                                        # case 2
                                        end += 2
                                        exp = arrVar[end + 2]
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["exponentiation"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()

                                        arrVar = restructure(x, start, end - 1, arrVar)

                                    else:
                                        # power value
                                        # case 1
                                        end += 2
                                        exp = arrVar[end + 2]
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["exponentiation"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()

                                        arrVar = restructure(x, start, end - 1, arrVar)

                                # radication (distributes across multiplication; only single term expressions)
                                # case 1: √ ( x * y ) => √ x * √ y
                                # case 2: a √ ( x * y ) => a √ x * a √ y, where "a" is a value
                                # case 3: z √ ( x * y ) => z √ x * z √ y, where "z" is a variable
                                # case 4 [EXCLUDE]: (a + b) √ ( x * y ) => (a + b) √ x * (a + b) √ y
                                
                                elif end < len(arrVar) - 1 - 2 and arrVar[end + 1] == operation["radication"]:
                                
                                    if arrVar[end + 2] == operation["open_parenthesis"]:
                                        # power expression
                                        nest = 0
                                        exp = []
                                        for i in range(end + 2, len(arrVar)):
                                            exp.append(arrVar[i])
                                            if var_test(arrVar[i]) == True:
                                                # case 4
                                                return arrVar
                                            if arrVar[i] == operation["open_parenthesis"]:
                                                nest += 1
                                            elif arrVar[i] == operation["close_parenthesis"]:
                                                nest -= 1
                                                if nest == 0:
                                                    # extend the end of setion to reach end of power expression
                                                    end = i
                                                    break
                                        
                                        # case 3: calculate power expression by parenthetical section
                                        exp = section(exp)
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["radication"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()

                                        parens_removed = True
                                        arrVar = restructure(x, start, end - 1, arrVar)
                                        
                                    elif var_test(arrVar[end + 2]) == True:
                                        # variable power
                                        # case 2
                                        end += 2
                                        exp = arrVar[end + 2]
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["radication"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()

                                        parens_removed = True
                                        arrVar = restructure(x, start, end - 1, arrVar)

                                    else:
                                        # power value
                                        # case 1
                                        end += 2
                                        exp = arrVar[end + 2]
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        for i in section:
                                            buffer.append(i)
                                            if i == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        x = []
                                        op = operation["radication"]
                                        for i in result:
                                            x += i
                                            x.append(op)
                                            x.append(exp)
                                            x.append(delimiter)
                                        x.pop()
                                        
                                        parens_removed = True
                                        arrVar = restructure(x, start, end - 1, arrVar)

                            elif terms_len > 1: # multiple term expression
                                
                                # multiplication (distributes across addition and subtraction; single and multiple term expressions)
                                
                                # case 1: a * ( x + y ) => a * x + a * y 
                                if start - 2 > -1 and arrVar[start - 1] == operation["multiplication"]:
                                    x = []
                                    multiplier = arrVar[start - 2]
                                    op1 = operation["addition"]
                                    op2 = operation["subtraction"]
                                    op3 = operation["multiplication"]
                                    for t in terms:
                                        if t[0] == subtract_key:
                                            x.append(op2)
                                        else:
                                            x.append(op1)
                                        x += t
                                        x.append(op3)
                                        x.append(multiplier)
                                    
                                    if x[0] == op1:
                                        # remove extra addition at start
                                        x.pop(0)
                                    elif x[0] == op2:
                                        # handle negation of first term
                                        x.pop(0) # remove subtraction sign
                                        if var_test(x[0]) == True:
                                            # add coefficient to term
                                            x.insert(0, op3)
                                            x.insert(0, '%s1' % (op2))
                                        else:
                                            # negate term coefficient
                                            coef = -x[0]
                                            x.pop(0)
                                            x.insert(0, coef)

                                    parens_removed = True
                                    start -= 2
                                    arrVar = restructure(x, start, end - 1, arrVar)

                                # case 2: ( x + y ) * a => a * x + a * y 
                                elif end + 1 < len(arrVar) and arrVar[end] == operation["multiplication"]:
                                    x = []
                                    multiplier = arrVar[end + 1]
                                    op1 = operation["addition"]
                                    op2 = operation["subtraction"]
                                    op3 = operation["multiplication"]
                                    for t in terms:
                                        if t[0] == subtract_key:
                                            x.append(op2)
                                        else:
                                            x.append(op1)
                                        x += t
                                        x.append(op3)
                                        x.append(multiplier)
                                    
                                    if x[0] == op1:
                                        # remove extra addition at start
                                        x.pop(0)
                                    elif x[0] == op2:
                                        # handle negation of first term
                                        x.pop(0) # remove subtraction sign
                                        if var_test(x[0]) == True:
                                            # add coefficient to term
                                            x.insert(0, op3)
                                            x.insert(0, '%s1' % (op2))
                                        else:
                                            # negate term coefficient
                                            coef = -x[0]
                                            x.pop(0)
                                            x.insert(0, coef)

                                    parens_removed = True
                                    end += 1
                                    arrVar = restructure(x, start, end - 1, arrVar)
                            
                            # if parenthetical algebraic expression cannot be simplified and has no expression operations to remove parenthesis
                            # then return current problem structure as solution
                            # because the expressions in less nested parenthesis cannot be solved beyond that level of nesting
                            if parens_removed == False:
                                # handle unresolvable algebraic parenthetical sections
                                x = [operation["open_parenthesis"]] + section + [operation["close_parenthesis"]]
                                arrVar = restructure(x, start, end - 1, arrVar)
                                global_bypass = True
                                return arrVar

                        else:
                            # update arrVar with non-algebraic solution
                            arrVar = restructure(section, start, end - 1, arrVar)

                    else:
                        # section contains error message from calculation
                        return section
                    
                else:
                    # update arrVar with calculations and simplifications
                    arrVar = restructure(section, start, end - 1, arrVar)
        
        # if paren_limit was not reached and nested expressions are solved
        if global_bypass == False and thresh < paren_limit:

            # perform remaining calculations on un-nested expression
            arrVar = calculate(arrVar)
        
        # return result
        return arrVar

    def evaluate(str):
        # top level function runs high level functions
        # evaluate > section > calculate > key_functions + arithmetic + simplify
        nonlocal valid_chars

        # TEST0: character validation
        valid = True
        character = ""
        for char in str:
            try:
                int(char)
            except:
                # not a number
                o = False
                for c in valid_chars:
                    if char == c:
                        o = True
                        break
                if o == False:
                    # not a non-numeral character
                    valid = False
                    character = char
                    break
        
        if valid == False:
            # invalid character => terminate program
            return 'Invalid character: %s' % character
        else:
            # change first log
            if use_logs == "1":
                process_log["0"] = "Process Log Start"

            # valid characters => proceed to structuring
            log_process("Generating Problem Structure from Problem String")
            log_process("Structuring multi-digit numbers, negative numbers, decimal numbers, mathematical operations, parenthesis, and square brackets")
            # structure multi-digit numbers, negative numbers, decimal numbers, mathematical operations, parenthesis, and square brackets
            structure = []
            digits = ""
            for i in range(0, len(str)):
                if str[i] == " ":
                    continue
                else:
                    try:
                        str[i] == "." or int(str[i])
                    except:
                        # handle negatives
                        if str[i] == "-" and str[i - 1] == "(":
                            structure.pop()
                            digits = "%s" % str[i]
                        elif str[i] == ")":
                            try:
                                if int(digits) < 0:
                                    structure.append(digits)
                                    digits = ""
                                else:
                                    # 
                                    if len(digits) > 0:
                                        structure.append(digits)
                                        digits = ""
                                    # 
                                    structure.append(str[i])
                            except:
                                if len(digits) > 0:
                                    structure.append(digits)
                                digits = ""
                                structure.append(str[i])
                        else:
                            if len(digits) > 0:
                                structure.append(digits)
                            digits = ""
                            structure.append(str[i])
                    else:
                        digits = digits + "%s" % str[i]
                    finally:
                        if (i == len(str) - 1 and len(digits) > 0):
                            structure.append(digits)
            
            log_process(structure)
            log_process("Structuring Constants")

            # structure pi
            ref = get_word("pi", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.pi, ref["first"], ref["last"] - 1, structure)
                ref = get_word("pi", structure)
            
            # structure euler's number
            ref = get_word("euler", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.e, ref["first"], ref["last"] - 1, structure)
                ref = get_word("euler", structure)

            # structure keywords
            log_process("Structuring Keywords")
            
            # structure key functions
            for module in range(0, len(info["key_functions"])):
                for i in range(0, len(info["key_functions"][module])):
                    structure = word_struct(info["key_functions"][module][i]["key"], structure, module)

            log_process(key_modules)

            # Identify program entities in problem structure
            identify_entities(structure)

            # validate problem structure
            nonlocal is_key
            nonlocal is_brack
            nonlocal is_paren

            # validation variables
            test1 = True
            test2 = True
            test3 = True
            test4 = True
            test5 = True
            test6 = True
            key_error = ""
            structure_length = len(structure)

            # TEST6: Zero Division

            for i in range(0, structure_length):
                if i + 1 < structure_length and structure[i] == operation["division"] and structure[i + 1] == "0":
                    test6 = False
                    break

            # TEST5: consecutive operations

            if test6 == True:
                for i in range(0, structure_length):
                    # each index in problem structure
                    if i + 1 < structure_length:

                        first = False
                        second = False

                        for j in range(0, len(info["operations"]) - 5):
                            if structure[i] == info["operations"][j]["syntax"]:
                                first = True
                                break

                        if first == True:
                            for j in range(0, len(info["operations"]) - 5):
                                if structure[i + 1] == info["operations"][j]["syntax"] and not structure[i + 1] == operation["radication"]:
                                    second = True
                                    break

                        if first == True and second == True:
                            test5 = False
                            break

            # TEST1: valid parenthesis
            
            if is_paren == True and test6 == True and test5 == True:

                nest_lvl = 0
                parens = []

                for i in range(0, structure_length):
                    if structure[i] == operation["open_parenthesis"]:
                        nest_lvl += 1
                        parens.append(structure[i])
                    elif structure[i] == operation["close_parenthesis"]:
                        nest_lvl -= 1
                        parens.append(structure[i])

                if nest_lvl != 0:
                    # unequal number of open and closing characters
                    test1 = False
                elif parens[len(parens) - 1] == operation["open_parenthesis"]:
                    # no opening character on end
                    test1 = False
                elif parens[0] == operation["close_parenthesis"]:
                    # no closing character on start
                    test1 = False
                else:
                    # test for pairs (account for nesting)
                    for i in range(0, structure_length):
                        if structure[i] == operation["open_parenthesis"]:
                            x = 0
                            for j in range(i, structure_length):
                                if structure[j] == operation["close_parenthesis"]:
                                    x -= 1
                                elif structure[j] == operation["open_parenthesis"]:
                                    x += 1
                                if x == 0:
                                    break
                            if x != 0:
                                test1 = False
            
            # TEST2: valid brackets

            if is_brack == True and test6 == True and test5 == True and test1 == True:
                    
                nest_lvl = 0
                bracks = []

                for i in range(0, structure_length):
                    if structure[i] == operation["open_bracket"]:
                        nest_lvl += 1
                        bracks.append(structure[i])
                    elif structure[i] == operation["close_bracket"]:
                        nest_lvl -= 1
                        bracks.append(structure[i])

                if nest_lvl != 0:
                    # unequal number of open and closing characters
                    test2 = False
                elif bracks[len(bracks) - 1] == operation["open_bracket"]:
                    # no opening character on end
                    test2 = False
                elif bracks[0] == operation["close_bracket"]:
                    # no closing character on start
                    test2 = False
                else:
                    # test for pairs (account for nesting)
                    for i in range(0, structure_length):
                        if structure[i] == operation["open_bracket"]:
                            x = 0
                            for j in range(i, structure_length):
                                if structure[j] == operation["close_bracket"]:
                                    x -= 1
                                elif structure[j] == operation["open_bracket"]:
                                    x += 1
                                if x == 0:
                                    break
                            if x != 0:
                                test2 = False
            
            # TEST3: consecutive variables
            if test6 == True and test5 == True and test1 == True and test2 == True:
                for i in range(0, structure_length):
                    if i + 1 < structure_length and var_test(structure[i]) and var_test(structure[i + 1]):
                        test3 = False
                        break
            
            # TEST4: valid key function syntax

            if len(is_key) > 0 and test6 == True and test5 == True and test1 == True and test2 == True and test3 == True:
                if is_paren == False and is_brack == False:
                    # is key but no parenthesis and no brackets
                    test4 = False
                    key_error = 'key requires arguments wrapped in parenthesis or brackets'
                else:
                    # is key and parens or is key and brackets => test index
                    for i in range(0, structure_length):
                        if key_test(structure[i]):
                            # key at i
                            key = structure[i]
                            if i + 3 >= structure_length:
                                # key passed last valid index to also have arguments
                                test4 = False
                                key_error = '%s key requires an argument' % key
                                break
                            elif i + 1 < structure_length:
                                after_key = structure[i + 1]

                                if after_key != operation["open_parenthesis"] and after_key != operation["open_bracket"]:
                                    # no parens or bracks
                                    test4 = False
                                    key_error = '%s key requires an argument' % key
                                    break

                                else:
                                    # scan for key in info structure (ommitting algebraic module)
                                    for module in range(0, len(info["key_functions"]) - 1):
                                        # use key modules to determine which module(s) to scan
                                        if key_modules[module]["use"] == True:
                                            # scan module
                                            for j in range(0, len(info["key_functions"][module])):
                                                if key == info["key_functions"][module][j]["key"]:
                                                    # key discovered
                                                    syntax = info["key_functions"][module][j]["syntax"]
                                                    open_char = syntax[len(key):][0]

                                                    if after_key != open_char:
                                                        test4 = False
                                                        key_error = '%s key requires %s not %s' % (key, open_char, after_key)
                                                        break

                                                    elif open_char == operation["open_parenthesis"]:

                                                        # get argument section of problem structure
                                                        nest_lvl = 0
                                                        end_idx = structure_length

                                                        for c in range(i + 1, structure_length):
                                                            if structure[c] == operation["open_parenthesis"]:
                                                                nest_lvl += 1
                                                            elif structure[c] == operation["close_parenthesis"]:
                                                                nest_lvl -= 1
                                                                if nest_lvl == 0:
                                                                    end_idx = c
                                                                    break
                                                        
                                                        arguments = structure[i + 1:end_idx]
                                                        
                                                        # remove parenthesis from argument section
                                                        # arguments.pop(0)
                                                        # arguments.pop(len(arguments) - 1)

                                                        # test for no argument
                                                        if len(arguments) == 0:
                                                            test4 = False
                                                            key_error = '%s key requires an argument' % key

                                                        # test argument for variable + single argument
                                                        for c in arguments:
                                                            if var_test(c):
                                                                test4 = False
                                                                key_error = 'variables detected in argument for %s key' % key
                                                                break
                                                            elif c == ",":
                                                                # parenthesis cannot contain multiple arguments
                                                                test4 = False
                                                                key_error = '%s key only accepts a single argument' % key
                                                                break

                                                    elif open_char == operation["open_bracket"]:

                                                        # get argument section of problem structure
                                                        nest_lvl = 0
                                                        end_idx = structure_length

                                                        for c in range(i + 1, structure_length):
                                                            if structure[c] == operation["open_bracket"]:
                                                                nest_lvl += 1
                                                            elif structure[c] == operation["close_bracket"]:
                                                                nest_lvl -= 1
                                                                if nest_lvl == 0:
                                                                    end_idx = c
                                                                    break
                                                        arguments = structure[i + 1:end_idx]
                                                        
                                                        # remove open bracket
                                                        arguments.pop(0)

                                                        # test for no argument
                                                        if len(arguments) == 0:
                                                            test4 = False
                                                            key_error = '%s requires an argument' % key

                                                        # test argument for variables
                                                        for c in arguments:
                                                            if var_test(c):
                                                                test4 = False
                                                                key_error = 'variables detected in argument for %s key' % key
                                                                break
                                                        
                                                        # confirm that expression arguments are wrapped in square brackets
                                                        if test4 != False:
                                                            # break down arguments list into each argument
                                                            buffer = []
                                                            args = []
                                                            nest = 0
                                                            for c in arguments:
                                                                if c == operation["open_bracket"]:
                                                                    nest += 1
                                                                elif c == operation["close_bracket"]:
                                                                    nest -= 1

                                                                if c == "," and nest == 0:
                                                                    args.append(buffer)
                                                                    buffer = []
                                                                else:
                                                                    buffer.append(c)
                                                            args.append(buffer)

                                                            # test number of arguments
                                                            syntax_arguments = syntax[len(key):]
                                                            num_args = 0
                                                            nest = -1
                                                            for c in syntax_arguments:
                                                                if c == operation["open_bracket"]:
                                                                    nest += 1
                                                                elif c == operation["close_bracket"]:
                                                                    nest -= 1
                                                                
                                                                if nest == 0 and c == ",":
                                                                    num_args += 1

                                                            # correct fencepost error: no "," after last argument in syntax
                                                            num_args += 1

                                                            if len(args) < num_args:
                                                                # incorrect number of arguments
                                                                test4 = False
                                                                key_error = '%s key has insufficient arguments' % key
                                                                break

                                                            # test each argument
                                                            for c in range(0, len(args)):
                                                                if len(args[c]) > 1:
                                                                    if args[c][0] != operation["open_bracket"] or args[c][len(args[c]) - 1] != operation["close_bracket"]:
                                                                        test4 = False
                                                                        key_error = 'wrap expression arguments in brackets for %s key' % key
                                                                        break

                                        if test4 == False:
                                            break
                            
            if test1 == False:
                # invalid parenthesis => terminate program
                return "invalid parenthesis"
            elif test2 == False:
                # invalid brackets => terminate program
                return "invalid brackets"
            elif test3 == False:
                # consecutive variables => terminate program
                return "no consecutive variables"
            elif test4 == False:
                # invalid key function syntax => terminate program
                return key_error
            elif test5 == False:
                # consecutive operations => terminate program
                return "no consecutive operations"
            elif test6 == False:
                # dicision by zero => terminate program
                return "no division by zero"
            else:

                # generates substructures, i.e. "sets", within structure
                # sets exist so that multiple arguments can be accessed at a single index for key functions
                if is_brack == True:
                    # structure sets
                    log_process("Structure Sets")
                    log_process(structure)
                    sets_ref = []
                    for i in range(0, len(structure)):
                        if structure[i] == "[":
                            sets_ref.append({"char": "[", "index": i})
                        elif structure[i] == "]":
                            sets_ref.append({"char": "]", "index": i})
                    
                    # identify next set to structure using sets_ref
                    while len(sets_ref) > 0:
                        log_process(structure)
                        for i in range(0, len(sets_ref)):
                            if sets_ref[i]["char"] == "[" and sets_ref[i + 1]["char"] == "]":
                                # build set
                                start_index = sets_ref[i]["index"]
                                end_index = sets_ref[i + 1]["index"]
                                solution_length = abs(start_index - end_index) + 1
                                the_set_itself = []
                                for i in range(0, solution_length):
                                    the_set_itself.append(structure[start_index + i])

                                # restructure
                                structure = restructure(the_set_itself, start_index, end_index, structure)
                                
                                # update reference
                                sets_ref = []
                                for i in range(0, len(structure)):
                                    if structure[i] == "[":
                                        sets_ref.append({"char": "[", "index": i})
                                    elif structure[i] == "]":
                                        sets_ref.append({"char": "]", "index": i})
                                break
                
                # mark end of structuring pocess
                log_process("Problem Structure Generation Complete")

                if is_paren == True:
                    # parenthetically section and solve
                    return section(structure)
                else:
                    # calculate answer from problem structure
                    return calculate(structure)

    # Evaluation
    use_logs = input["use_logs"]
    problem = "empty string"
    answer = "empty string"

    # pre-structure problem validation
    if len(input["problem"]) > 0:
        # non-empty string
        if len(set(input["problem"])) > 1:
            
            # run evaluation
            problem = input["problem"]
            answer = evaluate(problem)

        else:
            # string of single character type
            try:
                # numeral character type
                int(input["problem"])
                problem = input["problem"]
                answer = input["problem"]
            except:
                # non-numeral character type
                problem = input["problem"]
                answer = "single type of character"

    # convert answer expressions to answer string
    if isinstance(answer, list):
        string = ""
        for i in answer:
            string = string + str(i)
        answer = string

    # assign output object
    output = {
        "problem": problem,
        "answer": answer,
        "logs": process_log,
    }

    return output

#     # Development

#     # Prints feedback
#     logs = """"""
#     process_log_keys = list(process_log.keys())
#     for key in process_log_keys:
#         logs += """%s
# """ % process_log[key]
    
#     print(output["problem"])
#     print(output["answer"])
#     print(logs)

# # test case
# input = {
#     # next case to develop 
#     # "problem": "(4*x)/(2*x)", # note: 
#     # "problem": "expand[[x/b*a+y],[x/a*b-y]]", # note: 
#     # "problem": "2*((4+8)+x)", # note: prevents calulation beyond the level of parenthetical nesting of an unresolvable algebraic expression
#     "problem": "2*((x*y)^2)", # note: expression operation exponentiation case 1
#     # "problem": "", # note: 
#     "use_logs": "", # 1 = yes, else = no 
# }
# evaluator(input)

# # comprehensive testing
# tests = [

#     # PRE-STRUCTURE VALIDATION

#     {"problem": "", "answer": "empty string"}, # prevents evaluation on empty string
#     {"problem": "        ", "answer": "single type of character"}, # prevents evaluation of string with single type of character
#     {"problem": "11111111", "answer": "11111111"}, # returns problem of string with single type of numeral character

#     # TEST0
#     {"problem": "1+1/&%$#", "answer": "Invalid character: &"},

#     # PROBLEM STRUCTURE VALIDATION

#     # TEST6
#     {"problem": "1/0", "answer": "no division by zero"},
#     {"problem": "3/(2-2)", "answer": "no division by zero"},

#     # TEST5
#     {"problem": "1++1", "answer": "no consecutive operations"},
#     {"problem": "1+-1", "answer": "no consecutive operations"}, # different operations
#     {"problem": "2*√16", "answer": "8"}, # except for second operation being √
#     {"problem": "1√*16", "answer": "no consecutive operations"}, # including for first operation being √

#     # TEST1
#     {"problem": "1)+(1*2)", "answer": "invalid parenthesis"}, #      )()     : unequal number of open and close characters
#     {"problem": "1+)1(+(1*2)", "answer": "invalid parenthesis"}, #   )(()    : no close on first parens
#     {"problem": "(1*2)+)1(+1", "answer": "invalid parenthesis"}, #   ())(    : no open on last parens
#     {"problem": "(1*2)+)3(+(1)", "answer": "invalid parenthesis"}, # ())(()  : all open characters have a closing pair
    
#     # TEST2    
#     {"problem": "1]+[1*2]", "answer": "invalid brackets"}, #      ][]     : unequal number of open and close characters
#     {"problem": "1+]1[+[1*2]", "answer": "invalid brackets"}, #   ][[]    : no close on first parens
#     {"problem": "[1*2]+]1[+1", "answer": "invalid brackets"}, #   ]][     : no open on last parens
#     {"problem": "[1*2]+]3[+[1]", "answer": "invalid brackets"}, # []][[]  : all open characters have a closing pair

#     # TEST3
#     {"problem": "2+3-xi", "answer": "no consecutive variables"}, # prevents program from evaluating problem structure if the problem structure has consecutive variables

#     # TEST4
#     {"problem": "sin", "answer": "key requires arguments wrapped in parenthesis or brackets"}, # prevents program from evaluating problem structure if the problem structure has key without parens or bracks
#     {"problem": "7-sin+1", "answer": "key requires arguments wrapped in parenthesis or brackets"}, # prevents program from evaluating problem structure if the problem structure has key without parens or bracks in middle of problem
#     {"problem": "(1+2)*3-sin", "answer": "sin key requires an argument"}, # prevents program from evaulating problem structure if there is a key at the end with no argument
#     {"problem": "sin+1*(2-3)", "answer": "sin key requires an argument"}, # prevents program from evaulating problem structure if there is a key before the end with no argument
#     {"problem": "sin([9-8],2)", "answer": "sin key only accepts a single argument"}, # prevents multiple arguments in single argument functions while allowing expression arguments

#     {"problem": "sin[0]", "answer": "sin key requires ( not ["}, # prevents program from evaulating problem structure if wrong open and close characters are used
#     {"problem": "mean(4,8)", "answer": "mean key requires [ not ("}, # prevents program from evaulating problem structure if wrong open and close characters are used

#     {"problem": "sin(x)", "answer": "variables detected in argument for sin key"}, # prevents program from evaulating problem structure if variable argument in parenthesis
#     {"problem": "sin(1+2/x)", "answer": "variables detected in argument for sin key"}, # prevents program from evaulating problem structure if variable in expression argument in parenthesis
#     {"problem": "sin()", "answer": "sin key requires an argument"}, # prevents running of key function with no argument in parenthesis

#     {"problem": "mean[4,x]", "answer": "variables detected in argument for mean key"}, # prevents program from evaulating problem structure if variable argument in brackets
#     {"problem": "mean[4,[2*x]]", "answer": "variables detected in argument for mean key"}, # prevents program from evaulating problem structure if variable in expression argument in brackets
#     {"problem": "mean[]", "answer": "mean key requires an argument"}, # prevents running of key function with no argument in brackets
#     {"problem": "mean[4,4+4]", "answer": "wrap expression arguments in brackets for mean key"}, # prevents running of key function without expression arguments wrapped in square brackets
#     {"problem": "mean[4,[4+4]]", "answer": "6.0"}, # as it should be; gets 6.0

#     {"problem": "sd[[mean[0,0]],1]", "answer": "0.5"}, # validation works for key function composition; gets 0.5

#     {"problem": "mean[10]", "answer": "mean key has insufficient arguments"}, # prevents program from evaluating problem structure if insufficient arguments for key function
#     {"problem": "meanw[[10,0.5]]", "answer": "meanw key has insufficient arguments"}, # prevents program from evaluating problem structure if insufficient arguments for key function with expression arguments
    
#     {"problem": "sin(1,[2*8/4-2])", "answer": "sin key only accepts a single argument"}, # prevents mutiple arguments into single argument key function permitting expression arguments
    
#     # KEY FUNCTION ARGUMENT DOMAIN VALIDATION

#     # TRIGONOMIC
#     {"problem": "acsc(0)", "answer": "invalid argument = x, -1 < x < 1"},

#     {"problem": "csc(0)", "answer": "no zero argument"},

#     {"problem": "asec(0)", "answer": "invalid argument = x, -1 < x < 1"},

#     {"problem": "sec((-1))", "answer": "invalid argument = x, x <= 0 or x >= π"},
#     {"problem": "sec(0)", "answer": "invalid argument = x, x <= 0 or x >= π"},
#     {"problem": "sec(pi)", "answer": "invalid argument = x, x <= 0 or x >= π"},
#     {"problem": "sec(pi+1)", "answer": "invalid argument = x, x <= 0 or x >= π"},

#     {"problem": "acot(0)", "answer": "no zero argument"},

#     {"problem": "cot(0)", "answer": "invalid argument = x, x = 0 or x mod π = 0"},
#     {"problem": "cot(2*pi)", "answer": "invalid argument = x, x = 0 or x mod π = 0"},
    
#     {"problem": "acosh(0)", "answer": "invalid argument = x, x < 1"},

#     {"problem": "atanh(0)", "answer": "invalid argument = x, -1 < x < 1"},

#     {"problem": "asin(2)", "answer": "invalid argument = x, x < -1 or x > 1"},

#     {"problem": "acos(2)", "answer": "invalid argument = x, x < -1 or x > 1"},

#     {"problem": "tan(0)", "answer": "invalid argument = x, -1 < x < 1 or x mod π = 0"},
#     {"problem": "tan(2*pi)", "answer": "invalid argument = x, -1 < x < 1 or x mod π = 0"},

#     # GEOMTERIC
#     {"problem": "hypot[1,0]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "hypot[1,(-1)]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "hypot[0,1]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "hypot[(-1),1]", "answer": "invalid argument = x, x <= 0"},

#     {"problem": "heron[1,1,0]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "heron[1,1,(-1)]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "heron[1,0,1]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "heron[1,(-1),1]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "heron[0,1,1]", "answer": "invalid argument = x, x <= 0"},
#     {"problem": "heron[(-1),1,1]", "answer": "invalid argument = x, x <= 0"},

#     # COMBINATORIC
#     {"problem": "perm[(-1),3]", "answer": "invalid arguments: n <= 0 or r <= 0 or n < r"},
#     {"problem": "perm[3,(-1)]", "answer": "invalid arguments: n <= 0 or r <= 0 or n < r"},
#     {"problem": "perm[2,3]", "answer": "invalid arguments: n <= 0 or r <= 0 or n < r"},

#     {"problem": "comb[(-1),3]", "answer": "invalid arguments: n <= 0 or r <= 0 or n <= r"},
#     {"problem": "comb[3,(-1)]", "answer": "invalid arguments: n <= 0 or r <= 0 or n <= r"},
#     {"problem": "comb[2,5]", "answer": "invalid arguments: n <= 0 or r <= 0 or n <= r"},

#     # STATISTICAL
#     {"problem": "meanh[1,0,2]", "answer": "no zero argument"},
    
#     {"problem": "gcf[2,(-3)]", "answer": "invalid argument = x, x <= 0"},

#     {"problem": "lcm[2,(-3)]", "answer": "invalid argument = x, x <= 0"},
    
#     {"problem": "log[(-1),10]", "answer": "invalid argument = x, x <= 0"},

#     {"problem": "ln((-3))", "answer": "invalid argument = x, x <= 0"},

#     # ALGEBRAIC

    
#     # KEY FUNCTION LOGIC TESTS
    
#     # TRIGONOMIC
#     {"problem": "acsc(csc(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "asec(sec(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "acot(cot(1))", "answer": "1.0"}, # pass = 1

#     {"problem": "asinh(sinh(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "acosh(cosh(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "atanh(tanh(1))", "answer": "1.0"}, # pass = 1

#     {"problem": "asin(sin(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "acos(cos(1))", "answer": "1.0"}, # pass = 1
#     {"problem": "atan(tan(1))", "answer": "1.0"}, # pass = 1

#     # GEOMTERIC
#     {"problem": "hypot[3,4]", "answer": "5.0"}, # pass = 5
#     {"problem": "heron[3,4,5]", "answer": "6.0"}, # pass = 6

#     # COMBINATORIC
#     {"problem": "fact(5)", "answer": "120"}, # pass = 120
#     {"problem": "perm[3,2]", "answer": "6.0"}, # pass = 6.0
#     {"problem": "comb[3,2]", "answer": "3.0"}, # pass = 3.0

#     # STATISTICAL
#     {"problem": "sd[0,2]", "answer": "1.0"}, # pass = 1.0
#     {"problem": "var[0,2]", "answer": "1.0"}, # pass = 1.0
#     {"problem": "meanh[2,2]", "answer": "2.0"}, # pass = 2.0
#     {"problem": "meang[1,4]", "answer": "2.0"}, # pass = 2.0
#     {"problem": "meanw[[1,3],[5,1]]", "answer": "2.0"}, # pass = 2.0
#     {"problem": "mean[1,3]", "answer": "2.0"}, # pass = 2.0
#     {"problem": "rms[2,3]", "answer": "2.5495097567963922"}, # pass = 2.5495097567963922

#     {"problem": "gcf[10,15]", "answer": "5"}, # pass = 5
#     {"problem": "lcm[7,2]", "answer": "14"}, # pass = 14

#     {"problem": "log[10,10]", "answer": "1.0"}, # pass = 1.0
#     {"problem": "ln(1)", "answer": "0.0"}, # pass = 0.0

#     # KEY FUNCTION COMPOSITION TEST
#     {"problem": "sd[[sin(0)],[cos(0)]]", "answer": "0.5"}, # should get 0.5; key functions can run as arguments to other key functions for key function composition
    
#     # N-TH RADICATION
#     {"problem": "3√8", "answer": "2.0"}, # permits n-th degree radication

    
#     # ALGEBRAIC SIMPLIFICATION

#     {"problem": "a+a+a-2*3", "answer": "3*a-6"}, # solve arithmetic in algebraic expression even if not in parens

#     {"problem": "a*a*a", "answer": "a^3"}, # simplifies algebraic expression for consecutive multiplications
#     {"problem": "2*x*9", "answer": "18*x"}, #  a * x * b => (a*b) * x
#     {"problem": "2/x*9", "answer": "2/9*x"}, #  a / x * b => a / b * x
#     {"problem": "3*x*7*x", "answer": "21*x^2"}, # combine terms for variable with coefficients multiplied
#     {"problem": "3*x*x", "answer": "3*x^2"}, # combine terms one variable with coefficients multiplied
#     {"problem": "x*3*x", "answer": "3*x^2"}, # combine terms one variable with coefficients multiplied

#     {"problem": "a/a/a/a", "answer": "a/(a^3)"}, # simplifies algebraic expression for consecutive divisions of self; a/(a^3)
#     {"problem": "a*x/x", "answer": "a"}, # simplifies algebraic expression for cancelling out division by self with multiplication; x
#     {"problem": "x/a/a", "answer": "x"}, # simplifies algebraic expression for cancelling out division by self with division; x
#     {"problem": "a/a", "answer": "1"}, # simplifies algebraic expression for variable divide by itself; 1
#     {"problem": "10*x/2", "answer": "5*x"}, # a * x / b => (a/b) * x
#     {"problem": "10/x/2", "answer": "5/x"}, # a / x / b => (a/b) / x
#     {"problem": "4*x/2*x", "answer": "2"}, #  combine terms for variable with coefficients divided
#     {"problem": "3*x/x", "answer": "3"}, # combine terms one variable with coefficients divided
#     {"problem": "x/3", "answer": "x/3"}, # x / a cannot be further simplified
    
#     {"problem": "a+a+a", "answer": "3*a"}, # simplifies algebraic expression for consecutive additions
#     {"problem": "10+x+2", "answer": "x+12"}, # a + x + b => (a+b) + x
#     {"problem": "10-x+2", "answer": "(-x)+12"}, # a - x + b => (a+b) - x
#     {"problem": "2*x+4*x", "answer": "6*x"}, # add coefficients of like terms
#     {"problem": "2*x+4*y", "answer": "2*x+4*y"}, # don't add coefficients of not like terms
#     {"problem": "3*x+x", "answer": "4*x"}, # combine terms one variable with coefficients added
#     {"problem": "x+3*x", "answer": "4*x"}, # combine terms one variable with coefficients added
    
#     {"problem": "a-a-a-a", "answer": "-2*a"}, # simplifies algebraic expression for consecutive substractions
#     {"problem": "10+x-2", "answer": "x+8"}, # a + x - b => (a-b) + x
#     {"problem": "10-x-2", "answer": "(-x)+8"}, # a - x - b => (a-b) - x
#     {"problem": "8*x-3*x", "answer": "5*x"}, # subtract coefficients of like terms
#     {"problem": "8*x-3*y", "answer": "8*x-3*y"}, # don't subtract coefficients of not like terms
#     {"problem": "3*x-x", "answer": "2*x"}, # combine terms one variable with coefficients subtracted
#     {"problem": "x-3*x", "answer": "-2*x"}, # combine terms one variable with coefficients subtracted
#     {"problem": "3*x-x", "answer": "2*x"}, # a * x - x => (a - 1) * x
#     {"problem": "x-3*x", "answer": "-2*x"}, # x - a * x => (1 - a) * x

#     # ALGEBRAIC EXPRESSION FORMAT STANDARDIZATION

#     {"problem": "2-3*x", "answer": "-3*x+2"}, # prevents operation out of precedence in algebraic expressions using getidx function
#     {"problem": "x^2-3*y", "answer": "x^2-3*y"}, # prevents operation out of precedence in algebraic expressions using getidx function
#     {"problem": "2*y^2*3*x/b*a-5", "answer": "6*x*y^2/a*b-5"}, # standardizes terms: coefficient at start of divisional section + alphabetized variables + preserves subtraction of term
#     {"problem": "3+3*x-7-3*x^3", "answer": "-3*x^3+3*x-4"}, # standardizes expression: negates first term if subtracted + combines arithmetic terms into constant at end of expression
#     {"problem": "3*x^2-1+2*x^3", "answer": "2*x^3+3*x^2-1"}, # orders terms in decrimental order of term degree + prevent arithemetic on values operated on by higher precedence operators
#     {"problem": "a*x^3+a*x^2*y+a*x*y^2+a*y^3", "answer": "a*x^3+a*y^3+a*x^2*y+a*x*y^2"}, # (term indexes for coeficients) pascal's traingle expression format = 0, 1, 2, 3 => standard expression format = 0, 3, 1, 2; alternate from ends to center term assuming all term degrees from greatest to least are present
#     {"problem": "x*x+x*x*x", "answer": "x^3+x^2"}, # note: enure standards are enforced after simplification 

#     # COMBINATION OF LIKE TERMS
#     {"problem": "x*x+x*x*x+x*y+3*x*x*x", "answer": "4*x^3+x^2+x*y"}, # note: 
#     {"problem": "4*x^2+a^4*y-3*x^2+a^4*y", "answer": "2*a^4*y+x^2"}, # removes 1 coefficients + handles multiple lists of like terms
#     {"problem": "c*a^2/a*2+a*c*a/2*a", "answer": "2*a^2*c/2*a"}, # combines like terms with multiple divisional sections

#     # Expression Operations (distributable operations on algebraic expressions)
#     {"problem": "2*((4+8)+x)", "answer": "2*x+24"}, # able to remove last parenthesis by distributing 2 from before section
#     {"problem": "((4+8)+x)*2", "answer": "2*x+24"}, # able to remove last parenthesis by distributing 2 from after section

#     {"problem": "(x+1)+2", "answer": "(x+1)+2"}, # prevents calculation on unresolvable algebraic expressions
#     {"problem": "(x)+2", "answer": "x+2"}, # should get "x+2"; removes parenthesis on variables wrapped with no operations
#     {"problem": "(x-1*6/2)+2", "answer": "(x-3)+2"}, # solves up until unresolvable algebraic parenthetical section
    
#     # ALGEBRAIC KEY FUNCTIONS
#     {"problem": "algexp[[x+y],[2*1/1+1-1]]", "answer": "(x+y)*(x+y)"}, # algebraic exponentiation
#     {"problem": "expand[[a],[b-c],[d+e+f]]", "answer": "a*b*d+a*b*e+a*b*f-a*c*d-a*c*e-a*c*f"}, # polynomial expansion
#     {"problem": "expand[[x+y],[x-y]]", "answer": "x^2-y^2"}, # removes terms with zero coefficient; leaves constants be; catches coefficients after subtract key
#     {"problem": "expand[[x],[x]]", "answer": "x^2"}, # 

#     # {"problem": "x=2*x", "answer": ""}, # 
#     # {"problem": "x/(3*x)", "answer": "1/(2*x)"}, # 
#     # {"problem": "", "answer": ""}, # 
# ]
# def diagnostic():
#     global tests
#     print('Total number of tests: %s' % len(tests))
#     for i, obj in enumerate(tests):
#         print(obj["problem"])
#         output = evaluator({"problem": obj["problem"], "use_logs": ''})
#         if str(output["answer"]) != obj["answer"]:
#             return 'tests passed: %s' % str(i) + "\nproblem: " + obj["problem"] + "\ncorrect answer: " + obj["answer"] + "\ngiven answer: " + str(output["answer"])
#     return 'passed all tests'
# print(diagnostic())


# Flask APP
app = Flask(__name__)

# CORS wrapper
CORS(app)

# ROUTES

# Index route
@app.route("/", methods=["GET"])
def index():
    return "<div>Index route accessed.</div>"

# Hello world environment variable demonstration
@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "<p>%s</p>" % os.environ['greeting']

# Evaluator data root
@app.route("/eval", methods=["POST"])
def eval():
    try:
        return jsonify(evaluator(request.get_json()))
    except Exception as e:
        return "Error:", e
    
# Evaluator problem data
@app.route("/eval/problem", methods=["POST"])
def eval_problem():
    try:
        return jsonify(evaluator(request.get_json())["problem"])
    except Exception as e:
        return "Error:", e

# Evaluator answer data
@app.route("/eval/answer", methods=["POST"])
def eval_answer():
    try:
        return jsonify(evaluator(request.get_json())["answer"])
    except Exception as e:
        return "Error:", e

# Evaluator log data
@app.route("/eval/logs", methods=["POST"])
def eval_logs():
    try:
        return jsonify(evaluator(request.get_json())["logs"])
    except Exception as e:
        return "Error:", e

# Evaluator info object data (read-only)
@app.route("/eval/info", methods=["GET"])
def eval_info():
    try:
        return jsonify(info)
    except Exception as e:
        return "Error:", e