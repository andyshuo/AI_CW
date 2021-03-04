import numpy as np

import sys
sys.path.append("..")
from misc import legalMove
from misc import winningTest
from gomokuAgent import GomokuAgent
from copy import deepcopy
import time
import random

"""
I implemented alpha beta pruning. 
Alpha beta pruning runs much faster than minimax algorithm.

My evaluation function:
    1. Find position that isn't empty.
    2. For every position that is not empty
        2.1 Extract the vertical, horizontal, and the two diagnal lines.
        2.2 Match each line with different pattern and return a value for each line.
        2.3 Mark every viewed position as "seen" and don't score it again when next time see it.
    
"""


class Player(GomokuAgent):
    def __init__(self,ID,BOARDSIZE,X_IN_A_LINE):
        
        self.ID=ID
        self.opp_id=self.gen_opp_id(self.ID) #define the opponents ID for future use.
        self.BOARDSIZE=BOARDSIZE
        self.X_IN_A_LINE=X_IN_A_LINE
        
        
        # The below are the patterns and the corresponding values.
        # The values is decided by trial and errors and some basic understanding to the game.
        
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
                            
        # The below is just flipping the 1s and -1s for checking opponents patterns.
        self.opp_win = self.flip_states(deepcopy(self.win))
        self.opp_winning_states = self.flip_states(deepcopy(self.winning_states))
        self.opp_defend_winning_states = self.flip_states(deepcopy(self.defend_winning_states))
        self.opp_winning_three = self.flip_states(deepcopy(self.winning_three))
        self.opp_defend_three= self.flip_states(deepcopy(self.defend_three))
        self.opp_two=self.flip_states(deepcopy(self.two))
        self.opp_defend_two = self.flip_states(deepcopy(self.defend_two))
    
    def move(self,board):
        if self.all_zeros(board):
            # The player will play at 5,5 if there are no stones.
            return (5,5)
        else:
            value, action = self.max_value(board, -99999999,99999999, 0)
            return action
    
    def max_value(self, board,alpha, beta, depth):
        if (winningTest(self.opp_id, board, self.X_IN_A_LINE)or depth==2):
            # Depth 2 was chosen to terminate, the AI will lose because of timeout if I go deeper
            return (self.evaluate_move(board), (0,0))
            
        value = -99999999
        
        possi_moves = self.find_moves(board, True)
        possi_moves = list(dict.fromkeys(possi_moves)) # Remove duplicates
        best = (value,(0,0))
        for move, v in possi_moves:
            board[move[0],move[1]]=self.ID
            va, act = self.min_value(board, alpha,beta,depth+1)
            cur_value = (va, move)
            
            best = max(best, cur_value, key=lambda item:item[0])
            board[move[0],move[1]]=0
            
            if best[0]>=beta: 
                return best
            alpha = max(alpha, best[0])
        return best
    
    def min_value(self, board,alpha, beta, depth):
        if (winningTest(self.ID,board, self.X_IN_A_LINE)):
            return (self.evaluate_move(board), (0,0))
            
        value = 99999999
        
        possi_moves = self.find_moves(board, False)
        possi_moves = list(dict.fromkeys(possi_moves))
        
        best = (value,(0,0))
        for move, v in possi_moves:
            board[move[0],move[1]]=self.opp_id
            va, act = self.max_value(board, alpha, beta, depth+1)
            cur_value = (va, move)
            
            best = min(best, cur_value, key=lambda item: item[0])
            board[move[0],move[1]]=0
            
            if best[0] <=alpha:
                return best
            beta = min(beta, best[0])
        return best
    
    def no_my_stones(self,board):
        # Check if there are no player's stone for finding moves possible moves.
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r,c]==self.ID:
                    return False
        return True
    
    def find_moves(self,board, mine):
        """
        This function finds possible moves and sort it according one step rating on each move.
        Sorting it might utilizes alpha beta pruning if the first expanded node got the best value so far for min and max.
        
        Attributes:
            mine: boolean
                this is just to differ from max and min for evalution.
        
        """
        if self.all_zeros(board):
            return [((5,5),0)]
        elif self.no_my_stones(board):
            if legalMove(board, (5,5)):
                return [((5,5),0)]
            elif legalMove(board,(5,6)):
                return [((5,6),0)]
        else:
            list_of_moves=[] # this is a list of (move, value) tuples
            for r in range(len(board)):
                for c in range(len(board)):
                    if board[r,c]!=0:
                        list_of_moves = list_of_moves+self.get_moves_from_a_position(board, r,c, mine)
            if mine:
                list_of_moves.sort(key = lambda item:item[1], reverse=True)
            else:
                list_of_moves.sort(key = lambda item:item[1])
            return list_of_moves[:20] # list_of_moves is truncated to top 20 moves for efficiency.

    def get_move_result(self, board, r, c, id):
        board[r,c]=id
        value =  self.evaluate_move(board)
        board[r,c]=0
        return ((r,c), value)
        
    def get_moves_from_a_position(self, board, r,c, mine):
        list_of_moves=[]
        if legalMove(board, (r-1,c-1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c-1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c-1,self.opp_id)]
        if legalMove(board, (r-1,c)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c,self.opp_id)]
        if legalMove(board, (r-1,c+1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c+1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r-1,c+1,self.opp_id)]
        if legalMove(board, (r,c-1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c-1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c-1,self.opp_id)]
        if legalMove(board, (r,c)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c,self.opp_id)]
        if legalMove(board, (r,c+1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c+1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r,c+1,self.opp_id)]
        if legalMove(board, (r+1,c-1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c-1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c-1,self.opp_id)]
        if legalMove(board, (r+1,c)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c,self.opp_id)]
        if legalMove(board, (r+1,c+1)):
            if mine:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c+1,self.ID)]
            else:
                list_of_moves = list_of_moves+[self.get_move_result(board,r+1,c+1,self.opp_id)]
        return list_of_moves
    
    def all_zeros(self, board):
        # Check if there are no stones on the board.
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c]!=0:
                    return False
        return True
        
    def gen_opp_id(self, id):
        # Generate opponents ID for other use.
        if id==1:
            return -1
        else:
            return 1
          

    


    def evaluate_move(self, board):
        """
        This is the evalution function.
        
        As said above, it first find location that is not empty.
        Then it matches patterns.
        Then it mark stones as seen to prevent over estimation.
        
        """
        value = 0
        hori_seen=[]
        vert_seen=[]
        diag_1_seen=[]
        diag_2_seen=[]
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r,c]!=0:
                    hori = board[r]
                    vert = board[:,c]
                    diag_1 = np.array(board).diagonal(c-r)
                    diag_2 = np.fliplr(np.array(board)).diagonal((10-c)-r)
                    mine = True # This is to differ from max and mini.
                    # Below has 8 parts of codes. It includes checking patterns in four directions with different number of stones in every direction for both players.
                    if board[r,c]==self.ID:
                        count = np.sum(hori==self.ID) # Count is to map from to different subset of patterns.
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
                                value+= self.check_pattern(mine, diag_2, self.winning_three, self.defend_three)
                                diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                            elif count==2:
                                value+= self.check_pattern(mine, diag_2, self.two, self.defend_two)
                                diag_2_seen = self.check_seen_diag_2(diag_2, mine, diag_2_seen,r,c )
                    else:
                        count = np.sum(hori==self.opp_id)
                        if not ((r,c) in hori_seen):
                            if count ==5:
                                value += self.check_pattern(mine, hori, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(hori,not mine,hori_seen, r,c)
                            if count ==4:
                                value+= self.check_pattern(mine, hori, self.opp_winning_states, self.opp_defend_winning_states)
                                hori_seen = self.check_seen_hori(hori, not mine, hori_seen, r,c)
                            elif count==3:
                                value+= self.check_pattern(mine, hori, self.opp_winning_three, self.opp_defend_three)
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
                                value+= self.check_pattern(mine, vert, self.opp_winning_three, self.opp_defend_three)
                                vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                            elif count==2:
                                value+= self.check_pattern(mine, vert, self.opp_two, self.opp_defend_two)
                                vert_seen = self.check_seen_vert(vert, not mine, vert_seen, r,c)
                        count = np.sum(diag_1==self.opp_id)
                        if not ((r,c)in diag_1_seen):
                            if count ==5:
                                value += self.check_pattern(mine, diag_1, self.opp_win, self.opp_win)
                                hori_seen = self.check_seen_hori(diag_1,not mine,diag_1_seen, r,c)
                            if count ==4:
                                value+= self.check_pattern(mine, diag_1, self.opp_winning_states, self.opp_defend_winning_states)
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
                                diag_2_seen = self.check_seen_diag_2(diag_2, not mine, diag_2_seen,r,c )
        return value
                
    def check_pattern(self, is_my_stone, ls, states_1, states_2):
        # This function matches patterns and return values.
        value =0
        found=False # found is a boolean value used to reduce resources, and to prevent counting on both state_1 and state_2.
        # states_2 is the defendable states, which is first revealed, because not defendable states might be subset of defendable one.
        for state in states_2[0]:  
            if not found:
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                for p in possibles:
                    check=ls[p:p+N]
                    if len(check)==len(state):
                        if np.all(check==state):
                            found=True 
                            value+=states_2[1]
            
        for state in states_1[0]:
            if not found:
                N = len(state)
                possibles = np.where(state[0]==ls)[0]
                
                for p in possibles:
                    check=ls[p:p+N]
                    if len(check)==len(state):
                        if np.all(check==state):
                            found = True
                            value+=states_1[1]
        return value

    def flip_states(self, states):
        # The method used to generate opponent's pattern and heuristic value.
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
    
    
    #The below four function is to mark seen positions. 
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
            if not len(temp)==0:
                temp = temp-temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c+i)))
                for i, move in t:
                    seen.append(move)
        return seen 
        
    def check_seen_diag_2(self, ls,mine, seen, r,c):
        if mine:
            temp = np.where(ls==self.ID)[0]
            if not len(temp)==0:
                temp = temp -temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c-i)))
                for i, move in t:
                    seen.append(move)
        else:
        
            temp = np.where(ls==self.opp_id)[0]
            if not len(temp)==0:
                temp = temp -temp[0]
                t = []
                for i in temp:
                    t.append((i, (r+i,c-i)))
                for i, move in t:
                    seen.append(move)

        return seen 