import matplotlib.pyplot as plt

from NeuralEmulator.Preprocessing.PreprocessingBlock import PreprocessingBlock
from NeuralEmulator.Preprocessing.PosPreprocessingBlock import PosPreprocessingBlock

from NeuralEmulator.Configurators.PulseSynapseConfigurator import PulseSynapseConfigurator
from NeuralEmulator.PulseSynapse import PulseSynapse
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.OZNeuron import OZNeuron
from NeuralEmulator.Test.SimpleLeakCurrent import SimpleLeakCurrent
from NeuralEmulator.Utils.Utils import getFreqForSpikesVec
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource


def runSimObj(obj):
    obj.run()


if __name__ == "__main__":
    import os
    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"
    vin = SimpleVoltageSource()
    preProcessBlock = PreprocessingBlock(vin)
    vpos = PosPreprocessingBlock(preProcessBlock)

    pulseSynapse = PulseSynapse(vpos, PulseSynapseConfigurator())
    leakCurrent = SimpleLeakCurrent(3.5 * (10 ** (-6)))

    ozNeuron = OZNeuron(pulseSynapse, leakCurrent, OZNeuronConfigurator())

    simObjects = [vin, preProcessBlock, pulseSynapse, leakCurrent, ozNeuron]

    simResTime = OZNeuronConfigurator().getSimTimeTick()
    numberOfTicksPerOneSec = int(1.0 // simResTime)

    x = []
    freqs = []
    vstep = -1
    while vstep < 1:
        vout = []
        for t in range(numberOfTicksPerOneSec):
            vin.setVoltage(vstep)
            for obj in simObjects:
                obj.run()

            vout.append(simObjects[-1].getVoutVal())

        x.append(vstep)
        f = getFreqForSpikesVec(vout)
        freqs.append(f)

        vstep += 100 * (10 ** -3)

    plt.plot(x, freqs, "-o")
    plt.show()
