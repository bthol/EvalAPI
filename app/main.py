# Dependencies
import math
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()

# PROGRAMIC PROCESS

# Phase I: Character Validation
# Description: Tests each character in problem string to ensure only valid characters are used, otherwise, the program terminates and returns "invalid character"

# Phase II: Entity Structuring and Analysis
# Description: Analyzes problem string to create structure from string data storing relevant problem data as it goes. The problem string is structured into entities including and limited to multi-digit numbers, negative numbers, decimal numbers, operations, parenthesis, sets and keywords. After structuring, the program analyzes the structure to further identify remaining program entities from structure data.

# Phase III: Structural Manipulation
# Description: Bypassed unless, as identified in Phase I, there are parenthesis, in which case the section function manipulates the structure to solve section by section.

# Phase IV: Key Functions
# Description: Bypassed unless, in one case, there are parenthesis and keywords, in which case search for and run key functions or, in another case, there are square brackets and keywords, in which case manipulate the structure to form sets and search for and run key functions (sets permit key functions to have multiple arguments).

# Phase V: Calculation/Simplification
# Description: Search for and run appropriate operations on contents of structure, restructure with solution, and repeat until no operations are remaining.

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

    "key_functions": [
        # Trigonomic Module
        [
            # Fundamental
            {"name":"Sine", "key": "sin", "syntax": "sin(x)", "about": "Gets the sine of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Sine", "key":"asin", "syntax": "asin(x)", "about": "Gets the arcus sine, i.e. the inverse sine, of x, where x is a value or an expression that evaluates to a value."},

            {"name":"Cosine", "key": "cos", "syntax": "cos(x)", "about": "Gets the cosine of x, where x is a value or an expression that evaluates to a value."},

            {"name":"Arcus Cosine", "key": "acos", "syntax": "acos(x)", "about": "Gets the arc cosine, i.e. the inverse of cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Tangent", "key":"tan", "syntax": "tan(x)", "about": "Gets the tangent of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Tangent", "key": "atan", "syntax": "atan(x)", "about": "Gets the arcus tangent, i.e. the inverse tangent, of x, where x is a value or an expression that evaluates to a value."},
                
            # Reciprocal
            {"name":"Cosecant", "key":"csc", "syntax": "csc(x)", "about": "Gets the cosecant, i.e. the reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Cosecant", "key":"acsc", "syntax": "acsc(x)", "about": "Gets the arcus cosecant, i.e. the inverse reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Secant", "key":"sec", "syntax": "sec(x)", "about": "Gets the secant, i.e. the reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Secant", "key":"asec", "syntax": "asec(x)", "about": "Gets the arcus secant, i.e. the inverse reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Cotangent", "key":"cot", "syntax": "cot(x)", "about": "Gets the cotangent, i.e. the reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Cotangent", "key":"acot", "syntax": "acot(x)", "about": "Gets the arcus cotangent, i.e. the inverse reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},

            # Hyperbolic
            {"name":"Hyperbolic Sine", "key":"sinh", "syntax": "sinh(x)", "about": "Gets the hyperbolic sine, i.e the sine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Hyperbolic Sine", "key":"asinh", "syntax": "asinh(x)", "about": "Gets the arcus hyperbolic sine, i.e the inverse sine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Hyperbolic Cosine", "key":"cosh", "syntax": "cosh(x)", "about": "Gets the hyperbolic cosine, i.e the cosine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Hyperbolic Cosine", "key":"acosh", "syntax": "acosh(x)", "about": "Gets the arcus hyperbolic cosine, i.e the inverse cosine of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Hyperbolic Tangent", "key":"tanh", "syntax": "tanh(x)", "about": "Gets the hyperbolic tangent, i.e the tangent of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
            
            {"name":"Arcus Hyperbolic Tangent", "key":"atanh", "syntax": "atanh(x)", "about": "Gets the arcus hyperbolic tangent, i.e the inverse tangent of hyperbola instead of circle, of x, where x is a value or an expression that evaluates to a value."},
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

            {"name":"Root Mean Square", "key":"rms", "syntax": "rms[a1,a2]", "about": "Gets the geometeric mean of the the set of items within square brackets, where that set has at least two comma-demarcated items, and each item is a value or an expression that evaulates to a value wrapped within square brackets, e.g. rms[10,[2+3]]."},
                
            # Et Cetera
            {"name":"Greatest Common Factor", "key":"gcf", "syntax": "gcf[a,b]", "about": "Gets the greatest common factor of a and b within square brackets, where a and b are values or expressions that evaluate to values wrapped in square brackets, e.g. gcf[a,[b+x]]."},

            {"name":"Least Common Multiple", "key":"lcm", "syntax": "lcm[a,b]", "about": "Gets the least common multiple of values a and b within square brackets, where a and b are values or expressions that evaluate to values wrapped in square brackets, e.g. lcm[a,[b+x]]."},
            
            {"name":"Logarithm", "key":"log", "syntax": "log[x,b]", "about": "Gets the logarithm of x with base b, where x and b are values or an expression wrapped in square brackets that evaluates to a value."},

            {"name":"Natural Log", "key":"ln", "syntax": "ln(x)", "about": "Gets the natural log of x with base e, where x is a value or an expression wrapped in square brackets that evaluates to a value."},
        ],

        # Algebraic
        [
            {"name":"Algebraic Exponentiation", "key":"algexp", "syntax":"algexp[[a],x]", "about":"Gets an algebraic exponentiation given a polynomial expression a and power x, where x is a value or an arithmetic expression that evaluates to a positive integer value wrapped within square brackets, e.g. expand[[a],[x+y]]"},
            
            {"name":"Polynomial Expansion", "key":"expand", "syntax":"expand[[x+y][a+b]]", "about":"Gets a polynomial expansion given a list of at least 2 polynomial expressions x and y, where each expression may have a unique number of any number of terms, e.g. expand[[a][b+c][d+e+f]]"},
        
        # add:
        #  - combine like terms
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

    # the pi_limit parameter controls the maximum number of instances of any one constant allowed in any one evaluation
    c_limit = 10

    # the key_limit parameter controls the maximum number of the same key function allowed in any one evaluation
    key_limit = 10

    # PROGRAM ENTITY REFERENCE

    # variable characters (all lowercase letters except i for imaginary numbers)
    variables = "abcdefghjklmnopqrstuvwxyz"

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

    # represents a string containing all of the valid non-numeral characters
    valid_chars = "." + variables + operation["addition"] + operation["subtraction"] + operation["multiplication"] + operation["division"] + operation["exponentiation"] + operation["radication"] + operation["open_parenthesis"] + operation["close_parenthesis"] + operation["open_bracket"] + operation["close_bracket"]
    
    # algebraic_mode controls whether the program solves for an algebraic expression, True, or a single value, False
    algebraic_mode = False

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

    # key_modules structure represent which key functions modules should be run or bypassed on call
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
            process_log["%s" % new_key] = log
  
    # STRUCTURE START

    def num_cast(str):
        # a single data type converter for all your data type conversion needs!
        try:
            num = float(str)
            if (num / 1 % 1 == 0):
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
    
    def is_op(str):
        # tests if given str is an operation character
        for i in range(0, len(info["operations"])):
            if info["operations"][i]["syntax"] == str:
                return True
        return False

    def is_var(str):
        # test for variables
        for i in variables:
            if i == str:
                return True
        return False

    def identify_entities(arr):
        # identify program entities and update program entity reference
        nonlocal operation
        
        # Identify algebraic mode
        nonlocal algebraic_mode
        for i in arr:
            if is_var(i):
                algebraic_mode = True
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

    def exponentiate(base, exponent):
        base = float(base)
        if base / 1 % 1 == 0:
            base = int(base)

        exponent = float(exponent)
        if exponent / 1 % 1 == 0:
            exponent = int(exponent)

        power = math.pow(base, exponent)

        return power

    def root(radicand, degree):
        radicand = float(radicand)
        if radicand / 1 % 1 == 0:
            radicand = int(radicand)

        degree = float(degree)
        if degree / 1 % 1 == 0:
            degree = int(degree)

        root = math.pow(radicand, 1/degree)

        return root

    def multiply(multiplicand, multiplier):
        multiplicand = float(multiplicand)
        if multiplicand / 1 % 1 == 0:
            multiplicand = int(multiplicand)

        multiplier = float(multiplier)
        if multiplier / 1 % 1 == 0:
            multiplier = int(multiplier)

        product = multiplicand * multiplier

        return product

    def divide(dividend, divisor):
        dividend = float(dividend)
        if dividend / 1 % 1 == 0:
            dividend = int(dividend)

        divisor = float(divisor)
        if divisor / 1 % 1 == 0:
            divisor = int(divisor)

        quotient = dividend / divisor

        return quotient

    def add(augend, addend):
        augend = float(augend)
        if augend / 1 % 1 == 0:
            augend = int(augend)

        addend = float(addend)
        if addend / 1 % 1 == 0:
            addend = int(addend)

        total = augend + addend

        return total

    def subtract(minuend, subtrahend):
        minuend = float(minuend)
        if minuend / 1 % 1 == 0:
            minuend = int(minuend)

        subtrahend = float(subtrahend)
        if subtrahend / 1 % 1 == 0:
            subtrahend = int(subtrahend)

        difference = minuend - subtrahend

        return difference

    def factorial(x):
        y = 1
        for i in range(int(x), 1, -1):
            y = y * i
        return y

    def get_mean(arr):
        return sum(arr) / len(arr)

    # ARITHMETIC OPERATIONS END

    # ALGEBRAIC OPERATIONS START

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
            if arr[c1 - 1] == operation["addition"] or operation["subtraction"]:
                return True
        
        # test back end
        elif c2 + 1 < arr_len:
            if arr[c2 + 1] == operation["addition"] or arr[c2 + 1] == operation["subtraction"]:
                return True
        
        # no ends to test
        else:
            return True
        
        # no true condition reached
        return False

    def getTerms(arr):
        # identifies terms in algebraic expression and returns structured as such
        sect_struct = []
        term = []
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
                    term = []
            else:
                # compile term
                term.append(arr[i])
        
        # append last term
        sect_struct.append(term)

        return sect_struct
    
    def combineLikeTerms(arr):

        # combines like terms in algebraic and returns simplified expression
        nonlocal variables

        # identify terms
        sect_struct = getTerms(arr)

        # compare to test for like terms
        likeness = []

        # get variables + exponents for each term
        for term in sect_struct:
            # each term gets a "t object"
            t = {"variables": [], "exponent":""}

            for c in range(0, len(term)):
                # each character

                # test for exponents
                if term[c] == operation["exponentiation"]:
                    if c + 1 < len(term):
                        if term[c + 1] == operation["open_parenthesis"]:

                            # c + 1 is an expression

                            nest = 0
                            expression = []
                            # compile to expression until finding end parenthesis
                            for char in range(c + 1, len(term)):
                                # compile
                                expression.append(char)
                                # test for end parenthesis
                                if char == operation["open_parenthesis"]:
                                    nest += 1
                                elif char == operation["close_parenthesis"]:
                                    nest -= 1
                                    if nest == 0:
                                        # found end parenthesis
                                        t["exponent"] = expression
                                        break

                        else:

                            # c + 1 is a value

                            t["exponent"] = term[c + 1]

                    else:

                        # c + 1 is last character of term; is a value

                        t["exponent"] = term[c + 1]
                else:
                    # current character is not a exponentiation symbol

                    # test for variables
                    if is_var(term[c]):
                        t["variables"].append(term[c])


            # append t object to likeness
            likeness.append(t)
        
        # print(sect_struct)
        # print(likeness)
        
        return arr
    
    def simplify(arr):
        # log process label
        log_process("Simplifying")

        # simplifies algebraic expressions
        arrVar = arr

        # define process of simplification
        # 1.) identify first variable in arr testing from left to right
        # 2.) test for simplifications until one is discovered and run that
        # 3.) restart step 1 - 3 until no simplification are discovered during step 2
        
        simplifying = True
        x = 0
        while x < 10 and simplifying == True:
            # each while loop interation is one simplification
            x += 1
            
            # get length of arrVar
            length = len(arrVar)

            for c in range(0, length):
                # each character
                if is_var(arrVar[c]):
                    # each variable
                    var = arrVar[c]

                    # run simplifications

                    if c + 2 < length:
                        # is operation on current variable

                        # MULTIPLICATION
                        if arrVar[c + 1] == operation["multiplication"]:

                            # SIMP1: multiply a variable by itself

                            if arrVar[c + 2] == var:
                            
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
                            
                            if testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP2: a * x * b => (a*b) * x

                                if arrVar[c - 1] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(val1, val2), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break

                            # SIMP3: a / x * b => (a*b) / x

                                if arrVar[c - 1] == operation["division"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break

                            # SIMP4: combine terms for variable with coefficients multiplied

                            if testTermEnds(c - 2, c + 4, arrVar):
                                # correct term length for c index
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    # case: a * x * b * x => (a*b) * x ^ 2, where a and b are particular values

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % multiply(coefficient1, coefficient2), operation["multiplication"], var, operation["exponentiation"], "2"], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break
                        
                        # DIVISION            
                        elif arrVar[c + 1] == operation["division"]:

                            # SIMP5: divide a variable by itself

                            if arrVar[c + 2] == var:

                                # test if next operation after dividing by itself is another division by itself
                                if c + 4 < length and arrVar[c + 3] == operation["division"] and arrVar[c + 4] == var:
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

                            if testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP6: a * x / b => (a/b) * x

                                if arrVar[c - 1] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % divide(val1, val2), operation["multiplication"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break

                            # SIMP7: a / x / b => (a/b) / x

                                if arrVar[c - 1] == operation["division"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % divide(val1, val2), operation["division"], var], c - 2, c + 2, arrVar)
                                    
                                    # end current simplification
                                    break

                            # SIMP8: combine terms for variable with coefficients divided
                            if testTermEnds(c - 2, c + 4, arrVar):
                                # correct term length for c index
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    # case: a * x * b * x => (a*b), where a and b are particular values

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % divide(coefficient1, coefficient2)], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break
                        
                        # ADDITION
                        elif arrVar[c + 1] == operation["addition"]:

                            # SIMP9: add a variable to itself
                            
                            if arrVar[c + 2] == var:
                                
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
                            
                            if testTermEnds(c - 2, c + 2, arrVar):
                            
                            # SIMP10: a + x + b => (a+b) + x

                                if arrVar[c - 1] == operation["addition"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(val1, val2), operation["addition"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP11: a - x + b => (a+b) - x

                                if arrVar[c - 1] == operation["subtraction"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(val1, val2), operation["subtraction"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP12: add coefficients between terms with no exponents
                            
                            if testTermEnds(c - 2, c + 4, arrVar):

                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    # case: a * x + b * x => (a+b) * x
                                    
                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % add(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break              

                        # SUBTRACTION
                        elif arrVar[c + 1] == operation["subtraction"]:
                            
                            # SIMP13: subtracted from itself

                            if arrVar[c + 2] == var:
                            
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
                                arrVar = restructure([var, operation["subtraction"], '%s' % multiplier, operation["multiplication"], var], c, place, arrVar)
                                # end current simplification
                                break

                            if testTermEnds(c - 2, c + 2, arrVar):

                            # SIMP14: a + x - b => (a-b) + x

                                if arrVar[c - 1] == operation["addition"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    
                                    # get term data
                                    val1 = arrVar[c - 2]
                                    val2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % subtract(val1, val2), operation["addition"], var], c - 2, c + 2, arrVar)

                                    # end current simplification
                                    break
                            
                            # SIMP15: a - x - b => (a-b) - x

                                if arrVar[c - 1] == operation["subtraction"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                        
                                        # get term data
                                        val1 = arrVar[c - 2]
                                        val2 = arrVar[c + 2]

                                        # apply simplification to problem structure
                                        arrVar = restructure(['%s' % subtract(val1, val2), operation["subtraction"], var], c - 2, c + 2, arrVar)

                                        # end current simplification
                                        break
                            
                            # SIMP16: subtract coefficients between terms with no exponents

                            if testTermEnds(c - 2, c + 4, arrVar):
                                # correct term length for c index
                                if arrVar[c + 4] == var and arrVar[c - 1] == operation["multiplication"] and arrVar[c + 3] == operation["multiplication"] and not is_var(arrVar[c - 2]) and not is_var(arrVar[c + 2]):
                                    # a * x - b * x => (a-b) * x

                                    # get term data
                                    coefficient1 = arrVar[c - 2]
                                    coefficient2 = arrVar[c + 2]

                                    # apply simplification to problem structure
                                    arrVar = restructure(['%s' % subtract(coefficient1, coefficient2), operation["multiplication"], var], c - 2, c + 4, arrVar)
                                    
                                    # end current simplification
                                    break

                
                # test terminating condition
                if c + 1 == length:
                    # no further simplifications; on end character and no simplifications run
                    simplifying = False

        # log
        log_process("Simplified")
        # return simplified expression
        return arrVar

    # ALGEBRAIC OPERATIONS END

    # KEY FUNCTIONS START

    def getIdx(str, arr):
        # gets index of string in structure

        # get length of arr
        length = len(arr)

        # test if string contains an operation
        if is_op(str):

            # operation string
            val = None
            for i in range(0, length):
                if arr[i] == str:
                    # test for operation on variables
                    if i - 1 > -1 and i + 1 < length and not is_var(arr[i - 1]) and not is_var(arr[i + 1]):
                        val = i
                        # arithmetic operation approved; not operating on variable
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

    def trigonomic(arr):
        # key function module for trigonomic functions
        arrVar = arr
        if key_modules[0]["use"] == True:

            # fundamental functions

            # perform all sine functions
            ref = getIdx("sin", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.sin(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sin", arrVar)

            # perform all arcus sine functions
            ref = getIdx("asin", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                
                x = num_cast(arrVar[ref + 1])
                y = np.arcsin(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("asin", arrVar)
            
            # perform all cosine functions
            ref = getIdx("cos", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.cos(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("cos", arrVar)
        
            # perform all arcus cosine functions
            ref = getIdx("acos", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                
                x = num_cast(arrVar[ref + 1])
                y = np.arccos(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("acos", arrVar)

            # perform all tangent functions
            ref = getIdx("tan", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.tan(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("tan", arrVar)
            
            # perform all arcus tangent functions
            ref = getIdx("atan", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.arctan(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("atan", arrVar)

            # reciprocal functions
            
            # perform all cosecant functions
            ref = getIdx("csc", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = 1 / np.sin(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("csc", arrVar)
            
            # perform all arc cosecant functions
            ref = getIdx("acsc", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.arcsin(1/x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("acsc", arrVar)

            # perform all secant functions
            ref = getIdx("sec", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = 1 / np.cos(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sec", arrVar)
            
            # perform all arc secant functions
            ref = getIdx("sec", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.arccos(1/x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sec", arrVar)

            # perform all cotangent functions
            ref = getIdx("cot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = 1 / np.tan(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("cot", arrVar)
            
            # perform all cotangent functions
            ref = getIdx("acot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.arctan(1/x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("acot", arrVar)
            

            # hyperbolic functions

            # perform all hyperbolic sine functions
            ref = getIdx("sinh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("sinh", arrVar)
            
            # perform all arcus hyperbolic sine functions
            ref = getIdx("asinh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.asinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("asinh", arrVar)
            
            # perform all hyperbolic cosine functions
            ref = getIdx("cosh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("cosh", arrVar)
            
            # perform all arcus hyperbolic cosine functions
            ref = getIdx("acosh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.asinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("acosh", arrVar)
            
            # perform all hyperbolic tangent functions
            ref = getIdx("tanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.sinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("tanh", arrVar)
            
            # perform all arcus hyperbolic tangent functions
            ref = getIdx("atanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = np.asinh(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("atanh", arrVar)

        return arrVar

    def geometric(arr):
        # key function module for geometric functions
        arrVar = arr
        if key_modules[1]["use"] == True:
            # perform all right triangle hypotenuse functions
            ref = getIdx("hypot", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                leg1 = set_2[0]
                leg2 = set_2[1]
                
                y = np.hypot(leg1, leg2)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("hypot", arrVar)

            # perform all Heron's Formula functions
            ref = getIdx("heron", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)
                
                # perform calculation using numeral set
                # side lengths
                a = set_2[0]
                b = set_2[1]
                c = set_2[2]
                
                # semiperimeter
                s = (a + b + c) / 2
                
                # area calculation
                area = (s * (s - a) * (s - b) * (s - c))**0.5

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(area, ref, ref + 1, arrVar)
                ref = getIdx("heron", arrVar)

        return arrVar

    def combinatoric(arr):
        # key function module for combinatoric functions
        arrVar = arr

        if key_modules[2]["use"] == True:
            # perform all Factorial functions
            ref = getIdx("fact", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = factorial(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("fact", arrVar)

            # perform all Permutation functions
            ref = getIdx("perm", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                n = set_2[0]
                r = set_2[1]
                perm = factorial(n) / factorial(n - r)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(perm, ref, ref + 1, arrVar)
                ref = getIdx("perm", arrVar)
            
            # perform all Combination functions
            ref = getIdx("comb", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                n = set_2[0]
                r = set_2[1]
                comb = factorial(n) / (factorial(r) * factorial(n - r))

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(comb, ref, ref + 1, arrVar)
                ref = getIdx("comb", arrVar)

        return arrVar

    def statistical(arr):
        # key function module for statistical functions
        arrVar = arr
        if key_modules[3]["use"] == True:
            
            # perform all Standard Deviation functions
            ref = getIdx("sd", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                mean = get_mean(set_2)
                set_3 = []
                for i in set_2:
                    set_3.append(math.pow(i - mean, 2))
                sd = math.pow(sum(set_3)/len(set_3), 1/2)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(sd, ref, ref + 1, arrVar)
                ref = getIdx("sd", arrVar)
            
            # perform all Variance functions
            ref = getIdx("var", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                mean = get_mean(set_2)
                set_3 = []
                for i in set_2:
                    set_3.append(math.pow(i - mean, 2))
                sd = sum(set_3)/len(set_3)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(sd, ref, ref + 1, arrVar)
                ref = getIdx("var", arrVar)

            # perform all Harmonic Mean functions
            ref = getIdx("meanh", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        set_2.append(1/x)
                    else:
                        x = calculate(section(i))
                        set_2.append(1/x)

                # perform calculation using numeral set
                mean = len(set_2) / sum(set_2)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meanh", arrVar)
            
            # perform all Geometeric Mean functions
            ref = getIdx("meang", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # get string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                set_2 = 1
                for i in set_1:
                    if isinstance(i, str):
                        x = float(i)
                        set_2 = set_2 * x
                    else:
                        x = section(i)
                        set_2 = set_2 * x

                # perform calculation using numeral set
                mean = math.pow(set_2, 1/len(set_1))

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meang", arrVar)

            # perform all Weighted Mean functions
            ref = getIdx("meanw", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
            
                itr = itr + 1
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

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("meanw", arrVar)

            # perform all Mean functions
            ref = getIdx("mean", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                mean = get_mean(set_2)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(mean, ref, ref + 1, arrVar)
                ref = getIdx("mean", arrVar)
            
            # perform all Root Mean Square functions
            ref = getIdx("rms", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

                # perform calculation using numeral set
                square = []
                for i in set_2:
                    square.append(math.pow(i, 2))
                mean = get_mean(square)
                root = math.pow(mean, 1/2)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(root, ref, ref + 1, arrVar)
                ref = getIdx("rms", arrVar)
            
            # perform all Greatest Common Factor functions
            ref = getIdx("gcf", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

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
                
                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(gcf, ref, ref + 1, arrVar)
                ref = getIdx("gcf", arrVar)
            
            # perform all Least Common Multiple functions
            ref = getIdx("lcm", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
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
                        x = section(i)
                        set_2.append(x)

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

                    # if no multiples were found, add next multiple to each list, and test again
                    if same != True:
                        mult_1.append(mult_1[0] * x)
                        mult_2.append(mult_2[0] * x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(lcm, ref, ref + 1, arrVar)
                ref = getIdx("lcm", arrVar)
            
            # perform all Logarithm functions
            ref = getIdx("log", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1
                # get string string set
                set_1 = arrVar[ref + 1]
                log_process(set_1)

                # convert string set to numeral set
                set_2 = []
                for i in set_1:
                    if isinstance(i, str):
                        x = num_cast(i)
                        set_2.append(x)
                    else:
                        x = section(i)
                        set_2.append(x)
                
                x = set_2[0]
                b = set_2[1]
                y = math.log(x, b)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("log", arrVar)
            
            # perform all Natural Logarithm functions
            ref = getIdx("ln", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = math.log(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("ln", arrVar)
            
        return arrVar

    def algebraic(arr):
        # key function module for algebraic functions
        # algebraic operations translate to algebraic expressions
        # rather than solving for single value
        arrVar = arr

        if key_modules[4]["use"] == True:

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
                    # Log keyword
                    log_process(arrVar[ref])
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

                    # Log keyword
                    log_process(arrVar[ref])
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

                # print(nomials)
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
                        sect_struct.append(getTerms(nomial))

                    print(sect_struct)

                    # initialize sect_product with the first nomial in sect_struct
                    sect_product = sect_struct[0]

                    # multiply each nomial with the data in the sect_product variable
                    for i in range(1,len(sect_struct)):
                        product = []
                        for term1 in sect_product:
                            # each term in sect_product
                            for term2 in sect_struct[i]:
                                # each term in nomial multiplying with product

                                # append 1st term
                                for x in term1:
                                    product.append(x)
                                # append a multiplication symbol
                                product.append(operation["multiplication"])
                                # append 2nd term
                                for x in term2:
                                    product.append(x)
                                # append an addtion symbol
                                product.append(operation["addition"])
                        
                        # remove extra addition symbol from end
                        product.pop()

                        # simplify terms
                        prod_simp = []
                        for term in product:
                            prod_simp.append(simplify(term))

                        # combine like terms
                        prod_simp = combineLikeTerms(prod_simp)

                        # assign product to sect_simp
                        sect_product = prod_simp

                    # print(sect_product)

                return arrVar



                # # Use nomials to create sect_struct
                # for i in range(0, len(nomials)):
                #     # identify terms for each nomial
                #     length = len(nomials[i])
                #     if length == 1:
                #         # monomial
                #         sect_struct.append([nomials[i]])
                #     else:
                #         # polynomial
                #         terms = []
                #         for j in range(0, len(nomials[i])):
                #             # test each character in nomial for terms
                #             char = nomials[i][j]
                #             try:
                #                 # char is a number
                #                 float(char)
                #                 if nomials[i][j - 1] == operation["subtraction"]:
                #                     # negative
                #                     terms.append(["%s %s" % operation["subtraction"], char])
                #                 else:
                #                     # positive
                #                     terms.append([char])
                #             except:
                #                 if is_var(char):
                #                     # char is a variable
                #                     if nomials[i][j - 1] == operation["subtraction"]:
                #                         # negative
                #                         terms.append(["%s %s" % operation["subtraction"], char])
                #                     else:
                #                         # positive
                #                         terms.append([char])
                #                 else:
                #                     # char is not a term
                #                     continue

                #         # after terms are identified for that nomial
                #         sect_struct.append(terms)

                # print(sect_struct)

                # # total number of nomials
                # nomials_total = len(sect_struct)

                # # total number of terms
                # terms_total = 0
                # for i in range(0, len(sect_struct)):
                #     terms_total += len(sect_struct[i])
                
                # # total number of terms in product of distribution
                # # calculates the number of terms in the product expression of a nomial multiplication
                # # using the nested summation method
                # # where it works for:
                # #  - any number of nomials
                # #  - any number of terms in nomial
                # #  - variable number of terms in different nomials

                # product_terms_total = 0
                # for i in range(0, len(sect_struct)):
                #     # get terms of current nomial
                #     k = len(sect_struct[i])
                #     # sum previous terms
                #     s = 0
                #     for l in range(0, i):
                #         s += len(sect_struct[l])
                #     s += k
                #     product_terms_total += k * (terms_total - s)
                
                # # print(nomials_total)
                # # print(terms_total)
                # # print(product_terms_total)

                # # construct product expression

                # # now that the number of terms in the product expression is known, the number of multiplications is also known,
                # # because one multiplication creates one term, so the number of terms and multiplcations are the same number.

                # # the design of product expression construction is thus:
                # #  - to access two terms in the reference structure of unique combination, 
                # #  - build a list which includes those terms separated by a multication symbol,
                # #  - compile that list into the product structure, demarcating each concatenation to the product structure with an addition symbol,
                # #  - and repeating this process for the number of multiplications,
                # #  - except for the last multiplication, which should have no addition symbol following it.

                # # multiplier indexes
                # term1 = 0
                # nomial1 = 0

                # # multiplicand indexes
                # term2 = 0
                # nomial2 = 0

                # # structures
                # multiplier = []
                # multiplicand = []
                # product = []

                # for i in range(0, product_terms_total - 1):
                #     # initialize
                #     if nomial2 == 0:
                #         # first term in product expression
                #         multiplier = sect_struct[nomial1][term1]
                #         nomial2 += 1
                #         multiplicand = sect_struct[nomial2][term2]
                    
                #     # update indexes
                #     # multiplicand term
                #         # multiplicand nomial
                #             # multiplier term
                #                 # multiplier nomial

                #     # multiplicand term
                #     elif term2 + 1 != len(sect_struct[nomial2]):
                #         # mid term in nomial for the multiplicand
                #         term2 += 1
                #     else:
                #         # last term of nomial for the multiplicand
                #         term2 = 0 # first term of next nomial

                        
                #         # multiplicand nomial
                #         if nomial2 + 1 != nomials_total:
                #             # mid nomial for multiplicand
                #             nomial2 += 1
                #         else:
                #             # last nomial for multiplicand
                #             nomial2 = nomial1 + 1


                #             # multiplier term
                #             if term1 + 1 != len(sect_struct[nomial1]):
                #                 # mid term of nomial for multiplier
                #                 term1 += 1
                #             else:
                #                 # last term of nomial for multiplier
                #                 term1 = 0 # first term of next nomial
                                
                                
                #                 # multiplier nomial
                #                 if nomial1 + 1 != nomials_total - 1: # -1 : multiplier never the last nomial
                #                     # mid nomial for multiplier
                #                     nomial1 += 1
                #                     nomial2 = nomial1 + 1
                #                     term2 = 0
                #                 else:
                #                     # last nomial for multiplier
                #                     break

                #     # update multiplier
                #     multiplier = sect_struct[nomial1][term1]
                #     # update multiplicand
                #     multiplicand = sect_struct[nomial2][term2]

                #     # print("nomial: %s" % str(int(nomial2) + 1))
                #     # print("term: %s" % str(int(term2) + 1))
                #     # print(multiplier)
                #     # print(multiplicand)

                #     # concatenate multiplier and multiplicand with product
                #     product = product + multiplier + ["*"] + multiplicand + ["+"]

                # # last term
                # if len(sect_struct[len(sect_struct) - 1]) > 1:
                #     # for ending monomial
                #     term2 += 1
                #     multiplicand = sect_struct[nomial2][term2]
                #     product = product + multiplier + ["*"] + multiplicand
                # else:
                #     term1 += 1
                #     multiplier = sect_struct[nomial1][term1]
                #     product = product + multiplier + ["*"] + multiplicand

                # # Log keyword
                # log_process(arrVar[ref])
                # # restructure with product expression
                # arrVar = restructure(product, ref, ref + 1, arrVar)
                # # identify further cases of polynomial expansion
                # ref = getIdx("expand", arrVar)
        
        return arrVar

    def key_functions(arr):
        # runs key function modules
        nonlocal algebraic_mode
        arrVar = arr

        # Log process label for key functions
        log_process("Key Functions")

        if algebraic_mode == True:
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

        return arrVar
    
    # KEY FUNCTIONS END

    def calculate(arr):
        # scans for operations and calculates
        log_process("Calculating")
        arrVar = arr

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
        
        # perform all arithmetic operations accounting for operator precedence
        
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
                    arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                    d_ref = getIdx(operation["division"], arrVar)

                elif m_ref is not None and d_ref is not None and m_ref < d_ref:
                    # Multiply first
                    x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                    arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)

                    d_ref = getIdx(operation["division"], arrVar)
                    y = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                    arrVar = restructure(y, d_ref - 1, d_ref + 1, arrVar)

                    m_ref = getIdx(operation["multiplication"], arrVar)
                    d_ref = getIdx(operation["division"], arrVar)

                elif d_ref is not None and m_ref is not None and d_ref < m_ref:
                    # Divide First
                    x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                    arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                    m_ref = getIdx(operation["multiplication"], arrVar)

                    y = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                    arrVar = restructure(y, m_ref - 1, m_ref + 1, arrVar)

                    m_ref = getIdx(operation["multiplication"], arrVar)
                    d_ref = getIdx(operation["division"], arrVar)

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
                arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                d_ref = getIdx(operation["division"], arrVar)

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
                x = root(arrVar[ref + 1], 2)
                arrVar = restructure(x, ref, ref + 1, arrVar)
                ref = getIdx(operation["radication"], arrVar)
        
        log_process("Calculated")
        
        # test for variables in section
        is_variables = False
        for i in range(0, len(arrVar)):
            if is_var(arrVar[i]) == True:
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
        # performs calculations in order of parenthesis nesting
        nonlocal is_paren
        arrVar = arr
        thresh = 0
        while is_paren == True and thresh < paren_limit:
            thresh = thresh + 1
            # test for parenthesis
            parens = []
            count = 0
            for i in range(0, len(arrVar)):
                if arrVar[i] == "(":
                    count = count + 1
                    parens.append({"index": i, "char": "("})
                elif arrVar[i] == ")":
                    count = count + 1
                    parens.append({"index": i, "char": ")"})
            if count == 0:
                is_paren = False
                continue
            else:
                log_process("Parenthesis")
            
            # get section to be solved
            osme = []
            for i in range(0, len(parens)):
                if parens[i]["char"] == "(" and parens[i + 1]["char"] == ")":
                    arr_sect = arrVar[parens[i]["index"] + 1:parens[i + 1]["index"]]
                    # send to osme for restructing
                    osme.append({"section": arr_sect, "start": parens[i]["index"] + 1, "end": parens[i + 1]["index"]})
            
            # print(osme)

            # restructuring
            for i in range(0, len(osme)):
                start = osme[len(osme) - 1 - i]["start"] - 1
                end = osme[len(osme) - 1 - i]["end"] + 1
                section = osme[len(osme) - 1 - i]["section"]
                log_process(section)
                if len(section) > 1:
                    section = calculate(section)
                arrVar = restructure(section, start, end - 1, arrVar)

        arrVar = calculate(arrVar)
        return arrVar

    def evaluate(str):
        # top level function runs high level functions

        # test for invalid characters
        nonlocal valid_chars
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
            # invalid character => cancel evaluation
            return 'Invalid character: %s' % character
        else:
            # valid characters => proceed evaluation
            log_process("Structuring")
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

            log_process("Constants")

            # structure pi
            ref = get_word("pi", structure)
            itr = 0
            while itr < c_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.pi, ref["first"], ref["last"] - 1, structure)
                ref = get_word("pi", structure)
            
            # structure euler's number
            ref = get_word("euler", structure)
            itr = 0
            while itr < c_limit and ref is not None:
                itr = itr + 1
                structure = restructure(np.e, ref["first"], ref["last"] - 1, structure)
                ref = get_word("euler", structure)

            # structure keywords
            log_process("Keywords")
            
            # key functions
            for module in range(0, len(info["key_functions"])):
                for i in range(0, len(info["key_functions"][module])):
                    structure = word_struct(info["key_functions"][module][i]["key"], structure, module)
            log_process(key_modules)
                
            # change first log
            if use_logs == "1":
                process_log["0"] = "Process Log Start"
            
            # Identify program entities in structured string
            if not identify_entities(structure):
                # invalid entity detected
                return structure
            else:
                # all entities are valid
                nonlocal is_brack
                if is_brack == True:
                    # generates substructures, i.e. "sets", within structure
                    # sets exist so that multiple arguments can be accessed at a single index for key functions
                    log_process("Structure Sets")
                    log_process(structure)
                    # structure sets
                    sets_ref = []
                    for i in range(0, len(structure)):
                        if structure[i] == "[":
                            sets_ref.append({"char": "[", "index": i})
                        elif structure[i] == "]":
                            sets_ref.append({"char": "]", "index": i})
                    # identify next set to structure using sets_ref
                    while len(sets_ref) > 0:
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

                # parenthetically section and solve
                return section(structure)

    # Evaluation
    use_logs = input["use_logs"]
    answer = evaluate(input["problem"])

    # convert algebraic expressions to answer string
    if isinstance(answer, list):
        string = ""
        for i in answer:
            string = string + str(i)
        answer = string

    # assign output object
    output = {
        "problem": input["problem"],
        "answer": answer,
        "logs": process_log,
    }

    # return output

    # Development

    # Prints feedback
    logs = """"""
    process_log_keys = list(process_log.keys())
    for key in process_log_keys:
        logs += """%s
""" % process_log[key]
    
    print(output["problem"])
    print(output["answer"])
    print(logs)

# test data
input = {
    "problem": "a+a+a-2*3", # solve arithmetic in algebraic expression even if not in parens

    # "problem": "a*a*a", # simplifies algebraic expression for consecutive multiplications
    # "problem": "2*x*9", #  a * x * b => (a*b) * x
    # "problem": "2/x*9", #  a / x * b => (a*b) / x
    # "problem": "3*x*7*x", #  combine terms for variable with coefficients multiplied

    # "problem": "a/a/a/a", # simplifies algebraic expression for consecutive divisions of self; a/(a^3)
    # "problem": "x*a/a", # simplifies algebraic expression for cancelling out division by self with multiplication; x
    # "problem": "x/a/a", # simplifies algebraic expression for cancelling out division by self with division; x
    # "problem": "a/a", # simplifies algebraic expression for variable divide by itself; 1
    # "problem": "10*x/2", # a * x / b => (a/b) * x
    # "problem": "10/x/2", # a / x / b => (a/b) / x
    # "problem": "4*x/2*x", #  combine terms for variable with coefficients divided
    
    # "problem": "a+a+a", # simplifies algebraic expression for consecutive additions
    # "problem": "10+x+2", # a + x + b => (a+b) + x
    # "problem": "10-x+2", # a - x + b => (a+b) - x
    # "problem": "2*x+4*x", # add coefficients of like terms
    # "problem": "2*x+4*y", # don't add coefficients of not like terms
    
    # "problem": "a-a-a-a", # simplifies algebraic expression for consecutive substractions
    # "problem": "10+x-2", # a + x - b => (a-b) + x
    # "problem": "10-x-2", # a - x - b => (a-b) - x
    # "problem": "8*x-3*x", # subtract coefficients of like terms
    # "problem": "8*x-3*y", # don't subtract coefficients of not like terms

    # "problem": "1+1/&%$#", # returns "invalid characters"
    # "problem": "expand[[2*x^2+y][x+y][a+b]]",

    "use_logs": "1", # 1 = yes
}
evaluator(input)

# development tasks
#  - design remaining simplifications in simplify function
#  - complete and test expand key function with simplifications
#  - order each term at the end of the get terms function ( exempli gratia x*2*y => 2*x*y; x^2*3 => 3*x^2)

# vulnerabilities
#  - key without parens or brackets
#  - brackets without key
#  - variables with no operations between them
#  - 

# # Flask APP
# app = Flask(__name__)

# # CORS wrapper
# CORS(app)

# # ROUTES

# # Index route
# @app.route("/", methods=["GET"])
# def index():
#     return "<div>Index route accessed.</div>"

# # Hello world environment variable demonstration
# @app.route("/hello-world", methods=["GET"])
# def hello_world():
#     return "<p>%s</p>" % os.environ['greeting']

# # Evaluator data root
# @app.route("/eval", methods=["POST"])
# def eval():
#     try:
#         return jsonify(evaluator(request.get_json()))
#     except Exception as e:
#         return "Error:", e
    
# # Evaluator problem data
# @app.route("/eval/problem", methods=["POST"])
# def eval_problem():
#     try:
#         return jsonify(evaluator(request.get_json())["problem"])
#     except Exception as e:
#         return "Error:", e

# # Evaluator answer data
# @app.route("/eval/answer", methods=["POST"])
# def eval_answer():
#     try:
#         return jsonify(evaluator(request.get_json())["answer"])
#     except Exception as e:
#         return "Error:", e

# # Evaluator log data
# @app.route("/eval/logs", methods=["POST"])
# def eval_logs():
#     try:
#         return jsonify(evaluator(request.get_json())["logs"])
#     except Exception as e:
#         return "Error:", e

# # Evaluator info object data (read-only)
# @app.route("/eval/info", methods=["GET"])
# def eval_info():
#     try:
#         return jsonify(info)
#     except Exception as e:
#         return "Error:", e