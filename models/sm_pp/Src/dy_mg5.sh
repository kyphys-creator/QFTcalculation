#!/bin/bash
# Research note models/sm_pp, step (1b): aMC@NLO at fixed order, p p -> e+ e- (gamma*/Z), e+ ve (W+), e- ve~ (W-) [QCD] at 13 TeV,
# MG5's loop_sm with massless b (loop_sm-no_b_mass: 5 flavours, b in p), NNPDF4.0 NLO (LHAPDF 331700, alpha_s from the set),
# fixed mu_R = mu_F = mu0, the scale factors 1, 2, 1/2 for mu_R and mu_F by reweighting (9 combinations), no lepton cuts but
# m_ee > mll_sf; the histograms of analysis_HwU_dy.f.  LO and NLO.  -> work/dy/<proc>/Events/<run>/MADatNLO.HwU (read by
# dy_hadronic.py).  Runs (proc, run name, mll_sf, mu0):
#   z     zpeak   50   91.188     (m_ee 50-150 GeV, the window 66-116)
#   z     zhigh   500  1000       (m_ee 0.5-3.5 TeV)
#   wp    wpeak   -    80.419002  (M_W of the param card's inputs)
#   wm    wpeak   -    80.419002
# Each at req_acc_FO = 3e-4 (runs <run>_<order>) and again with another seed (<run>_<order>_p) at 1e-4 (W at NLO: 3e-4;
# without a cut on m_enu its integration converges slowly, about 30 minutes at 3e-4).
# With --reuse, nothing is run again that has a MADatNLO.HwU.  About 2.5 hours on 10 cores.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
REUSE=0; [ "$1" = "--reuse" ] && REUSE=1
W=work/dy
mkdir -p $W
if [ ! -d $W/z ] || [ ! -d $W/wp ] || [ ! -d $W/wm ]; then
  printf 'set automatic_html_opening False\nimport model loop_sm-no_b_mass\ndefine p = g u c d s b u~ c~ d~ s~ b~\ndefine j = p\n'\
'generate p p > e+ e- [QCD]\noutput ./%s/z -f\ngenerate p p > e+ ve [QCD]\noutput ./%s/wp -f\n'\
'generate p p > e- ve~ [QCD]\noutput ./%s/wm -f\n' $W $W $W > $W/output.mg5
  ~/hep/bin/mg5_aMC $W/output.mg5 > $W/output.log 2>&1 || { echo "MG5 output failed: $W/output.log"; exit 1; }
fi
for P in z wp wm; do
  cp analysis_HwU_dy.f $W/$P/FixedOrderAnalysis/
  sed -i '' 's/^FO_ANALYSE = .*/FO_ANALYSE = analysis_HwU_dy.o/' $W/$P/Cards/FO_analyse_card.dat
done
run() { # proc name order mll_sf mu0 seed [accuracy suffix]
  local P=$1 N=$2 O=$3 M=$4 MU=$5 S=$6 A=${7:-0.0003} X=$8
  if [ "$REUSE" = 1 ] && ls $W/$P/Events/${N}_$O$X/MADatNLO.HwU > /dev/null 2>&1; then return; fi
  printf 'set nb_core 10\nlaunch ./%s/%s -n %s_%s%s\nfixed_order=ON\norder=%s\ndone\n'\
'set lpp1 1\nset lpp2 1\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset muR_ref_fixed %s\nset muF_ref_fixed %s\n'\
'set reweight_scale True\nset rw_rscale 1.0 2.0 0.5\nset rw_fscale 1.0 2.0 0.5\nset reweight_PDF False\n'\
'set req_acc_FO %s\nset iseed %s\nset ptl 0\nset etal -1\nset drll 0\nset drll_sf 0\nset mll 0\nset mll_sf %s\n'\
'set ptj 0\nset etaj -1\ndone\n' $W $P $N $O "$X" $O $MU $MU $A $S $M > $W/${P}_${N}_$O$X.mg5
  ~/hep/bin/mg5_aMC $W/${P}_${N}_$O$X.mg5 > $W/${P}_${N}_$O$X.log 2>&1 || { echo "MG5 launch failed: $W/${P}_${N}_$O$X.log"; exit 1; }
  echo "$P $N $O$X: $(grep -a 'Total cross section' $W/${P}_${N}_$O$X.log | tail -1)"
}
run z  zpeak LO  50  91.188    11
run z  zpeak NLO 50  91.188    12
run z  zhigh LO  500 1000      13
run z  zhigh NLO 500 1000      14
run wp wpeak LO  0   80.419002 15
run wp wpeak NLO 0   80.419002 16
run wm wpeak LO  0   80.419002 17
run wm wpeak NLO 0   80.419002 18
run z  zpeak LO  50  91.188    21 0.0001 _p
run z  zpeak NLO 50  91.188    22 0.0001 _p
run z  zhigh LO  500 1000      23 0.0001 _p
run z  zhigh NLO 500 1000      24 0.0001 _p
run wp wpeak LO  0   80.419002 25 0.0001 _p
run wp wpeak NLO 0   80.419002 26 0.0003 _p
run wm wpeak LO  0   80.419002 27 0.0001 _p
run wm wpeak NLO 0   80.419002 28 0.0003 _p
# the W tails (histograms 9-13 of analysis_HwU_dy.f, added after the runs above): runs <run>_<order>_t
run wp wpeak LO  0   80.419002 35 0.0001 _t
run wp wpeak NLO 0   80.419002 36 0.0003 _t
run wm wpeak LO  0   80.419002 37 0.0001 _t
run wm wpeak NLO 0   80.419002 38 0.0003 _t
