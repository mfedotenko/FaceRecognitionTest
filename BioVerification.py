import BioConstants as bconst

import sklearn.metrics
import numpy
import math

class BioVerification():
    def __init__(self):
        pass

    def getFPRTPR(self, bioProbes, isMatrix=bconst.SIMILARITY):
        probeIds, probePersons, galleryIds, galleryPersons, reals, distances, similarity = bioProbes.get()
        if isMatrix == bconst.DISTANCE:
            matrix = distances
            maxD = numpy.max(matrix)
            pos = math.floor(maxD)
            reals_new = (1 - reals) * pos
            pos = 0
        else:
            matrix = similarity
            reals_new = reals.astype(int)
            pos = 1
        pairs = set()
        realList = []
        probeList = []
        (m, n) = matrix.shape
        for i in range(m):
            for j in range(n):
                if probeIds[i] == galleryIds[j]: continue
                pair = frozenset({probeIds[i], galleryIds[j]})
                if pair in pairs: continue
                realList.append(reals_new[i][j])
                probeList.append(matrix[i][j])
                pairs.add(pair)
        realList = numpy.asarray(realList)
        probeList = numpy.asarray(probeList)
        fpr, tpr, thresholds = sklearn.metrics.roc_curve(realList, probeList, pos_label=pos)
        if isMatrix == bconst.DISTANCE:
            fpr = 1 - fpr
            tpr = 1 - tpr
        return fpr, tpr, thresholds

    def getFPRFNR(self, bioProbes, isMatrix=bconst.SIMILARITY):
        fpr, tpr, thresholds = self.getFPRTPR(bioProbes, isMatrix)
        fnr = 1 - tpr
        return fpr, fnr, thresholds