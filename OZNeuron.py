import sys
import os
import matplotlib.pyplot as plt

scriptpath = r"C:\Users\Avi\Desktop\PyProj\NeuralEmulator\Test"
sys.path.append(os.path.abspath(scriptpath))

from SimBase import SimBase
from SimpleSynapse import SimpleSynapse
from OZNeuronConfigurator import OZNeuronConfigurator


class OZNeuron(SimBase):
    def __init__(self, synapse, oZNeuronConfigurator):
        self.oZNeuronConfigurator = oZNeuronConfigurator
        self.synapse = synapse

        spikeValsList = self.oZNeuronConfigurator.getSpikevalsList()

        timeTime = len(spikeValsList) * self.oZNeuronConfigurator.getSimTimeTick()
        self.maxSpike = 1.0 / timeTime

        self.__configWindow()

    def __configWindow(self):
        self.inCurrent = self.synapse.getCurrent()

        spikeValsList = self.oZNeuronConfigurator.getSpikevalsList()
        freg = self.getFreq()

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

    def setVoutVal(self, i):
        if i < len(self.spikeSamplesValsList):
            self.vout = self.spikeSamplesValsList[i]
        else:
            self.vout = 0

    def getVoutVal(self):
        return self.vout

    def getWindowSize(self):
        return self.windowSize

    def getIinCoef(self):
        return self.oZNeuronConfigurator.getCoef()

    def getIin(self):
        return self.synapse.getCurrent()

    def getFreq(self):
        freq = 0
        iin = self.getIin()
        coef = self.oZNeuronConfigurator.getIInCoef()

        for x in range(len(coef)):
            freq += coef[x] * iin ** x
        freq -= (freq % 5)

        return int(freq)

    def getMaxFreq(self):
        return self.maxSpike

    def run(self):
        currentCurrent = self.synapse.getCurrent()
        if (not self.__isInSpike()) and self.inCurrent != self.synapse.getCurrent():
            self.__configWindow()

        self.setVoutVal(self.simIndex)
        self.simIndex = self.simIndex + 1
        if self.simIndex >= self.getWindowSize():
            self.simIndex = 0


if __name__ == "__main__":

    simpleSynapse = SimpleSynapse(1.0 * 10.0 ** (-6))
    oZNeuronConfigurator = OZNeuronConfigurator()
    n = OZNeuron(simpleSynapse, oZNeuronConfigurator)
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
