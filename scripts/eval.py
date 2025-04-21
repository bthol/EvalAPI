import math
import numpy as np

# PROGRAMIC PROCESS

# Phase I: Entity Structuring and Analysis
# Description: Analyzes problem string to create structure from string data and analyzes structure to identify program entities from structure data, including and limited to multi-digit numbers, negative numbers, decimal numbers, mathematical operators, parenthesis, sets and keywords.

# Phase II: Structural Manipulation
# Description: Bypassed unless, as identified in Phase I, there are parenthesis, in which case, a test for distribution is run, where either there is distribution and the distribution and section functions manipulate the structure accordingly or there isn't distribution and only the section function manipulates the structure accordingly.

# Phase III: Key Functions
# Description: Bypassed unless, in one case, there are parenthesis and keywords, in which case search for and run key functions or, in another case, there are square brackets and keywords, in which case manipulate the structure to form sets and search for and run key functions.

# Phase IV: Calculation
# Description: Search for and run appropriate mathematical operation on contents of structure, restructure with solution, and repeat until no operations are remaining.

# PROGRAM PARAMETERS

# the paren_limit parameter controls the maximum number of levels of parenthesis nesting in any one evaluation
paren_limit = 10

# the poly_degree_limit parameter controls the maximum degree of a polynomial expression resulting from factoring in any one evaluation
poly_degree_limit = 10

# the poly_fact_limit parameter controls the maximum number of times that polynomial expressions can be factored out in any one evaluation
poly_fact_limit = 10

# the pi_limit parameter controls the maximum number of instances of any one constant allowed in any one evaluation
c_limit = 10

# the key_limit parameter controls the maximum number of the same key function allowed in any one evaluation
key_limit = 10

# PROGRAM MODES

# defines valid variable characters
variables = "abcdefghijklmnopqrstuvwxyz"

# algebraic_mode controls whether the program solves for an algebraic expression, True, or a single value, False
algebraic_mode = False

# PROGRAM ENTITY REFERENCE

# system_operation indicates whether there are system operations, True, or not, False
# If True, terminates program after system operations are complete
system_operation = False

# is_paren indicates whether there are parenthesis, True, or not, False
# If False, bypasses distribute and section functions
is_paren = False

# is_dist indicates whether there is distribution, True, or not, False
# If False, bypasses distribute function
is_dist = False

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

# use_logs determines whether or not to use logging
# if use_logs is "1", then logging is active, otherwise it remains defaultly inactive
use_logs = ""

# Program Information
info = {
    "system_operations": [
        {"name": "info", "about": "Prints program information, i.e. system operations, program entities, key functions, and their related information."},
    ],
    
    "operations": [
        {"name":"Negative Numbers", "syntax":"(-x)"},
        {"name":"Exponentiation", "syntax":"^"},
        {"name":"root", "syntax":"√"}, # alt code 251
        {"name":"Multiplication", "syntax":"*"},
        {"name":"Division", "syntax":"/"},
        {"name":"Addition", "syntax":"+"},
        {"name":"Subtraction", "syntax":"-"},
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
            # {"name":"Cosecant", "key":"csc", "syntax": "csc(x)", "about": "Gets the cosecant, i.e. the reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            # {"name":"Arcus Cosecant", "key":"csc", "syntax": "csc(x)", "about": "Gets the arcus cosecant, i.e. the inverse reciprocal sine, of x, where x is a value or an expression that evaluates to a value."},
            
            # {"name":"Secant", "key":"sec", "syntax": "sec(x)", "about": "Gets the secant, i.e. the reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            # {"name":"Arcus Secant", "key":"sec", "syntax": "sec(x)", "about": "Gets the arcus secant, i.e. the inverse reciprocal cosine, of x, where x is a value or an expression that evaluates to a value."},
            
            # {"name":"Cotangent", "key":"cot", "syntax": "cot(x)", "about": "Gets the cotangent, i.e. the reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},
            
            # {"name":"Arcus Cotangent", "key":"cot", "syntax": "cot(x)", "about": "Gets the arcus cotangent, i.e. the inverse reciprocal tangent, of x, where x is a value or an expression that evaluates to a value."},

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
            {"name":"Algebraic Exponentiation", "key":"algexp", "syntax":"algexp[[a],x]", "about":"Gets an algebraic exponentiation given a polynomial expression a and power x, where x is a value or an arithmetic expression that evaluates to a value wrapped within square brackets, e.g. expand[[a],[x]]"},
            
            {"name":"Polynomial Expansion", "key":"expand", "syntax":"expand[[x][y]]", "about":"Gets a polynomial expansion given a list of at least 2 polynomial expressions x and y, where each expression may have a unique number of any number of terms, e.g. expand[[a][b+c][d+e+f]]"},
        ],
    ],
}

