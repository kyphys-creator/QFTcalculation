/* Stage 4 of the EFT and dark-matter tools: micrOMEGAs' own model SingletDM (Feynman gauge, its own SM inputs, running
   quark masses), as an implementation independent of the FeynRules model. Its h ~x1 ~x1 vertex is -2 laSH v, so
   laSH = lambda_hs/2. Copied by run_stage4.sh to ~/hep/micromegas_7.1.10/SingletDM/main_eftdm.c.  Usage: ./main_eftdm Mdm1 laSH */
#include"../include/micromegas.h"
#include"../include/micromegas_aux.h"
#include"lib/pmodel.h"

int main(int argc, char** argv)
{ int err; char cdmName[10]; double Xf, Omega;
  double pA0[2], pA5[2], nA0[2], nA5[2];
  VZdecay = 0; VWdecay = 0;
  if(argc > 2) { assignValW("Mdm1", atof(argv[1])); assignValW("laSH", atof(argv[2])); }
  err = sortOddParticles(cdmName);
  if(err) { printf("Can't calculate %s\n", cdmName); return 1; }
  printf("CDM %s mass %.10g MW %.10g\n", cdmName, Mcdm, findValW("MW"));
  printf("vSigma 20 %.10e\n", vSigmaA(Mcdm/20, 0, 1E-6));
  Omega = darkOmega(&Xf, 0, 1E-6, &err);
  printf("Omega %.10e Xf %.6f err %d\n", Omega, Xf, err);
  printChannels(Xf, 1E-6, 1E-6, 1, stdout);
  err = nucleonAmplitudes(CDM[1], pA0, pA5, nA0, nA5);
  printf("A0 %.10e %.10e err %d\n", pA0[0], nA0[0], err);
  killPlots();
  return 0;
}
