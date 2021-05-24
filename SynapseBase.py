from SimBase import SimBase
class SynapseBase(SimBase):
    def getCurrent(self):
        raise RuntimeError("getcurrent function is not implemented")
