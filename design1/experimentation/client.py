# send user id, requests need to be sent to user ids

import socket
HOST = '127.0.0.1'
PORT = 6009

# op codes
# 0: create account
# 1: login
# 2: send message
# 3: logout
# 4: delete account

# TODO: take care of empty messages

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

        # wait for response (indicates success or not)
        # return self.receive_message()
    
    # def receive_message(self):
    #     data = self.conn.recv(1024).decode('ascii')
    #     print(data)
    #     isError, first, msg = data.split('%')
        
    #     # first can be status or sender
    #     # msg can be error message or text message
    #     if isError == '0':
    #         if first == '0':
    #             print('Success')
    #             return True
    #         else:
    #             print(f'Error {first}: {msg}')
    #             return False
    #     elif isError == '1':
    #         print(f'[From {first}] {msg}')
    #     pass
    
    def query_message(self):
        valid = False
        while valid is False:
            print('Who would you like to send a message to?')
            target = input()
            if (target == '') or (' ' in target):
                print(f'Username "{target}" is invalid, please try again.')
            else:
                valid = True
        
        valid = False
        while valid is False:
            print('What is your message?')
            msg = input()
            if msg == '':
                print('Message must not be empty')
            else:
                valid = True

        success = self.send_message(2, self.username, msg, target)
        
    
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

