# ----- HEADERS -----

from collections import deque
import time
import csv
from logical_clock import LogicalClock
from random import randint
import socket
import random
from _thread import start_new_thread
from os import path

# ----- VARIABLES -----

HOST = 'localhost'
BASE_PORT = 6740
PORTS = {'A': BASE_PORT, 'B': BASE_PORT + 1, 'C': BASE_PORT + 2}

DURATION = 60

# ----- FUNCTIONS -----

def global_time_ms():
    '''Returns the current time in milliseconds.'''
    return int(round(time.time() * 1000))

class ModelMachine:

    def __init__(self, id, ticks_ps, out_dir, p_internal):
        # Check that user is valid (i.e. named A, B, or C)
        assert id in PORTS.keys(), 'Invalid machine id. Please use A, B, or C.'

        # internal variables
        self.id = id
        self.ticks_ps = float(ticks_ps)
        self.out_dir = out_dir
        self.p_internal = float(p_internal)
        self.queue = deque()
        self.connections = dict()
        self.filename = f'{self.out_dir}/machine_{id}_log.csv'
        self.logical_clock = LogicalClock()
        self.last_tick_time = global_time_ms()

        # IDs of other machines
        other_ids = [id for id in PORTS.keys() if id != self.id]

        # Start server (spawns separate threads for each incoming connection)
        start_new_thread(self.start_server, (PORTS[id],))

        # Wait for servers to start
        time.sleep(1)

        # Connect as client to other machines in main thread to enable sending messages to other machine
        for id in other_ids:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((HOST, PORTS[id]))
            self.connections[id] = conn
            assert conn

        csv.writer(open(self.filename, 'w')).writerow(['received', 'global time', 'len of queue', 'logical clock time'])
        assert path.exists(self.filename)
        
        self.cycle()


    def log(self, event_type):
        '''log to csv'''
        with open(self.filename, 'a') as f:
            # print(f"!!!!!!! LOGGING into {self.filename} !!!!!!!!!!")
            writer = csv.writer(f)
            writer.writerow([event_type, time.time(), len(self.queue), self.logical_clock.time])


    def send_event(self, id):
        '''Send a message to another process (and log event)'''
        message = str(self.logical_clock.time) + '%|'
        self.connections[id].sendall(message.encode('ascii'))
        self.log(f'SEND TO {id}')
        
        # unit test of logical clock incrementing
        before = self.logical_clock.time
        self.logical_clock.increment()
        assert self.logical_clock.time == before + 1
        
        # log event
        print(f'{self.id} - Sent {message} to {id}')

    def internal_event(self):
        '''Model internal event'''
        self.log(f'INTERNAL EVENT')
        self.logical_clock.increment()

    def cycle(self):
        '''Start infinite cycle loop to take tick action'''
        start_time = global_time_ms()
        while global_time_ms() - start_time < DURATION * 1000:
            if global_time_ms() - self.last_tick_time > 1000 / self.ticks_ps:
                self.last_tick_time = global_time_ms()
                self.tick()
        print('Done')

    def tick(self):
        '''Action to take upon a tick'''
        if len(self.queue) > 0:
            # Process message on queue
            logical_time = self.queue.popleft()
            self.logical_clock.update(int(logical_time))
            assert self.logical_clock.time >= int(logical_time) + 1
            
            print(f'{self.id} - Popped {logical_time} from queue (new length: {len(self.queue)}, new logical time {self.logical_clock.time})')
            self.log(f'POP FROM QUEUE')
        elif random.random() < self.p_internal:
            assert len(self.queue) == 0
            # Internal event
            self.internal_event()

        else:
            assert len(self.queue) == 0
            # Take random n:
            #   if n == 0, send to one machine
            #   if n == 1, send to other machine
            #   if n == 2, send to both machines
            n = randint(0, 2)
            if n in [0, 2]:
                self.send_event(list(self.connections.keys())[0])
            if n in [1, 2]:
                self.send_event(list(self.connections.keys())[1])

    def start_server(self, port):
        # Start new with one thread for each machine
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, port))
        print("Socket binded to port", port)

        # put the socket into listening mode
        self.socket.listen(5)
        print("Socket is listening!")

        # a forever loop until client wants to exit
        while True:

            try:
                # establish connection with client
                c, addr = self.socket.accept()
            except ConnectionAbortedError as e:
                # else:
                    raise e

            print("-------------------")
            print("> NEW HOMIE ALERT")
            print('> Connected to :' + str(addr[0]) + ':' + str(addr[1]))

            # Start a new thread and return its identifier
            start_new_thread(self.listen, (c,))


    # thread function
    def listen(self, c):
        '''Thread function for receiving messages from other machines.'''

        while True:
            # data received from client
            data = c.recv(1024)

            # a thread has dropped, likely indicating that a user has logged out or deleted their account
            if not data:
                print('> HOMIE DEPARTURE ALERT')
                break

            data = data.decode('ascii')
            if not data:
                raise ValueError

            # split incoming message into distinct packets (delimited by '|')
            packets = data.split('|')
            for packet in packets:
                if packet == '':
                    continue
                logical_time = packet.split('%')[0]
                self.queue.append(logical_time)
                # self.log('RECEIVED FROM ' + str(c.getpeername()))
                print(f'{self.id} - Added {logical_time} to queue (new length: {len(self.queue)})')
