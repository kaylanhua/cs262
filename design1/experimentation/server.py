import socket

HOST = '127.0.0.1'
PORT = 6000

# ==================================

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        # to track who is logged in (dictionary w all usernames as key and connection as value)
        self.sessions = dict() 

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        # self.socket.setblocking(False)
        # self.socket.settimeout(0.2)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            try:
                connection, address = self.socket.accept()
                self.receive_message(connection)
                # self.new_user(connection, address)
            except OSError as e:
                pass 

    def receive_message(self, connection):
        data = connection.recv(128)
        data = data.decode('ascii') 
        print(f"The data is: {data}")
        self.socket.close()
        
        
    # def new_user(self, username, address):
    #     self.users.add(username)
    #     self.sessions.append(connection)


def main() -> None:

    serv = Server(HOST, PORT)
    serv.start()
    

if __name__ == "__main__":
    main()
    
