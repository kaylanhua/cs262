import argparse
from model_machine import ModelMachine

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id')
    parser.add_argument('--ticks_ps')
    parser.add_argument('--out_dir')
    parser.add_argument('--p_internal')
    args = parser.parse_args()

    machine = ModelMachine(args.id, args.ticks_ps, args.out_dir, args.p_internal)

