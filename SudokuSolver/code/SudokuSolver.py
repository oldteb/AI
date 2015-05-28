import numpy as np
import math
import random
import time
from random import randrange
from copy import deepcopy

from math import e


class SudokuSolver:

    dimension = 0
    row_num = col_num = 0
    block_num = 0

    board = 0

    mask = 0

    mark = 0

    # time the algorithm started and ended
    s_time = 0
    e_time = 0

    isOutofTime = False

    minlevel = 100000
    

    # Check if the current value is valid or not
    # Return the number of conflicts if there is any
    def isValid(Self,board):

        err_num = 0;

        for i in xrange(0,Self.row_num):
            err_num += Self.isValid_rc(board[i])

        for i in xrange(0,Self.col_num):
            temp = []
            for j in xrange(0,Self.row_num):
                temp.append(board[j][i])
            err_num += Self.isValid_rc(temp)

        
        i = 0
        while i < int(math.pow(Self.block_num,2)):
            j = 0
            while j < int(math.pow(Self.block_num,2)):
                temp = []
                for m in xrange(0,Self.block_num):
                    for n in xrange(0,Self.block_num):
                        temp.append(board[i+m][j+n])
                        
                err_num += Self.isValid_block(temp)

                j = j + Self.block_num

            i = i + Self.block_num

        
        return err_num


    # Determine if a given row or col is valid
    # Reture the error it find if there is any
    def isValid_rc(Self,list):
        # check if this array makes sense
        err = 0
        count = [0]*(Self.dimension+1)
        for i in list:
            if i != -1:
                count[i] += 1

        for i in count:
            if i > 1:
                err += math.factorial(i)/(2*math.factorial(i-2))

        return err

    # Determine if a given block is valid
    # Reture the conflicts it find except those already-find conflicts 
    def isValid_block(Self,list):
        # check if this array makes sense
        err = 0
        for i in xrange(0,len(list)):
            for j in xrange(i,len(list)):
                if list[i] != -1 and list[j] != -1 and list[i] == list[j]:
                    if i%Self.block_num != j%Self.block_num:
                        if i/Self.block_num != j/Self.block_num:
                            # new conflict detected
                            err += 1
                            

        return err


    # Read in a sudoku problem from a file
    # Store it in a N*N 2D array called board
    def getBoard(Self,filepath):

        # Determine the dimension of the puzzle
        with open(filepath) as f:
            content = f.readline()
            arr = content.strip().split(',')
            Self.dimension = len(arr)
            Self.row_num = Self.col_num = Self.dimension
            Self.block_num = int(math.sqrt(Self.dimension))
            

        # Creates a list containing 9 lists
        board = [[0 for x in xrange(Self.col_num)] for x in xrange(Self.row_num)]

        # Initialize the Board wiht -1


        # Assign the values
        with open(filepath) as f:
            for i in xrange(0,Self.row_num):
                content = f.readline()
                arr = content.strip().split(',')
                for j in xrange(0,Self.col_num):
                    if arr[j] == '?':
                        board[i][j] = -1
                    else:
                        board[i][j] = int(arr[j])


        Self.board = board
        
        return board


    # Print out a board
    # Values are comma seperated
    def printBoard(Self, board):
        for i in xrange(0,Self.row_num):
            for j in xrange(0,Self.col_num):
                if board[i][j] == -1:
                    print'?',
                else:
                    print board[i][j],

                if j != Self.col_num-1:
                    print',',

            print''


    # Use Simulated Annealing to solve Sudoku problem
    # Return the board if problem solved
    def SA_solver(Self, board):

        t = 0
        curr_conf = 0
        next_conf = 0
        T = 1
        prob = 0
        next_state = [0,0,0,0]
        N = [0,0,10000,50000,10000000]

        # mark is to record which value we can not change
        mark = [[0 for x in xrange(Self.col_num)] for x in xrange(Self.row_num)]
        for i in xrange(0,Self.row_num):
            for j in xrange(0,Self.col_num):
                if board[i][j] != -1:   # fix value
                    mark[i][j] = 1
                else:
                    mark[i][j] = 0     # changable value    


        # Assign the board randomly
        if Self.isValid(board) is not 0:
            print "Error input!"
            return
        else:
            Self.SA_init(board)

        # Start simulated annealing
        curr_conf = Self.isValid(board)
        step = 0
        while t < N[Self.block_num] and curr_conf > 0:
            step += 1
            # Get the successor state
            next_state = Self.SA_next(board,mark)
            board[next_state[0]][next_state[1]] = next_state[3]     # Assign new value
            next_conf = Self.isValid(board)

            # Calculate delta E
            dE = next_conf - curr_conf

            # Determin if or not move to next state
            if dE < 0:
                # Move to next state
                curr_conf = next_conf
                t += 1
            else:
                T = Self.SA_temp(t,N)
                if(randrange(1000000) < 1000000*(math.pow(e,-dE/T))):
                    # move to next state
                    curr_conf = next_conf
                    t += 1

                else:
                    # refuse to move to next state, start new iteration
                    board[next_state[0]][next_state[1]] = next_state[2]     # Recover value
                    Self.swap(next_state[0],next_state[1],next_state[2],next_state[3],board)
                    t += 1

        Self.board = board
        
        return board 

    # Use Simulated Annealing to solve Sudoku problem
    # Return the board if problem solved
    def SA_solver2(Self, board):

        # set start time
        Self.s_time = time.time()
        
        t = 0
        curr_conf = 0   # conflicts of old state 
        next_conf = 0   # conflicts of new state
        T = 1           # temperature
        prob = 0
        next_state = [0,0,0,0]      # save old state info for recovery usage
        N = [0,0,10000,200000,10000000]   #  iteration times for different dimenssion
        vlist = []    # keep track of the conflicts to visulize the changing rate

        # mask is to record how many times each cell is being operated
        mask = [[0 for x in xrange(Self.col_num)] for x in xrange(Self.row_num)]
        for i in xrange(0,Self.row_num):
            for j in xrange(0,Self.col_num):
                mask[i][j] = 0
        Self.mask = mask

        # mark is to record which value we can not change
        mark = [[0 for x in xrange(Self.col_num)] for x in xrange(Self.row_num)]
        for i in xrange(0,Self.row_num):
            for j in xrange(0,Self.col_num):
                if board[i][j] != -1:   # fix value
                    mark[i][j] = 1
                else:
                    mark[i][j] = 0     # changable value    


        # Assign the board randomly
        if Self.isValid(board) is not 0:
            print "Error input!"       # input board contains conflicts
            return
        else:
            Self.SA_init2(board)       # initilize the board, and print it out


        # Start simulated annealing
        curr_conf = Self.isValid(board)
        # print "init",curr_conf
        step = 0
        while t < N[Self.block_num] and curr_conf > 0:
            # if running time exceedes 5 mins
            if Self.checkTime() == False:
                return False
            step += 1
            #print curr_conf
            vlist.append(curr_conf)
            # Get the successor state
            next_state = Self.SA_next2(board,mark)
            #board[next_state[0]][next_state[1]] = next_state[3]     # Assign new value
            next_conf = Self.isValid(board)

            # Calculate delta E
            dE = next_conf - curr_conf

            # Determin if or not move to next state
            T = Self.SA_temp(t,N)
            r = random.uniform(0, 1.0)
            q = math.pow(e,-float(dE)/T)
            # print T
            if q > r:
                curr_conf = deepcopy(next_conf)
                t += 1
                #print ">"
            else:
                #print next_state
                Self.swap(next_state[0],next_state[1],next_state[2],next_state[3],board)
                t += 1

            
        Self.e_time = time.time() - Self.s_time
        Self.board = board


        # Visulize
        file_obj = open('d:/aaaa.csv','w')
        for i in range(len(vlist)):
            file_obj.write(str(i) + "," + str(vlist[i]) + "\n")

        file_obj.close()
        
        return board 

    

    # Generate initial state
    def SA_init(Self,board):
        for i in xrange(0,Self.row_num):
            for j in xrange(0,Self.col_num):
                if board[i][j] == -1:
                    board[i][j] = random.randint(1,Self.dimension)

        return board

    # Generate initial state version 2
    def SA_init2(Self,board):
        i = 0
        while i < Self.dimension:
            j = 0
            while j < Self.dimension:
                temp = [0]*(Self.dimension+1)
                s = 1
                for m in xrange(0,Self.block_num):
                    for n in xrange(0,Self.block_num):
                        if board[i+m][j+n] != -1:
                            temp[board[i+m][j+n]] = 1
                for m in xrange(0,Self.block_num):
                    for n in xrange(0,Self.block_num):
                        if board[i+m][j+n] == -1:
                            while temp[s] == 1:
                                s += 1
                            board[i+m][j+n] = s
                            s += 1

                j = j + Self.block_num

            i = i + Self.block_num

        # print out the board
        # Self.printBoard(board)



    # Temperature schedule function
    # T0 = 2  15 14
    # Tn = 0.3  3  2.5
    # N = 100000    e,-dE/T
    def SA_temp(Self,t,N):

        # No.1
        #T = 100 - t * ((99.99999)/N[Self.block_num])
        # T = -0.0023 * t + 14
        # No.6
        # T = 0.5*(11.5)*(1+math.cos((t*math.pi)/N[Self.block_num]))+2.5
        # No.2
        #T = math.pow(float(4)/float(15),float(t)/N[Self.block_num])
        # No.3
        # A = (-11.5 * (N[Self.block_num]+1))/N[Self.block_num]
        # B = float(14) - A
        #T = A/float(t+1) + B
        # T = 1/(0.00005*t + 1.99995)
        T = 0.05*(t-1)/(N[Self.block_num]-1)+0.3

        return T

    # Get the successor state
    def SA_next(Self,board,mark):

        # pick up a value randomly and assign a random value to it
        # Can not change the original one
        i = randrange(Self.dimension)
        j = randrange(Self.dimension)
        while mark[i][j] == 1:
            i = randrange(Self.dimension)
            j = randrange(Self.dimension)

        return [i,j,board[i][j],random.randint(1,Self.dimension)]

    # Get the successor state version 2
    def SA_next2(Self,board,mark):

        # pick up a value randomly and assign a random value to it
        # Can not change the original one
        i = randrange(Self.dimension)
        j = randrange(Self.dimension)
        i = int(i/Self.block_num) * Self.block_num
        j = int(j/Self.block_num) * Self.block_num
        m1 = randrange(Self.block_num)
        n1 = randrange(Self.block_num)
        while mark[i+m1][j+n1] == 1:
            m1 = randrange(Self.block_num)
            n1 = randrange(Self.block_num)
        m2 = randrange(Self.block_num)
        n2 = randrange(Self.block_num)
        while mark[i+m2][j+n2] == 1:
            m2 = randrange(Self.block_num)
            n2 = randrange(Self.block_num)

        # print i+m1,j+n1,i+m2,j+n2
        Self.swap(i+m1,j+n1,i+m2,j+n2,board)
        
        

        return [i+m1,j+n1,i+m2,j+n2]


    def swap(Self,x1,y1,x2,y2,board):
        swap = board[x2][y2]
        board[x2][y2] = board[x1][y1]
        board[x1][y1] = swap

        #Self.mask[x1][y1] += 1
        #Self.mask[x2][y2] += 1
        

        
        

    




    def AS_solver(Self, board):

        # set start time
        Self.s_time = time.time()

        if Self.isValid(board) != 0:
            print "Error input!"       # input board contains conflicts
            return

        # A* start
        nextcell = Self.AS_getNextCell(board)
        if nextcell[0].fn_value == 1000000:
            return

        # print nextcell[0].aval_list
        while len(nextcell[0].aval_list) > 0:
            v = deepcopy(nextcell[0].aval_list[0])
            del nextcell[0].aval_list[0]
            # print v
            if Self.AS_solve_rcr(board,nextcell[1],nextcell[2],v) == True:
                Self.e_time = time.time() - Self.s_time
                return True

        return False



    def AS_solve_rcr(Self, board, i, j, value):

        # level1 = deepcopy(level)
        # loop = 0
        
        if Self.isOutofTime == True:
            return False

        # if running time exceedes 5 mins
        if Self.checkTime() == False:
            Self.isOutofTime = True
            return False
        
        nextcell = 0

        #print i,j,value
        
        board[i][j] = deepcopy(value)

        # get next taget cell
        nextcell = Self.AS_getNextCell(board)
        # check if nextcell is valid
        if nextcell[0].fn_value == 1000000:
            # reach the bottom, solution found
            return True
        elif len(nextcell[0].aval_list) == 0:
            # bad end reached
            # print "backtrack"

            return False

        
        while len(nextcell[0].aval_list) > 0:
            # print nextcell[1],nextcell[2],nextcell[0].aval_list
            # print level1
            #if loop == 1 and level1 < Self.minlevel:
             #   Self.minlevel = deepcopy(level1)
              #  print level1
            v = deepcopy(nextcell[0].aval_list[0])
            del nextcell[0].aval_list[0]
            if Self.AS_solve_rcr(board,nextcell[1],nextcell[2],v) == True:
                return True
            # recover from last change
            board[nextcell[1]][nextcell[2]] = -1
            #loop = 1


        return False
    
        
        
    def AS_getNextCell(Self, board):
        # In this function, only fn is changed
        # it will reture the next location
        x = -1
        y = -1
        min_node = AS_node()
        min_node.fn_value = 1000000    # 100000 stands for infinite large here
        for i in range(Self.row_num):
            for j in range(Self.col_num):
                if board[i][j] == -1:
                    temp_node = Self.AS_calculateCell(board,i,j)
                    if min_node.fn_value > temp_node.fn_value:
                        # min_node.fn_value = deepcopy(temp_node.fn_value)
                        # min_node.aval_list = deepcopy(temp_node.aval_list)
                        min_node = temp_node
                        x = deepcopy(i)
                        y = deepcopy(j)

        # here if min_node.fn_value == 1000000, meaning all cells are assigned
        # if min_node.fn_value == 0, bad end reached, trace back
        # otherwise, optimal cell found

        # print x,y,min_node.fn_value,min_node.aval_list

        return [min_node, x, y]
                
                
        


    # reture a AS_node
    def AS_calculateCell(Self,board,i,j):
        g = 0
        h = [0]*(Self.dimension+1)

        # for ith row
        for m in range(Self.col_num):
            if m != j:
                if board[i][m] != -1:
                    g += 1
                    h[board[i][m]] += 1


        # for jth col
        for n in range(Self.row_num):
            if n != i:
                if board[n][j] != -1:
                    g += 1
                    h[board[n][j]] += 1

        
        # for the block that [i,j] is located in
        x = int(i/Self.block_num) * Self.block_num
        y = int(j/Self.block_num) * Self.block_num
        for m in range(Self.block_num):
            for n in range(Self.block_num):
                if x+m != i and y+n != j:   # not in same row and col but in same block
                    if board[x+m][y+n] != -1:
                        g += 1
                        h[board[x+m][y+n]] += 1

        # get fn
        m = 1
        asn = AS_node()
        asn.aval_list = []
        while m < len(h):
            if h[m] == 0:
                asn.aval_list.append(m)
            m += 1

        fn = g + len(asn.aval_list)

        asn.fn_value = fn
        # print ">>>",i,j,fn,asn.aval_list


        return asn







    # CSP 
    def CSP_solver(Self, board):
        # set start time
        Self.s_time = time.time()
        
        if Self.isValid(board) != 0:
            print "Error input!"       # input board contains conflicts
            return

        # use Degree Heuristic to choose a starting point
        start_point = Self.CSP_getStartPoint(board)


        while len(start_point[0].aval_list) > 0:
            v = deepcopy(start_point[0].aval_list[0])
            del start_point[0].aval_list[0]
            if Self.CSP_solve_rcr(board,start_point[1],start_point[2],v) == True:
                Self.e_time = time.time() - Self.s_time
                return True

        return False

    def CSP_solve_rcr(Self, board, i, j, value):
        if Self.isOutofTime == True:
            return False

        # if running time exceedes 5 mins
        if Self.checkTime() == False:
            Self.isOutofTime = True
            return False
        
        nextcell = 0

        #print i,j,value
        
        board[i][j] = deepcopy(value)
        #print "apply",i,j,value
        
        # get next taget cell
        nextcell = Self.CSP_getNextCell(board)
        # check if all the cells have been assigned
        if nextcell[1] == -1:
            # reach the bottom, solution found
            return True
        elif len(nextcell[0].aval_list) == 0:
            # bad end reached
            # print "backtrack"
            return False

        # use Least-constraining-value heuristic to decide which value to pick first
        dict = Self.CSP_getLeastConstrain(board,nextcell[1],nextcell[2],nextcell[0])
        while len(dict) > 0:
            dic = deepcopy(dict[0])
            del dict[0]
            #curvaluel = dict.popitem()
            if Self.CSP_solve_rcr(board,nextcell[1],nextcell[2],int(dic[0])) == True:
                return True
        # recover from last change
        board[nextcell[1]][nextcell[2]] = -1

        
        return False


    def CSP_getStartPoint(Self, board):
        # it will reture the next location
        x = -1
        y = -1
        max_node = AS_node()
        max_node.aval_list = []
        max_node.fn_value = -1   # -1 stands for infinite small here
        for i in range(Self.row_num):
            for j in range(Self.col_num):
                if board[i][j] == -1:
                    temp_node = Self.CSP_getCellAval(board,i,j)
                    if max_node.fn_value < temp_node.fn_value:
                        max_node = temp_node
                        x = deepcopy(i)
                        y = deepcopy(j)

        # here if x == -1, meaning all cells are assigned
        # if len(min_node.aval_list) == 0, bad end reached, trace back
        # otherwise, optimal cell found

        # print x,y,max_node.fn_value,max_node.aval_list

        return [max_node, x, y]
    


    # use Minimum remaining values Heuristic to decide next point
    def CSP_getNextCell(Self, board):
        # it will reture the next location
        x = -1
        y = -1
        min_node = AS_node()
        min_node.aval_list = []
        min_node.fn_value = 1000000   # 1000000 stands for infinite small here
        for i in range(Self.row_num):
            for j in range(Self.col_num):
                if board[i][j] == -1:
                    temp_node = Self.CSP_getCellAval(board,i,j)
                    if min_node.fn_value > temp_node.fn_value:
                        min_node = temp_node
                        x = deepcopy(i)
                        y = deepcopy(j)

        # here if x == -1, meaning all cells are assigned
        # if len(min_node.aval_list) == 0, bad end reached, trace back
        # otherwise, optimal cell found

        # print x,y,min_node.fn_value,min_node.aval_list

        return [min_node, x, y]


    



    # return the number of the unssigned cells that related to cell(i,j)
    def CSP_getCellAval(Self, board, i, j):
        g = 0
        h = [0]*(Self.dimension+1)

        # for ith row
        for m in range(Self.col_num):
            if m != j:
                if board[i][m] == -1:
                    g += 1
                else:
                    h[board[i][m]] += 1


        # for jth col
        for n in range(Self.row_num):
            if n != i:
                if board[n][j] == -1:
                    g += 1
                else:
                    h[board[n][j]] += 1

        
        # for the block that [i,j] is located in
        x = int(i/Self.block_num) * Self.block_num
        y = int(j/Self.block_num) * Self.block_num
        for m in range(Self.block_num):
            for n in range(Self.block_num):
                if x+m != i and y+n != j:   # not in same row and col but in same block
                    if board[x+m][y+n] == -1:
                        g += 1
                    else:
                        h[board[x+m][y+n]] += 1

        # get fn
        m = 1
        asn = AS_node()
        asn.aval_list = []
        while m < len(h):
            if h[m] == 0:
                asn.aval_list.append(m)
            m += 1

        
        asn.fn_value = g   # fn_value maintains number of empty cells
        # print ">>>",asn.fn_value,asn.aval_list


        return asn


    # use Least-constraining-value heuristic to decide which value to pick first
    # return a sorted dictionary of the static 
    def CSP_getLeastConstrain(Self,board,i,j,node):

        static = [0]*(len(node.aval_list) + 1)
        dic = {}
        
        
        for m in range(Self.col_num):
            # for ith row
            if m != j:
                if board[i][m] == -1:
                    temp_node = Self.CSP_getCellAval(board, i, m)
                    for c in range(len(temp_node.aval_list)):
                        for t in range(len(node.aval_list)):
                            if temp_node.aval_list[c] == node.aval_list[t]:
                                static[t+1] += 1
            # for jth col
            if m != i:
                if board[m][j] == -1:
                    temp_node = Self.CSP_getCellAval(board, m, j)
                    for c in range(len(temp_node.aval_list)):
                        for t in range(len(node.aval_list)):
                            if temp_node.aval_list[c] == node.aval_list[t]:
                                static[t+1] += 1


        
        # for the block that [i,j] is located in
        x = int(i/Self.block_num) * Self.block_num
        y = int(j/Self.block_num) * Self.block_num
        for m in range(Self.block_num):
            for n in range(Self.block_num):
                if x+m != i and y+n != j:   # not in same row and col but in same block
                    if board[x+m][y+n] == -1:
                        temp_node = Self.CSP_getCellAval(board, x+m, y+n)
                        for c in range(len(temp_node.aval_list)):
                            for t in range(len(node.aval_list)):
                                if temp_node.aval_list[c] == node.aval_list[t]:
                                    static[t+1] += 1

        # generate dictionary
        for c in range(len(node.aval_list)):
            dic[node.aval_list[c]] = int(static[c+1])

        # sort the dic
        # sort according to the value small to large
        
        dict = sorted(dic.iteritems(), key=lambda d:d[1])

        return dict

    def checkTime(Self):
        if time.time() - Self.s_time >= 300:
            return False
        else:
            return True

# A node contained fn value and list of available value
class AS_node:

    fn_value = 0
    aval_list = []
    
