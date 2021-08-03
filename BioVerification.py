import BioConstants as bconst
import BioUtils as bu

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
            direct = False
            pos = None
        else:
            matrix = similarity
            direct = True
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
                realList.append(reals[i][j])
                probeList.append(matrix[i][j])
                pairs.add(pair)
        realList = numpy.asarray(realList)
        probeList = numpy.asarray(probeList)
        fpr, tpr, thresholds = bu.sklearn_metrics_roc_curve(realList, probeList, direct=direct, pos_label=pos)
        return fpr, tpr, thresholds

    def getFPRFNR(self, bioProbes, isMatrix=bconst.SIMILARITY):
        fpr, tpr, thresholds = self.getFPRTPR(bioProbes, isMatrix)
        fnr = 1 - tpr
        return fpr, fnr, thresholds