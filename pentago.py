# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:52:42 2023

Author: Derrick Wong Liang Jun

"""

import numpy as np
import random
import copy
import json

class GameBoard:
    def __init__(self, size=6):
        self.size = size
        self.board = np.zeros((self.size, self.size), dtype=int)
    
    def display(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(['.' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]))
        print()
    
    def is_full(self):
        return not np.any(self.board == 0)
    
    def check_move_valid(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col] == 0
        return False
    
    def apply_move(self, turn, row, col, rotation):
        self.board[row][col] = turn
        self.rotate(rotation)
    
    def rotate(self, rot):
        # Define rotation mappings
        rotation_map = {
            1: ('clockwise', 'top-right'),
            2: ('counter', 'top-right'),
            3: ('clockwise', 'bottom-right'),
            4: ('counter', 'bottom-right'),
            5: ('clockwise', 'bottom-left'),
            6: ('counter', 'bottom-left'),
            7: ('clockwise', 'top-left'),
            8: ('counter', 'top-left')
        }
        if rot not in rotation_map:
            return  # Invalid rotation
        
        direction, quadrant = rotation_map[rot]
        sub_board_coords = {
            'top-left': (slice(0, 3), slice(0, 3)),
            'top-right': (slice(0, 3), slice(3, 6)),
            'bottom-left': (slice(3, 6), slice(0, 3)),
            'bottom-right': (slice(3, 6), slice(3, 6))
        }
        rows, cols = sub_board_coords[quadrant]
        sub_board = self.board[rows, cols]
        k = 1 if direction == 'clockwise' else 3  # 90 degrees clockwise or counter (270 degrees)
        rotated_sub = np.rot90(sub_board, k=k)
        self.board[rows, cols] = rotated_sub
    
    def check_victory(self, turn, rot):
        # Check victory after applying rotation
        temp_board = copy.deepcopy(self.board)
        if self.check_status(temp_board, 1) and self.check_status(temp_board, 2):
            return 3  # Draw
        elif self.check_status(temp_board, 1):
            return 1
        elif self.check_status(temp_board, 2):
            return 2
        else:
            # Undo rotation
            inverse_rot = self.get_inverse_rotation(rot)
            if inverse_rot:
                self.rotate(inverse_rot)
                if self.check_status(self.board, turn):
                    return turn
                elif self.is_full():
                    return 3
                else:
                    return 0
            return 0
    
    def get_inverse_rotation(self, rot):
        inverse_map = {
            1: 2,
            2: 1,
            3: 4,
            4: 3,
            5: 6,
            6: 5,
            7: 8,
            8: 7
        }
        return inverse_map.get(rot, None)
    
    def check_status(self, board, turn):
        return (self.check_horizontal(board, turn) or
                self.check_vertical(board, turn) or
                self.check_diagonal(board, turn) or
                self.check_opposite_diagonal(board, turn))
    
    def check_horizontal(self, board, turn):
        for row in board:
            count = 0
            for cell in row:
                count = count + 1 if cell == turn else 0
                if count >= 5:
                    return True
        return False
    
    def check_vertical(self, board, turn):
        for col in board.T:
            count = 0
            for cell in col:
                count = count + 1 if cell == turn else 0
                if count >= 5:
                    return True
        return False
    
    def check_diagonal(self, board, turn):
        # Check all diagonals with length >=5
        for offset in range(-self.size + 5, self.size - 4):
            diag = np.diagonal(board, offset=offset)
            count = 0
            for cell in diag:
                count = count + 1 if cell == turn else 0
                if count >= 5:
                    return True
        return False
    
    def check_opposite_diagonal(self, board, turn):
        flipped_board = np.fliplr(board)
        return self.check_diagonal(flipped_board, turn)

class Player:
    def __init__(self, name, turn):
        self.name = name
        self.turn = turn  # 1 for Player 1 (X), 2 for Player 2 (O)
    
    def get_move(self, game_board):
        while True:
            try:
                row = int(input(f"{self.name} (X/O) - Choose your row (0-5): "))
                col = int(input(f"{self.name} (X/O) - Choose your column (0-5): "))
                rotation = int(input(f"{self.name} (X/O) - Choose your rotation (1-8): "))
                if not game_board.check_move_valid(row, col):
                    print("Invalid move! The cell is already occupied or out of bounds. Please try again.")
                    continue
                if rotation not in range(1, 9):
                    print("Invalid rotation! Please choose a rotation between 1 and 8.")
                    continue
                confirm = input(f"Confirm move - Row: {row}, Column: {col}, Rotation: {rotation} (Y/N): ").strip().upper()
                if confirm == 'Y':
                    return row, col, rotation
                else:
                    print("Move cancelled. Please enter your move again.")
            except ValueError:
                print("Invalid input! Please enter numeric values for row, column, and rotation.")

class ComputerPlayer(Player):
    def __init__(self, name, turn, level=1):
        super().__init__(name, turn)
        self.level = level  # 1 for Random, 2 for Medium
    
    def get_move(self, game_board):
        if self.level == 1:
            return self.random_move(game_board)
        else:
            return self.medium_move(game_board)
    
    def random_move(self, game_board):
        available_moves = [(i, j) for i in range(game_board.size) for j in range(game_board.size) if game_board.board[i][j] == 0]
        if not available_moves:
            return None
        row, col = random.choice(available_moves)
        rotation = random.randint(1, 8)
        print(f"Computer (Random) chooses Row: {row}, Column: {col}, Rotation: {rotation}")
        return row, col, rotation
    
    def medium_move(self, game_board):
        # First, check if computer can win in the next move
        for row in range(game_board.size):
            for col in range(game_board.size):
                if game_board.board[row][col] == 0:
                    temp_board = copy.deepcopy(game_board)
                    temp_board.board[row][col] = self.turn
                    for rot in range(1, 9):
                        temp_board.rotate(rot)
                        if temp_board.check_status(temp_board.board, self.turn):
                            print(f"Computer (Medium) chooses winning move - Row: {row}, Column: {col}, Rotation: {rot}")
                            return row, col, rot
                        temp_board.rotate(game_board.get_inverse_rotation(rot))  # Undo rotation
                    temp_board.board[row][col] = 0  # Undo move
        
        # Then, check if player can win in their next move and block it
        opponent_turn = 1 if self.turn == 2 else 2
        for row in range(game_board.size):
            for col in range(game_board.size):
                if game_board.board[row][col] == 0:
                    temp_board = copy.deepcopy(game_board)
                    temp_board.board[row][col] = opponent_turn
                    for rot in range(1, 9):
                        temp_board.rotate(rot)
                        if temp_board.check_status(temp_board.board, opponent_turn):
                            print(f"Computer (Medium) blocks at - Row: {row}, Column: {col}, Rotation: {rot}")
                            return row, col, rot
                        temp_board.rotate(game_board.get_inverse_rotation(rot))  # Undo rotation
                    temp_board.board[row][col] = 0  # Undo move
        
        # Otherwise, make a random move
        return self.random_move(game_board)

class Leaderboard:
    def __init__(self, filename="leader_board.json"):
        self.filename = filename
        self.leader_board = self.load_leaderboard()
    
    def load_leaderboard(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def view(self):
        if not self.leader_board:
            print("Leaderboard is empty.")
            return
        print("\nLeaderboard:")
        for idx, entry in enumerate(self.leader_board, start=1):
            print(f"Rank {idx}: {entry['name']} - {entry['score']} wins")
        print()
    
    def update(self, player_name):
        for entry in self.leader_board:
            if entry['name'] == player_name:
                entry['score'] += 1
                break
        else:
            self.leader_board.append({'name': player_name, 'score': 1})
        # Sort the leaderboard
        self.leader_board.sort(key=lambda x: x['score'], reverse=True)
        self.save_leaderboard()
    
    def save_leaderboard(self):
        with open(self.filename, "w") as file:
            json.dump(self.leader_board, file, indent=4)

class PentagoGame:
    def __init__(self):
        self.game_board = GameBoard()
        self.leaderboard = Leaderboard()
        self.player1 = None
        self.player2 = None
    
    def menu(self):
        while True:
            print("Welcome to 6x6 PENTAGO Tic-Tac-Toe!")
            print("(1): Play game")
            print("(2): View Leaderboard")
            print("(3): Exit")
            try:
                option = int(input("Select an option: "))
                if option == 1:
                    self.setup_game()
                elif option == 2:
                    self.leaderboard.view()
                elif option == 3:
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option! Please select 1, 2, or 3.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    def setup_game(self):
        opponent = input("Choose Opponent (Player/Computer): ").strip().upper()
        if opponent == "PLAYER":
            player1_name = input("Input name for Player 1: ").strip().upper()
            player2_name = input("Input name for Player 2: ").strip().upper()
            self.player1 = Player(player1_name, turn=1)
            self.player2 = Player(player2_name, turn=2)
            self.play_game()
        elif opponent == "COMPUTER":
            player1_name = input("Input name for Player 1: ").strip().upper()
            self.player1 = Player(player1_name, turn=1)
            computer_level = self.choose_computer_level()
            self.player2 = ComputerPlayer("Computer", turn=2, level=computer_level)
            self.play_game()
        else:
            print("Invalid opponent selection! Returning to main menu.")
    
    def choose_computer_level(self):
        while True:
            try:
                level = int(input("(1) Random Computer or (2) Medium Computer? "))
                if level in [1, 2]:
                    return level
                else:
                    print("Invalid selection! Choose 1 or 2.")
            except ValueError:
                print("Invalid input! Please enter 1 or 2.")
    
    def play_game(self):
        self.game_board = GameBoard()  # Reset the board
        current_player = self.player1
        while True:
            self.game_board.display()
            move = current_player.get_move(self.game_board)
            if move is None:
                print("No available moves! It's a draw.")
                break
            row, col, rotation = move
            self.game_board.apply_move(current_player.turn, row, col, rotation)
            victory = self.game_board.check_victory(current_player.turn, rotation)
            if victory == 1:
                self.game_board.display()
                print(f"{self.player1.name} (X) wins!")
                self.leaderboard.update(self.player1.name)
                break
            elif victory == 2:
                self.game_board.display()
                if isinstance(self.player2, ComputerPlayer):
                    print("Computer (O) wins!")
                else:
                    print(f"{self.player2.name} (O) wins!")
                if isinstance(self.player2, ComputerPlayer):
                    # Optionally, you can track computer wins differently
                    pass
                else:
                    self.leaderboard.update(self.player2.name)
                break
            elif victory == 3:
                self.game_board.display()
                print("It's a draw!")
                break
            if self.game_board.is_full():
                self.game_board.display()
                print("The board is full! It's a draw.")
                break
            # Switch player
            current_player = self.player2 if current_player == self.player1 else self.player1
        self.exit_game()
    
    def exit_game(self):
        while True:
            choice = input("Do you want to play again? (Y/N): ").strip().upper()
            if choice == 'Y':
                self.menu()
                break
            elif choice == 'N':
                print("Goodbye!")
                exit()
            else:
                print("Invalid input! Please enter Y or N.")

if __name__ == "__main__":
    PentagoGame().menu()
