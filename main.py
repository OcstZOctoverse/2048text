import random


board = [  #Board for the 2048 game
    [" ", " ", " ", " "],  #list inside list because each list is row and then column counts in the sub row
    [" ", " ", " ", " "],
    [" ", " ", " ", " "],
    [" ", " ", " ", " "]
]

def print_board(board_parameter):
    for row in board_parameter:
        print(row)

def find_empty_squares(board_parameter):  #board passes in for board parameter obviously
    empty_squares = []  #list for the empty squares
    for i in range(len(board_parameter)):  #goes for each cause len finds
        for j in range(len(board_parameter)):
            if board_parameter[i][j] == " ":  #i and j are row and column respectively i is the item in the first list and j is item in the sublist
                empty_squares.append((i, j))
    return empty_squares


def can_move_up(board_parameter, row, col):  #row and col are row and column. This function checks if square can go up
    if row == 0:  # Top row can't ever go up
        return False
    return board_parameter[row - 1][col] == " " or board_parameter[row - 1][col] == board[row][col]  #if something ahead is empty because row-1 or if the squares are combinable because checks the values of both squares


def can_move_right(board_parameter, row, col):
    if col == 3:
        return False
    return board_parameter[row][col + 1] == " " or board_parameter[row][col + 1] == board[row][col]


def can_move_left(board_parameter, row, col):
    if col == 0:
        return False
    return board_parameter[row][col - 1] == " " or board_parameter[row][col - 1] == board[row][col]


def can_move_down(board_parameter, row, col):
    if row == 3:
        return False
    return board_parameter[row + 1][col] == " " or board_parameter[row + 1][col] == board[row][col]


def left_movement(row):
    row2 = [i for i in row if i != " "]  #creates row2 which has only filled squares (squares without " ")
    row2 += [" "] * (len(row) - len(row2))  #adds empty at the back of the list on row. amount is calculated with the full row (4) minus the amount of the filled spaces
    return row2


def left_combine(row):
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != " ":  #row[i] is index of one square and if it equals the thing to the right of it, and they aren't both empty (two empties don't combine) then combine
            row[i] *= 2  #This combines the tiles
            row[i + 1] = " "  #the right factor of combination becomes an empty square
    return row


def go_left(board_parameter):
    board2 = []
    for row in board_parameter:  #for every row in the board
        row = left_movement(row)  #changes the rows/sub-lists in the board to the left_movement board
        row = left_combine(row)  #Same but for combine
        row = left_movement(row)  #Moves again to make everything right after the combine
        board2.append(row)  #makes new row with the changes
    return board2


def go_right(board_parameter):
    board2 = []
    for row in board_parameter:
        row = row[::-1]  #reverses the list
        row = left_movement(row)
        row = left_combine(row)
        row = left_movement(row)
        row = row[::-1]  #re-reversed the list
        board2.append(row)
    return board2


def x_to_y(board_parameter):  #for going up and down
    return [list(row) for row in zip(*board_parameter)]  #returns a list of and up and down version of the board_parameter matrix

def go_up(board_parameter):
    board_parameter = x_to_y(board_parameter)  #changes the board from x to y
    board_parameter = go_left(board_parameter)  #Then go left because left is now up
    return x_to_y(board_parameter)  #returns the board


def go_down(board_parameter):
    board_parameter = x_to_y(board_parameter)
    board_parameter = go_right(board_parameter)  #right is down
    return x_to_y(board_parameter)


def new_tile(board_parameter):
    empty_squares = find_empty_squares(board_parameter)  #assigns all empty squares to empty_squares
    if not empty_squares:  #If there aren't any empty squares, don't do anything
        return board_parameter
    row, col = random.choice(empty_squares)  #Chooses random square and assigns the values to row and col
    board_parameter[row][col] = 2 if random.random() < 0.9 else 4  #chooses whether it should be 2 if random choice is less than 0.9 and 4 otherwise
    return board_parameter  #gives the board back


def inputs(board_parameter, direction):
    if direction == 'w':  #w does up, a does left etc.
        board2 = go_up(board_parameter)
    elif direction == 'a':
        board2 = go_left(board_parameter)
    elif direction == 's':
        board2 = go_down(board_parameter)
    elif direction == 'd':
        board2 = go_right(board_parameter)
    else:
        return board_parameter, False

    if board2 != board_parameter:  #is the board is new after the moves, return the new board and True to say that it was a valid input
        return board2, True
    return board2, False  #otherwise not valid input


def game_over(board_parameter):
    if find_empty_squares(board_parameter):  #If can find empty squares, then game isn't over
        return False
    for i in range(4):
        for j in range(4):
            if can_move_up(board_parameter, i, j) or can_move_down(board_parameter, i, j) or can_move_right(board_parameter, i, j) or can_move_left(board_parameter, i, j):  #if any movement is possible on any square, not game over
                return False
    return True  #otherwise, game over


def play_game(board_parameter):
    board_parameter = new_tile(board_parameter)  #changes board to the one with a new tile twice to start game with a combine
    board_parameter = new_tile(board_parameter)
    while not game_over(board_parameter):
        print_board(board_parameter)  #print the board
        move = input("Enter move w or a or s or d): ").strip().lower()  #asks for input
        board_parameter, valid_move = inputs(board_parameter, move)  #the board after inputs is the board and valid move is just any move unless returns false then it's an invalid move
        if valid_move:
            board_parameter = new_tile(board_parameter)
        else:
            print("Invalid move! Try again.")


play_game(board)  #does the stuff
