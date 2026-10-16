#!/bin/bash
# Research note models/qcd, step (9): heavy-quark pair production at NLO (partonic f1_ij by reverse unitarity, hadronic vs aMC@NLO).
#   1. hq_me_mg5.py: MadGraph5 standalone 2 -> 3 matrix elements at random points (check of step 2 at D = 4)
#   2. hq_real.wl: D-dimensional squared real-emission matrix elements, pair by pair (gg in 6 processes), sum, check at D = 4
#   3. hq_reduce.wl: partial fractions, cut families, Kira, distinct masters
#   4. hq_amflow.wl: the masters with AMFlow on the s grid of results/hq_sgrid.txt (3 processes)
#   5. hq_born.wl, hq_virtual.py: D-dimensional Born and colour correlations; MadLoop on an angular grid (needs work/ml_A, work/ml_B
#      from run_madloop_check.sh)
#   6. hq_assemble.wl: f1 per channel (the poles cancel) -> results/hq_f1_<chan>.csv
#   7. hq_cm.wl: the exact f1 of Czakon-Mitov at the grid and at the nodes of the hadronic integrals (only if ../Ref/cm08_src exists;
#      see hq_cm.wl for the download) -> results/hq_cm.csv, results/hq_cm_nodes.csv
#   8. hq_mg5.sh, hq_mg5_fix.sh (MG5 with the p pbar fix; unless NO_MG5=1; needs work/QCD_NLO_UFO_amc from ee_mg5.py), hq_hadronic.py,
#      hq_plot.py
# About 4 hours on 8 cores (AMFlow about 2 hours, the gg matrix element about 1 hour, aMC@NLO 40 minutes).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work/hq results
S=$(cat results/hq_sgrid.txt)
set -e
echo "=== MadGraph5 standalone 2 -> 3"
"$PY" hq_me_mg5.py
echo "=== real emission"
wolframscript -file hq_real.wl qq 2>&1 | grep -E "^\(a\)|^\(c\)"
wolframscript -file hq_real.wl qg 2>&1 | grep -E "^\(a\)|^\(c\)"
for r in "1 43" "44 85" "86 128" "129 170" "171 213" "214 256"; do
  set -- $r
  wolframscript -file hq_real.wl gg "$1" "$2" > "work/hq/real_gg_$1.log" 2>&1 &
done
wait
wolframscript -file hq_real.wl gg 2>&1 | grep -E "^\(a\)|^\(c\)"
echo "=== reduction"
for c in qq qg gg; do wolframscript -file hq_reduce.wl $c 2>&1 | grep -E "^\(a\)|^\(b\)|^\(c\)"; done
echo "=== AMFlow"
for c in qq qg gg; do
  for f in $(wolframscript -code "Print[StringRiffle[ToString /@ Get[\"work/hq/unique_$c.m\"][\"chosen\"], \" \"]]" | head -1); do
    echo "$c $f $S"
  done
done > work/hq/amflow_jobs.txt
xargs -P 3 -L 1 bash -c 'wolframscript -file hq_amflow.wl $0 $1 "$2" > work/hq/amflow_$0_$1.log 2>&1' < work/hq/amflow_jobs.txt
echo "=== Born, virtual"
wolframscript -file hq_born.wl 2>&1 | grep -E "colour|Eq.\(13\)"
"$PY" hq_virtual.py "$S" 64 | tail -1
echo "=== f1"
for c in qq qg gg; do wolframscript -file hq_assemble.wl $c 2>&1 | grep -E "f1 =|missing" | sed 's/.*f1 = K (V + C + R) = /  f1 = /' | cut -c1-60; done
echo "=== Czakon-Mitov"
if [ -f ../Ref/cm08_src/x/NLOXSections.m ]; then wolframscript -file hq_cm.wl 2>&1 | grep -E "max|wrote"; else echo "  ../Ref/cm08_src missing: skipped"; fi
echo "=== hadronic"
if [ "${NO_MG5:-0}" != 1 ]; then ./hq_mg5.sh; ./hq_mg5_fix.sh; fi
"$PY" hq_hadronic.py
"$PY" hq_plot.py
