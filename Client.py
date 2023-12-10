import socket
import CryptoDef as crypto
import json
import random

def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))

    data = client_socket.recv(1024).decode()
    print(data)
    message = input("->")  # login
    client_socket.send(message.encode())

    data = client_socket.recv(1024).decode()
    if data == "Wrong user. Lets registration: ":
        print('Received from server: ' + data)
        N = int(client_socket.recv(1024).decode())
        S = crypto.generate_friend_simple_numper(int(N))
        while S > N - 1:
            S = crypto.generate_friend_simple_numper(int(N))
        f = open(message + "_password", "w")
        f.write(str(S))
        f.close()
        client_socket.send(str(pow(S, 2, N)).encode())
        print("Succes registration")
        return
    else:
        N = int(data)

    V = client_socket.recv(1024).decode()

    #Секрет клиента - S
    f = open(message + "_password", "r")
    _s = int(f.readlines()[0])

    t = 20
    for step in range(t):
        r = random.randint(2, N)

        x = pow(r, 2, N)
        client_socket.send(str(x).encode())

        e = int(client_socket.recv(1024).decode())

        y = pow(r * pow(_s, e, N), 1, N)
        client_socket.send(str(y).encode())

        data = client_socket.recv(1024).decode()
        if data == "Wrong user. Disconnect...":
            print("You are not " + message)
            client_socket.close()
            return
        if data == "Success. Welcome":
            print("Welcome " + message)
            client_socket.close()
            return


if __name__ == '__main__':
    client_program()