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
    check_board = copy.deepcopy(board)
    xs, ys, xd, yd = move
    check_board[xd][yd] = check_board[xs][ys]
    check_board[xs][ys] = None
    return not is_king_in_check(check_board, color)