
class LogicalClock:
    
    def __init__(self):
        self.time = 0

    def update(self, new_time):
        self.time = max(self.time, new_time) + 1
    
    def increment(self):
        self.time += 1
