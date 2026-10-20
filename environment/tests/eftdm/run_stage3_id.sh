#!/bin/bash
# Stage 3 of the EFT and dark-matter tools (environment.pdf), MadDM's continuum indirect detection at tree level: the sigma v of
# every channel of real scalar DM with a Higgs portal (lambda_hs = 0.1; m_S = 70, 100, 200 GeV), against own formulas.
#   1. the model of run_stage3.sh (out/model/SM_SingletDM_UFO, unitary gauge; made by model/make_ufo.wl if missing)
#   2. MadDM: generate indirect_detection; one launch per mass (indirect=sigmav, sigmav_method madevent: no spectra, nothing
#      to download), each followed by test_maddm_id.py --collect
#   3. test_maddm_id.py: the comparison
# About 1.5 minutes.  MadDM runs from MG5's directory and needs the local patches files/maddm_MGoutput.py.patch (the tree-level
# indirect output does not compile with MG5 3.8.1 without it) and files/maddm_run_interface.py.patch (the madevent path).
cd "$(dirname "$0")"
H=$(pwd)
PY=~/miniforge3/envs/qft/bin/python
mkdir -p out
if [ ! -d out/model/SM_SingletDM_UFO ]; then
  ~/hep/bin/wolframscript -file model/make_ufo.wl > out/make_ufo.log 2>&1 || { echo "make_ufo.wl failed: out/make_ufo.log"; exit 1; }
fi
rm -rf out/maddm_id
cat > out/maddm_id_gen.txt <<CMD
import model $H/out/model/SM_SingletDM_UFO
define darkmatter ~sdm
generate indirect_detection
output $H/out/maddm_id
CMD
(cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/maddm "$H/out/maddm_id_gen.txt") > out/maddm_id_gen.log 2>&1
for m in 70 100 200; do
  cat > out/maddm_id_launch.txt <<CMD
launch $H/out/maddm_id
indirect=sigmav
set MS0 $m
set lamHS 0.1
set sigmav_method madevent
done
CMD
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/maddm "$H/out/maddm_id_launch.txt") > out/maddm_id_m$m.log 2>&1
  grep -q "Results written in" out/maddm_id_m$m.log || { echo "MadDM failed at m_S = $m: out/maddm_id_m$m.log"; exit 1; }
  $PY test_maddm_id.py --collect $m || exit 1
done
$PY test_maddm_id.py
