"""geant4_pybind (conda env g4) on ~/hep/geant4-11.4.3 (environment.pdf): TestEm0's materials and EM physics
(emstandard_opt3) rebuilt in Python, G4EmCalculator's numbers for the two runs of TestEm0.in (gamma 300 keV in
germanium; e- 10 MeV in water with 100 um cuts) against the C++ TestEm0 output given as argument, then 100 events.
Usage (run_geant4.sh): ~/miniforge3/envs/g4/bin/python test_pybind.py <TestEm0.out of the C++ run>
"""
import re
import sys

from geant4_pybind import *

UNITS = {"barn": barn, "mbarn": millibarn, "ubarn": microbarn, "nbarn": nanobarn, "pbarn": picobarn,
         "cm^-1": 1 / cm, "mm^-1": 1 / mm, "m^-1": 1 / m, "km^-1": 1 / km,
         "GeV/cm": GeV / cm, "MeV/cm": MeV / cm, "keV/cm": keV / cm, "eV/cm": eV / cm,
         "km": km, "m": m, "cm": cm, "mm": mm, "um": um, "nm": nm}


class Detector(G4VUserDetectorConstruction):
    """TestEm0's Water and Germanium (DetectorConstruction.cc), a germanium box inside a water box."""

    def Construct(self):
        h = G4Element("Hydrogen", "H", 1.0, 1.01 * g / mole)
        o = G4Element("Oxygen", "O", 8.0, 16.00 * g / mole)
        water = G4Material("Water", 1.000 * g / cm3, 2)
        water.AddElement(h, 2)
        water.AddElement(o, 1)
        water.GetIonisation().SetMeanExcitationEnergy(78.0 * eV)
        ge = G4Material("Germanium", 32.0, 72.61 * g / mole, 5.323 * g / cm3)
        self.keep = [h, o, water, ge]
        world_lv = G4LogicalVolume(G4Box("World", 1 * m, 1 * m, 1 * m), water, "World")
        ge_lv = G4LogicalVolume(G4Box("Ge", 10 * cm, 10 * cm, 10 * cm), ge, "Ge")
        self.keep += [world_lv, ge_lv]
        G4PVPlacement(None, G4ThreeVector(), ge_lv, "Ge", world_lv, False, 0)
        return G4PVPlacement(None, G4ThreeVector(), world_lv, "World", None, False, 0)


class Physics(G4VModularPhysicsList):
    """TestEm0's PhysicsList with emstandard_opt3: cut converter from 100 eV to 1 GeV, CSDA ranges built, no general
    gamma process; 100 um cuts (its run 1)."""

    def __init__(self):
        super().__init__()
        self.SetDefaultCutValue(100 * um)
        G4ProductionCutsTable.GetProductionCutsTable().SetEnergyRange(100 * eV, 1 * GeV)  # as TestEm0
        self.RegisterPhysics(G4EmStandardPhysics_option3())
        G4EmParameters.Instance().SetBuildCSDARange(True)
        G4EmParameters.Instance().SetGeneralProcessActive(False)


class Gun(G4VUserPrimaryGeneratorAction):
    def __init__(self):
        super().__init__()
        self.gun = G4ParticleGun(1)
        self.gun.SetParticleDefinition(G4Electron.Electron())
        self.gun.SetParticleEnergy(10 * MeV)
        self.gun.SetParticlePosition(G4ThreeVector(0, 0, -50 * cm))
        self.gun.SetParticleMomentumDirection(G4ThreeVector(0, 0, 1))

    def GeneratePrimaries(self, event):
        self.gun.GeneratePrimaryVertex(event)


class Edep(G4UserSteppingAction):
    def __init__(self, total):
        super().__init__()
        self.total = total

    def UserSteppingAction(self, step):
        self.total[0] += step.GetTotalEnergyDeposit()


class Actions(G4VUserActionInitialization):
    """The user actions must be made after the physics list is set (Build() is called then)."""

    def __init__(self, total):
        super().__init__()
        self.total = total

    def Build(self):
        self.SetUserAction(Gun())
        self.SetUserAction(Edep(self.total))


