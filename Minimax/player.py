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
        
        self.winning_states = ([
        
        
                            [ID,ID,ID,ID,0],
                            [ID,ID,ID,0,ID],
                            [ID,ID,0,ID,ID],
                            [ID,0,ID,ID,ID],
                            [0,ID,ID,ID,ID]
                            ],99999)
        self.one_step_to_winning = ([
                                [-ID,ID,ID,0,ID,0],
                                [ID,ID,0,ID,0],
                                [-ID,ID,0,ID,ID,0],
                                [ID,0,ID,ID,0],
                                [0,ID,ID,ID,0],
                                [0,ID,ID,0,ID,-ID],
                                [0,ID,ID,0,ID],
                                [0,ID,0,ID,ID,-ID],
                                [0,ID,0,ID,ID]
                                ],1000)
        
        self.defend_one_step_to_winning = ([
                                        [-ID,ID,ID,ID,0,0],
                                        [ID,ID,ID,0,0],
                                        [-ID,ID,ID,0,ID,0],
                                        [ID,ID,0,ID,0],
                                        [0,ID,ID,0,ID,-ID],
                                        [0,ID,ID,0,ID],
                                        [0,ID,0,ID,ID,-ID],
                                        [0,ID,0,ID,ID],
                                        [0,0,ID,ID,ID,-ID],
                                        [0,0,ID,ID,ID],
                                        [ID,0,ID,0,ID],
                                        [ID,0,0,ID,ID],
                                        [ID,ID,0,0,ID],
                                        [ID,ID,0,0,ID,ID]       
                                        ],10)
        self.two_step_to_winning = ([
                                [-ID,ID,ID,0,0,0],
                                [ID,ID,0,0,0],
                                [-ID,ID,0,ID,0,0],
                                [ID,0,ID,0,0],
                                [-ID,0,ID,ID,0,0],
                                [0,ID,ID,0,0],
                                [0,ID,0,ID,0],
                                [0,0,ID,ID,0,-ID],
                                [0,0,ID,ID,0],
                                [0,0,ID,0,ID,-ID],
                                [0,0,ID,0,ID],
                                [0,0,0,ID,ID,-ID],
                                [0,0,0,ID,ID],
                                [ID,0,0,0,ID],
                                [0,ID,0,0,ID,0],
                                [-ID,ID,0,0,ID,0],
                                [ID,0,0,ID,0],
                                [0,ID,0,0,ID,-ID],
                                [0,ID,0,0,ID]
                                ],3)
        self.opp_winning_states = self.flip_states(deepcopy(self.winning_states))
        #print(self.opp_winning_states)
        self.opp_one_step_to_winning = self.flip_states(deepcopy(self.one_step_to_winning))
        self.opp_defend_one_step_to_winning = self.flip_states(deepcopy(self.defend_one_step_to_winning))
        self.opp_two_step_to_winning= self.flip_states(deepcopy(self.two_step_to_winning))
        self.opp_all_states = [self.opp_winning_states,self.opp_one_step_to_winning,self.opp_defend_one_step_to_winning,self.opp_two_step_to_winning]
        self.all_states = [self.winning_states, self.one_step_to_winning, self.defend_one_step_to_winning, self.two_step_to_winning]
    
    def move(self,board):
        if self.all_zeros(board):
            return (5,5)
        else:
            print("----------------------------------")
            ls = []
            temp_v = self.evaluate_board(board)
            if temp_v>=0:
                possi_moves=self.find_my_moves(board)
            else:
                possi_moves=self.find_opp_moves(board)
            for move in possi_moves:
                board[move[0],move[1]]=self.ID
                ls.append((move, self.min_value(board,0,-999999,999999)))
                board[move[0],move[1]]=0
            print("----------------------------------")
            return max(ls, key= lambda item:[1])[0]
    
    def max_value(self, board, depth, alpha, beta):
        print("depth is:{d}".format(d=depth))
        
        if depth==2:
            return self.evaluate_board( board)
        if winningTest(self.opp_id, board, self.X_IN_A_LINE):
            return self.evaluate_board(board)
        value = -99999
        temp_v = self.evaluate_board(board)
        print("max")
        print(board)
        print("value is: {v}".format(v=temp_v))
        if temp_v>=0:
            possi_moves = self.find_my_moves(board)
        else:
            possi_moves = self.find_opp_moves(board)
        for move in possi_moves:
            print("({r},{c})".format(r=move[0], c=move[1]))
            board[move[0],move[1]]=self.ID
            
            value= max(value, self.min_value(board,depth+1, alpha, beta))
            board[move[0],move[1]]=0
            print(beta)
            if value>=beta:
                return value
            alpha = max(alpha, value)
        return value
    
    def min_value(self, board, depth, alpha, beta):
        print("depth is:{d}".format(d=depth))
        if depth==2:
            return self.evaluate_board(board)
        if winningTest(self.ID, board, self.X_IN_A_LINE):
            return self.evaluate_board(board)
        value=99999
        
        temp_v = self.evaluate_board(board)
        print("min")
        print(board)
        print("value is: {v}".format(v=temp_v))
        if temp_v<0:
            possi_moves = self.find_opp_moves(board)
        else:
            possi_moves = self.find_my_moves(board)
        
        for move in possi_moves:
            print("({r},{c})".format(r=move[0], c=move[1]))
            board[move[0],move[1]]=self.opp_id
            
            value = min(value, self.max_value(board,depth+1, alpha, beta))
            board[move[0],move[1]]=0
            if value<=alpha:
                return value
            beta = min(beta, value)
        return value
    
    #def move(self, board):
       # return (0,0)
        
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
            print("length: {l}".format(l=len(list_of_moves)))
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
            print("length: {l}".format(l=len(list_of_moves)))
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
                
        #end_time = time.time()
        #print("{time} ms".format(time = end_time-start_time))
        #print(value)
        return value

    def evaluate_move(self, board, r, c):
        horis = []
        for i in range(4):
            if not c-i<0 and not c+i>10:
                horis.append(board[r,c-i:c-i+5])
                horis.append(board[r,c+i:c+i+5])
                #print(board[r,c-i:c-i+5])
                #print(board[r,c+i:c+i+5])
        verts = []
        for i in range(4):
            if not r-i<0 and not r+i>10:
                verts.append(board[r-i:r-i+5,c])
                verts.append(board[r+i:r+i+5,c])
                
        diag_1 = []
        for i in range(4):
            if not r-i<0 and not c-i<0 and not r+i>10 and not c+i>10:
                diag_1.append(board[r-i:r-i+5,c-i:c-i+5])
                diag_1.append(board[r+i:r+i+5,c+i:c+i+5])
            
        diag_2 = []
        for i in range(4):
            if not r-i<0 and not c-i<0 and not r+i>10 and not c+i>10:
                diag_2.append(board[r-i:r-i+5,c+i:c+i+5])
                diag_2.append(board[r+i:r+i+5,c-i:c-i+5])
        

    def flip_states(self, states):
        for state in states[0]:
            for i in range(len(state)):
                if state[i]==-1:
                    state[i]=1
                if state[i]==1:
                    state[i]=-1
        return states
                
    