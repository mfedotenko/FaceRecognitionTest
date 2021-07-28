class BioSample():
    def __init__(self, id=None, person=None, descriptor=None):
        self.id = id
        self.person = person
        self.descriptor = descriptor

class BioData():
    def __init__(self, id=None, person=None, imagePath=None):
        self.id = id
        self.person = person
        self.imagePath = imagePath

class BioTemplate():
    def __init__(self, id=None, descriptor=None):
        self.id = id
        self.descriptor = descriptor

class BioPersonTemplates():
    def __init__(self, person=None, templates=[]):
        self.person = person
        self.templates = templates
    def addTemplate(self, template):
        self.templates.append(template)