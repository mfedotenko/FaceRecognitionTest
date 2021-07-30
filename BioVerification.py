import BioConstants as bconst

import sklearn.metrics

class BioVerification():
    def __init__(self):
        pass

    def getFPRTPR(self, bioProbes, isMatrix=bconst.SIMILARITY):
        probeIds, probePersons, galleryIds, galleryPersons, reals, distances, similarity = bioProbes.get()
        if isMatrix == bconst.DISTANCE:
            matrix = distances
        else:
            matrix = similarity
        pairs = set()
        for i in

        reals = [1 if reals else 0]

        fpr, tpr, thresholds = sklearn.metrics.roc_curve(reals, matrix, pos_label=True)
        return fpr, tpr, thresholds
