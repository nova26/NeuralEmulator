from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase
import numpy as np
import matplotlib.pyplot as plt


class LinearSignal(VoltageSourceBase):
    def __init__(self, simTime, simStep, endVale):
        size = int(simTime // simStep)
        x = np.linspace(0, size, size)
        m = endVale / simTime
        self.y = (m * x) / size
        self.index = 0
        self.vout = 0

    def getVoltage(self):
        return self.vout

    def run(self):
        if self.index > len(self.y):
            self.vout = self.y[-1]
        else:
            self.vout = self.y[self.index]
            self.index += 1


class StaticSource(VoltageSourceBase):
    def __init__(self, vin):
        self.vin = vin

    def getVoltage(self):
        return self.vin

    def setVoltage(self, val):
        self.vin = val

    def run(self):
        pass


class ListVoltageSource(VoltageSourceBase):

    def __init__(self, values):
        self.values = values
        self.index = 0
        self.len = len(values)

    def getVoltage(self):
        if self.index >= len(self.values):
            return self.values[-1]
        else:
            return self.values[self.index]

    def run(self):
        self.index += 1


class OscylatorRefSignal(VoltageSourceBase):

    def __init__(self, vmain, vref, factor):
        self.vmain = vmain
        self.vref = vref
        self.factor = factor
        self.vout = 0

    def run(self):
        self.vout = self.vmain.getVoltage() + self.factor * self.vref.getVoltage()

    def getVoltage(self):
        return self.vout


class PulseSource(VoltageSourceBase):
    def __init__(self, pulseStartTime, pulseWidth, pulseAmplitude, simTick=4.8809138070110005e-05):
        self.pulseStartTime = pulseStartTime
        self.pulseWidth = pulseWidth
        self.pulseAmplitude = pulseAmplitude
        self.simTick = simTick
        self.counter = 1
        self.vout = 0

    def run(self):
        ctime = self.counter * self.simTick
        if self.pulseStartTime <= ctime <= self.pulseStartTime + self.pulseWidth:
            self.vout = self.pulseAmplitude
        else:
            self.vout = 0
        self.counter += 1

    def getVoltage(self):
        return self.vout


if __name__ == "__main__":
    sinSignal = LinearSignal(1, 4.8809138070110005e-05, 1)
    t = sinSignal.getVoltage()
    print("dsf")
