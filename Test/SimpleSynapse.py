from NeuralEmulator.Interfaces.SynapseBase import SynapseBase


class SimpleSynapse(SynapseBase):
    def __init__(self, currentVal=0):
        self.current = currentVal

    def getCurrent(self):
        return self.current

    def setCurrent(self, current):
        self.current = current

    def run(self):
        pass


if __name__ == "__main__":
    print("asda")
    b = SimpleSynapse()
    val = b.getCurrent()
    print(val)
