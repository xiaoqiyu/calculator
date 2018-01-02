# calculator

 This module is used for the rational number calculation. The calculator support any rational number,e.g. signed/unsigned interger/fraction for the operations of '+,-,*,/', and also support '(',')'. For use cases, please reference to test script (test_bh_calc.py) 

#Useage: 
 * from bh_calc import bh_calc  *
 * bh_calc('1/7+1/7')           *
 
#Workflow
-With the input of the string as a calculation fomular, we first break it downs to list of opeartion numbers and operators.
-Convert the expression list to Reverse Polish notation(RPN) list, ref to function: get_rpn_expr.
-Evaluate the rpn expression list, ref to function: rpn_evaluate
-Formatting the final result.


#Data structure:
In order to keep the precision of the rational number, we use Fraction, which is availabe for python 3.X, to represent the number and calculation.

#Test cases:
The test script demonstrate the test cases which are supported/unsupported in the calculator and the expected results. 
