# Eval API

**Developer**: Blake Thollaug

**Technologies**: Flask, Python, Pip, Numpy

## Overview
Eval API is a backend resource for pythonic cloud calculation. It is developed alongside the GoodEval web computational package in order that the resources it makes available are appropriate for the needs of any software in that package. That said, its resources are general-purpose.

## Program Evolution
In its inception, EvalAPI was neither an evaluator nor an API, but an effort to reconnect and further the relationship between the subjects of computer science and mathematics guided by a princple of generality and created in the form of a software program. The most basic relationship between computer science and mathematics was, of course, that of a calculator, so the original software was a simple script for performing basic mathematical operations like addition, subtraction and so on so forth for the production of a single resulting value. It was dicided that the program should handle an entire expression rather than perform a single operation at a time on a dynamic variable in order to become more general in what it could compute, which resulted in a change in the data type that the program used to represent the problems it computed from numeral type data to string type data. This change in data type made the program excellent at solving arithemetic expressions, and meant that the program had evolved from a calculator into an evaluator imbued with a requirement of operational extensibility, meaning that there were minimal limits to which and how many operations occur in the process of evaluation of any given arithemtic expression.

The change to string type data also presented an opportunity to create a system for using keywords in the process of evaluation. There are primarily two methods in which keys are utilized in EvalAPI's keyword system. The first being a keyword placeholder for common constant values such as pi, and the second being a key function system built thereon, where key function syntax is used to decide which function gets called with which inputs before arithmetic is even calculated. By solving the problems involved in defining and identifying keywords and in designing the key function system upon those solutions, EvalAPI became capable of using all of the computational features of the programming language in which the program was written. Although, the initial focus for key function developemnt was trigonomic such that EvalAPI could be considered scientific-grade in its expression calculations.

While extensibility abided the princple of generality in the program's design, new feature developemnt began to interfere with the performance on simpler expressions. To solve this, the key function system was refactored into a system of modular bypasses to prevent running functionality which was not required to solve a given expression. This was so effective a solution that the rest of the program was refactored to also be modular and bypassable, and modularity became another principle of the program's design.

Due to the nature of the technologies involved, there were some obstacles involved in the implimentation of the program within a web environment, so the majority of its early developement occured apart from any associated interface, and instead was fed test data directly in the development environment with a few assumptions in mind: namely, that the data input into the program would be pre-validated, correctly formatted, be synchronously processed and not time-sensitive in producing its result, and that the interface would eventually handle all of these assumptions. The decision to make the program an API with no single associated interface, in adherence to the princple of generality for program application, therefore presented a number of challenges, where those assumptions had to be handled by the program, instead of any single interface, as a pre-process to evaluation. The avoidance of these problems in earlier development may ostensibly resemble an oversight, but the delay in solving them provided a clear separation of input testing from the evaluation of the input in the overall structure of the program--save for some intermittent error handling--and they did eventually become solved after much of the features for the process of evaluation had been developed.

Increasing the number of key functions, improving the performance of evaluation through an additional principle of modularity, and the completion of evaluation pre-processes to handle initial input errors and intermittent testing to catch errors that arise during the process of evaluation, while beneficial, fail to further the generality of the program's computation, so, as development in those areas underwent, it became increasingly clear that the purpose of the program was even more general than that of the original design. Thus, the process of extending the capability of the program into the realm of symbolic computation began, and its fundamental design has since been established to enable computation for complex symbolic manipulations such as the simplification of algebraic expressions and to introduce key functions in a new algebraic key module that perform lower-order algebraic operations such as polynomial expansion and factorization that rely heavily on symbolic computation capabilities.

By this point, the program was getting large and difficult to manage. There was a pesky reoccuring theme in developemnt, where creation of new functionality would interfere with existing functionality only to be discovered much later on with new features depending on the interference. A diagnostic function served as a solution to this developmental quandary by running all of a growing list of program tests after a new fearture is added to prevent this pesky theme from reoccuring. This also led to the creation of a error code system within the program, which helped to organize and complete due considerations for errors throught the programic process, but especially for making key functions much more robust.

**Data Security**: Contrary to most cases, data security is of lesser concern for EvalAPI. This is primarily due to the nature of the data involved, which is neither sensitive nor personal, but additionally due to the fact that there is no database involved in its operations. That said, basic security precautions are yet abided to protect the operations of the API over a network.

## Developer Resources

**Flask commands**:
 - run development server:      `$flask run`
**pipenv commands**
 - purge dependencies:          `$pipenv uninstall --all`
 - install dependencies:        `$pipenv install`
 - activate shell:              `$pipenv shell`
 - deactivate shell:            `$exit`

 *Note*: run `$pipenv shell` after dependency install and before running server

