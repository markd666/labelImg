# generateTestFiles.py
# Python class to generate the necessary test.txt / tree_test.txt / etc files.
# Class will scan through correspondng trainval.txt / tree_train.txt file, select
# and copy 5 percent of the entries.
import os.path
import math
import numpy as np

class GenerateTestFiles(object):
    """docstring for GenerateTestFiles"""
    def __init__(self, directory=None):
        self.saveDirectory=None
        self.trainvalFile = "trainval.txt"
        self.trainval = "trainval"
        self.testFile = "test.txt"
        if directory is not None:
            self.saveDirectory = directory


    def createNewTestFiles(self):

        labelSet = self.findAllTrainvalFileTypes()

        for singleFilePath in set(labelSet):
            linesToSample = self.findLineNumbersToSample(singleFilePath)

            sampledLines = self.extractSampleContent(singleFilePath, linesToSample)

            self.saveSamplesToTestFiles(singleFilePath, sampledLines)

            self.deleteSampledContent(singleFilePath, linesToSample)

        return

    def findAllTrainvalFileTypes(self):
        labelSetPaths = set()
        if os.path.isdir(self.saveDirectory):
            for root, dirs, files in os.walk(self.saveDirectory):
                for singleFile in files:
                    if self.trainvalFile in singleFile:
                        singleFilePath = os.path.join(root, singleFile)
                        labelSetPaths.add(singleFilePath)
        return labelSetPaths


    def extractFilenameWithoutExt(self, filenameAndPath):
        filename = os.path.basename(filenameAndPath)
        filename = os.path.splitext(filename)[0]
        return filename

    def findLineNumbersToSample(self, singleFilePath=None):
        sortedSetOfLinesToSample = set()
        linesInFile =  self.fileLength(singleFilePath)
        if linesInFile >= 10:
            numberOfTestImagesNeeded = int(math.ceil(0.05 * linesInFile))
            selectedLinesToSample = np.random.choice(linesInFile, numberOfTestImagesNeeded)
            sortedSetOfLinesToSample =  sorted(set(selectedLinesToSample))
        else:
            numberOfTestImagesNeeded = 0

        return sortedSetOfLinesToSample

    def fileLength(self, filename):
        with open(filename) as f:
            for lines, l in enumerate(f):
                pass
        return lines + 1

    def extractSampleContent(self, filenameToSampleFrom=None, linesToSample=None):
        sampledLinesContent = []
        with open(filenameToSampleFrom) as trainvalFile:
            for i, line in enumerate(trainvalFile):
                for lineSampleNumber in linesToSample:
                    if i == lineSampleNumber:
                        sampledLinesContent.append(line)

        return sampledLinesContent

    def deleteSampledContent(self, filenameToSampleFrom=None, linesToSample=None):
        allLinesInFile = []
        with open(filenameToSampleFrom, "r") as trainvalFile:
            allLinesInFile = trainvalFile.readlines()
            trainvalFile.close()

        updatedListOfLines = []
        for lineNumber, lineContent in enumerate(allLinesInFile):
            lineSampleFound = False
            for lineSampleNumber in linesToSample:
                if lineNumber == lineSampleNumber:
                    lineSampleFound = True

            if not lineSampleFound:
                updatedListOfLines.append(lineContent)

        with open(filenameToSampleFrom, "w") as newTrainvalFile:
            newTrainvalFile.writelines(updatedListOfLines)

    def saveSamplesToTestFiles(self, singleFilePath=None, sampledLines=None):
        testFileToWriteSampleTo = ""
        if singleFilePath.endswith("_" + self.trainvalFile):
            singleFileName = singleFilePath[:-13]
            testFileToWriteSampleTo = singleFileName + "_test.txt"
        elif singleFilePath.endswith(self.trainvalFile):
            singleFileName = singleFilePath[:-12]
            testFileToWriteSampleTo = singleFileName + self.testFile

        with open(testFileToWriteSampleTo, "w") as testFile:
            testFile.writelines(sampledLines)
            testFile.close()
        return
