import pieces
import copy


def is_king_in_check(board, color):
    """
    Checks whether the king of a certain color is in line of sight of an opposing piece
    :param board: the state of the board to be checked
    :param color: the color of the king
    :return: True if the king is in check, False otherwise
    """
    opposing_pieces = []
    king_position = None
    for i in range(1, 9):
        for j in range(1, 9):
            if isinstance(board[i][j], pieces.King) and board[i][j].color == color:
                king_position = (i, j)
            elif isinstance(board[i][j], pieces.Piece) and board[i][j].color != color:
                opposing_pieces.append(board[i][j])
    for piece in opposing_pieces:
        if king_position in piece.get_possible_moves(board):
            return True
    return False


def check_if_move_blocks_check(board, color, move):
    """
    Checks if there is still a check present on the table in the event of a provided move
    :param board: the state of the board
    :param color: the color that is moving
    :param move: the move to be checked
    :return: True if there is no check on the table anymore, False otherwise
    """
    check_board = copy.deepcopy(board)
    xs, ys, xd, yd = move
    check_board[xd][yd] = check_board[xs][ys]
    check_board[xs][ys] = None
    return not is_king_in_check(check_board, color)


def get_available_moves(board, color):
    """
    Gets all legal moves that a player of a certain color can make
    :param board: the state of the board
    :param color: the color of the player
    :return: the list of moves that can be made in the form of 4-tuples
    """
    moves = list()
    for i in range(1, 9):
        for j in range(1, 9):
            if isinstance(board[i][j], pieces.Piece) and board[i][j].color == color:
                for x, y in board[i][j].get_possible_moves(board):
                    moves.append(tuple([i, j, x, y]))
    return moves


def is_king_under_attack(board, color):
    """
    Checks if King is Attacked By any Piece
    :param board: state of the board
    :param color: the color of the king
    :return: True if Under Attack, False Otherwise
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    king_position = None
    for i in range(1, 9):
        for j in range(1, 9):
            if isinstance(board[i][j], pieces.King) and board[i][j].color == color:
                king_position = i, j
    for dr, dc in directions:
        row, col = king_position
        while True:
            row += dr
            col += dc
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board[row][col] is not None:
                    if board[row][col].color != color and (isinstance(board[row][col], pieces.Queen) or
                                                           isinstance(board[row][col], pieces.Rook)):
                        return True
                    else:
                        break
            else:
                break
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for dr, dc in directions:
        row, col = king_position
        while True:
            row += dr
            col += dc
            if 1 <= row <= 8 and 1 <= col <= 8:
                if board[row][col] is not None:
                    if board[row][col].color != color and (isinstance(board[row][col], pieces.Queen) or
                                                           isinstance(board[row][col], pieces.Bishop)):
                        return True
                    else:
                        break
            else:
                break
    directions = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, -1), (-2, 1)]
    for dr, dc in directions:
        row, col = king_position
        row += dr
        col += dc
        if 1 <= row <= 8 and 1 <= col <= 8:
            if board[row][col] is not None:
                if board[row][col].color != color and isinstance(board[row][col], pieces.Knight):
                    return True
                else:
                    break
        else:
            break
    for dr, dc in [(-1, 1), (-1, -1)]:
        row, col = king_position
        row += dr
        col += dc
        if 1 <= row <= 8 and 1 <= col <= 8:
            if board[row][col] is not None:
                if board[row][col].color != color and isinstance(board[row][col], pieces.Pawn):
                    return True
    return False
