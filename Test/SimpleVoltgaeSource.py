import os
import sys

scriptpath = r"C:\Users\Avi\Desktop\PyProj\NeuralEmulator"
sys.path.append(os.path.abspath(scriptpath))

from VoltgaeSourceBase import VoltgaeSourceBase

class SimpleVoltgaeSource(VoltgaeSourceBase):
    def __init__(self):
        self.v = 0
    def getVoltage(self):
        return self.v
    def setVoltage(self,v):
        self.v = v

