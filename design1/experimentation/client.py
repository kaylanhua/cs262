# main that sets up and loops
# You should use sockets and transfer buffers (of your definition) between the machines.
# TODO: set up a conda env

# send user id, requests need to be sent to user ids

import socket
HOST = '127.0.0.1'
PORT = 6000

# op codes
# 0: create account
# 1: login
# 2: send message
# 3: logout
# 4: delete account

# ==================================

class Client:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = ''
        
    def create_account(self):
        print('Please choose a username.')
        username = input()
        self.username = username
        self.send_message('0', username)
        pass
        
    def login(self):
        print('Please enter your username.')
        username = input()
        self.username = username
        self.send_message('1', username)
        pass
    
    def send_message(self, opcode, message, target=None):
        if target:
            msg = f'{opcode}{target}%{message}'
        else:
            msg = f'{opcode}{message}'
        bmsg = msg.encode('ascii')
        sent = self.conn.send(bmsg)
        print(f'Message sent, {sent}/{len(msg)} bytes transmitted')
        pass
    
    def query_message(self):
        print('Who would you like to send a message to?')
        target = input()
        print('What is your message?')
        msg = input()
        self.send_message(2, msg, target)
        pass
    
    def welcome_message(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        
        print('Welcome! Type 0 to create an account, type 1 to log in.')
        response = input()
        if response == '0':
            self.create_account()
        elif response == '1':
            self.login()
        else:
            print('Invalid input. Please try again.')
            self.welcome_message()
            return
        
    def main_message(self):
        print('What do you want? 2 for send message, 3 for log out, 4 for delete account :(')
        op = input()
        if op == "2":
            self.query_message()
        elif op == "3":
            self.send_message('3', self.username)
            self.logout()
        elif op == "4":
            self.send_message('4', self.username)
        else: 
            print('Invalid input. Please try again.')
            self.main_message()
            return
        
    def run_client(self):
        self.welcome_message()
        while True:
            self.main_message()
            
    def logout(self):
        self.conn.close()
        print('You have been logged out. Exiting...')
        exit()

def main() -> None:
    
    client = Client(HOST, PORT)
    client.run_client()
    

    return

# def send_msg(self, addr, line):
#     line = line +'\n'
    
#     for session in self.sessions:
#         if addr == session.addr:
#             session.push(line.encode())
            
            
    
if __name__ == "__main__":
    main()

