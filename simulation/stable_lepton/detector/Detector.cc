// A simplified CMS-like barrel detector (lengths in mm), all cylinders about the beam (z) axis:
//   solenoid volume  r < 2980, |z| < 3000, uniform 3.8 T along +z, holding
//     beam pipe      Be, r 22.5-23.3
//     tracker        12 silicon layers, 0.3 thick, |z| < 2500, at r = 30 ... 1050 (copy number = layer 0-11)
//     ECAL           PbWO4, r 1290-1520 (25.8 X0), |z| < 3000
//     HCAL           brass (Cu 70 Zn 30), r 1770-2950, |z| < 3000, with 20 layers of 4 mm plastic scintillator every 59
//   coil             Al, r 3000-3300, |z| < 3000, no field
//   muon system      |z| < 6500: four Ar/CO2 (80/20) stations, 100 thick, at r = 4000, 4800, 5930, 7060 (copy number =
//                    station 0-3), and three iron layers between them (4300-4600, 5100-5730, 6230-6860), -1.8 T along z
// No endcaps: the barrel covers about |eta| < 1.2 up to the muon stations.  The rest is vacuum.
#include "vlldet.hh"

#include "G4AutoDelete.hh"
#include "G4FieldManager.hh"
#include "G4LogicalVolume.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4Material.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4SDManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4UniformMagField.hh"

namespace {
const G4double kTrackerR[12] = {30, 70, 110, 160, 250, 340, 430, 520, 610, 750, 900, 1050};
const G4double kStationR[4] = {4000, 4800, 5930, 7060};
const G4double kIron[3][2] = {{4300, 4600}, {5100, 5730}, {6230, 6860}};

G4LogicalVolume* Tube(const G4String& name, G4double rmin, G4double rmax, G4double hz, G4Material* mat)
{
  return new G4LogicalVolume(new G4Tubs(name, rmin * mm, rmax * mm, hz * mm, 0, 360 * deg), mat, name);
}
void Place(G4LogicalVolume* lv, G4LogicalVolume* mother, G4int copy = 0)
{
  new G4PVPlacement(nullptr, G4ThreeVector(), lv, lv->GetName(), mother, false, copy, true);
}
}  // namespace

G4VPhysicalVolume* Detector::Construct()
{
  auto nist = G4NistManager::Instance();
  auto vacuum = nist->FindOrBuildMaterial("G4_Galactic");
  auto brass = new G4Material("Brass", 8.53 * g / cm3, 2);
  brass->AddElement(nist->FindOrBuildElement("Cu"), 0.70);
  brass->AddElement(nist->FindOrBuildElement("Zn"), 0.30);
  auto gas = new G4Material("ArCO2", 1.82 * mg / cm3, 2, kStateGas);
  gas->AddMaterial(nist->FindOrBuildMaterial("G4_Ar"), 0.8 * 1.784 / (0.8 * 1.784 + 0.2 * 1.977));
  gas->AddMaterial(nist->FindOrBuildMaterial("G4_CARBON_DIOXIDE"), 0.2 * 1.977 / (0.8 * 1.784 + 0.2 * 1.977));

  auto world = new G4LogicalVolume(new G4Box("World", 7.5 * m, 7.5 * m, 7.0 * m), vacuum, "World");
  auto worldPV = new G4PVPlacement(nullptr, G4ThreeVector(), world, "World", nullptr, false, 0, true);

  auto solenoid = Tube("Solenoid", 0, 2980, 3000, vacuum);
  Place(solenoid, world);
  Place(Tube("BeamPipe", 22.5, 23.3, 3000, nist->FindOrBuildMaterial("G4_Be")), solenoid);
  auto si = nist->FindOrBuildMaterial("G4_Si");
  for (G4int i = 0; i < 12; ++i)
    Place(Tube("TrackerLayer", kTrackerR[i], kTrackerR[i] + 0.3, 2500, si), solenoid, i);
  Place(Tube("ECAL", 1290, 1520, 3000, nist->FindOrBuildMaterial("G4_PbWO4")), solenoid);
  auto hcal = Tube("HCAL", 1770, 2950, 3000, brass);
  Place(hcal, solenoid);
  auto scint = nist->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
  for (G4int i = 0; i < 20; ++i) {
    const G4double r = 1770 + 59 * i + 55;
    Place(Tube("HCALScint", r, r + 4, 3000, scint), hcal, i);
  }
  Place(Tube("Coil", 3000, 3300, 3000, nist->FindOrBuildMaterial("G4_Al")), world);
  for (G4int i = 0; i < 4; ++i) Place(Tube("MuonStation", kStationR[i], kStationR[i] + 100, 6500, gas), world, i);
  auto iron = nist->FindOrBuildMaterial("G4_Fe");
  for (G4int i = 0; i < 3; ++i) Place(Tube("YokeIron", kIron[i][0], kIron[i][1], 6500, iron), world, i);
  return worldPV;
}

