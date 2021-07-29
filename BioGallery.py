import pickle

import numpy

import BioConstants as bconst
import copy
import os

class bioGallery():
    def __init__(self, mode="All"):
        self.mode = mode
        # gallery = {"persons": persons, "descriptors": descriptors}
        # persons = {id: person}    descriptors = {id: descriptor}
        self.init()
        self.galleryPath = bconst.GALLERY_PATH

    def init(self):
        self.gallery = {bconst.PERSONS: {}, bconst.DESCRIPTORS: {}}
        self.lastNum = 0

    def add(self, person, descriptor):
        persons = self.gallery.get(bconst.PERSONS)
        descriptors = self.gallery.get(bconst.DESCRIPTORS)
        persons.update({self.lastNum: person})
        descriptors.update({self.lastNum: descriptor})
        self.gallery.update({bconst.PERSONS: persons, bconst.DESCRIPTORS: descriptors})
        self.lastNum += 1

    def isSave(self, galleryPath):
        return os.path.exists(galleryPath)

    def save(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'wb') as f:
            pickle.dump(self.gallery, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'rb') as f:
            self.gallery = pickle.load(f)

    def copy(self):
        return copy.deepcopy(self.gallery)

    def getGalleryAsArrays(self):
        ids = []
        persons = []
        descriptors = []
        for id, person in self.gallery[bconst.PERSONS].items():
            ids.append(id)
            persons.append(person)
            descriptors.append(self.gallery[bconst.DESCRIPTORS][id])
        return ids, persons, descriptors

    def getGalleryAsNumpyArrays(self):
        ids, persons, descriptors = self.getGalleryAsArrays()
        return numpy.asarray(ids), numpy.asarray(persons), numpy.asarray(descriptors)
