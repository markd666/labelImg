# Check to see if each annotation file has a corresponding JPEG file.
# Occassionally when building up training data JPEGs get deleted but the annotation
# file may still exist.
import os.path

class CheckFiles(object):
    """docstring for CheckFiles"""
    def __init__(self, annotationsDir, jpegDir):
        self.annotationsDir = annotationsDir
        self.jpegDir = jpegDir
        self.setOfAnnotationFiles = set()
        self.setOfJpegFiles = set()

        self.parseAnnotationAndJpegFolders()

    def parseAnnotationAndJpegFolders(self):
        for root, dirs, files in os.walk(self.annotationsDir):
            for singleFile in files:
                self.setOfAnnotationFiles.add(self.extractFilenameWithoutExt(singleFile))

        for root, dirs, files in os.walk(self.jpegDir):
            for singleJpegFile in files:
                self.setOfJpegFiles.add(self.extractFilenameWithoutExt(singleJpegFile))

    def checkAnnotationFilesForJpeg(self):
        extraFiles = [x for x in self.setOfAnnotationFiles if x not in self.setOfJpegFiles]
        return extraFiles

    def checkJpegFilesForAnnotation(self):
        extraFiles = [x for x in self.setOfJpegFiles if x not in self.setOfAnnotationFiles]
        return extraFiles

    def extractFilenameWithoutExt(self, filename):
        filename = os.path.splitext(filename)[0]
        return filename
