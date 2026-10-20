#!/bin/bash
# Research note models/sm_pp, step (3): MC@NLO with Pythia 8 at 13 TeV, NNPDF4.0 NLO (LHAPDF 331700, alpha_s from the set), fixed
# mu_R = mu_F with the factors 1, 2, 1/2 by reweighting, 200000 events each, showered by MG5_aMC's Pythia 8 step (parton level: hadronization, the underlying
# event and the QED shower off; nsplit_jobs = 10) with the analysis py8an_HwU_mc.f:
#   z: p p > e+ e- [QCD], loop_sm-no_b_mass (5 flavours), m_ee > 50 GeV (mll_sf), mu = M_Z = 91.188 GeV (as the run zpeak of dy_mg5.sh);
#   h: p p > h QCD=2 QED=1 [QCD], the note's own NLO UFO (work copy work/gh/QCDH_NLO_UFO of gh_own_madloop.py, its order HIG named
#      QED, below), MH = 125.2 GeV,
#      kHgg = 1, mu = M_H, the Higgs stable in the shower (h_stable).
# The shower card's EXTRAPATHS gets the directory of libgfortran: the Pythia 8 driver (MCatNLO/srcPythia8/Pythia83.cc) is linked by
# clang++ with -lgfortran and no -L for it ("ld: library 'gfortran' not found").  The scale reweighting must stay on: without it the
# events carry no <rwgt> block (jwgtinfo = 0) and MG5's MCatNLO/include/LHEFRead.h (lhef_read_wgts_) loops for ever looking for
# </rwgt>, appending the LHE header to a stringstream at each turn (tens of GB per shower job; ten jobs froze the machine).
# Usage: ./mc_mg5.sh [--reuse] [nevents] (default 200000).
# -> work/mc/<proc>/Events/<run>/ (the showered histograms plot_PYTHIA8*.HwU, read by mc_hadronic.py).  With --reuse, a run that has
# its showered HwU is not run again; otherwise an earlier run of the same name is moved to the trash.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
REUSE=0; [ "$1" = "--reuse" ] && { REUSE=1; shift; }
NEV=${1:-200000}
W=work/mc
mkdir -p $W
GFLIB=$(cd "$(dirname "$(/opt/homebrew/bin/gfortran -print-file-name=libgfortran.dylib)")" && pwd)   # MG5's fortran_compiler
[ -d work/gh/QCDH_NLO_UFO ] || { echo "run gh_own_madloop.py first (work copy of the own NLO UFO)"; exit 1; }
out() { # proc model generate
  if [ ! -d $W/$1/SubProcesses ]; then
    printf 'set automatic_html_opening False\nimport model %s\ndefine p = g u c d s b u~ c~ d~ s~ b~\ndefine j = p\n'\
'generate %s\noutput ./%s -f\n' "$2" "$3" $1 > $W/$1_output.mg5
    (cd $W && ~/hep/bin/mg5_aMC $1_output.mg5 > $1_output.log 2>&1)
    [ -d $W/$1/SubProcesses ] || { echo "MG5 output failed: $W/$1_output.log"; exit 1; }
  fi
  cp py8an_HwU_mc.f $W/$1/MCatNLO/PY8Analyzer/
  sed -i '' -e 's/^\(hadronize *=\) *[TF]/\1 F/' -e 's/^\(ue_enabled *=\) *[TF]/\1 F/' -e 's/^\(qed_shower *=\) *[TF]/\1 F/'\
    -e 's/^\(nsplit_jobs *=\) *[0-9]*/\1 10/' -e 's/^ANALYSE *=.*/ANALYSE      = HwU.o py8an_HwU_mc.o/'\
    -e "s|^EXTRAPATHS *=.*|EXTRAPATHS   = ../lib $GFLIB|" $W/$1/Cards/shower_card.dat
}
out z loop_sm-no_b_mass "p p > e+ e- [QCD]"
# the H: aMC@NLO's event generation (iproc_map.f, add_write_info.f, montecarlocounter.f) reads split_type at the QED position of
# the split orders, which is -1 in a model whose only other order is HIG ('IPROCMAP: NOT IMPLEMENTED' from an out-of-range read): a
# copy of the own UFO's work copy with the order HIG named QED (QED_POS = 2; [QCD] leaves split_type(QED) false), the dummy QED
# order of gh_own_madloop.py dropped
U=$W/QCDH_NLO_UFO_qed
if [ ! -d $U ]; then
  mkdir -p $U && cp work/gh/QCDH_NLO_UFO/*.py $U/
  python3 - $U <<'PYEOF'
import pathlib, sys
u = pathlib.Path(sys.argv[1])
co = u / "coupling_orders.py"
s = co.read_text()
s = s[:s.index("\n# research note models/sm_pp: a QED order")] + "\n"
assert s.count("HIG = CouplingOrder(name = 'HIG',") == 1
co.write_text(s.replace("HIG = CouplingOrder(name = 'HIG',", "QED = CouplingOrder(name = 'QED',"))
for f in ("couplings.py", "CT_couplings.py"):
    p = u / f
    p.write_text(p.read_text().replace("'HIG':", "'QED':"))
PYEOF
fi
out h ./QCDH_NLO_UFO_qed "p p > h QCD=2 QED=1 [QCD]"
sed -i '' 's/^\(h_stable *=\) *[TF]/\1 T/' $W/h/Cards/shower_card.dat
run() { # proc name mu seed extra-settings
  local P=$1 N=$2 MU=$3 S=$4 X=$5
  if [ "$REUSE" = 1 ] && ls $W/$P/Events/$N/plot_PYTHIA8*.HwU > /dev/null 2>&1; then return; fi
  [ -d $W/$P/Events/$N ] && /usr/bin/trash $W/$P/Events/$N
  printf 'set nb_core 10\nlaunch ./%s -n %s\norder=NLO\nfixed_order=OFF\nshower=PYTHIA8\ndone\n'\
'set lpp1 1\nset lpp2 1\nset ebeam1 6500\nset ebeam2 6500\nset pdlabel lhapdf\nset lhaid 331700\n'\
'set fixed_ren_scale True\nset fixed_fac_scale True\nset muR_ref_fixed %s\nset muF_ref_fixed %s\n'\
'set reweight_scale True\nset rw_rscale 1.0 2.0 0.5\nset rw_fscale 1.0 2.0 0.5\nset reweight_PDF False\nset nevents %s\n'\
'set iseed %s\nset ptj 0\nset etaj -1\n%bdone\n' $P $N $MU $MU $NEV $S "$X" > $W/${P}_$N.mg5
  (cd $W && ~/hep/bin/mg5_aMC ${P}_$N.mg5 > ${P}_$N.log 2>&1)
  ls $W/$P/Events/$N/plot_PYTHIA8*.HwU > /dev/null 2>&1 || { echo "MG5 launch failed: $W/${P}_$N.log"; exit 1; }
  echo "$P $N: $(grep -a 'Total cross section' $W/${P}_$N.log | tail -1)"
}
run z ${RUNNAME:-mc} 91.188 71 'set ptl 0\nset etal -1\nset drll 0\nset drll_sf 0\nset mll 0\nset mll_sf 50\n'
run h ${RUNNAME:-mc} 125.2 72 'set MH 125.2\nset kHgg 1.0\n'
