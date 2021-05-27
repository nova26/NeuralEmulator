from NeuralEmulator.Interfaces.LeakCurrentBase import LeakCurrentBase


class NormalLeakSource(LeakCurrentBase):
    def __init__(self, vin, configurator):
        self.vin = vin
        self.cacheVoltage = vin.getVoltage()
        self.current = 0
        self.coef = configurator.getCoef()

    def getCurrent(self):
        return self.current

    def __calcCurrent(self):
        self.current = 0
        for x in range(len(self.coef)):
            self.current += self.coef[x] * (self.cacheVoltage ** x)

    def run(self):
        if self.cacheVoltage != self.vin.getVoltage():
            self.cacheVoltage = self.vin.getVoltage()
            self.__calcCurrent()
