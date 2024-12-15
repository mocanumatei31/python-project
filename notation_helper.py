import pieces

piece_notations = {
    pieces.King: "K",
    pieces.Queen: "Q",
    pieces.Rook: "R",
    pieces.Bishop: "B",
    pieces.Knight: "N",
    pieces.Pawn: ""
}


def get_notation_from_coordinates(row, col, piece):
    """
    Gets algebraic notation of passed position
    :param piece: Piece that made the move
    :param row: the row of the position to be converted
    :param col: the column of the position to be converted
    :return: algebraic notation of passed position
    """
    return piece_notations[type(piece)] + chr(col + ord('a') - 1) + str(row)


def get_coordinates_from_notation(algebraic):
    """
    Transforms algebraic notation into board coordinates
    :param algebraic: algebraic notation to be converted
    :return: 2-tuple of coordinates
    """
    return tuple([int(algebraic[1]), ord(algebraic[0]) - ord('a') + 1])


