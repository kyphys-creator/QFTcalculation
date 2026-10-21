// The event record and its output.  A primary is "of interest" when it is lv+- or charged with pT > 5 GeV; for those the
// tracking action records the start and the end of the track, the sensitive detectors (Detector.cc) the tracker and
// muon-station crossings.  Batch runs write four ntuples to one ROOT file (merged over the threads):
//   prim  : evt id pdg px py pz e [GeV] endx endy endz [mm] endekin [GeV]
//   trk   : evt id layer x y z [mm] t [ns] p [GeV] bg path [mm] edep [keV]
//   muon  : evt id station x y z [mm] t [ns] p [GeV]
//   event : evt nprim ecal hcal [GeV]   (nprim: the primaries passed to Geant4; ecal, hcal: all deposits, HCAL's in
//           the scintillator)
// evt is the index of the event in the HepMC file and id the Geant4 track ID.  Interactive runs print lv+- instead.
#include "vlldet.hh"

#include "G4AnalysisManager.hh"
#include "G4Event.hh"
#include "G4EventManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4Track.hh"
#include "G4TrackingManager.hh"

#include <cstdio>

EventAction* EventAction::Current()
{
  return static_cast<EventAction*>(G4EventManager::GetEventManager()->GetUserEventAction());
}

void EventAction::EndOfEventAction(const G4Event*)
{
  if (fWrite) {
    auto am = G4AnalysisManager::Instance();
    for (const auto& [id, p] : prims) {
      const G4double v[] = {p.p.x() / GeV, p.p.y() / GeV, p.p.z() / GeV, p.e / GeV, p.end.x() / mm, p.end.y() / mm,
                            p.end.z() / mm, p.endEkin / GeV};
      am->FillNtupleIColumn(0, 0, evt);
      am->FillNtupleIColumn(0, 1, id);
      am->FillNtupleIColumn(0, 2, p.pdg);
      for (G4int c = 0; c < 8; ++c) am->FillNtupleDColumn(0, 3 + c, v[c]);
      am->AddNtupleRow(0);
    }
    for (const auto& [key, c] : tracker) {
      if (!c.seen) continue;   // only secondaries of the primary in this layer
      const G4double v[] = {c.pos.x() / mm, c.pos.y() / mm, c.pos.z() / mm, c.t / ns, c.p / GeV, c.bg, c.path / mm,
                            c.edep / keV};
      am->FillNtupleIColumn(1, 0, evt);
      am->FillNtupleIColumn(1, 1, key.first);
      am->FillNtupleIColumn(1, 2, key.second);
      for (G4int k = 0; k < 8; ++k) am->FillNtupleDColumn(1, 3 + k, v[k]);
      am->AddNtupleRow(1);
    }
    for (const auto& [key, c] : muon) {
      const G4double v[] = {c.pos.x() / mm, c.pos.y() / mm, c.pos.z() / mm, c.t / ns, c.p / GeV};
      am->FillNtupleIColumn(2, 0, evt);
      am->FillNtupleIColumn(2, 1, key.first);
      am->FillNtupleIColumn(2, 2, key.second);
      for (G4int k = 0; k < 5; ++k) am->FillNtupleDColumn(2, 3 + k, v[k]);
      am->AddNtupleRow(2);
    }
    am->FillNtupleIColumn(3, 0, evt);
    am->FillNtupleIColumn(3, 1, nPrimaries);
    am->FillNtupleDColumn(3, 2, ecal / GeV);
    am->FillNtupleDColumn(3, 3, hcal / GeV);
    am->AddNtupleRow(3);
  }
  if (fPrint) {
    char s[256];
    std::snprintf(s, sizeof s, "event %d of the file: %d primaries; ECAL %.1f GeV, HCAL scintillator %.3f GeV", evt,
                  nPrimaries, ecal / GeV, hcal / GeV);
    G4cout << s << G4endl;
    for (const auto& [id, p] : prims) {
      if (std::abs(p.pdg) != kLVpdg) continue;
      std::snprintf(s, sizeof s, "  %s: p = %.1f GeV, pT = %.1f GeV, eta = %+.2f, beta = %.3f; track ends at r = %.2f m,"
                    " z = %+.2f m with %.1f GeV", p.pdg > 0 ? "lv-" : "lv+", p.p.mag() / GeV, p.p.perp() / GeV,
                    p.p.pseudoRapidity(), p.p.mag() / p.e, p.end.perp() / m, p.end.z() / m, p.endEkin / GeV);
      G4cout << s;
      for (G4int st = 0; st < 4; ++st) {
        auto it = muon.find({id, st});
        if (it == muon.end()) continue;
        std::snprintf(s, sizeof s, "%s station %d at %.1f ns", st == 0 ? "\n    muon" : ",", st + 1, it->second.t / ns);
        G4cout << s;
      }
      G4cout << G4endl;
    }
  }
  prims.clear();
  tracker.clear();
  muon.clear();
  ecal = hcal = 0;
}

