//
//  di-jet invariant mass
//
// usage: root -l Minv.C'("delphes_output.root")'
//

#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#endif

//------------------------------------------------------------------------------

void Minv(const char *inputFile)
{
  gSystem->Load("./MG5_aMC_v2_3_3/Delphes/libDelphes");

  // Create chain of root trees
  TChain chain("Delphes");
  chain.Add(inputFile);

  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();

  // Get pointers to branches used in this analysis
  TClonesArray *branchJet = treeReader->UseBranch("Jet");

  // Book histograms
  TH1 *histMass = new TH1F("mass", "M_{inv}(j_{1}, j_{2})", 100, 0.0, 2000.0);

  // Loop over all events
  for(Int_t entry = 0; entry < numberOfEntries; entry++) {
    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);

    Jet *j1, *j2;

    // If event contains at least 2 jets
    if (branchJet->GetEntries() > 1) {
      // Take first two jets
      j1 = (Jet*) branchJet->At(0);
      j2 = (Jet*) branchJet->At(1);

      // Plot their invariant mass
      histMass->Fill( ((j1->P4()) + (j2->P4())).M() );
    }
  }

  // Show resulting histograms
  histMass->Draw();
}

