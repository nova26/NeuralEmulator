from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase


class ErrorBlock(VoltageSourceBase):
    def __init__(self, inputSignal, refSignal,neuronsNumber):
        self.inputSignal = inputSignal
        self.refSignal = refSignal
        self.error = 0
        self.neuronsNumber = neuronsNumber

    def __calcError(self):
        self.error = -(self.inputSignal.getVoltage() - self.refSignal.getVoltage())
        self.error = self.error / self.neuronsNumber

    def getVoltage(self):
        return self.error

    def run(self):
        self.__calcError()
