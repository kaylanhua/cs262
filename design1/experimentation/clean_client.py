# Import socket module
import socket
from _thread import start_new_thread
import time
import select
import os

# colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# max length of message body in bytes
MESSAGE_MAX_LENGTH_BYTES = 800

# local host IP '127.0.0.1'
host = 'localhost'
# host = '10.250.94.109'        # or replace w/ external machine's ip address

# Define the port on which you want to connect
port = 6027

# disallowed characters (used in packet encoding)
disallowed_chars = ['%', '|', ' ']

logged_in = False

def get_username():
    '''Get username from user, ensuring it is valid.'''
    valid = False
    while valid is False:
        username = input()
        for char in disallowed_chars:
            if char in username:
                print(f'Username "{username}" is invalid (must not contain "{char}"), please try again.')
                break
        if (len(username) > 20):
            print(f'Username must not be longer than 20 characters, please try again.')
        else:
            valid = True
    return username

def get_message():
    '''Get message from user, ensuring it is valid.'''
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
    '''Thread function for receiving messages from server.'''
    while True:
        # data received from client
        try:
            ready = select.select([conn], [], [], 1)
            if ready[0]:
                data = conn.recv(1024)

                print('Data (raw):', data, ' len:', len(data))

                data = data.decode('ascii')
                print('Data (decoded):', data, ' len:', len(data))

                if not data:
                    print('Bye')
                    break
                elif "SERVER%Someone else" in data:
                    print('Someone else is logged in with that username. Please try again.')
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                    os._exit(1)
                elif "SERVER%Account does not exist" in data:
                    print('Account does not exist. Please try again.')
                    print('____')
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                    os._exit(1)
                    # TODO: thread doesn't actually exit (same above)

                # split incoming message into distict packets (delimited by '|')
                packets = data.split('|')
                for packet in packets:
                    if packet == '':
                        continue
                    sender, message = packet.split('%')
                    print(f"{bcolors.OKBLUE}[{sender}] {message}{bcolors.ENDC}")
        except Exception as e:
            # Error occurs when parent thread closes connection:
            #   not a problem as we are logging out anyway, so ignore
            break


def welcome_menu(client):
    '''Welcome menu for new users.'''
    print(bcolors.OKBLUE + '''
 __     __     ______     __         ______     ______     __    __     ______    
/\ \  _ \ \   /\  ___\   /\ \       /\  ___\   /\  __ \   /\ "-./  \   /\  ___\   
\ \ \/ ".\ \  \ \  __\   \ \ \____  \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  __\   
 \ \__/".~\_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ 
  \/_/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ 
                                                                                  
''' + bcolors.ENDC )
    print('Welcome! Type 0 to create an account, type 1 to log in.')

    valid = False
    while valid is False:
        response = input().replace(" ", "")
        if response == '0' :
            # create account or login (same effect)
            print('Please enter your username.')
            client.create_account(get_username())
            valid = True

        elif response == '1':
            print('Please enter your username.')
            client.login(get_username())
            valid = True

        else:
            print('Invalid input. Please try again.')


class Client:

    def __init__(self, host, port):
        '''Initialize client.'''
        self.host = host
        self.port = port
        self.username = ''
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

    def create_account(self, username):
        '''Create new account.'''
        self.username = username
        self.send_message('0', username)

    def login(self, username):
        '''Log in to existing account by sending message to server with opcode 1.'''
        self.username = username
        # TODO: handle failure
        self.send_message('1', username)

    def send_message(self, opcode, username, message=None, target=None):
        '''Send message to server with opcode, username, message, and target.'''
        msg = f'{opcode}%{username}%{target}%{message}'
        bmsg = msg.encode('ascii')
        self.conn.sendall(bmsg)
        print(f'Message sent, {len(msg)} bytes transmitted')

    def query_message(self):
        '''Obtain message details from user and send to server.'''
        print('Please enter username of recipient.')
        target = get_username()
        print('Please enter your message.')
        message = get_message()
        self.send_message(2, self.username, message, target)

    def logout(self):
        '''Log out of account by closing connection to server.'''
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        print('You are logged out. Exiting ...')

    def list_all_users(self):
        '''
        Request a list of all users from the server.
        Server will respond with a list of all users, which will be printed to the console.
        '''
        self.send_message('5', self.username)

def Main():
    '''Main messaging loop.'''

    # create new client instance
    client = Client(host, port)

    # start thread for receiving messages in background
    start_new_thread(threaded_receive, (client.conn,))

    # log in / create account
    welcome_menu(client)

    while True:
        # sleep for a moment to improve user experience
        time.sleep(0.5)

        # show menu to user
        print('Select an option: 2 for send message, 3 for log out, 4 for delete account, 5 for list all users.')

        # strip whitespace from input
        op = input().replace(" ", "")

        # take action based on user input
        if op == "2":
            # send message
            client.query_message()
        elif op == "3":
            # logout
            client.send_message('3', client.username)
            client.logout()
            exit()
        elif op == "4":
            # delete account
            client.send_message('4', client.username)
            client.logout()
            exit()
        elif op == "5":
            # list all users
            client.list_all_users()
        else:
            print('Invalid input. Please try again.')


if __name__ == '__main__':
    print("Client Started")
    Main()
