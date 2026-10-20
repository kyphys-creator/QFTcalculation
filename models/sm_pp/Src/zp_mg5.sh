#!/bin/bash
# Research note models/sm_pp, step (4c): aMC@NLO at fixed order, p p -> e+ e- [QCD] through the SSM Z' with the note's NLO UFO
# (QCDZp.fr; work copy work/zp/QCDZp_NLO_UFO with inert Z, W, t made by zp_madloop.py) at 13 TeV, MZp = 1, 3, 5 TeV with the
# widths of stage 6 (MadWidth), NNPDF4.0 NLO (LHAPDF 331700), mu_R = mu_F = MZp fixed with the factors 1, 2, 1/2 by reweighting,
# m_ee > 225 GeV (mll_sf, as the search's selection), no other cuts, the histograms of analysis_HwU_zp.f.  LO and NLO,
# req_acc_FO = 1e-3 (the 3 TeV NLO also at 3e-4, run m3000_NLO_p).  -> work/zp/ppzp/Events/<run>/MADatNLO.HwU (read by zp_compare.py).  With --reuse, nothing is run again
# that has its HwU.  About 15 minutes on 10 cores.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
REUSE=0; [ "$1" = "--reuse" ] && REUSE=1
W=work/zp
[ -d $W/QCDZp_NLO_UFO ] || { echo "run zp_madloop.py first (work copy of the NLO UFO)"; exit 1; }
if [ ! -d $W/ppzp/SubProcesses ]; then
  printf 'set automatic_html_opening False\nimport model ./QCDZp_NLO_UFO\ndefine p = g u c d s u~ c~ d~ s~\ndefine j = p\n'\
'generate p p > e+ e- [QCD]\noutput ./ppzp -f\n' > $W/ppzp_output.mg5
  (cd $W && ~/hep/bin/mg5_aMC ppzp_output.mg5 > ppzp_output.log 2>&1)
  [ -d $W/ppzp/SubProcesses ] || { echo "MG5 output failed: $W/ppzp_output.log"; exit 1; }
fi
cp analysis_HwU_zp.f $W/ppzp/FixedOrderAnalysis/
sed -i '' 's/^FO_ANALYSE = .*/FO_ANALYSE = analysis_HwU_zp.o/' $W/ppzp/Cards/FO_analyse_card.dat
run() { # name order mass width seed [accuracy]
  local N=$1 O=$2 M=$3 G=$4 S=$5 A=${6:-0.001}
  if [ "$REUSE" = 1 ] && ls $W/ppzp/Events/$N/MADatNLO.HwU > /dev/null 2>&1; then return; fi
  printf 'set nb_core 10\nlaunch ./ppzp -n %s\nfixed_order=ON\norder=%s\ndone\n'\
'set MZp %s\nset WZp %s\nset lpp1 1\nset lpp2 1\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset muR_ref_fixed %s\nset muF_ref_fixed %s\n'\
'set reweight_scale True\nset rw_rscale 1.0 2.0 0.5\nset rw_fscale 1.0 2.0 0.5\nset reweight_PDF False\n'\
'set req_acc_FO %s\nset iseed %s\nset ptl 0\nset etal -1\nset drll 0\nset drll_sf 0\nset mll 0\nset mll_sf 225\n'\
'set ptj 0\nset etaj -1\ndone\n' $N $O $M $G $M $M $A $S > $W/ppzp_$N.mg5
  (cd $W && ~/hep/bin/mg5_aMC ppzp_$N.mg5 > ppzp_$N.log 2>&1)
  ls $W/ppzp/Events/$N/MADatNLO.HwU > /dev/null 2>&1 || { echo "MG5 launch failed: $W/ppzp_$N.log"; exit 1; }
  echo "$N: $(grep -a 'Total cross section' $W/ppzp_$N.log | tail -1)"
}
run m1000_LO  LO  1000 29.1391 81
run m1000_NLO NLO 1000 29.1391 82
run m3000_LO  LO  3000 88.6729 83
run m3000_NLO NLO 3000 88.6729 84
run m5000_LO  LO  5000 147.960 85
run m5000_NLO NLO 5000 147.960 86
# the 3 TeV NLO again with another seed and req_acc_FO = 3e-4 (the m_ee > 225 GeV total of the first run was 2.9 sigma high)
run m3000_NLO_p NLO 3000 88.6729 87 0.0003
