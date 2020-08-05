# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:08:04 2020

@author: Mike
"""
from copy import deepcopy

def introduction():
    print('Welcome to Mike\'s Connect Four Game!')
    response = input('Would you like to play (two)-player or against the (com)puter?\n> ').lower()
    if response == 'two' or response == '2':
        two_player()
    elif response == 'com' or response == 'computer':
        ai_intro()
    else:
        print('Please type one of the given options.\n> ')
        introduction()

# function that creates a connect four table as at 7x1 array
def create_table():
    table = [[' ']*7 for i in range(6)]
    return table
    
def print_table(table):  # A function that displays a connect four table as an actual table, rather than as lists
    printed_row = ''
    content = '| {} |'
    column_counter = 0
    for row in table:
        for space in row:
            if column_counter % 7 == 0:
                printed_row += '\n'
            if space == 'X':
                printed_row += content.format('X')
            elif space == 'O':
                printed_row += content.format('O')
            else:
                printed_row += content.format(' ')
            column_counter += 1
    printed_table = printed_row + '\n  1    2    3    4    5    6    7'
    print(printed_table)

def select_space(table, character): # Function for making a move
    column = -1
    while column == -1:
        try: 
            response = int(input('Type the column you want to play in: \n> ')) -1
            if response >= 0 and response < 7:
                if table[0][response] != ' ':
                    print('This column is full, please try another')
                else:
                    column = response
            else:
                print('\nPlease enter a number between 1 and 7')
        except ValueError:
            print('\nPlease enter a number between 1 and 7')
    for i in range(1, 7):
        if table[-i][column] == ' ':
            table[-i][column] = character
            break
        
def ai_move(table, character, column):
    for i in range(1, 7):
        if table[-i][column] == ' ':
            table[-i][column] = character
            break

def win_checker(table):      # This function checks which character has won the game, or whether the board is full
    streak_counter = 0
    full_column_counter = 0
    characters = ['X', 'O']
    winner = ''
    for character in characters:
        num_four_streaks = 0
        for row in range(len(table)):
            for col in range(len(table[0])):
                if streak_counter == 4:
                    break
                streak_counter = 0
                if col < 4:   #check_horizontal
                    for i in range(4):  
                            if table[row][col+i] == character:
                                streak_counter += 1
                            else:
                                streak_counter = 0
                    if streak_counter >= 4:
                        num_four_streaks += 1
                if row < 3:            #check vertical
                    for i in range(4):
                        if table[row+i][col] == character:
                            streak_counter += 1
                        else:
                            streak_counter = 0
                    if streak_counter >= 4:
                        num_four_streaks += 1
                if row < 3 and col > 4 :  #check forward diagonal /
                    for i in range(4):
                        if table[row+i][col-i] == character:
                            streak_counter += 1
                        else: 
                            streak_counter = 0
                    if streak_counter >= 4:
                        num_four_streaks += 1
                                
                if row < 3 and col < 4:     #check backward diagonal \
                    for i in range(4):
                        if table[row+i][col+i] == character:
                            streak_counter += 1
                        else: 
                            streak_counter = 0
                    if streak_counter >= 4:
                        num_four_streaks += 1
        if num_four_streaks >= 1:
            winner = character
    for col in table[0]:        # Detects whether the column is full
        if col != ' ':
            full_column_counter += 1
    if winner == 'X':
        return float('inf')
    elif winner == 'O':
        return float('-inf')
    elif full_column_counter == 7:      #If all columns are full, ends the game with a draw
        return 0
    
def who_wins(table):    # Function to determine if a player has four in a row
    result =  ''
    if win_checker(table) == float('inf'):
        result = 'X'
    elif win_checker(table) == float('-inf'):
        result = 'O'
    elif win_checker(table) == 0:
        result = 'No one'
    return result
            
def two_player():           #This runs a two-player version of Connect Four, where the first player is X and the second O
    table = create_table()
    winner = ''
    print('\n\nX goes first!\n')
    while winner == '':
        print_table(table)
        # response = int(input('Type the column you want to play in: \n> ')) -1
        select_space(table, 'X')
        winner = who_wins(table)
        if winner != '':
            break
        print_table(table)
        # response = int(input('Type the column you want to play in: \n> ')) -1
        select_space(table, 'O')
        winner = who_wins(table)
    print_table(table)
    print(winner + ' wins!')
    print('\n\n')
    introduction()
         
def is_complete(table):
    if win_checker(table) != None:
        return True
    else:
        return False

# introduction()

def available_moves(board):
    available_moves = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            available_moves.append(col)         #identifying the possible moves
    return available_moves

def minimax(old_board, first_player, depth, alpha, beta, evaluate):
    if first_player == True:                    #Setting the character
        character = 'X'
        nonchar = 'O'
    else:
        character = 'O'
        nonchar = 'X'
    moves_available = available_moves(old_board)
    best_move = 4
    if depth == 0 or who_wins(old_board) != '':
        # print(evaluate(old_board, character, nonchar))
        return evaluate(old_board), 4
    else:
        if first_player == True:
            best_evaluation = float('-inf')
            for move in moves_available:
                #print(moves_available)
                # print(move)
                board = deepcopy(old_board)
                ai_move(board, character, move)
                evaluation = (minimax(board, not first_player, depth-1, alpha, beta, evaluate)[0])
                #print(evaluation)
                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
        else:
            best_evaluation = float('inf')
            for move in moves_available:
                #print(moves_available)
                # print(move)
                board = deepcopy(old_board)
                ai_move(board, character, move)
                evaluation = (minimax(board, not first_player, depth-1, alpha, beta, evaluate)[0])
                #print(evaluation)
                if evaluation < best_evaluation:
                    best_evaluation = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
    
    #print(best_evaluation, best_move)    
    return best_evaluation, best_move
        
def ai_evaluation(board):
    streak_number = 0
    if win_checker(board) == float('inf') or win_checker(board) == float('-inf'):
        return win_checker(board)
    else:
       streak_number = streak_counter(board, 'X') - streak_counter(board, 'O')
    return streak_number


def streak_counter(board, symbol):
  two_count = 0
  three_count = 0
  for col in range(len(board)):
    for row in range(len(board[0])):
      if board[col][row] != symbol: 
        continue
      #right
      if col < len(board) - 3:
        streak_count = 0
        for i in range(4):
          if board[col+i][row] == symbol:
            streak_count += 1
          elif board[col+i][row] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
      #left
      if col > 2:
        streak_count = 0
        for i in range(4):
          if board[col-i][row] == symbol:
            streak_count += 1
          elif board[col-i][row] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
       #up
      if row > 2:
        streak_count = 0
        for i in range(4):
          if board[col][row-i] == symbol:
            streak_count += 1
          elif board[col][row-i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
        #down
      if row < 3:
        streak_count = 0
        for i in range(4):
          if board[col][row+i] == symbol:
            streak_count += 1
          elif board[col][row+i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
      #up-right
      if (col < 3) and (row > 3):
        streak_count = 0
        for i in range(4):
          if board[col+i][row-i] == symbol:
            streak_count += 1
          elif board[col+i][row-i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
      #up_left
      if (col > 2) and (row > 2):
        streak_count = 0
        for i in range(4):
          if board[col-i][row-i] == symbol:
            streak_count += 1
          elif board[col-i][row-i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
      #down right
      if (col < 3) and (row < 3):
        streak_count = 0
        for i in range(4):
          if board[col+i][row+i] == symbol:
            streak_count += 1
          elif board[col+i][row+i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
      #down left
      if (col > 2) and (row < 3):
        streak_count = 0
        for i in range(4):
          if board[col-1][row+i] == symbol:
            streak_count += 1
          elif board[col-1][row+i] != ' ':
            streak_count = 0
            break
        if streak_count == 3:
          three_count +=1
        elif streak_count ==2:
          two_count +=1
  return two_count + three_count*3

def ai_game(difficulty):
    table = create_table()
    winner = ''
    while winner == '':
        print_table(table)
        select_space(table, 'X')
        winner = who_wins(table)
        print_table(table)
        if winner != '':
            break
        move = minimax(table, False, difficulty, float('-inf'), float('inf'), ai_evaluation)[1]
        print('\n\nThe computer went at ' + str(move+1) + '\n')
        #print(move)
        ai_move(table, 'O', move)
        winner = who_wins(table)
        if winner != '':
            break
    print_table(table)
    print(winner + ' wins!')
    print('\n\n')
    
def ai_game_second(difficulty):
    table = create_table()
    winner = ''
    while winner == '':
        move = minimax(table, False, difficulty, float('-inf'), float('inf'), ai_evaluation)[1]
        print('\n\nThe computer went at ' + str(move+1) + '\n')
        #print(move)
        ai_move(table, 'O', move)
        print_table(table)
        winner = who_wins(table)
        if winner != '':
            break
        select_space(table, 'X')
        winner = who_wins(table)
        print_table(table)
        if winner != '':
            break
    print_table(table)
    print(winner + ' wins!')
    print('\n\n')

def ai_intro():
   response = int(input('\nPlease choose an AI difficulty between 1 and 7 (note: higher difficulties will take longer to act):\n> '))
   if response >= 1 and response <=7:
        answer = input('\nWould you like to go first or second?:\n> ').lower()
        if answer in ['first', '1st', '1']:
            ai_game(response)
        elif answer in ['second', '2nd', '2']:
            ai_game_second(response)
        else:
            print('Please choose either first or second')
            ai_intro()
   else:
       print('Please enter a number between 1 and 7')
       ai_intro()
   introduction()
    
introduction()
    
