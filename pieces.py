import pygame

color_values = {'black': 1, 'white': -1}


class Piece():
    def __init__(self, color, image, board_position):
        """
        Initializes a Piece Object
        :param color: color of the piece (can be black or white)
        :param image: path of the image corresponding to the piece
        :param board_position: 2-tuple of location on the board
        """
        self.color = color
        self.image = image
        self.board_position = board_position

    def get_possible_moves(self, board_state):
        """
        Computes a list of possible moves for the piece
        :param board_state: the current state of the board
        :return: a list of 2-tuples consisting of coordinates of possible moves
        """
        pass


class King(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            row += dr
            col += dc
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board_state[row][col] is None:
                    moves.append((row, col))
                elif board_state[row][col].color != self.color:
                    moves.append((row, col))
        return moves


class Queen(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            moves.append((row, col))
                        break
                else:
                    break
        return moves


class Bishop(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            moves.append((row, col))
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, -1), (-2, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            row += dr
            col += dc
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board_state[row][col] is None:
                    moves.append((row, col))
                elif board_state[row][col].color != self.color:
                    moves.append((row, col))
        return moves


class Rook(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            moves.append((row, col))
                        break
                else:
                    break
        print(moves)
        if len(moves) == 0:
            self.kill()
        return moves


class Pawn(Piece):
    def __init__(self, color, image, board_position):
        super().__init__(color, image, board_position)
        self.initial_position = board_position

    def get_possible_moves(self, board_state):
        moves = list()
        row, col = self.board_position
        new_row = row + (1 * color_values[self.color])
        for i in range(-1, 2, 2):
            if (1 <= col + i <= 8 and board_state[new_row][col + i] is not None
                    and board_state[new_row][col + i].color != self.color):
                moves.append(tuple([new_row, col + i]))
        if board_state[new_row][col] is None:
            moves.append(tuple([new_row, col]))
            if (self.board_position == self.initial_position and
                    board_state[new_row + (1 * color_values[self.color])][col] is None):
                moves.append(tuple([new_row + (1 * color_values[self.color]), col]))
        return moves
