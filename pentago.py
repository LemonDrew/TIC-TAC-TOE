# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:52:42 2023

@author: tayje
"""
import numpy as np
import random
import copy
import json


def check_victory(board, turn, rot):
    new_board = copy.deepcopy(board) #preserve the originality of the game board
    if (check_status(new_board,1) and check_status(new_board,2)): #check if both players win after rotation - game is draw
        return 3
    elif check_status(new_board,1): #check if player 1 wins after rotation
        return 1
    elif check_status(new_board,2): #check if player 2 wins after rotation
        return 2
    else: #player can choose to rotate different sub-boards of game board ranging from 1 to 8
        if rot == 8:
            new_board = rotate(new_board,7) #change the board to before rotation
        elif rot == 7:
            new_board = rotate(new_board,8)
        elif rot == 6:
            new_board = rotate(new_board,5)
        elif rot == 5:
            new_board = rotate(new_board,6)
        elif rot == 4:
            new_board = rotate(new_board,3)
        elif rot == 3:
            new_board = rotate(new_board,4)
            
        elif rot == 2:
            new_board = rotate(new_board,1)
        elif rot == 1:
            new_board = rotate(new_board,2)
        if check_status(new_board,turn): #check if current player making the rotation wins
            return turn
        elif is_full(new_board):
            return 3
        else:
            return 0
        
def check_status(board,turn): #check the types of victory when 5 or more consecutive same-coloured marbles are present in the game board
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


def is_full(board):  #check if board is fully occupied and if there is any available moves for both Player 1 and 2 
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
        
def computer_move(board,turn,level): #player can choose between 2 qualities of computer player to play
    if level == 1:
        return random_computer(board)
    else:
        return medium_computer(board,turn)
    
def random_computer(board): #random quality of computer player implemented
    row = random.randint(0,5)
    col = random.randint(0,5)
    rotation = random.randint(1,8)
    while board[row][col] != 0:
        row = random.randint(0,5)
        col = random.randint(0,5)
    return [row,col,rotation]

def medium_computer(board,turn): #medium quality of computer player implemented
    player_turn = 1
    if turn == 1:
        player_turn = 2
    new_board = copy.deepcopy(board)
    for i in range(6):  #check if computer can win in next move
        for j in range(6):
            if new_board[i][j] == 0:
                new_board[i][j] = turn
                for k in range(1,9,1):
                    first_copy = copy.deepcopy(new_board)
                    first_copy = rotate(first_copy,k)
                    if check_victory(first_copy,turn,k) == turn:
                        return [i,j,k]
                new_board[i][j] = 0
    for i in range(6):  #check if player can win in next move
        for j in range(6):
            if new_board[i][j] == 0:
                new_board[i][j] = player_turn
                for k in range(1,9,1):
                    second_copy = copy.deepcopy(new_board)
                    second_copy = rotate(second_copy,k)
                    if check_victory(second_copy,player_turn,k) == player_turn: #if player can win next move, computer execute step to block the player's move
                        return [i,j,k]
                new_board[i][j] = 0

    return random_computer(board) #else randomly make a move if neither player wins in next move

    
    

def player_move(board,turn):
    while True:
        try:
            row = int(input("Player " + str(turn) +" : Choose your row: "))
            col = int(input("Player " + str(turn) +" : Choose your column: "))
            rotation = int(input("Player " + str(turn) +" : Choose your rotation: Rotate by 90 degrees clockwise or anticlockwise "))
            if not check_move(board,row,col): #check if the specific index value for row or column is within or beyond the acceptable range before proceeding
                print("Invalid Row or Column! Please try again!")
                continue
            elif rotation not in [1,2,3,4,5,6,7,8]: #check if the specific rotation value is within or beyond the acceptable range before proceeding 
                print("Invalid Rotation number! Please try again!")
                continue
            else:
                confirm = input("Are you sure you want to make this move? (Row: " + str(row) + " Column: " + str(col) + " Rotation: " + str(rotation) + ")" + " Y/N ") #player can verify their moves before proceeding the game
                if confirm.upper() == "Y":
                    return [row,col,rotation]
                elif confirm.upper()  == "N": #implement undo feature to allow player to reconsider their previously executed move, especially in player VS player game
                    print("Redoing move......")
                    continue
                else:
                    print("Invalid input! Please make your move again!")
                    continue
        except ValueError: #check and display error if a string of characters is input by player
            print("Error! Please try again!")
            player_move(board,turn)
            break

def exit_game(): #player can choose to continue or exit the game after each (player VS player) or (player VS computer) move
    exit_game = input("Play again? Y/N ")
    if exit_game.upper() == "Y":
        menu()
    else:
        print("Goodbye!")

def view_leaderboard(): #track players' scores and achievements if display of leaderboard is chosen
    with open("leader_board.json", "r") as ranking:
        leader_board = json.load(ranking)
    for i in range(len(leader_board)):
        print("RANKING " + str(i+1) + " : " + str(leader_board[i][0]) + " score: " + str(leader_board[i][1]))

def update_leaderboard(player): #leaderboard will update the players' score accordingly
    found = False
    with open("leader_board.json", "r") as ranking:
        leader_board = json.load(ranking)
    if len(leader_board) == 0:
        leader_board.append([player,1])
        with open("leader_board.json", "w") as ranking:
            json.dump(leader_board, ranking)
        return
    for i in range(len(leader_board)): #check leaderboard for existing player
        if leader_board[i][0] == player:
            leader_board[i] = [player, leader_board[i][1] + 1]
            found = True
    if found == False: #no existing player found in leaderboard and new player has entered the game
        leader_board.append([player,1])
    leader_board.sort(key = lambda x:x[1], reverse = True) #sort leaderboard according to the players' scores
    with open("leader_board.json", "w") as ranking:
        json.dump(leader_board, ranking)
    
def menu():
    game_board = np.zeros((6, 6))
    print("Welcome to 6x6 PENTAGO Tic-Tac-Toe!")
    print("(1): Play game")
    print("(2): View Leaderboard")
    option = int(input("Select options: "))
    if option == 1:
        opponent = input("Choose Opponent: Player or Computer ") #player can choose to play with another human player or computer
        if (opponent.upper() == "PLAYER"):
            player1_name = input("Input name for Player 1: ").upper()
            player2_name = input("Input name for Player 2: ").upper()
            while True:
                move = player_move(game_board,1)
                game_board = apply_move(game_board,1,move[0],move[1],move[2])
                display_board(game_board)
                if check_victory(game_board,1,move[2]) == 3:
                    print("Draw!")
                    exit_game()
                    break
                elif check_victory(game_board,1,move[2]) == 1:
                    print(player1_name + " wins!")
                    update_leaderboard(player1_name)
                    exit_game()
                    break
                elif check_victory(game_board,1,move[2]) == 2:
                    print(player2_name + " wins!")
                    update_leaderboard(player2_name)
                    exit_game()
                    break
                second_move = player_move(game_board,2)
                game_board = apply_move(game_board,2,second_move[0],second_move[1],second_move[2])
                display_board(game_board)
                if check_victory(game_board,2,second_move[2]) == 3:
                    print("Draw!")
                    exit_game()
                    break
                elif check_victory(game_board,2,second_move[2]) == 1:
                    print(player1_name + " wins!")
                    update_leaderboard(player1_name)
                    exit_game()
                    break
                elif check_victory(game_board,2,second_move[2]) == 2:
                    print(player2_name + " wins!")
                    update_leaderboard(player2_name)
                    exit_game()
                    break
                status = input("Do you still want to continue? Y/N ")
                if status.upper() == "N":
                    print("GoodBye!")
                    break
        elif (opponent.upper() == "COMPUTER"):
            type = int(input("(1) Random Computer or (2) Medium Computer? ")) #player can choose the mode of computer players between 2 quality levels
            player1_name = input("Input name for Player 1: ").upper()
            if (type == 1): #random computer player is chosen
                while True:
                    move = player_move(game_board,1)
                    game_board = apply_move(game_board,1,move[0],move[1],move[2])
                    display_board(game_board)
                    if check_victory(game_board,1,move[2]) == 3:
                       print("Draw!")
                       exit_game()
                       break
                    elif check_victory(game_board,1,move[2]) == 1:
                       print(player1_name + " wins!")
                       update_leaderboard(player1_name)
                       exit_game()
                       break
                    elif check_victory(game_board,1,move[2]) == 2:
                       print("Computer wins!")
                       exit_game()
                       break
                    computer_result = computer_move(game_board,2,1)
                    game_board = apply_move(game_board,2,computer_result[0],computer_result[1],computer_result[2])
                    print("Computer has made its move! Rotation Index: " + str(computer_result[2]))
                    display_board(game_board)
                    if check_victory(game_board,2,computer_result[2]) == 3:
                       print("Draw!")
                       exit_game()
                       break
                    elif check_victory(game_board,2,computer_result[2]) == 1:
                       print(player1_name + " wins!")
                       update_leaderboard(player1_name)
                       exit_game()
                       break
                    elif check_victory(game_board,2,computer_result[2]) == 2:
                       print("Computer wins!")
                       exit_game()
                       break
                    status = input("Do you still want to continue? Y/N ")
                    if status.upper() == "N":
                       print("GoodBye!")
                       break
            elif (type == 2): #medium computer player is chosen
                while True:
                    move = player_move(game_board,1)
                    game_board = apply_move(game_board,1,move[0],move[1],move[2])
                    display_board(game_board)
                    if check_victory(game_board,1,move[2]) == 3:
                       print("Draw!")
                       exit_game()
                       break
                    elif check_victory(game_board,1,move[2]) == 1:
                       print(player1_name + " wins!")
                       update_leaderboard(player1_name)
                       exit_game()
                       break
                    elif check_victory(game_board,1,move[2]) == 2:
                       print("Computer wins!")
                       exit_game()
                       break
                    computer_result = computer_move(game_board,2,2)
                    game_board = apply_move(game_board,2,computer_result[0],computer_result[1],computer_result[2])
                    print("Computer has made its move! Rotation Index: " + str(computer_result[2]))
                    display_board(game_board)
                    if check_victory(game_board,2,computer_result[2]) == 3:
                       print("Draw!")
                       exit_game()
                       break
                    elif check_victory(game_board,2,computer_result[2]) == 1:
                       print(player1_name + " wins!")
                       update_leaderboard(player1_name)
                       exit_game()
                       break
                    elif check_victory(game_board,2,computer_result[2]) == 2:
                       print("Computer wins!")
                       exit_game()
                       break
                    status = input("Do you still want to continue? Y/N ")
                    if status.upper() == "N":
                       print("GoodBye!")
                       break
            else: 
                print("No such option! Please try again!")
                menu()
        else:
            print("No such opponent! Please try again!")
            menu()
    elif option == 2:
        view_leaderboard()
        choice = input("Input exit to main menu ")
        if choice.upper() == "EXIT": #player can opt to exit the PENTAGO game is no other options are chosen
            menu()

menu()