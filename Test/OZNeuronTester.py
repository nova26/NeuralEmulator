import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

os.environ["SIM_ROOT"] = r"C:\Users\Avi\Desktop\PyProj\NeuralEmulator"
os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"

sys.path.append(os.path.abspath(os.environ["SIM_ROOT"] + "\\config"))
sys.path.append(os.path.abspath(os.environ["SIM_ROOT"] + "\\Utils"))

from SimpleSynapse import SimpleSynapse
from OZNeuronConfigurator import OZNeuronConfigurator
from OZNeuron import OZNeuron
from Utils import getFreqForSpikesVec

ozConfigurator = OZNeuronConfigurator()

csvFile = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\circuits\FreqAsIin\OZ_8_bounded_curves.csv"
df = pd.read_csv(csvFile)

iIn = df['Iin'].tolist()

numberOfTicksPerOneSec = int(1.0 // ozConfigurator.getSimTimeTick())

simTickTime = OZNeuronConfigurator().getSimTimeTick()

simOZfreqs = []

simpleSynapse = SimpleSynapse()
oz = OZNeuron(simpleSynapse, ozConfigurator)

for i in iIn:
    simpleSynapse.setCurrent(i)
    vals = []

    for x in range(numberOfTicksPerOneSec):
        oz.run()
        vals.append(oz.getVoutVal())

    freq = getFreqForSpikesVec(vals)
    simOZfreqs.append(freq)
    print(freq)

df["simOz"] = simOZfreqs
f = csvFile.replace(".csv", "2.csv")
df.to_csv(f)
