import os
import sys
import time

import matplotlib.pyplot as plt
import pandas as pd

from NeuralEmulator.Adder import Adder
from NeuralEmulator.Configurators.NormalLeakSourceConfigurator import NormalLeakSourceConfigurator
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.Configurators.PulseSynapseConfigurator import PulseSynapseConfigurator
from NeuralEmulator.Configurators.TemporalConfigurator import TemporalConfigurator
from NeuralEmulator.ErrorBlock import ErrorBlock
from NeuralEmulator.LearningBlock import LearningBlock
from NeuralEmulator.NormalLeakSource import NormalLeakSource
from NeuralEmulator.OZNeuron import OZNeuron
from NeuralEmulator.Preprocessing.NegPreprocessingBlock import NegPreprocessingBlock
from NeuralEmulator.Preprocessing.PosPreprocessingBlock import PosPreprocessingBlock
from NeuralEmulator.Preprocessing.PreprocessingBlock import PreprocessingBlock
from NeuralEmulator.PulseSynapse import PulseSynapse
from NeuralEmulator.TemporalIntegration import TemporalIntegration
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.Utils.NeuronsGenerator import NeuronsGenerator
from NeuralEmulator.VoltageSources.SinSignal import SinSignal

OUTOUT_FILE = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\Learning\lr.csv"

os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

SIM_TIME = 1.0

pulseSynapseConfigurator = PulseSynapseConfigurator()
noramalLeakSourceConfigurator = NormalLeakSourceConfigurator()
ozNeuronConfigurator = OZNeuronConfigurator()
temporalConfigurator = TemporalConfigurator()

# VIN
vin = SinSignal(SIM_TIME, ozNeuronConfigurator.getSimTimeTick(), 2)
preProcessBlock = PreprocessingBlock(vin)
vposPort = PosPreprocessingBlock(preProcessBlock)
vnegPort = NegPreprocessingBlock(preProcessBlock)

# Synapses
positivePulseSynapse = PulseSynapse(vposPort, pulseSynapseConfigurator)
negativePulseSynapse = PulseSynapse(vnegPort, pulseSynapseConfigurator)

# Leak
normalLeakSource = NormalLeakSource(SimpleVoltageSource(745.0 * (10 ** -3)), noramalLeakSourceConfigurator)
normalLeakSource2 = NormalLeakSource(SimpleVoltageSource(735.0 * (10 ** -3)), noramalLeakSourceConfigurator)
normalLeakSource3 = NormalLeakSource(SimpleVoltageSource(725.0 * (10 ** -3)), noramalLeakSourceConfigurator)
normalLeakSource4 = NormalLeakSource(SimpleVoltageSource(715.0 * (10 ** -3)), noramalLeakSourceConfigurator)

# Neuron
ozNeuron1 = OZNeuron(positivePulseSynapse, normalLeakSource, ozNeuronConfigurator)
ozNeuron2 = OZNeuron(positivePulseSynapse, normalLeakSource2, ozNeuronConfigurator)
ozNeuron3 = OZNeuron(positivePulseSynapse, normalLeakSource3, ozNeuronConfigurator)
ozNeuron4 = OZNeuron(positivePulseSynapse, normalLeakSource4, ozNeuronConfigurator)
ozNeuron5 = OZNeuron(negativePulseSynapse, normalLeakSource, ozNeuronConfigurator)
ozNeuron6 = OZNeuron(negativePulseSynapse, normalLeakSource2, ozNeuronConfigurator)
ozNeuron7 = OZNeuron(negativePulseSynapse, normalLeakSource3, ozNeuronConfigurator)
ozNeuron8 = OZNeuron(negativePulseSynapse, normalLeakSource4, ozNeuronConfigurator)

# Temporal Integration
temporalConfig = 450 * (10 ** -3)
temporalIntegration1 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron1)
temporalIntegration2 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron2)
temporalIntegration3 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron3)
temporalIntegration4 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron4)
temporalIntegration5 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron5)
temporalIntegration6 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron6)
temporalIntegration7 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron7)
temporalIntegration8 = TemporalIntegration(temporalConfig, temporalConfigurator, ozNeuron8)

# Adder
adder = Adder()

# ErrorCKT
errorBlock = ErrorBlock(adder, vin, 8)

# LearningBlocks
LR = 0.01
learningBlock1 = LearningBlock(LR, errorBlock, temporalIntegration1)
learningBlock2 = LearningBlock(LR, errorBlock, temporalIntegration2)
learningBlock3 = LearningBlock(LR, errorBlock, temporalIntegration3)
learningBlock4 = LearningBlock(LR, errorBlock, temporalIntegration4)
learningBlock5 = LearningBlock(LR, errorBlock, temporalIntegration5)
learningBlock6 = LearningBlock(LR, errorBlock, temporalIntegration6)
learningBlock7 = LearningBlock(LR, errorBlock, temporalIntegration7)
learningBlock8 = LearningBlock(LR, errorBlock, temporalIntegration8)

# Layers
L1 = [vin, preProcessBlock]
L2 = [negativePulseSynapse, positivePulseSynapse]
L3 = [ozNeuron1, ozNeuron2, ozNeuron3, ozNeuron4, ozNeuron5, ozNeuron6, ozNeuron7, ozNeuron8]
L4 = [temporalIntegration1, temporalIntegration2, temporalIntegration3, temporalIntegration4, temporalIntegration5, temporalIntegration6,
      temporalIntegration7, temporalIntegration8]
L5 = [learningBlock1, learningBlock2, learningBlock3, learningBlock4, learningBlock5, learningBlock6, learningBlock7, learningBlock8]

L6 = [adder]
L7 = [errorBlock]

adder.setListOfSources(L5)
layers = [L1, L2, L3, L4, L5, L6, L7]

timeAxis = []
neuronsVout = {}
temporalBlockVout = {}

learningBlockVout = {}

keyToNeuronObj = {}
keyToTemporalObj = {}
keyToLRObj = {}

vinVals = []
adderVals = []
errorVals = []

for x in range(len(L3)):
    k = "n{}".format(x)
    neuronsVout[k] = []
    temporalBlockVout[k] = []
    learningBlockVout[k] = []

    keyToNeuronObj[k] = L3[x]
    keyToTemporalObj[k] = L4[x]
    keyToLRObj[k] = L5[x]

simResTime = ozNeuronConfigurator.getSimTimeTick()
SIMULATION_TICKS = int(SIM_TIME // simResTime)

timeAxisVal = 0
startTime = time.time()
for tick in range(SIMULATION_TICKS):

    sys.stdout.write("\rSTEP {}/{}".format(tick, SIMULATION_TICKS))
    timeAxis.append(timeAxisVal)
    timeAxisVal += simResTime

    for l in layers:
        for obj in l:
            obj.run()

    for ko in keyToNeuronObj.keys():
        neuronsVout[ko].append(keyToNeuronObj[ko].getVoutVal())
        temporalBlockVout[ko].append(keyToTemporalObj[ko].getVoltage())
        learningBlockVout[ko].append(keyToLRObj[ko].getVoltage())

    adderVals.append(adder.getVoltage())
    errorVals.append(errorBlock.getVoltage())
    vinVals.append(vin.getVoltage())

print("\nsimulation runtime {}".format(time.time() - startTime))
plt.plot(timeAxis, vinVals)
plt.plot(timeAxis, adderVals)
plt.show()

oo = {"time": timeAxis, "VIN": vinVals, "VOUT": adderVals}

df = pd.DataFrame(oo)
df.to_csv(OUTOUT_FILE, header=True, index=False)
plt.plot()

