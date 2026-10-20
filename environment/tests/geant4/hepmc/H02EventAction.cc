// HepMCEx02 for run_hepmc.sh: instead of printing the muon hits, write every imported primary (one line per particle,
// with its vertex) to primaries.csv, and the number of muon-chamber hits of each event to events.csv.
// If H02_FIELD_EPS is set, the relative accuracy of the field propagation (epsilon min = max) is set to it, and
// DeltaOneStep to it times 1 m (the defaults are 5e-5, 1e-3 and 0.01 mm).  The run is initialised before this
// constructor is called (HepMCEx02.cc), so the global field manager exists.
#include "H02EventAction.hh"

#include "G4Event.hh"
#include "G4FieldManager.hh"
#include "G4HCofThisEvent.hh"
#include "G4PrimaryParticle.hh"
#include "G4PrimaryVertex.hh"
#include "G4SystemOfUnits.hh"
#include "G4TransportationManager.hh"

#include <cstdlib>
#include <fstream>

namespace
{
std::ofstream& primaries()
{
  static std::ofstream f("primaries.csv");
  return f;
}
std::ofstream& events()
{
  static std::ofstream f("events.csv");
  return f;
}
}  // namespace

H02EventAction::H02EventAction() : G4UserEventAction()
{
  primaries().precision(17);
  primaries() << "event,pdg,x_mm,y_mm,z_mm,px_GeV,py_GeV,pz_GeV\n";
  events() << "event,primaries,muon_hits\n";
  if (const char* eps = std::getenv("H02_FIELD_EPS")) {
    const G4double e = std::atof(eps);
    G4FieldManager* fm = G4TransportationManager::GetTransportationManager()->GetFieldManager();
    fm->SetMinimumEpsilonStep(e);
    fm->SetMaximumEpsilonStep(e);
    fm->SetDeltaOneStep(e * m);
    G4cout << "H02EventAction: field propagation with epsilon = " << e << ", DeltaOneStep = " << e * m / mm << " mm"
           << G4endl;
  }
}

H02EventAction::~H02EventAction() {}

void H02EventAction::BeginOfEventAction(const G4Event*) {}

void H02EventAction::EndOfEventAction(const G4Event* anEvent)
{
  G4int n = 0;
  for (G4int i = 0; i < anEvent->GetNumberOfPrimaryVertex(); ++i) {
    const G4PrimaryVertex* v = anEvent->GetPrimaryVertex(i);
    for (const G4PrimaryParticle* p = v->GetPrimary(); p != nullptr; p = p->GetNext(), ++n) {
      primaries() << anEvent->GetEventID() << ',' << p->GetPDGcode() << ',' << v->GetX0() / mm << ','
                  << v->GetY0() / mm << ',' << v->GetZ0() / mm << ',' << p->GetPx() / GeV << ','
                  << p->GetPy() / GeV << ',' << p->GetPz() / GeV << '\n';
    }
  }
  G4HCofThisEvent* hce = anEvent->GetHCofThisEvent();
  G4int hits = (hce != nullptr && hce->GetNumberOfCollections() > 0) ? hce->GetHC(0)->GetSize() : 0;
  events() << anEvent->GetEventID() << ',' << n << ',' << hits << '\n';
}
