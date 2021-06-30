import numpy as np
import os
import matplotlib.pyplot as plt
from NeuralEmulator.Interfaces.SimBase import SimBase
from NeuralEmulator.Interfaces.VoltageSourceBase import VoltageSourceBase
from NeuralEmulator.Test.SimpleSynapse import SimpleSynapse
from NeuralEmulator.Test.SimpleLeakCurrent import CurrentSourceBase, SimpleLeakCurrent
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.Utils.Utils import getValueFromPoly, getObjID


class OZNeuron(VoltageSourceBase):
    def __init__(self, ozNeuronConfigurator, synapse=None, leakCurrent=None, invertOutput=False, printLog=False):
        self.synapse = synapse
        self.leakCurrent = leakCurrent
        self.configurator = ozNeuronConfigurator
        self.spikeValsList = ozNeuronConfigurator.getSpikevalsList()

        self.simTimeTick = ozNeuronConfigurator.getSimTimeTick()

        timeTime = len(self.spikeValsList) * ozNeuronConfigurator.getSimTimeTick()
        self.maxSpike = 1.0 / timeTime
        self.printLog = printLog
        self.inCurrent = 0
        self.simIndex = 0
        self.outLeak = 0
        self.vout = 0
        self.invertOutput = invertOutput

        self.__configWindow()

        self.setSynapse(synapse)

    def setLeakSource(self, leakCurrent):
        self.leakCurrent = leakCurrent

    def setSynapse(self, synapse):
        self.synapse = synapse
        if self.synapse is not None:
            print("OZ {} Synapse {}".format(getObjID(self), getObjID(self.synapse)))

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

    def getVoltage(self):
        if self.invertOutput is True:
            self.vout = (self.vout * -1) + 3.3

        if self.printLog is True and self.vout < 3.3 and self.vout > 0:
            print("Neuron {} vout {}".format(getObjID(self), self.vout))
        return self.vout

    def __getWindowSize(self):
        return self.windowSize

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

        self.freq = self.configurator.getFreqForCurrent(iIn)

        return self.freq

    def __getMaxFreq(self):
        return self.maxSpike

    def getFreq(self):
        return self.freq

    def reset(self):
        self.simIndex = 0
        self.inCurrent = 0
        self.outLeak = 0

    def run(self):
        #  print("OZ {} call {}".format(getObjID(self),getObjID(self.synapse)))
        inc = self.synapse.getCurrent()
        #   print("OZ {} Iin {} from {}".format(getObjID(self), inc, getObjID(self.synapse)))

        #    print("OZ {} call Leak {}".format(getObjID(self),getObjID(self.synapse)))
        ouc = self.leakCurrent.getCurrent()
        #     print("OZ {} Leak {} from {}\n".format(getObjID(self), ouc, getObjID(self.leakCurrent)))

        if (not self.__isInSpike()) and (self.inCurrent != inc or self.outLeak != ouc):
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
    n = OZNeuron(oZNeuronConfigurator, simpleSynapse, leakCurrent, )
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
