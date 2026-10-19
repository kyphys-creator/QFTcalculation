#!/bin/bash
# Stage 1 of the LHC tools (environment.pdf): LHAPDF 6.5.5 (MG5's HEPTools) and the PDF sets.
#   1. the sum rules of the sets from their grids                                               (test_lhapdf.py sumrules)
#   2. MG5 madevent: p p -> e+ e- (model sm) and g g -> h (the HEFT UFO of models/sm_higgs), 13 TeV, LHAPDF set 331700
#   3. the two LO cross sections against own integrals with the same PDF                       (test_lhapdf.py dy ggh)
# Output in ./out (process directories, logs, the param_cards used).  About 5 minutes.
cd "$(dirname "$0")"
HERE=$(pwd)
mkdir -p out
# MG5 rewrites a Python-2 UFO in place when it imports it (object_library.py, write_param_card.py, py3_model.pkl):
# import a fresh copy, so that the committed UFO of models/sm_higgs stays as generated
rm -rf out/SM_CKM_HEFT_UFO && cp -R "$HERE/../../../models/sm_higgs/Src/generated/SM_CKM_HEFT_UFO" out/
UFO="$HERE/out/SM_CKM_HEFT_UFO"
python3 test_lhapdf.py sumrules
common () {   # run card settings shared by both processes
  cat <<CARD
set nevents $1
set ebeam1 6500
set ebeam2 6500
set pdlabel lhapdf
set lhaid 331700
set fixed_ren_scale True
set fixed_fac_scale True
set scale $2
set dsqrt_q2fact1 $2
set dsqrt_q2fact2 $2
set use_syst False
CARD
}
{ echo "import model sm"; echo "generate p p > e+ e-"; echo "output $HERE/out/dy_proc -f"; echo "launch $HERE/out/dy_proc"; echo "done"
  common 100000 91.188
  echo "set ptl 0"; echo "set etal -1"; echo "set drll 0"; echo "set mmll 60"; echo "set mmllmax 120"; echo "done"; } > out/dy.mg5
{ echo "import model $UFO"; echo "generate g g > h"; echo "output $HERE/out/ggh_proc -f"; echo "launch $HERE/out/ggh_proc"; echo "done"
  common 20000 125.0
  echo "set param_card HEFT 1 -0.0125"; echo "set param_card MASS 25 125.0"; echo "done"; } > out/ggh.mg5
# run MG5 from its own directory (its 'install' and HEPTools paths are relative to the working directory)
for p in dy ggh; do
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/$p.mg5") > out/$p.log 2>&1 || { echo "MG5 $p failed: out/$p.log"; exit 1; }
  cp out/${p}_proc/Cards/param_card.dat out/${p}_param_card.dat
done
python3 test_lhapdf.py dy ggh
