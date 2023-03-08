import unittest
from model_machine import ModelMachine
from logical_clock import LogicalClock
from random import randint
import io
import sys


class Test(unittest.TestCase):   

    def test_one_machine_starts_correctly(self):
        ModelMachine('A', 2, 'testing_logs', 0.3)
        # self.machine.listen()
        # machine.log()
    
    # def test_two_machines_start_correctly(self):
    #     machine = ModelMachine('A', randint(1,6), 'testing_logs', 0.3)
    #     machine.listen()
    #     machine.log()
        
        # machine2 = ModelMachine('B', randint(1,6), 'testing_logs', 0.3)
        # machine2.listen()
        # machine2.log()
        
    def test_logical_clock_increment(self):
        logical = LogicalClock()
        before = logical.time
        logical.increment()
        self.assertEqual(before, logical.time - 1)
        
    def test_logical_clock_update(self):
        logical = LogicalClock()
        before = logical.time
        logical.update(before + 5)
        self.assertEqual(before + 6, logical.time)

    # def assert_printed_output(self, string):
    #     capturedOutput = io.StringIO()                  # Create StringIO object
    #     sys.stdout = capturedOutput                     #  and redirect stdout.
    #     self.assertIn(string, capturedOutput)           # Call function.
    #     sys.stdout = sys.__stdout__                     # Reset redirect.

    # def test_machine_message_sent(self):
    #     self.machine.send_event(self.machine2.id)
    #     self.assert_printed_output("Sent message to B")
        
    # def test_machine_message_received(self):
    #     '''this is def funky'''
    #     self.machine.send_event(self.machine2.id)
    #     self.machine2.listen()
    #     self.assert_printed_output("Received message from A")
        
    # def test_machine_internal_event(self):
    #     self.machine.internal_event()
    #     self.assert_printed_output("INTERNAL EVENT")
        
    # def test_machine_tick(self):
    #     self.machine.tick()
    #     # self.assert_printed_output("INTERNAL EVENT")
    
        

if __name__ == '__main__':
    unittest.main()
