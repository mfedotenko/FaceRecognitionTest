import numpy
from tqdm import tqdm

import BioConstants as bconst

class BioIdentification():
    def __init__(self):
        pass

    def getFPIRFNIRScores(self, probeIds, probePersons, galleryIds, galleryPersons, matrix, isMatrix=bconst.SIMILARITY, mode="any", L=1):
        fpirScores = []
        fnirScores = []
        fnirRanks = []
        fnirOtherRanks = []
        for probeId in tqdm(range(len(probeIds))):
            # получаем имя строки
            probePerson = probePersons[probeId]
            probeRow = matrix[probeId]
            # удаляем сравнение с фоткой по которой идет идентификация
            otherId = numpy.where(galleryIds != probeIds[probeId])[0].tolist()
            persons = galleryPersons[otherId]
            probeRow = probeRow[otherId]
            # сортировка по значениям строки таблицы (от лучшего результата к худшему)
            if isMatrix == bconst.DISTANCE:
                sortIds = numpy.argsort(probeRow).tolist()
            else:
                sortIds = numpy.argsort(-probeRow).tolist()
            sortPersons = persons[sortIds]
            sortProbeRow = probeRow[sortIds]
            # находим индексы сравнений в фоткой того же человека
            ownPersonIds = numpy.where(sortPersons == probePerson)[0]
            # находим индексы сравнений в фотками других людей
            otherPersonIds = numpy.where(sortPersons != probePerson)[0]
            # FPIR
            if len(otherPersonIds) > 0:
                otherSortProbeRow = numpy.delete(sortProbeRow, ownPersonIds)
                fpirScore = otherSortProbeRow[0]
                fpirScores.append(fpirScore)
            # FNIR
            if len(ownPersonIds) > 0:
                ownSortProbeRow = numpy.delete(sortProbeRow, otherPersonIds)
                if mode == "all":
                    fnirScoreOwn = ownSortProbeRow[-1] if len(ownSortProbeRow) < L else ownSortProbeRow[L - 1]
                    fnirRankOwn = (numpy.asarray(ownPersonIds)).max() if len(ownSortProbeRow) < L else (numpy.asarray(ownPersonIds))[L - 1]
                    fnirRankOther = (numpy.asarray(otherPersonIds)).min()
                else:
                    fnirScoreOwn = ownSortProbeRow[0]
                    fnirRankOwn = (numpy.asarray(ownPersonIds)).min()
                    fnirRankOther = (numpy.asarray(ownPersonIds)).min()
                fnirScores.append(fnirScoreOwn)
                fnirRanks.append(fnirRankOwn)
                fnirOtherRanks.append(fnirRankOther)
        return numpy.asarray(fpirScores), numpy.asarray(fnirScores), numpy.asarray(fnirRanks), numpy.asarray(fnirOtherRanks)

    def getFPIRFNIR(self, bioProbes, isMatrix=bconst.SIMILARITY, mode="any", L=1):
        probeIds, probePersons, galleryIds, galleryPersons, reals, distances, similarity = bioProbes.get()
        if isMatrix == bconst.DISTANCE:
            matrix = distances
        else:
            matrix = similarity
        fpirScores, fnirScores, fnirRanks, fnirOtherRanks = self.getFPIRFNIRScores(probeIds, probePersons, galleryIds, galleryPersons, matrix, isMatrix=isMatrix, mode=mode, L=L)
        thresholds = numpy.arange(0, max(fpirScores.max(), fnirScores.max()), 0.001)
        thresholds = numpy.sort(numpy.concatenate((thresholds, fpirScores, fnirScores), axis=0))
        fpirLevels = numpy.zeros_like(thresholds)
        fnirLevels = numpy.zeros_like(thresholds)
        if mode == "all":
            bad_ranks = False
        else:
            bad_ranks = (fnirRanks >= L)
        for index, threshold in enumerate(thresholds):
            if isMatrix == bconst.DISTANCE:
                fpirLevels[index] = (fpirScores <= threshold).sum()
                fnirLevels[index] = ((fnirScores > threshold) | bad_ranks).sum()
            else:
                fpirLevels[index] = (fpirScores >= threshold).sum()
                fnirLevels[index] = ((fnirScores < threshold) | bad_ranks).sum()
        fpir = fpirLevels / len(fpirScores)
        fnir = fnirLevels / len(fnirScores)
        return fpir, fnir, thresholds
