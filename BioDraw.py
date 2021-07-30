import seaborn
import matplotlib.pyplot

class BioDraw():
    def __init__(self):
        pass

    # falsePositive = FAR/FPIR  falseNegative = FRR/FNIR
    def drawRocCurve(self, curveName, falsePositiveName, falsePositives, truePositiveName, truePositives, filename, zoom=False, zoom_tp=0, zoom_fp=1):
        fp, tp = [], []
        if zoom:
            for x in range(len(falsePositives)):
                if falsePositives[x] <= zoom_fp and truePositives[x] >= zoom_tp:
                    fp.append(falsePositives[x])
                    tp.append(truePositives[x])
        else:
            fp = falsePositives
            tp = truePositives
        seaborn.set(font_scale=1.5)
        seaborn.set_color_codes("muted")
        matplotlib.pyplot.figure(figsize=(10, 8))
        lw = 2
        matplotlib.pyplot.plot(fp, tp, lw=lw, label=curveName)
        matplotlib.pyplot.minorticks_on()
        matplotlib.pyplot.grid(which='minor', color='gray', linestyle=':')
        matplotlib.pyplot.xlim([min(fp), max(fp)])
        matplotlib.pyplot.ylim([min(tp), max(tp) + (max(tp) - min(tp)) / 10])
        matplotlib.pyplot.xlabel(falsePositiveName)
        matplotlib.pyplot.ylabel(truePositiveName)
        matplotlib.pyplot.title(curveName)
        matplotlib.pyplot.savefig(filename)
        matplotlib.pyplot.show()

    # falsePositive = FAR/FPIR  falseNegative = FRR/FNIR
    def drawErrorsOfThresholdCurve(self, curveName, falsePositiveName, falsePositives, falseNegativeName, falseNegatives, thresholds, filename, zoom=False, zoom_rate=1):
        fp, fn, th = [], [], []
        if zoom:
            for x in range(len(thresholds)):
                if falsePositives[x] <= zoom_rate and falseNegatives[x] <= zoom_rate:
                    fp.append(falsePositives[x])
                    fn.append(falseNegatives[x])
                    th.append(thresholds[x])
        else:
            fp = falsePositives
            fn = falseNegatives
            th = thresholds
        seaborn.set(font_scale=1.5)
        seaborn.set_color_codes("muted")
        matplotlib.pyplot.figure(figsize=(10, 8))
        lw = 2
        matplotlib.pyplot.plot(th, fp, lw=lw, label=falsePositiveName)     # синяя
        matplotlib.pyplot.plot(th, fn, lw=lw, label=falseNegativeName)     # оранжевая
        matplotlib.pyplot.minorticks_on()
        matplotlib.pyplot.grid(which='minor', color='gray', linestyle=':')
        if zoom:
            minX = min(th)
            minY = min(min(fp), min(fn))
        else:
            minX = 0
            minY = 0
        maxX = max(th)
        maxY = max(max(fp), max(fn))
        matplotlib.pyplot.xlim([minX, maxX])
        matplotlib.pyplot.ylim([minY, maxY + (maxY-minY)/10])
        matplotlib.pyplot.xlabel('Threshold')
        matplotlib.pyplot.ylabel('Rate')
        matplotlib.pyplot.title(curveName)
        matplotlib.pyplot.savefig(filename)
        matplotlib.pyplot.show()

