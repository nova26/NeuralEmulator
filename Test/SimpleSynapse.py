import os
import sys

scriptpath = r"C:\Users\Avi\Desktop\PyProj\NeuralEmulator"
sys.path.append(os.path.abspath(scriptpath))

from SynapseBase import SynapseBase

class SimpleSynapse(SynapseBase):
    def __init__(self, currentVal=0):
        self.current = currentVal
    def getCurrent(self):
        return self.current
    def setCurrent(self,current):
        self.current = current




if __name__ == "__main__":
    print("asda")
    b = SimpleSynapse()
    val = b.getcurrent()
    print(val)