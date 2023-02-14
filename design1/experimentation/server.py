import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 6009

# TODO: set a limit on message size

# ==================================

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sessions = dict()  # who is logged in (usernames: connection | None)
        self.messages = dict()  # queue for messages

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
            except ConnectionAbortedError as e:
                return
            except OSError as e:
                print('Error:', e)
                pass 
        
        # self.socket.close()

    def create_account(self, username, connection):
        print(f"{username} has created an account")
        self.login(username, connection)
   
    def login(self, username, connection):
        self.sessions[username] = connection
        print(f"{username} has logged in")

    def receive_message(self, connection):
        data = connection.recv(4096)
        print('Data (raw):', data, ' len:', len(data))
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
            if self.messages.has_key(username):
                for message in self.messages[username]:
                    self.send_message(1, username, message)
        elif opcode == '2':
            if target not in self.sessions.keys():
                status = 1
                err_msg = (f"User {target} does not exist")
            else: 
                toSend = username+'%'+message
                if self.sessions == None:
                    # user not logged in
                    if not self.messages.has_key(target):
                        self.messages[target] = []
                    self.messages[target].append(toSend)
                else:
                    # send message to target
                    self.send_message(1, target, toSend)
        else:
            if opcode == '3': # log out
                response = f"{status}%{err_msg}"
                self.send_message(0, username, response)
                self.logout(username)
                return False
            elif opcode == '4': # delete account
                self.sessions.pop(username)
                self.messages.pop(username)
                self.logout(username)
            elif opcode == '5': # list all users
                message = str(self.sessions.keys())
                self.send_message(0, username, message)
            
            response = f"{status}%{err_msg}"
            self.send_message(0, username, response)
            return False

        # Return status code (and error message if applicable)
        response = f"{status}%{err_msg}"
        self.send_message(0, username, response)

        return True
    
    def send_message(self, isError, target, message):
        message = str(isError) + '%' + message
        connection = self.sessions[target]
        print(f'Received the following message for {target}: {message}')
        msg = message.encode('ascii')
        connection.sendall(msg)
        pass
    
    def logout(self, username):
        self.sessions[username] = None
        self.socket.close()
        print(f"{username} has logged out")
    
        
        


def main() -> None:

    serv = Server(HOST, PORT)
    serv.listen()
    

if __name__ == "__main__":
    main()
    
