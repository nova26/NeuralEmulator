def getFreqForSpikesVec(voutIndexToVal):
    spikeCount = 0

    for x in range(len(voutIndexToVal)):
        if voutIndexToVal[x] < 1.0:
            continue

        if x - 1 < 0 or x + 1 >= len(voutIndexToVal):
            continue

        try:
            if voutIndexToVal[x] > voutIndexToVal[x - 1] and voutIndexToVal[x] > voutIndexToVal[x + 1]:
                spikeCount = spikeCount + 1

        except:
            print("Exception")

    return spikeCount
