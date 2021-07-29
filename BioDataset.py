import os
import cv2
import numpy
import base64
from tqdm import tqdm
import BioConstants as bconst

class BioDataset():
    def __init__(self, datasetPath):
        self.datasetPath = datasetPath
        self.lastNum = 0
        # dataset = {"persons": persons, "images": images}
        # persons = {id: person}    images = {id: image}
        self.dataset = {}
        self.loadPersonsWithImagePaths()

    def getmageFromPath(self, path):
        return cv2.imread(path)

    def getImageFromUri(self, uri):
        encodeData = uri.split(',')[1]
        nparr = numpy.fromstring(base64.b64decode(encodeData), numpy.uint8)
        image = cv2.imdecode(nparr)
        return image

    def getImagePaths(self, datasetPath):
        if datasetPath is None: datasetPath = self.datasetPath
        imagePaths = []
        for name1 in os.listdir(datasetPath):
            path = os.path.join(datasetPath, name1)
            for name2 in os.listdir(path):
                d = os.path.join(path, name2)
                for im in os.listdir(d):
                    im = os.path.join(d, im)
                    imagePaths.append(im)
        return imagePaths

    def deleteAll(self):
        self.dataset = {}
        self.lastNum = 0

    def add(self, person, image):
        persons = self.dataset.get(bconst.PERSONS)
        images = self.dataset.get(bconst.IMAGES)
        persons.update({self.lastNum: person})
        images.update({self.lastNum: image})
        self.dataset.update({bconst.PERSONS: persons, bconst.IMAGES: images})
        self.lastNum += 1

    def loadPersonsWithImagePaths(self, datasetPath):
        if datasetPath is None: datasetPath = self.datasetPath
        self.deleteAll()
        imagePaths = self.getImagePaths(datasetPath)
        for i in tqdm(range(len(imagePaths)), desc="getPersonsWithImagePaths"):
            imagePath = imagePaths[i]
            person = imagePath.split('/')[-2]
            self.add(person, imagePath)
