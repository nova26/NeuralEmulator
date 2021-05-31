from NeuralEmulator.Interfaces.SynapseBase import SynapseBase
from NeuralEmulator.Configurators.PulseSynapseConfigurator import PulseSynapseConfigurator
from NeuralEmulator.Preprocessing.PreprocessingBlock import PreprocessingBlock
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.Preprocessing.PosPreprocessingBlock import PosPreprocessingBlock


class PulseSynapse(SynapseBase):
    def __init__(self, vin, configurator):
        self.vin = vin
        self.configurator = configurator

        self.cacheVinVal = self.vin.getVoltage()
        self.current = 0

    def __updateCurrent(self):
        self.cacheVinVal = self.vin.getVoltage()
        i = 0
        vin = self.vin.getVoltage()
        coef = self.configurator.getCoef()

        for x in range(len(coef)):
            i += coef[x] * (vin ** x)
        self.current = i

    def getCurrent(self):
        return self.current

    def run(self):
        if self.cacheVinVal != self.vin.getVoltage():
            self.__updateCurrent()


if __name__ == "__main__":
    import os
    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

    vin = SimpleVoltageSource()
    p = PreprocessingBlock(vin)

    posPreprocessingBlock = PosPreprocessingBlock(p)
    cfg = PulseSynapseConfigurator()

    pulseSyn = PulseSynapse(posPreprocessingBlock, cfg)
    print("asd {}".format(pulseSyn.getCurrent()))
