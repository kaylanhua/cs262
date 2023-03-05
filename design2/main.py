import argparse
from model_machine import ModelMachine

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id')
    parser.add_argument('--ticks_ps')
    args = parser.parse_args()

    machine = ModelMachine(args.id, args.ticks_ps)

