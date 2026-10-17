#!/bin/bash
# Step (9d) of the SM note: the note's general NLO UFO (all FJ counterterm vertices, generated/SM_NLO_FJ_UFO) against
# MadGraph's on-shell EW NLO model for several processes with massless external particles, [virt=QED].
#   1. the UFO: nlo_ctrules.wl (FeynRules: counterterm and tadpole vertices with symbolic constants), nlo_dz.wl (NLOCT's
#      on-shell field constants from SM_CT.nlo, which nlo_writect.wl of run_nunu_check.sh writes), nlo_fjdelta.wl (FJ
#      MS-bar constants, dvT), nlo_ctparams.wl (CT parameters, massless light fermions), nlo_ufo.wl (WriteUFO)
#   2. MadLoop standalone for each process with loop_qcd_qed_sm-no_widths (work/fj/<name>_off) and with the UFO
#      restricted to light masses and widths 0 (restrict_light0.dat; work/fj/<name>_fj)
#   3. fj_madloop.py: off - fj against the conversion of the parameters (results/nunu_conv.csv of nunu_numeric.wl)
#      -> results/fj_madloop.csv
# Usage: ./run_fj_check.sh [--no-ufo]   (about 10 minutes; --no-ufo: MadLoop and the comparison only)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work/fj results
if [ "$1" != "--no-ufo" ]; then
  for f in nlo_ctrules nlo_dz nlo_fjdelta nlo_ctparams nlo_ufo; do
    echo "== $f"
    wolframscript -file "$f.wl" > "work/$f.log" 2>&1 || { echo "$f failed (work/$f.log)"; exit 1; }
    grep -E '^(counterterm|tadpole|field|solved|constants|check|CT param|FJ|UV|written|K de|pole of)' "work/$f.log" | cut -c1-300
  done
fi
# the UFO and its restriction card (from the param_card of a tree-level output)
rm -rf work/fj/SM_NLO_FJ_UFO work/fj/card0
cp -r generated/SM_NLO_FJ_UFO work/fj/
# (from work/fj: a tree-level standalone output writes nsqso_born.inc into the current directory and its parent)
printf 'import model ./SM_NLO_FJ_UFO\ngenerate ve ve~ > vm vm~\noutput standalone ./card0\n' > work/fj/card0.mg5
(cd work/fj && mg5_aMC card0.mg5 < /dev/null > card0.log 2>&1)
python3 fj_madloop.py --restrict work/fj/card0/Cards/param_card.dat work/fj/SM_NLO_FJ_UFO/restrict_light0.dat || exit 1
build() {   # name, model, process
  local out="work/fj/$1"
  rm -rf "$out"
  printf 'import model %s\ngenerate %s [virt=QED]\noutput standalone ./%s\n' "$2" "$3" "$out" > "$out.mg5"
  mg5_aMC "$out.mg5" < /dev/null > "$out.log" 2>&1
  echo "  $1: $(grep -E 'Contributing diagrams' "$out.log" | head -1)"
  local P
  P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
  python3 patch_check_sa.py "$P/check_sa.f"
  (cd "$P" && make check > make.log 2>&1) || { echo "compilation failed, see $P/make.log"; exit 1; }
}
python3 fj_madloop.py --procs > work/fj/procs.txt
while IFS='|' read -r name proc; do
  echo "== $proc"
  build "${name}_off" loop_qcd_qed_sm-no_widths "$proc"
  build "${name}_fj" ./work/fj/SM_NLO_FJ_UFO-light0 "$proc"
done < work/fj/procs.txt
python3 fj_madloop.py
