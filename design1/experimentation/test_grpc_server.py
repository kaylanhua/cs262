import unittest

from grpc_server import Server
from grpc_client import Client
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

        server = Server()
        server_thread = threading.Thread(target = server.start, args = (SERVER_ADDR, port))
        server_thread.start()

        # Wait for server to start
        time.sleep(0.1)
        
        return server_thread, server, port
    
    def add_client(self, username, port):
        client = Client(CLIENT_ADDR, port)
        response = client.create_account(username)
        return client, response
    
    def cleanup(self, clients, server, server_thread):
        for client in clients:
            client.logout()
        # server.stop()
        server_thread.join()

    def assert_response_contains(self, data, string):
        self.assertIn(string, data.message)
    
    def assert_response_not_contains(self, data, string):
        self.assertNotIn(string, data.message)

    def test_server_accepts_one_client(self):
        with test_lock:
            print('TEST: test_server_accepts_one_client')
            server_thread, server, port = self.spawn_server()

            # One client connects
            client1, response1 = self.add_client(TEST_USERNAME_1, port)

            # Both clients receive welcome messages
            self.assert_response_contains(response1, "Welcome")
            self.assert_response_contains(response1, TEST_USERNAME_1)


    def test_server_accepts_two_clients(self):
        with test_lock:
            print('TEST: test_server_accepts_two_clients')
            server_thread, server, port = self.spawn_server()

            # Two clients connect
            client1, response1 = self.add_client(TEST_USERNAME_1, port)
            client2, response2 = self.add_client(TEST_USERNAME_2, port)

            # Both clients receive welcome messages
            self.assert_response_contains(response1, "Welcome")
            self.assert_response_contains(response1, TEST_USERNAME_1)

            self.assert_response_contains(response2, "Welcome")
            self.assert_response_contains(response2, TEST_USERNAME_2)

            # Both usernames are in a list of all users
            response = client1.list_all_users()
            self.assert_response_contains(response, TEST_USERNAME_1)
            self.assert_response_contains(response, TEST_USERNAME_2)

     
    def test_clients_can_message_eachother(self):
        with test_lock:
            print('TEST: test_clients_can_message_eachother')
            server_thread, server, port = self.spawn_server()

            # Two clients connect
            client1, response1 = self.add_client(TEST_USERNAME_1, port)
            client2, response2 = self.add_client(TEST_USERNAME_2, port)

            # Message is received by client2
            client1.send_message('2', client2.username, TEST_MESSAGE)
            
            # Get message from server
            response = client2.send_message('6')
            self.assert_response_contains(response, TEST_MESSAGE)


    def test_logout_handled_correctly(self):
        with test_lock:
            print('TEST: test_logout_handled_correctly')
            server_thread, server, port = self.spawn_server()

            # Two clients connect
            client1, response1 = self.add_client(TEST_USERNAME_1, port)
            client2, response2 = self.add_client(TEST_USERNAME_2, port)

            # Client 2 logs out successfully
            server.logout(client2.username)

            # Get list of users logged in from server
            response = client1.list_all_users()
            # response = client1.send_message('6')
            self.assert_response_contains(response, TEST_USERNAME_1)
            self.assert_response_not_contains(response, TEST_USERNAME_2)

            # Message is queued and delivered after logout/login
            client1.send_message('2', client2.username, TEST_MESSAGE + "_queued")

            client2, _ = self.add_client(TEST_USERNAME_2, port)

            # Get message from server
            response = client2.send_message('6')
            self.assert_response_contains(response, TEST_USERNAME_1)
            self.assert_response_contains(response, TEST_MESSAGE + "_queued")


if __name__ == '__main__':
    unittest.main()
