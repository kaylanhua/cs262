"""The Python implementation of the GRPC messages.Server server."""

from concurrent import futures
import logging

import grpc
import messages_pb2
import messages_pb2_grpc

from threading import Lock 

host = 'localhost'  # replace with 0.0.0.0 to open up to other machines
port = '50051'
sessions = dict()   # manages which users are currently logged in, as in the socket server
messages = dict()   # manages which users have outstanding messages which are yet to be delivered

server_lock = Lock()    # lock for server mutx

# following four functions taken from clean_server.py
def create_account(username, connection):
    sessions[username] = connection
    print(f"{username} has created an account")
        
def login(username, connection):
    sessions[username] = connection
    print(f"{username} has logged in")
    
def logout(username):
    sessions[username] = None
    print(f"{username} has logged out")

def queue_message(sender, recipient, message):
    if recipient not in messages:
        messages[recipient] = []
    messages[recipient].append((sender, message))


class Server(messages_pb2_grpc.ServerServicer):

    def send_pending(self, messages, username, justLoggedIn=False):
        '''
        sends outstanding messages to the client who has just queried the server
        applies for a backlog of messages (seen upon log in) and real time messages (seen while logged in)
        '''
        toClient = None
        if username in messages and messages[username] is not None:
            if justLoggedIn:
                info_msg = f"You have {len(messages[username])} new messages since you last logged in:\n"
            else:
                info_msg = f"\nNew message!\n"
            toClient = info_msg

            for sender, message in messages[username]:
                toClient += f"[{sender}] {message}\n"
            messages.pop(username)
        return toClient
    
    def ReceiveMessageFromClient(self, request, context):
        '''receive and parse a message from the client'''

        with server_lock:
            # parse request structure
            opcode = request.opcode
            username = request.username
            target = request.target      # optional
            message = request.message    # optional
            toClient = ''                # final message to be sent to the client who queried the server
            
            # CREATE ACCOUNT
            if opcode == '0':
                if username in sessions:
                    # user already exists, log in
                    login(username, True)
                    toClient = f"User already exists. Welcome back, {username}.\n"
                    if sessions[username] is not None:
                        # someone else is logged into the requested account
                        toClient = "Someone else has logged into this account so you're being logged out. Goodbye!"
                        logout(username)
                else:
                    # user does not exist yet, create new user and log in
                    create_account(username, True)
                    toClient = f"Welcome to your new account, {username}."

            # LOG IN
            elif opcode == '1': # log in
                if username not in sessions:
                    # user does not exist, give error
                    toClient = "Account does not exist. Please create an account first."
                    logout(username)
                    return messages_pb2.ServerLog(message=toClient)

                if sessions[username] is not None:
                    # someone else is logged into the requested account
                    toClient = "Someone else has logged into this account so you're being logged out. Goodbye!"
                    logout(username)
                    return messages_pb2.ServerLog(message=toClient)
                
                login(username, True)
                toClient = f"Welcome back, {username}.\n"
                # Send undelivered messages, if any
                pending = self.send_pending(messages, username, True)
                if pending:
                    toClient += pending

            # SEND MESSAGE    
            elif opcode == '2':
                if target not in sessions.keys():
                    # TODO: raise exception instead?
                    toClient = f"Error: User {target} does not exist. Message could not be sent"
                else: 
                    if sessions[target] == None: 
                        # target is not logged in, queue message
                        queue_message(username, target, message)
                    else:
                        # send message to target
                        print(f"someone is trying to send a message to {target}")
                        queue_message(username, target, message)
            
            # LOG OUT            
            elif opcode == '3': 
                toClient = "You have logged out. Goodbye!"
                logout(username)

            # DELETE ACCOUNT    
            elif opcode == '4':
                toClient = "Your account has been deleted. Goodbye!"
                sessions.pop(username)
                if username in messages:
                    messages.pop(username)
            
            # LIST ALL USERS    
            elif opcode == '5':
                toClient = "[ALL ACCOUNTS]" + str(list(sessions.keys()))
            
            # QUERYING FOR MESSAGES
            # this is never explicitly chosen by users, this code is used by the client to automatically listen for incoming messages
            elif opcode == '6':
                res = self.send_pending(messages, username)
                if res:
                    toClient = res

            return messages_pb2.ServerLog(message=toClient)
    

def serve():
    # basic gRPC server set up using info from the auto generated messages_pb2_grpc
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port(host + ':' + port) 
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()