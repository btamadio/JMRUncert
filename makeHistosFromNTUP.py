#!/usr/bin/env python
import ROOT,sys,math
from array import array
from profileMaker import profileMaker
import argparse
parser = argparse.ArgumentParser(add_help=False, description='Make histograms')
parser.add_argument('--inputList', dest='use_inputFileList', action='store_true', help='If enabled, will read in a text file containing a list of paths/filenames.')
parser.add_argument('--isData',dest='isData',action='store_true',help='If enabled, will skip calculating denominators.')
parser.add_argument('input')
parser.add_argument('outfilename')
parser.add_argument('run')
args = parser.parse_args()
usePreSel = True
inFileName = args.input
outFileName= args.outfilename
inFileList = []
if not args.use_inputFileList:
    inFileList.append(inFileName)
else:
    with open(inFileName) as fi:
        for line in fi:
            inFileList.append(line.rstrip())
t=ROOT.TChain('outTree/nominal')
for filename in inFileList:
    t.AddFile(filename)

outFile = ROOT.TFile.Open(outFileName,'RECREATE')
h_cutflow = ROOT.TH1F('h_cutflow','h_cutflow',7,0.5,7.5)
h_cutflow.GetXaxis().SetBinLabel(1,'all')
h_cutflow.GetXaxis().SetBinLabel(2,'p_{T}^{lead} > 200 GeV')
h_cutflow.GetXaxis().SetBinLabel(3,'H_{T} > 1 TeV')
h_cutflow.GetXaxis().SetBinLabel(4,'n_{fatjet} >= 5')
h_cutflow.GetXaxis().SetBinLabel(5,'M_{J}^{#Sigma} > 600 GeV')
h_cutflow.GetXaxis().SetBinLabel(6,'M_{J}^{#Sigma} > 700 GeV')
h_cutflow.GetXaxis().SetBinLabel(7,'M_{J}^{#Sigma} > 800 GeV')
h_jet_pt = ROOT.TH1F('h_jet_pt','h_jet_pt',30,0,2000)
h_jet_eta = ROOT.TH1F('h_jet_eta','h_jet_eta',100,-5,5)
h_jet_phi = ROOT.TH1F('h_jet_phi','h_jet_phi',70,-3.5,3.5)
h_jet_E = ROOT.TH1F('h_jet_E','h_jet_E',110,0,2200)
h_nJet = ROOT.TH1F('h_nJet','h_nJet',20,0.5,20.5)

h_fatjet_pt = ROOT.TH1F('h_fatjet_pt','fat jet p_{T} [GeV]',30,0,2000)
h_fatjet_eta = ROOT.TH1F('h_fatjet_eta','fat jet #eta',20,-2,2)
h_fatjet_phi = ROOT.TH1F('h_fatjet_phi','fat jet phi',20,-3.25,3.25)
h_fatjet_m_0 = ROOT.TH1F('h_fatjet_m_0','fat jet mass [GeV]',30,0,250)
h_fatjet_m_1 = ROOT.TH1F('h_fatjet_m_1','fat jet mass [GeV]',30,0,1200)

h_fatjet_m_nsub = [ROOT.TH1F('h_fatjet_m_nsub'+str(i+1),'fat jet mass [GeV]',30,0,250) for i in range(3)]
h_fatjet_m1_nsub = [ROOT.TH1F('h_fatjet_m1_nsub'+str(i+1),'fat jet mass [GeV]',30,0,1200) for i in range(3)]
h_fatjet_pt_nsub = [ROOT.TH1F('h_fatjet_pt_nsub'+str(i+1),'fat jet p_{T} [GeV]',30,0,2000) for i in range(3)]
h_fatjet_split12_nsub = [ROOT.TH1F('h_fatjet_split12_nsub'+str(i+1),'#sqrt{d_{12}} [GeV]',30,0,120) for i in range(3)]
h_fatjet_tau32_nsub = [ROOT.TH1F('h_fatjet_tau32_nsub'+str(i+1),'#tau_{32} WTA',30,0,1.2) for i in range(3)]
h_fatjet_tau21_nsub = [ROOT.TH1F('h_fatjet_tau21_nsub'+str(i+1),'#tau_{21} WTA',30,0,1.2) for i in range(3)]
h_fatjet_C2_nsub = [ROOT.TH1F('h_fatjet_C2_nsub'+str(i+1),'C2',30,0,0.6) for i in range(3)]
h_fatjet_D2_nsub = [ROOT.TH1F('h_fatjet_D2_nsub'+str(i+1),'D2',30,0,8) for i in range(3)]

