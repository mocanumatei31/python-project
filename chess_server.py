import socket
import threading
import pickle
import logic_helper as lh
import pieces

HOST = '127.0.0.1'
PORT = 8080

clients = list()
turn = 0
colors = ['white', 'black']
games = list()


def handle_client(conn, addr, game):
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
    while isinstance(games[game], list):
        if colors[turn] == color:
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
            if len(lh.get_available_moves(rev_board, colors[1 - turn])) == 0:
                for client in games[game]:
                    if client != conn:
                        client.sendall(pickle.dumps(0))
                        received_tuple = None
                    else:
                        client.sendall(pickle.dumps(1))
                games[game] = 0
                break
            for client in games[game]:
                if client != conn:
                    client.sendall(pickle.dumps(received_tuple))
                    received_tuple = None
            turn = 1 - turn


    conn.close()
    clients.remove((conn, addr))
    print(f"Connection with {addr} closed.")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    threads = []
    while True:
        conn, addr = s.accept()
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
