from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase


class PosPreprocessingBlock(VoltageSourceBase):
    def __init__(self, preprocessingBlock):
        self.preprocessingBlock = preprocessingBlock

    def getVoltage(self):
        return self.preprocessingBlock.getVoutPOS()
    def run(self):
        pass
