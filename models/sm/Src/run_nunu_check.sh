#!/bin/bash
# Step (9) of the SM note: nu_e nubar_e -> nu_mu nubar_mu at one loop, MS-bar with FJ tadpoles, against MadLoop
# (a) with MadGraph's on-shell EW NLO model and the conversion of the parameters, (b) with the note's own NLO UFO.
# About 50 minutes in all.
#   1. nunu_feyncalc.wl: the note's FeynArts model + FeynCalc, general R_xi (results/nunu_feyncalc.m, about 40 MB, not in
#      git; about 35 minutes)
#   2. nunu_numeric.wl: MS-bar finite part with LoopTools, UV pole check, gauge check, conversion to on-shell inputs
#      (alpha(MZ) scheme, on-shell MW, MZ) -> results/nunu_numeric.csv
#   3. nunu_formcalc.wl: unpatched FeynArts + FormCalc, Feynman gauge (results/nunu_formcalc.csv)
#   4. MadLoop with MadGraph's EW NLO model loop_qcd_qed_sm-no_widths (on-shell, its own R2 and counterterms):
#      generate ve ve~ > vm vm~ [virt=QED], output standalone -> work/ml_nunu; check_sa.f reads the point from PS.input
#      and MU_R from MU_R.input
#   5. (9b) the note's own NLO UFO: nlo_renormalize.wl (FeynRules + NLOCT, renormalized model, Feynman gauge),
#      nlo_writect.wl (FeynArts + NLOCT: R2 vertices -> generated/SM_R2.m; SM_CT.nlo is not in git),
#      nlo_fjct.wl (FeynCalc: the FJ counterterms of this process), and the general FJ counterterms of step (9d):
#      nlo_ctrules.wl, nlo_dz.wl, nlo_fjdelta.wl, nlo_ctparams.wl, nlo_ufo.wl (FeynRules WriteUFO ->
#      generated/SM_NLO_FJ_UFO; other processes: run_fj_check.sh); MadLoop with it -> work/ml_nunu_fj, and with it
#      restricted to light masses and widths 0 (restrict_light0.dat) -> work/ml_nunu_fj_r
#   6. nunu_madloop.py sets the param_cards, runs mu_R = MZ and 500 GeV and compares -> results/nunu_madloop.csv
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in nunu_feyncalc nunu_numeric nunu_formcalc; do
  echo "== $f"
  wolframscript -file "$f.wl" > "work/$f.log" 2>&1 || { echo "$f failed (work/$f.log)"; exit 1; }
  grep -E '^\(|^   ' "work/$f.log" | cut -c1-400
done

echo "== MadLoop"
out=work/ml_nunu
rm -rf "$out"
printf 'import model loop_qcd_qed_sm-no_widths\ngenerate ve ve~ > vm vm~ [virt=QED]\noutput standalone ./%s\n' "$out" > "$out.mg5"
mg5_aMC "$out.mg5" > "$out.log" 2>&1
grep -E 'Contributing diagrams' "$out.log"
P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
python3 patch_check_sa.py "$P/check_sa.f"
(cd "$P" && make check > make.log 2>&1) || { echo "compilation failed, see $P/make.log"; exit 1; }

echo "== (9b) the note's NLO UFO with the FJ counterterms"
for f in nlo_renormalize nlo_writect nlo_fjct nlo_ctrules nlo_dz nlo_fjdelta nlo_ctparams nlo_ufo; do
  echo "== $f"
  wolframscript -file "$f.wl" > "work/$f.log" 2>&1 || { echo "$f failed (work/$f.log)"; exit 1; }
  grep -E '^\([a-z]\) |^renormalized|^written|^NLOCT|^FJ|^decimal' "work/$f.log" | cut -c1-300
done
rm -rf work/SM_NLO_FJ_UFO work/ml_nunu_fj
cp -r generated/SM_NLO_FJ_UFO work/
printf 'import model ./work/SM_NLO_FJ_UFO\ngenerate ve ve~ > vm vm~ [virt=QED]\noutput standalone ./work/ml_nunu_fj\n' > work/ml_nunu_fj.mg5
mg5_aMC work/ml_nunu_fj.mg5 > work/ml_nunu_fj.log 2>&1
grep -E 'Contributing diagrams' work/ml_nunu_fj.log
P=$(ls -d work/ml_nunu_fj/SubProcesses/P0_* | head -1)
python3 patch_check_sa.py "$P/check_sa.f"
(cd "$P" && make check > make.log 2>&1) || { echo "compilation failed, see $P/make.log"; exit 1; }
# the same UFO with a restriction card (light masses and widths 0, as MadGraph's no_widths)
rm -rf work/SM_NLO_FJ_UFO_r work/ml_nunu_fj_r
cp -r generated/SM_NLO_FJ_UFO work/SM_NLO_FJ_UFO_r
python3 nunu_madloop.py --restrict work/ml_nunu_fj/Cards/param_card.dat work/SM_NLO_FJ_UFO_r/restrict_light0.dat
printf 'import model ./work/SM_NLO_FJ_UFO_r-light0\ngenerate ve ve~ > vm vm~ [virt=QED]\noutput standalone ./work/ml_nunu_fj_r\n' > work/ml_nunu_fj_r.mg5
mg5_aMC work/ml_nunu_fj_r.mg5 > work/ml_nunu_fj_r.log 2>&1
grep -E 'Contributing diagrams' work/ml_nunu_fj_r.log
P=$(ls -d work/ml_nunu_fj_r/SubProcesses/P0_* | head -1)
python3 patch_check_sa.py "$P/check_sa.f"
(cd "$P" && make check > make.log 2>&1) || { echo "compilation failed, see $P/make.log"; exit 1; }
python3 nunu_madloop.py
