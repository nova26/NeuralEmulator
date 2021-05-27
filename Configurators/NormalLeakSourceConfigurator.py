import os
import json


class NoramalLeakSourceConfigurator:
    def __init__(self):
        configFileName = os.getenv('NERUSIM_CONF')
        if configFileName is None:
            raise RuntimeError("Env var NERUSIM_CONF is not define")

        confFilePath = configFileName + r"\SimpleLeakCurrent.json"

        if not os.path.exists(confFilePath):
            raise RuntimeError("Configuration file do not exists " + confFilePath)

        data = None
        with open(confFilePath) as f:
            data = json.load(f)
        coef = data["ioutCoef"]
        coef.reverse()

        self.coef = coef

    def getCoef(self):
        return self.coef


if __name__ == "__main__":
    os.environ["NERUSIM_CONF"] = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\config"
    noramalLeakSourceConfigurator = NoramalLeakSourceConfigurator()