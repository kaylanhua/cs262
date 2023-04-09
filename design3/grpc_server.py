from concurrent import futures


import grpc
import messages_pb2
import messages_pb2_grpc

from threading import Lock

from socket_client import bcolors
from socket_server import printg
from grpc_client import PORTS

import csv
from os import path

# GLOBALS --------------------------------

HOST = 'localhost'  # replace with 0.0.0.0 to open up to other machines
server_lock = Lock()    # lock for server mutex

# FUNCTIONS --------------------------------

class Server(messages_pb2_grpc.ServerServicer):

    def __init__(self, id):
        # Check that user is valid (i.e. named A, B, or C)
        assert id in PORTS.keys(), 'Invalid machine id. Please use A, B, or C.'
        
        self.id = id
        print(f'initializing replica {self.id}')
        self.sessions = dict()              # manages which users are currently logged in, as in the socket server
        self.messages = dict()              # manages which users have outstanding messages which are yet to be delivered
        self.filename = f'{id}_db.csv'
        
        csv.writer(open(self.filename, 'w'))
        assert path.exists(self.filename)
        
    def log_messages(self):
        '''log to csv and overwrite anything existing'''
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['recipient', 'sender', 'message'])
            for name in self.messages.keys():
                for sender, message in self.messages[name]:
                    writer.writerow([name, sender, message])

    # following four functions taken from clean_server.py
    def create_account(self, username, connection):
        self.sessions[username] = connection
        printg(f"> {username} has created an account.")

    def login(self, username, connection):
        self.sessions[username] = connection
        printg(f"> {username} has logged in.")

    def logout(self, username):
        self.sessions[username] = None
        printg(f"> {username} has logged out.")

    def queue_message(self, sender, recipient, message):
        if recipient not in self.messages:
            self.messages[recipient] = []
        self.messages[recipient].append((sender, message))

    def start(self, host, port):
        # basic gRPC server set up using info from the auto generated messages_pb2_grpc
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        messages_pb2_grpc.add_ServerServicer_to_server(self, server)
        server.add_insecure_port(host + ':' + str(port))
        server.start()
        print("Server started, listening on " + str(port))
        server.wait_for_termination()

    def send_pending(self, messages, username, justLoggedIn=False):
        '''
        sends outstanding messages to the client who has just queried the server
        applies for a backlog of messages (seen upon log in) and real time messages (seen while logged in)
        '''
        toClient = None
        if username in messages and messages[username] is not None:
            # determines whether the message to be sent is a live or queried message
            if justLoggedIn:
                info_msg = f"You have {len(messages[username])} new messages since you last logged in:\n"
            else:
                info_msg = ""
            toClient = info_msg

            # combine all backlogged messages into one larger message to send to client
            for sender, message in messages[username]:
                toClient += f"[{sender}] {message}\n"
            messages.pop(username)
        return toClient

    def ReceiveMessageFromClient(self, request, context):
        '''receive and parse a message from the client'''

        with server_lock:
            # immediately add to pending log
            self.pending_log.append(request)
        
            # parse request structure
            opcode = request.opcode
            username = request.username
            target = request.target      # optional
            message = request.message    # optional
            toClient = ''                # final message to be sent to the client who queried the server

            # CREATE ACCOUNT
            if opcode == '0':
                if username in self.sessions:
                    # user already exists, log in
                    if self.sessions[username] is not None:
                        # someone else is logged into the requested account
                        toClient = "SERVER%KillSomeone else is already logged into this account. Goodbye!"
                else:
                    # user does not exist yet, create new user and log in
                    self.create_account(username, True)
                    toClient = f"Welcome to your new account, {username}."

            # LOG IN
            elif opcode == '1': # log in
                if username not in self.sessions:
                    # user does not exist, give error
                    toClient = "SERVER%KillAccount does not exist. Please create an account first."
                    self.logout(username)
                    return messages_pb2.ServerLog(message=toClient)

                if self.sessions[username] is not None:
                    # someone else is logged into the requested account
                    toClient = "SERVER%KillSomeone else is already logged into this account. Goodbye!"
                    return messages_pb2.ServerLog(message=toClient)

                self.login(username, True)
                toClient = f"Welcome back, {username}.\n"
                
                # Send undelivered messages, if any
                pending = self.send_pending(self.messages, username, True)
                if pending:
                    toClient += pending

            # SEND MESSAGE
            elif opcode == '2':
                if target not in self.sessions.keys():
                    # TODO: raise exception instead?
                    toClient = f"Error: User {target} does not exist. Message could not be sent"
                else:
                    if self.sessions[target] == None:
                        # target is not logged in, queue message
                        self.queue_message(username, target, message)
                    else:
                        # send message to target
                        printg(f"> {username} is trying to send a message to {target}.")
                        self.queue_message(username, target, message)

            # LOG OUT
            elif opcode == '3':
                toClient = "You have logged out. Goodbye!"
                self.logout(username)

            # DELETE ACCOUNT
            elif opcode == '4':
                toClient = "Your account has been deleted. Goodbye!"
                self.sessions.pop(username)
                if username in self.messages:
                    self.messages.pop(username)

            # LIST ALL USERS
            elif opcode == '5':
                toClient = "[ALL ACCOUNTS]" + str([key for key in self.sessions.keys() if self.sessions[key] is not None])

            # QUERYING FOR MESSAGES
            # this is never explicitly chosen by users, this code is used by the client to automatically listen for incoming messages
            elif opcode == '6':
                res = self.send_pending(self.messages, username)
                if res:
                    toClient = res

            return messages_pb2.ServerLog(message=toClient)
        