#!/bin/bash
# Step (9) of the CKM note: the note's CKM NLO UFO (NLOCT's R2 vertices; the FJ counterterms, the CKM counterterm dV and
# the on-shell field constants with the off-diagonal quark ones) and MadLoop against the note's own amplitudes.
#   1. the UFO (unless --no-ufo):
#      nlo_ckm_renormalize.wl nomix, nlo_ckm_writect.wl msbar   (NLOCT: the R2 vertices, generated/SM_CKM_R2.m)
#      nlo_ckm_ctrules.wl     (FeynRules: counterterm, CKM-counterterm and tadpole vertices, symbolic constants)
#      nlo_ckm_fjdelta.wl     (the MS-bar FJ constants, dV, dvT)
#      nlo_ckm_dzown.wl       (this note's on-shell field constants at the point)
#      nlo_ckm_dz.wl          (the field constants for the UFO; NLOCT's where available, compared with this note's)
#      nlo_ckm_ctparams.wl, nlo_ckm_ufo.wl   (CT parameters, WriteUFO -> generated/SM_CKM_NLO_UFO)
#   2. the references: wud_madloop_ref.wl (W+ -> u_i dbar_j, step (5)), fcnc_madloop_ref.wl (steps (7), (8))
#   3. MadLoop standalone for the outputs of ckm_madloop.py --outputs (work/ml/<name>), then ckm_madloop.py
#      -> results/ckm_madloop.csv
# Usage: ./run_madloop_check.sh [--no-ufo]
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work/ml results
wl() {   # script, argument, log name
  echo "== $1 $2"
  wolframscript -file "$1.wl" $2 > "work/$3.log" 2>&1 || { echo "$1 failed (work/$3.log)"; exit 1; }
  grep -E '^(renormalized|written|counterterm|CKM|check|tadpole|K de|V = 1|constants|field|solved|finite|NLOCT|largest|off-diag|this note|CT param|  dV|  dvT|UV |decimal|\(a\)|\(b\)|\(c\)|mu = |   [a-z][a-z]:)' "work/$3.log" | cut -c1-300
}
if [ "$1" != "--no-ufo" ]; then
  wl nlo_ckm_renormalize nomix nlo_ckm_renormalize0
  wl nlo_ckm_writect msbar nlo_ckm_writectms
  wl nlo_ckm_ctrules "" nlo_ckm_ctrules
  wl nlo_ckm_fjdelta "" nlo_ckm_fjdelta
  wl nlo_ckm_dzown "" nlo_ckm_dzown
  wl nlo_ckm_dz "" nlo_ckm_dz
  wl nlo_ckm_ctparams "" nlo_ckm_ctparams
  wl nlo_ckm_dzown ms0 nlo_ckm_dzown_ms0
  wl nlo_ckm_dz ms0 nlo_ckm_dz_ms0
  wl nlo_ckm_ctparams ms0 nlo_ckm_ctparams_ms0
  wl nlo_ckm_ufo "" nlo_ckm_ufo
fi
wl wud_madloop_ref "" wud_madloop_ref
wl fcnc_madloop_ref "" fcnc_madloop_ref
# the UFO, and a copy with the CT parameters of m_s = 0 for the flavour-changing processes (nlo_ckm_ctparams.wl ms0)
rm -rf work/ml/SM_CKM_NLO_UFO work/ml/SM_CKM_NLO_UFO_ms0
cp -r generated/SM_CKM_NLO_UFO work/ml/
cp -r generated/SM_CKM_NLO_UFO work/ml/SM_CKM_NLO_UFO_ms0
cp generated/SM_CKM_CT_parameters_ms0.py work/ml/SM_CKM_NLO_UFO_ms0/CT_parameters.py
build() {   # output name, model, processes separated by |
  local out="work/ml/$1"
  rm -rf "$out"
  { echo "import model ./work/ml/$2"
    IFS='|' read -ra ps <<< "$3"
    echo "generate ${ps[0]}"
    for p in "${ps[@]:1}"; do echo "add process $p"; done
    echo "output standalone ./$out"; } > "$out.mg5"
  mg5_aMC "$out.mg5" < /dev/null > "$out.log" 2>&1
  grep -E 'Contributing diagrams' "$out.log" | sed 's/^/  /'
  python3 ckm_madloop.py --card "$out/Cards/param_card.dat" "$1" || exit 1
  for P in "$out"/SubProcesses/P*_*; do
    [ -f "$P/check_sa.f" ] || continue
    python3 ../../sm/Src/patch_check_sa.py "$P/check_sa.f"
    (cd "$P" && make check > make.log 2>&1) || { echo "compilation failed, see $P/make.log"; exit 1; }
  done
}
echo "== MadLoop"
python3 ckm_madloop.py --outputs > work/ml/outputs.txt
while IFS='|' read -r name model procs; do
  build "$name" "$model" "$procs"
done < work/ml/outputs.txt
python3 ckm_madloop.py
