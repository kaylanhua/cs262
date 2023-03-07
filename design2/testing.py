import unittest
from model_machine import ModelMachine
from logical_clock import LogicalClock
from random import randint

# HOST = 'localhost'
# PORT = 6918

class Test(unittest.TestCase):      

    def test_one_machine_starts_correctly(self):
        machine = ModelMachine('A', randint(1,6), 'testing_logs', 0.3)
        machine.listen()
        machine.log()
        # self.assertTrue(False)
    
    def test_two_machines_start_correctly(self):
        machine = ModelMachine('A', randint(1,6), 'testing_logs', 0.3)
        machine.listen()
        machine.log()
        machine2 = ModelMachine('B', randint(1,6), 'testing_logs', 0.3)
        machine2.listen()
        machine2.log()
        # self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
