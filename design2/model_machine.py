# ----- HEADERS -----

from collections import deque
import time 
import csv
from logical_clock import LogicalClock
from random import randint
import select
import socket

# ----- VARIABLES -----
host = '10.250.94.109'  
ports = {'A': 6900, 'B': 6901, 'C': 6902}

# ----- FUNCTIONS -----

def global_time_ms():
    '''Returns the current time in milliseconds.'''
    return int(round(time.time() * 1000))

class ModelMachine:

    # connections = 

    def __init__(self, name):
        self.name = name
        self.port = ports[name]
        self.ticks_ps = randint(1,6)
        self.queue = deque()
        self.filename = 'machine_log.csv'
        self.logical_clock = LogicalClock()
        self.last_tick_time = global_time_ms()

        other_ports = [port for port in ports.values() if port != self.port]

        for port in other_ports:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connections.append(conn)
            conn.connect((host, port))

        # TODO: erase and restart file upon intialization
        csv.writer(open('machine_log.csv', 'w')).writerow(['received', 'global time', 'len of queue', 'logical clock time'])
    
    def log(self):
        '''log to csv'''
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([True, time.time(), len(self.queue), LogicalClock.time])
    
    def send_message(self):
        '''called if no messages in the queue'''
        
        if n == 1:
            
            # send to machine 1
        elif n == 2:
            # send to machine 2
        else: 


    def cycle(self):
        '''dictates the number of ticks/sec'''
        while True:
            if global_time_ms() - self.last_tick_time > 1000 / self.ticks_ps:
                self.last_tick_time = global_time_ms()
                self.tick()


    def tick(self):
        '''action to take upon a tick'''
        if len(self.queue) > 0:
            logical_time = self.queue.dequeue()
            self.logical_clock.update(logical_time)
        else: 
            n = randint(1, 10)

    
    # thread function
    def listen(self, conn):
        '''Thread function for receiving messages from one other machine.'''
        while True:
            # data received from client
            try:
                ready = select.select([conn], [], [], 1)
                if ready[0]:
                    data = conn.recv(1024)
                    print('Data (raw):', data, ' len:', len(data))

                    data = data.decode('ascii')
                    print('Data (decoded):', data, ' len:', len(data))

                    if not data:
                        raise ValueError

                    # split incoming message into distict packets (delimited by '|')
                    packets = data.split('|')
                    for packet in packets:
                        if packet == '':
                            continue
                        logical_time = packet.split('%')[0]
                        self.queue.enqueue(logical_time)
                        
            except Exception as e:
                # Error occurs when parent thread closes connection:
                #   not a problem as we are logging out anyway, so ignore
                # break
                raise e

    

if __name__ == '__main__':
    test = ModelMachine() # name, port
    test.log()
    print("testing csv done")