// fcalview: showers in the ATLAS forward calorimeter of Geant4's example advanced/lAr_calorimeter (its CERN test beam),
// shown in the Qt session.  The example's classes with this main instead of lArCal.cc: serial, initialised, then
// fcalview.mac (viewer on the FCAL, see-through modules, trajectories, the first event) before the window goes to the
// user.  With FCALVIEW_EXPORT=<file.png> set, the view is exported once the window is up and the session then closes
// (run_fcalview.sh --check).
#include "FCALActionInitialization.hh"
#include "FCALTestbeamSetup.hh"

#include "G4PhysListFactory.hh"
#include "G4RunManagerFactory.hh"
#include "G4UIExecutive.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"

#include <QApplication>
#include <QTimer>

#include <cstdlib>

int main(int argc, char** argv)
{
  auto ui = new G4UIExecutive(argc, argv, "qt");
  auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);
  runManager->SetUserInitialization(new FCALTestbeamSetup);
  G4PhysListFactory factory;
  runManager->SetUserInitialization(factory.ReferencePhysList());   // FTFP_BERT unless PHYSLIST is set
  runManager->SetUserInitialization(new FCALActionInitialization);
  runManager->Initialize();
  auto visManager = new G4VisExecutive("warnings");
  visManager->Initialize();
  auto UImanager = G4UImanager::GetUIpointer();
  UImanager->ApplyCommand("/control/execute fcalview.mac");
  if (const char* png = std::getenv("FCALVIEW_EXPORT")) {
    const G4String cmd = G4String("/vis/tsg/export zb_png ") + png;
    QTimer::singleShot(5000, [UImanager, cmd] { UImanager->ApplyCommand(cmd); });
    QTimer::singleShot(8000, [] { QApplication::quit(); });
  }
  ui->SessionStart();
  delete ui;
  delete visManager;
  delete runManager;
}
