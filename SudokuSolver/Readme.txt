*This is a readme file for CS534 HW2
*This file is written by Yunhe Tang in 10/06/2014


Project code includes 2 file:

1. SudokuSolver.py
In this file there is two classes, which are SudokuSolver and AS_node.
    SudokuSolver contains:
	1> some gerneral methods like: printBoard(), isValid() ...
	2> basiclly every method has a prefix name indicating which algorithm it is for
		"SA_" is for simulated annealing
		"AS_" is for A*
		"CSP_" is for CSP
    AS_node is a structure to help with calculation

2. Imp.py
   The main fuction
   When you want to run a algorithm, say simulated annealing, just delete the "#" in imp 3 part, and leave all         other part noted ("# ....")

 
The code is self adaptable for differnet dimenssion of puzzle. Simply change the name of input file to run  differnet puzzle. The file name indicates the dimenssion of puzzle.


For any further question, email: ytang3@wpi.edu
  
	

