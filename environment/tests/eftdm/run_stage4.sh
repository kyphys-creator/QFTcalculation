#!/bin/bash
# Stage 4 of the EFT and dark-matter tools (environment.pdf): micrOMEGAs 7.1.10.
#   1. the FeynRules model (CalcHEP files of model/make_ufo.wl, written by run_stage3.sh) in the project SingletFR
#   2. micrOMEGAs' own model SingletDM at the same point (laSH = lambda_hs/2)
#   3. test_micromegas.py: against own formulas with micrOMEGAs' inputs, and against MadDM (stage 3)
# About 1 minute (the first run compiles the CalcHEP processes). Run run_stage3.sh first.
cd "$(dirname "$0")"
H=$(pwd)
M=~/hep/micromegas_7.1.10
source ~/hep/opt/buildenv.sh
[ -d $M/SingletFR ] || (cd $M && ./newProject SingletFR > /dev/null)
cp out/model/SM_SingletDM_CH/*.mdl $M/SingletFR/work/models/
cp micromegas/SingletFR_main.c $M/SingletFR/main.c
cp micromegas/SingletDM_main.c $M/SingletDM/main_eftdm.c
(cd $M/SingletFR && rm -f work/so_generated/* && gmake main=main.c > $H/out/micromegas_build.log 2>&1 && ./main 100 0.1) > out/micromegas_fr.txt 2>&1 || { echo "SingletFR failed"; exit 1; }
(cd $M/SingletDM && gmake main=main_eftdm.c >> $H/out/micromegas_build.log 2>&1 && ./main_eftdm 100 0.05) > out/micromegas_native.txt 2>&1 || { echo "SingletDM failed"; exit 1; }
~/miniforge3/envs/qft/bin/python test_micromegas.py
