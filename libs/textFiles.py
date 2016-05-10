# textFiles.py
# Python class to save the current image file name to text files needed
# for py-faster-rcnn training. i.e trainval.txt, tree_trainval.txt
# Mark Shilton <mark.shilton@gmail.com>
import os.path

class TextFiles(object):
    """Fill in TextFiles"""
    def __init__(self, directory=None):
        self.saveDirectory = None
        self.trainvalFile = "trainval.txt"
        if directory is not None:
            self.saveDirectory = directory


    def addFilenameToTextFiles(self, filenameAndPath=None, itemsFoundInImage=None, listOfAllClasses=None):
        filename = self.extractFilenameWithoutExt(filenameAndPath)

        setOfItemsInImage = set()
        for item in itemsFoundInImage:
            setOfItemsInImage.add(item['label'])

        dictionary = dict()
        for classType in listOfAllClasses:
            if classType in setOfItemsInImage:
                dictionary[classType] = " 1"
            #else:
                #dictionary[classType] = " -1"


        if os.path.isdir(self.saveDirectory):
            for root, dirs, files in os.walk(self.saveDirectory):
                self.searchForTrainvalFile(files, root, filename)
                self.searchForClassTrainvalFiles(files, root, filename, dictionary)

        return

    def extractFilenameWithoutExt(self, filenameAndPath):
        filename = os.path.basename(filenameAndPath)
        filename = os.path.splitext(filename)[0]
        return filename

    def searchForTrainvalFile(self, files, root, filename):
        full_path = os.path.join(root, self.trainvalFile)
        if self.trainvalFile in files:
            self.addFilenameTo(full_path, filename)
        else:
            with open(full_path, 'w') as createNewFile:
                createNewFile.close()
            self.addFilenameTo(full_path, filename)

        return

    def searchForClassTrainvalFiles(self, files, root, filename, labeldict):
        for filePrefix, value in labeldict.iteritems():
            #construct filename from set
            classFilename = filePrefix + "_" + self.trainvalFile
            full_path = os.path.join(root, classFilename)
            if classFilename in files:
                self.addFilenameTo(full_path, filename, value)
            else:
                with open(full_path, 'w') as createNewFile:
                    createNewFile.close()
                self.addFilenameTo(full_path, filename, value)

    def addFilenameTo(self, fileToSaveTo, filename, suffix=None):

        fileFound = self.searchFileForString(fileToSaveTo, filename, suffix)

        if not fileFound:
                self.appendFilenameToFile(fileToSaveTo, filename, suffix)

        self.alphabeticalSortFile(fileToSaveTo)

        return

    def searchFileForString(self, fileToSaveTo, filename, suffix):

        # Search file for filename
        if suffix != None:
            filename = filename + suffix
        fileFound = False
        linesInFile = open(fileToSaveTo).read().splitlines()
        for line in linesInFile:
            if line in filename:
                fileFound = True
        return fileFound

    def appendFilenameToFile(self, fileToSaveTo, filename, suffix=None):

        if suffix != None:
            filename = filename + suffix
        with open(fileToSaveTo, 'a') as appendFile:
            appendFile.write(filename + "\r\n")
            appendFile.close()
        return

    def alphabeticalSortFile(self, pathOfFileToSort):
        # Sort the contents of file into alphabetical order
        with open(pathOfFileToSort, 'r+') as sortFile:
            unsortedLines = sortFile.readlines()
            sortedLines = sorted(unsortedLines)
            sortFile.seek(0)
            sortFile.writelines(sortedLines)
            sortFile.close()
        return
