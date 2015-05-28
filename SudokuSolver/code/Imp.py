from SudokuSolver import SudokuSolver
from SudokuSolver import AS_node
from copy import deepcopy


def main():

    ss = SudokuSolver()
    print "Algorithm is running..."
    print "Running time limit: 5 mins"
    
    # Imp 1
    #ss.printBoard(ss.getBoard("sudoku9_1.txt"))

    # Imp 2
    #print ss.isValid(ss.getBoard("sudoku4_1.txt"))

    # Imp 3
    #if ss.SA_solver2(ss.getBoard("sudoku9_9.txt")) != False:
    #    ss.printBoard(ss.board)
    #    print "Conflicts:",ss.isValid(ss.board)
    #    print "Time used:",int(ss.e_time),"secs"
    #else:
    #    print "No solution found."


    # Imp 4
    #if ss.AS_solver(ss.getBoard("sudoku9_8.txt")) == True:
    #    ss.printBoard(ss.board)
    #    print "Conflicts:",ss.isValid(ss.board)
    #    print "Time used:",int(ss.e_time),"secs"
    #else:
    #    print "No solution found."


    # Imp 5    
    if ss.CSP_solver(ss.getBoard("sudoku9_8.txt")) == True:
        ss.printBoard(ss.board)
        print "Conflicts:",ss.isValid(ss.board)
        print "Time used:",int(ss.e_time),"secs"
    else:
        print "No solution found."



if __name__ == '__main__':
    main()
