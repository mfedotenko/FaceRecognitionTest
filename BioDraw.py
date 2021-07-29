import seaborn
import matplotlib.pyplot

class BioDraw():
    def __init__(self):
        pass

    # falsePositive = FAR/FPIR  falseNegative = FRR/FNIR
    def drawErrorsOfThresholdCurve(self, falsePositiveName, falsePositives, falseNegativeName, falseNegatives, thresholds, filename):
        seaborn.set(font_scale=1.5)
        seaborn.set_color_codes("muted")
        matplotlib.pyplot.figure(figsize=(10, 8))
        lw = 2
        matplotlib.pyplot.plot(thresholds, falsePositives, lw=lw, label=falsePositiveName)     # синяя
        matplotlib.pyplot.plot(thresholds, falseNegatives, lw=lw, label=falseNegativeName)     # оранжевая
        matplotlib.pyplot.minorticks_on()
        matplotlib.pyplot.grid(which='minor', color='gray', linestyle=':')
        minX = 0    # min(thresholds)
        maxX = max(thresholds)
        minY = 0    # min(min(fpir), min(fnir))
        maxY = max(max(falsePositives), max(falseNegatives))
        matplotlib.pyplot.xlim([minX, maxX])
        matplotlib.pyplot.ylim([minY, maxY + (maxY-minY)/10])
        matplotlib.pyplot.xlabel('Threshold')
        matplotlib.pyplot.ylabel('Rate')
        matplotlib.pyplot.title(falsePositiveName + '/' + falseNegativeName + ' curve')
        matplotlib.pyplot.savefig(filename)
        matplotlib.pyplot.show()
