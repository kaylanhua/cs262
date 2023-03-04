import unittest
from server import Server
from client import Client
import threading

HOST = '127.0.0.1'
PORT = 6001

class Test(unittest.TestCase):      

    def start_server():
        serv = Server(HOST, PORT)
        serv.listen()

    def test_server_accepts_connection(self):
        threading.Thread(target = self.start,args = (client, address)).start()

        serv = Server(HOST, PORT)
        serv.listen()
        serv.end()
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
