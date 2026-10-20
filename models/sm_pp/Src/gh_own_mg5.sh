#!/bin/bash
# Research note models/sm_pp, step (2f): aMC@NLO at fixed order, p p -> h [QCD] at 13 TeV with the note's own NLO UFO (QCDH.fr with
# the own g g H R2 and UV vertices, gh_nlo_ufo.wl; work copy work/gh/QCDH_NLO_UFO with inert Z, W, t and a QED order made by
# gh_own_madloop.py),
# MH = 125.2 GeV, kHgg = 1 (no Wilson coefficient), 5 massless flavours, NNPDF4.0 NLO (LHAPDF 331700, alpha_s from the set),
# mu_R = mu_F = mu0 = MH fixed with the factors 1, 2, 1/2 by reweighting (9 combinations; the g g h coupling carries alpha_s as
# QCD = 2, so MG5's mu_R reweighting moves it), the histograms of analysis_HwU_gh.f.  LO and NLO, req_acc_FO = 1e-4 (runs o_LO, o_NLO).
# As with HC_NLO_X0, the IR-finite q qbar -> h g is not in p p > h [QCD].  The orders are given (QCD=2 HIG=1): without them aMC@NLO
# guesses the QED and QCD orders from the model's hierarchy and stops with KeyError 'QED' (the model has no QED order).
# -> work/gh/ppo/Events/<run>/MADatNLO.HwU (read by gh_hadronic.py).  With --reuse, nothing is run again that has its HwU.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
REUSE=0; [ "$1" = "--reuse" ] && REUSE=1
W=work/gh
[ -d $W/QCDH_NLO_UFO ] || { echo "run gh_own_madloop.py first (work copy of the own NLO UFO)"; exit 1; }
if [ ! -d $W/ppo ]; then
  printf 'set automatic_html_opening False\nimport model ./QCDH_NLO_UFO\ndefine p = g u c d s b u~ c~ d~ s~ b~\ndefine j = p\n'\
'generate p p > h QCD=2 HIG=1 [QCD]\noutput ./ppo -f\n' > $W/ppo_output.mg5
  (cd $W && ~/hep/bin/mg5_aMC ppo_output.mg5 > ppo_output.log 2>&1)
  [ -d $W/ppo/SubProcesses ] || { echo "MG5 output failed: $W/ppo_output.log"; exit 1; }
fi
cp analysis_HwU_gh.f $W/ppo/FixedOrderAnalysis/
sed -i '' 's/^FO_ANALYSE = .*/FO_ANALYSE = analysis_HwU_gh.o/' $W/ppo/Cards/FO_analyse_card.dat
run() { # name order seed accuracy
  local N=$1 O=$2 S=$3 A=$4
  if [ "$REUSE" = 1 ] && ls $W/ppo/Events/$N/MADatNLO.HwU > /dev/null 2>&1; then return; fi
  printf 'set nb_core 10\nlaunch ./ppo -n %s\nfixed_order=ON\norder=%s\ndone\n'\
'set MH 125.2\nset kHgg 1.0\nset lpp1 1\nset lpp2 1\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset muR_ref_fixed 125.2\nset muF_ref_fixed 125.2\n'\
'set reweight_scale True\nset rw_rscale 1.0 2.0 0.5\nset rw_fscale 1.0 2.0 0.5\nset reweight_PDF False\n'\
'set req_acc_FO %s\nset iseed %s\nset ptj 0\nset etaj -1\ndone\n' $N $O $A $S > $W/ppo_$N.mg5
  (cd $W && ~/hep/bin/mg5_aMC ppo_$N.mg5 > ppo_$N.log 2>&1)
  ls $W/ppo/Events/$N/MADatNLO.HwU > /dev/null 2>&1 || { echo "MG5 launch failed: $W/ppo_$N.log"; exit 1; }
  echo "$N: $(grep -a 'Total cross section' $W/ppo_$N.log | tail -1)"
}
run o_LO  LO  61 0.0001
run o_NLO NLO 62 0.0001
