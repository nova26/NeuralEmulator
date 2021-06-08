from NeuralEmulator.Interfaces.SynapseBase import SynapseBase
from NeuralEmulator.Configurators.PulseSynapseConfigurator import PulseSynapseConfigurator
from NeuralEmulator.Preprocessing.PreprocessingBlock import PreprocessingBlock
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.Preprocessing.PosPreprocessingBlock import PosPreprocessingBlock
from NeuralEmulator.Utils.Utils import getValueFromPoly
import numpy as np


class PulseSynapse(SynapseBase):
    def __init__(self, vin, configurator):
        self.vin = vin
        self.configurator = configurator

        self.cacheVinVal = self.vin.getVoltage()
        self.current = 0
        self.coef = np.array(self.configurator.getCoef())
        self.__updateCurrent()

    def __updateCurrent(self):
        self.cacheVinVal = self.vin.getVoltage()
        self.current = self.configurator.getCurrentForVoltage(self.cacheVinVal)

    def getCurrent(self):
        return self.current

    def run(self):
        vin = self.vin.getVoltage()
        if self.cacheVinVal != vin:
            self.__updateCurrent()


class PulseSynapseWeighted(SynapseBase):
    def __init__(self, vinSource, vwSource, configurator):
        self.vinSource = vinSource
        self.vwSource = vwSource

        self.configurator = configurator

        self.cacheVinVal = self.vinSource.getVoltage()
        self.cacheVwVal = self.vwSource.getVoltage()
        self.current = 0
        self.__updateCurrent()

    def __updateCurrent(self):
        self.cacheVinVal = self.vinSource.getVoltage()
        self.cacheVwVal = self.vwSource.getVoltage()

        self.current = self.configurator.getCurrentForVoltage(self.cacheVinVal, self.cacheVwVal)

    def getCurrent(self):
        return self.current

    def run(self):
        vin = self.vinSource.getVoltage()
        vw = self.vwSource.getVoltage()
        if self.cacheVinVal != vin or self.cacheVwVal != vw:
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
