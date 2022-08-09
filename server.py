import socket
from datetime import datetime

HOST = '' # Listens all
PORT = 1773
CAPACITY = 1

class Server:
    def __init__(self, host=HOST, port=PORT, capacity=CAPACITY) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (host, port)
        self.__capacity = capacity

    def __log(self, msg):
        print("[SERVER] {} - {}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), msg))

    def start(self):
        self.__socket.bind(self.__address)
        self.__socket.listen(self.__capacity)
        self.__log("Started on {} port {}".format(
            self.__address[0], self.__address[1]))

    def run(self):
        while True:
            self.__log("Waiting for a connection")
            connection, client_addr = self.__socket.accept()
            try:
                self.__log("Connected from {}".format(client_addr))
                while True:
                    received_data = connection.recv(1024)
                    # Process data
                    if not received_data:
                        break
            finally:
                connection.close()
                self.__log("Disconnected")

if __name__ == "__main__":
    server = Server()
    server.start()
    server.run()