h_fatjet_split12 = ROOT.TH1F('h_fatjet_split12','#sqrt{d_{12}} [GeV]',30,0,120)
h_fatjet_tau32 = ROOT.TH1F('h_fatjet_tau32','#tau_{32} WTA',30,0,1.2)
h_fatjet_tau21 = ROOT.TH1F('h_fatjet_tau21','#tau_{21} WTA',30,0,1.2)
h_fatjet_C2 = ROOT.TH1F('h_fatjet_C2','fat jet C2',30,0,0.6)
h_fatjet_D2 = ROOT.TH1F('h_fatjet_D2','fat jet D2',30,0,8)
h_fatjet_NTrimSubjets = ROOT.TH1F('h_fatjet_NTrimSubjets','# subjets',6,0.5,6.5)

responseBinsM = [0,50,100,150,200,300,400,500,600,1500]
responseBinsPt = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,2700]
responseBinsNsub = [0.5,1.5,2.5,3.5,4.5,5.5]

h_m_responseM = ROOT.TH2D('h_m_responseM','mass response profile',len(responseBinsM)-1,array('d',responseBinsM),1000,0,5)
h_m_responsePt = ROOT.TH2D('h_m_responsePt','mass response vs. pT',len(responseBinsPt)-1,array('d',responseBinsPt),1000,0,5)

h_m_responsePt_nsub = [ROOT.TH2D('h_m_responsePt_nsub'+str(i+1),'mass response vs. pT',len(responseBinsPt)-1,array('d',responseBinsPt),1000,0,5) for i in range(3)]
h_m_responseM_nsub = [ROOT.TH2D('h_m_responseM'+str(i+1),'mass response profile',len(responseBinsM)-1,array('d',responseBinsM),1000,0,5) for i in range(3)]

h_m_response1D = ROOT.TH1D('h_m_response1D','Mass response',1000,0,5)

h_m_responseEta = ROOT.TH2D('h_m_responseEta','mass response vs. Eta',30,-5,5,100,0,5)
h_m_responseNsub = ROOT.TH2D('h_m_responseNsub','mass response vs. n_{subjets}',5,0.5,5.5,1000,0,5)

h_m_reco_v_truth = ROOT.TH2D('h_m_reco_v_truth','reco vs. truth mass',50,0,500,50,0,500)
h_deltaR = ROOT.TH1D('h_deltaR','#DeltaR(reco,truth)',100,0,1)
h_nFatJet = ROOT.TH1F('h_nFatJet','h_nFatJet',20,0.5,20.5)
h_ht = ROOT.TH1F('h_ht','h_ht',700,0,7000)
h_mj = ROOT.TH1F('h_mj','h_mj',250,0,2500)

nEntries = t.GetEntries()

htCut = 0.0
jetPtCut = 0.0
fatJetPtCut = 0.0
jetEtaCut = 5.0
fatJetEtaCut = 5.0
leadJetPtCut = 0.0

if usePreSel:
    htCut = 0.0
    jetPtCut = 50.0
    fatJetPtCut = 200.0
    jetEtaCut = 2.8
    fatJetEtaCut = 2.0
    leadJetPtCut = 0.0