void Detector::ConstructSDandField()
{
  auto sdm = G4SDManager::GetSDMpointer();
  auto tracker = new TrackerSD("Tracker");
  auto muon = new MuonSD("Muon");
  auto ecal = new CaloSD("ECALSD", false);
  auto hcal = new CaloSD("HCALSD", true);
  for (auto sd : std::vector<G4VSensitiveDetector*>{tracker, muon, ecal, hcal}) sdm->AddNewDetector(sd);
  SetSensitiveDetector("TrackerLayer", tracker, true);
  SetSensitiveDetector("MuonStation", muon, true);
  SetSensitiveDetector("ECAL", ecal);
  SetSensitiveDetector("HCALScint", hcal, true);

  // the fields: per thread; the fields go to Geant4's auto-delete, the field managers to its G4FieldManagerStore
  auto inner = new G4UniformMagField(G4ThreeVector(0, 0, 3.8 * tesla));
  auto innerFM = new G4FieldManager(inner);
  innerFM->CreateChordFinder(inner);
  G4AutoDelete::Register(inner);
  auto yoke = new G4UniformMagField(G4ThreeVector(0, 0, -1.8 * tesla));
  auto yokeFM = new G4FieldManager(yoke);
  yokeFM->CreateChordFinder(yoke);
  G4AutoDelete::Register(yoke);
  for (auto lv : *G4LogicalVolumeStore::GetInstance()) {
    if (lv->GetName() == "Solenoid") lv->SetFieldManager(innerFM, true);
    if (lv->GetName() == "YokeIron") lv->SetFieldManager(yokeFM, true);
  }
}

// ---- sensitive detectors: they fill this thread's event record (EventAction)
G4bool TrackerSD::ProcessHits(G4Step* step, G4TouchableHistory*)
{
  auto rec = EventAction::Current();
  const auto track = step->GetTrack();
  const G4int id = track->GetTrackID();
  // the primaries of interest, and their direct secondaries (delta electrons) for the energy deposit
  G4int owner = 0;
  if (rec->prims.count(id)) owner = id;
  else if (rec->prims.count(track->GetParentID())) owner = track->GetParentID();
  if (!owner) return false;
  const auto pre = step->GetPreStepPoint();
  auto& c = rec->tracker[{owner, pre->GetTouchable()->GetCopyNumber()}];
  c.edep += step->GetTotalEnergyDeposit();
  if (id == owner) {
    c.path += step->GetStepLength();
    if (!c.seen) {
      c.seen = true;
      c.pos = pre->GetPosition();
      c.t = pre->GetGlobalTime();
      c.p = pre->GetMomentum().mag();
      c.bg = c.p / track->GetDefinition()->GetPDGMass();
    }
  }
  return true;
}

G4bool MuonSD::ProcessHits(G4Step* step, G4TouchableHistory*)
{
  auto rec = EventAction::Current();
  const G4int id = step->GetTrack()->GetTrackID();
  if (!rec->prims.count(id)) return false;
  const auto pre = step->GetPreStepPoint();
  const auto key = std::make_pair(id, pre->GetTouchable()->GetCopyNumber());
  if (rec->muon.count(key)) return false;
  rec->muon[key] = {pre->GetPosition(), pre->GetGlobalTime(), pre->GetMomentum().mag()};
  return true;
}

G4bool CaloSD::ProcessHits(G4Step* step, G4TouchableHistory*)
{
  auto rec = EventAction::Current();
  (fHcal ? rec->hcal : rec->ecal) += step->GetTotalEnergyDeposit();
  return true;
}
