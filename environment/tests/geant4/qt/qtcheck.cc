// Qt check of the Geant4 11.4.3 build (run_geant4.sh --qt): example B1's geometry and actions in the Qt session;
// qtcheck.mac opens an OpenGL viewer and a ToolsSG viewer and draws the geometry and 10 events.  Once the window is up,
// timers export each view (qt_ogl.png, qt_tsg.png) and close the session, so the check needs no input.
#include "ActionInitialization.hh"
#include "DetectorConstruction.hh"

#include "G4RunManagerFactory.hh"
#include "G4UIExecutive.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"
#include "QBBC.hh"

#include <QApplication>
#include <QTimer>

#include <vector>

int main(int argc, char** argv)
{
  auto ui = new G4UIExecutive(argc, argv, "qt");
  auto runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);
  runManager->SetUserInitialization(new B1::DetectorConstruction());
  runManager->SetUserInitialization(new QBBC(0));
  runManager->SetUserInitialization(new B1::ActionInitialization());
  auto visManager = new G4VisExecutive("warnings");
  visManager->Initialize();
  auto UImanager = G4UImanager::GetUIpointer();
  UImanager->ApplyCommand("/control/execute qtcheck.mac");
  // once the window is up: redraw each viewer (the 10 kept events) and export it, then close the session
  auto later = [UImanager](int ms, std::vector<G4String> commands) {
    QTimer::singleShot(ms, [UImanager, commands] {
      for (const auto& c : commands) UImanager->ApplyCommand(c);
    });
  };
  later(4000, {"/vis/viewer/select viewer-0", "/vis/viewer/rebuild"});
  later(6000, {"/vis/ogl/export qt_ogl.png"});      // written as qt_ogl_0000.png
  later(7000, {"/vis/viewer/select viewer-1", "/vis/viewer/rebuild"});
  later(9000, {"/vis/tsg/export zb_png qt_tsg.png"});  // format first: zbuffer offscreen to png
  QTimer::singleShot(11000, [] { QApplication::quit(); });
  ui->SessionStart();
  delete ui;
  delete visManager;
  delete runManager;
  G4cout << "qtcheck: session closed" << G4endl;
}
