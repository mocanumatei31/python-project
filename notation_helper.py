def get_notation_from_coordinates(row, col):
    """
    Gets algebraic notation of passed position
    :param row: the row of the position to be converted
    :param col: the column of the position to be converted
    :return: algebraic notation of passed position
    """
    return chr(col + ord('a') - 1) + str(row)


def get_coordinates_from_notation(algebraic):
    """
    Transforms algebraic notation into board coordinates
    :param algebraic: algebraic notation to be converted
    :return: 2-tuple of coordinates
    """
    return tuple([int(algebraic[1]), ord(algebraic[0]) - ord('a') + 1])
