import logic_helper as lh


class Piece:
    def __init__(self, color, image, board_position, player_color):
        """
        Initializes a Piece Object
        :param color: color of the piece (can be black or white)
        :param image: path of the image corresponding to the piece
        :param board_position: 2-tuple of location on the board
        """
        self.color = color
        self.image = image
        self.board_position = board_position
        self.has_moved = False
        self.color_values = {'black': 1, 'white': -1}
        self.rev_values(player_color)

    def rev_values(self, player_color):
        if player_color == 'black':
            self.color_values['black'] = -1
            self.color_values['white'] = 1

    def get_possible_moves(self, board_state):
        """
        Computes a list of possible moves for the piece
        :param board_state: the current state of the board
        :return: a list of 2-tuples consisting of coordinates of possible moves
        """
        pass

    def move(self, row, col, board_state):
        px, py = self.board_position
        board_state[row][col] = self
        board_state[px][py] = None
        self.board_position = (row, col)
        self.has_moved = True


class King(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)
        self.initial_position = board_position

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            row += dr
            col += dc
            move = tuple([self.board_position[0], self.board_position[1], row, col])
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board_state[row][col] is None:
                    if (self.color_values[self.color] == 1 or
                            lh.check_if_move_blocks_check(board_state, self.color, move)):
                        moves.append((row, col))
                else:
                    if board_state[row][col].color != self.color:
                        if (self.color_values[self.color] == 1 or
                                lh.check_if_move_blocks_check(board_state, self.color, move)):
                            moves.append((row, col))
        if not self.has_moved:
            for dr, dc in [(0, 1), (0, -1)]:
                row, col = self.board_position
                while True:
                    row += dr
                    col += dc
                    if 1 <= row <= 8 and 1 <= col <= 8:
                        if board_state[row][col] is not None:
                            if (board_state[row][col].color == self.color and
                                    isinstance(board_state[row][col], Rook) and not board_state[row][col].has_moved):
                                move = tuple([self.board_position[0], self.board_position[1], row, col - dc])
                                if (self.color_values[self.color] == 1 or
                                        lh.check_if_move_blocks_check(board_state, self.color, move)):
                                    moves.append((row, col - dc))
                            else:
                                break
                    else:
                        break
        return moves

    def move(self, row, col, board_state):
        px, py = self.board_position
        if abs(col - py) == 2:
            rook = None
            if col > py:
                rook = board_state[row][col + 1]
                rook.move(row, col - 1, board_state)
            else:
                rook = board_state[row][col - 1]
                rook.move(row, col + 1, board_state)
        elif abs(col - py) == 3:
            rook = None
            if col > py:
                rook = board_state[row][col + 1]
                rook.move(row, col - 2, board_state)
                col -= 1
            else:
                rook = board_state[row][col - 1]
                rook.move(row, col + 2, board_state)
                col += 1
        board_state[row][col] = self
        board_state[px][py] = None
        self.board_position = (row, col)
        self.has_moved = True


class Queen(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                move = tuple([self.board_position[0], self.board_position[1], row, col])
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        if (self.color_values[self.color] == 1 or
                                lh.check_if_move_blocks_check(board_state, self.color, move)):
                            moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            if (self.color_values[self.color] == 1 or
                                    lh.check_if_move_blocks_check(board_state, self.color, move)):
                                moves.append((row, col))
                        break
                else:
                    break
        return moves


class Bishop(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                move = tuple([self.board_position[0], self.board_position[1], row, col])
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        if (self.color_values[self.color] == 1 or
                                lh.check_if_move_blocks_check(board_state, self.color, move)):
                            moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            if (self.color_values[self.color] == 1 or
                                    lh.check_if_move_blocks_check(board_state, self.color, move)):
                                moves.append((row, col))
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, -1), (-2, 1)]
        for dr, dc in directions:
            row, col = self.board_position
            row += dr
            col += dc
            move = tuple([self.board_position[0], self.board_position[1], row, col])
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board_state[row][col] is None:
                    if (self.color_values[self.color] == 1 or
                            lh.check_if_move_blocks_check(board_state, self.color, move)):
                        moves.append((row, col))
                elif board_state[row][col].color != self.color:
                    if self.color_values[self.color] == 1 or lh.check_if_move_blocks_check(board_state, self.color,
                                                                                           move):
                        moves.append((row, col))
        return moves


class Rook(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)
        self.initial_position = board_position

    def get_possible_moves(self, board_state):
        moves = list()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            row, col = self.board_position
            while True:
                row += dr
                col += dc
                move = tuple([self.board_position[0], self.board_position[1], row, col])
                if 1 <= row <= 8 and 1 <= col <= 8:
                    if board_state[row][col] is None:
                        if (self.color_values[self.color] == 1 or
                                lh.check_if_move_blocks_check(board_state, self.color, move)):
                            moves.append((row, col))
                    else:
                        if board_state[row][col].color != self.color:
                            if (self.color_values[self.color] == 1 or
                                    lh.check_if_move_blocks_check(board_state, self.color, move)):
                                moves.append((row, col))
                        break
                else:
                    break
        return moves


class Pawn(Piece):
    def __init__(self, color, image, board_position, player_color):
        super().__init__(color, image, board_position, player_color)
        self.initial_position = board_position

    def get_possible_moves(self, board_state):
        moves = list()
        row, col = self.board_position
        new_row = row + (1 * self.color_values[self.color])
        for i in range(-1, 2, 2):
            move = tuple([self.board_position[0], self.board_position[1], new_row, col + i])
            if ((1 <= col + i <= 8 and board_state[new_row][col + i] is not None
                 and board_state[new_row][col + i].color != self.color) and
                    (self.color_values[self.color] == 1 or
                     lh.check_if_move_blocks_check(board_state, self.color, move))):
                moves.append(tuple([new_row, col + i]))
        if board_state[new_row][col] is None:
            move = tuple([self.board_position[0], self.board_position[1], new_row, col])
            if (self.color_values[self.color] == 1 or
                    lh.check_if_move_blocks_check(board_state, self.color, move)):
                moves.append(tuple([new_row, col]))
            move = tuple(
                [self.board_position[0], self.board_position[1], new_row + (1 * self.color_values[self.color]), col])
            if ((self.board_position == self.initial_position and
                 board_state[new_row + (1 * self.color_values[self.color])][col] is None)
                    and (self.color_values[self.color] == 1 or
                         lh.check_if_move_blocks_check(board_state, self.color, move))):
                moves.append(tuple([new_row + (1 * self.color_values[self.color]), col]))
        return moves