TrackingAction::TrackingAction(EventAction* record, G4bool view) : fRecord(record), fView(view), fStoreAbove(1 * GeV)
{
  if (!view) return;
  fMessenger = std::make_unique<G4GenericMessenger>(this, "/vlldet/", "vlldet's events");
  fMessenger->DeclarePropertyWithUnit("storeAbove", "GeV", fStoreAbove,
                                      "keep the trajectories of the tracks above this momentum (and of lv+-)");
}

void TrackingAction::PreUserTrackingAction(const G4Track* track)
{
  const auto def = track->GetDefinition();
  const auto p = track->GetMomentum();
  if (fView)   // 2: smooth trajectories, as /vis/scene/add/trajectories smooth sets
    fpTrackingManager->SetStoreTrajectory(std::abs(def->GetPDGEncoding()) == kLVpdg || p.mag() > fStoreAbove ? 2 : 0);
  if (track->GetParentID() != 0) return;
  if (std::abs(def->GetPDGEncoding()) == kLVpdg || (def->GetPDGCharge() != 0 && p.perp() > 5 * GeV))
    fRecord->prims[track->GetTrackID()] = {def->GetPDGEncoding(), p, track->GetTotalEnergy(), {}, 0};
}

void TrackingAction::PostUserTrackingAction(const G4Track* track)
{
  auto it = fRecord->prims.find(track->GetTrackID());
  if (it == fRecord->prims.end()) return;
  it->second.end = track->GetPosition();
  it->second.endEkin = track->GetKineticEnergy();
}

void SteppingAction::UserSteppingAction(const G4Step* step)
{
  auto track = step->GetTrack();
  if (track->GetGlobalTime() > kMaxTime * ns && std::abs(track->GetDefinition()->GetPDGEncoding()) != kLVpdg) {
    track->SetTrackStatus(fStopAndKill);
    return;
  }
  if (track->GetCurrentStepNumber() < kMaxSteps) return;
  const auto x = track->GetPosition();
  char s[300];
  std::snprintf(s, sizeof s, "event %d: track %d (%s, parent %d) killed after %d steps: Ekin %.4g MeV, p (%.4g, %.4g, %.4g) MeV,"
                " at (%.1f, %.1f, %.1f) mm in %s, t %.4g ns", EventAction::Current()->evt, track->GetTrackID(),
                track->GetDefinition()->GetParticleName().c_str(), track->GetParentID(), kMaxSteps,
                track->GetKineticEnergy() / MeV, track->GetMomentum().x() / MeV, track->GetMomentum().y() / MeV,
                track->GetMomentum().z() / MeV, x.x() / mm, x.y() / mm, x.z() / mm,
                track->GetVolume()->GetName().c_str(), track->GetGlobalTime() / ns);
  G4cout << s << G4endl;
  track->SetTrackStatus(fStopAndKill);
}

RunAction::RunAction(const G4String& file)
{
  auto am = G4AnalysisManager::Instance();
  am->SetDefaultFileType("root");
  am->SetFileName(file);
  am->SetNtupleMerging(true);
  am->SetVerboseLevel(0);
  const std::vector<std::pair<G4String, std::vector<G4String>>> books = {
    {"prim", {"px", "py", "pz", "e", "endx", "endy", "endz", "endekin"}},
    {"trk", {"x", "y", "z", "t", "p", "bg", "path", "edep"}},
    {"muon", {"x", "y", "z", "t", "p"}}};
  const char* third[] = {"pdg", "layer", "station"};
  for (std::size_t n = 0; n < books.size(); ++n) {
    am->CreateNtuple(books[n].first, books[n].first);
    am->CreateNtupleIColumn("evt");
    am->CreateNtupleIColumn("id");
    am->CreateNtupleIColumn(third[n]);
    for (const auto& c : books[n].second) am->CreateNtupleDColumn(c);
    am->FinishNtuple();
  }
  am->CreateNtuple("event", "event");
  am->CreateNtupleIColumn("evt");
  am->CreateNtupleIColumn("nprim");
  am->CreateNtupleDColumn("ecal");
  am->CreateNtupleDColumn("hcal");
  am->FinishNtuple();
}

void RunAction::BeginOfRunAction(const G4Run*)
{
  G4AnalysisManager::Instance()->OpenFile();
}

void RunAction::EndOfRunAction(const G4Run*)
{
  auto am = G4AnalysisManager::Instance();
  am->Write();
  am->CloseFile();
}

void Actions::BuildForMaster() const
{
  if (!fFile.empty()) SetUserAction(new RunAction(fFile));
}

void Actions::Build() const
{
  const G4bool batch = !fFile.empty();
  auto record = new EventAction(batch, !batch);
  SetUserAction(new PrimaryGenerator(fEvents, record, !batch));
  SetUserAction(record);
  SetUserAction(new TrackingAction(record, !batch));
  SetUserAction(new SteppingAction);
  if (batch) SetUserAction(new RunAction(fFile));
}
