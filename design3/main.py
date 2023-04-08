import logging
import argparse
from grpc_server import Server, HOST
from grpc_client import PORTS

if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--id')
    parser.add_argument('--is_primary', action='store_true')
    args = parser.parse_args()

    if args.is_primary:
        print('Starting primary server')
        machine = Server(args.id, args.is_primary)
    else:
        machine = Server(args.id, is_primary=False)
    machine.start(HOST, PORTS[args.id])