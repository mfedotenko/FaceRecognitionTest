import numpy
import sklearn.metrics

import BioProbes as bp
import BioIdentification as bi
import BioConstants as bconst
import BioPlotting as bd
import BioVerification as bv

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

    def VerificationCurves(self, isMatrix=bconst.SIMILARITY, filepath="", zoom=False, zoom_rates={'fnfp': 1.0, 'tp': 0.9, 'fp': 0.1, 'fn': 0.1}):
        bioVerification = bv.BioVerification()
        # получение значений
        fpr, fnr, thresholds = bioVerification.getFPRFNR(self.bioProbes, isMatrix)
        # построение графиков
        bioDraw = bd.BioDraw()
        curveName = 'FRR/FAR Curve\n' + 'Type=' + isMatrix + ' Zoom=' + str(zoom)
        filename = filepath + '/FARFRR_' + isMatrix + ('_zoom' if zoom else '') + '.png'
        bioDraw.drawErrorsOfThresholdCurve(curveName, 'FAR', fpr, 'FRR', fnr, thresholds, filename, zoom, zoom_rates['fnfp'])
        curveName = 'ROC Curve\n' + 'Type=' + isMatrix + ' Zoom=' + str(zoom)
        filename = filepath + '/ROC_' + isMatrix + ('_zoom' if zoom else '') + '.png'
        tpr = 1 - fnr
        bioDraw.drawRocCurve(curveName, 'FAR', fpr, 'TAR', tpr, filename, zoom, zoom_rates['tp'], zoom_rates['fp'])
        curveName = 'DET Curve\n' + 'Type=' + isMatrix + ' Zoom=' + str(zoom)
        filename = filepath + '/DET_' + isMatrix + ('_zoom' if zoom else '') + '.png'
        bioDraw.drawDetCurve(curveName, 'FAR', fpr, 'FRR', fnr, filename, zoom, zoom_rates['fp'], zoom_rates['fn'])

    def IdentificationCurves(self, isMatrix=bconst.SIMILARITY, mode="any", L=1, filepath="", zoom=False, zoom_rates={'fnfp': 1.0, 'tp': 0.9, 'fp': 0.1}):
        bioIdentification = bi.BioIdentification()
        fpir, fnir, thresholds = bioIdentification.getFPIRFNIR(self.bioProbes, isMatrix, mode, L)
        bioDraw = bd.BioDraw()
        curveName =  'FPIR/FNIR Curve\n' + 'Type=' + isMatrix + ' Mode=' + mode + ' L=' + str(L) + ' Zoom=' + str(zoom)
        filename = filepath + '/FPIRFNIR_' + isMatrix + '_' + mode + '_' + str(L) + ('_zoom' if zoom else '') + '.png'
        bioDraw.drawErrorsOfThresholdCurve(curveName, 'FPIR', fpir, 'FNIR', fnir, thresholds, filename, zoom, zoom_rates['fnfp'])
        curveName = 'ROC Curve\n' + 'Type=' + isMatrix + ' Mode=' + mode + ' L=' + str(L) + ' Zoom=' + str(zoom)
        filename = filepath + '/ROC_' + isMatrix + '_' + mode + '_' + str(L) +  ('_zoom' if zoom else '') + '.png'
        tpir = 1 - fnir
        bioDraw.drawRocCurve(curveName, 'FPIR', fpir, 'TPIR', tpir, filename, zoom, zoom_rates['tp'], zoom_rates['fp'])

bioEstimation = BioEstimation(bconst.PROBES_PATH)

bioEstimation.VerificationCurves(isMatrix=bconst.SIMILARITY, filepath="./output")
bioEstimation.VerificationCurves(isMatrix=bconst.SIMILARITY, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02, 'fn': 0.02})
bioEstimation.VerificationCurves(isMatrix=bconst.DISTANCE, filepath="./output")
bioEstimation.VerificationCurves(isMatrix=bconst.DISTANCE, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02, 'fn': 0.02})

#Ls = [1, 2, 3, 5, 10, 50, 100]
#for L in Ls:
#    bioEstimation.IdentificationCurves(isMatrix=bconst.DISTANCE, mode="any", L=L, filepath="./output")
#    bioEstimation.IdentificationCurves(isMatrix=bconst.DISTANCE, mode="any", L=L, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02})
#    bioEstimation.IdentificationCurves(isMatrix=bconst.DISTANCE, mode="all", L=L, filepath="./output")
#    bioEstimation.IdentificationCurves(isMatrix=bconst.DISTANCE, mode="all", L=L, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02})
#    bioEstimation.IdentificationCurves(isMatrix=bconst.SIMILARITY, mode="any", L=L, filepath="./output")
#    bioEstimation.IdentificationCurves(isMatrix=bconst.SIMILARITY, mode="any", L=L, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02})
#    bioEstimation.IdentificationCurves(isMatrix=bconst.SIMILARITY, mode="all", L=1, filepath="./output")
#    bioEstimation.IdentificationCurves(isMatrix=bconst.SIMILARITY, mode="all", L=1, filepath="./output", zoom=True, zoom_rates={'fnfp': 0.05, 'tp': 0.98, 'fp': 0.02})