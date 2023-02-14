# Import socket module
import socket

MESSAGE_MAX_LENGTH_BYTES = 1000

def get_username():
    valid = False
    while valid is False:
        username = input()
        if (username == '') or (' ' in username):
            print(f'Username "{username}" is invalid, please try again.')
        else:
            valid = True
    return username

def get_message():
    valid = False
    while valid is False:
        message = input()
        if (message == ''):
            print(f'Message must not be empty, please try again.')
        if (len(message.encode('ascii')) > MESSAGE_MAX_LENGTH_BYTES):
            print(f'Message must not be longer than {MESSAGE_MAX_LENGTH_BYTES} bytes, please try again.')
        else:
            valid = True
    return message


def welcome_menu():
    print('Welcome! Type 0 to create an account, type 1 to log in.')

    valid = False
    while valid is False:
        response = input()
        if response == '0' or response == '1':
            # create account or login (same effect)
            print('Please enter your username.')
            return get_username()
        else:
            print('Invalid input. Please try again.')


class Client:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = ''
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

    # def create_account(self):
    #     print('Please choose a username.')
    #     username = input()
    #     self.username = username
    #     success = self.send_message('0', username)
    #     if not success:
    #         raise Exception('Account creation failed')
        
    def login(self, username):
        self.username = username
        # TODO: try again on failure
        self.send_message('1', username)
    

    def send_message(self, opcode, username, message=None, target=None):
        msg = f'{opcode}%{username}%{target}%{message}'
        print(msg)
        bmsg = msg.encode('ascii')
        self.conn.sendall(bmsg)
        print(f'Message sent, {len(msg)} bytes transmitted')

        # wait for response (indicates success or not)
        data = self.conn.recv(1024).decode('ascii')
        print(data)
        status, text = data.split('%')
        
        # first can be status or sender
        # msg can be error message or text message
        if status == '0':
            print('Success')
        else:
            print(f'Error {text}')
    

    def query_message(self):
        print('Please enter username of recipient.')
        target = get_username()
        print('Please enter your message.')
        message = get_message()
        success = self.send_message(2, self.username, message, target)


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
        
            
    def logout(self):
        self.conn.close()
        print('You have been logged out. Exiting...')
        exit()

def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 6010

    client = Client(host, port)

    # get client username
    username = welcome_menu()

    # login / create account
    client.login(username)

    while True:

        client.main_message()

        # # message received from server
        # data = client.conn.recv(1024)

        # # print the received message
        # # here it would be a reverse of sent message
        # print('Received from the server :',str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    # close the connection
    client.conn.close()

if __name__ == '__main__':
    print("Client Started")
    Main()
