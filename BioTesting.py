import numpy

import BioConstants as bconst
import BioInterface as bi
import BioDataset as bds
import BioProbes as bp

from tqdm import tqdm

class BioTesting():
    def __init__(self, datasetPath=bconst.DATASET_PATH):
        self.datasetPath = datasetPath
        self.testPath = "./output/bioTest.save"
        self.bioGallery = bi.BioInterface()
        self.bioSampling = bi.BioInterface()
        self.bioProbes = bp.BioProbes()

    def learn(self, datasetPath):
        bioDataset = bds.BioDataset(datasetPath)
        self.bioGallery.enrolls(bioDataset)

    def addlearn(self, galleryPath, datasetPath):
        self.bioGallery.load(galleryPath)
        bioDataset = bds.BioDataset(datasetPath)
        self.bioGallery.enrolls(bioDataset.dataset)

    def sampling(self):
        self.bioSampling.copy(self.bioGallery)

    def getReal(self, samplePerson, galleryPerson):
        if samplePerson == galleryPerson:
            real = True
        else:
            real = False
        return real

    def testing(self):
        sampleIds, samplePersons, sampleDescriptors = self.bioGallery.getGalleryAsArrays()
        galleryIds, galleryPersons, galleryDescriptors = self.bioSampling.getGalleryAsArrays()
        reals, distances, similarities = [], [], []
        for sampleId in tqdm(sampleIds, desc="Match"):
            samplePerson = samplePersons[sampleId]
            sampleDescriptor = sampleDescriptors[sampleId]
            rs, dists, sims = [], [], []
            for galleryId in galleryIds:
                galleryPerson = galleryPersons[galleryId]
                galleryDescriptor = galleryDescriptors[galleryId]
                real = self.getReal(samplePerson, galleryPerson)
                distance, similarity = self.bioGallery.match(sampleDescriptor, galleryDescriptor)
                rs.append(real)
                dists.append(distance)
                sims.append(similarity)
            reals.append(rs)
            distances.append(dists)
            similarities.append(sims)
        self.bioProbes.replaces(numpy.asarray(sampleIds), numpy.asarray(samplePersons), numpy.asarray(galleryIds), numpy.asarray(galleryPersons), numpy.asarray(reals), numpy.asarray(distances), numpy.asarray(similarities))

    def save(self, probesPath):
        self.bioProbes.save(probesPath)

    def saveAll(self):
        self.bioGallery.save()
        self.bioSampling.save()
        self.save()

    def load(self, probesPath):
        self.bioProbes.load(probesPath)

    def loadAll(self):
        self.bioGallery.load()
        self.bioSampling.load()
        self.load()

bioTesting = BioTesting()

if bioTesting.bioGallery.isSave(bconst.GALLERY_PATH):
    bioTesting.bioGallery.load(bconst.GALLERY_PATH)
else:
    bioTesting.learn(bconst.DATASET_PATH)
    bioTesting.bioGallery.save(bconst.GALLERY_PATH)

if bioTesting.bioSampling.isSave(bconst.SAMPLES_PATH):
    bioTesting.bioSampling.load(bconst.SAMPLES_PATH)
else:
    bioTesting.sampling()
    bioTesting.bioSampling.save(bconst.SAMPLES_PATH)

bioTesting.testing()
bioTesting.save(bconst.PROBES_PATH)
