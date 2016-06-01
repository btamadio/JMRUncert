#!/usr/bin/env python
import ROOT,sys,math,os
from array import array
import argparse
parser = argparse.ArgumentParser(add_help=False, description='Make histograms')
parser.add_argument('inFileName')
parser.add_argument('outFileName')
parser.add_argument('--hist',dest='responseHistFileName',type=str,default='/project/projectdirs/atlas/btamadio/RPV_SUSY/JMRUncert/response.root')
args = parser.parse_args()
os.system('cp '+args.inFileName+' '+args.outFileName)
inFile = ROOT.TFile.Open(args.inFileName,'READ')
histFile = ROOT.TFile.Open(args.responseHistFileName,'READ')
outFile = ROOT.TFile.Open(args.outFileName,'UPDATE')
outFile.cd('outTree')
nomTree = outFile.Get('outTree/nominal')
systTree = nomTree.CloneTree(0)
systTree.SetName('JMR_Smear__1up')
smearedMass = ROOT.std.vector('float')()
systTree.SetBranchAddress('fatjet_m',smearedMass)
rHist = histFile.Get('h_m_responsePt_fit0_width')
r = ROOT.TRandom3(0)
for entry in range(nomTree.GetEntries()):
    smearedMass.clear()
    nomTree.GetEntry(entry)
    for i in range(nomTree.fatjet_pt.size()):
        pt = nomTree.fatjet_pt.at(i)
        if pt > 1800:
            pt = 1800
        if pt < 200:
            pt = 200
        bin = rHist.FindBin(pt)
        width = rHist.GetBinError(bin)
        p = r.Gaus(1,0.66*width)
        newMass = p*nomTree.fatjet_m.at(i)
        smearedMass.push_back(newMass)
        print 'width = %f, p = %f, old mass = %f, new mass = %f' % (width,p,nomTree.fatjet_m.at(i),newMass)
    systTree.Fill()
outFile.Write()
