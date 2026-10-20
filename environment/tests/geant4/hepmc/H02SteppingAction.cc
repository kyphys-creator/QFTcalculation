// HepMCEx02 for run_hepmc.sh: the example's stepping action (secondaries other than muons are killed in the
// calorimeters), plus one line in calo_entry.csv where a primary e+- crosses from the hall into the barrel
// calorimeter (r = 2 m): its momentum at the vertex (from the primary) and its position and momentum at the entry.
#include "H02SteppingAction.hh"

#include "G4DynamicParticle.hh"
#include "G4Event.hh"
#include "G4EventManager.hh"
#include "G4MuonMinus.hh"
#include "G4MuonPlus.hh"
#include "G4PrimaryParticle.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4Track.hh"
#include "G4VPhysicalVolume.hh"

#include <cstdlib>
#include <fstream>

namespace
{
std::ofstream& entries()
{
  static std::ofstream f("calo_entry.csv");
  return f;
}
}  // namespace

H02SteppingAction::H02SteppingAction() : G4UserSteppingAction()
{
  entries().precision(17);
  entries() << "event,track,pdg,px0_GeV,py0_GeV,pz0_GeV,x_mm,y_mm,z_mm,px_GeV,py_GeV,pz_GeV\n";
}

H02SteppingAction::~H02SteppingAction() {}

void H02SteppingAction::UserSteppingAction(const G4Step* astep)
{
  G4Track* atrack = astep->GetTrack();

  const G4StepPoint* post = astep->GetPostStepPoint();
  const G4PrimaryParticle* primary = atrack->GetDynamicParticle()->GetPrimaryParticle();
  if (atrack->GetParentID() == 0 && primary != nullptr
      && std::abs(atrack->GetDefinition()->GetPDGEncoding()) == 11
      && post->GetStepStatus() == fGeomBoundary && post->GetPhysicalVolume() != nullptr
      && post->GetPhysicalVolume()->GetName() == "BARREL_CAL_PV"
      && astep->GetPreStepPoint()->GetPhysicalVolume()->GetName() == "EXP_HALL_PV")
  {
    const G4ThreeVector x = post->GetPosition();
    const G4ThreeVector p = post->GetMomentum();
    entries() << G4EventManager::GetEventManager()->GetConstCurrentEvent()->GetEventID() << ','
              << atrack->GetTrackID() << ',' << atrack->GetDefinition()->GetPDGEncoding() << ','
              << primary->GetPx() / GeV << ',' << primary->GetPy() / GeV << ',' << primary->GetPz() / GeV
              << ',' << x.x() / mm << ',' << x.y() / mm << ',' << x.z() / mm << ',' << p.x() / GeV << ','
              << p.y() / GeV << ',' << p.z() / GeV << '\n';
  }

  // the example's own action
  if (atrack->GetTrackStatus() != fAlive) return;
  if (atrack->GetParentID() == 0) return;
  G4ParticleDefinition* particleType = atrack->GetDefinition();
  if ((particleType == G4MuonPlus::MuonPlusDefinition())
      || (particleType == G4MuonMinus::MuonMinusDefinition()))
    return;
  G4String pvname = astep->GetPreStepPoint()->GetPhysicalVolume()->GetName();
  if (pvname == "BARREL_CAL_PV" || pvname == "ENDCAP_CAL_PV") {
    atrack->SetTrackStatus(fKillTrackAndSecondaries);
  }
}
