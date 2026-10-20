// lhcview: the stage-3 LHC events (p p -> e+ e-, 13 TeV, MG5 + Pythia 8, HepMC 2) in Geant4's example HepMCEx02 (a
// simplified collider detector with a 3 T solenoid field), shown in the Qt session.  The example's classes with this main
// instead of HepMCEx02.cc, which in interactive mode opens the session without any visualization set up: this one runs
// lhcview.mac (HepMC input, viewer, trajectories, the first event) first and then hands the window to the user.
#include "H02DetectorConstruction.hh"
#include "H02EventAction.hh"
#include "H02PrimaryGeneratorAction.hh"
#include "H02SteppingAction.hh"

#include "FTFP_BERT.hh"
#include "G4RunManagerFactory.hh"
#include "G4UIExecutive.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"

int main(int argc, char** argv)
{
  auto ui = new G4UIExecutive(argc, argv, "qt");
  // as in HepMCEx02.cc: serial (the HepMC reader is not thread-safe), FTFP_BERT, actions after the initialization
  auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::SerialOnly);
  runManager->SetUserInitialization(new H02DetectorConstruction);
  runManager->SetUserInitialization(new FTFP_BERT);
  runManager->Initialize();
  runManager->SetUserAction(new H02PrimaryGeneratorAction);
  runManager->SetUserAction(new H02EventAction);
  runManager->SetUserAction(new H02SteppingAction);
  auto visManager = new G4VisExecutive("warnings");
  visManager->Initialize();
  G4UImanager::GetUIpointer()->ApplyCommand("/control/execute lhcview.mac");
  ui->SessionStart();
  delete ui;
  delete visManager;
  delete runManager;
}