def evaluator(input):
    # process_log is an object literal that stores string values for all process checkpoints during evalution
    # use_logs indicates whether to use logs, True, or not, False
    # note: log_process is run on every restructure, run for calculation reference, and run for process labels
    global info
    global key_modules
    global use_logs
    process_log = {"0":"no logging"}
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
            else:
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
        global is_key
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

    def structure_sets(arr):
        # generates substructures, i.e. "sets", within structure
        # sets exist so that an expression can be accessed at a single index for key functions
        global is_brack
        if is_brack == True:
            log_process("Structure Sets")
            log_process(arr)
            # structure sets
            sets_ref = []
            for i in range(0, len(arr)):
                if arr[i] == "[":
                    sets_ref.append({"char": "[", "index": i})
                elif arr[i] == "]":
                    sets_ref.append({"char": "]", "index": i})
            # identify next set to structure using reference
            while len(sets_ref) > 0:
                for i in range(0, len(sets_ref)):
                    if sets_ref[i]["char"] == "[" and sets_ref[i + 1]["char"] == "]":
                        # build set
                        start_index = sets_ref[i]["index"]
                        end_index = sets_ref[i + 1]["index"]
                        solution_length = abs(start_index - end_index) + 1
                        the_set_itself = []
                        for i in range(0, solution_length):
                            the_set_itself.append(arr[start_index + i])

                        # restructure
                        arr = restructure(the_set_itself, start_index, end_index, arr)
                        
                        # update reference
                        sets_ref = []
                        for i in range(0, len(arr)):
                            if arr[i] == "[":
                                sets_ref.append({"char": "[", "index": i})
                            elif arr[i] == "]":
                                sets_ref.append({"char": "]", "index": i})
                        break
        return arr

    def entity_no_pass():
        # bypasses everything
        # reset for identify_entities
        global is_paren
        global is_dist
        global is_exp
        global is_poly_fact
        global is_brack
        global is_root
        global is_mult
        global is_div
        global is_add
        global is_sub

        is_paren = False
        is_dist = False
        is_exp = False
        is_poly_fact = False
        is_brack = False
        is_root = False
        is_mult = False
        is_div = False
        is_add = False
        is_sub = False
    
    def identify_dist(arr):
        # tests for distribution on section
        global is_dist
        is_dist = False
        end = len(arr) - 1
        for i in range(0, len(arr)):
            if i != 0 and i != end:
                if (arr[i] == "(" and arr[i - 1] == "*") or (arr[i] == ")" and i < len(arr) - 1 and arr[i + 1] == "*"):
                    is_dist = True
                    break
    
    def is_var(str):
        # test for variables
        global variables
        for i in variables:
            if i == str:
                return True
        return False

    def identify_entities(arr):
        # Identify algebraic mode
        global algebraic_mode
        for i in range(0, len(arr)):
            if is_var(arr[i]):
                algebraic_mode = True
                break
        
        # Identify parenthesis
        global is_paren
        if is_paren == False:
            for i in range(0, len(arr)):
                if arr[i] == "(":
                    is_paren = True
                    break
        
        # identify distribution
        global is_dist
        if is_dist == False:
            if (is_paren):
                end = len(arr) - 1
                for i in range(0, len(arr)):
                    if i != 0 and i != end:
                        if (arr[i] == "(" and arr[i - 1] == "*") or (arr[i] == ")" and i < len(arr) - 1 and arr[i + 1] == "*"):
                            # multiplicative distribution
                            is_dist = True
                            break
        
        # Identify exponentiation
        global is_exp
        if is_exp == False:
            for i in range(0, len(arr)):
                if arr[i] == "^":
                    is_exp = True
                    break
        
        # Identify square brackets
        global is_brack
        if is_brack == False:
            for i in range(0, len(arr)):
                if arr[i] == "[":
                    is_brack = True
                    break
        
        # Identify roots
        global is_root
        if is_root == False:
            for i in range(0, len(arr)):
                if arr[i] == "√":
                    is_root = True
                    break
        
        # Identify multiplication
        global is_mult
        if is_mult == False:
            for i in range(0, len(arr)):
                if arr[i] == "*":
                    is_mult = True
                    break
        
        # Identify division
        global is_div
        if is_dist == False:
            for i in range(0, len(arr)):
                if arr[i] == "/":
                    is_div = True
                    break
        
        # Identify addition
        global is_add
        if is_add == False:
            for i in range(0, len(arr)):
                if arr[i] == "+":
                    is_add = True
                    break
        
        # Identify subtraction
        global is_sub
        if is_sub == False:
            for i in range(0, len(arr)):
                if arr[i] == "-":
                    is_sub = True
                    break

    # Phase I Process
    def structure_string(str):
        # Analyzes string to generate structure containing string data
        log_process("Structuring")
        # structure multi-digit numbers, negative numbers, decimal numbers, mathematical operations, parenthesis, and square brackets
        arr = []
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
                        arr.pop()
                        digits = "%s" % str[i]
                    elif str[i] == ")":
                        try:
                            if int(digits) < 0:
                                arr.append(digits)
                                digits = ""
                            else:
                                # 
                                if len(digits) > 0:
                                    arr.append(digits)
                                    digits = ""
                                # 
                                arr.append(str[i])
                        except:
                            if len(digits) > 0:
                                arr.append(digits)
                            digits = ""
                            arr.append(str[i])
                    else:
                        if len(digits) > 0:
                            arr.append(digits)
                        digits = ""
                        arr.append(str[i])
                else:
                    digits = digits + "%s" % str[i]
                finally:
                    if (i == len(str) - 1 and len(digits) > 0):
                        arr.append(digits)
        log_process(arr)

        log_process("Constants")
        # structure pi
        ref = get_word("pi", arr)
        itr = 0
        while itr < c_limit and ref is not None:
            itr = itr + 1
            arr = restructure(np.pi, ref["first"], ref["last"] - 1, arr)
            ref = get_word("pi", arr)
        
        # structure euler's number
        ref = get_word("euler", arr)
        itr = 0
        while itr < c_limit and ref is not None:
            itr = itr + 1
            arr = restructure(np.e, ref["first"], ref["last"] - 1, arr)
            ref = get_word("euler", arr)

        # structure keywords
        log_process("Keywords")

        # system operations
        for i in range(0, len(info["system_operations"])):
            arr = word_struct(info["system_operations"][i]["name"], arr)
        
        # key functions
        for module in range(0, len(info["key_functions"])):
            for i in range(0, len(info["key_functions"][module])):
                arr = word_struct(info["key_functions"][module][i]["key"], arr, module)
        log_process(key_modules)

        return arr
    # STRUCTURE END

    # OPERATIONS START
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
    
    # OPERATIONS END

    # KEY FUNCTIONS START
    def getIdx(str, arr):
        # gets index of string in structure
        val = None
        for i in range(0, len(arr)):
            if arr[i] == str:
                val = i
                break
        return val

    def trigonomic(arr):
        # key function module for trigonomic functions
        arrVar = arr
        if key_modules[0]["use"] == True:
            # perform all sine functions
            ref = getIdx("sin", arrVar)
            itr = 0
            while itr < key_limit and ref is not None:
                itr = itr + 1

                x = num_cast(arrVar[ref + 1])
                y = math.sin(x)

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
                y = math.asin(x)

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
                y = math.cos(x)

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
                y = math.acos(x)

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
                y = math.tan(x)

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
                y = math.atan(x)

                # Log keyword
                log_process(arrVar[ref])
                arrVar = restructure(y, ref, ref + 1, arrVar)
                ref = getIdx("atan", arrVar)

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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = calculate(section(distribute(i)))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                        x = section(distribute(i))
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
                    x = section(distribute(args[1]))
                    args[1] = x

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

                # reference structure for section with distribution
                sect_struct = []

                # Use nomials to create sect_struct
                for i in range(0, len(nomials)):
                    # identify terms for each nomial
                    length = len(nomials[i])
                    if length == 1:
                        # monomial
                        sect_struct.append([nomials[i]])
                    else:
                        # polynomial
                        terms = []
                        for j in range(0, len(nomials[i])):
                            # test each character in nomial for terms
                            char = nomials[i][j]
                            try:
                                # char is a number
                                float(char)
                                if nomials[i][j - 1] == "-":
                                    # negative
                                    terms.append(["- % s" % char])
                                else:
                                    # positive
                                    terms.append([char])
                            except:
                                if is_var(char):
                                    # char is a variable
                                    if nomials[i][j - 1] == "-":
                                        # negative
                                        terms.append(["- % s" % char])
                                    else:
                                        # positive
                                        terms.append([char])
                                else:
                                    # char is not a term
                                    continue

                        # after terms are identified for that nomial
                        sect_struct.append(terms)

                # print(sect_struct)

                # total number of nomials
                nomials_total = len(sect_struct)

                # total number of terms
                terms_total = 0
                for i in range(0, len(sect_struct)):
                    terms_total += len(sect_struct[i])
                
                # total number of terms in product of distribution
                # calculates the number of terms in the product expression of a nomial multiplication
                # using the nested summation method
                # where it works for:
                #  - any number of nomials
                #  - any number of terms in nomial
                #  - different number of terms in different nomials

                product_terms_total = 0
                for i in range(0, len(sect_struct)):
                    # get terms of current nomial
                    k = len(sect_struct[i])
                    # sum previous terms
                    s = 0
                    for l in range(0, i):
                        s += len(sect_struct[l])
                    s += k
                    product_terms_total += k * (terms_total - s)
                
                # print(nomials_total)
                # print(terms_total)
                # print(product_terms_total)

                # construct product expression

                # now that the number of terms in the product expression is known, the number of multiplications is also known,
                # because one multiplication creates one term, so the number of terms and multiplcations are the same number.

                # the design of product expression construction is thus:
                #  - to access two terms in the reference structure of unique combination, 
                #  - build a list which includes those terms separated by a multication symbol,
                #  - compile that list into the product structure, demarcating each concatenation to the product structure with an addition symbol,
                #  - and repeating this process for the number of multiplications,
                #  - except for the last multiplication, which should have no addition symbol following it.

                # multiplier indexes
                term1 = 0
                nomial1 = 0

                # multiplicand indexes
                term2 = 0
                nomial2 = 0

                # structures
                multiplier = []
                multiplicand = []
                product = []

                for i in range(0, product_terms_total - 1):
                    # initialize
                    if nomial2 == 0:
                        # first term in product expression
                        multiplier = sect_struct[nomial1][term1]
                        nomial2 += 1
                        multiplicand = sect_struct[nomial2][term2]
                    
                    # update indexes
                    # multiplicand term
                        # multiplicand nomial
                            # multiplier term
                                # multiplier nomial

                    # multiplicand term
                    elif term2 + 1 != len(sect_struct[nomial2]):
                        # mid term in nomial for the multiplicand
                        term2 += 1
                    else:
                        # last term of nomial for the multiplicand
                        term2 = 0 # first term of next nomial

                        
                        # multiplicand nomial
                        if nomial2 + 1 != nomials_total:
                            # mid nomial for multiplicand
                            nomial2 += 1
                        else:
                            # last nomial for multiplicand
                            nomial2 = nomial1 + 1


                            # multiplier term
                            if term1 + 1 != len(sect_struct[nomial1]):
                                # mid term of nomial for multiplier
                                term1 += 1
                            else:
                                # last term of nomial for multiplier
                                term1 = 0 # first term of next nomial
                                
                                
                                # multiplier nomial
                                if nomial1 + 1 != nomials_total - 1: # -1 : multiplier never the last nomial
                                    # mid nomial for multiplier
                                    nomial1 += 1
                                    nomial2 = nomial1 + 1
                                    term2 = 0
                                else:
                                    # last nomial for multiplier
                                    break

                    # update multiplier
                    multiplier = sect_struct[nomial1][term1]
                    # update multiplicand
                    multiplicand = sect_struct[nomial2][term2]

                    # print("nomial: %s" % str(int(nomial2) + 1))
                    # print("term: %s" % str(int(term2) + 1))
                    # print(multiplier)
                    # print(multiplicand)

                    # concatenate multiplier and multiplicand with product
                    product = product + multiplier + ["*"] + multiplicand + ["+"]

                # last term
                if len(sect_struct[len(sect_struct) - 1]) > 1:
                    # for ending monomial
                    term2 += 1
                    multiplicand = sect_struct[nomial2][term2]
                    product = product + multiplier + ["*"] + multiplicand
                else:
                    term1 += 1
                    multiplier = sect_struct[nomial1][term1]
                    product = product + multiplier + ["*"] + multiplicand

                # Log keyword
                log_process(arrVar[ref])
                # restructure with product expression
                arrVar = restructure(product, ref, ref + 1, arrVar)
                # identify further cases of polynomial expansion
                ref = getIdx("expand", arrVar)
        
        return arrVar

    def key_functions(arr):
        # runs key function modules
        # Log process label for key functions
        global algebraic_mode
        log_process("Key Functions")
        arrVar = arr
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

    # Phase III and IV Process
    def calculate(arr):
        # scans for operations and calculates
        log_process("Calculating")
        arrVar = arr

        # Phase III
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

        # test for variables in section
        is_variables = False
        for i in range(0, len(arrVar)):
            if is_var(arrVar[i]) == True:
                is_variables = True
                break

        if is_variables == True:
            # return expression
            return arrVar
        else:
            # Phase IV
            # perform all arithmetic operations in operator precedence
            
            # perform all Multiplications and Divisions as they appear from left to right
            if is_mult == True and is_div == True:
                m_ref = getIdx("*", arrVar)
                d_ref = getIdx("/", arrVar)
                while m_ref is not None or d_ref is not None:
                    if d_ref is None and m_ref is not None:
                        # Only Multiply
                        x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                        arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)
                        m_ref = getIdx("*", arrVar)

                    elif m_ref is None and d_ref is not None:
                        # Only Divide
                        x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                        arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                        d_ref = getIdx("/", arrVar)

                    elif m_ref is not None and d_ref is not None and m_ref < d_ref:
                        # Multiply first
                        x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                        arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)

                        d_ref = getIdx("/", arrVar)
                        y = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                        arrVar = restructure(y, d_ref - 1, d_ref + 1, arrVar)

                        m_ref = getIdx("*", arrVar)
                        d_ref = getIdx("/", arrVar)

                    elif d_ref is not None and m_ref is not None and d_ref < m_ref:
                        # Divide First
                        x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                        arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                        m_ref = getIdx("*", arrVar)

                        y = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                        arrVar = restructure(y, m_ref - 1, m_ref + 1, arrVar)

                        m_ref = getIdx("*", arrVar)
                        d_ref = getIdx("/", arrVar)

            elif is_mult == True:
                m_ref = getIdx("*", arrVar)
                while m_ref is not None:
                    x = multiply(arrVar[m_ref - 1], arrVar[m_ref + 1])
                    arrVar = restructure(x, m_ref - 1, m_ref + 1, arrVar)
                    m_ref = getIdx("*", arrVar)

            elif is_div == True:
                d_ref = getIdx("/", arrVar)
                while d_ref is not None:
                    x = divide(arrVar[d_ref - 1], arrVar[d_ref + 1])
                    arrVar = restructure(x, d_ref - 1, d_ref + 1, arrVar)
                    d_ref = getIdx("/", arrVar)

            # perform all Additions and Subtractions as they appear from left to right
            if is_add == True and is_sub == True:
                a_ref = getIdx("+", arrVar)
                s_ref = getIdx("-", arrVar)
                while a_ref is not None or s_ref is not None:
                    if s_ref is None and a_ref is not None:
                        # only add
                        x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                        arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                        a_ref = getIdx("+", arrVar)

                    elif a_ref is None and s_ref is not None:
                        # only subtract
                        x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                        arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                        s_ref = getIdx("-", arrVar)

                    elif a_ref is not None and s_ref is not None and a_ref < s_ref:
                        # add first
                        x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                        arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                        a_ref = getIdx("+", arrVar)

                        s_ref = getIdx("-", arrVar)
                        y = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                        arrVar = restructure(y, s_ref - 1, s_ref + 1, arrVar)

                        a_ref = getIdx("+", arrVar)
                        s_ref = getIdx("-", arrVar)

                    elif s_ref is not None and a_ref is not None and s_ref < a_ref:
                        # subtract first
                        x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                        arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                        s_ref = getIdx("-", arrVar)

                        a_ref = getIdx("+", arrVar)
                        y = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                        arrVar = restructure(y, a_ref - 1, a_ref + 1, arrVar)

                        a_ref = getIdx("+", arrVar)
                        s_ref = getIdx("-", arrVar)
            
            elif is_add == True:
                a_ref = getIdx("+", arrVar)
                while a_ref is not None:
                    x = add(arrVar[a_ref - 1], arrVar[a_ref + 1])
                    arrVar = restructure(x, a_ref - 1, a_ref + 1, arrVar)
                    a_ref = getIdx("+", arrVar)
            
            elif is_sub == True:
                s_ref = getIdx("-", arrVar)
                while s_ref is not None:
                    x = subtract(arrVar[s_ref - 1], arrVar[s_ref + 1])
                    arrVar = restructure(x, s_ref - 1, s_ref + 1, arrVar)
                    s_ref = getIdx("-", arrVar)
            
            # perform all exponentiations
            if is_exp == True:
                ref = getIdx("^", arrVar)
                while ref is not None:
                    x = exponentiate(arrVar[ref - 1], arrVar[ref + 1])
                    arrVar = restructure(x, ref - 1, ref + 1, arrVar)
                    ref = getIdx("^", arrVar)

            # Perform all square roots
            if is_root == True:
                ref = getIdx("√", arrVar)
                while ref is not None:
                    x = root(arrVar[ref + 1], 2)
                    arrVar = restructure(x, ref, ref + 1, arrVar)
                    ref = getIdx("√", arrVar)
            
            return arrVar[0]

    # Phase II Process START
    def section(arr):
        # performs calculations in order of parenthesis nesting
        global is_paren
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
 
    def distribute(arr):
        # restructures with distributed terms
        global is_dist
        arrVar = arr

        x = 0
        while is_dist == True and x < paren_limit:
            # runs distribution process
            x += 1
            log_process("Distribution")
            
            refer = []
            for i in range(0, len(arrVar)):
                if arrVar[i] == "(" or arrVar[i] == ")" or arrVar[i] == "*":
                    refer.append({"char": arrVar[i], "index": i})

            # search for a case of distribution
            
            # get nest center index
            center = 0
            nest = 0
            for i in range(0, len(refer)):
                if refer[i]["char"] == "(":
                    nest += 1
                elif refer[i]["char"] == ")":
                    nest -= 1
                elif refer[i]["char"] == "*" and nest > 0 and refer[i]["index"] + 1 < len(arrVar) and arrVar[refer[i]["index"] + 1] == "(":
                    # print("pass")
                    center = i
                    break
            
            # # if no nest center index
            if center == 0:
                # get first center index tested from left-to-right
                for i in range(0, len(refer)):
                    # by testing if the current object's index value (only a "*") and previous object's index value are 1 index away from each other in arrVar and are the ")" and "*" characters
                    # or if the current object's index value (only a "*") and next object's index values are 1 index away from each other in arrVar and are the "*" and "(" characters
                    if refer[i]["char"] == "*" and i > 0 and arrVar[refer[i]["index"] - 1] == ")" or refer[i]["char"] == "*" and refer[i]["index"] + 1 < len(arrVar) and arrVar[refer[i]["index"] + 1] == "(":
                        # case of distribution
                        center = i
                        break
            
            # print(refer[center])

            # get section for distribution
            start = 0
            end = 0
            section = []

            # search for start
            if center > 0 and refer[center - 1]["char"] == ")" and refer[center]["index"] == refer[center - 1]["index"] + 1:
                a = 0
                for j in range(0, center):
                    # backtrack to find start
                    if refer[center - j - 1]["char"] == "(":
                        a += 1
                        if a == 0:
                            start = refer[center - j - 1]["index"]
                            break
                    elif refer[center - j - 1]["char"] == ")":
                        a -= 1
            else:
                # first nomial is a monomial
                start = refer[center]["index"] - 1
            
            # search for end
            # if the current and next objects have characters that are right next to each other in arrVar
            if center + 1 < len(refer) and refer[center]["index"] == refer[center + 1]["index"] - 1:
                # and the character in the next object is a "("
                if refer[center + 1]["char"] == "(":
                    # fronttrack to find end
                    nest = 0
                    for j in range(refer[center]["index"], len(arrVar)):
                        if arrVar[j] == "(":
                            nest += 1
                        elif arrVar[j] == ")":
                            nest -= 1
                            if nest == 0:
                                # if at last character
                                if j == len(arrVar) - 1:
                                    end = j
                                    break
                                # else next character is "*"
                                elif arrVar[j + 1] != "*":
                                    end = j
                                    break
            else:
                # test for last nomial
                if center + 1 == len(refer):
                    # end of structure
                    end = refer[center]["index"] + 1
                elif refer[center]["index"] + 2 < len(arrVar) and arrVar[refer[center]["index"] + 2] == "*":
                    # case of the intermittent monomial
                    for j in range(center, len(refer)):
                        # search for next case of distribution
                        if refer[j]["char"] == "*" and refer[j]["index"] + 1 < len(arrVar) and arrVar[refer[j]["index"] + 1] == "(":
                            # fronttrack to find end
                            nest = 0
                            for k in range(refer[j]["index"], len(arrVar)):
                                if arrVar[k] == "(":
                                    nest += 1
                                elif arrVar[k] == ")":
                                    nest -= 1
                                    if nest == 0:
                                        # if at last character
                                        if k == len(arrVar) - 1:
                                            end = k
                                            break
                                        # else next character isn't "*"
                                        elif arrVar[k + 1] != "*":
                                            end = k
                                            break

                elif refer[center]["index"] + 2 < len(arrVar) and arrVar[refer[center]["index"] + 2] != "*":
                    # no further multiplication in case of distribution
                    end = refer[center]["index"] + 1
            
            # build section
            for j in range(start, end + 1):
                section.append(arrVar[j])
            log_process(section)

            # print(section)
            
            # add parens to intermittent monomials in section for distribution
            for i in range(1, len(section) - 1):
                if section[i + 1] == "*" and section[i - 1] == "*":
                    # restrtucture with parens for each case of intermittent monomials
                    section = restructure(["(", section[i], ")"], i, i, section)

            # reference structure for section with distribution
            sect_struct = []

            # Use section for distribution to create sect_struct
            
            # test for leading monomial
            if section[0] != "(":
                sect_struct.append([[section[0]]]) # monomial
            
            # test middle of sect_struct
            count = 0
            for i in range(0, len(section)):
                # only test on update to prevent false positives
                # positive case indicates index in section for the end of the first nomial
                is_zero = False
                if section[i] == "(":
                    # update count
                    count += 1
                    # test count
                    if count == 0:
                        is_zero = True
                elif section[i] == ")":
                    # update count
                    count -= 1
                    # test count
                    if count == 0:
                        is_zero = True
                
                if is_zero == True:
                    # each zero counted after update count is the last index of another nomial
                    nomial = []
                    term = []
                    nest = 0
                    # backtrack to start of nomial
                    # + identify terms as-you-go
                    for k in range(0, i + 1):
                        char = section[i - k]
                        try:
                            # test for number
                            int(char)
                            # insert character at start of term structure since iterating backward
                            term.insert(0, char)
                        except:
                            # count zeros
                            if char == "(":
                                nest += 1
                                if nest == 0:
                                    # zero identified
                                    nomial.insert(0, term) # add term to polynomial
                                    term = [] # clear term buffer
                                    break

                                elif nest > -2:
                                    # add first character of expression term
                                    term.insert(0, char)

                            elif char == ")":
                                nest -= 1
                            
                            elif nest == -1:
                                if char == "+":
                                    # different term if added
                                    nomial.insert(0, term)
                                    term = [] # clear term buffer
                                elif char == "-":
                                    # different term if subtracted
                                    if section[i - k + 1] == "(":
                                        # negate expression term
                                        term.insert(0, "*")
                                        term.insert(0, "-1")
                                        nomial.insert(0, term)
                                        term = [] # clear term buffer
                                    else:
                                        # negate previous term
                                        term.pop(0) # remove positive value
                                        term.insert(0, "-%s" % section[i - k + 1]) # add negated value
                                        nomial.insert(0, term)
                                        term = [] # clear term buffer
                                elif char == "*" or char == "/":
                                    # same term if multiplied or divided
                                    term.insert(0, char)

                            if nest < -1:
                                term.insert(0, char)

                    sect_struct.append(nomial)
            
            # test for ending monomial
            if section[len(section) - 1] != ")":
                sect_struct.append([[section[len(section) - 1]]])

            # print(sect_struct)

            # total number of nomials
            nomials_total = len(sect_struct)

            # total number of terms
            terms_total = 0
            for i in range(0, len(sect_struct)):
                terms_total += len(sect_struct[i])
            
            # total number of terms in product of distribution
            # calculates the number of terms in the product expression of a nomial multiplication
            # using the nested summation method
            # where it works for:
            #  - any number of nomials
            #  - any number of terms in nomial
            #  - different number of terms in different nomials

            product_terms_total = 0
            for i in range(0, len(sect_struct)):
                # get terms of current nomial
                k = len(sect_struct[i])
                # sum previous terms
                s = 0
                for l in range(0, i):
                    s += len(sect_struct[l])
                s += k
                product_terms_total += k * (terms_total - s)
            
            # print(nomials_total)
            # print(terms_total)
            # print(product_terms_total)

            # construct product expression

            # now that the number of terms in the product expression is known, the number of multiplications is also known,
            # because one multiplication creates one term, so the number of terms and multiplcations are the same number.

            # the design of product expression construction is thus:
            #  - to access two terms in the reference structure of unique combination, 
            #  - build a list which includes those terms separated by a multication symbol,
            #  - compile that list into the product structure, demarcating each concatenation to the product structure with an addition symbol,
            #  - and repeating this process for the number of multiplications,
            #  - except for the last multiplication, which should have no addition symbol following it.

            # multiplier indexes
            term1 = 0
            nomial1 = 0

            # multiplicand indexes
            term2 = 0
            nomial2 = 0

            # structures
            multiplier = []
            multiplicand = []
            product = []

            for i in range(0, product_terms_total - 1):
                # initialize
                if nomial2 == 0:
                    # first term in product expression
                    multiplier = sect_struct[nomial1][term1]
                    nomial2 += 1
                    multiplicand = sect_struct[nomial2][term2]
                
                # update indexes
                # multiplicand term
                    # multiplicand nomial
                        # multiplier term
                            # multiplier nomial

                # multiplicand term
                elif term2 + 1 != len(sect_struct[nomial2]):
                    # mid term in nomial for the multiplicand
                    term2 += 1
                else:
                    # last term of nomial for the multiplicand
                    term2 = 0 # first term of next nomial

                    
                    # multiplicand nomial
                    if nomial2 + 1 != nomials_total:
                        # mid nomial for multiplicand
                        nomial2 += 1
                    else:
                        # last nomial for multiplicand
                        nomial2 = nomial1 + 1


                        # multiplier term
                        if term1 + 1 != len(sect_struct[nomial1]):
                            # mid term of nomial for multiplier
                            term1 += 1
                        else:
                            # last term of nomial for multiplier
                            term1 = 0 # first term of next nomial
                            
                            
                            # multiplier nomial
                            if nomial1 + 1 != nomials_total - 1: # -1 : multiplier never the last nomial
                                # mid nomial for multiplier
                                nomial1 += 1
                                nomial2 = nomial1 + 1
                                term2 = 0
                            else:
                                # last nomial for multiplier
                                break

                # update multiplier
                multiplier = sect_struct[nomial1][term1]
                # update multiplicand
                multiplicand = sect_struct[nomial2][term2]

                # print("nomial: %s" % str(int(nomial2) + 1))
                # print("term: %s" % str(int(term2) + 1))
                # print(multiplier)
                # print(multiplicand)

                # concatenate multiplier and multiplicand with product
                product = product + multiplier + ["*"] + multiplicand + ["+"]

            # last term
            if len(sect_struct[len(sect_struct) - 1]) > 1:
                # for ending monomial
                term2 += 1
                multiplicand = sect_struct[nomial2][term2]
                product = product + multiplier + ["*"] + multiplicand
            else:
                term1 += 1
                multiplier = sect_struct[nomial1][term1]
                product = product + multiplier + ["*"] + multiplicand
            
            log_process(product)

            # restructure with product expression
            arrVar = restructure(product, start, end, arrVar)

            # print(arrVar)

            # identify further distribution
            identify_dist(arrVar)
            if is_dist == False:
                # update bypasses to reflect changes from distribution
                identify_entities(arrVar)

        return arrVar
    # Phase II Process END

    # System Operations
    def get_info():
        # system function for displaying system information in logs
        log_process()
        log_process("System Operations")
        log_process()

        for i in range(0, len(info["system_operations"])):
            log_process(info["system_operations"][i]["name"] + ": " + info["system_operations"][i]["about"])
            log_process()
        
        log_process()
        log_process("Program Entities")
        log_process()

        log_process("Operations")
        for i in range(0, len(info["operations"])):
            log_process(info["operations"][i]["name"] + ": " + info["operations"][i]["syntax"])
            log_process()
        
        log_process("Constants")
        for i in range(0, len(info["constants"])):
            log_process(info["constants"][i]["name"] + ": " + info["constants"][i]["syntax"])
            log_process()

        log_process()
        log_process("Key Functions")
        log_process()

        for module in range(0, len(info["key_functions"])):
            for i in range(0, len(info["key_functions"][module])):
                log_process("Name: " + info["key_functions"][module][i]["name"])
                log_process("Syntax: " + info["key_functions"][module][i]["syntax"])
                log_process("About: " + info["key_functions"][module][i]["about"])
                log_process()
        
    def system_ops(arr):
        # tests for and runs all system functions
        global system_operation

        ref = getIdx("info", arr)
        if ref is not None:
            system_operation = True
            get_info()

        return system_operation

    def evaluate(str):
        # top level function runs high level functions
        global system_operation
        # structure string data
        structure = structure_string(str)
        # test for and run system operation
        system_ops(structure)
        # if no system operations, then continue evaluation
        if system_operation == False:
            # change first log
            if use_logs == "1":
                process_log["0"] = "Process Log Start"
            # Identify program entities in structured string
            identify_entities(structure)
            # restructure to distribute out terms
            structure = distribute(structure)
            # restructure for "sets" (substructures)
            structure = structure_sets(structure)
            # solve section by section
            structure = section(structure)

            return structure

    # Evaluation
    return evaluate(input)

    # use_logs = input["use_logs"]

    # print(input["problem"])
    # answer = evaluate(input["problem"])

    # output = {
    #     "problem": input["problem"],
    #     "answer": answer,
    #     "logs": process_log,
    # }

    # return output
    
