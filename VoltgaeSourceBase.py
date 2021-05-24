from SimBase import SimBase


class VoltgaeSourceBase(SimBase):
    def getVoltage(self):
        raise RuntimeError("VoltgaeSourceBase::getVoltage function is not implemented")


