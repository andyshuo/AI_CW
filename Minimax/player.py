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
        
        self.winning_states = ([[0,ID,ID,ID,ID,0]],10000)
        self.defend_winning_states = ([
                                        [-ID,ID,ID,ID,ID,0],
                                        [0,ID,ID,ID,ID,-ID],
                                        [ID,ID,ID,0,ID],
                                        [ID,ID,-ID,ID,ID]
                                        ],9000)
        self.winning_three = ([
                                [ID,ID,ID],
                                [ID,ID,0,ID],
                                [ID,0,ID,ID]
                                ],5000)
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
                                ],3000)
        self.two = ([
                    [0,0,ID,ID,0,0],
                    [0,ID,0,ID,0],
                    [0,ID,0,0,ID,0],
                    ],700)
                    
        self.defend_two = ([
                            [-ID,ID,ID,0,0,0],
                            [-ID,ID,0,ID,0,0],
                            [-ID,ID,0,0,ID],
                            [ID,0,0,0,ID],
                            [0,0,0,ID,ID,-ID],
                            [0,0,ID,0,ID,-ID],
                            [ID,0,0,ID,-ID]
                            ],70)
        
        self.opp_winning_states = self.flip_states(deepcopy(self.winning_states))
        #print(self.opp_winning_states)
        self.opp_defend_winning_states = self.flip_states(deepcopy(self.defend_winning_states))
        self.opp_winning_three = self.flip_states(deepcopy(self.winning_three))
        self.opp_defend_three= self.flip_states(deepcopy(self.defend_three))
        self.opp_two=self.flip_states(deepcopy(self.two))
        self.opp_defend_two = self.flip_states(deepcopy(self.defend_two))
        self.opp_all_states = [self.opp_winning_states,self.opp_defend_winning_states,self.opp_winning_three,self.opp_defend_three, self.opp_two, self.opp_defend_two]
        self.all_states = [self.winning_states, self.defend_winning_states, self.winning_three, self.defend_three, self.two, self.defend_two]
    
    def move(self,board):
        if self.all_zeros(board):
            return (5,5)
        else:
            value, action = self.max_value(board, -999999,999999, 0)
            print(value)
            print(action)
            #print(action)
            return action
    
    def max_value(self, board,alpha, beta, depth):
        #print(depth)
        if (winningTest(self.ID, board, self.X_IN_A_LINE) or depth>3):
            return self.evaluate_move(board), (0,0)
        value = -99999
        #board_value = self.evaluate_move(board)
        
        #if self.no_my_stones(board):
        #    possi_moves = self.find_opp_moves(board)
        #elif board_value<70 and board_value>=0:
        #    possi_moves = self.find_my_moves(board)
        #else:
        #    possi_moves=self.find_opp_moves(board)
        possi_moves = self.find_moves(board)
        possi_moves = list(dict.fromkeys(possi_moves))
        act = None
        possi_moves = possi_moves
        #possi_moves = possi_moves[:10]
        #print("board value: {board}".format(board=board_value))
        #print("len: {len}".format(len=len(possi_moves)))
        
        for move in possi_moves:
        
            board[move[0],move[1]]=self.ID
            act = move
            tttv, ttta = self.min_value(board, alpha,beta,depth+1)
            #print("{value},{action}, {depth}".format(value = tttv, action = move, depth=depth))
            value= max(value, tttv)
            board[move[0],move[1]]=0
            if value>=beta: return value, act
            alpha = max(alpha, value)
        
        return value, act
    
    def min_value(self, board,alpha, beta, depth):
        #print(depth)
        if (winningTest(self.opp_id,board, self.X_IN_A_LINE) or depth>3):
            #print(board)
            #print(self.evaluate_move(board))
            return self.evaluate_move(board), (0,0)
        value = 99999
        #board_value = self.evaluate_move(board)
        
        #if board_value>-70 and board_value<0:
        #    possi_moves = self.find_opp_moves(board)
        #elif board_value>=0:
        #    possi_moves = self.find_my_moves(board)
        #else:
        #    possi_moves = self.find_opp_moves(board)
        possi_moves = self.find_moves(board)
        possi_moves = list(dict.fromkeys(possi_moves))
        possi_moves = possi_moves
        act = None
        #print(board_value)
        #print(len(possi_moves))
        #possi_moves = possi_moves[:10]
        
        for move in possi_moves:
            board[move[0],move[1]]=self.opp_id
            act = move
            tttv, ttta = self.max_value(board, alpha, beta, depth+1)
            #print("{value},{action}, {depth}".format(value = tttv, action = ttta, depth=depth))
            value= min(value, tttv)
            board[move[0],move[1]]=0
            if value <=alpha: return value, act
            beta = min(beta, value)
        return value, act
    
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
          
    def get_value_hori(self, board,all_states, r,c):
        value = 0
        for states in all_states:
            for state in states[0]:
                temp = board[r,c:c+len(state)]
                #print("r={r},c={c}".format(r=r,c=c))
                #print(temp)
                #print(state)
                if len(temp)==len(state):
                    if all([temp[i]==state[i] for i in range (len(state))]):
                        value+=states[1]
        return value 
     
    def get_value_vert(self,board,all_states,r,c):
        value = 0
        for states in all_states:
            for state in states[0]:
                temp = board[r:r+len(state),c]
                if len(temp)==len(state):
                    if all([temp[i]==state[i] for i in range(len(state))]):
                        value+=states[1]
        return value
    
    def get_value_diag(self,board,all_states,r,c):
        value = 0
        #print(all_states)
        for states in all_states:
            #print(states[0])
            for state in states[0]:
                temp = []
                for i in range(len(state)):
                    if r+i>10 or c+i>10:
                        break
                    temp.append(board[r+i,c+i])
                #print(temp)
                if len(temp)==len(state):
                    if all([temp[i]==state[i] for i in range(len(state))]):
                        #print(temp)
                        #print(state)
                        value+=states[1]
        return value
        
        
    def get_value_diag_2(self,board,all_states,r,c):
        value = 0
        #print(all_states)
        for states in all_states:
            #print(states[0])
            for state in states[0]:
                temp = []
                for i in range(len(state)):
                    if r+i>10 or c-i<0:
                        break
                    temp.append(board[r+i,c-i])
                #print(temp)
                if len(temp)==len(state):
                    if all([temp[i]==state[i] for i in range(len(state))]):
                        #print(temp)
                        #print(state)
                        value+=states[1]
        return value
    
    def evaluate_attack(self, board):
        value = 0
        for r in range(len(board)):
            for c in range(len(board[r])):
                #print("{r},{c}".format(r=r,c=c))
                #if board[r,c]==id:
                    #temp = board[r:r+5,c]
                value += self.get_value_hori(board,self.all_states, r, c)
                value += self.get_value_vert(board,self.all_states,r,c)
                value += self.get_value_diag(board,self.all_states,r,c)
                value += self.get_value_diag_2(board,self.all_states,r,c)
        return value
        
    def evaluate_defense(self,board):
        value = 0
        for r in range(len(board)):
            for c in range(len(board[r])):
                value -= self.get_value_diag(board,self.opp_all_states,r,c)
                value -= self.get_value_hori(board,self.opp_all_states,r,c)
                value -= self.get_value_vert(board, self.opp_all_states, r,c)
                value -= self.get_value_diag_2(board,self.all_states,r,c)
        return value
    
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
        value = 1
        hori_seen=[]
        vert_seen=[]
        diag_1_seen=[]
        diag_2_seen=[]
        print(value)
        for r in range(len(board)):
            #print(value)
            for c in range(len(board)):
                
                if board[r,c]!=0:
                    if board[r,c]==self.ID:
                        mine = True
                    else:
                        mine = False
                    
                    hori = board[r]
                    vert = board[:,c]
                    diag_1 = np.array(board).diagonal(c-r)
                    diag_2 = np.fliplr(np.array(board)).diagonal((10-c)-r)

                    count = np.sum(hori==self.ID)
                    #print((r,c))
                    #print((r,c)in hori_seen)
                    #print(hori_seen)
                    if not ((r,c) in hori_seen):
                        if count ==4:
                            value+= self.check_pattern(mine, hori, self.winning_states, self.defend_winning_states)
                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                        elif count==3:
                            value+= self.check_pattern(mine, hori, self.winning_three, self.defend_three)
                            print(value)
                            print("check")
                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                        elif count==2:
                            value+= self.check_pattern(mine, hori, self.two, self.defend_two)
                            hori_seen = self.check_seen_hori(hori, mine, hori_seen, r,c)
                            #print("check")
                    #print(value)
                    count = np.sum(vert==self.ID)
                    if not ((r,c) in vert_seen):
                        if count ==4:
                            value+= self.check_pattern(mine, vert, self.winning_states, self.defend_winning_states)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                        elif count==3:
                            value+= self.check_pattern(mine, vert, self.winning_three, self.defend_three)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                        elif count==2:
                            value+= self.check_pattern(mine, vert, self.two, self.defend_two)
                            vert_seen = self.check_seen_vert(vert, mine, vert_seen, r,c)
                            #print("check")
                    count = np.sum(diag_1==self.ID)
                    if not ((r,c)in diag_1_seen):
                    
                        if count ==4:
                            value+= self.check_pattern(mine, diag_1, self.winning_states, self.defend_winning_states)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                        elif count==3:
                            value+= self.check_pattern(mine, diag_1, self.winning_three, self.defend_three)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_1, self.two, self.defend_two)
                            diag_1_seen = self.check_seen_diag_1(diag_1, mine, diag_1_seen,r,c )
                            #print("check")
                    count = np.sum(diag_2==self.ID)
                    if not ((r,c) in diag_2_seen):
                        if count ==4:
                            value+= self.check_pattern(mine, diag_2, self.winning_states, self.defend_winning_states)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                        elif count==3:
                            value+= self.check_pattern(mine, diag_2, self.winning_three, self.defend_three)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                        elif count==2:
                            value+= self.check_pattern(mine, diag_2, self.two, self.defend_two)
                            diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                            #print(diag_2_seen)
                            #print("check")
                    print("hi"+str(value))
                #print(value)
        #print(value)
        return value
                
    def check_pattern(self, is_my_stone, ls, states_1, states_2):
        value =0
        if is_my_stone:
            for state in states_1[0]:
                #print("---------------------")
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                for p in possibles:
                    check=ls[p:p+N]
                    if np.all(check==state):
                        value+=states_1[1]
                #print("---------------------")
            
            for state in states_2[0]:
                #print("---------------------")
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                
                
                for p in possibles:
                    check=ls[p:p+N]
                    #print(check)
                    #print(state)
                    if np.all(check==state):
                        #print("hi")
                        value+=states_2[1]
                #print("---------------------")
            
        else:

            for state in states_1[0]:
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                for p in possibles:
                    check=ls[p:p+N]
                    if np.all(check==state):
                        value-=states_1[1]
                    

            for state in states_2[0]:
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                for p in possibles:
                    check=ls[p:p+N]
                    if np.all(check==state):
                        value-=states_2[1]
        #print(value)
        return value

    def flip_states(self, states):
        for state in states[0]:
            for i in range(len(state)):
                if state[i]==-1:
                    state[i]=1
                if state[i]==1:
                    state[i]=-1
        return states
                
    def check_seen_hori(self,ls,mine, seen,r,c):
        if mine:
            temp = np.where(ls==self.ID)
            for y,x in zip(np.full(len(temp[0]), r),temp[0]):
                seen.append((y,x))
        else:
            temp = np.where(ls==self.opp_id)
            for y,x in zip(np.full(len(temp[0]), r),temp[0]):
                seen.append((y,x))
        return seen
    
    def check_seen_vert(self,ls,mine,seen,r,c):
        if mine:
            temp = np.where(ls==self.ID)
            for y,x in zip(temp[0], np.full(len(temp[0]), c)):
                seen.append((y,x))
        else:
            temp = np.where(ls==self.opp_id)
            for y,x in zip(temp[0], np.full(len(temp[0]), c)):
                seen.append((y,x))
        return seen        
    
    def check_seen_diag_1(self, ls,mine, seen,r,c):
        if mine:
            temp = np.where(ls==self.ID)
            for y,x in zip(temp[0],np.arange(c,c+len(temp[0]))):
                seen.append((y,x))
        else:
            temp = np.where(ls==self.opp_id)
            for y,x in zip(temp[0],np.arange(c,c+len(temp[0]))):
                seen.append((y,x))
        return seen 
        
    def check_seen_diag_2(self, ls,mine, seen, r,c):
        if mine:
            temp = np.where(ls==self.ID)
            #print("Hi")
            #print(ls)
            for y,x in zip(temp[0], np.flip(np.arange(c-len(temp[0])+1,c+1),0)):
                #print((y,x))
                seen.append((y,x))
        else:
            temp = np.where(ls==self.opp_id)
            for y,x in zip(temp[0], np.flip(np.arange(c-len(temp[0])+1,c+1),0)):
                #print((y,x))
                seen.append((y,x))
        return seen 