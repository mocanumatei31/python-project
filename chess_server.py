import socket
import threading
import pickle

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
    while True:
        if colors[turn] == color:
            data = conn.recv(1024)
            if not data:
                break
            received_tuple = pickle.loads(data)
            print(f"Received tuple from {addr}: {received_tuple}")
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
