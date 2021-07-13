import os
import sys
import time

import matplotlib.pyplot as plt
import pandas as pd
from numpy import single

from NeuralEmulator.Adder import Adder
from NeuralEmulator.ClusterSources import ClusterCurrentSource, ClusterVoltageSource
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
from NeuralEmulator.Utils.Generators import Generator
from NeuralEmulator.Utils.Utils import playSound, rasterplotFromCsv
from NeuralEmulator.VoltageSources.LinearSignal import LinearSignal, OscylatorRefSignal, PulseSource, LinearSignalSteps
from NeuralEmulator.VoltageSources.SinSignal import SinSignal, SquaredSin

OUTOUT_FOLDER = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\results\Emulator\Encoding\Bounded\Sin"
OUTOUT_FILE = OUTOUT_FOLDER + "\\lr.csv"

os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

SIM_TIME = 1.0
NUMBER_OF_NEURONS = 8

LR = 0.5 * (10 ** -3)

generator = Generator()
pulseSynapseConfigurator = PulseSynapseConfigurator()
noramalLeakSourceConfigurator = NormalLeakSourceConfigurator()
ozNeuronConfigurator = OZNeuronConfigurator()
temporalConfigurator = TemporalConfigurator()
####################################################################################


vin = SinSignal(SIM_TIME, ozNeuronConfigurator.getSimTimeTick(), 2)
#vin = LinearSignal(SIM_TIME, ozNeuronConfigurator.getSimTimeTick())

l1 = [vin]

# Sin Preprocess
preProcessBlockSin = PreprocessingBlock(l1[0])

vposPortSin = PosPreprocessingBlock(preProcessBlockSin)
vnegPortSin = NegPreprocessingBlock(preProcessBlockSin)

positivePulseSynapsex1 = PulseSynapse(vposPortSin, pulseSynapseConfigurator)
negativePulseSynapsex1 = PulseSynapse(vnegPortSin, pulseSynapseConfigurator)

l2 = [preProcessBlockSin, vposPortSin, vnegPortSin, positivePulseSynapsex1, negativePulseSynapsex1]

l3 = Generator().generateBoundedLeaks()

posNeurons = generator.generateEnsemble(positivePulseSynapsex1, l3)
negNeurons = generator.generateEnsemble(negativePulseSynapsex1, l3)
l4 = posNeurons + negNeurons

layers = [l1, l2, l3, l4]

simResTime = ozNeuronConfigurator.getSimTimeTick()
SIMULATION_TICKS = int(SIM_TIME // simResTime)

timeAxisVal = 0
startTime = time.time()

neurons = [[] for n in l4]

timeAxis = []

vinVals = []
vposVals = []
vnegVals = []

for tick in range(SIMULATION_TICKS):
    print("\rSTEP {}/{}".format(tick + 1, SIMULATION_TICKS))
    timeAxis.append(timeAxisVal)
    timeAxisVal += simResTime

    for layer in layers:
        for obj in layer:
            obj.run()

    vinVals.append(l1[0].getVoltage())
    vposVals.append(vposPortSin.getVoltage())
    vnegVals.append(vnegPortSin.getVoltage())

    for n in range(len(l4)):
        neurons[n].append(l4[n].getVoltage())

fig, axs = plt.subplots(8, 2)

axs[0, 0].plot(timeAxis, vinVals)
axs[1, 0].plot(timeAxis, vposVals)
axs[2, 0].plot(timeAxis, vnegVals)

axs[0, 1].plot(timeAxis,  neurons[3])
axs[1, 1].plot(timeAxis, neurons[2])
axs[2, 1].plot(timeAxis, neurons[1])
axs[3, 1].plot(timeAxis, neurons[0])
axs[4, 1].plot(timeAxis, neurons[7])
axs[5, 1].plot(timeAxis, neurons[6])
axs[6, 1].plot(timeAxis, neurons[5])
axs[7, 1].plot(timeAxis, neurons[4])
plt.show()

df = pd.DataFrame(
    {'time': timeAxis, 'N1': neurons[3], 'N2': neurons[2], 'N3': neurons[1], 'N4': neurons[0],
     'N5': neurons[7], 'N6': neurons[6], 'N7': neurons[5], 'N8': neurons[4], })

df.to_csv(OUTOUT_FILE, index=False)
rasterplotFromCsv(OUTOUT_FOLDER)
