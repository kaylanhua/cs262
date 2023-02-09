import socket
import time

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
        print(f"Server started on {self.host}:{self.port}")
        
        connection, address = self.socket.accept()

        cont = self.receive_message(connection)
        while cont:
            try:
                cont = self.receive_message(connection)
                time.sleep(0.5)

            except OSError as e:
                pass 

    def create_account(self, username, connection):
        print(f"{username} has created an account")
        self.login(username, connection)
   
    def login(self, username, connection):
        self.sessions[username] = connection
        print(f"{username} has logged in")

    def receive_message(self, connection):
        data = connection.recv(4096)
        print('Data (raw):', data)
        data = data.decode('ascii') 
        if len(data) == 0:
            return False
        print(f"The data is: {data}")
        
        opcode = data[:1]
        meat = data[1:]
        if opcode == '0':
            if meat in self.sessions:
                # user alr exists, log in
                self.login(meat, connection)
            else:
                # user does not exist yet, create new user and log in
                self.create_account(meat, connection)
        elif opcode == '1':
            self.login(meat, connection)
        elif opcode == '2':
            target, message = meat.split('%')
            self.new_message(target, message, connection)
        elif opcode == '3': # log out
            self.logout(meat)
            return False
        elif opcode == '4': # delete account
            self.sessions.pop(meat)
            self.logout(meat)
            return False
        
        return True
    
    def new_message(self, target, message, connection):
        print(f'Received the following message for {target}: {message}')
    
    def logout(self, username):
        self.sessions[username] = None
        self.socket.close()
        print(f"{username} has logged out")
    
    def end(self):
        self.socket.close()
        
        


def main() -> None:

    serv = Server(HOST, PORT)
    serv.start()
    

if __name__ == "__main__":
    main()
    
