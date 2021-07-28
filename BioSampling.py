import BioInterface as bi
import BioDataset as bds
import pickle

galleryPath = "/output/bioGallery.save"
datasetPath = "../dataset_1/"

class BioSampling():
    def __init__(self):
        self.samplesPath = "./output/bioSamples.save"
        # samples = [{"id": id, "person": person, "descriptor": descriptor}]
        self.samples = []

    def add(self, id, person, descriptor):
        self.samples.append({"id": id, "person": person, "descriptor": descriptor})

    def save(self, samplesPath):
        if samplesPath is None: samplesPath = self.samplesPath
        with open(samplesPath, 'wb') as f:
            pickle.dump(self.samples, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def load(self, samplesPath):
        if samplesPath is None: samplesPath = self.samplesPath
        with open(samplesPath, 'rb') as f:
            self.samples = pickle.load(f)

    def loadFromGallery(self, galleryPath):
        self.samples = []
        bioInterface = bi.BioInterface()
        bioInterface.load(galleryPath)
        self.samples = bioInterface.export()

    def loadFromDataset(self, datasetPath):
        self.samples = []
        bioDataset = bds.BioDataset(datasetPath)
        bioInterface = bi.BioInterface()
        for data in bioDataset.dataset:
            descriptor = bioInterface.extract(data["imagePath"])
            self.add(data["id"], data["person"], descriptor)
