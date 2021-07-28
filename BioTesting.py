import BioInterface as bi
import BioDataset as bds
import BioSampling as bs
import pickle
from tqdm import tqdm

class BioTesting():
    def __init__(self, datasetPath):
        self.datasetPath = datasetPath
        self.testPath = "./output/bioTest.save"
        self.bioInterface = bi.BioInterface()
        self.bioSampling = bs.BioSampling()
        self.probes = []

    def learn(self, datasetPath):
        bioDataset = bds.BioDataset(datasetPath)
        self.bioInterface.enrolls(bioDataset.dataset)

    def addlearn(self, galleryPath, datasetPath):
        self.bioInterface.load(galleryPath)
        bioDataset = bds.BioDataset(datasetPath)
        self.bioInterface.enrolls(bioDataset.dataset)

    def sampling(self, galleryPath):
        bioSampling = bs.BioSampling()
        bioSampling.loadFromGallery(galleryPath)

    def testing(self):
        samples = self.bioSampling.samples
        gallery = self.bioInterface.export()
        sampleIds = samples[{}]
        samplePersons = []
        galleryIds = []
        galleryPersons = []
        distances = []
        similarities = []

        for sample in tqdm(samples):
            sampleIds.append(sample["id"])
            samplePerson = sample["person"]
            sampleDescriptor = sample["descriptor"]
            dists = []
            sims = []
            for galleryPerson, value in gallery:
                for galleryId, galleryDescriptor in value:
                    result = self.bioInterface.match(sampleDescriptor, galleryDescriptor)
                    dists.append(result.distance)
                    sims.append(result.similarity)
            distances.append(dists)
            similarities.append(sims)

            return numpy.asarray(result_distance), numpy.asarray(result_similarity)

    def save(self, testPath):
        if testPath is None: testPath = self.testPath
        with open(testPath, 'wb') as f:
            pickle.dump(self.probes, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def saveAll(self):
        self.bioInterface.save()
        self.bioSampling.save()
        self.save()

    def load(self, testPath):
        if testPath is None: testPath = self.testPath
        with open(testPath, 'rb') as f:
            self.probes = pickle.load(f)

    def loadAll(self):
        self.bioInterface.load()
        self.bioSampling.load()
        self.load()



bioSampling = BioSampling()
bioSampling.learn(galleryPath, datasetPath)
bioSampling.getSamples(galleryPath)