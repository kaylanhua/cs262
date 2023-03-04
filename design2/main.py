import argparse
from model_machine import ModelMachine

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name')
    parser.add_argument('--port')
    parser.add_argument('--ticks_ps')

    machine = ModelMachine(parser.name, parser.port, parser.ticks_ps)