for entry in range(nEntries):
    t.GetEntry(entry)
    passLeadJet = False
    ht = 0.0
    mj = 0.0
    nJet = 0
    nFatJet = 0
    iCut = 1
    w=t.mcEventWeight
    for i in range(t.jet_pt.size()):
        if abs(t.jet_eta.at(i)) < jetEtaCut:
            if t.jet_pt.at(i) > leadJetPtCut:
                passLeadJet = True
            if t.jet_pt.at(i) > jetPtCut:
                ht+=t.jet_pt.at(i)
                nJet+=1
    for i in range(t.fatjet_pt.size()):
        if abs(t.fatjet_eta.at(i)) < fatJetEtaCut and t.fatjet_pt.at(i) > fatJetPtCut:
            nFatJet+=1
            if nFatJet <= 4:
                mj+=t.fatjet_m.at(i)
    h_cutflow.Fill(iCut,w)
    iCut+=1
    if passLeadJet:
        h_cutflow.Fill(iCut,w)
        iCut+=1
    if passLeadJet and ht > htCut:
        h_cutflow.Fill(iCut,w)
        iCut+=1
        h_nJet.Fill(nJet,w)
        h_nFatJet.Fill(nFatJet,w)
        h_mj.Fill(mj,w)
        if nFatJet >= 5:
            h_cutflow.Fill(iCut,w)
            iCut+=1
            if mj > 600:
                h_cutflow.Fill(iCut,w)
                iCut+=1
                if mj > 700:
                    h_cutflow.Fill(iCut,w)
                    iCut+=1
                    if mj > 800:
                        h_cutflow.Fill(iCut,w)
                        iCut+=1
        h_ht.Fill(ht,w)
        for i in range(t.jet_pt.size()):
            if abs(t.jet_eta.at(i)) < jetEtaCut and t.jet_pt.at(i) > jetPtCut:
                h_jet_pt.Fill(t.jet_pt.at(i),w)
                h_jet_eta.Fill(t.jet_eta.at(i),w)
                h_jet_phi.Fill(t.jet_phi.at(i),w)
                h_jet_E.Fill(t.jet_E.at(i),w)
        for i in range(t.fatjet_pt.size()):
            if abs(t.fatjet_eta.at(i)) < fatJetEtaCut and t.fatjet_pt.at(i) > fatJetPtCut:
                h_fatjet_pt.Fill(t.fatjet_pt.at(i),w)
                h_fatjet_eta.Fill(t.fatjet_eta.at(i),w)
                h_fatjet_phi.Fill(t.fatjet_phi.at(i),w)
                h_fatjet_m_0.Fill(t.fatjet_m.at(i),w)
                h_fatjet_m_1.Fill(t.fatjet_m.at(i),w)
                
                h_fatjet_split12.Fill(t.fatjet_split12.at(i),w)
                h_fatjet_tau32.Fill(t.fatjet_tau32_wta.at(i),w)
                h_fatjet_tau21.Fill(t.fatjet_tau21_wta.at(i),w)
                h_fatjet_D2.Fill(t.fatjet_D2.at(i),w)
                h_fatjet_C2.Fill(t.fatjet_C2.at(i),w)
                h_fatjet_NTrimSubjets.Fill(t.fatjet_NTrimSubjets.at(i),w)

                h_fatjet_m_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_m.at(i),w)
                h_fatjet_m1_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_m.at(i),w)
                
                h_fatjet_pt_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_pt.at(i),w)
                h_fatjet_split12_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_split12.at(i),w)
                h_fatjet_tau32_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_tau32_wta.at(i),w)
                h_fatjet_tau21_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_tau21_wta.at(i),w)
                h_fatjet_C2_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_C2.at(i),w)
                h_fatjet_D2_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(t.fatjet_D2.at(i),w)

                deltaR = []
                mTruthList = []
                #find matching truth fat jet:
                for j in range(t.truthJet_pt.size()):
                    dR = (t.fatjet_eta.at(i)-t.truthJet_eta.at(j))*(t.fatjet_eta.at(i)-t.truthJet_eta.at(j))
                    dR = (t.fatjet_phi.at(i)-t.truthJet_phi.at(j))*(t.fatjet_phi.at(i)-t.truthJet_phi.at(j))
                    dR = math.sqrt(dR)
                    deltaR.append(dR)
                    mTruthList.append(t.truthJet_m.at(j))
                if len(deltaR) > 0 and min(deltaR) < 0.2:
                    j = deltaR.index(min(deltaR))
                    mTruth = t.truthJet_m.at(j)
                    ptTruth = t.truthJet_pt.at(j)
                    etaTruth = t.truthJet_eta.at(j)
                    if mTruth > 0:
                        h_deltaR.Fill(min(deltaR),w)
                        h_m_responseM.Fill(mTruth,t.fatjet_m.at(i)/mTruth,w)
                        h_m_response1D.Fill(t.fatjet_m.at(i)/mTruth,w)
                        h_m_responsePt.Fill(t.fatjet_pt.at(i),t.fatjet_m.at(i)/mTruth,w)
                        h_m_responsePt_nsub[min(2,t.fatjet_NTrimSubjets.at(i)-1)].Fill(ptTruth,t.fatjet_m.at(i)/mTruth,w)
                        h_m_responseEta.Fill(etaTruth,t.fatjet_m.at(i)/mTruth,w)
                        h_m_reco_v_truth.Fill(mTruth,t.fatjet_m.at(i),w)

pp0 = profileMaker(h_m_responsePt,'h_m_responsePt_fit0')
(prof_pt0_err,prof_pt0_width,c_pt0) = pp0.getResponseFits()
c_pt0.Print('responsePt_fit0_'+args.run+'.pdf')

pp1 = profileMaker(h_m_responsePt_nsub[0],'h_m_responsePt_fit1')
(prof_pt1_err,prof_pt1_width,c_pt1) = pp1.getResponseFits()
c_pt1.Print('responsePt_fit1_'+args.run+'.pdf')

pp2 = profileMaker(h_m_responsePt_nsub[1],'h_m_responsePt_fit2')
(prof_pt2_err,prof_pt2_width,c_pt2) = pp2.getResponseFits()
c_pt2.Print('responsePt_fit2_'+args.run+'.pdf')

pp3 = profileMaker(h_m_responsePt_nsub[2],'h_m_responsePt_fit3')
(prof_pt3_err,prof_pt3_width,c_pt3) = pp3.getResponseFits()
c_pt3.Print('responsePt_fit3_'+args.run+'.pdf')

outFile.Write()
outFile.Close()
