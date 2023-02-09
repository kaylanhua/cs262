# main that sets up and loops
# You should use sockets and transfer buffers (of your definition) between the machines.
# TODO: set up a conda env

# send user id, requests need to be sent to user ids

import socket
HOST = '127.0.0.1'
PORT = 6000

# ==================================

class Client:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = 0
        
        
    def create_account(self):
        print('Please choose a username.')
        username = input()
        self.send_message('0', username)
        pass
        
    def log_in(self):
        print('Please enter your username.')
        username = input()
        self.send_message('1', username)
        pass
    
    def send_message(self, opcode, message):
        msg = f'{opcode}{message}'
        bmsg = msg.encode('ascii')
        sent = self.conn.send(bmsg)
        print(f'Message sent, {sent}/{len(msg)} bytes transmitted')
        pass
    
    def start_message(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        
        print('Welcome! Type 0 to create an account, type 1 to log in.')
        response = input()
        if response == '0':
            self.create_account()
        elif response == '1':
            self.log_in()
        else:
            print('Invalid input. Please try again.')
            self.start_message()
            
    def end(self):
        self.conn.close()

def main() -> None:
    
    client = Client(HOST, PORT)
    client.start_message()

    return

# def send_msg(self, addr, line):
#     line = line +'\n'
    
#     for session in self.sessions:
#         if addr == session.addr:
#             session.push(line.encode())
            
            
    
if __name__ == "__main__":
    main()

