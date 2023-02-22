import unittest

from socket_server import Server, logout
from socket_client import Client
import threading
import time

SERVER_ADDR = '127.0.0.1'
CLIENT_ADDR = '127.0.0.1'

TEST_USERNAME_1 = 'testuser1'
TEST_USERNAME_2 = 'testuser2'
TEST_MESSAGE = '<<testmessage>>'

DATA_SIZE = 1024

next_port = 6302
test_lock = threading.Lock()


class Test(unittest.TestCase):   

    def spawn_server(self):
        global next_port
        port = next_port
        next_port += 1

        server = Server(testing = True)
        server_thread = threading.Thread(target = server.start, args = (SERVER_ADDR, port))
        server_thread.start()
        return server_thread, server, port
    
    def add_client(self, username, port, login=False):
        client = Client(CLIENT_ADDR, port)
        if login:
            client.login(username)
        else:
            client.create_account(username)
        return client
    
    def cleanup(self, clients, server, server_thread):
        for client in clients:
            client.logout()
        server.stop()
        server_thread.join()

    def assert_response_contains(self, data, string):
        self.assertIn(string, data.decode('ascii'))
    
    def assert_response_not_contains(self, data, string):
        self.assertNotIn(string, data.decode('ascii'))

    #         # self.cleanup([client1, client2], server, server_thread)
    #         print('_______ CLEANUP ______________')


    def test_server_accepts_two_clients(self):
        server_thread, server, port = self.spawn_server()

        # Two clients connect
        client1 = self.add_client(TEST_USERNAME_1, port)
        client2 = self.add_client(TEST_USERNAME_2, port)

        # Both clients receive welcome messages
        data = client1.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, "Welcome")
        self.assert_response_contains(data, TEST_USERNAME_1)

        data = client2.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, "Welcome")
        self.assert_response_contains(data, TEST_USERNAME_2)

        # Both usernames are in a list of all users
        client1.list_all_users()
        data = client1.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, TEST_USERNAME_1)
        self.assert_response_contains(data, TEST_USERNAME_2)

        # Message is received by client2
        client1.send_message(2, client1.username, TEST_MESSAGE, client2.username)
        data = client2.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, TEST_MESSAGE)

        # Client 2 logs out successfully
        client2.logout()
        logout(client2.username)
        client1.list_all_users()
        data = client1.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, TEST_USERNAME_1)
        self.assert_response_not_contains(data, TEST_USERNAME_2)

        # Message is queued and delivered after logout/login
        client1.send_message(2, client1.username, TEST_MESSAGE + "_queued", client2.username)

        client2 = self.add_client(TEST_USERNAME_2, port, login=True)

        data = client2.conn.recv(DATA_SIZE)
        self.assert_response_contains(data, TEST_MESSAGE + "_queued")

        self.cleanup([client1, client2], server, server_thread)

if __name__ == '__main__':
    unittest.main()
