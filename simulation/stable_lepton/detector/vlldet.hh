// vlldet: the stable vector-like lepton of ../model/VLL.fr (lv-, lv+) and the rest of the Pythia 8 events in a simplified
// CMS-like barrel detector (Detector.cc): silicon tracker, PbWO4 ECAL and brass-scintillator HCAL in a 3.8 T solenoid, an
// aluminium coil, and four gas muon stations in an iron yoke with a -1.8 T return field.  The events come from a HepMC 2
// file (Events.cc); lv+- get their own Geant4 particles with multiple scattering and ionisation (Physics.cc).  Batch runs
// write the primaries of interest and their tracker and muon-station crossings to a ROOT file (Actions.cc); interactive
// runs show the events one at a time in the Qt session (vlldet.cc, view.mac).
#ifndef VLLDET_HH
#define VLLDET_HH

#include "G4GenericMessenger.hh"
#include "G4ThreeVector.hh"
#include "G4UserEventAction.hh"
#include "G4UserRunAction.hh"
#include "G4UserSteppingAction.hh"
#include "G4UserTrackingAction.hh"
#include "G4VPhysicsConstructor.hh"
#include "G4VSensitiveDetector.hh"
#include "G4VUserActionInitialization.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4VUserPrimaryGeneratorAction.hh"

#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>

// lv- of VLL.fr: PDG code and charge (in units of e); lv+ is -kLVpdg.  The mass is the one of the event file.
constexpr G4int kLVpdg = 9000011;
constexpr G4double kLVcharge = -1.0;

// ---- events (Events.cc)
struct GenParticle {
  G4int pdg;
  G4double px, py, pz, e, m;   // GeV
  G4double x, y, z, t;         // production vertex, mm (t = c t)
  G4int vertex;                // its barcode
};
using GenEvent = std::vector<GenParticle>;   // the final-state particles (status 1)
// all events of a HepMC 2 (IO_GenEvent) file, plain or gzipped, in GeV and mm; lvMass: the mass of lv+- in it (GeV)
std::vector<GenEvent> ReadHepMC(const std::string& path, G4double& lvMass);

class EventAction;

class PrimaryGenerator : public G4VUserPrimaryGeneratorAction {
 public:
  // sequential: events in the order of /vlldet/event (interactive); else the event ID picks the event (batch)
  PrimaryGenerator(const std::vector<GenEvent>* events, EventAction* record, G4bool sequential);
  void GeneratePrimaries(G4Event* event) override;

 private:
  const std::vector<GenEvent>* fEvents;
  EventAction* fRecord;
  G4bool fSequential;
  G4int fNext = 0;
  std::unique_ptr<G4GenericMessenger> fMessenger;
};

// ---- detector (Detector.cc)
class Detector : public G4VUserDetectorConstruction {
 public:
  G4VPhysicalVolume* Construct() override;
  void ConstructSDandField() override;
};

class TrackerSD : public G4VSensitiveDetector {
 public:
  using G4VSensitiveDetector::G4VSensitiveDetector;
  G4bool ProcessHits(G4Step* step, G4TouchableHistory*) override;
};
class MuonSD : public G4VSensitiveDetector {
 public:
  using G4VSensitiveDetector::G4VSensitiveDetector;
  G4bool ProcessHits(G4Step* step, G4TouchableHistory*) override;
};
class CaloSD : public G4VSensitiveDetector {   // ECAL, or the HCAL's scintillator
 public:
  CaloSD(const G4String& name, G4bool hcal) : G4VSensitiveDetector(name), fHcal(hcal) {}
  G4bool ProcessHits(G4Step* step, G4TouchableHistory*) override;

 private:
  G4bool fHcal;
};

// ---- lv+- (Physics.cc)
class LVPhysics : public G4VPhysicsConstructor {
 public:
  explicit LVPhysics(G4double massGeV) : G4VPhysicsConstructor("vll"), fMass(massGeV) {}
  void ConstructParticle() override;
  void ConstructProcess() override;

 private:
  G4double fMass;
};

// ---- run, event and tracking actions (Actions.cc)
struct Prim {             // a primary of interest: lv+-, or charged with pT > 5 GeV
  G4int pdg;
  G4ThreeVector p;        // at production
  G4double e;
  G4ThreeVector end;      // where its track ends (stopped or out of the world)
  G4double endEkin;
};
struct TrackerCrossing {  // a primary of interest in a tracker layer
  G4ThreeVector pos;      // where it enters
  G4double t = 0, p = 0, bg = 0;   // there: time, momentum, beta gamma
  G4double path = 0;      // its path length in the layer
  G4double edep = 0;      // energy deposited by it and its direct secondaries in the layer
  G4bool seen = false;
};
struct MuonCrossing {
  G4ThreeVector pos;
  G4double t = 0, p = 0;
};

class EventAction : public G4UserEventAction {
 public:
  EventAction(G4bool write, G4bool print) : fWrite(write), fPrint(print) {}
  void EndOfEventAction(const G4Event* event) override;
  static EventAction* Current();   // the event action of this thread

  G4int evt = -1;                  // index of the event in the file
  G4int nPrimaries = 0;
  std::map<G4int, Prim> prims;     // by track ID
  std::map<std::pair<G4int, G4int>, TrackerCrossing> tracker;   // by (track ID, layer)
  std::map<std::pair<G4int, G4int>, MuonCrossing> muon;         // by (track ID, station)
  G4double ecal = 0, hcal = 0;     // all energy deposited in the ECAL and in the HCAL's scintillator

 private:
  G4bool fWrite, fPrint;
};

class TrackingAction : public G4UserTrackingAction {
 public:
  // view: keep the (smooth) trajectories of lv+- and of the tracks above fStoreAbove only (/vlldet/storeAbove): a full
  // event's showers have some 10^5 tracks, too many for the viewer's memory
  TrackingAction(EventAction* record, G4bool view);
  void PreUserTrackingAction(const G4Track* track) override;
  void PostUserTrackingAction(const G4Track* track) override;

 private:
  EventAction* fRecord;
  G4bool fView;
  G4double fStoreAbove;
  std::unique_ptr<G4GenericMessenger> fMessenger;
};

// Tracks other than lv+- are killed at a global time of kMaxTime (the slowest lv+- reach the last muon station in about
// 170 ns): in this vacuum-filled detector a soft electron with pz ~ 0 can circle at a tracker layer's surface for ever,
// crossing it without losing its energy and without being taken for a looper by Geant4.  A track still going after
// kMaxSteps steps is printed and killed.
constexpr G4double kMaxTime = 500;   // ns
constexpr G4int kMaxSteps = 20000;
class SteppingAction : public G4UserSteppingAction {
 public:
  void UserSteppingAction(const G4Step* step) override;
};

class RunAction : public G4UserRunAction {
 public:
  explicit RunAction(const G4String& file);
  void BeginOfRunAction(const G4Run*) override;
  void EndOfRunAction(const G4Run*) override;
};

class Actions : public G4VUserActionInitialization {
 public:
  // file: the ROOT file of a batch run; empty for the interactive session (no file, events printed)
  Actions(const std::vector<GenEvent>* events, const G4String& file) : fEvents(events), fFile(file) {}
  void BuildForMaster() const override;
  void Build() const override;

 private:
  const std::vector<GenEvent>* fEvents;
  G4String fFile;
};

#endif
