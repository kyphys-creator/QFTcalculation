#!/bin/bash
# Research note models/sm_pp, step (2d): aMC@NLO at fixed order, p p -> x0 / t [QCD] at 13 TeV with HC_NLO_X0-heft (the heavy-top
# effective theory, 5 massless flavours; work copy work/gh/HC_NLO_X0_UFO made by gh_madloop.py), MX0 = 125.2 GeV, NNPDF4.0 NLO (LHAPDF
# 331700, alpha_s from the set), mu_R = mu_F = mu0 = MX0 fixed with the factors 1, 2, 1/2 by reweighting (9 combinations), the
# histograms of analysis_HwU_gh.f.  LO and NLO, req_acc_FO = 3e-4 (runs h_<order>) and 1e-4 with another seed (h_<order>_p);
# mu_R = M/2, 2M as the central scale (runs h_<order>_r05, _r2; HC_NLO_X0's alpha_s in gHgg is not moved by MG5's mu_R
# reweighting).  aMC@NLO generates the real emission by splitting the Born g g > x0, so the IR-finite q qbar -> x0 g is not in
# p p > x0 [QCD]: it is run at LO with MadEvent (work/gh/qqh, run qq; mu_R = mu_F = MX0, no cuts).
# -> work/gh/pph/Events/<run>/MADatNLO.HwU (read by gh_hadronic.py).  With --reuse, nothing is run again that has its HwU.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
REUSE=0; [ "$1" = "--reuse" ] && REUSE=1
W=work/gh
[ -d $W/HC_NLO_X0_UFO ] || { echo "run gh_madloop.py first (work copy of HC_NLO_X0)"; exit 1; }
if [ ! -d $W/pph ]; then
  printf 'set automatic_html_opening False\nimport model ./HC_NLO_X0_UFO-heft\ngenerate p p > x0 / t [QCD]\noutput ./pph -f\n' > $W/pph_output.mg5
  (cd $W && ~/hep/bin/mg5_aMC pph_output.mg5 > pph_output.log 2>&1) || { echo "MG5 output failed: $W/pph_output.log"; exit 1; }
fi
cp analysis_HwU_gh.f $W/pph/FixedOrderAnalysis/
sed -i '' 's/^FO_ANALYSE = .*/FO_ANALYSE = analysis_HwU_gh.o/' $W/pph/Cards/FO_analyse_card.dat
run() { # name order seed accuracy [mu_R]
  local N=$1 O=$2 S=$3 A=$4 R=${5:-125.2}
  if [ "$REUSE" = 1 ] && ls $W/pph/Events/$N/MADatNLO.HwU > /dev/null 2>&1; then return; fi
  printf 'set nb_core 10\nlaunch ./pph -n %s\nfixed_order=ON\norder=%s\ndone\n'\
'set MX0 125.2\nset lpp1 1\nset lpp2 1\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset muR_ref_fixed %s\nset muF_ref_fixed 125.2\n'\
'set reweight_scale True\nset rw_rscale 1.0 2.0 0.5\nset rw_fscale 1.0 2.0 0.5\nset reweight_PDF False\n'\
'set req_acc_FO %s\nset iseed %s\nset ptj 0\nset etaj -1\ndone\n' $N $O $R $A $S > $W/pph_$N.mg5
  (cd $W && ~/hep/bin/mg5_aMC pph_$N.mg5 > pph_$N.log 2>&1) || { echo "MG5 launch failed: $W/pph_$N.log"; exit 1; }
  echo "$N: $(grep -a 'Total cross section' $W/pph_$N.log | tail -1)"
}
run h_LO    LO  51 0.0003
run h_NLO   NLO 52 0.0003
run h_LO_p  LO  53 0.0001
run h_NLO_p NLO 54 0.0001
run h_LO_r05  LO  55 0.0003 62.6
run h_NLO_r05 NLO 56 0.0003 62.6
run h_LO_r2   LO  57 0.0003 250.4
run h_NLO_r2  NLO 58 0.0003 250.4
# q qbar -> x0 g at LO (MadEvent), mu_R = mu_F = MX0, no generation cuts
if ! { [ "$REUSE" = 1 ] && ls $W/qqh/Events/qq/*banner.txt > /dev/null 2>&1; }; then
  printf 'set automatic_html_opening False\nimport model ./HC_NLO_X0_UFO-heft\ndefine q = u c d s b\ndefine qb = u~ c~ d~ s~ b~\n'\
'generate q qb > x0 g / t\nadd process qb q > x0 g / t\noutput ./qqh -f\nlaunch ./qqh -n qq\nshower=OFF\ndone\n'\
'set MX0 125.2\nset nevents 20000\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset scale 125.2\nset dsqrt_q2fact1 125.2\nset dsqrt_q2fact2 125.2\n'\
'set ptj 0\nset etaj -1\nset drjj 0\nset xptj 0\nset use_syst False\nset iseed 59\ndone\n' > $W/qqh.mg5
  (cd $W && ~/hep/bin/mg5_aMC qqh.mg5 > qqh.log 2>&1) || { echo "MG5 q qbar -> x0 g failed: $W/qqh.log"; exit 1; }
  echo "q qbar -> x0 g: $(grep -a 'Cross-section :' $W/qqh.log | tail -1)"
fi
