from NeuralEmulator.Interfaces.VoltageSourceBase import VoltgaeSourceBase


class NegPreprocessingBlock(VoltgaeSourceBase):
    def __init__(self, preprocessingBlock):
        self.preprocessingBlock = preprocessingBlock

    def getVoltage(self):
        return self.preprocessingBlock.getVoutNEG()

    def run(self):
        pass
