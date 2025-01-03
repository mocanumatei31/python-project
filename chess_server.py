import random
import socket
import threading
import pickle
import logic_helper as lh
import pieces
import select

from chess import player_values

HOST = '127.0.0.1'
PORT = 8080

clients = list()
turn = 0
colors = ['white', 'black']
games = list()


def handle_client(conn, addr, game):
    """
    Handles the moves sent in by a client in a pvp game
    :param conn: the connected socket corresponding to the player
    :param addr: player's address
    :param game: id of the played game
    """
    global turn
    print('Connected by', addr)
    color = None
    if conn == games[game][0]:
        data = pickle.dumps('white')
        color = 'white'
    else:
        data = pickle.dumps('black')
        color = 'black'
    conn.sendall(data)
    try:
        while isinstance(games[game], list):
            if colors[turn] == color:
                data = conn.recv(4096)
                if not data:
                    break
                received_tuple = pickle.loads(data)
                print(f"Received tuple from {addr}: {received_tuple}")
                if isinstance(received_tuple, tuple):
                    board = received_tuple[0]
                    if insufficient_material(board):
                        for client in games[game]:
                            if client != conn:
                                client.sendall(pickle.dumps(0))
                                received_tuple = None
                            else:
                                client.sendall(pickle.dumps(0))
                        games[game] = 0
                        break
                    rev_board = [[None] * 9 for _ in range(9)]
                    for i in range(1, 9):
                        for j in range(1, 9):
                            rev_board[i][j] = board[8 - i + 1][8 - j + 1]
                            if isinstance(rev_board[i][j], pieces.Piece):
                                rev_board[i][j].board_position = (i, j)
                                if rev_board[i][j].color_values['black'] == -1:
                                    rev_board[i][j].color_values['black'] = 1
                                    rev_board[i][j].color_values['white'] = -1
                                else:
                                    rev_board[i][j].color_values['black'] = -1
                                    rev_board[i][j].color_values['white'] = 1
                    print(color)
                    if len(lh.get_available_moves(rev_board, colors[1 - turn])) == 0:
                        if lh.is_king_in_check(rev_board, colors[1 - turn]):
                            for client in games[game]:
                                if client != conn:
                                    client.sendall(pickle.dumps(-1))
                                    received_tuple = None
                                else:
                                    client.sendall(pickle.dumps(1))
                        else:
                            for client in games[game]:
                                if client != conn:
                                    client.sendall(pickle.dumps(0))
                                    received_tuple = None
                                else:
                                    client.sendall(pickle.dumps(0))
                        games[game] = 0
                        break
                    for client in games[game]:
                        if client != conn:
                            client.sendall(pickle.dumps(received_tuple))
                            received_tuple = None
                    turn = 1 - turn
                else:
                    for client in games[game]:
                        if client != conn:
                            client.sendall(pickle.dumps(1))
                            received_tuple = None
                    games[game] = 0
                    break
    except ConnectionResetError:
        print(111)
        read_sockets, _, _ = select.select(games[game], [], [])
        for sock in read_sockets:
            data = sock.recv(1024)
            if not data:
                if sock is conn:
                    for client in games[game]:
                        if client != conn:
                            client.sendall(pickle.dumps(1))
                else:
                    conn.sendall(pickle.dumps(1))
    conn.close()
    # clients.remove((conn, addr))
    print(f"Connection with {addr} closed.")


