from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase


class LearningBlock(VoltageSourceBase):
    def __init__(self, LR, errorSignal, temporalSignal):
        self.LR = LR
        self.errorSignal = errorSignal
        self.temporalSignal = temporalSignal
        self.vout = 0
        self.weight = 0

    def __calcVout(self):
        deltaW = self.errorSignal.getVoltage() * self.temporalSignal.getVoltage() * self.LR
        self.weight = self.weight + deltaW
        self.vout = self.temporalSignal.getVoltage() * self.weight

    def getVoltage(self):
        return self.vout
    
    def run(self):
        self.__calcVout()
