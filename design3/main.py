
import argparse
from grpc_server import Server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id')
    parser.add_argument('--is_primary', action='store_true')
    args = parser.parse_args()

    machine = Server(args.id, args.is_primary)

