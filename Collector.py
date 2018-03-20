import os,ROOT

class Collector(object):
    def __init__(self):
        self.objDict = {}
        self.fileDict = {}

    def makeSampleList(self,inputDir):
        self.samples = [n for n in os.listdir(inputDir) if os.path.isdir(os.path.join(inputDir, n))]
    
    def openFiles(self,samples,inputInfo):
        for sample in samples:
            if sample in self.fileDict: continue
            inputPath = inputInfo.outputDir+"/"+sample+"/"+inputInfo.TFileName
            self.fileDict[sample] = ROOT.TFile(inputPath,"READ")
    
    def getObj(self,sample,pathInFile):
        key = "/".join([sample,pathInFile])
        if key not in self.objDict:
            self.objDict[key] = self.fileDict[sample].Get(pathInFile)
        return self.objDict[key]

    def closeFiles(self):
        for fileToClose in self.fileDict.values():
            fileToClose.Close()