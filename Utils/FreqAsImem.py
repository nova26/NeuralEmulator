import glob
import csv

FOLDER_PATH = r"C:\Users\Avi\Desktop\IntelliSpikesLab\Emulator\circuits\FreqAsIin"

FILE_PATH = FOLDER_PATH + r'\*.txt'


def toFloat(val):
    if 'm' in val:
        val = val.replace("m", "")
        val = float(val)
        val = val * float(10 ** (-3))
        return val
    if 'µ' in val:
        val = val.replace("µ", "")
        val = float(val)
        val = val * float(10 ** (-6))
        return val
    if 'n' in val:
        val = val.replace("n", "")
        val = float(val)
        val = val * float(10 ** (-9))
        return val


    val = float(val)
    return val


def HandleSample(voutIndexToVal):
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


def createCSV():
    filesToRead = glob.glob(FILE_PATH)
    for res in filesToRead:
        print(res)

        with open(res, 'r') as in_file:
            timeVed = []
            spikeVout = []
            iin = None

            iinToFreq = {}
            firstLine = in_file.readline()

            for line in in_file:
                splittedLine = line.split()

                if 'Step' in line:
                    print(line)

                    if iin is None:
                        iin = toFloat(splittedLine[2].split("=")[1])
                    else:
                        freq = HandleSample(spikeVout)
                        iinToFreq[iin] = freq

                        try:
                            iin = toFloat(splittedLine[2].split("=")[1])
                        except:
                            print("ccc")

                        timeVed.clear()
                        spikeVout.clear()

                    continue

                splittedLine = [toFloat(x) for x in splittedLine]
                timeVed.append(splittedLine[0])
                spikeVout.append(splittedLine[1])

            print("Done")
            freq = HandleSample(spikeVout)
            iinToFreq[iin] = freq

            cvsFileName = res.replace(".txt", ".csv")

            with open(cvsFileName, mode='w', newline='') as out_file:
                writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                firstLine = ["Iin","Freq"]
                writer.writerow(firstLine)
                for k in iinToFreq.keys():
                    try:
                        iin = k
                        freq = iinToFreq[iin]

                        writer.writerow([iin, freq])

                    except:
                        print("asdas")


createCSV()
