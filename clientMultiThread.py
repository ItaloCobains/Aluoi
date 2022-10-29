import socket
import sys
import os

from dotenv import load_dotenv, find_dotenv


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

def main() -> None:
    load_dotenv(find_dotenv())
    data = " ".join(sys.argv[1:])
    HOST = str(os.getenv('HOST'))
    PORT = int(os.getenv('PORT'))
    client(HOST, PORT, data)

if __name__ == "__main__":
    main()
       
