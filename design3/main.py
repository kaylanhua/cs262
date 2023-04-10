import logging
import argparse
from grpc_server import Server, HOST
from grpc_client import PORTS

if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--id')
    args = parser.parse_args()

    machine = Server(args.id)
    machine.start(HOST, PORTS[args.id])