import pickle

class bioGallery():

    def __init__(self, mode="All"):
        self.lastNum = 0
        self.mode = mode
        # gallery = {"persons": persons, "templates": templates}
        # persons = {id: person}    templates = {id: descriptor}
        self.gallery = {"persons": {}, "templates": {}}
        self.galleryPath = "./output/bioGallery.save"

    def add(self, person, descriptor):
        persons = self.gallery.get("persons")
        templates = self.gallery.get("templates")
        persons.update({self.lastNum: person})
        templates.update({self.lastNum: descriptor})
        self.gallery.update({"persons": persons, "templates": templates})
        self.lastNum += 1

    def adds(self, dataset):
        for data in dataset:
            self.add(data["person"], data["descriptor"])

    def save(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'wb') as f:
            pickle.dump(self.gallery, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def load(self, galleryPath):
        if galleryPath is None: galleryPath = self.galleryPath
        with open(galleryPath, 'rb') as f:
            self.gallery = pickle.load(f)

    def export(self):
        samples = []
        for person, value in self.gallery:
            for id, descriptor in value:
                samples.append({"id": id, "person": person, "descriptor": descriptor})
        return samples

    def getPersonById(self, id):
        return [k for k, v in self.gallery.items() if id in v.keys()][0]