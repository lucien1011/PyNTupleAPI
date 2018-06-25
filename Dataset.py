from .ComponentList import ComponentList
from .Events import BEvents
from .Events import MultiBEvents
from .FileInfo import FileInfo
import ROOT
import copy

class Dataset(object):
    def __init__(self,name,componentList,isMC=True,sumw=None,xs=None,maxEvents=-1,build_type="TTree",lumi=1.,json=None):
        self.name = name
        self.componentList = componentList
        self.isMC = isMC
        self.isData = not self.isMC
        self.sumw = sumw
        self.xs = xs
        self.fb_to_pb_factor = 1000
        self.maxEvents = maxEvents
        self.build_type = build_type
        self.lumi = lumi
        self.json = json

    def setSumWeight(self,fileName,histPath="SumWeight",inUFTier2=False):
        fileInfo = FileInfo(fileName,inUFTier2)
        fileName = fileInfo.file_path()
        inputFile = ROOT.TFile.Open(fileName,"READ")
        inputHist = inputFile.Get(histPath)
        if self.sumw: print "Overwriting sumw in datast "+self.name
        self.sumw = inputHist.Integral()
        inputFile.Close()

    def makeComponents(self):
        componentList = []
        for icmp,cmp in enumerate(self.componentList):
            tmpCmp = copy.deepcopy(self)
            tmpCmp.componentList = [cmp]
            tmpCmp.name = self.name+"_"+str(icmp)
            tmpCmp.fileName = cmp.fileName
            tmpCmp.treeName = cmp.treeName
            tmpCmp.maxEvents = cmp.maxEvents
            tmpCmp.parent = self
            tmpCmp.fdPaths = cmp.fdPaths
            tmpCmp.fdFiles = cmp.fdFiles
            tmpCmp.fdTrees = cmp.fdTrees
            componentList.append(tmpCmp)
        return componentList 
