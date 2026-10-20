#!/bin/bash
# Stage 3 of the EFT and dark-matter tools (environment.pdf), MadDM's loop-induced lines: S S -> a a and a Z of real scalar DM
# with a Higgs portal at one loop (lambda_hs = 0.1; m_S = 70, 100, 200 GeV), against the Higgs note's one-loop amplitudes.
#   1. model/make_nlo_ufo.wl ren, ct, ufo: FeynRules + NLOCT -> out/model_nlo/SM_SingletDM_NLO_UFO (Feynman gauge; R2 and the
#      on-shell h Z a counterterm; about 5 min; skipped with --no-ufo)
#   2. MadDM: generate indirect_spectral_features a a, add indirect_spectral_features a z; one launch per mass (sigmav_method
#      madevent, WH = 0), each followed by test_maddm_line.py --collect (MadDM's results and MadLoop's standalone check, which
#      use the parameters compiled in at that launch)
#   3. test_maddm_line.py: the comparison
# About 7 minutes (1 with --no-ufo).  MadDM runs from MG5's directory and needs the local patch files/maddm_run_interface.py.patch
# (its madevent path with MG5 3.8.1).
cd "$(dirname "$0")"
H=$(pwd)
PY=~/miniforge3/envs/qft/bin/python
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p out
if [ "$1" != "--no-ufo" ]; then
  rm -rf out/model_nlo
  mkdir -p out/model_nlo
  for step in ren ct ufo; do
    ~/hep/bin/wolframscript -file model/make_nlo_ufo.wl $step > out/model_nlo/$step.log 2>&1 \
      || { echo "make_nlo_ufo.wl $step failed: out/model_nlo/$step.log"; exit 1; }
  done
  grep -hE "^(Feynman rules of|written|R2 vertices with|h a a|h Z a|decimal|messages)" out/model_nlo/{ren,ct,ufo}.log | cut -c1-200
fi
rm -rf out/maddm_line
cat > out/maddm_line_gen.txt <<CMD
import model $H/out/model_nlo/SM_SingletDM_NLO_UFO
define darkmatter ~sdm
generate indirect_spectral_features a a
add indirect_spectral_features a z
output $H/out/maddm_line
CMD
(cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/maddm "$H/out/maddm_line_gen.txt") > out/maddm_line_gen.log 2>&1
grep -E "Contributing diagrams" out/maddm_line_gen.log
for m in 70 100 200; do
  cat > out/maddm_line_launch.txt <<CMD
launch $H/out/maddm_line
set MS0 $m
set lamHS 0.1
set WH 0.0
set sigmav_method madevent
done
CMD
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/maddm "$H/out/maddm_line_launch.txt") > out/maddm_line_m$m.log 2>&1
  grep -q "Results written in" out/maddm_line_m$m.log || { echo "MadDM failed at m_S = $m: out/maddm_line_m$m.log"; exit 1; }
  $PY test_maddm_line.py --collect $m || exit 1
done
$PY test_maddm_line.py
