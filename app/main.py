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
        {"name":"𝜏", "syntax":"tau"}, # alt code 231
        {"name":"φ", "syntax":"phi"}, # alt code 237 or 232 for capital
        {"name":"Euler's Number (e)", "syntax":"euler"},
        {"name":"Euler's Constant (Γ)", "syntax":"gamma"}, # alt code 226
    ],

    # the whole lowercase alphabet may be used as variables (keys are also composed of lowercase letters)
    # "variables": ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w"],
    "variables": ["x", "y", "z", "a", "b", "c", "n", "i"], # 8 variables is plenty

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
    paren_limit = 1000

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
        variables += v

    # represents a string containing all of the valid non-numeral characters
    valid_chars = " " + "." + "," + "defghijklmnopqrstuvw" + variables + operation["addition"] + operation["subtraction"] + operation["multiplication"] + operation["division"] + operation["exponentiation"] + operation["radication"] + operation["open_parenthesis"] + operation["close_parenthesis"] + operation["open_bracket"] + operation["close_bracket"]
    
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
        neg = operation["subtraction"]
        for i in variables:
            if i == str or neg + i == str:
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
        # serve error on non-entity detection
        nonlocal operation
        nonlocal is_paren
        nonlocal is_brack
        nonlocal is_exp
        nonlocal is_root
        nonlocal is_mult
        nonlocal is_div
        nonlocal is_add
        nonlocal is_sub
        nonlocal is_var
        
        for i in arr:

            # Identify parenthesis
            if i == operation["open_parenthesis"] or i == operation["close_parenthesis"]:
                is_paren = True
        
            # Identify square brackets
            elif i == operation["open_bracket"] or i == operation["close_bracket"]:
                is_brack = True

            # Identify exponentiation
            elif i == operation["exponentiation"]:
                is_exp = True

            # Identify roots
            elif i == operation["radication"]:
                is_root = True
        
            # Identify multiplication
            elif i == operation["multiplication"]:
                is_mult = True
        
            # Identify division
            elif i == operation["division"]:
                is_div = True
        
            # Identify addition
            elif i == operation["addition"]:
                is_add = True
        
            # Identify subtraction
            elif i == operation["subtraction"]:
                is_sub = True
            
            # Identify number
            elif not isinstance(num_cast(i), bool):
                continue
            
            # Identify algebraic mode
            elif var_test(i):
                is_var = True

            # identify key
            elif key_test(i):
                continue

            # serve error for non-entity
            elif i != " " and i != "." and i != ",":
                return "non-entity detected: %s" % i
        
        # return empty string on no error
        return ""
        
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
    def neg_var(v1, v2):
        # handles negativity for multiplication and division of variables v1 and v2
        s = operation["subtraction"]
        v_neg1 = True
        v_neg2 = True
        if str(v1)[0] == s:
            v_neg1 = False
        if str(v2)[0] == s:
            v_neg2 = False
        
        if v_neg1 and v_neg2: # both positive
            # return positive
            return v1
        elif not v_neg1 and not v_neg2: # both negative
            # return positive
            return v1
        elif not v_neg1 and v_neg2: # first negative, second positive 
            # return first
            return v1
        elif v_neg1 and not v_neg2: # first positive, second negative
            # return second
            return v2
    
    def equ_var(v1, v2):
        # returns true if same variable () negated or not
        s = operation["subtraction"]
        vs1 = str(v1)
        vs2 = str(v2)
        if vs1 == vs2: # both negative or both positive
            return True
        elif s + vs1 == vs2: # positive v1 and negative v2
            return True
        elif vs1 == s + vs2: # negative v1 and positive v2
            return True
        else:
            return False
            
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
        nonlocal subtract_key
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
                if t1_dat[x]["var"] != t2_dat[x]["var"]:
                    return False
                else:
                    p1 = num_cast(t1_dat[x]["pow"])
                    p2 = num_cast(t2_dat[x]["pow"])
                    if not isinstance(p1, bool) and not isinstance(p2, bool) and p1 != p2:
                        return False
        else:
            # dissimilar length of main term and compare term  
            return False

        # no conditions met for falsification
        return True

    def combine_terms(t1, t2):
        # returns terms combined by addition or subtraction
        # note: for use on terms returning true from like_terms(t1, t2)
        # meaning t1 and t2 both have the same variables and powers for those variables
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

    def test_term_ends(c1, c2, arr):
        # tests ends of term to ensure that the entire term is identified by condition
        arr_len = len(arr)

        # test both ends
        if c1 - 1 > -1 and c2 + 1 < arr_len:
            if arr[c1 - 1] == operation["addition"] or arr[c1 - 1] == operation["subtraction"]:
                if arr[c2 + 1] == operation["addition"] or arr[c2 + 1] == operation["subtraction"]:
                    return True
            
        # test back end
        elif c1 - 1 > -1 and c2 + 1 >= arr_len:
            if arr[c1 - 1] == operation["addition"] or arr[c1 - 1] == operation["subtraction"]:
                return True
        
        # test front end
        elif c2 + 1 < arr_len and c2 + 1 < arr_len:
            if arr[c2 + 1] == operation["addition"] or arr[c2 + 1] == operation["subtraction"]:
                return True
        
        # no ends to test
        elif c1 == 0 and c2 + 1 == arr_len:
            return True
        
        # no true condition reached (e.g. index out of range or not entire term)
        return False

    def standardize_form(arr):
        # identifies terms in algebraic expression,
        # standardizes term forms, combines like terms,
        # standardizes expression form, returns result
        log_process("Standardizing Format of Algebraic Terms and Expressions")
        log_process(arr)
        # print(arr)

        # return empty argument
        if len(arr) == 0:
            log_process("Standardization Aborted")
            return arr

        # prevent standardization on blacklisted characters
        for i in arr:
            if i == operation["open_parenthesis"] or i == operation["close_parenthesis"] or i == operation["open_bracket"] or i == operation["close_bracket"]:
                log_process("Standardization Aborted")
                return arr

        # term standards
        #  1- single coefficient at starting index 2*x^2*3*y => 6*x^2*y
        #  2- variables in alphabetical order within divisional sections of term b^2*3*a^3/b*a => 3*a^3*b^2/a*b

        # expression standards
        #  1- Decremental order of term degree  x^2 + 2*x^3 - 6*x => 2*x^3 + x^2 - 6*x
        #  2- arithmetic terms are combined into single constant at end of expression
        #  3- combine like algebraic terms
        #  4- terms with zero coefficient are removed
        #  5- Negativity is transfered from variables to coefficients and from coefficients to operators
        #       - negative variables with coefficients become positive variables with negated coefficients
        #       - non-leading terms subtract positive coefficient instead of adding negative coefficient
        #       - leading term stores negativity in coefficient
        
        nonlocal subtract_key
        sect_struct = get_terms(arr) # stores terms as sublists
        expression = [] # stores terms as sublists in original order but with term standards
        formatted = [] # stores terms concatenated into single list with term and expression standards

        # print(sect_struct)

        # --- TERM STANDARDS ---
        log_process("Imposition of Term Standards")

        # iterate over each term
        for t in sect_struct:
            log_process("Term Identified")

            # declare variables
            is_subtracted = False
            if len(str(t[0])) > 0 and t[0] == subtract_key:
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
                    var = t[j]

                    # remove negativity from var for alphabetic index test
                    if len(var) > 1 and var[0] == operation["subtraction"]:
                        v = var[1]
                        var = v
                    
                    alpha = None
                    for a in range(0, 26):
                        if var == alphabet[a]:
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

                        elif j + 4 < length and t[j + 1] == operation["multiplication"] and not isinstance(num_cast(t[j + 2]), bool) and t[j + 3] == operation["exponentiation"]:
                            # case: a * b ^ x or a * b ^ (x + 1)
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

                # store product of coeffients from each divisional section in term
                log_process(" 1- Calculate Coefficient Product")
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

                # alphabetize variables in each divisional section of current term
                log_process(" 2- Variable Alphabetization")
                # 1. initialize divisional section variables
                # 2. skip initial divisional sections without variables
                # 3. iterate for the number of variables in current term
                # 4. iterate from start index to end index (each divisional section)
                # 5. collect variables in section, preventng duplicate selection
                # 6. get differences between each variable's alphabetical index and the index of the last selection
                # 7. identify smallest difference
                # 8. append tdata object for variable with smallest difference to the alphabetical structure
                # 9. at last variable in divisional section, skip intermittent divisional sections without variables until at next section
                # 10. repeat for next divisional section, until there are none remaining or until the number of variables is reached
                # 11. skip final divisional sections without variables (if any)
                
                # initialize divisional section variables
                divisions_i = 0
                start = 0
                end = length
                if d_length > 0:
                    end = divisions[divisions_i]["term_index"]
                
                # declare alphabetical structure before skipping divisional sections to add placeholders for divisional sections
                alphabetical = []
                # declare alphabetical_not structure before skipping divisional sections to add placeholders for divisional sections
                alphabetical_not = []
                a_is = False
                a_isnt = False

                # skip initial divisional sections without variables
                loop_count = 0
                while loop_count < d_length and divisions[divisions_i]["var_count"] == 0:
                    loop_count += 1

                    # append placeholder for divisional section
                    alphabetical.append({"term_index": None})
                    alphabetical_not.append({"term_index": None})

                    # move to next divisional section
                    start = end
                    divisions_i += 1
                    if divisions_i < d_length:
                        end = divisions[divisions_i]["term_index"]
                    else:
                        end = length
                
                for i in range(0, var_count):

                    # store difference ommitting variables below previous minimum alphabetic index
                    diffs = []
                    op1 = operation["exponentiation"]
                    op2 = operation["radication"]
                    for j in range(start, end):
                        d = tdata[j]["alpha_index"]
                        ti = tdata[j]["term_index"]
                        if d != None and d >= last:
                            use = True
                            
                            # ommit variables that are powers and variables that are indexes of radicals from alphabetization
                            cond1 = j > 1 and tdata[j - 1]["value"] == op1
                            cond2 = j + 1 < length and tdata[j + 1]["value"] == op2
                            if cond1 == True or cond2 == True:
                                use = False
                                unique = True

                                # exclude variables that are powers with variable bases and variables that are indexes of radicals with variable bases
                                if cond1 == True and j > 2 and var_test(tdata[j - 2]["value"]) == True or cond2 == True and j + 2 < length and var_test(tdata[j + 2]["value"]) == True:
                                    unique = False
                                else:
                                    # test alphabetical_not for duplicates
                                    for a in alphabetical_not:
                                        if ti == a["term_index"]:
                                            unique = False
                                            break

                                # append variables that are not to be alphabetized to alpha_not
                                if unique == True:
                                    a_isnt = True
                                    alphabetical_not.append(tdata[j])
                            
                            # test alphabetical for duplicates
                            if use == True:
                                for a in alphabetical:
                                    if ti == a["term_index"]:
                                        use = False
                                        break
                            
                            if use == True:
                                a_is = True
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
                                break
                    
                    # on end of divisional section
                    if divisions_i < d_length and i == divisions[divisions_i]["var_count"] - 1 or i == var_count - 1:
                        
                        last = 0

                        # skip intermittent divisional sections without variables
                        loop_count = divisions_i
                        if loop_count + 1 < d_length and divisions[loop_count + 1]["var_count"] == divisions[loop_count]["var_count"]:
                            
                            while loop_count + 1 < d_length and divisions[loop_count + 1]["var_count"] == divisions[loop_count]["var_count"]:

                                loop_count += 1

                                # append placeholder for divisional section
                                alphabetical.append({"term_index": None})
                                alphabetical_not.append({"term_index": None})

                                # move to next divisional section
                                start = end
                                divisions_i += 1
                                if divisions_i < d_length:
                                    end = divisions[divisions_i]["term_index"]
                                else:
                                    end = length
                        
                        # handle placeholders
                        elif a_is == True and a_isnt == False:
                            a_is = False
                            alphabetical_not.append({"term_index": None})

                        elif a_is == False and a_isnt == True:
                            a_isnt == False
                            alphabetical.append({"term_index": None})
                        else:
                            a_is = False
                            a_isnt = False
                            
                        # move to next divisional section
                        start = end
                        divisions_i += 1
                        if divisions_i < d_length:
                            end = divisions[divisions_i]["term_index"]
                        else:
                            end = length
                
                # skip final divisional sections without variables
                loop_count = divisions_i
                while loop_count <= d_length:
                    loop_count += 1

                    # append placeholder for divisional section
                    alphabetical.append({"term_index": None})
                    alphabetical_not.append({"term_index": None})

                    # move to next divisional section
                    start = end
                    divisions_i += 1
                    if divisions_i < d_length:
                        end = divisions[divisions_i]["term_index"]
                    else:
                        end = length

                # print(alphabetical)
                # print(alphabetical_not)

                # append sub-lists of divisional sections from alphabetical list to alpha list
                alpha_do = [] # from alphabetical
                div_sect = []
                divisions_i = 0 # reset to zero
                alphabetical_len = len(alphabetical)
                for i in range(alphabetical_len):
                    if alphabetical[i]["term_index"] == None:
                        # object at current index is a placeholder

                        # skipped divisional sections without variables
                        if len(div_sect) > 0:
                            alpha_do.append(div_sect)
                            div_sect = []
                        alpha_do.append([alphabetical[i]]) # append placeholder
                        divisions_i += 1

                    elif i + 1 < alphabetical_len and alphabetical[i + 1]["term_index"] == None:
                        # object at next index is a placeholder
                        
                        # end of divisional section
                        div_sect.append(alphabetical[i])
                        if len(div_sect) > 0:
                            alpha_do.append(div_sect)
                            div_sect = []
                        divisions_i += 1

                    elif divisions_i < d_length and i + 1 < alphabetical_len and alphabetical[i + 1]["term_index"] != None and alphabetical[i + 1]["term_index"] > divisions[divisions_i]["term_index"]:
                        # object at next index has value at property term_index that is greater than the value at property term_index for the object at the current index of divisions
                        
                        # end of divisional section
                        div_sect.append(alphabetical[i])
                        if len(div_sect) > 0:
                            alpha_do.append(div_sect)
                            div_sect = []
                        divisions_i += 1
                        
                    else:
                        # general case
                        div_sect.append(alphabetical[i])
                
                # append remainder
                if len(div_sect) > 0:
                    alpha_do.append(div_sect)

                alpha_dont = [] # from alphabetical_not
                div_sect = [] # clear previous
                divisions_i = 0 # reset to zero
                alphabetical_not_len = len(alphabetical_not)
                for i in range(alphabetical_not_len):
                    if alphabetical_not[i]["term_index"] == None:
                        # object at current index is a placeholder

                        # skipped divisional sections without variables
                        if len(div_sect) > 0:
                            alpha_dont.append(div_sect)
                            div_sect = []
                        alpha_dont.append([alphabetical_not[i]]) # append placeholder
                        divisions_i += 1

                    elif i + 1 < alphabetical_not_len and alphabetical_not[i + 1]["term_index"] == None:
                        # object at next index is a placeholder
                        
                        # end of divisional section
                        div_sect.append(alphabetical_not[i])
                        if len(div_sect) > 0:
                            alpha_dont.append(div_sect)
                            div_sect = []
                        divisions_i += 1

                    elif divisions_i < d_length and i + 1 < alphabetical_not_len and alphabetical_not[i + 1]["term_index"] != None and alphabetical_not[i + 1]["term_index"] > divisions[divisions_i]["term_index"]:
                        # object at next index has value at property term_index that is greater than the value at property term_index for the object at the current index of divisions

                        # end of divisional section
                        div_sect.append(alphabetical_not[i])
                        if len(div_sect) > 0:
                            alpha_dont.append(div_sect)
                            div_sect = []
                        divisions_i += 1
                        
                    else:
                        # general case
                        div_sect.append(alphabetical_not[i])
                
                # append remainder
                if len(div_sect) > 0:
                    alpha_dont.append(div_sect)

                # print(alpha_do)
                # print(alpha_dont)

                # collect non-coefficient constants by divisional section
                constants = []
                add_placeholder = True
                div_sect = [] # repurpose as buffer for constants
                divisions_i = 0 # reset to zero
                end = length
                if d_length > 0:
                    end = divisions[divisions_i]["term_index"]
                
                for i in range(length):
                    if i < end:
                        # test if non-coefficient constant
                        op1 = operation["exponentiation"]
                        op2 = operation["radication"]
                        if tdata[i]["coef"] == False and tdata[i]["alpha_index"] == None and not op_test(tdata[i]["value"]):
                            if i - 1 <= -1 or tdata[i - 1]["value"] != op1:
                                if i + 1 >= length or tdata[i + 1]["value"] != op2:
                                    if i + 1 >= length or tdata[i + 1]["value"] != op1:
                                        # start and middle
                                        add_placeholder = False
                                        div_sect.append(tdata[i])

                    elif i == length - 1 and len(constants) == d_length and tdata[i]["coef"] == False and tdata[i]["alpha_index"] == None and not op_test(tdata[i]["value"]):
                        # ensure is constant
                        if i - 1 > -1:
                            # in bounds for test
                            if tdata[i - 1]["value"] == operation["addition"] or tdata[i - 1]["value"] == operation["subtraction"] or tdata[i - 1]["value"] == operation["division"]:
                                # special end case: constant in last divisional section
                                div_sect.append(tdata[i])
                                constants.append(div_sect)
                            else:
                                # not a constant
                                if add_placeholder == True:
                                    # add placeholder
                                    div_sect.append({"term_index": None})
                                else:
                                    # setup placeholder for next divisional section
                                    add_placeholder = True

                                constants.append(div_sect)
                                div_sect = []

                        else:
                            # out of bounds for constant test
                            div_sect.append(tdata[i])
                            constants.append(div_sect)

                    else:
                        # check at end for weather at least one value was added in last divisional section
                        if add_placeholder == True: # no value added
                            # add placeholder
                            div_sect.append({"term_index": None})
                        else:
                            # setup placeholder for next divisional section
                            add_placeholder = True

                        constants.append(div_sect)
                        div_sect = []

                        divisions_i += 1
                        if divisions_i < d_length:
                            end = divisions[divisions_i]["term_index"]
                        else:
                            end = length - 1

                # print(coefficiency) # coefficient products are collected by divisional section within each term
                # print(alpha_do) # variables (non-radical and non-exponential) are collected and alphabatized by divisional section within each term
                # print(alpha_dont) # variables (radical and exponential) are collected by divisional section within each term
                # print(constants) # constants are properly identified and structured by divisional section within each term

                # use data to create expression term structure
                term = []
                coefficiency_len = len(coefficiency)
                alpha_do_len = len(alpha_do)
                alpha_dont_len = len(alpha_dont)
                constants_len = len(constants)
                for i in range(0, d_length + 1):
                    # iterate over each divisional section
                    # coefficient goes at start of divisional section in term
                    # coefficients are broken down by divisional section to avoid rounding errors from division
                    # ommit coefficients of 1
                    if i < coefficiency_len and coefficiency[i] != 1:
                        term.append(coefficiency[i])

                    # print(term)

                    if i < alpha_do_len:
                        # alphabetized
                        for obj in alpha_do[i]:
                            t_i = obj["term_index"]
                            start = t_i
                            end = t_i
                            if t_i != None: # exclude placeholders
                                # test for bounds of variable
                                if t_i + 2 < length and t[t_i + 1] == operation["exponentiation"]:
                                    end += 2
                                if t_i - 1 > -1 and t[t_i - 1] == operation["radication"]:
                                    if t_i - 2 > -1 and not op_test(t[t_i - 2]):
                                        # n-th root
                                        start -= 2
                                    else:
                                        # square root
                                        start -= 1

                                # add data to term
                                if start == end:
                                    # single variable
                                    if len(term) == 0:
                                        # variable at start of term or of divisional section
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
                                    # intermittent expression
                                    term_len = len(term)
                                    term.append(operation["multiplication"])
                                    # test for begining of divisional section of term
                                    if term_len == 0 or term[term_len - 1] == operation["division"]:
                                        term.pop() # remove multiplication symbol
                                    exp = t[start:end + 1]
                                    for obj in exp:
                                        term.append(obj)

                    # print(term)

                    if i < alpha_dont_len:
                        # not alphabetized

                        for j in range(len(alpha_dont[i])):
                            obj = alpha_dont[i][j]
                            t_i = obj["term_index"]
                            if t_i != None: # exclude placeholders
                                # test for bounds of variable
                                o = [obj["value"]]
                                op1 = operation["exponentiation"]
                                op2 = operation["radication"]
                                
                                # x = variable
                                # k = number
                                # a√b^c, a = x or a = k, b = x or b = k, c = x or c = k
                                # restrictions: a = b = c =/ k and a = b =/ k and b = c =/ k

                                # ---------------------------------
                                # CASE      | NAME      | RANGES 
                                # ---------------------------------
                                #             Combined
                                # ---------------------------------
                                # √x^k      | case b    | -1 to +2
                                # ---------------------------------
                                # √k^x      | case c    | -3 to +0
                                # ---------------------------------
                                # k√x^k     | case b    | -2 to +2
                                # ---------------------------------
                                # k√k^x     | case c    | -4 to +0
                                # ---------------------------------
                                # √x^x      | case b    | -1 to +2
                                # ---------------------------------
                                # x√x^k     | case ab   | -0 to +4
                                # ---------------------------------
                                # x√k^x     | case ac   | -0 to +4
                                # ---------------------------------
                                # k√x^x     | case bc   | -2 to +2
                                # ---------------------------------
                                # x√x^x     | case abc  | -0 to +4
                                # ---------------------------------
                                #             Exponent
                                # ---------------------------------
                                # x^k       | case b    | -0 to +2
                                # ---------------------------------
                                # k^x       | case c    | -2 to +0
                                # ---------------------------------
                                # x^x       | case bc   | -0 to +2
                                # ---------------------------------
                                #             Radical
                                # ---------------------------------
                                # x√k       | case a    | -0 to +2
                                # ---------------------------------
                                # k√x       | case b    | -2 to +0
                                # ---------------------------------
                                # x√x       | case ab   | -0 to +2
                                # ---------------------------------
                                # √x        | case b    | -1 to +0
                                # ---------------------------------

                                # cases ommitted from alphabetical

                                # Combined
                                if t_i - 4 > -1 and test_term_ends(t_i - 4, t_i, t) and t[t_i - 1] == op1 and t[t_i - 3] == op2 and t[t_i - 4] != operation["close_parenthesis"]:
                                    # allow expression if previous non-alpha variable has term index below min index of expresion or above max index of expression
                                    if j - 1 <= -1 or alpha_dont[i][j - 1]["term_index"] < t_i - 4 or alpha_dont[i][j - 1]["term_index"] > t_i:
                                        # extend term
                                        # x = c
                                        o = t[t_i - 4: t_i + 1]
                                        term_len = len(term)
                                        if term_len > 0 and term[term_len - 1] != operation["division"]:
                                            term.append(operation["multiplication"])
                                        term.extend(o)

                                elif t_i - 2 > -1 and t_i + 2 < length and test_term_ends(t_i - 2, t_i + 2, t) and t[t_i - 1] == op2 and t[t_i + 2] == op1 and t[t_i + 3] != operation["open_parenthesis"]:
                                    # allow expression if previous non-alpha variable has term index below min index of expresion or above max index of expression
                                    if j - 1 <= -1 or alpha_dont[i][j - 1]["term_index"] < t_i - 2 or alpha_dont[i][j - 1]["term_index"] > t_i + 2:
                                        # extend term
                                        # x = b
                                        o = t[t_i - 2 : t_i] + o + t[t_i + 1: t_i + 2]
                                        term_len = len(term)
                                        if term_len > 0 and term[term_len - 1] != operation["division"]:
                                            term.append(operation["multiplication"])
                                        term.extend(o)
                                
                                elif t_i + 4 < length and test_term_ends(t_i, t_i + 4, t) and t[t_i + 1] == op2 and t[t_i + 3] == op1 and t[t_i + 4] != operation["open_parenthesis"]:
                                    # allow expression if previous non-alpha variable has term index below min index of expresion or above max index of expression
                                    if j - 1 <= -1 or alpha_dont[i][j - 1]["term_index"] < t_i or alpha_dont[i][j - 1]["term_index"] > t_i + 4:
                                        # extend term
                                        # x = a
                                        o = t[t_i: t_i + 4 + 1]
                                        term_len = len(term)
                                        if term_len > 0 and term[term_len - 1] != operation["division"]:
                                            term.append(operation["multiplication"])
                                        term.extend(o)
                                
                                # Exponent
                                elif t_i - 2 > -1 and t[t_i - 1] == op1:
                                    o.insert(0, op1)
                                    if t[t_i - 2] == operation["close_parenthesis"]:
                                        # get expression base
                                        opar = operation["open_parenthesis"]
                                        cpar = operation["close_parenthesis"]
                                        nest = 0
                                        close = t_i + 2
                                        count = 0
                                        maxim = length - close
                                        while count < maxim and nest == 0 and t[close] != cpar:
                                            count += 1
                                            close += 1
                                            if t[close] == opar:
                                                nest += 1
                                            elif t[close] == cpar:
                                                nest -= 1

                                        # extend with expression base
                                        o = t[t_i + 2 : close + 1] + o

                                        # extend term
                                        term_len = len(term)
                                        if term_len > 0 and term[term_len - 1] != operation["division"]:
                                            term.append(operation["multiplication"])
                                        term.extend(o)

                                    elif not var_test(t[t_i - 2]):
                                        # insert base
                                        o.insert(0, t[t_i - 2])

                                        # extend term
                                        term_len = len(term)
                                        if len(term) > 0 and term[term_len - 1] != operation["division"]:
                                            term.append(operation["multiplication"])
                                        term.extend(o)

                                # Radical 
                                elif t_i + 2 < length and t[t_i + 1] == op2:
                                    if t[t_i + 2] == operation["open_parenthesis"]:
                                        opar = operation["open_parenthesis"]
                                        cpar = operation["close_parenthesis"]
                                        nest = 0
                                        close = t_i + 2
                                        count = 0
                                        maxim = length - close
                                        while count < maxim and nest == 0 and t[close] != cpar:
                                            count += 1
                                            close += 1
                                            if t[close] == opar:
                                                nest += 1
                                            elif t[close] == cpar:
                                                nest -= 1
                                        
                                        # extend with expression base
                                        o = t[t_i + 2 : close + 1] + o

                                        # extend term

                                        term.extend(o)

                                    else:
                                        # insert base
                                        o.insert(0, t[t_i + 2])

                                        # extend term
                                        term.extend(o)
                                
                                # print(term)
                    
                    # print(term)

                    if i < constants_len and constants[i][0]["term_index"] != None:
                        term.append(constants[i][0]["value"])
                    
                    # print(term)

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
        # print(expression)
        if len(expression) == 1:
            # not an expression of terms; single term
            # return formatted term
            log_process("Standardization Complete")
            log_process(expression[0])
            return expression[0]
        else:
            log_process("Imposition of Expression Standards")

            # combine all arithemtic terms into single constant term at end of expression
            log_process(" 1- Combination of Arithmetic Terms into Constant")
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
                c = num_cast(c)
                if not isinstance(c, bool):
                    if c >= 0:
                        constant = [c]
                    else:
                        constant = [subtract_key, -c]
                
                # put constant on end of term
                expression.append(constant)

            # print(expression)

            # order expression in decremental order of term degree
            log_process(" 2- Polynomials in Decremental Order of Term Degree")
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
                        if not isinstance(x, bool) and x > degree:
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

            log_process(" 3- Combination of Like Algebraic Terms")
            # print(degree_order)
            
            # combine like terms:
            #  - same degree in both terms
            #  - same variables in both terms
            #  - same exponenets for each variable in both terms

            indexes = list(range(len(degree_order)))

            main_index = 0
            while len(indexes) > 1:

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
            log_process(" 4- Remove terms with zero coefficient")
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


            # Handle Negativity
            log_process(" 5- Negativity is transfered from variables to coefficients and from coefficients to operators")
            # print(degree_order)

            # concatenate terms into formatted expression
            degree_order_len = len(degree_order)

            # leading term
            if degree_order[0][0] == subtract_key:
                # subtract key

                # remove subtract key
                degree_order[0].pop(0)
                a = degree_order[0][0]
                x = num_cast(a)
                # test for coefficient
                if not isinstance(x, bool):
                    # transfer negativity of variables to coefficient
                    op = operation["subtraction"]
                    do = degree_order[0]
                    for j in range(len(do)): # iterate over term
                        if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                            # nagtive variable => transfer to coefficient
                            v = do[j][1]
                            degree_order[0][j] = v # remove negativity from variable
                            x = -x # negate coefficient

                    # transfer negativity from operation to coefficient
                    degree_order[0][0] = -x

                    # handle 1/-1 coefficient
                    if x == 1:
                        # remove coefficient
                        degree_order[0].pop(0)
                        # remove multiplication symbol
                        degree_order[0].pop(0)
                    elif x == -1 and len(degree_order[0]) > 2 and var_test(degree_order[0][2]) == True:
                        if len(degree_order[0]) > 4 == False or degree_order[0][3] != operation["exponentiation"] and degree_order[0][3] != operation["radication"]:
                            # remove coefficient
                            degree_order[0].pop(0)
                            # remove multiplication symbol
                            degree_order[0].pop(0)
                            # negate variable
                            if len(degree_order[0][0]) > 1 and degree_order[0][0][0] == operation["subtraction"]:
                                # negative variable
                                degree_order[0][0] = degree_order[0][0][1] # remove negativity 
                            else:
                                # positive variable
                                degree_order[0][0] = operation["subtraction"] + degree_order[0][0] # add negativity 


                else:
                    # transfer negativity of variables to placeholder
                    x = 1 # holder
                    op = operation["subtraction"]
                    do = degree_order[0]
                    for j in range(len(degree_order[0])): # iterate over term
                        if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                            # nagtive variable => transfer to coefficient
                            v = do[j][1]
                            degree_order[0][j] = v # remove negativity from variable
                            x = -x # negate coefficient
                    
                    if x > 0:
                        if x == 1:
                            if len(degree_order[0]) < 3 or degree_order[0][1] != operation["exponentiation"] and degree_order[0][1] != operation["radication"]:
                                degree_order[0][0] = operation["subtraction"] + degree_order[0][0] # negate variable
                            else:
                                # insert multiplication symbol
                                degree_order[0].insert(0, operation["multiplication"])
                                # insert negative coefficient
                                degree_order[0].insert(0, -x)
                        else:
                            # insert multiplication symbol
                            degree_order[0].insert(0, operation["multiplication"])
                            # insert negative coefficient
                            degree_order[0].insert(0, -x)
                    
            else:
                # no subtract key
                
                a = degree_order[0][0]
                x = num_cast(a)
                # test for coefficient
                if not isinstance(x, bool):
                    # transfer negativity of variables to coefficient
                    op = operation["subtraction"]
                    do = degree_order[0]
                    for j in range(len(do)): # iterate over term
                        if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                            # nagtive variable => transfer to coefficient
                            v = do[j][1]
                            degree_order[0][j] = v # remove negativity from variable
                            x = -x # negate coefficient
                            degree_order[0][0] = x # update structure with negated coefficient
                    
                    # handle 1/-1 coefficient
                    if x == 1:
                        # remove coefficient
                        degree_order[0].pop(0)
                        # remove multiplication symbol
                        degree_order[0].pop(0)
                    elif x == -1 and len(degree_order[0]) > 2 and var_test(degree_order[0][2]) == True:
                        if len(degree_order[0]) > 4 == False or degree_order[0][3] != operation["exponentiation"] and degree_order[0][3] != operation["radication"]:
                            # remove coefficient
                            degree_order[0].pop(0)
                            # remove multiplication symbol
                            degree_order[0].pop(0)
                            # negate variable
                            if len(degree_order[0][0]) > 1 and degree_order[0][0][0] == operation["subtraction"]:
                                # negative variable
                                degree_order[0][0] = degree_order[0][0][1] # remove negativity 
                            else:
                                # positive variable
                                degree_order[0][0] = operation["subtraction"] + degree_order[0][0] # add negativity 

            # extend with leading term
            formatted.extend(degree_order[0])
            
            # append addition symbol
            formatted.append(operation["addition"])

            # print(formatted)

            # rest of the iterations
            if degree_order_len > 1:
                for i in range(1, degree_order_len):
                    
                    # subtract key
                    if degree_order[i][0] == subtract_key:

                        # remove subtract key
                        degree_order[i].pop(0)

                        # store first value in term
                        x = num_cast(degree_order[i][0])
                        
                        # coefficient
                        if not isinstance(x, bool):

                            # transfer negativity of variables to coefficient
                            op = operation["subtraction"]
                            do = degree_order[i]
                            for j in range(len(do)): # iterate over term
                                if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                                    # nagtive variable => transfer to coefficient
                                    v = do[j][1]
                                    degree_order[i][j] = v # remove negativity from variable
                                    x = -x # negate coefficient
                                    
                            # transfer negativity of coefficient to operation
                            if x < 0:
                                # negative coefficieint
                                x = -x # make positive

                                # handle 1 coefficient
                                if x == 1 and len(degree_order[i]) > 2 and degree_order[i][1] == operation["multiplication"] and var_test(degree_order[2]):
                                    # remove coefficient
                                    degree_order[i].pop(0)
                                    # remove multiplication symbol
                                    degree_order[i].pop(0)
                                else:
                                    degree_order[i][0] = x # update

                                # operation remains as addition

                            else:
                                # handle 1 coefficient
                                if x == 1 and len(degree_order[i]) > 2 and degree_order[i][1] == operation["multiplication"] and var_test(degree_order[2]):
                                    # remove coefficient
                                    degree_order[i].pop(0)
                                    # remove multiplication symbol
                                    degree_order[i].pop(0)
                                else:
                                    # positive coeffficient
                                    degree_order[i][0] = x # update

                                # remove previous operation
                                formatted.pop()
                                # replace it with appropriate operation
                                formatted.append(op)
                        
                        # no coefficient
                        else:
                            # transfer negativity of variables to operation
                            x = 1 # placeholder
                            op = operation["subtraction"]
                            do = degree_order[i]
                            for j in range(len(do)): # iterate over term
                                if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                                    # nagtive variable => transfer to coefficient
                                    v = do[j][1]
                                    degree_order[i][j] = v # remove negativity from variable
                                    x = -x # negate coefficient
                            
                            # transfer negativity of placeholder to operation
                            if x > 0:
                                # remove previous operation
                                formatted.pop()
                                # replace it with appropriate operation
                                formatted.append(op)
                    
                    # no subtract key
                    else:

                        # store first value in term
                        x = num_cast(degree_order[i][0])
                        
                        # coefficient
                        if not isinstance(x, bool):

                            # transfer negativity of variables to coefficient
                            op = operation["subtraction"]
                            do = degree_order[i]
                            for j in range(len(do)): # iterate over term
                                if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                                    # nagtive variable => transfer to coefficient
                                    v = do[j][1]
                                    degree_order[i][j] = v # remove negativity from variable
                                    x = -x # negate coefficient

                            # transfer negativity of coefficient to operation
                            if x < 0:
                                # negative coefficient

                                x = -x # make positive

                                # handle 1 coefficient
                                if x == 1 and len(degree_order[i]) > 2 and degree_order[i][1] == operation["multiplication"] and var_test(degree_order[i][2]):
                                    # remove coefficient
                                    degree_order[i].pop(0)
                                    # remove multiplication symbol
                                    degree_order[i].pop(0)
                                else:
                                    # positive coeffficient
                                    degree_order[i][0] = x # update

                                # remove previous operation
                                formatted.pop()
                                # replace it with appropriate operation
                                formatted.append(op)

                            else:
                                # positive coefficient

                                # handle 1 coefficient
                                if x == 1 and len(degree_order[i]) > 2 and degree_order[i][1] == operation["multiplication"] and var_test(degree_order[2]):
                                    # remove coefficient
                                    degree_order[i].pop(0)
                                    # remove multiplication symbol
                                    degree_order[i].pop(0)
                                else:
                                    # positive coeffficient
                                    degree_order[i][0] = x # update
                                
                                # operation remains as addition

                        # no coefficient
                        else:
                            # transfer negativity of variables to operation
                            x = 1 # placeholder
                            op = operation["subtraction"]
                            do = degree_order[i]
                            for j in range(len(do)): # iterate over term
                                if var_test(do[j]) == True and len(do[j]) > 1 and do[j][0] == op:
                                    # nagtive variable => transfer to coefficient
                                    v = do[j][1]
                                    degree_order[i][j] = v # remove negativity from variable
                                    x = -x # negate coefficient
                            
                            # transfer negativity of placeholder to operation
                            if x < 0:
                                # remove previous operation
                                formatted.pop()
                                # replace it with appropriate operation
                                formatted.append(op)
                    
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

        # determines post-processes for simplification
        destandardized = False # re-standardize
        recalculate = False # re-calculate
        arrVar = standardize_form(arr)

        # log process label
        log_process("Simplification of Algebraic Expression")

        # define process of simplification
        # 1.) Format expression and terms into standard forms
        # 2.) identify first variable in arr testing from left to right
        # 3.) test simplification tree structure for cases until one is discovered and run that
        # 4.) repeat step 2 - 4 until no simplifications are discovered during step 2, then go to step 5
        # 5.) return result
        
        simplifying = True
        x = 0
        while x < simp_limit and simplifying == True:

            # each while loop interation is one simplification
            x += 1
            
            # get length of arrVar
            length = len(arrVar)

            # iterate over each string in problem structure
            for c in range(0, length):
                
                # identify variables in problem structure from left to right
                if var_test(arrVar[c]):

                    # each variable
                    var = arrVar[c]

                    # SIMPLIFICATION TREE STRUCTURE
                    # SUPERCLASSES: organizational layer for developer clarity
                    #   # CLASSES: layer for grouping cases to expedite tree performance
                    #    #   # CASES: each exact character by character case of simplification

                    # class switches (defaultly all on)
                    class_num = 11 # stores number of classes
                    x_y = True  # x^y
                    x_i = True  # x^i, where i is a number
                    i_x = True  # i^x, where i is a number
                    
                    k_x = True  # k√x, where k is a number
                    x_k = True  # x√k, where k is a number
                    y_x = True  # y√x
                    _x = True   # √x 

                    mult = True # multiplication
                    div = True  # division
                    add = True  # addition
                    sub = True  # subtraction

                    # while loop repeats, at most for the number of classes as stored in class_num, if no cases are identified in a class so other classes may be tested
                    # while loop terminates when all class are switched false
                    
                    lim = 0
                    simplifiable = True
                    while simplifiable == True and lim < class_num:
                        lim += 1
                        
                        # EXPONENTIATION SUPERCLASS

                        # x^y class
                        if x_y == True and c + 2 < length and arrVar[c + 1] == operation["exponentiation"] and var_test(arrVar[c + 2]) == True:
                            
                            # x^y case 1: x*x^y => x^(y+1), index = 2nd x
                            if c - 2 > -1 and c + 2 < length and test_term_ends(c - 2, c + 2, arrVar) and equ_var(arrVar[c - 2], var) and arrVar[c - 1] == operation["multiplication"]:
                                start = c - 2
                                end = c + 2
                                simp = [neg_var(arrVar[c - 2], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 2], operation["addition"], 1, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^y case 2: x^y*x => x^(y+1), index = 1st x
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 3] == operation["multiplication"] and equ_var(arrVar[c + 4], arrVar[c]):
                                start = c
                                end = c + 4
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 2], operation["addition"], 1, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                        
                            # x^y case 3: x^y * x^i
                            elif c + 6 < length and test_term_ends(c, c + 6, arrVar) and arrVar[c + 3] == operation["multiplication"] and equ_var(arrVar[c + 4], var) and arrVar[c + 5] == operation["exponentiation"] and not isinstance(num_cast(arrVar[c + 6]), bool):
                                start = c
                                end = c + 6
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 2], operation["addition"], arrVar[c + 6], operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^y case 4: x/x^y => x^(1-y), index = 2nd x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and equ_var(arrVar[c - 2], var) and arrVar[c - 1] == operation["division"]:
                                start = c - 2
                                end = c + 2
                                simp = [neg_var(arrVar[c - 2], var), operation["exponentiation"], operation["open_parenthesis"], 1, operation["subtraction"], arrVar[c + 2], operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                                
                            # x^y case 5: x^y/x => x^(y-1), index = 1st x
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and equ_var(arrVar[c + 4], var) and arrVar[c + 3] == operation["division"]:
                                start = c
                                end = c + 4
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 2], operation["subtraction"], 1, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^y case 6: x^y / x^i => x^(y-i)
                            elif c + 6 < length and test_term_ends(c, c + 6, arrVar) and arrVar[c + 3] == operation["division"] and equ_var(arrVar[c + 4], var) and arrVar[c + 5] == operation["exponentiation"] and not isinstance(num_cast(arrVar[c + 6]), bool):
                                start = c
                                end = c + 6
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 2], operation["subtraction"], arrVar[c + 6], operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                x_y = False
                            
                        # x^i class
                        elif x_i == True and c + 2 < length and arrVar[c + 1] == operation["exponentiation"] and not isinstance(num_cast(arrVar[c + 2]), bool):
                            
                            # expedite falsification
                            x_y = True  # x^y
                            
                            # x^i case 1: x*x^i => x^b, where b = i + 1, index = 2nd x
                            if c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and equ_var(arrVar[c - 2], var) and arrVar[c - 1] == operation["multiplication"]:
                                start = c - 2
                                end = c + 2
                                b = num_cast(arrVar[c + 2]) + 1
                                simp = [neg_var(arrVar[c - 2], var), operation["exponentiation"], b]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^i case 2: x/x^i => x^b, where b = 1 - i, index = 2nd x
                            elif c - 2 > -1 and c + 2 < length and test_term_ends(c - 2, c + 2, arrVar) and equ_var(arrVar[c - 2], var) and arrVar[c - 1] == operation["division"]:
                                start = c - 2
                                end = c + 2
                                b = 1 - num_cast(arrVar[c + 2])
                                simp = [neg_var(arrVar[c - 2], var), operation["exponentiation"], b]
                                arrVar = restructure(simp, start, end, arrVar)
                                break

                            # x^i case 3: x^i*x => x^b, where b = i + 1, index = 1st x
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 3] == operation["multiplication"] and equ_var(arrVar[c + 4], var):
                                start = c
                                end = c + 4
                                b = num_cast(arrVar[c + 2]) + 1
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], b]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^i case 4: x^i/x => x^b, where b = i - 1, index = 1st x
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 3] == operation["division"] and equ_var(arrVar[c + 4], var):
                                start = c
                                end = c + 4
                                b = num_cast(arrVar[c + 2]) - 1
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], b]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # x^i case 5: x^i * x^y => x^(y+i)
                            elif c + 6 < length and test_term_ends(c, c + 6, arrVar) and arrVar[c + 3] == operation["multiplication"] and equ_var(arrVar[c + 4], var) and arrVar[c + 5] == operation["exponentiation"] and var_test(arrVar[c + 6]) == True:
                                start = c
                                end = c + 6
                                simp = [neg_var(arrVar[c + 4], var), operation["exponentiation"], operation["open_parenthesis"], arrVar[c + 6], operation["addition"], arrVar[c + 2], operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                x_i = False

                        # i^x class
                        elif i_x == True and c - 2 > -1 and not isinstance(num_cast(arrVar[c - 2]), bool) and arrVar[c - 1] == operation["exponentiation"]:

                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            
                            # i^x case 1: i*i^x => i^(x+1)
                            if c - 4 > -1 and test_term_ends(c - 4, c, arrVar) and num_cast(arrVar[c - 4]) == num_cast(arrVar[c - 2]) and arrVar[c - 3] == operation["multiplication"]:
                                start = c - 4
                                end = c
                                simp = [arrVar[c - 2], operation["exponentiation"], operation["open_parenthesis"], var, operation["addition"], 1, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # i^x case 2: i/i^x => i^(1-x)
                            elif c - 4 > -1 and test_term_ends(c - 4, c, arrVar) and num_cast(arrVar[c - 4]) == num_cast(arrVar[c - 2]) and arrVar[c - 3] == operation["division"]:
                                start = c - 4
                                end = c
                                simp = [arrVar[c - 2], operation["exponentiation"], operation["open_parenthesis"], 1, operation["subtraction"], var, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            # i^x case 4: i^x/i => i^(x-1)
                            elif c + 2 < length and test_term_ends(c - 2, c + 2, arrVar) and not isinstance(num_cast(arrVar[c + 2]), bool) and arrVar[c + 1] == operation["division"]:
                                start = c - 2
                                end = c + 2
                                simp = [arrVar[c - 2], operation["exponentiation"], operation["open_parenthesis"], var, operation["subtraction"], 1, operation["close_parenthesis"]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                i_x = False

                        # RADICATION SUPERCLASS

                        # k√x class
                        elif k_x == True and c - 2 > -1 and arrVar[c - 1] == operation["radication"] and not isinstance(num_cast(arrVar[c - 2]), bool):
                            
                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            # k√x case 1: k√x^k = > x, operations cancel
                            if c + 2 < length and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c + 1] == operation["exponentiation"] and not isinstance(num_cast(arrVar[c + 2]), bool) and num_cast(arrVar[c + 2]) == num_cast(arrVar[c - 2]):
                                start = c - 2
                                end = c + 2
                                simp = [var]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                k_x = False
                                
                        # x√k class
                        elif x_k == True and c + 2 < length and arrVar[c + 1] == operation["radication"] and not isinstance(num_cast(arrVar[c + 2]), bool):
                            
                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            
                            # x√k case 1: x√k^x => k, operations cancel
                            if c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 3] == operation["exponentiation"] and equ_var(arrVar[c + 4], var):
                                start = c
                                end = c + 4
                                simp = [arrVar[c + 2]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                x_k = False
                                
                        # y√x class
                        elif y_x == True and c + 2 < length and arrVar[c + 1] == operation["radication"] and var_test(arrVar[c + 2]) == True:
                            
                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number

                            if c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 3] == operation["exponentiation"] and equ_var(arrVar[c + 4], var):
                                start = c
                                end = c + 4
                                simp = [arrVar[c + 2]]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                y_x = False
                            
                        # √x class
                        elif _x == True and c - 1 > -1 and arrVar[c - 1] == operation["radication"]:
                            
                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number
                            y_x = True  # y√x

                            # √x case 1: √x*√x => x, operations cancel
                            if c + 3 < length and test_term_ends(c - 1, c + 3, arrVar) and arrVar[c + 1] == operation["multiplication"] and arrVar[c + 2] == operation["radication"] and equ_var(arrVar[c + 3], var):
                                start = c - 1
                                end = c + 3
                                simp = [var]
                                arrVar = restructure(simp, start, end, arrVar)
                                break

                            # √x case 2: √x^2 => x, operations cancel
                            elif c + 2 < length and test_term_ends(c - 1, c + 2, arrVar) and arrVar[c + 1] == operation["exponentiation"] and not isinstance(num_cast(arrVar[c + 2]), bool) and num_cast(arrVar[c + 2]) == 2:
                                start = c - 1
                                end = c + 2
                                simp = [var]
                                arrVar = restructure(simp, start, end, arrVar)
                                break
                            
                            else:
                                _x = False
                            
                        # ALGEBRAIC ARITHMETIC SUPERCLASS
                        
                        # MULTIPLICATION CLASS
                        elif mult == True and c + 2 < length and arrVar[c + 1] == operation["multiplication"]:

                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number
                            y_x = True  # y√x
                            _x = True   # √x 

                            # SIMP1: multiplication of variables with coefficients

                            # case: a * x * b * x => (a*b) * x ^ 2, where a and b are particular values
                            if c - 2 > -1 and c + 4 < length and test_term_ends(c - 2, c + 4, arrVar) and arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not isinstance(num_cast(arrVar[c + 2]), bool):
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
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 4] == var and not var_test(arrVar[c + 2]):
                                # switch post-standardization to on
                                destandardized = True

                                # get term data
                                coefficient = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % coefficient, operation["multiplication"], var, operation["exponentiation"], "2"], c, c + 4, arrVar)
                                
                                # end current simplification
                                break

                            # SIMP3: a * x * b => (a*b) * x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % multiply(val1, val2), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                # end current simplification
                                break

                            # SIMP4: a / x * b => (a*b) / x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["division"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % multiply(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                        
                            # SIMP2: multiply a variable by itself
                            elif arrVar[c + 2] == var and operate(c + 1, arrVar) == True:

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
                            
                            else:
                                mult = False
                            
                        # DIVISION CLASS
                        elif div == True and c + 2 < length and arrVar[c + 1] == operation["division"]:

                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number
                            y_x = True  # y√x
                            _x = True   # √x 

                            mult = True # multiplication

                            # SIMP5: division of variables with coefficients

                            # case: a * x / b * x => a / b, where a and b are particular values
                            if c - 2 > -1 and c + 4 < length and test_term_ends(c - 2, c + 4, arrVar) and arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):

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

                            # SIMP7: a * x / b => (a/b) * x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
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
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and  arrVar[c - 1] == operation["division"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % divide(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)
                                
                                # end current simplification
                                break
                            
                            # SIMP6: divide a variable by itself
                            elif arrVar[c + 2] == var and operate(c + 1, arrVar) == True:

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
                                    # apply simplification to problem structure
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
                                    # numerical result triggers recalculation
                                    recalculate = True
                                    # apply simplification to problem structure
                                    arrVar = restructure("1", c, c + 2, arrVar)
                                    # end current simplification
                                    break
                            
                            else:
                                div = False
                                
                        # ADDITION CLASS
                        elif add == True and c + 2 < length and arrVar[c + 1] == operation["addition"]:

                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number
                            y_x = True  # y√x
                            _x = True   # √x 

                            mult = True # multiplication
                            div = True  # division
                            
                            # SIMP9: add coefficients between terms with no exponents
                            
                            # case: a * x + b * x => (a+b) * x
                            if c - 2 > -1 and c + 4 < length and test_term_ends(c - 2, c + 4, arrVar) and arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                coefficient1 = arrVar[c - 2]
                                coefficient2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % add(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                
                                # end current simplification
                                break

                            # case: a * x + x => (a + 1) * x, where a is a particular value
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c + 2] == var and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]):
                                    
                                # get term data
                                coefficient = arrVar[c - 2]

                                # apply simplification to problem structure
                                arrVar = restructure([str(int(coefficient) + 1), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                        
                            # case: x + a * x => (a + 1) * x, where a is a particular value
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar):
                                if arrVar[c + 4] == var and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c + 2]):

                                    # get term data
                                    coefficient = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure([str(int(coefficient) + 1), operation["multiplication"], var], c, c + 4, arrVar)

                                    # end current simplification
                                    break

                            # SIMP11: a + x + b => (a+b) + x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["addition"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % add(val1, val2), operation["addition"], var], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                            
                            # SIMP12: a - x + b => (a+b) - x
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["subtraction"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(val1, val2), operation["subtraction"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP10: add a variable to itself
                            elif arrVar[c + 2] == var and operate(c + 1, arrVar) == True:
                                
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
                            
                            else:
                                add = False
                            
                        # SUBTRACTION CLASS
                        elif sub == True and c + 2 < length and arrVar[c + 1] == operation["subtraction"]:

                            # expedite falsification
                            x_y = True  # x^y
                            x_i = True  # x^i, where i is a number
                            i_x = True  # i^x, where i is a number
                            
                            k_x = True  # k√x, where k is a number
                            x_k = True  # x√k, where k is a number
                            y_x = True  # y√x
                            _x = True   # √x 

                            mult = True # multiplication
                            div = True  # division
                            add = True  # addition

                            # SIMP13: subtract coefficients between terms with no exponents

                            # case: a * x - b * x => (a-b) * x
                            if c - 2 > -1 and c + 4 < length and test_term_ends(c - 2, c + 4, arrVar) and arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):

                                # get term data
                                coefficient1 = arrVar[c - 2]
                                coefficient2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure(['%s' % subtract(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                
                                # end current simplification
                                break

                            # case: a * x - x => (a - 1) * x, where a is a particular value
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c + 2] == var and arrVar[c - 1] == operation["multiplication"] and not var_test(arrVar[c - 2]):
                                    
                                # get term data
                                coefficient = arrVar[c - 2]

                                # apply simplification to problem structure
                                arrVar = restructure([str(int(coefficient) - 1), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                            
                            # case: x - a * x => (1 - a) * x, where a is a particular value
                            elif c + 4 < length and test_term_ends(c, c + 4, arrVar) and arrVar[c + 4] == var and arrVar[c + 3] == operation["multiplication"] and not var_test(arrVar[c + 2]):

                                # get term data
                                coefficient = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure([str(1 - int(coefficient)), operation["multiplication"], var], c, c + 4, arrVar)

                                # end current simplification
                                break

                            # SIMP15: a + x - b => x+(a-b)
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["addition"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                    
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]

                                # apply simplification to problem structure
                                arrVar = restructure([var, operation["addition"], '%s' % subtract(val1, val2)], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                            
                            # SIMP16: a - x - b => (-x)+(a-b)
                            elif c - 2 > -1 and test_term_ends(c - 2, c + 2, arrVar) and arrVar[c - 1] == operation["subtraction"] and not var_test(arrVar[c - 2]) and not var_test(arrVar[c + 2]):
                                        
                                # get term data
                                val1 = arrVar[c - 2]
                                val2 = arrVar[c + 2]
                                var = operation["negation"]

                                # apply simplification to problem structure
                                arrVar = restructure([var, operation["addition"], '%s' % subtract(val1, val2)], c - 2, c + 2, arrVar)

                                # end current simplification
                                break
                        
                            # SIMP14: subtracted from itself
                            elif arrVar[c + 2] == var and operate(c + 1, arrVar) == True:
                            
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
                            
                            else:
                                sub = False
                            
                        else:
                            # terminate while loop
                            simplifiable = False

                    
                    # if simplifiable, keep simplifying
                    # a.k.a. restart iteration on simplified problem
                    if simplifiable == True:
                        break # prevents testing of terminating condition
                    
                # test terminating condition
                if c + 1 == length:
                    # no further simplifications; on end character and no simplifications run
                    simplifying = False

        # log end of simplification
        log_process("Simplification Complete")

        # re-standardize simplified expression
        if destandardized == True:
            log_process("Standards Broken by Simplification")
            arrVar = standardize_form(arrVar)
        
        # calculate arithmetic
        if recalculate == True:
            arrVar = calculate(arrVar)

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
                        elif str == operation["radication"] and i + 1 < length and not var_test(arr[i + 1]):
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

            # performs all polynomial expansions
            ref = getIdx("expand", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                # get arguments
                nomials = arrVar[ref + 1]
                nomials_len = len(nomials)

                # Log keyword
                log_process(arrVar[ref])
                log_process(nomials)

                if nomials_len == 0:
                    global_bypass == True
                    return "expand key function requires at least 1 argument"

                elif nomials_len == 1:
                    # cannot expand a single nomial or no nomial

                    # Log keyword
                    log_process(arrVar[ref])
                    # standardize/simplify
                    nomials = simplify(nomials)
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
                        # simplify nomial
                        x = simplify(nomial)
                        # structure by terms
                        x = get_terms(x)
                        # concatenate with sect_struct
                        sect_struct += get_terms(x)

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
                                        # negate variable
                                        y[0]
                                        op = operation["subtraction"]
                                        if len(y[0]) > 1 and y[0][0] == op:
                                            y[0] = y[0][1]
                                        else:
                                            y[0] = op + y[0]

                                # get product term

                                product += simplify(product_term(x, y))
                                product.append(operation["addition"])
                        
                            # update sect product with last product for next expansion
                            product.pop() #remove extra addition symbol
                            sect_product = get_terms(product)
                            product.append(operation["addition"])

                        expansion = []
                        for i in sect_product:
                            expansion += i
                            expansion += operation["addition"]
                        expansion.pop()
                        
                        expansion = simplify(expansion)

                        sect_product = get_terms(expansion)

                    # log_process(sect_product)

                    expansion = []
                    for i in sect_product:
                        expansion += i
                        expansion += operation["addition"]
                    expansion.pop()

                    expansion = simplify(expansion)
                    
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
            thresh += 1

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
                sect = osme[osme_length - 1 - i]["section"]

                log_process(sect)

                if len(sect) > 1:

                    # calculate and simplify section
                    sect = calculate(sect)

                    if global_bypass == True:
                        # section contains error message from calculation
                        return sect
                    else:
                        # test for variables in section
                        # if there are no variables, section should be the single value result of the arithmetic operations of the pre-calculated section
                        if isinstance(sect, list):

                            # handle parenthetical algebraic expressions

                            # identify expression operations (distributable operations)
                            # any case which does not remove the parenthesis should be excluded from expression operations
                            terms = get_terms(sect)
                            terms_len = len(terms)
                            parens_removed = False

                            if terms_len == 1: # single term expression

                                # exponentation (distributes accross multiplication; only single term expressions)
                                # case 1: ( x * y / z ) ^ a => x ^ a * y ^ a / z ^ a, where "a" is a value
                                # case 2: ( x * y / z ) ^ k => x ^ k * y ^ k / z ^ k, where "k" is a variable
                                # case 3: ( x * y ) ^ (a + b) => x ^ c * y ^ c, where "a" and "b" are values whose sum is "c"
                                # case 4 [EXCLUDE]: ( x * y ) ^ (a + z) => x ^ (a + z) * y ^ (a + z), where "a + z" is an algebraic expression

                                if end + 1 < len(arrVar) and arrVar[end] == operation["exponentiation"]:
                                    if arrVar[end + 1] == operation["open_parenthesis"]:

                                        nest = 0
                                        exp = []
                                        for i in range(end + 2, len(arrVar)):
                                            exp.append(arrVar[i])
                                            if var_test(arrVar[i]) == True:
                                                # case 4: unresolvable algebraic power expression
                                                global_bypass = True
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
                                        exp = section(exp) # watch for loops
                                        if global_bypass == True:
                                            # section contains error message from calculation
                                            return sect
                                        else:
                                            buffer = []
                                            result = []
                                            delimiter = operation["multiplication"]
                                            div = operation["division"]
                                            op = operation["exponentiation"]
                                            x = []
                                            for i in sect:
                                                buffer.append(i)
                                                if i == delimiter:
                                                    result.append(buffer)
                                                    buffer = []
                                            if len(buffer) > 0:
                                                result.append(buffer)

                                            for i in result:
                                                if i[0] == div:
                                                    x.pop() # remove multiplication
                                                    x.append(div) # replace with division
                                                else:
                                                    x += i
                                                    x.append(op)
                                                    x.append(exp)
                                                    x.append(delimiter)
                                            x.pop()

                                            parens_removed = True
                                            arrVar = restructure(x, start, end, arrVar)
                                        
                                    else:

                                        # power value
                                        # case 1 + 2
                                        exp = arrVar[end + 1]
                                        end += 1
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        div = operation["division"]
                                        op = operation["exponentiation"]
                                        x = []

                                        for i in sect:
                                            buffer.append(i)
                                            if i == delimiter:
                                                buffer.pop()
                                                result.append(buffer)
                                                buffer = []
                                            elif i == div:
                                                buffer.pop()
                                                result.append(buffer)
                                                buffer = []
                                                result.append([div])

                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        for i in result:
                                            if i[0] == div:
                                                x.pop() # remove multiplication
                                                x.append(div) # replace with division
                                            else:
                                                x += i
                                                x.append(op)
                                                x.append(exp)
                                                x.append(delimiter)
                                        x.pop()

                                        parens_removed = True
                                        arrVar = restructure(x, start, end, arrVar)

                                # radication (distributes across multiplication and division; only single term expressions)
                                # case 1: √ ( x * y / z ) => √ x * √ y / √ z
                                # case 2: a √ ( x * y / z ) => a √ x * a √ y / a √ , where "a" is a number
                                # case 3: k √ ( x * y / z ) => k √ x * k √ y / k √ z, where "k" is a variable
                                # case 4: (a + b) √ ( x * y / z ) => c √ x * c √ y / c √ z, where a + b = c
                                # case 5 [EXCLUDE]: (a + k) √ ( x * y ) => (a + k) √ x * (a + k) √ y, where a + k is an unresolvable algebraic expression
                                
                                elif start - 1 > -1 and arrVar[start - 1] == operation["radication"]:
                                    if start - 2 > -1 and arrVar[start - 2] == operation["open_parenthesis"]:

                                        nest = 0
                                        exp = []
                                        for i in range(-1, start - 2, -1):
                                            exp.insert(0, arrVar[i])
                                            if var_test(arrVar[i]) == True:
                                                # case 5: algebraic expression radical
                                                global_bypass = True
                                                return arrVar
                                            if arrVar[i] == operation["open_parenthesis"]:
                                                nest += 1
                                            elif arrVar[i] == operation["close_parenthesis"]:
                                                nest -= 1
                                                if nest == 0:
                                                    # extend range of section
                                                    start = i
                                                    break
                                        
                                        # case 4: expression radical
                                        exp = section(exp) # watch for loops
                                        if global_bypass == True:
                                            # section contains error message from calculation
                                            return sect
                                        else:
                                            buffer = []
                                            result = []
                                            delimiter = operation["multiplication"]
                                            div = operation["division"]
                                            op = operation["radication"]
                                            x = []
                                            for i in sect:
                                                buffer.append(i)
                                                if i == delimiter:
                                                    result.append(buffer)
                                                    buffer = []
                                            if len(buffer) > 0:
                                                result.append(buffer)
                                            
                                            for i in result:
                                                if i[0] == div:
                                                    x.pop() # remove multiplication
                                                    x.append(div) # replace with division
                                                else:
                                                    x.append(op)
                                                    x += i
                                                    x.append(delimiter)
                                            x.pop()

                                            parens_removed = True
                                            arrVar = restructure(x, start, end, arrVar)

                                    elif start - 2 > -1 and not op_test(arrVar[start - 2]):
                                        # case 2: numerical radical
                                        # case 3: variable radical
                                        start -= 2
                                        exp = arrVar[start]
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        div = operation["division"]
                                        op = operation["radication"]
                                        op2 = operation["exponentiation"]
                                        sect_len = len(sect)
                                        x = []
                                        for i in range(sect_len):
                                            if sect[i] == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                            elif var_test(sect[i]) == True:
                                                # ommit variable that are exponents and radicals
                                                use = True
                                                if i - 1 > -1 and sect[i - 1] == op2 or i + 1 < sect_len and sect[i + 1] == op:
                                                    # e.g. 2^x or n√3
                                                    use = False
                                                if use == True:
                                                    buffer.append(exp)
                                                    buffer.append(op)
                                                    buffer.append(sect[i])
                                                else:
                                                    buffer.append(sect[i])
                                            else:
                                                buffer.append(sect[i])

                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        for i in result:
                                            if i[0] == div:
                                                x.pop() # remove multiplication
                                                x.append(div) # replace with division
                                            else:
                                                x += i
                                                x.append(delimiter)
                                        x.pop()

                                        parens_removed = True
                                        arrVar = restructure(x, start, end, arrVar)

                                    else:
                                        # case 1: square root
                                        start -= 1
                                        buffer = []
                                        result = []
                                        delimiter = operation["multiplication"]
                                        div = operation["division"]
                                        op = operation["radication"]
                                        op2 = operation["exponentiation"]
                                        sect_len = len(sect)
                                        x = []
                                        for i in range(sect_len):
                                            if sect[i] == delimiter:
                                                result.append(buffer)
                                                buffer = []
                                            elif var_test(sect[i]) == True:
                                                # ommit variable that are exponents and radicals
                                                use = True
                                                if i - 1 > -1 and sect[i - 1] == op2 or i + 1 < sect_len and sect[i + 1] == op:
                                                    # e.g. 2^x or n√3
                                                    use = False
                                                if use == True:
                                                    buffer.append(op)
                                                    buffer.append(sect[i])
                                                else:
                                                    buffer.append(sect[i])
                                            else:
                                                buffer.append(sect[i])

                                        if len(buffer) > 0:
                                            result.append(buffer)

                                        for i in result:
                                            if i[0] == div:
                                                x.pop() # remove multiplication
                                                x.append(div) # replace with division
                                            else:
                                                x += i
                                                x.append(delimiter)
                                        x.pop()

                                        parens_removed = True
                                        arrVar = restructure(x, start, end, arrVar)

                            elif terms_len > 1: # multiple term expression
                                
                                # multiplication (distributes across addition and subtraction; single and multiple term expressions)
                                
                                # case 1: a * ( x + y - z) => a * x + a * y - a * z
                                if start - 2 > -1 and arrVar[start - 1] == operation["multiplication"] and arrVar[start - 2] != operation["close_parenthesis"]:
                                    
                                    x = []
                                    multiplier = arrVar[start - 2]
                                    op1 = operation["addition"]
                                    op2 = operation["subtraction"]
                                    op3 = operation["multiplication"]
                                    for t in terms:
                                        if t[0] == subtract_key:
                                            x.append(op2)
                                            x.append(multiplier)
                                            x.append(op3)
                                            t.pop(0)
                                            x += t

                                        else:
                                            x.append(op1)
                                            x.append(multiplier)
                                            x.append(op3)
                                            x += t

                                    if x[0] == op1:
                                        # remove extra addition at start
                                        x.pop(0)
                                    elif x[0] == op2:
                                        # handle negation of first term
                                        x.pop(0) # remove subtraction sign
                                        if var_test(x[2]) == True:
                                            # add coefficient to term
                                            x.insert(0, op3)
                                            x.insert(0, '%s1' % op2)
                                        else:
                                            # negate term coefficient
                                            coef = -x[0]
                                            x.pop(0)
                                            x.insert(0, coef)
                                    parens_removed = True
                                    start -= 2
                                    arrVar = restructure(x, start, end - 1, arrVar)

                                # case 2: ( x + y ) * a => a * x + a * y 
                                elif end + 1 < len(arrVar) and arrVar[end] == operation["multiplication"] and arrVar[end + 1] != operation["close_parenthesis"]:
                                    
                                    x = []
                                    multiplier = arrVar[end + 1]
                                    op1 = operation["addition"]
                                    op2 = operation["subtraction"]
                                    op3 = operation["multiplication"]
                                    for t in terms:
                                        if t[0] == subtract_key:
                                            x.append(op2)
                                            x.append(multiplier)
                                            x.append(op3)
                                            t.pop(0)
                                            x += t

                                        else:
                                            x.append(op1)
                                            x.append(multiplier)
                                            x.append(op3)
                                            x += t
                                            
                                    if x[0] == op1:
                                        # remove extra addition at start
                                        x.pop(0)
                                    elif x[0] == op2:
                                        # handle negation of first term
                                        x.pop(0) # remove subtraction sign
                                        if var_test(x[2]) == True:
                                            # add coefficient to term
                                            x.insert(0, op3)
                                            x.insert(0, '%s1' % op2)
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
                                x = [operation["open_parenthesis"]] + sect + [operation["close_parenthesis"]]
                                arrVar = restructure(x, start, end - 1, arrVar)
                                global_bypass = True
                                return arrVar

                        else:
                            # update arrVar with non-algebraic solution
                            arrVar = restructure(sect, start, end - 1, arrVar)
                else:
                    # update arrVar with calculations and simplifications
                    arrVar = restructure(sect, start, end - 1, arrVar)
            
        
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
            negative = False
            for i in range(0, len(str)):
                if str[i] == " ":
                    continue
                else:
                    try:
                        #  decimals or variables while negative is true or numeral strings
                        str[i] == "." or negative == True and var_test(str[i]) == True or int(str[i])
                    except:
                        # handle negatives
                        if str[i] == "-" and str[i - 1] == "(":
                            structure.pop()
                            digits = "%s" % str[i]
                            negative = True
                        elif str[i] == ")" and negative == True:
                            if len(digits) > 0:
                                structure.append(digits)
                                digits = ""
                            negative = False
                        else:
                            if len(digits) > 0:
                                structure.append(digits)
                            digits = ""
                            structure.append(str[i])
                    else:
                        # add to buffer if try block is true
                        digits = digits + "%s" % str[i]
                    finally:
                        # test after everything in each iteration
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
            
            # structure tau
            ref = get_word("tau", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.pi/2, ref["first"], ref["last"] - 1, structure)
                ref = get_word("tau", structure)
            
            # structure phi
            ref = get_word("phi", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(1.61803398874989484820, ref["first"], ref["last"] - 1, structure)
                ref = get_word("phi", structure)
            
            # structure euler's number
            ref = get_word("euler", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.e, ref["first"], ref["last"] - 1, structure)
                ref = get_word("euler", structure)
            
            # structure euler's constant (gamma)
            ref = get_word("gamma", structure)
            itr = 0
            while itr < const_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.euler_gamma, ref["first"], ref["last"] - 1, structure)
                ref = get_word("gamma", structure)

            # structure keywords
            log_process("Structuring Keywords")
            
            # structure key functions
            for module in range(0, len(info["key_functions"])):
                for i in range(0, len(info["key_functions"][module])):
                    structure = word_struct(info["key_functions"][module][i]["key"], structure, module)

            log_process(key_modules)

            # Identify program entities in problem structure
            err = identify_entities(structure)
            if len(err) > 0:
                return err

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
            test7 = True
            key_error = ""
            structure_length = len(structure)

            # TEST6: Zero Division

            for i in range(0, structure_length):
                if i + 1 < structure_length and structure[i] == operation["division"] and structure[i + 1] == "0":
                    test6 = False
                    break

            # TEST5: consecutive operations / TEST7: no operands (number, variable, expression, set) for operation

            if test6 == True:

                # test ends of structure for operation
                s_start = structure[0]
                s_end = structure[structure_length - 1]
                if op_test(s_end) and s_end != operation["close_parenthesis"] and s_end != operation["close_bracket"]:
                    # operation at end of structure
                    test7 = False
                elif op_test(s_start) and s_start != operation["radication"] and s_start != operation["open_parenthesis"] and s_start != operation["open_bracket"]:
                    # operation at start of structure
                    test7 = False
                if test7 == True:
                    for i in range(0, structure_length):
                        # each index in problem structure
                        if i + 1 < structure_length:
                            s1 = structure[i]
                            s2 = structure[i + 1]
                            first = op_test(s1) and s1 != operation["open_parenthesis"] and s1 != operation["close_parenthesis"] and s1 != operation["open_bracket"] and s1 != operation["close_bracket"]
                            second = op_test(s2) and s2 != operation["open_parenthesis"] and s2 != operation["close_parenthesis"] and s2 != operation["open_bracket"] and s2 != operation["close_bracket"]
                            
                            if s2 != operation["radication"]:
                                if first == True and second == True:
                                    # consecutive operations
                                    test5 = False
                                    break
                                elif first == True and s1 != operation["radication"] and i - 1 > -1:
                                    s0 = structure[i - 1]
                                    if isinstance(num_cast(s0), bool) and var_test(s0) == False and s0 != operation["close_parenthesis"] and s0 != operation["close_bracket"] or isinstance(num_cast(s2), bool) and var_test(s2) == False and s2 != operation["open_parenthesis"] and s2 != operation["open_bracket"]:
                                        # missing operands (number, variable, expression, set) for operation
                                        test7 = False
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
            elif test7 == False:
                # no operands for operation => terminate program
                return "operations require operands"
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
    else:
        # prevent unnecessary decimal
        try:
            int(answer)
            answer = num_cast(answer)
        except:
            log_process("ERROR: %s" % answer)

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
#     # "problem": "2*((x*y)^2)", # note: expression operation exponentiation case 1
#     # "problem": "", # note: 
#     "use_logs": "1", # 1 = yes, else = no 
#     "problem": "√4", # note: 
#     # "problem": "n√b*3√a", # note: 
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
#     {"problem": "1+A/27", "answer": "Invalid character: A"}, # no captial letters

#     # PROBLEM STRUCTURE VALIDATION

#     # TEST0.1
#     {"problem": "1+q", "answer": "non-entity detected: q"}, # formatting error for valid characters but no semantic meaning

#     # TEST6
#     {"problem": "1/0", "answer": "no division by zero"}, # prevents zero division before calculation
#     {"problem": "3/(2-2)", "answer": "no division by zero"}, # prevents zero division during calculation

#     # TEST5
#     {"problem": "1++1", "answer": "no consecutive operations"},
#     {"problem": "1+-1", "answer": "no consecutive operations"}, # different operations
#     {"problem": "2*√16", "answer": "8"}, # except for second operation being √
#     {"problem": "1√*16", "answer": "no consecutive operations"}, # including for first operation being √
#     {"problem": "-1*2", "answer": "operations require operands"}, # prevent operations without operands

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
#     {"problem": "2+3-xy", "answer": "no consecutive variables"}, # prevents program from evaluating problem structure if the problem structure has consecutive variables

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
#     {"problem": "mean[4,[4+4]]", "answer": "6"}, # as it should be; gets 6

#     {"problem": "sd[[mean[0,0]],1]", "answer": "0.5"}, # validation works for key function composition; gets 0.5

#     {"problem": "mean[10]", "answer": "mean key has insufficient arguments"}, # prevents program from evaluating problem structure if insufficient arguments for key function
#     {"problem": "meanw[[10,0.5]]", "answer": "meanw key has insufficient arguments"}, # prevents program from evaluating problem structure if insufficient arguments for key function with expression arguments
    
#     {"problem": "sin(1,[2*8/4-2])", "answer": "sin key only accepts a single argument"}, # prevents mutiple arguments into single argument key function permitting expression arguments
    
#     # CONSTANTS

#     {"problem": "pi", "answer": "3.141592653589793"}, # pi
#     {"problem": "tau", "answer": "1.5707963267948966"}, # half pi
#     {"problem": "phi", "answer": "1.618033988749895"}, # Golden Ratio
#     {"problem": "euler", "answer": "2.718281828459045"}, # Euler's Number ; base e
#     {"problem": "gamma", "answer": "0.5772156649015329"}, # Euler's Constant ; Gamma Function

#     # ARITHMETIC
    
#     {"problem": "2^2", "answer": "4"}, # exponentiation
#     {"problem": "√16", "answer": "4"}, # radication
#     {"problem": "2*3", "answer": "6"}, # multplication
#     {"problem": "12/2", "answer": "6"}, # division
#     {"problem": "1+1", "answer": "2"}, # addition
#     {"problem": "1-1", "answer": "0"}, # subtraction

#     {"problem": "2^1√4*2/2+1-2", "answer": "1"}, # operator precedence is enforced

#     {"problem": "√4", "answer": "2"}, # implicit square root for radication without radical
#     {"problem": "3√8", "answer": "2"}, # performs nth roots where n = given radical

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

    
#     # KEY FUNCTION LOGIC TESTS
    
#     # TRIGONOMIC
#     {"problem": "acsc(csc(1))", "answer": "1"}, # pass = 1
#     {"problem": "asec(sec(1))", "answer": "1"}, # pass = 1
#     {"problem": "acot(cot(1))", "answer": "1"}, # pass = 1

#     {"problem": "asinh(sinh(1))", "answer": "1"}, # pass = 1
#     {"problem": "acosh(cosh(1))", "answer": "1"}, # pass = 1
#     {"problem": "atanh(tanh(1))", "answer": "1"}, # pass = 1

#     {"problem": "asin(sin(1))", "answer": "1"}, # pass = 1
#     {"problem": "acos(cos(1))", "answer": "1"}, # pass = 1
#     {"problem": "atan(tan(1))", "answer": "1"}, # pass = 1

#     # GEOMTERIC
#     {"problem": "hypot[3,4]", "answer": "5"}, # pass = 5
#     {"problem": "heron[3,4,5]", "answer": "6"}, # pass = 6

#     # COMBINATORIC
#     {"problem": "fact(5)", "answer": "120"}, # pass = 120
#     {"problem": "perm[3,2]", "answer": "6"}, # pass = 6
#     {"problem": "comb[3,2]", "answer": "3"}, # pass = 3

#     # STATISTICAL
#     {"problem": "sd[0,2]", "answer": "1"}, # pass = 1
#     {"problem": "var[0,2]", "answer": "1"}, # pass = 1
#     {"problem": "meanh[2,2]", "answer": "2"}, # pass = 2
#     {"problem": "meang[1,4]", "answer": "2"}, # pass = 2
#     {"problem": "meanw[[1,3],[5,1]]", "answer": "2"}, # pass = 2
#     {"problem": "mean[1,3]", "answer": "2"}, # pass = 2
#     {"problem": "rms[2,3]", "answer": "2.5495097567963922"}, # pass = 2.5495097567963922

#     {"problem": "gcf[10,15]", "answer": "5"}, # pass = 5
#     {"problem": "lcm[7,2]", "answer": "14"}, # pass = 14

#     {"problem": "log[10,10]", "answer": "1"}, # pass = 1
#     {"problem": "ln(1)", "answer": "0"}, # pass = 0

#     # KEY FUNCTION COMPOSITION TEST
#     {"problem": "sd[[sin(0)],[cos(0)]]", "answer": "0.5"}, # should get 0.5; key functions can run as arguments to other key functions for key function composition

#     # ALGEBRAIC FORMAT STANDARDIZATION

#     {"problem": "2-3*x", "answer": "-3*x+2"}, # prevents operation out of precedence in algebraic expressions using getidx function
#     {"problem": "x^2-3*y", "answer": "x^2-3*y"}, # prevents operation out of precedence in algebraic expressions using getidx function
#     {"problem": "2*y^2*3*x/b*a-5", "answer": "6*x*y^2/a*b-5"}, # standardizes terms: coefficient at start of divisional section + alphabetized variables + preserves subtraction of term
#     {"problem": "3+3*x-7-3*x^3", "answer": "-3*x^3+3*x-4"}, # standardizes expression: negates first term if subtracted + combines arithmetic terms into constant at end of expression
#     {"problem": "3*x^2-1+2*x^3", "answer": "2*x^3+3*x^2-1"}, # orders terms in decrimental order of term degree + prevent arithemetic on values operated on by higher precedence operators
#     {"problem": "a*x^3+a*x^2*y+a*x*y^2+a*y^3", "answer": "a*x^3+a*y^3+a*x^2*y+a*x*y^2"}, # (term indexes for coeficients) pascal's traingle expression format = 0, 1, 2, 3 => standard expression format = 0, 3, 1, 2; alternate from ends to center term assuming all term degrees from greatest to least are present
#     {"problem": "x*x+x*x*x", "answer": "x^3+x^2"}, # note: enure standards are enforced after simplification 

#     {"problem": "100/y*x/2/b*a/3", "answer": "100/x*y/2/a*b/3"}, # placeholders test 1

#     # VARIABLE EXPONENTS
#     {"problem": "2*a*2^x/b+1", "answer": "2*a*2^x/b+1"}, # variable exponents are handled
#     {"problem": "b+1/2^x*2*a", "answer": "b+1/2*a*2^x"}, # variable exponents are handled

#     # COMBINATION OF LIKE TERMS
#     {"problem": "x*x+x*x*x+x*y+3*x*x*x", "answer": "4*x^3+x^2+x*y"}, # note: 
#     {"problem": "4*x^2+a^4*y-3*x^2+a^4*y", "answer": "2*a^4*y+x^2"}, # removes 1 coefficients + handles multiple lists of like terms
#     {"problem": "c*a^2/a*2+a*c*a/2*a", "answer": "2*a^2*c/2*a"}, # combines like terms with multiple divisional sections

#     # REMOVE TERMS WITH ZERO COEFFICIENT + REMOVE COEFFICIENT OF 1
#     {"problem": "(2-1)*x+3*y", "answer": "x+3*y"}, # remove 1 coefficient
#     {"problem": "(1-1)*x+3*y", "answer": "3*y"}, # remove term with zero coefficient

#     # TRANSFER NEGATIVITY FROM VARIABLE TO COEFFICIENT TO OPERATION
#     {"problem": "x-(-y)", "answer": "x+y"}, # var => op ; - => - : +
#     {"problem": "x-y", "answer": "x-y"}, # var => op ; + => - : -
#     {"problem": "x+(-y)", "answer": "x-y"}, # var => op ; - => + : -
#     {"problem": "x+y", "answer": "x+y"}, # var => op ; + => + : +

#     {"problem": "x-(-2)*(-y)", "answer": "x-2*y"}, # var => coef => op ; - => - => - : -
#     {"problem": "x-(-2)*y", "answer": "x+2*y"}, # var => coef => op ; + => - => - : +
#     {"problem": "x-2*(-y)", "answer": "x+2*y"}, # var => coef => op ; - => + => - : +
#     {"problem": "x-2*y", "answer": "x-2*y"}, # var => coef => op ; + => + => - : -
    
#     {"problem": "x+(-2)*(-y)", "answer": "x+2*y"}, # var => coef => op ; - => - => + : +
#     {"problem": "x+(-2)*y", "answer": "x-2*y"}, # var => coef => op ; + => - => + : -
#     {"problem": "x+2*(-y)", "answer": "x-2*y"}, # var => coef => op ; - => + => + : -
#     {"problem": "x+2*y", "answer": "x+2*y"}, # var => coef => op ; + => + => + : +

#     # ALGEBRAIC SIMPLIFICATION

#     {"problem": "a+a+a-2*3", "answer": "3*a-6"}, # solve arithmetic in algebraic expression even if not in parens

#     # x^y
#     # x^y case 1: x*x^y => x^(y+1), index = 2nd x
#     {"problem": "x*x^y", "answer": "x^(y+1)"}, # 
#     # x^y case 2: x^y*x => x^(y+1), index = 1st x
#     {"problem": "x^y*x", "answer": "x^(y+1)"}, # 
#     # x^y case 3: x^y * x^i
#     {"problem": "x^y*x^2", "answer": "x^(y+2)"}, # 
#     # x^y case 4: x/x^y => x^(1-y), index = 2nd x
#     {"problem": "x/x^y", "answer": "x^(1-y)"}, # 
#     # x^y case 5: x^y/x => x^(y-1), index = 1st x
#     {"problem": "x^y/x", "answer": "x^(y-1)"}, # 
#     # x^y case 6: x^y / x^i => x^(y-i)
#     {"problem": "x^y/x^2", "answer": "x^(y-2)"}, # 

#     # x^i
#     # x^i case 1: x*x^i => x^b, where b = i + 1, index = 2nd x
#     {"problem": "x*x^2", "answer": "x^3"}, # 
#     # x^i case 2: x/x^i => x^b, where b = 1 - i, index = 2nd x
#     {"problem": "x/x^2", "answer": "x^-1"}, # 
#     # x^i case 3: x^i*x => x^b, where b = i + 1, index = 1st x
#     {"problem": "x^2*x", "answer": "x^3"}, # 
#     # x^i case 4: x^i/x => x^b, where b = i - 1, index = 1st x
#     {"problem": "x^3/x", "answer": "x^2"}, # 
#     # x^i case 5: x^i * x^y => x^(y+i)
#     {"problem": "x^3*x^y", "answer": "x^(y+3)"}, # 

#     # i^x
#     # i^x case 1: i*i^x => i^(x+1)
#     {"problem": "2*2^x", "answer": "2^(x+1)"}, # 
#     # i^x case 2: i/i^x => i^(1-x)
#     {"problem": "2/2^x", "answer": "2^(1-x)"}, # 
#     # i^x case 3: i^x*i => i^(x+1)
#     {"problem": "2^x*2", "answer": "2^(x+1)"}, # 
#     # i^x case 4: i^x/i => i^(x-1)
#     {"problem": "2^x/2", "answer": "2^(x-1)"}, # 

#     # k√x
#     # k√x case 1: k√x^k = > x, operations cancel
#     {"problem": "3√x^3", "answer": "x"}, # 
    
#     # x√k
#     # x√k case 1: x√k^x => k, operations cancel
#     {"problem": "x√4^x", "answer": "4"}, # 

#     # y√x
#     # y√x case 1: x√y^x => y, operations cancel
#     {"problem": "x√y^x", "answer": "y"}, # 

#     # √x
#     # √x case 1: √x*√x => x, operations cancel
#     {"problem": "√x*√x", "answer": "x"}, # 
#     # √x case 2: √x^2 => x, operations cancel
#     {"problem": "√x^2", "answer": "x"}, # 


#     # RADICTION CANCELS OUT
#     {"problem": "x√y^x", "answer": "y"}, # x√y^x => y
#     {"problem": "x√3^x", "answer": "3"}, # x√a^x => a
#     {"problem": "3√x^3", "answer": "x"}, # a√x^a => x
#     {"problem": "√x^2", "answer": "x"}, # √x^2 => x

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
#     {"problem": "10-x+2", "answer": "-x+12"}, # a - x + b => (a+b) - x
#     {"problem": "2*x+4*x", "answer": "6*x"}, # add coefficients of like terms
#     {"problem": "2*x+4*y", "answer": "2*x+4*y"}, # don't add coefficients of not like terms
#     {"problem": "3*x+x", "answer": "4*x"}, # combine terms one variable with coefficients added
#     {"problem": "x+3*x", "answer": "4*x"}, # combine terms one variable with coefficients added
    
#     {"problem": "a-a-a-a", "answer": "-2*a"}, # simplifies algebraic expression for consecutive substractions
#     {"problem": "10+x-2", "answer": "x+8"}, # a + x - b => (a-b) + x
#     {"problem": "10-x-2", "answer": "-x+8"}, # a - x - b => (a-b) - x
#     {"problem": "8*x-3*x", "answer": "5*x"}, # subtract coefficients of like terms
#     {"problem": "8*x-3*y", "answer": "8*x-3*y"}, # don't subtract coefficients of not like terms
#     {"problem": "3*x-x", "answer": "2*x"}, # combine terms one variable with coefficients subtracted
#     {"problem": "x-3*x", "answer": "-2*x"}, # combine terms one variable with coefficients subtracted
#     {"problem": "3*x-x", "answer": "2*x"}, # a * x - x => (a - 1) * x
#     {"problem": "x-3*x", "answer": "-2*x"}, # x - a * x => (1 - a) * x

#     # EXPRESSION OPERATIONS (distributable operations on algebraic expressions)

#     # unresolvable
#     {"problem": "(x-1*6/2)+2", "answer": "(x-3)+2"}, # solves up until unresolvable algebraic parenthetical section
#     {"problem": "(x+1)+2", "answer": "(x+1)+2"}, # prevents calculation on unresolvable algebraic expressions
#     {"problem": "(x)+2", "answer": "x+2"}, # should get "x+2"; removes parenthesis on variables wrapped with no operations

#     {"problem": "2^((4+8)+x)", "answer": "2^(x+12)"}, # handle unresolvable algebraic parenthetical sections
#     {"problem": "((4+8)+x)^2", "answer": "(x+12)^2"}, # handle unresolvable algebraic parenthetical sections
#     {"problem": "√(x*y+z)", "answer": "√(x*y+z)"}, # handle unresolvable algebraic parenthetical sections
#     {"problem": "(x+10)√9", "answer": "(x+10)√9"}, # handle unresolvable algebraic parenthetical sections

#     # exponentiation
#     {"problem": "(x*y/z)^2", "answer": "x^2*y^2/z^2"}, # able to remove last parenthesis by distributing exponentiation across multiplication
#     {"problem": "(x*y/z)^a", "answer": "x^a*y^a/z^a"}, # able to remove last parenthesis by distributing exponentiation across multiplication
    
#     # radication
#     {"problem": "√(x*y/z)", "answer": "√x*√y/√z"}, # able to remove last parenthesis by distributing radication across multiplication
#     {"problem": "3√(x*y/z)", "answer": "3√x*3√y/3√z"}, # able to remove last parenthesis by distributing radication across multiplication
#     {"problem": "n√(x*y/z)", "answer": "n√x*n√y/n√z"}, # able to remove last parenthesis by distributing radication across multiplication
#     {"problem": "(x/x+1)√4", "answer": "2"}, # able to simplify radical and produce result of radication
    
#     # multiplication
#     {"problem": "2*((4+8)+x)", "answer": "2*x+24"}, # able to remove last parenthesis by distributing 2 from before section
#     {"problem": "((4+8)+x)*2", "answer": "2*x+24"}, # able to remove last parenthesis by distributing 2 from after section
#     {"problem": "2*((4+8)-x)", "answer": "-2*x+24"}, # able to remove last parenthesis by distributing 2 from before section
#     {"problem": "((4-16)+x)*2", "answer": "2*x-24"}, # able to remove last parenthesis by distributing 2 from after section

#     # ALGEBRAIC KEY FUNCTION ARGUMENT DOMAIN VALIDATION

#     # ALGEBRAIC KEY FUNCTIONS
#     {"problem": "algexp[[x+y],[2*1/1+1]]", "answer": "(x+y)*(x+y)*(x+y)"}, # algebraic exponentiation

#     {"problem": "expand[[x],[x]]", "answer": "x^2"}, # 
#     {"problem": "expand[[x],[x],[x]]", "answer": "x^3"}, # 
#     {"problem": "expand[[a],[b-c],[x+y+z]]", "answer": "a*b*x+a*b*y+a*b*z-a*c*x-a*c*y-a*c*z"}, # polynomial expansion
    
#     # algebraic identities

#     # square of binomial
#     {"problem": "expand[[x+y],[x+y]]", "answer": "x^2+y^2+2*x*y"}, # (x+y)^2 = X^2+y^2+2*x*y
#     {"problem": "expand[[x-y],[x-y]]", "answer": "x^2+y^2-2*x*y"}, # (x-y)^2 = X^2+y^2-2*x*y
#     # cube of binomial
#     {"problem": "expand[[x+y],[x+y],[x+y]]", "answer": "x^3+y^3+3*x^2*y+3*x*y^2"}, # (x+y)^3 = x^3+y^3+3*x^2*y+3*x*y^2
#     {"problem": "expand[[x-y],[x-y],[x-y]]", "answer": "x^3-y^3-3*x^2*y+3*x*y^2"}, # (x-y)^3 = x^3-y^3-3*x^2*y+3*x*y^2
#     # sum of sqaures
#     {"problem": "expand[[x+y],[x+y]]-2*x*y", "answer": "x^2+y^2"}, # (x+y)^2-2*x*y = x^2+y^2
#     {"problem": "expand[[x-y],[x-y]]+2*x*y", "answer": "x^2+y^2"}, # (x-y)^2+2*x*y = x^2+y^2
#     # diference of squares
#     {"problem": "expand[[x+y],[x-y]]", "answer": "x^2-y^2"}, # (x+y)*(x-y) = x^2-y^2
#     # sum of cubes
#     {"problem": "expand[[x+y],[x^2+y^2-x*y]]", "answer": "x^3+y^3"}, # (x+y)*(x^2+y^2-x*y) = x^3+y^3
#     # difference of cubes
#     {"problem": "expand[[x-y],[x^2+y^2+x*y]]", "answer": "x^3-y^3"}, # (x-y)*(x^2+y^2+x*y) = x^3-y^3

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
