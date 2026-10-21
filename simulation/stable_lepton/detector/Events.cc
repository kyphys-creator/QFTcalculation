// The HepMC 2 events (MG5 + Pythia 8) as Geant4 primaries.  The file is read once, in the master, into memory; each
// event's final-state particles (status 1, outgoing from their production vertex) become primaries at their production
// vertices.  Neutrinos are not passed on, nor particles made outside the world (Detector.cc; none when Pythia decays only
// particles with c tau < 10 mm, as in run_workflow.sh).  HepMC's lengths are mm and its times are c t in mm.
#include "vlldet.hh"

#include "G4Event.hh"
#include "G4ParticleTable.hh"
#include "G4PhysicalConstants.hh"
#include "G4PrimaryParticle.hh"
#include "G4PrimaryVertex.hh"
#include "G4SystemOfUnits.hh"

#include <zlib.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>

std::vector<GenEvent> ReadHepMC(const std::string& path, G4double& lvMass)
{
  std::vector<GenEvent> events;
  gzFile f = gzopen(path.c_str(), "rb");   // gzipped or not
  if (!f) {
    G4cerr << "cannot open " << path << G4endl;
    std::exit(1);
  }
  static char line[1 << 16];
  G4double vx = 0, vy = 0, vz = 0, vt = 0;
  G4int vbar = 0, nOrphans = 0, k = 0;
  lvMass = 0;
  while (gzgets(f, line, sizeof line)) {
    switch (line[0]) {
      case 'E':
        events.emplace_back();
        break;
      case 'U':   // momentum and length units
        if (std::strncmp(line, "U GEV MM", 8) != 0) {
          G4cerr << path << ": units are not GEV MM: " << line << G4endl;
          std::exit(1);
        }
        break;
      case 'V':   // V barcode id x y z ct n_orphans_in n_particles_out ...: then n_orphans_in incoming, the rest outgoing
        std::sscanf(line + 1, "%d %*d %lf %lf %lf %lf %d", &vbar, &vx, &vy, &vz, &vt, &nOrphans);
        k = 0;
        break;
      case 'P': {   // P barcode pdg px py pz E m status ...
        G4int pdg, status;
        G4double px, py, pz, e, m;
        std::sscanf(line + 1, "%*d %d %lf %lf %lf %lf %lf %d", &pdg, &px, &py, &pz, &e, &m, &status);
        if (status == 1 && k >= nOrphans && !events.empty())
          events.back().push_back({pdg, px, py, pz, e, m, vx, vy, vz, vt, vbar});
        if (std::abs(pdg) == kLVpdg) lvMass = m;
        ++k;
        break;
      }
      default:
        break;
    }
  }
  gzclose(f);
  return events;
}

PrimaryGenerator::PrimaryGenerator(const std::vector<GenEvent>* events, EventAction* record, G4bool sequential)
  : fEvents(events), fRecord(record), fSequential(sequential)
{
  fMessenger = std::make_unique<G4GenericMessenger>(this, "/vlldet/", "vlldet's events");
  fMessenger->DeclareProperty("event", fNext, "index (from 0) of the next event of the file to simulate (interactive)");
}

void PrimaryGenerator::GeneratePrimaries(G4Event* event)
{
  const G4int i = fSequential ? fNext++ : event->GetEventID();
  if (i < 0 || i >= static_cast<G4int>(fEvents->size())) {
    G4Exception("PrimaryGenerator", "vlldet01", FatalException, "no such event in the file");
    return;
  }
  auto table = G4ParticleTable::GetParticleTable();
  std::map<G4int, G4PrimaryVertex*> vertices;   // by HepMC barcode
  G4int n = 0;
  for (const auto& gp : (*fEvents)[i]) {
    const G4int a = std::abs(gp.pdg);
    if (a == 12 || a == 14 || a == 16) continue;
    if (std::abs(gp.x) > 7500 || std::abs(gp.y) > 7500 || std::abs(gp.z) > 7000) {
      G4cout << "event " << i << ": PDG " << gp.pdg << " made outside the world, not simulated" << G4endl;
      continue;
    }
    if (!table->FindParticle(gp.pdg)) {
      G4cout << "event " << i << ": PDG " << gp.pdg << " unknown to Geant4, not simulated" << G4endl;
      continue;
    }
    auto& v = vertices[gp.vertex];
    if (!v) {
      v = new G4PrimaryVertex(gp.x * mm, gp.y * mm, gp.z * mm, gp.t * mm / c_light);
      event->AddPrimaryVertex(v);
    }
    v->SetPrimary(new G4PrimaryParticle(gp.pdg, gp.px * GeV, gp.py * GeV, gp.pz * GeV, gp.e * GeV));
    ++n;
  }
  fRecord->evt = i;
  fRecord->nPrimaries = n;
}
