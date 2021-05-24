import os
import sys
from SimBase import SimBase

scriptpath = r"C:\Users\Avi\Desktop\PyProj\NeuralEmulator\Test"
sys.path.append(os.path.abspath(scriptpath))

from SimpleVoltgaeSource import SimpleVoltgaeSource


class PreprocessingBlock(SimBase):
    def __init__(self, voltgaeSource):
        self.voltgaeSource = voltgaeSource
        self.VPOS = 0
        self.VNEG = 0

    def getVoutPOS(self):
        return self.VPOS

    def getVoutNEG(self):
        return self.VNEG


    def run(self):
        vin = self.voltgaeSource.getVoltage()

        VPOS = -vin
        VPOS = VPOS + 1
        VPOS = VPOS * (3.3 / 2.0)
        self.VPOS = VPOS

        VNEG = vin
        VNEG = VNEG + 1
        VNEG = VNEG * (3.3 / 2.0)
        self.VNEG = VNEG


if __name__ == "__main__":
    vin = SimpleVoltgaeSource()
    p = PreprocessingBlock(vin)
    print("VIN -1")
    vin.setVoltage(-1.0)
    p.run()
    print("VPOS {} VNEG {}".format(p.getVoutPOS(),p.getVoutNEG()))

    print("VIN -1")
    vin.setVoltage(1.0)
    p.run()
    print("VPOS {} VNEG {}".format(p.getVoutPOS(),p.getVoutNEG()))
