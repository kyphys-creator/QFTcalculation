// vlldet (vlldet.hh): the Pythia 8 events of p p -> lv+ lv- in the simplified barrel detector.
//   vlldet <events.hepmc[.gz]> --batch <file.root> [--threads N] [--nevents N] [--macro file.mac]
//       all events of the file (or the first N), multithreaded, ntuples to <file.root> (Actions.cc); the macro, if
//       given, runs after the initialisation (verbosity, seeds)
//   vlldet <events.hepmc[.gz]>
//       the Qt session, serial: runs view.mac of the working directory, then hands the window to the user.  With
//       VLLDET_OFFSCREEN set there is no window and no session: view.mac then opens TSG_OFFSCREEN (run_view.sh --check).
// The mass of lv+- is taken from the event file.  Physics: FTFP_BERT with lv+- added (Physics.cc).
#include "vlldet.hh"

#include "FTFP_BERT.hh"
#include "G4RunManagerFactory.hh"
#include "G4SystemOfUnits.hh"
#include "G4UIExecutive.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"

#include <cstdlib>
#include <string>

int main(int argc, char** argv)
{
  if (argc < 2) {
    G4cerr << "usage: vlldet <events.hepmc[.gz]> [--batch <file.root> [--threads N] [--nevents N] [--macro file.mac]]"
           << G4endl;
    return 1;
  }
  G4String file, macro;
  G4int threads = 6, nevents = -1;
  for (G4int i = 2; i + 1 < argc; i += 2) {
    const std::string a = argv[i];
    if (a == "--batch") file = argv[i + 1];
    else if (a == "--threads") threads = std::atoi(argv[i + 1]);
    else if (a == "--nevents") nevents = std::atoi(argv[i + 1]);
    else if (a == "--macro") macro = argv[i + 1];
  }
  G4double lvMass = 0;
  const auto events = ReadHepMC(argv[1], lvMass);
  if (events.empty() || lvMass <= 0) {
    G4cerr << argv[1] << ": no events, or no lv+- in them" << G4endl;
    return 1;
  }
  G4cout << argv[1] << ": " << events.size() << " events, lv+- mass " << lvMass << " GeV" << G4endl;
  const G4bool batch = !file.empty();
  if (nevents < 0 || nevents > static_cast<G4int>(events.size())) nevents = events.size();

  G4UIExecutive* ui = batch || std::getenv("VLLDET_OFFSCREEN") ? nullptr : new G4UIExecutive(1, argv, "qt");
  auto runManager = G4RunManagerFactory::CreateRunManager(batch ? G4RunManagerType::Default : G4RunManagerType::SerialOnly);
  if (batch) runManager->SetNumberOfThreads(threads);
  runManager->SetUserInitialization(new Detector);
  auto physics = new FTFP_BERT(0);
  physics->RegisterPhysics(new LVPhysics(lvMass));
  runManager->SetUserInitialization(physics);
  runManager->SetUserInitialization(new Actions(&events, file));
  runManager->Initialize();
  auto UImanager = G4UImanager::GetUIpointer();

  if (batch) {
    UImanager->ApplyCommand("/run/printProgress " + std::to_string(std::max(1, nevents / 20)));
    if (!macro.empty()) UImanager->ApplyCommand("/control/execute " + macro);
    runManager->BeamOn(nevents);
    delete runManager;
    return 0;
  }
  auto visManager = new G4VisExecutive("warnings");
  visManager->Initialize();
  UImanager->ApplyCommand("/control/execute view.mac");
  if (ui) ui->SessionStart();
  delete ui;
  delete visManager;
  delete runManager;
}
