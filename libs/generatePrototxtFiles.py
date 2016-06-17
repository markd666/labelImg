# Class is responsible for generating prototxt files that describe
# Caffe models. The models files will be altered depending on the number of class.
import os.path
import fileinput
from shutil import copyfile

class GeneratePrototxtFiles(object):
    """docstring for GeneratePrototxtFiles"""
    def __init__(self, prototxtDir):
        self.rootDirectory = prototxtDir
        self.modelsAvailable = ['ZF', 'VGG16']
        self.backgroundClass = 1
        self.totalNumberOfClasses = 0
        self.totalBboxPredictions = 0
        self.trainPrototxtFilename = "train.prototxt"
        self.testPrototxtFilename = "test.prototxt"
        self.fasterRcnnTestFilename = "faster_rcnn_test.pt"
        self.TOTAL_NUMBER_OF_CLASSES = "TOTAL_NUMBER_OF_CLASSES"
        self.TOTAL_NUMBER_OF_BBOX_PREDICTIONS = "TOTAL_NUMBER_OF_BBOX_PREDICTIONS"

        self.filesToChange = [self.trainPrototxtFilename, self.testPrototxtFilename, self.fasterRcnnTestFilename]


    def createPrototxtFiles(self, numberOfClasses):
        self.createModelSubFolders()
        self.totalNumberOfClasses = numberOfClasses + self.backgroundClass
        self.totalBboxPredictions = self.totalNumberOfClasses * 4

        for model in self.modelsAvailable:
            self.alterModelFiles(model)
        return

    def createModelSubFolders(self):
        # check if prototxtDir has model folders already if not create them
        if os.path.isdir(self.rootDirectory):
            for model in self.modelsAvailable:
                modelFilePath = os.path.join(self.rootDirectory, model)
                if not os.path.isdir(modelFilePath):
                    os.mkdir(modelFilePath)
        return

    def alterModelFiles(self, modelName):
        # change train.prototxt
        modelDirectory = os.path.join('./data', modelName)

        for singleFile in self.filesToChange:
            self.alterFile(singleFile, modelDirectory, modelName)

        return

    def alterFile(self, fileToChange, modelBlueprint, modelName):
        fileBlueprint = os.path.join(modelBlueprint, fileToChange)
        newAlteredFile = os.path.join(self.rootDirectory, modelName, fileToChange)

        filedata = None
        with open(fileBlueprint, 'r') as searchFile:
            filedata = searchFile.read()

        filedata = filedata.replace(self.TOTAL_NUMBER_OF_CLASSES, str(self.totalNumberOfClasses))
        filedata = filedata.replace(self.TOTAL_NUMBER_OF_BBOX_PREDICTIONS, str(self.totalBboxPredictions))

        with open(newAlteredFile, 'w') as writeNewFile:
            writeNewFile.write(filedata)

        return
