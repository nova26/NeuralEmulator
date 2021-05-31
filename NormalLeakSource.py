from NeuralEmulator.Interfaces.LeakCurrentBase import LeakCurrentBase
from NeuralEmulator.Utils.Utils import getValueFromPoly
import numpy as np

from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.Configurators.NormalLeakSourceConfigurator import NormalLeakSourceConfigurator


class NormalLeakSource(LeakCurrentBase):
    def __init__(self, vin, configurator):
        self.vin = vin
        self.cacheVoltage = vin.getVoltage()
        self.current = 0
        self.coef = np.array(configurator.getCoef())
        self.__calcCurrent()

    def getCurrent(self):
        return self.current

    def __calcCurrent(self):
        c = getValueFromPoly(self.coef,self.coef.shape[0], self.cacheVoltage)
        self.current = c

    def run(self):
        if self.cacheVoltage != self.vin.getVoltage():
            self.cacheVoltage = self.vin.getVoltage()
            self.__calcCurrent()


if __name__ == "__main__":
    import os

    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

    vlk = SimpleVoltageSource(780 * (10 ** -3))
    noramalLeakSourceConfigurator = NormalLeakSourceConfigurator()
    normalLeakSource = NormalLeakSource(vlk, noramalLeakSourceConfigurator)
    normalLeakSource.run()
    print(normalLeakSource.getCurrent())
