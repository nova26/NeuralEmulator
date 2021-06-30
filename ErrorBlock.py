from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase


class ErrorBlock(VoltageSourceBase):
    def __init__(self, inputSignal, refSignal, neuronsNumber):
        self.inputSignal = inputSignal
        self.refSignal = refSignal
        self.error = 0
        self.neuronsNumber = neuronsNumber

    def setInputSignal(self):
        pass

    def __calcError(self):
        inputSig = self.inputSignal.getVoltage()
        refSig = self.refSignal.getVoltage()

        self.error = -(inputSig - refSig)
        self.error = self.error / self.neuronsNumber

    def getVoltage(self):
        return self.error

    def run(self):
        self.__calcError()
