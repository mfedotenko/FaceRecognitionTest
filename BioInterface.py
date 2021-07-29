import VisionLabs as vl
import BioGallery as bg
import BioConstants as bconst
from tqdm import tqdm

class BioInterface():
    def __init__(self, vendor="VL", model=""):
        self.gallery = bg.bioGallery()
        self.vendor = vendor
        self.model = model
        self.threshold = 0.5
        if self.vendor == "VL":
            self.bioEngine = vl.Luna()
        else:
            self.bioEngine = vl.Luna()

    def imageConvert(self, imagePath):
        convertImage = self.bioEngine.imageConvert(imagePath)
        return convertImage

    def extract(self, imagePath):
        """
        This function represents facial images as vectors.
        :param image: image path or based64 encoded images could be passed.
        :return: Represent function returns a multidimensional vector. The number of dimensions is changing based on the reference model. E.g. FaceNet returns 128 dimensional vector; VGG-Face returns 2622 dimensional vector.
        """
        descriptor = self.bioEngine.extract(imagePath)
        return descriptor

    def match(self, desciptor1, descriptor2):
        return self.bioEngine.match(desciptor1, descriptor2)

    def imageMatch(self, image1, image2):
        descriptor1 = self.extract(image1)
        descriptor2 = self.extract(image2)
        return self.bioEngine.match(descriptor1, descriptor2)

    def enroll(self, person, image):
        descriptor = self.extract(image)
        if descriptor is None: return -1
        self.gallery.add(person, descriptor)
        return 0

    def enrolls(self, bioDataset):
        dataset = bioDataset.dataset
        persons = dataset[bconst.PERSONS]
        images = dataset[bconst.IMAGES]
        for id, person in tqdm(persons.items(), desc="Enrolls"):
        #for i in tqdm(range(len(bioDataset)), desc="Enrolls"):
            image = images[id]
            self.enroll(person, image)
        return 0

    def idenify(self):
        pass

    def verify(self, image1, image2):
        """
        This function verifies an image pair is same person or different persons.
        :param image1: image path or based64 encoded images could be passed.
        :param image2: image path or based64 encoded images could be passed.
        :param distance_metric: cosine, euclidean, euclidean_l2
        :return: Verify function returns a dictionary.
            {
                "verified": True
                , "distance": 0.2563
                , "similarity": 0.9999
            }
        """
        matchResult = self.imageMatch(image1, image2)
        verified = True if matchResult.distance <= self.threshold else False
        return {"verified": verified, "distance": matchResult.distance, "similarity": matchResult.similarity}

    def isSave(self, galleryPath):
        return self.gallery.isSave(galleryPath)

    def save(self, galleryPath):
        self.gallery.save(galleryPath)

    def load(self, galleryPath):
        self.gallery.load(galleryPath)

    def copy(self, bioInterface):
        self.gallery.gallery = bioInterface.gallery.copy()

    def getGalleryAsArrays(self):
        return self.gallery.getGalleryAsArrays()

    def getGalleryAsNumpyArrays(self):
        return self.gallery.getGalleryAsNumpyArrays()
