import numpy as np
import os
import matplotlib.pyplot as plt
from NeuralEmulator.Interfaces.SimBase import SimBase
from NeuralEmulator.Test.SimpleSynapse import SimpleSynapse
from NeuralEmulator.Test.SimpleLeakCurrent import SimpleLeakCurrent
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.Utils.Utils import getValueFromPoly


class OZNeuron(SimBase):
    def __init__(self, synapse, leakCurrent, ozNeuronConfigurator):
        self.synapse = synapse
        self.leakCurrent = leakCurrent
        self.configurator = ozNeuronConfigurator
        self.spikeValsList = ozNeuronConfigurator.getSpikevalsList()

        self.simTimeTick = ozNeuronConfigurator.getSimTimeTick()

        timeTime = len(self.spikeValsList) * ozNeuronConfigurator.getSimTimeTick()
        self.maxSpike = 1.0 / timeTime

        self.coef = np.array(ozNeuronConfigurator.getIInCoef())
        self.inCurrent = 0
        self.simIndex = 0
        self.outLeak = 0
        self.vout = 0

        self.__configWindow()

    def __configWindow(self):

        freq = self.__getFreq()

        netoSpikesTime = freq * (len(self.spikeValsList) * self.simTimeTick)
        notSpikeTime = 1.0 - netoSpikesTime

        notSpikePerSpikeTime = notSpikeTime / freq if freq != 0 else 1.0

        notSpikeSamples = notSpikePerSpikeTime // self.simTimeTick

        self.spikeSamplesValsList = self.spikeValsList

        if freq == 0:
            self.spikeSamplesValsList = [0 for x in self.spikeSamplesValsList]

        self.notSpikeSamplesCount = notSpikeSamples

        self.windowSize = len(self.spikeValsList) + notSpikeSamples
        self.simIndex = 0
        self.vout = 0

    def __isInSpike(self):
        return self.simIndex < len(self.spikeSamplesValsList) and self.simIndex != 0

    def __setVoutVal(self, i):
        if i < len(self.spikeSamplesValsList):
            self.vout = self.spikeSamplesValsList[i]
        else:
            self.vout = 0

    def getVoutVal(self):
        return self.vout

    def __getWindowSize(self):
        return self.windowSize

    def __getIinCoef(self):
        return self.coef

    def __getIin(self):
        return self.inCurrent

    def __getILeak(self):
        return self.outLeak

    def __updateCurrents(self):
        self.inCurrent = self.synapse.getCurrent()
        self.outLeak = self.leakCurrent.getCurrent()

    def __getFreq(self):

        Isyn = self.__getIin()
        Ileak = self.__getILeak()
        iIn = Isyn - Ileak

        if iIn < 0:
            iIn = 0

        self.freq = int(getValueFromPoly(self.coef, self.coef.shape[0], iIn))
        self.freq = self.configurator.getFreqForCurrent(iIn)

        return self.freq

    def __getMaxFreq(self):
        return self.maxSpike

    def getFreq(self):
        return self.freq

    def run(self):
        inc = self.synapse.getCurrent()
        ouc = self.leakCurrent.getCurrent()
        if (not self.__isInSpike()) and (self.inCurrent != inc or self.outLeak !=ouc):
            self.__updateCurrents()
            self.__configWindow()

        self.__setVoutVal(self.simIndex)
        self.simIndex = self.simIndex + 1
        if self.simIndex >= self.__getWindowSize():
            self.simIndex = 0


if __name__ == "__main__":
    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

    simpleSynapse = SimpleSynapse(1.0 * 10.0 ** (-6))
    leakCurrent = SimpleLeakCurrent(0)
    oZNeuronConfigurator = OZNeuronConfigurator()
    n = OZNeuron(simpleSynapse, leakCurrent, oZNeuronConfigurator)
    simTime = oZNeuronConfigurator.getSimTimeTick()
    numberOfTicksPerOneSec = int(1.0 // oZNeuronConfigurator.getSimTimeTick())
    vals = []
    indexs = [0]
    for x in range(numberOfTicksPerOneSec):
        n.run()
        vals.append(n.getVoutVal())
        indexs.append(indexs[-1] + simTime)

    indexs.remove(0)
    plt.plot(indexs, vals)
    plt.show()
