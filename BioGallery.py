import pickle
import numpy
import BioConstants as bconst

class bioGallery():

    def __init__(self, mode="All"):
        self.lastNum = 0
        self.mode = mode
        # gallery = {"persons": persons, "descriptors": descriptors}
        # persons = {id: person}    descriptors = {id: descriptor}
        self.gallery = {bconst.DESCRIPTOR_IDS: {}, bconst.DESCRIPTORS: {}}
        self.galleryPath = "./output/bioGallery.save"

    def add(self, person, descriptor):
        persons = self.gallery.get(bconst.PERSONS)
        descriptors = self.gallery.get(bconst.DESCRIPTORS)
        persons.update({self.lastNum: person})
        descriptors.update({self.lastNum: descriptor})
        self.gallery.update({bconst.PERSONS: persons, bconst.DESCRIPTORS: descriptors})
        self.lastNum += 1

    def deleteAll(self):
        self.gallery = {}
        self.lastNum = 0

    def save(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'wb') as f:
            pickle.dump(self.gallery, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def load(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'rb') as f:
            self.gallery = pickle.load(f)

    def getGalleryAsArrays(self):
        ids = persons = descriptors = []
        for id, person in self.gallery[bconst.PERSONS].values():
            ids.append(id)
            persons.append(person)
            descriptors.append(self.gallery[bconst.DESCRIPTORS][id])
        samples = {bconst.DESCRIPTOR_IDS: ids, bconst.PERSONS: persons, bconst.DESCRIPTORS: descriptors}
        return samples

    def getGalleryAsNumpyArrays(self):
        samples = self.getGalleryAsArrays()
        samples = {bconst.DESCRIPTOR_IDS: numpy.asarray(samples[bconst.DESCRIPTOR_IDS]), bconst.PERSONS: numpy.asarray(samples[bconst.PERSONS]), bconst.DESCRIPTORS: numpy.asarray(samples[bconst.DESCRIPTORS])}
        return samples

    def getGalleryAsArray(self):
        samples = []
        for id, person in self.gallery[bconst.PERSONS].values():
            samples.append({bconst.DESCRIPTOR_ID: id, bconst.PERSON: person, bconst.DESCRIPTOR: self.gallery[bconst.DESCRIPTORS][id]})
        return samples

    def getPersonById(self, id):
        # return [k for k, v in self.gallery.items() if id in v.keys()][0]
        pass