import unittest
from server import Server
from client import Client

HOST = '127.0.0.1'
PORT = 6001

class Test(unittest.TestCase):      

    def test_server_starts_correctly(self):
        serv = Server(HOST, PORT)
        serv.listen()
        serv.end()
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
