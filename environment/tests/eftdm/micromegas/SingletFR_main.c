/* Stage 4 of the EFT and dark-matter tools (QFTcalculation/environment/tests/eftdm): micrOMEGAs 7.1.10 on the FeynRules
   model SM + real scalar DM with a Higgs portal (the CalcHEP files written by model/make_ufo.wl), the same model as
   MadDM's in stage 3. Copied by run_stage4.sh to ~/hep/micromegas_7.1.10/SingletFR/main.c.  Usage: ./main MS0 lamHS
   Pitfall: the FeynRules unitary-gauge model has no Goldstone bosons, but its W and Z carry CalcHEP's gauge flag 'G';
   with ForceUG = 0 (the default) micrOMEGAs uses Feynman-gauge polarization sums and sigma v(W W) is 40% too small. */
#include"../include/micromegas.h"
#include"../include/micromegas_aux.h"
#include"lib/pmodel.h"

int main(int argc, char** argv)
{ int err; char cdmName[10]; double Xf, Omega, x;
  double pA0[2], pA5[2], nA0[2], nA5[2];
  ForceUG = 1;                              /* unitary gauge (see above) */
  VZdecay = 0; VWdecay = 0;                 /* 2 -> 2 only, as MadDM */
  if(argc > 2) { assignValW("MS0", atof(argv[1])); assignValW("lamHS", atof(argv[2])); }
  err = sortOddParticles(cdmName);
  if(err) { printf("Can't calculate %s\n", cdmName); return 1; }
  printf("CDM %s mass %.10g WH %.10e\n", cdmName, Mcdm, pWidth("H", NULL));   /* the auto width !WH */
  for(x = 15; x <= 30; x += 5) printf("vSigma %g %.10e\n", x, vSigmaA(Mcdm/x, 0, 1E-6));   /* [pb] */
  Omega = darkOmega(&Xf, 0, 1E-6, &err);
  printf("Omega %.10e Xf %.6f err %d\n", Omega, Xf, err);
  printChannels(Xf, 1E-6, 1E-6, 1, stdout);
  printf("FF p %.6e %.6e %.6e n %.6e %.6e %.6e\n", ScalarFFPu, ScalarFFPd, ScalarFFPs, ScalarFFNu, ScalarFFNd, ScalarFFNs);
  err = nucleonAmplitudes(CDM[1], pA0, pA5, nA0, nA5);
  printf("A0 %.10e %.10e err %d\n", pA0[0], nA0[0], err);
  printf("alphaQCD(MT) %.10f MT %.10g\n", alphaQCD(findValW("MT")), findValW("MT"));
  killPlots();
  return 0;
}
