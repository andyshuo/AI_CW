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
            print(value)
            print(action)
            
            return action
    
    def max_value(self, board,alpha, beta, depth):
        #print(depth)
        
        if (winningTest(self.opp_id, board, self.X_IN_A_LINE)or depth>1):
            #print(winningTest(self.opp_ID, board, self.X_IN_A_LINE))
            #print("End")
            return (self.evaluate_move(board), (0,0))
        value = -99999999

        temp = self.evaluate_move(board)
        #print(temp)
        #if temp >-100:
        #    possi_moves = self.find_my_moves(board)
        #else:
        #    possi_moves = self.find_opp_moves(board)
        possi_moves = self.find_moves(board)

        act = None

        ls = []
        best = (value,(0,0))
        #print("max")
        for move in possi_moves:
            
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
        #print(depth)
        if (winningTest(self.ID,board, self.X_IN_A_LINE)):
            #print(board)
            #print("End")
            #print(self.evaluate_move(board))
            return (self.evaluate_move(board), (0,0))
        value = 99999999
        #board_value = self.evaluate_move(board)
        
        #if board_value>-70 and board_value<0:
        #    possi_moves = self.find_opp_moves(board)
        #elif board_value>=0:
        #    possi_moves = self.find_my_moves(board)
        #else:
        #    possi_moves = self.find_opp_moves(board)
        #temp = self.evaluate_move(board)
        #if temp <100:
        #    possi_moves=self.find_opp_moves(board)
        #else:
        #    possi_moves = self.find_my_moves(board)
        possi_moves = self.find_moves(board)
        #possi_moves = self.find_moves(board)
        #possi_moves = list(dict.fromkeys(possi_moves))
        #possi_moves = possi_moves
        act = None
        #print(board_value)
        #print(len(possi_moves))
        #possi_moves = possi_moves[:10]
        ls = []
        best = (value,(0,0))
        #print("min")
        for move in possi_moves:
            board[move[0],move[1]]=self.opp_id
            #act = move
            tttv, ttta = self.max_value(board, alpha, beta, depth+1)
            #print("{value},{action}, {depth}".format(value = tttv, action = ttta, depth=depth))
            cur = (tttv, move)
            #print(tttv)
            #print("Best compare in min: {value} vs {best}".format(value=value, best=cur[0]))
            #print("Best compare in min: {value} vs {best}".format(value=value, best=cur[0]))
            best = min(best, cur, key=lambda item: item[0])
            
            #value= min(value, tttv)
            board[move[0],move[1]]=0
            if best[0] <=alpha:
                #print("HI min")
                return best
            beta = min(beta, best[0])
        return best
    
    #def move(self, board):
       # return (0,0)
    
    def no_my_stones(self,board):
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r,c]==self.ID:
                    return False
        return True
    
    def find_moves(self,board):
        if self.all_zeros(board):
            return [(5,5)]
        elif self.no_my_stones(board):
            if legalMove(board, (5,5)):
                return [(5,5)]
            elif legalMove(board,(5,6)):
                return [(5,6)]
        else:
            list_of_moves=[]
            for r in range(len(board)):
                for c in range(len(board)):
                    if board[r,c]!=0:
                        if legalMove(board, (r-1,c-1)):
                            list_of_moves.append((r-1,c-1))
                        if legalMove(board, (r-1,c)):
                            list_of_moves.append((r-1,c))
                        if legalMove(board, (r-1,c+1)):
                            list_of_moves.append((r-1,c+1))
                        if legalMove(board, (r,c-1)):
                            list_of_moves.append((r,c-1))
                        if legalMove(board, (r,c)):
                            list_of_moves.append((r-1,c))
                        if legalMove(board, (r,c+1)):
                            list_of_moves.append((r,c+1))
                        if legalMove(board, (r+1,c-1)):
                            list_of_moves.append((r+1,c-1))
                        if legalMove(board, (r+1,c)):
                            list_of_moves.append((r+1,c))
                        if legalMove(board, (r+1,c+1)):
                            list_of_moves.append((r+1,c+1))
            random.shuffle(list_of_moves)
            return list_of_moves
    
    def find_my_moves(self, board):
        if self.all_zeros(board):
            return [(5,5)]
        elif self.no_my_stones(board):
            if legalMove(board,(5,5)):
                return[(5,5)]
            elif legalMove(board,(5,6)):
                return [(5,6)]
        else:
            list_of_moves=[]
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r,c]==self.ID:
                        if  r!=0 and c!=0:
                            if board[r-1,c-1]==0:
                                list_of_moves.append((r-1,c-1))
                        if r!=0:
                            if board[r-1,c]==0:
                                list_of_moves.append((r-1,c))
                        if r!=0 and c!=10:
                            if board[r-1,c+1]==0:
                                list_of_moves.append((r-1,c+1))
                        if c!=0:
                            if board[r,c-1]==0:
                                list_of_moves.append((r,c-1))
                        if c!=10:
                            if board[r,c+1]==0:
                                list_of_moves.append((r,c+1))
                        if r!=10 and c!=0:
                            if board[r+1,c-1]==0:
                                list_of_moves.append((r+1,c-1))
                        if r!=10:
                            if board[r+1,c]==0:
                                list_of_moves.append((r+1,c))
                        if r!=10 and c!=10: 
                            if board[r+1,c+1]==0:
                                list_of_moves.append((r+1,c+1))
            #print("length: {l}".format(l=len(list_of_moves)))
            random.shuffle(list_of_moves)
            return list_of_moves
    
    def find_opp_moves(self,board):
        if self.all_zeros(board):
            return [(5,5)]
        else:
            list_of_moves=[]
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r,c]==self.opp_id:
                        if  r!=0 and c!=0:
                            if board[r-1,c-1]==0:
                                list_of_moves.append((r-1,c-1))
                        if r!=0:
                            if board[r-1,c]==0:
                                list_of_moves.append((r-1,c))
                        if r!=0 and c!=10:
                            if board[r-1,c+1]==0:
                                list_of_moves.append((r-1,c+1))
                        if c!=0:
                            if board[r,c-1]==0:
                                list_of_moves.append((r,c-1))
                        if c!=10:
                            if board[r,c+1]==0:
                                list_of_moves.append((r,c+1))
                        if r!=10 and c!=0:
                            if board[r+1,c-1]==0:
                                list_of_moves.append((r+1,c-1))
                        if r!=10:
                            if board[r+1,c]==0:
                                list_of_moves.append((r+1,c))
                        if r!=10 and c!=10: 
                            if board[r+1,c+1]==0:
                                list_of_moves.append((r+1,c+1))
            #print("length: {l}".format(l=len(list_of_moves)))
            random.shuffle(list_of_moves)
            return list_of_moves
    
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
          

    
    def evaluate_board(self, board):
        #start_time = time.time()
        value = self.evaluate_attack(board)+self.evaluate_defense(board)
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c]==self.ID:
                    value+=1
                elif board[r][c]==self.opp_id:
                    value-=1

        return value

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
                    
                    #print(diag_2_seen)
                    #print(value)
                    
                    count = np.sum(hori==self.ID)
                    if not ((r,c) in hori_seen):
                        if count ==5:
                            value += self.check_pattern(mine, hori, self.win, self.win)
                            hori_seen = self.check_seen_hori(hori,mine,hori_seen, r,c)
                        elif count ==4:
                            value+= self.check_pattern(mine, hori, self.winning_states, self.defend_winning_states)
                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                        elif count==3:
                            value+= self.check_pattern(mine, hori, self.winning_three, self.defend_three)

                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                        elif count==2:
                            value+= self.check_pattern(mine, hori, self.two, self.defend_two)
                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                    count = np.sum(vert==self.ID)
                    if not ((r,c) in vert_seen):
                        if count ==5:
                            value += self.check_pattern(mine, vert, self.win, self.win)
                            hori_seen = self.check_seen_hori(vert,mine,vert_seen, r,c)
                        elif count ==4:
                            value+= self.check_pattern(mine, vert, self.winning_states, self.defend_winning_states)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                        elif count==3:
                            value+= self.check_pattern(mine, vert, self.winning_three, self.defend_three)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                        elif count==2:
                            value+= self.check_pattern(mine, vert, self.two, self.defend_two)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                    count = np.sum(diag_1==self.ID)
                    if not ((r,c)in diag_1_seen):
                        if count ==5:
                            value += self.check_pattern(mine, diag_1, self.win, self.win)
                            hori_seen = self.check_seen_hori(diag_1,mine,diag_1_seen, r,c)
                        elif count ==4:
                            value+= self.check_pattern(mine, diag_1, self.winning_states, self.defend_winning_states)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                        elif count==3:
                            value+= self.check_pattern(mine, diag_1, self.winning_three, self.defend_three)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_1, self.two, self.defend_two)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                    count = np.sum(diag_2==self.ID)
                    if not ((r,c) in diag_2_seen):
                        if count ==5:
                            value += self.check_pattern(mine, diag_2, self.win, self.win)
                            hori_seen = self.check_seen_hori(diag_2,mine,diag_2_seen, r,c)
                        elif count ==4:
                            value+= self.check_pattern(mine, diag_2, self.winning_states, self.defend_winning_states)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                        elif count==3:
                            #print("hi")
                            value+= self.check_pattern(mine, diag_2, self.winning_three, self.defend_three)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_2, self.two, self.defend_two)
                            #print( value)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                    
                    count = np.sum(hori==self.opp_id)
                    #print(hori_seen)
                    if not ((r,c) in hori_seen):
                        if count ==5:
                            value += self.check_pattern(mine, hori, self.opp_win, self.opp_win)
                            hori_seen = self.check_seen_hori(hori,not mine,hori_seen, r,c)
                        if count ==4:
                            value+= self.check_pattern(mine, hori, self.opp_winning_states, self.opp_defend_winning_states)
                            hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                        elif count==3:
                            value+= self.check_pattern(mine, hori, self.opp_winning_three, self.opp_defend_three)
                            #print("check")
                            hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                        elif count==2:
                            value+= self.check_pattern(mine, hori, self.opp_two, self.opp_defend_two)
                            hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                    count = np.sum(vert==self.opp_id)
                    if not ((r,c) in vert_seen):
                        if count ==5:
                            value += self.check_pattern(mine, vert, self.opp_win, self.opp_win)
                            hori_seen = self.check_seen_hori(vert,not mine,vert_seen, r,c)
                        if count ==4:

                            value+= self.check_pattern(mine, vert, self.opp_winning_states, self.opp_defend_winning_states)
                            vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                        elif count==3:
                            #print("hi")
                            value+= self.check_pattern(mine, vert, self.opp_winning_three, self.opp_defend_three)
                            vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                        elif count==2:
                            #print(self.opp_two)
                            value+= self.check_pattern(mine, vert, self.opp_two, self.opp_defend_two)
                            vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                    count = np.sum(diag_1==self.opp_id)
                    #print(diag_1_seen)
                    if not ((r,c)in diag_1_seen):
                        if count ==5:
                            value += self.check_pattern(mine, diag_1, self.opp_win, self.opp_win)
                            hori_seen = self.check_seen_hori(diag_1,not mine,diag_1_seen, r,c)
                        if count ==4:
                            value+= self.check_pattern(mine, diag_1, self.opp_winning_states, self.opp_defend_winning_states)
                            #print("hi")
                            diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                        elif count==3:
                            value+= self.check_pattern(mine, diag_1, self.opp_winning_three, self.opp_defend_three)
                            diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_1, self.opp_two, self.opp_defend_two)
                            diag_1_seen = self.check_seen_diag_1(diag_1, not mine, diag_1_seen,r,c )
                    count = np.sum(diag_2==self.opp_id)
                    if not ((r,c) in diag_2_seen):
                        if count ==5:
                            value += self.check_pattern(mine, diag_2, self.opp_win, self.opp_win)
                            hori_seen = self.check_seen_hori(diag_2,not mine,diag_2_seen, r,c)
                        if count ==4:
                            value+= self.check_pattern(mine, diag_2, self.opp_winning_states, self.opp_defend_winning_states)
                            diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                        elif count==3:
                            value+= self.check_pattern(mine, diag_2, self.opp_winning_three, self.opp_defend_three)
                            diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_2, self.opp_two, self.opp_defend_two)
                            #print( "hi")
                            diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
                    #print("-----------------------")
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
                    #print(check)
                    #print(state)
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
                    
                    #print(state)
                    #print(check)
                    if np.all(check==state):
                        found = True
                        #print("hi")
                        value+=states_1[1]
                    #print(value)
                #print("---------------------")            
        #print("---------------")
        #print(value)
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