"""
File:         board_square.py
Author:       Alex Strong
Date:         11/15/2020
Section:      44
E-mail:       astrong3@umbc.edu
Description:  This code stores the classes which assist to run the game such as the
              UrPiece class and the BoardSquare class which contain methods and attributes
              to keep track of components, and help the game to run smoothly
"""
class UrPiece:
    def __init__(self, color, symbol, rosettes, entrance, exit):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol
        self.rosettes = rosettes
        self.entrance = entrance
        self.exit = exit

    def can_move(self, num_moves):
        """
        Runs basically the same code as move_piece function, but instead of changing piece and board values
        it instead checks to see if the piece is able to remove and returns either true or false
        :param num_moves:
        :return:
        """
        temp_num_moves = num_moves
        this_piece = self
        most_recent_square = None
        original_position = self.position

        # same code comments as move_piece
        while temp_num_moves != 0:
            if not this_piece.position and not this_piece.complete:
                this_piece.position = this_piece.entrance
                most_recent_square = this_piece.position
            elif this_piece.position and not this_piece.complete:
                if this_piece.color == 'White':
                    if this_piece.position.exit == 'White':
                        if temp_num_moves == 1:
                            # if the piece is on an exit position and can move only 1 spot forward then it can move
                            return True
                        else:
                            # if the piece reaches exit position and has more than 1 move then it cannot exit
                            return False
                    else:
                        this_piece.position = this_piece.position.next_white
                        most_recent_square = this_piece.position
                else:
                    if this_piece.color == 'Black':
                        if this_piece.position.exit == 'Black':
                            if temp_num_moves == 1:
                                # same as with white color
                                return True
                            else:
                                return False
                        else:
                            this_piece.position = this_piece.position.next_black
                            most_recent_square = this_piece.position
            temp_num_moves -= 1
        this_piece.position = original_position

        if most_recent_square:
            if most_recent_square.piece:
                # if color is the same then you cannot move onto that piece
                if most_recent_square.piece.color == self.color:
                    return False
                # if color is different but the piece is on a rosette then you cannot bump them off
                elif most_recent_square.piece.color != self.color and most_recent_square.rosette:
                    return False
                # if color is different but piece not on rosette then you can move there and bump them off
                elif most_recent_square.piece.color != self.color and not most_recent_square.rosette:
                    return True
            # if square piece is empty then you can move onto it
            else:
                return True


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
