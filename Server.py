import random
import socket
import CryptoDef as crypto
import json
import random


def registration(conn, login):
    P = crypto.generate_simple_number(1000, 100000000)
    Q = crypto.generate_simple_number(1000, 100000000)
    while P == Q:
        Q = crypto.generate_simple_number(1000, 100000000)
    N = P * Q
    conn.send(str(N).encode())

    V = conn.recv(1024).decode()

    account = {
        "N": N,
        "V": int(V)
    }
    with open('data_file.json') as f:
        data = json.load(f)
    data[login] = account
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)
    return


def server_program():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Waiting connection...")
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    authorize = True

    message = conn.send("Enter a login: ".encode())
    data = conn.recv(1024).decode()
    login = str(data)

    with open('data_file.json') as f:
        data = json.load(f)

    if login not in data:
        conn.send("Wrong user. Lets registration: ".encode())
        registration(conn, login)
        return
    f.close()
    with open('data_file.json') as f:
        database = json.load(f)

    # Open keys
    N = int(database[login]["N"])
    V = int(database[login]["V"])
    f.close()
    conn.send(str(N).encode())
    conn.send(str(V).encode())
    print("User login: " + login)

    t = 20
    for step in range(t):
        x = int(conn.recv(1024).decode())

        e = random.choice([0, 1])
        conn.send(str(e).encode())

        y = int(conn.recv(1024).decode())

        left_op = pow(y * y, 1, N)
        right_op = (x * pow(V, e)) % N
        if left_op == right_op and step != 19:
            authorize = True
            conn.send("Continue...".encode())
            continue

        if left_op == right_op and step == 19:
            conn.send("Success. Welcome".encode())
            continue


        conn.send("Wrong user. Disconnect...".encode())
        print("Wrong user. Disconnect...")
        conn.close()
        return


if __name__ == '__main__':
    while True:
        server_program()
