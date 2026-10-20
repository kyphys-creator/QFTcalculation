#!/bin/bash
# Stage 3 of the EFT and dark-matter tools (environment.pdf): MadDM 3.3 (rc/3.3) on real scalar DM with a Higgs portal.
#   1. model/make_ufo.wl: FeynRules SM + model/SingletDM.fr -> out/model/SM_SingletDM_UFO (and CalcHEP files for stage 4)
#   2. MadDM: relic density and direct detection at m_S = 100 GeV, lambda_hs = 0.1 (run_01); the relic density again
#      with eps_ode = 1e-4 (run_02)
#   3. test_maddm.py: against own formulas with MadDM's inputs
# About 2 minutes. MadDM runs from MG5's directory (its install paths are relative to the working directory).
cd "$(dirname "$0")"
H=$(pwd)
mkdir -p out
rm -rf out/model out/maddm_hp
~/hep/bin/wolframscript -file model/make_ufo.wl > out/make_ufo.log 2>&1
grep -E "messages" out/make_ufo.log
cat > out/maddm_hp.txt <<CMD
import model $H/out/model/SM_SingletDM_UFO
define darkmatter ~sdm
generate relic_density
add direct_detection
output $H/out/maddm_hp
launch $H/out/maddm_hp
set MS0 100.0
set lamHS 0.1
done
launch $H/out/maddm_hp
set eps_ode 0.0001
done
CMD
(cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/maddm "$H/out/maddm_hp.txt") > out/maddm_hp.log 2>&1 || { echo "MadDM failed: out/maddm_hp.log"; exit 1; }
~/miniforge3/envs/qft/bin/python test_maddm.py
