from NeuralEmulator.Configurators.NormalLeakSourceConfigurator import NormalLeakSourceConfigurator
from NeuralEmulator.Configurators.OZNeuronConfigurator import OZNeuronConfigurator
from NeuralEmulator.Configurators.TemporalConfigurator import TemporalConfigurator
from NeuralEmulator.LearningBlock import LearningBlock
from NeuralEmulator.NormalLeakSource import NormalLeakSource
from NeuralEmulator.OZNeuron import OZNeuron
from NeuralEmulator.TemporalIntegration import TemporalIntegration
from NeuralEmulator.Test.SimpleVoltageSource import SimpleVoltageSource
from NeuralEmulator.VoltageSources.LinearSignal import StaticSource


class Generator:
    def __init__(self):
        self.noramalLeakSourceConfigurator = NormalLeakSourceConfigurator()
        self.ozNeuronConfigurator = OZNeuronConfigurator()
        self.temporalConfigurator = TemporalConfigurator()

    def generateNormalLeakSources(self, numberOfSources, startVale, step):
        leakSources = []

        for x in range(numberOfSources):
            normalLeakSource = NormalLeakSource(self.noramalLeakSourceConfigurator, StaticSource(startVale))
            leakSources.append(normalLeakSource)
            startVale += step

        return leakSources

    def generateUniformLeaks(self):
        normalLeakSource = NormalLeakSource(self.noramalLeakSourceConfigurator, StaticSource(745.0 * (10 ** -3)))
        normalLeakSource2 = NormalLeakSource(self.noramalLeakSourceConfigurator, StaticSource(700.0 * (10 ** -3)))
        normalLeakSource3 = NormalLeakSource(self.noramalLeakSourceConfigurator, StaticSource(600.0 * (10 ** -3)))
        normalLeakSource4 = NormalLeakSource(self.noramalLeakSourceConfigurator, StaticSource(450.0 * (10 ** -3)))

        return [normalLeakSource, normalLeakSource2, normalLeakSource3, normalLeakSource4]

    def generateBoundedLeaks(self):
        return self.generateNormalLeakSources(int(8 / 2), 730.0 * (10 ** -3), 15.0 * (10 ** -3))
    def generateEnsemble(self, inputSrc, leakSources):
        ens = []
        for lk in leakSources:
            oz = OZNeuron(self.ozNeuronConfigurator, inputSrc, lk)
            ens.append(oz)
        return ens

    def generateTempIntegrations(self, temporalConfig, ozNeurons):
        temps = []
        for n in ozNeurons:
            tempIntegration = TemporalIntegration(temporalConfig, self.temporalConfigurator, n)
            temps.append(tempIntegration)
        return temps

    def generateLearningBlock(self, LR, temporals, errblock):
        blocks = []

        for x in range(len(temporals)):
            learningBlock = LearningBlock(LR, temporals[x], errblock)
            blocks.append(learningBlock)
        return blocks
