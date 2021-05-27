import sys
import os
import matplotlib.pyplot as plt

from NeuralEmulator.Interfaces.SimBase import SimBase
from NeuralEmulator.Test.SimpleSynapse import SimpleSynapse
from NeuralEmulator.Test.SimpleLeakCurrent import SimpleLeakCurrent

from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator


class OZNeuron(SimBase):
    def __init__(self, synapse, leakCurrent, oZNeuronConfigurator):
        self.oZNeuronConfigurator = oZNeuronConfigurator
        self.synapse = synapse
        self.leakCurrent = leakCurrent

        spikeValsList = self.oZNeuronConfigurator.getSpikevalsList()

        timeTime = len(spikeValsList) * self.oZNeuronConfigurator.getSimTimeTick()
        self.maxSpike = 1.0 / timeTime

        self.__configWindow()

    def __configWindow(self):
        self.__updateCurrents()

        spikeValsList = self.oZNeuronConfigurator.getSpikevalsList()
        freg = self.__getFreq()

        netoSpikesTime = freg * (len(spikeValsList) * self.oZNeuronConfigurator.getSimTimeTick())
        notSpikeTime = 1.0 - netoSpikesTime
        notSpikePerSpikeTime = notSpikeTime / freg

        notSpikeSamples = notSpikePerSpikeTime // self.oZNeuronConfigurator.getSimTimeTick()

        self.spikeSamplesValsList = spikeValsList
        self.notSpikeSamplesCount = notSpikeSamples

        self.windowSize = len(spikeValsList) + notSpikeSamples
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
        return self.oZNeuronConfigurator.getCoef()

    def __getIin(self):
        return self.inCurrent

    def __getILeak(self):
        return self.outLeak

    def __updateCurrents(self):
        self.inCurrent = self.synapse.getCurrent()
        self.outLeak = self.leakCurrent.getCurrent()

    def __getFreq(self):
        freq = 0
        iIn = self.__getIin()
        iLeak = self.__getILeak()

        iIn = iIn - iLeak
        if iIn < 0:
            iIn = 0

        coef = self.oZNeuronConfigurator.getIInCoef()

        for x in range(len(coef)):
            freq += coef[x] * (iIn ** x)
        freq -= (freq % 5)

        return int(freq)

    def __getMaxFreq(self):
        return self.maxSpike

    def run(self):
        if (not self.__isInSpike()) and self.inCurrent != self.synapse.getCurrent():
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
    simTime = OZNeuronConfigurator().getSimTimeTick()
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
