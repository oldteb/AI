from __future__ import print_function
from random import shuffle, random, sample, randint, randrange
from copy import deepcopy
import math
import fileinput
import time
import sys

global board_size
global block_size

def print_board(m):
    for i in range (board_size):
        for j in range(board_size):
            print(str(m[i][j]).rjust(3),end = '')
            if j%block_size == block_size -1:
                print (" |",end = '')
        print()
        if i%block_size == block_size -1:
            print("-"*int(block_size*(3*block_size+2)))

def get_block(m,b_row,b_col):
    block = []
    for i in range (block_size):
        for j in range (block_size):
            block.append(m[i+b_row*block_size][j+b_col*block_size])
    return block

def check(m):
    conflict = 0
    for i in range(board_size):
        filtered = filter(lambda x:x!=0, m[i])
        if len(filtered)-len(set(filtered))>0:
            conflict += 1
        l = [m[j][i] for j in range (board_size)]
        filtered = filter(lambda x:x!=0, l)
        if len(filtered)-len(set(filtered))>0:
            conflict +=1
    for i in range (block_size):
        for j in range (block_size):
            l = get_block(m,i,j)
            filtered = filter(lambda x:x!=0, l)
            if len(filtered)-len(set(filtered))>0:
                conflict += 1
    return conflict

def fill_block(m,b_row,b_col):
    val_list = []
    for i in range (1, board_size+1):
        val_list.append (int(i))
    for i in range (block_size):
        for j in range(block_size):
            if m[i+b_row*block_size][j+b_col*block_size]!= 0:
                val_list.remove(int(m[i+b_row*block_size][j+b_col*block_size]))
    for i in range (block_size):
        for j in range(block_size):
            if m[i+b_row*block_size][j+b_col*block_size] == 0:
                index = randrange(len(val_list))
                m[i+b_row*block_size][j+b_col*block_size] = val_list[index]
                val_list.remove(m[i+b_row*block_size][j+b_col*block_size])

def init(m):
    for i in range(block_size):
        for j in range(block_size):
            fill_block(m,i,j)

def get_zero_block(m,row,col):
    zero_indices = []
    for r in range(block_size):
        for c in range(block_size):
            if m[row + r][col + c] == 0:
                zero_indices.append((row+r,col+c))
    return zero_indices

def fit_func0(m):
    res = []
    score = 0
    for i in range (board_size):
        row = [m[i][j] for j in range (board_size)]
        row_score = -len(set(row))
        score += row_score
        res.append(row_score)
    for i in range (board_size):
        col = [m[j][i] for j in range (board_size)]
        col_score = -len(set(col))
        score += col_score
        res.append(col_score)
    res.append(score)
    return res

def pick_worst(l):
    worst = -sys.maxint-1
    for i in range (len(l)):
        temp = fit_func0(l[i])[2*board_size]
        if temp> worst:
            worst = temp
            res = deepcopy(l[i])
    return [res,worst]

def pick_best(l):
    best = sys.maxint
    for i in range (len(l)):
        temp = fit_func0(l[i])[2*board_size]
        if temp< best:
            best = temp
            res = deepcopy(l[i])
    return [res,best]

def pick(sample_list):
    res = []
    tournament1 = sample(sample_list,3)
    res.append(pick_best(tournament1)[0])
    tournament2 = sample(sample_list,3)
    res.append(pick_best(tournament2)[0])
    return res
    
def cross_over(parents):
    x = random()
    child0 = []
    child1 = []
    for i in range (board_size):
        child1.append([])
    if x<0.3 :
        p0_score = fit_func0(parents[0])
        p1_score = fit_func0(parents[1])
        for i in range (block_size):
            p0 = sum(p0_score[i*block_size:i*block_size+3])
            p1 = sum(p1_score[i*block_size:i*block_size+3])
            if(p0<p1):
                child0+= parents[0][i*block_size : i*block_size+3]
            else:
                child0+= parents[1][i*block_size : i*block_size+3]
        for i in range (block_size):
            p0 = sum(p0_score[board_size+i*block_size:board_size+i*block_size+3])
            p1 = sum(p1_score[board_size+i*block_size:board_size+i*block_size+3])
            if (p0<p1):
                for j in range (board_size):
                    child1[j]+=parents[0][j][i*block_size : i*block_size+3]
            else:
                for j in range (board_size):
                    child1[j]+=parents[1][j][i*block_size : i*block_size+3]
        return [child0,child1]
    else:
        return parents


def mutation(children,input_m):
    res = []
    for i in range (2):
        temp = []
        for j in range (3):
            news = deepcopy(children[i])
            x = random()
            if (x<1):
                randblk = randint(0,board_size - 1)
                row = block_size*(randblk //block_size)
                col = block_size* (randblk %block_size)
                swap_indices = get_zero_block(input_m, row, col)
                if len(swap_indices) >=2:
                    rand1, rand2 = sample (range(len(swap_indices)), 2)
                    r1 = swap_indices[rand1][0]
                    c1 = swap_indices[rand1][1]
                    r2 = swap_indices[rand2][0]
                    c2 = swap_indices[rand2][1]
                    news[r1][c1],news[r2][c2] = news[r2][c2],news[r1][c1]
            temp.append(news)
        best = pick_best(temp)
        res.append(best[0])
    return res

def GA_solver(input_m):
    sample_list = []
    total = -1
    for i in range (150):
        temp = deepcopy(input_m)
        init(temp)
        sample_list.append(temp)

    best = pick_best(sample_list)
    if (best[1] == -162):
        print (total)
        return best[0]
    else:
        while (best[1] != -162):
            total+=1
            parents = pick(sample_list)
            children = cross_over(parents)
            children = mutation(children, input_m)
            best = pick_best(children)
            if (total % 5000 ==0):
                print (best[1])
                print_board(best[0])
            sample_list+= children

            x = random()
            if (x<0.3):
                worst = pick_worst(sample_list)
                sample_list.remove(worst[0])
                worst = pick_worst(sample_list)
                sample_list.remove(worst[0])
            else:
                to_remove = sample(sample_list, 2)
                sample_list.remove(to_remove[0])
                sample_list.remove(to_remove[1])
            
            
        print (total)
        return best[0]
    


s_time = time.time()
if __name__=="__main__":
    m = []

    for line in fileinput.input('sudoku9_2.txt'):
        line_int = []
        line_word = line.strip().split(',')
        board_size = len(line_word)
        block_size = int(math.sqrt(board_size))

        for i in line_word:
            if i == '?':
                line_int.append(int(0))
            else:
                line_int.append(int(i))
        m.append(line_int)
    fileinput.close()
    print("Input sudoku:")
    print_board(m)
    if check(m)!=0:
        print("Invalid input")
        sys.exit()
    input_m = deepcopy(m)
    #init(m)
    solution = GA_solver(input_m)
    print ("solution found.")
    print_board(solution)
    
    #res = SA_solver(m,input_m)
    #m = deepcopy(res[1])
    #if res[0]:
    #    print("solution found:")
    #else:
    #    print("failed. last step:")

    print("Runtime: {:.2f} seconds".format(time.time() - s_time))
