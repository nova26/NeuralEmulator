import matplotlib.pyplot as plt
import pandas as pd
from NeuralEmulator.Preprocessing.PreprocessingBlock import PreprocessingBlock
from NeuralEmulator.Preprocessing.PosPreprocessingBlock import PosPreprocessingBlock
from NeuralEmulator.Preprocessing.NegPreprocessingBlock import NegPreprocessingBlock
from NeuralEmulator.Configurators.PulseSynapseConfigurator import PulseSynapseConfigurator
from NeuralEmulator.PulseSynapse import PulseSynapse
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.OZNeuron import OZNeuron
from NeuralEmulator.Test.SimpleLeakCurrent import SimpleLeakCurrent
from NeuralEmulator.Utils.Utils import getFreqForSpikesVec
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.Configurators.NormalLeakSourceConfigurator import NormalLeakSourceConfigurator
from NeuralEmulator.NormalLeakSource import NormalLeakSource

OUTOUT_FOLDER = r'C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\tuneCurves'
OUTOUT_FILE = OUTOUT_FOLDER + "\\curves.csv"


def runSimObj(obj):
    obj.run()


def buildNeuron(vinSource, vinConfigurator, vlkVal, noramalLeakSourceConfigurator, ozNeuronConfigurator):
    pulseSynapse = PulseSynapse(vinSource, vinConfigurator)

    vlk = SimpleVoltageSource(vlkVal)
    normalLeakSource = NormalLeakSource(vlk, noramalLeakSourceConfigurator)

    ozNeuron = OZNeuron(pulseSynapse, normalLeakSource, ozNeuronConfigurator)
    return ozNeuron


if __name__ == "__main__":
    import os

    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

    pulseSynapseConfigurator = PulseSynapseConfigurator()
    noramalLeakSourceConfigurator = NormalLeakSourceConfigurator()
    ozNeuronConfigurator = OZNeuronConfigurator()

    # vin
    vin = SimpleVoltageSource()
    preProcessBlock = PreprocessingBlock(vin)
    vpos = PosPreprocessingBlock(preProcessBlock)
    vneg = NegPreprocessingBlock(preProcessBlock)

    # Neurons
    positivePulseSynapse = PulseSynapse(vpos, pulseSynapseConfigurator)
    negativePulseSynapse = PulseSynapse(vneg, pulseSynapseConfigurator)

    normalLeakSource1 = NormalLeakSource(SimpleVoltageSource(760.0 * (10 ** -3)), noramalLeakSourceConfigurator)
    normalLeakSource2 = NormalLeakSource(SimpleVoltageSource(740.0 * (10 ** -3)), noramalLeakSourceConfigurator)
    normalLeakSource3 = NormalLeakSource(SimpleVoltageSource(720.0 * (10 ** -3)), noramalLeakSourceConfigurator)
    normalLeakSource4 = NormalLeakSource(SimpleVoltageSource(700.0 * (10 ** -3)), noramalLeakSourceConfigurator)

    ozNeuron1 = OZNeuron(positivePulseSynapse, normalLeakSource1, ozNeuronConfigurator)
    ozNeuron2 = OZNeuron(positivePulseSynapse, normalLeakSource2, ozNeuronConfigurator)
    ozNeuron3 = OZNeuron(positivePulseSynapse, normalLeakSource3, ozNeuronConfigurator)
    ozNeuron4 = OZNeuron(positivePulseSynapse, normalLeakSource4, ozNeuronConfigurator)

    ozNeuron5 = OZNeuron(negativePulseSynapse, normalLeakSource1, ozNeuronConfigurator)
    ozNeuron6 = OZNeuron(negativePulseSynapse, normalLeakSource2, ozNeuronConfigurator)
    ozNeuron7 = OZNeuron(negativePulseSynapse, normalLeakSource3, ozNeuronConfigurator)
    ozNeuron8 = OZNeuron(negativePulseSynapse, normalLeakSource4, ozNeuronConfigurator)

    # Layers
    L1 = [vin, preProcessBlock, vpos]
    L2 = [positivePulseSynapse, negativePulseSynapse, normalLeakSource1, ozNeuron1, ozNeuron2, ozNeuron3, ozNeuron4, ozNeuron5, ozNeuron6,
          ozNeuron7, ozNeuron8]
    layers = [L1, L2]

    SIM_TIME = 1.0

    NEURON_NUM = 8

    neuronsVout = {}
    neuronsFreqs = {"VIN": []}
    keyToObj = {}
    for x in range(NEURON_NUM):
        k = "n{}".format(x)
        neuronsVout[k] = []
        neuronsFreqs[k] = []
        keyToObj[k] = L2[x + 3]

    simResTime = ozNeuronConfigurator.getSimTimeTick()
    numberOfTicksPerOneSec = int(SIM_TIME // simResTime)

    VIN = -1
    STEP_SIZE = 50 * (10 ** -3)
    VIN_MAX = 1

    totalIncrements = int((VIN_MAX - VIN) // STEP_SIZE) + 1
    currentStep = 1
    while VIN < VIN_MAX:
        print("STEP {}/{}".format(currentStep, totalIncrements))
        currentStep += 1
        neuronsFreqs["VIN"].append(VIN)

        for t in range(numberOfTicksPerOneSec):
            vin.setVoltage(VIN)
            for l in layers:
                for obj in l:
                    obj.run()
            for ko in keyToObj.keys():
                neuronsVout[ko].append(keyToObj[ko].getVoutVal())

        for k in neuronsFreqs.keys():
            if k != "VIN":
                f1 = getFreqForSpikesVec(neuronsVout[k])
                s = neuronsFreqs[k]
                s.append(f1)
                neuronsFreqs[k] = s
                neuronsVout[k] = []

        VIN += STEP_SIZE

    df = pd.DataFrame(neuronsFreqs)
    df.to_csv(OUTOUT_FILE, header=True, index=False)
