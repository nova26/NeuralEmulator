from numba import njit, vectorize, float64, int64
import time
import numpy as np


def getFreqForSpikesVec(voutIndexToVal):
    spikeCount = 0

    for x in range(len(voutIndexToVal)):
        if voutIndexToVal[x] < 3.0:
            continue

        if x - 1 < 0 or x + 1 >= len(voutIndexToVal):
            continue

        try:
            if voutIndexToVal[x] > voutIndexToVal[x - 1] and voutIndexToVal[x] > voutIndexToVal[x + 1]:
                spikeCount = spikeCount + 1

        except:
            print("Exception")

    return spikeCount


@njit
def getValueFromPoly(coef, len, x):
    value = 0
    for c in range(len):
        value = value + coef[c] * (x ** c)

    return value


if __name__ == "__main__":
    coef = [x + 1 for x in range(2000)]
    coef = np.array(coef)
    l = coef.shape[0]
    x = 1

    start = time.time()
    getValueFromPoly(coef,l, x)
    print("First Time elapsed:", time.time() - start)

    start = time.time()
    getValueFromPoly(coef,l, x)
    print("Second Time elapsed:", time.time() - start)