#     # TESTING
#     # Simulated Program Input
#     test = {
#         # "problem": "info",
#         # "problem": "sd[[sin(100+4*((-26)+1))],1]+0.5",
#         # "problem": "3*(4-1)", # monomial start 9
#         # "problem": "(2+3)*4", # monomial end 20
#         # "problem": "4*(7-(3-1))", # expression term 17
#         # "problem": "1+(2+3)*4*(7-2)", # monomial intermittent 66
#         # "problem": "1+(2+3)*4+3*2", # monomial intermittent not case 27
#         # "problem": "(2+3)*4*(7-(5-3))", # nested distribution 47
#         # "problem": "1+(1+2)*(3+4)*(5+6)-4", # general 128
#         # "problem": "2*(2+3)", # should be 10

#         # "problem": "expand[[a+b][c][d+e]]", # note
#         "problem": "algexp[[a+b],[2*(2-1)+1]]", # note
#         # "problem": "(1+2)*(3+4)*(5+6)", # note
#         "use_logs": "1",
#     }
#     use_logs = test["use_logs"]

#     # Evaluation
#     answer = evaluate(test["problem"])

#     # Simulated Program Output
#     output = {
#         "problem": test["problem"],
#         "answer": answer,
#         "logs": process_log,
#     }

#     # Prints feedback for program development
#     logs = """"""
#     process_log_keys = list(process_log.keys())
#     for key in process_log_keys:
#         logs += """%s
# """ % process_log[key]

#     print(test["problem"])
#     print(answer)
#     print(logs)
#     # print("Output Object: %s" % output)

# evaluator("") # remove or comment out after testing