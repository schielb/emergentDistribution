# This history class is useful for keeping a record of what was generated previously
class History():
    def __init__(self, length=15):
        self.history_length = length
        
        self.vals_history = [[[0]*10]*10]*self.history_length
        self.start = 0
        self.end = 0
        self.index = length - 1

    def push(self, vals):
        self.vals_history[self.start] = vals

        # If we reached the end of our history length, move the end with us as well
        if ((self.start + 1) % self.history_length) == self.end:
            self.end = (self.end + 1) % self.history_length
        
        self.start = (self.start + 1) % self.history_length
        self.index = (self.index + 1) % self.history_length

    def getPrev(self):
        if self.index != (self.end) % self.history_length:
            self.index = (self.index - 1 + self.history_length) % self.history_length
        return self.vals_history[self.index]

    def getNext(self):
        if self.index != self.start:
            self.index = (self.index + 1) % self.history_length
        return self.vals_history[self.index]

    def getReturn(self):
        self.index = self.start
        self.index = (self.index - 1 + self.history_length) % self.history_length
        return self.vals_history[self.index]

    def clear(self, length=30):
        # Reset everything
        self.history_length = length
        self.vals_history = [[[0]*10]*10]*self.history_length
        self.start = 0
        self.end = 0
        self.index = length - 1

    def canStillMove(self):
        return [self.index != self.end, self.index != (self.start - 1 + self.history_length) % self.history_length]
