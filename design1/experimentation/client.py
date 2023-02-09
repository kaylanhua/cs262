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
        success = self.send_message('0', username)
        if not success:
            raise Exception('Account creation failed')
        
    def login(self):
        print('Please enter your username.')
        username = input()
        self.username = username
        success = self.send_message('1', username)
        if not success:
            raise Exception('Login failed')
    
    def send_message(self, opcode, username, message=None, target=None):
        msg = f'{opcode}%{username}%{target}%{message}'
        print(msg)
        bmsg = msg.encode('ascii')
        sent = self.conn.sendall(bmsg)
        print(f'Message sent, {len(msg)} bytes transmitted')

        # wait for response
        data = self.conn.recv(1024).decode('ascii') 
        status, err_msg = data.split('%')
        if status == '0':
            print('Success')
            return True
        else:
            print(f'Error {status}: {err_msg}')
            return False
    
    def query_message(self):
        print('Who would you like to send a message to?')
        target = input()
        print('What is your message?')
        msg = input()
        self.send_message(2, self.username, msg, target)
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
            # logout
            self.send_message('3', self.username)
            self.logout()
        elif op == "4":
            # delete account
            self.send_message('4', self.username)
            self.logout()
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

