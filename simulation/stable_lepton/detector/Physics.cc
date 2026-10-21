// lv- and lv+ of VLL.fr as Geant4 particles: spin 1/2, charge -+1, stable, the mass of the event file.  Their only
// interactions with matter are electromagnetic: multiple scattering and ionisation (G4hIonisation: the Bragg or ICRU73
// model below 2 MeV x M/m_p, Bethe-Bloch above, scaled from the proton's or the antiproton's tables; the standard
// fluctuations).  Bremsstrahlung and pair production scale as 1/M^2 and are left out.  Geant4's standard EM builder
// adds processes only to the particles it lists, so these are not duplicated.
#include "vlldet.hh"

#include "G4ParticleDefinition.hh"
#include "G4ParticleTable.hh"
#include "G4PhysicsListHelper.hh"
#include "G4SystemOfUnits.hh"
#include "G4hIonisation.hh"
#include "G4hMultipleScattering.hh"

void LVPhysics::ConstructParticle()
{
  if (G4ParticleTable::GetParticleTable()->FindParticle(kLVpdg)) return;
  // name, mass, width, charge, 2 spin, parity, C, 2 I, 2 I3, G, type, lepton and baryon numbers, PDG code, stable,
  // lifetime, decay table, short-lived, subtype, antiparticle's PDG code
  new G4ParticleDefinition("lv-", fMass * GeV, 0, kLVcharge * eplus, 1, 0, 0, 0, 0, 0, "exotic", 0, 0, kLVpdg, true, -1,
                           nullptr, false, "vll", -kLVpdg);
  new G4ParticleDefinition("lv+", fMass * GeV, 0, -kLVcharge * eplus, 1, 0, 0, 0, 0, 0, "exotic", 0, 0, -kLVpdg, true, -1,
                           nullptr, false, "vll", kLVpdg);
}

void LVPhysics::ConstructProcess()
{
  auto helper = G4PhysicsListHelper::GetPhysicsListHelper();
  for (const G4int pdg : {kLVpdg, -kLVpdg}) {
    auto p = G4ParticleTable::GetParticleTable()->FindParticle(pdg);
    helper->RegisterProcess(new G4hMultipleScattering(), p);
    helper->RegisterProcess(new G4hIonisation(), p);
  }
}
