import numpy as np

import sys
sys.path.append("..")
from misc import legalMove
from misc import winningTest
from gomokuAgent import GomokuAgent
from copy import deepcopy
import time
import random


class Player(GomokuAgent):
    def __init__(self,ID,BOARDSIZE,X_IN_A_LINE):
        self.ID=ID
        #print(self.ID)
        
        self.opp_id=self.gen_opp_id(self.ID)
        #print(self.opp_id)
        self.BOARDSIZE=BOARDSIZE
        self.X_IN_A_LINE=X_IN_A_LINE
        self.win=([[ID,ID,ID,ID,ID]],100000)
        self.winning_states = ([[0,ID,ID,ID,ID,0]],10000)
        self.defend_winning_states = ([
                                        [-ID,ID,ID,ID,ID,0],
                                        [0,ID,ID,ID,ID,-ID],
                                        [ID,ID,ID,0,ID],
                                        [ID,0,ID,ID,ID],
                                        [ID,ID,0,ID,ID]
                                        ],1000)
        self.winning_three = ([
                                [ID,ID,ID],
                                [ID,ID,0,ID],
                                [ID,0,ID,ID]
                                ],1000)
        self.defend_three = ([
                                [-ID,ID,ID,ID,0,0],
                                [0,0,ID,ID,ID,-ID],
                                [-ID,ID,ID,0,ID,0],
                                [0,ID,0,ID,ID,-ID],
                                [-ID,ID,0,ID,ID,0],
                                [0,ID,ID,0,ID,-ID],
                                [ID,ID,0,0,ID],
                                [ID,0,0,ID,ID],
                                [ID,0,ID,0,ID],
                                [-ID,0,ID,ID,ID,0,-ID],
                                ],100)
        self.two = ([
                    [0,0,ID,ID,0,0],
                    [0,ID,0,ID,0],
                    [0,ID,0,0,ID,0],
                    ],100)
                    
        self.defend_two = ([
                            [-ID,ID,ID,0,0,0],
                            [-ID,ID,0,ID,0,0],
                            [-ID,ID,0,0,ID],
                            [ID,0,0,0,ID],
                            [0,0,0,ID,ID,-ID],
                            [0,0,ID,0,ID,-ID],
                            [ID,0,0,ID,-ID]
                            ],10)
        self.opp_win = self.flip_states(deepcopy(self.win))
        self.opp_winning_states = self.flip_states(deepcopy(self.winning_states))
        #print(self.opp_winning_states)
        self.opp_defend_winning_states = self.flip_states(deepcopy(self.defend_winning_states))
        self.opp_winning_three = self.flip_states(deepcopy(self.winning_three))
        self.opp_defend_three= self.flip_states(deepcopy(self.defend_three))
        self.opp_two=self.flip_states(deepcopy(self.two))
        #print("1111111")
        #print(self.opp_two)
        #print("1111111")
        self.opp_defend_two = self.flip_states(deepcopy(self.defend_two))
        
        
    
    def move(self,board):
        if self.all_zeros(board):
            return (5,5)
        else:
            value, action = self.max_value(board, -99999999,99999999, 0)
            #print(value)
            #print(action)
            
            return action
    
    def max_value(self, board,alpha, beta, depth):
        #print(depth)
        #print(depth)
        if (winningTest(self.opp_id, board, self.X_IN_A_LINE)or depth==2):
            #print(winningTest(self.opp_ID, board, self.X_IN_A_LINE))
            #print("End")
            #print("-->")
            #print("min winning state or depth")
            #print(board)
            #print("<--")
            return (self.evaluate_move(board), (0,0))
        value = -99999999

        temp = self.evaluate_move(board)
        #print(temp)
        #if temp >-100:
        #    possi_moves = self.find_my_moves(board)
        #else:
        #    possi_moves = self.find_opp_moves(board)
        #print("---------------------max---------------------")
        possi_moves = self.find_moves(board, True)
        possi_moves = list(dict.fromkeys(possi_moves))
        #print(possi_moves)
        act = None

        ls = []
        best = (value,(0,0))
        #print("max")
        for move, v in possi_moves:
            #print(move)
            board[move[0],move[1]]=self.ID
            #act = move
            tttv, ttta = self.min_value(board, alpha,beta,depth+1)
            
            cur = (tttv, move)
            #print("{value},{action}, {depth}".format(value = tttv, action = move, depth=depth))
            #value= max(value, tttv)
            best = max(best, cur, key=lambda item:item[0])
            #print("Best is: {best}".format(best=best))
            board[move[0],move[1]]=0
            if best[0]>=beta: 
                #print("hi")
                return best
            alpha = max(alpha, best[0])
        
        return best
    
    def min_value(self, board,alpha, beta, depth):

        if (winningTest(self.ID,board, self.X_IN_A_LINE)):
            
            #print("-->")
            #print("max winning state")
            #print(board)
            #print("<--")
            return (self.evaluate_move(board), (0,0))
        value = 99999999
        #print("---------------------min---------------------")
        possi_moves = self.find_moves(board, False)
        possi_moves = list(dict.fromkeys(possi_moves))
        #print(possi_moves)
        act = None

        ls = []
        best = (value,(0,0))

        for move, v in possi_moves:
            board[move[0],move[1]]=self.opp_id

            tttv, ttta = self.max_value(board, alpha, beta, depth+1)

            cur = (tttv, move)

            best = min(best, cur, key=lambda item: item[0])
            

            board[move[0],move[1]]=0
            if best[0] <=alpha:
                return best
            beta = min(beta, best[0])
        return best
    
    def no_my_stones(self,board):
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r,c]==self.ID:
                    return False
        return True
    
    def find_moves(self,board, mine):
        if self.all_zeros(board):
            return [((5,5),0)]
        elif self.no_my_stones(board):
            if legalMove(board, (5,5)):
                return [((5,5),0)]
            elif legalMove(board,(5,6)):
                return [((5,6),0)]
        else:
            list_of_moves=[]
            for r in range(len(board)):
                for c in range(len(board)):
                    if board[r,c]!=0:
                        if legalMove(board, (r-1,c-1)):
                            if mine:
                                board[r-1,c-1]=self.ID
                                list_of_moves.append(((r-1,c-1), self.evaluate_move(board)))
                                board[r-1,c-1]=0
                            else:
                                board[r-1,c-1]=self.opp_id
                                list_of_moves.append(((r-1,c-1), self.evaluate_move(board)))
                                board[r-1,c-1]=0
                            
                        if legalMove(board, (r-1,c)):
                            if mine:
                                board[r-1,c]=self.ID
                                list_of_moves.append(((r-1,c), self.evaluate_move(board)))
                                board[r-1,c]=0
                            else:
                                board[r-1,c]=self.opp_id
                                list_of_moves.append(((r-1,c), self.evaluate_move(board)))
                                board[r-1,c]=0
                        if legalMove(board, (r-1,c+1)):
                            if mine:
                                board[r-1,c+1]=self.ID
                                list_of_moves.append(((r-1,c+1), self.evaluate_move(board)))
                                board[r-1,c+1]=0
                            else:
                                board[r-1,c+1]=self.opp_id
                                list_of_moves.append(((r-1,c+1), self.evaluate_move(board)))
                                board[r-1,c+1]=0
                        if legalMove(board, (r,c-1)):
                            if mine:
                                board[r,c-1]=self.ID
                                list_of_moves.append(((r,c-1), self.evaluate_move(board)))
                                board[r,c-1]=0
                            else:
                                board[r,c-1]=self.opp_id
                                list_of_moves.append(((r,c-1), self.evaluate_move(board)))
                                board[r,c-1]=0
                        if legalMove(board, (r,c)):
                            #print(1)
                            if mine:
                                board[r,c]=self.ID
                                list_of_moves.append(((r,c), self.evaluate_move(board)))
                                board[r,c]=0
                            else:
                                board[r,c]=self.opp_id
                                list_of_moves.append(((r,c), self.evaluate_move(board)))
                                board[r,c]=0
                        if legalMove(board, (r,c+1)):
                            if mine:
                                board[r,c+1]=self.ID
                                list_of_moves.append(((r,c+1), self.evaluate_move(board)))
                                board[r,c+1]=0
                            else:
                                board[r,c+1]=self.opp_id
                                list_of_moves.append(((r,c+1), self.evaluate_move(board)))
                                board[r,c+1]=0
                        if legalMove(board, (r+1,c-1)):
                            if mine:
                                board[r+1,c-1]=self.ID
                                list_of_moves.append(((r+1,c-1), self.evaluate_move(board)))
                                board[r+1,c-1]=0
                            else:
                                board[r+1,c-1]=self.opp_id
                                list_of_moves.append(((r+1,c-1), self.evaluate_move(board)))
                                board[r+1,c-1]=0
                        if legalMove(board, (r+1,c)):
                            if mine:
                                board[r+1,c]=self.ID
                                list_of_moves.append(((r+1,c), self.evaluate_move(board)))
                                board[r+1,c]=0
                            else:
                                board[r+1,c]=self.opp_id
                                list_of_moves.append(((r+1,c), self.evaluate_move(board)))
                                board[r+1,c]=0
                        if legalMove(board, (r+1,c+1)):
                            if mine:
                                board[r+1,c+1]=self.ID
                                list_of_moves.append(((r+1,c+1), self.evaluate_move(board)))
                                board[r+1,c+1]=0
                            else:
                                board[r+1,c+1]=self.opp_id
                                list_of_moves.append(((r+1,c+1), self.evaluate_move(board)))
                                board[r+1,c+1]=0
            #random.shuffle(list_of_moves)
            if mine:
                list_of_moves.sort(key = lambda item:item[1], reverse=True)
            else:
                list_of_moves.sort(key = lambda item:item[1])
            #print(list_of_moves)
            return list_of_moves[:20]


    
    def all_zeros(self, board):
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c]!=0:
                    return False
        return True
        
    def gen_opp_id(self, id):
        if id==1:
            return -1
        else:
            return 1
          

    


    def evaluate_move(self, board):
        value = 0
        hori_seen=[]
        vert_seen=[]
        diag_1_seen=[]
        diag_2_seen=[]
        #print(value)
        for r in range(len(board)):
            #print(value)
            for c in range(len(board)):
                
                if board[r,c]!=0:
                    hori = board[r]
                    vert = board[:,c]
                    diag_1 = np.array(board).diagonal(c-r)
                    #print(diag_1)
                    diag_2 = np.fliplr(np.array(board)).diagonal((10-c)-r)
                    #if board[r,c]==self.ID:
                    mine = True
                    #print((r,c))
                    #print(diag_1_seen)
                    #print(diag_2_seen)
                    #print(value)
                    if board[r,c]==self.ID:
                        count = np.sum(hori==self.ID)
                        if not ((r,c) in hori_seen):
                            if count ==5:
                                #print(".")
                                value += self.check_pattern(mine, hori, self.win, self.win)
                                hori_seen = self.check_seen_hori(hori,mine,hori_seen, r,c)
                            elif count ==4:
                                #print(".")
                                value+= self.check_pattern(mine, hori, self.winning_states, self.defend_winning_states)
                                hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                            elif count==3:
                                #print(".")
                                value+= self.check_pattern(mine, hori, self.winning_three, self.defend_three)

                                hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                            elif count==2:
                                #print(".")
                                value+= self.check_pattern(mine, hori, self.two, self.defend_two)
                                hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                        count = np.sum(vert==self.ID)
                        if not ((r,c) in vert_seen):
                            if count ==5:
                                #print(".")
                                value += self.check_pattern(mine, vert, self.win, self.win)
                                hori_seen = self.check_seen_hori(vert,mine,vert_seen, r,c)
                            elif count ==4:
                                #print(".")
                                value+= self.check_pattern(mine, vert, self.winning_states, self.defend_winning_states)
                                vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                            elif count==3:
                                #print(".")
                                value+= self.check_pattern(mine, vert, self.winning_three, self.defend_three)
                                vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                            elif count==2:
                                #print(".")
                                value+= self.check_pattern(mine, vert, self.two, self.defend_two)
                                vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                        count = np.sum(diag_1==self.ID)
                        if not ((r,c)in diag_1_seen):
                            if count ==5:
                                #print(".")
                                value += self.check_pattern(mine, diag_1, self.win, self.win)
                                hori_seen = self.check_seen_hori(diag_1,mine,diag_1_seen, r,c)
                            elif count ==4:
                                #print(".")
                                value+= self.check_pattern(mine, diag_1, self.winning_states, self.defend_winning_states)
                                diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                            elif count==3:
                                #print(".")
                                value+= self.check_pattern(mine, diag_1, self.winning_three, self.defend_three)
                                diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                            elif count==2:
                                #print(".")
                                value+= self.check_pattern(mine, diag_1, self.two, self.defend_two)
                                diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                        count = np.sum(diag_2==self.ID)
                        #print("asdf")
                        #print("count = {c}".format(c=count))
                        #print(diag_2)
                        
                        if not ((r,c) in diag_2_seen):
                            if count ==5:
                                #print(".")
                                value += self.check_pattern(mine, diag_2, self.win, self.win)
                                hori_seen = self.check_seen_hori(diag_2,mine,diag_2_seen, r,c)
                            elif count ==4:
                               #print("56")
                                value+= self.check_pattern(mine, diag_2, self.winning_states, self.defend_winning_states)
                                diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                            elif count==3:
                               #print(".")
                                #print("hi")
                                value+= self.check_pattern(mine, diag_2, self.winning_three, self.defend_three)
                                diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                            elif count==2:
                               #print(".")
                                value+= self.check_pattern(mine, diag_2, self.two, self.defend_two)
                                #print( value)
                                diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                    else:
                        count = np.sum(hori==self.opp_id)
                        #print(hori_seen)
                        if not ((r,c) in hori_seen):
                            if count ==5:
                               #print(1)
                                value += self.check_pattern(mine, hori, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(hori,not mine,hori_seen, r,c)
                            if count ==4:
                               #print(2)
                                value+= self.check_pattern(mine, hori, self.opp_winning_states, self.opp_defend_winning_states)
                                hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                            elif count==3:
                               #print(3)
                                value+= self.check_pattern(mine, hori, self.opp_winning_three, self.opp_defend_three)
                                #print("check")
                                hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                            elif count==2:
                               #print(4)
                                value+= self.check_pattern(mine, hori, self.opp_two, self.opp_defend_two)
                                hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                        count = np.sum(vert==self.opp_id)
                        if not ((r,c) in vert_seen):
                            if count ==5:
                               #print(5)
                                value += self.check_pattern(mine, vert, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(vert,not mine,vert_seen, r,c)
                            if count ==4:
                               #print(6)
                                value+= self.check_pattern(mine, vert, self.opp_winning_states, self.opp_defend_winning_states)
                                vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                            elif count==3:
                               #print(7)
                                #print("hi")
                                value+= self.check_pattern(mine, vert, self.opp_winning_three, self.opp_defend_three)
                                vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                            elif count==2:
                               #print(8)
                                #print(self.opp_two)
                                value+= self.check_pattern(mine, vert, self.opp_two, self.opp_defend_two)
                                vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                        count = np.sum(diag_1==self.opp_id)
                        #print("count is {c}".format(c=count))
                        #print(diag_1_seen)
                        if not ((r,c)in diag_1_seen):
                            #print("hi")
                            if count ==5:
                                #print(9)
                                value += self.check_pattern(mine, diag_1, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(diag_1,not mine,diag_1_seen, r,c)
                            if count ==4:
                               #print(10)
                                value+= self.check_pattern(mine, diag_1, self.opp_winning_states, self.opp_defend_winning_states)
                                #print("hi")
                                diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                            elif count==3:
                               #print(11)
                                value+= self.check_pattern(mine, diag_1, self.opp_winning_three, self.opp_defend_three)
                                diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                            elif count==2:
                               #print(12)
                                value+= self.check_pattern(mine, diag_1, self.opp_two, self.opp_defend_two)
                                diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                        count = np.sum(diag_2==self.opp_id)
                        if not ((r,c) in diag_2_seen):
                            if count ==5:
                               #print(13)
                                value += self.check_pattern(mine, diag_2, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(diag_2,not mine,diag_2_seen, r,c)
                            if count ==4:
                               #print(14)
                                value+= self.check_pattern(mine, diag_2, self.opp_winning_states, self.opp_defend_winning_states)
                                diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                            elif count==3:
                               #print(15)
                                value+= self.check_pattern(mine, diag_2, self.opp_winning_three, self.opp_defend_three)
                                diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                            elif count==2:
                               #print(16)
                                value+= self.check_pattern(mine, diag_2, self.opp_two, self.opp_defend_two)
                                #print( "hi")
                                diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                        #print("-----------------------")
                    #print(value)    
        return value
                
    def check_pattern(self, is_my_stone, ls, states_1, states_2):
        value =0
        found=False
        
        for state in states_2[0]:
            if not found:
                #print("---------------------")
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                
                
                for p in possibles:
                    check=ls[p:p+N]
                    #print("check:")
                    #print(check)
                    #print("state")
                    #print(state)
                    if len(check)==len(state):
                        if np.all(check==state):
                            #print("Found")
                            found=True
                            value+=states_2[1]
                #print("---------------------")
            
        for state in states_1[0]:
            #print("Not found: {dd}".format(dd=not found))
            if not found:
            
                #print("---------------------")
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
               #print(possibles)
                
                for p in possibles:
                    #print("ss")
                    
                    check=ls[p:p+N]
                   #print("check:")
                   #print(check)
                   #print("state")
                   #print(state)
                    if len(check)==len(state):
                        if np.all(check==state):
                            found = True
                           #print(found)
                            value+=states_1[1]
                    #print(value)
                #print("---------------------")            
        #print("---------------")
        #print(value)
        #print("value is {v}".format(v=value))
        return value

    def flip_states(self, states):
        states = list(states)
        
        states[1]=states[1]*-1
        states = tuple(states)
        for state in states[0]:
            for i in range(len(state)):
                if state[i]==-1:
                    state[i]=1
                elif state[i]==1:
                    state[i]=-1
        return states
                
    def check_seen_hori(self,ls,mine, seen,r,c):
        if mine:
            
            temp = np.where(ls==self.ID)
            if not len(temp)==0:
                for y,x in zip(np.full(len(temp[0]), r),temp[0]):
                    seen.append((y,x))
        else:
            
            temp = np.where(ls==self.opp_id)
            if not len(temp)==0:
                for y,x in zip(np.full(len(temp[0]), r),temp[0]):
                    seen.append((y,x))
        return seen
    
    def check_seen_vert(self,ls,mine,seen,r,c):
        if mine:
            
            temp = np.where(ls==self.ID)
            if not len(temp)==0:
                for y,x in zip(temp[0], np.full(len(temp[0]), c)):
                    seen.append((y,x))
        else:
            
            temp = np.where(ls==self.opp_id)
            if not len(temp)==0:
                for y,x in zip(temp[0], np.full(len(temp[0]), c)):
                    seen.append((y,x))            
        return seen        
    
    def check_seen_diag_1(self, ls,mine, seen,r,c):
        if mine:
            
            temp = np.where(ls==self.ID)[0]
            if not len(temp)==0:
                
                temp = temp-temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c+i)))
                for i, move in t:
                    seen.append(move)
        else:
            
            temp = np.where(ls==self.opp_id)[0]
            #print(temp)
            if not len(temp)==0:
                temp = temp-temp[0]
                #print(temp)
                t = []
                for i in temp:
                    t.append((i, (r+i,c+i)))
                for i, move in t:
                    seen.append(move)
        #print(seen)
        return seen 
        
    def check_seen_diag_2(self, ls,mine, seen, r,c):
        if mine:
            #print("hi")
            temp = np.where(ls==self.ID)[0]
            #print(temp)
            if not len(temp)==0:
                temp = temp -temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c-i)))
                for i, move in t:
                    #print(move)
                    seen.append(move)
        else:
        
            temp = np.where(ls==self.opp_id)[0]
            if not len(temp)==0:
                temp = temp -temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c-i)))
                for i, move in t:
                    #print(move)
                    seen.append(move)

        return seen 