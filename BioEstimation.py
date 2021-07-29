import numpy

import BioProbes as bp
import BioIdentification as bi
import BioConstants as bconst
import BioDraw as bd

class BioEstimation():
    def __init__(self, probesPath):
        self.probesPath = "probesPath"
        self.bioProbes = bp.BioProbes()
        self.reals = []
        self.load(probesPath)

    def load(self, probesPath):
        if probesPath is None: probesPath = self.probesPath
        self.bioProbes.load(probesPath)

    def realsMark(self, mode):
        _, _, _, _, reals, distances, _ = self.bioProbes.get()
        if mode == bconst.SIMILARITY:
            self.reals = [bconst.SIMILARITY_TRUE_VALUE if reals else bconst.SIMILARITY_FALSE_VALUE]
        else:
            distanceMax = numpy.asarray(distances).max()
            self.reals = [bconst.DISTANCE_TRUE_VALUE if reals else distanceMax]

    def FPIRFNIR(self, isMatrix=bconst.SIMILARITY, mode="any", L=1, filename=""):
        bioIdentification = bi.BioIdentification()
        fpir, fnir, thresholds = bioIdentification.getFPIRFNIR(self.bioProbes, isMatrix, mode, L)
        bioDraw = bd.BioDraw()
        bioDraw.drawErrorsOfThresholdCurve('FPIR', fpir, 'FNIR', fnir, thresholds, filename)

bioEstimation = BioEstimation(bconst.PROBES_PATH)
bioEstimation.FPIRFNIR(isMatrix=bconst.DISTANCE, mode="any", L=1, filename="./output/FPIRFNIR_Distance_Any_1.png")
