# main that sets up and loops
# You should use sockets and transfer buffers (of your definition) between the machines.
# TODO: set up a conda env

# send user id, requests need to be sent to user ids

import socket
HOST = '127.0.0.1'
PORT = 6000

users = set()

# ==================================

def main() -> None:

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    
    msg = 'Hello, World!' # TODO: get from terminal
    bmsg = msg.encode('ascii')
    sent = clientsocket.send(bmsg)
    print(f'Message sent, {sent}/{len(msg)} bytes transmitted')
    clientsocket.close()

    return

def send_msg(self, addr, line):
    line = line +'\n'
    
    for session in self.sessions:
        if addr == session.addr:
            session.push(line.encode())
            
            
    
if __name__ == "__main__":
    main()