def handle_client_v_computer(conn, addr):
    """
    Handles the moves sent in by a client in a pvc game
    :param conn: :param conn: the connected socket corresponding to the player
    :param addr: player's address
    """
    print('Connected by', addr)
    color = None
    comp_color = None
    rand = random.randint(0, 1)
    if rand == 1:
        data = pickle.dumps('white')
        color = 'white'
        comp_color = 'black'
    else:
        data = pickle.dumps('black')
        color = 'black'
        comp_color = 'white'
    conn.sendall(data)
    received_tuple = None
    while True:
        rev_board = None
        if comp_color == 'black' or received_tuple is not None:
            data = conn.recv(4096)
            if not data:
                break
            received_tuple = pickle.loads(data)
            print(f"Received tuple from {addr}: {received_tuple}")
            board = received_tuple[0]
            rev_board = [[None] * 9 for _ in range(9)]
            for i in range(1, 9):
                for j in range(1, 9):
                    rev_board[i][j] = board[8 - i + 1][8 - j + 1]
                    if isinstance(rev_board[i][j], pieces.Piece):
                        rev_board[i][j].board_position = (i, j)
                        if rev_board[i][j].color_values['black'] == -1:
                            rev_board[i][j].color_values['black'] = 1
                            rev_board[i][j].color_values['white'] = -1
                        else:
                            rev_board[i][j].color_values['black'] = -1
                            rev_board[i][j].color_values['white'] = 1
            if len(lh.get_available_moves(rev_board, comp_color)) == 0:
                if lh.is_king_under_attack(rev_board, comp_color):
                    conn.sendall(pickle.dumps(1))
                else:
                    conn.sendall(pickle.dumps(0))
                break
        if rev_board is None:
            rev_board = generate_initial_board(comp_color)
        moves = lh.get_available_moves(rev_board, comp_color)
        move = random.choice(moves)
        piece = rev_board[move[0]][move[1]]
        piece.move(move[2], move[3], rev_board)
        board = rev_board
        rev_board = [[None] * 9 for _ in range(9)]
        for i in range(1, 9):
            for j in range(1, 9):
                rev_board[i][j] = board[8 - i + 1][8 - j + 1]
                if isinstance(rev_board[i][j], pieces.Piece):
                    rev_board[i][j].board_position = (i, j)
                    if rev_board[i][j].color_values['black'] == -1:
                        rev_board[i][j].color_values['black'] = 1
                        rev_board[i][j].color_values['white'] = -1
                    else:
                        rev_board[i][j].color_values['black'] = -1
                        rev_board[i][j].color_values['white'] = 1
        if len(lh.get_available_moves(rev_board, color)) == 0:
            if lh.is_king_under_attack(rev_board, color):
                conn.sendall(pickle.dumps(-1))
            else:
                conn.sendall(pickle.dumps(0))
            break
        received_tuple = [rev_board]
        received_tuple.extend(move)
        received_tuple = tuple(received_tuple)
        conn.sendall(pickle.dumps(received_tuple))


def generate_initial_board(comp_color):
    """
    Generates the board state according to initial configuration of a chess game
    """
    board_state = [[None] * 9 for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if 0 < row <= 2:
                color = [x for x in player_values if x != comp_color][0]
                image_path = color[0]
            elif row > 6:
                color = comp_color
                image_path = color[0]
            else:
                color = None
            if row == 1 or row == 8:
                if col == 1 or col == 8:
                    board_state[row][col] = pieces.Rook(color, f"assets/{image_path}r.png", (row, col),
                                                        comp_color)
                elif col == 2 or col == 7:
                    board_state[row][col] = pieces.Knight(color, f"assets/{image_path}n.png", (row, col),
                                                          comp_color)
                elif col == 3 or col == 6:
                    board_state[row][col] = pieces.Bishop(color, f"assets/{image_path}b.png", (row, col),
                                                          comp_color)
                elif (col == 4 and comp_color == 'white') or (col == 5 and comp_color == 'black'):
                    board_state[row][col] = pieces.Queen(color, f"assets/{image_path}q.png", (row, col),
                                                         comp_color)
                elif (col == 5 and comp_color == 'white') or (col == 4 and comp_color == 'black'):
                    board_state[row][col] = pieces.King(color, f"assets/{image_path}k.png", (row, col),
                                                        comp_color)
            elif row == 2 or row == 7:
                board_state[row][col] = pieces.Pawn(color, f"assets/{image_path}p.png", (row, col),
                                                    comp_color)
    return board_state


def insufficient_material(board):
    white_pieces = {}
    black_pieces = {}
    coefficient = {}
    for row in board:
        for piece in row:
            if piece is not None:
                if piece.color == 'white':
                    white_pieces[type(piece)] = white_pieces.get(type(piece), 0) + 1
                else:
                    black_pieces[type(piece)] = black_pieces.get(type(piece), 0) + 1
    coefficient[pieces.King] = 0
    coefficient[pieces.Knight] = 1
    coefficient[pieces.Bishop] = 2
    coefficient[pieces.Rook] = 3
    coefficient[pieces.Queen] = 4
    coefficient[pieces.Pawn] = 5
    white_score = 0
    black_score = 0
    for t in white_pieces.keys():
        white_score += 2 ** coefficient[t]
    for t in black_pieces.keys():
        black_score += 2 ** coefficient[t]
    if white_score == 1 and (black_score in [1, 3] or (black_score == 5 and black_pieces[pieces.Bishop] == 1)):
        return True
    if black_score == 1 and (white_score in [1, 3] or (white_score == 5 and white_pieces[pieces.Bishop] == 1)):
        return True
    return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    threads = []
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        data = pickle.loads(data)
        print(data)
        if data == 'human':
            if len(games) == 0 or len(games[-1]) == 2:
                games.append([conn])
            else:
                games[-1].append(conn)
            if len(games[-1]) == 2:
                player1, player2 = games[-1]
                client_thread1 = threading.Thread(target=handle_client, args=(player1, addr, len(games) - 1))
                client_thread2 = threading.Thread(target=handle_client, args=(player2, addr, len(games) - 1))
                client_thread1.start()
                client_thread2.start()
        else:
            client_thread1 = threading.Thread(target=handle_client_v_computer, args=(conn, addr))
            client_thread1.start()
