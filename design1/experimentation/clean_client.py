# Import socket module
import socket
from _thread import start_new_thread

MESSAGE_MAX_LENGTH_BYTES = 1000
# local host IP '127.0.0.1'
host = '127.0.0.1'

# Define the port on which you want to connect
port = 6022

def get_username():
    valid = False
    while valid is False:
        username = input()
        if (username == '') or (' ' in username) or ('%' in username):
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
        elif (len(message.encode('ascii')) > MESSAGE_MAX_LENGTH_BYTES):
            print(f'Message must not be longer than {MESSAGE_MAX_LENGTH_BYTES} bytes, please try again.')
        elif '%' in message:
            print('Message must not contain the character "%", please try again.')
        else:
            valid = True
    return message



# thread function
def threaded_receive(conn):
    while True:
        # data received from client
        data = conn.recv(1024)
        print('Data (raw):', data, ' len:', len(data))
        
        if not data:
            print('Bye')
            # lock released on exit
            # print_lock.release()
            break
        
        data = data.decode('ascii')
        sender, message = data.split('%') 
        print(f"[{sender}] {message}")


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

        
    def login(self, username):
        self.username = username
        # TODO: try again on failure
        self.send_message('1', username)


    def send_message(self, opcode, username, message=None, target=None):
        msg = f'{opcode}%{username}%{target}%{message}'
        print(msg)
        bmsg = msg.encode('ascii')
        # TODO: catch exception if sending fails (and retry?)
        self.conn.sendall(bmsg)
        print(f'Message sent, {len(msg)} bytes transmitted')

        # wait for response (indicates success or not)
        # data = self.conn.recv(1024).decode('ascii')
        # print(data)
        # status, text = data.split('%')
        
        # # first can be status or sender
        # # msg can be error message or text message
        # if status == '0':
        #     print('Success')
        # else:
        #     print(f'Error {text}')
    

    def query_message(self):
        print('Please enter username of recipient.')
        target = get_username()
        print('Please enter your message.')
        message = get_message()
        self.send_message(2, self.username, message, target)

     
    def logout(self):
        self.conn.close()
        print('You have been logged out. Exiting...')
        exit()

def Main():


    client = Client(host, port)

    # get client username
    username = welcome_menu()

    # login / create account
    client.login(username)

    start_new_thread(threaded_receive, (client.conn,))

    while True:
        
        # MENU
        print('Select an option: 2 for send message, 3 for log out, 4 for delete account, 5 for list all users.')
        op = input()
        if op == "2":
            client.query_message()    
        elif op == "3":
            # logout
            client.send_message('3', client.username)
            client.logout()
        elif op == "4":
            # delete account
            client.send_message('4', client.username)
            client.logout()
        elif op == "5":
            # list all users
            client.send_message('5', client.username)
        else: 
            print('Invalid input. Please try again.')


if __name__ == '__main__':
    print("Client Started")
    Main()
