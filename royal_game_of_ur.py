"""
File:         royal_game_of_ur.py
Author:       Alex Strong
Date:         11/15/2020
Section:      44
E-mail:       astrong3@umbc.edu
Description:  This code is the primary file to running the royal game of ur.  Which
              involves 2 players each getting 7 pieces and trying to get their pieces
              to complete the course of the board.  Through the course of the board, there
              are cases in which you can knock off your opponent's pieces and spots that
              allow you to stay safe.  As soon as you get all 7 of your pieces to complete
              the course then you win.
"""
from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece


class RoyalGameOfUr:
    STARTING_PIECES = 7

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)
        # more code should be added to the function
        self.white_pieces = []
        self.white_piece_objects = []
        self.black_pieces = []
        self.black_piece_objects = []
        self.white_name = ''
        self.black_name = ''
        self.winner = ''



    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))
                # print(self.board)
                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def register_pieces(self):
        # sets up the piece symbols
        for i in range(1, self.STARTING_PIECES + 1):
            self.white_pieces.append('W' + str(i))
            self.black_pieces.append('B' + str(i))
        # keeps track of where all the rosettes are
        rosette_spots = []
        # keeps track of all entrances and exits and rosettes
        for rows in range(len(self.board)):
            for columns in range(len(self.board[rows])):
                if self.board[rows][columns].entrance == 'White':
                    white_start = self.board[rows][columns]
                elif self.board[rows][columns].entrance == 'Black':
                    black_start = self.board[rows][columns]
                elif self.board[rows][columns].exit == 'Black':
                    black_exit = self.board[rows][columns]
                elif self.board[rows][columns].exit == 'White':
                    white_exit = self.board[rows][columns]
                elif self.board[rows][columns].rosette:
                    rosette_spots.append(self.board[rows][columns].position)
        # makes the pieces a part of the UrPiece class
        for white_piece_register in range(len(self.white_pieces)):
            self.white_piece_objects.append(UrPiece('White', self.white_pieces[white_piece_register], rosette_spots, white_start, white_exit))
        for black_piece_register in range(len(self.black_pieces)):
            self.black_piece_objects.append(UrPiece('Black', self.black_pieces[black_piece_register], rosette_spots, black_start, black_exit))

    def game_continue_checker(self):
        """
        checks to see if the game is still going on the basis if all 7 of the pieces are complete or not
        :return:
        """
        white_confirmation = 0
        for white in range(len(self.white_piece_objects)):
            if self.white_piece_objects[white].complete:
                white_confirmation += 1
        black_confirmation = 0
        for black in range(len(self.black_piece_objects)):
            if self.black_piece_objects[black].complete:
                black_confirmation += 1
        if white_confirmation == len(self.white_piece_objects) or black_confirmation == len(self.black_piece_objects):
            if white_confirmation == len(self.white_piece_objects):
                self.winner = self.white_name
            if black_confirmation == len(self.black_piece_objects):
                self.winner = self.black_name
            return False
        else:
            return True

    def play_game(self):
        """
            This function is the main driving function that runs all functions throughout it
        """
        white_player = input('What is your name? ')
        self.white_name = white_player
        print(white_player, ' you will play as white.')
        black_player = input('What is your name? ')
        self.black_name = black_player
        print(black_player, ' you will play as black.')
        self.register_pieces()
        game_continues = True
        # while loops which iterates through taking turns until the game is finished
        while game_continues:
            game_continues = self.game_continue_checker()
            self.take_turn_white()
            self.take_turn_black()
        print('Game is over! ', self.winner, 'wins!')

    def take_turn_white(self, take_turn_again=False):
        """
        Same function as take_turn_black.  Rolls the dice for each turn, as well as taking in the parameter
        that determines if the function is being recursed when someone lands on a rosette.  Also runs
        can_move to be able to print out a list of moves that you can make
        :param take_turn_again:
        :return:
        """
        self.display_board()
        dice_roll = self.roll_d4_dice()
        # if this function is being rerun due to a rosette it will print out a different prompt to inform you
        if take_turn_again:
            print(self.white_name, 'you landed on a rosette so roll again! New roll is: ', dice_roll)
        else:
            print(self.white_name, 'rolled a', dice_roll)
        counter = 1
        viable_moves_white = {}
        # if dice roll is 0 then it will not give you an option to select a move to make
        if dice_roll == 0:
            print('Out of luck')
            anything = input('Enter anything to skip turn: ')
        else:
            # prints out all of your options to move after checking if it can_move
            for w in range(len(self.white_piece_objects)):
                if self.white_piece_objects[w].can_move(dice_roll):
                    # if piece is not on the board then this statement will occur
                    if not self.white_piece_objects[w].position:
                        off_the_board = 'currently off the board'
                        print(counter, ':', self.white_piece_objects[w].symbol, off_the_board)
                    # if piece on the board then it will tell you where this piece is currently at
                    else:
                        print(counter, ':', self.white_piece_objects[w].symbol, self.white_piece_objects[w].position.position)
                    viable_moves_white[counter] = (self.white_piece_objects[w])
                    counter += 1
            white_input = int(input(self.white_name + ', what move would you wish to make? '))
            # will return true if you land on a rosette
            if self.move_piece(viable_moves_white[white_input], dice_roll):
                print(self.white_name, 'you landed on a rosette! Time to roll again!')
                take_turn_again = True
                self.take_turn_white(take_turn_again)

    def take_turn_black(self, take_turn_again=False):
        """
        Same exact comments as take_turn_white
        :param take_turn_again:
        :return:
        """
        self.display_board()
        dice_roll = self.roll_d4_dice()
        if take_turn_again:
            print(self.black_name, 'you landed on a rosette so roll again! New roll is: ', dice_roll)
        else:
            print(self.black_name, 'rolled a', dice_roll)
        counter = 1
        viable_moves_black = {}
        if dice_roll == 0:
            print('Out of luck')
            anything = input('Enter anything to skip turn: ')
        else:
            for b in range(len(self.black_piece_objects)):
                if self.black_piece_objects[b].can_move(dice_roll):
                    if not self.black_piece_objects[b].position:
                        off_the_board = 'currently off the board'
                        print(counter, ':', self.black_piece_objects[b].symbol, off_the_board)
                    else:
                        print(counter, ':', self.black_piece_objects[b].symbol, self.black_piece_objects[b].position.position)
                    viable_moves_black[counter] = (self.black_piece_objects[b])

                    counter += 1
            black_input = int(input(self.black_name + ', what move would you wish to make? '))
            if self.move_piece(viable_moves_black[black_input], dice_roll):
                print(self.black_name, 'you landed on a rosette! Time to roll again!')
                take_turn_again = True
                self.take_turn_black(take_turn_again)

    def move_piece(self, targeted_object, roll):
        """
        This function does the actual moving of the pieces. Also changes variables in the BoardSquare and UrPiece
        classes
        :param targeted_object:
        :param roll:
        :return:
        """
        temp_roll = roll
        piece_object = targeted_object
        final_square = None
        # keeps track of the previous square object
        previous_square = None
        entrance_used = False
        is_it_complete = False

        # only works if there is a previous position and the piece isn't complete
        if piece_object.position and not piece_object.complete:
            previous_square = piece_object.position
        while temp_roll != 0:
            # if the piece has no position (meaning it is not on the board)
            if not piece_object.position and not piece_object.complete:
                # sets the position to the entrance
                piece_object.position = piece_object.entrance
                final_square = piece_object.position
                entrance_used = True
            # if the piece already has a position (meaning it is already on the board)
            elif piece_object.position and not piece_object.complete:
                if piece_object.color == 'White':
                    # this determines if the piece has reached it's exit point
                    if piece_object.position.exit == 'White' and temp_roll == 1:
                        piece_object.complete = True
                        piece_object.position = None
                        previous_square.piece = None
                        is_it_complete = True
                        temp_roll = 0
                    else:
                        # runs if it has not yet reached exit point
                        piece_object.position = piece_object.position.next_white
                        final_square = piece_object.position
                else:
                    # this determines if the piece has reached it's exit point
                    if piece_object.exit == 'Black' and temp_roll == 1:
                        piece_object.complete = True
                        piece_object.position = None
                        previous_square.piece = None
                        is_it_complete = True
                        temp_roll = 0
                    else:
                        # runs if it has not yet reached exit point
                        piece_object.position = piece_object.position.next_black
                        final_square = piece_object.position
            # minus 1 roll until it reaches 0 and is done moving
            temp_roll -= 1

        # after the while loop completes it then updates the board
        if roll > 0 and not is_it_complete:
            if final_square:
                if final_square.piece:
                    final_square.piece.position = None
                    final_square.piece = None
                    final_square.piece = piece_object
                else:
                    final_square.piece = piece_object
                if not entrance_used:
                    previous_square.piece = None
                if final_square.rosette:
                    print('ROSETTE HERE')
                    return True
                else:
                    return False


if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
