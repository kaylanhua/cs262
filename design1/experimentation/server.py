import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 6000

# ==================================

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        # to track who is logged in (dictionary w all usernames as key and connection as value)
        self.sessions = dict() 
        # TODO: queue for messages

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client, address = self.socket.accept()
            # client.settimeout(60)
            threading.Thread(target = self.start,args = (client, address)).start()
    
    def start(self, connection, address):
        print(f"New connection from {address}")
        cont = True
        while cont:
            try:
                cont = self.receive_message(connection)
                time.sleep(0.5)
            except OSError as e:
                print('Error:', e)
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
            return True
        print(f"The data is: {data}")
        
        opcode, username, target, message = data.split('%')
        print(opcode, username, target, message)

        status = 0
        err_msg = ''
        
        if opcode == '0':
            if username in self.sessions:
                # user alr exists, log in
                self.login(username, connection)
            else:
                # user does not exist yet, create new user and log in
                self.create_account(username, connection)
        elif opcode == '1':
            self.login(username, connection)
        elif opcode == '2':
            if target not in self.sessions.keys():
                status = 1
                err_msg = (f"User {target} does not exist")
                # TODO: consider if not logged in
            else: 
                # send message to target
                self.send_message(target, message)
        elif opcode == '3': # log out
            self.logout(username)
            return False
        elif opcode == '4': # delete account
            self.sessions.pop(username)
            self.logout(username)
            return False
        elif opcode == '5': # list all users
            message = str(self.sessions.keys())
            self.send_message(username, message)
            return False

        # Return status code (and error message if applicable)
        response = f"{status}%{err_msg}"
        self.send_message(username, response)

        return True
    
    def send_message(self, target, message):
        connection = self.sessions[target]
        print(f'Received the following message for {target}: {message}')
        msg = message.encode('ascii')
        connection.sendall(msg)
        pass
    
    def logout(self, username):
        self.sessions[username] = None
        self.socket.close()
        print(f"{username} has logged out")
    
    def end(self):
        self.socket.close()
        
        


def main() -> None:

    serv = Server(HOST, PORT)
    serv.listen()
    

if __name__ == "__main__":
    main()
    
