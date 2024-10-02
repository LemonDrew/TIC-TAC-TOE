# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:01:53 2023

@author: Derrick Wong Liang Jun
"""
import numpy as np
import random
import copy


def create_board():
    # Initialize a 6x6 board with zeros
    return np.zeros((6, 6), dtype=int)

def check_victory(board, turn):
    new_board = copy.deepcopy(board) #preserve the originality of the game_board
    if (check_status(new_board,1) and check_status(new_board,2)): #check if both players win after rotation - game is draw
        return 3
    elif check_status(new_board,1): #check if player 1 wins after rotation
        return 1
    elif check_status(new_board,2): #check if player 2 wins after rotation
        return 2
        
def check_status(board,turn): #check the types of victory when 5 or more consecutive same coloured marbles are present in the game board
    return check_horizontal(board,turn) or check_vertical(board,turn) or check_diagonal(board,turn) or check_opposite_diagonal(board,turn)


def check_horizontal(board,turn):
    for i in range(6): #check the left side of the board
        number = 0
        for j in range(5):
            if board[i][j] == turn:
                number +=1
        if number == 5:
            return True
    
    for i in range(6): #check the right side of the board
        number = 0
        for j in range(1,6,1):
            if board[i][j] == turn:
                number +=1
        if number == 5:
            return True
    return False


def check_vertical(board,turn):
    for j in range(6): #check the top side of the board
        number = 0
        for i in range(5):
            if board[i][j] == turn:
                number +=1
        if number == 5:
            return True
    
    for j in range(6): #check the bottom side of the board
        number = 0
        for i in range(1,6,1):
            if board[i][j] == turn:
                number +=1
        if number == 5:
            return True
    return False

def check_diagonal(board,turn): #check diagonal victory from top left to bottom right
    first = 0
    for i in range(5):
        if board[i][i] == turn:
            first +=1
    second = 0
    for j in range(5):
        if board[j][j+1] == turn:
            second += 1
    third = 0
    for k in range(1,6,1):
        if board[k][k-1] == turn:
            third += 1
    fourth = 0
    for l in range(1,6,1):
        if board[l][l] == turn:
            fourth += 1
    
    if (first == 5 or second == 5 or third == 5 or fourth == 5):
        return True
    else:
        return False



def check_opposite_diagonal(board,turn): #check opposite diagonal victory from top right to bottom left
    first = 0
    number = 1
    for i in range(4,-1,-1):
        if board[i][number] == turn:
            first += 1
            number+= 1

    number = 0
    second = 0
    for j in range(4,-1,-1):
        if board[j][number] == turn:
            second += 1
            number+= 1

    number = 1
    third = 0
    for k in range(5,0,-1):
        if board[k][number] == turn:
            third += 1
            number += 1

    number = 0
    fourth = 0
    for l in range(5,0,-1):
        if board[l][number] == turn:
            fourth += 1
            number += 1
    
    if (first == 5 or second == 5 or third == 5 or fourth == 5):
        return True
    else:
        return False


def is_full(board): #check if board is fully occupied and if there is any available moves for both Player 1 and 2
    for i in range(0,6):
        if 0 in board[i]:
            return False
    return True

def apply_move(board, turn, row, col, rot): #add player's coloured marble to specific and unoccupied location on game board before rotating the board
    new_board = copy.deepcopy(board)
    new_board[row][col] = turn
    new_board = rotate(new_board,rot)
    return new_board
    

def rotate(board, rot): #player is required to rotate 1 out of 4 sub-boards by 90 degrees clockwise or anti-clockwise
    if rot == 4:
        board[3:6, 3:6] = np.rot90(board[3:6, 3:6], 1)
    elif rot == 3:
        board[3:6, 3:6] = np.rot90(board[3:6, 3:6], 3)
    elif rot == 2:
        board[:3, 3:6] = np.rot90(board[:3, 3:6], 1)
    elif rot == 1:
        board[:3, 3:6] = np.rot90(board[:3, 3:6], 3)
    elif rot == 8:
        board[:3, :3] = np.rot90(board[:3, :3], 1)
    elif rot == 7:
        board[:3, :3] = np.rot90(board[:3, :3], 3)
    elif rot == 6:
        board[3:6, :3] = np.rot90(board[3:6, :3], 1)
    elif rot == 5:
        board[3:6, :3] = np.rot90(board[3:6, :3], 3)
    return board




def check_move(board, row, col): #check if current location on game board has already been filled
    if (row not in [0,1,2,3,4,5] or col not in [0,1,2,3,4,5]):
        return False
    elif (board[row][col] == 1):
        return False
    elif (board[row][col] == 2):
        return False
    else:
        return True
    
    
def display_board(board): #display 6x6 PENTAGO game board which is divided into four 3x3 sub-boards
    for i in range(0,6,1):
        print(board[i])
        



    
    

    