def cpp_values(path):
    """{(run, row label): [value in Geant4 units]} of the C++ TestEm0 output."""
    out, run = {}, -1
    for line in open(path, errors="replace"):
        if line.startswith("### Run"):
            run += 1
        m = re.match(r"\s+(cross section per atom|cross section per volume|restricted dE/dx|unrestricted dE/dx|"
                     r"range from restrict dE/dx|range from full dE/dx)\s*:(.*)", line)
        if m:
            vals = re.findall(r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)\s+(\S+)", m.group(2))
            out[(run, m.group(1))] = [float(v) * UNITS[u] for v, u in vals if u in UNITS]
    return out


def main():
    G4UImanager.GetUIpointer().ApplyCommand("/control/verbose 0")
    rm = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
    edep = [0.0]
    rm.SetUserInitialization(Detector())
    rm.SetUserInitialization(Physics())
    rm.SetUserInitialization(Actions(edep))
    rm.Initialize()
    rm.BeamOn(100)  # also builds the physics tables used below

    calc = G4EmCalculator()
    gamma, electron = G4Gamma.Gamma(), G4Electron.Electron()
    ge, water = G4Material.GetMaterial("Germanium"), G4Material.GetMaterial("Water")
    # energy cuts of the 100 um range cut as in the production-cuts table (TestEm0 uses the table's values)
    cuts = G4ProductionCutsTable.GetProductionCutsTable()
    ecut_e = cuts.ConvertRangeToEnergy(electron, water, 100 * um)
    ecut_g = cuts.ConvertRangeToEnergy(gamma, water, 100 * um)
    print(f"pybind: energy cuts in water: e- {ecut_e / keV:.6g} keV, gamma {ecut_g / keV:.6g} keV; "
          f"ComputeEnergyCutFromRangeCut: e- {calc.ComputeEnergyCutFromRangeCut(100 * um, electron, water) / keV:.6g} keV")
    py = {}
    procs = ["phot", "compt", "conv", "Rayl"]
    e0 = 300 * keV
    xs = [calc.ComputeCrossSectionPerAtom(e0, gamma, p, ge.GetZ(), ge.GetA(), 0) for p in procs]
    py[(0, "cross section per atom")] = xs + [sum(xs)]
    xs = [calc.GetCrossSectionPerVolume(e0, gamma, p, ge) for p in procs]
    py[(0, "cross section per volume")] = xs + [sum(xs)]
    e1 = 10 * MeV
    procs = [("eIoni", ecut_e), ("eBrem", ecut_g), ("ePairProd", ecut_e)]
    d = [calc.ComputeDEDX(e1, electron, p, water, c) for p, c in procs]
    py[(1, "restricted dE/dx")] = d + [sum(d)]
    d = [calc.ComputeDEDX(e1, electron, p, water, e1) for p, _ in procs]
    py[(1, "unrestricted dE/dx")] = d + [sum(d)]
    # GetRangeFromRestricteDEDX and GetCSDARange are not bound; GetRange is the CSDA range when it is built
    py[(1, "range from full dE/dx")] = [calc.GetRange(e1, electron, water)]

    cpp = cpp_values(sys.argv[1])
    n, worst = 0, 0.0
    for key, vals in py.items():
        ref = cpp[key][:len(vals)]
        for a, b in zip(vals, ref):
            n += 1
            if a != b:
                d = abs(a - b) / max(abs(a), abs(b))
                if d > 1e-5:
                    print(f"pybind: {key[1]} (run {key[0]}): Python {a:.7g}, C++ {b:.7g}, relative difference {d:.1e}")
                worst = max(worst, d)
    print(f"pybind: geant4_pybind on Geant4 {G4Version.strip('$ ')}; {n} numbers of TestEm0 (cross sections, dE/dx, "
          f"ranges) against the C++ run: largest relative difference {worst:.1e} (printed to 6 digits)")
    print(f"pybind: e.g. compt per atom in Ge {py[(0, 'cross section per atom')][1] / barn:.6g} b, "
          f"CSDA range of e- 10 MeV in water {py[(1, 'range from full dE/dx')][0] / cm:.6g} cm")
    print(f"pybind: 100 events of e- 10 MeV: mean deposited energy {edep[0] / 100 / MeV:.4g} MeV per event")


if __name__ == "__main__":
    main()
