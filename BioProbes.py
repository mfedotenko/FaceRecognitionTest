import BioConstants as bconst
import pickle
import numpy

class BioProbes():
    def __init__(self):
        self.probesPath = ""
        self.init()

    def init(self):
        self.probes = {bconst.SAMPLE_IDS: numpy.array([]), bconst.SAMPLE_PERSONS: numpy.array([]), bconst.GALLERY_IDS: numpy.array([]), bconst.GALLERY_PERSONS: numpy.array([]), bconst.REALS: numpy.array([]), bconst.DISTANCES: numpy.array([]), bconst.SIMILARITIES: numpy.array([])}

    def replaces(self, sampleIds, samplePersons, galleryIds, galleryPersons, reals, distances, similarities):
        self.probes = {bconst.SAMPLE_IDS: sampleIds, bconst.SAMPLE_PERSONS: samplePersons, bconst.GALLERY_IDS: galleryIds, bconst.GALLERY_PERSONS: galleryPersons, bconst.REALS: reals, bconst.DISTANCES: distances, bconst.SIMILARITIES: similarities}

    def save(self, probesPath):
        if probesPath is None: probesPath = self.probesPath
        with open(probesPath, 'wb') as f:
            pickle.dump(self.probes, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, probesPath):
        if probesPath is None: probesPath = self.probesPath
        with open(probesPath, 'rb') as f:
            self.probes = pickle.load(f)

    def get(self):
        sampleIds = self.probes.get(bconst.SAMPLE_IDS)
        samplePersons = self.probes.get(bconst.SAMPLE_PERSONS)
        galleryIds = self.probes.get(bconst.GALLERY_IDS)
        galleryPersons = self.probes.get(bconst.GALLERY_PERSONS)
        reals = self.probes.get(bconst.REALS)
        distances = self.probes.get(bconst.DISTANCES)
        similarities = self.probes.get(bconst.SIMILARITIES)
        return sampleIds, samplePersons, galleryIds, galleryPersons, reals, distances, similarities
