# def connections():
#     print('Got connection from', addr)
#     while True:
#         c, addr = s.accept()     # Establish connection with client.
#         thread.start_new_thread(on_new_client,(c,addr))
        

# def receive_message():
    # receives from the client
    # within each thread function it's just a while loop that listens to a client message
    
    
# def broadcast(self, line):
#     for session in self.sessions:
#         line = line + '\n'
#         session.push(line.encode())   



    # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serversocket.bind((HOST, PORT))
    # serversocket.listen()
    # clientsocket, addr = serversocket.accept()
    # print('Connected to by:', addr)
    
    # data = clientsocket.recv(128)
    # data = data.decode('ascii')

    # print(f"The data is: {data}")

    # serversocket.close()