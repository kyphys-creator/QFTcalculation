#!/bin/bash
# Research note models/qcd: the checks of the derivations in the appendices (scripts deriv_*; each header names the appendix paragraphs).
# The printed output of every script is saved as results/deriv_<name>.txt (FeynArts loader messages and timings removed), so that a rerun
# can be compared with the committed files (environment/interactive/samefiles.sh).
#   app:ren, app:os        deriv_ren_os.py            quark loop (a4), quark self-energy (c), on-shell mass and residues (R1-R4)
#                          deriv_ren_dirac.wl         D-dimensional Dirac algebra of (a4), (c) and of the vertex (d1), (d2) (FeynCalc)
#   app:rules, app:st      deriv_rules_brst.py        gluon propagator, counterterm two-point rules, BRST nilpotency for SU(3) (R5, R6)
#   app:vertex             deriv_vertex_d1_v3.wl      UV poles of (d1), (d2) and of the three-gluon vertex per class, tab:v3class (FeynArts)
#                          deriv_vertex_4g.wl         UV poles of the four-gluon vertex per class, SU(3) projections (FeynArts)
#                          deriv_vertex_bose.py       the unique Bose-antisymmetric rank-3 tensor = tree three-gluon vertex
#   app:color, app:tree    deriv_color.py, .wl        colour algebra (explicit SU(2), SU(3), SU(4) matrices; FeynCalc for general N), gg -> gg
#                          deriv_tree_B.py, .wl       g g -> Q Qbar: colour-split spin sums, -g sums and ghosts (numerical; traces)
#                          deriv_tree_C.py, .wl       g g -> g g: colour decomposition, linear-polarization table, polarization sum
#   app:hq                 deriv_hq_pwave.py          the [T^a,T^b] part of g g -> Q Qbar is a p wave (threshold Coulomb term)
#   app:ee, app:tree (D)   deriv_ee_feyncalc.wl       D-dimensional traces of the real and virtual corrections (FeynCalc)
#                          deriv_ee_sympy.py          reduction of the vertex, C0/B0, Dirichlet integrals, r_V, r_R, phase space
#                          deriv_ee_thrust_rmass.py   thrust (Eq. (thrust)) and the limits of Eq. (rmass)
#   app:rg                 deriv_twoloop_perdiag.wl   per-diagram two-loop self-energies (FeynArts, FeynCalc, Kira) -> results/twoloop_perdiag.m
#                          deriv_twoloop_export.wl    class sums and diagram (c) -> results/twoloop_latex_ref.txt, results/twoloop_diag4.txt
#                          deriv_twoloop_table.wl     tab:twoloopclass, tab:twoloopclassgh, z_22, z_21, beta_1, the finite parts
#                          deriv_twoloop_latex.py     the two tables as typed in ../ResearchNote/note.tex against the pipeline
#                          deriv_twoloop_cftf.py      the C_F T_F n_f part by hand (diagram (c)) against the pipeline
#                          deriv_twoloop_trace.wl     the Dirac algebra of diagram (c) (FeynCalc)
#   app:inst               deriv_inst_spinor.py       the vector fluctuation operator in 2x2 form, the sign of M_A (N1)
#                          deriv_inst_cn.py           SU(N) orientation zero modes, Vol(SU(N)/H), C_N (N3)
#                          deriv_inst_smallmass.wl    the small-mass term by covariant point splitting (N2a)
#                          deriv_inst_a4_constpot.py  heat-kernel b_2, b_3, b_4 for constant potentials against FHSS O_n (N2b)
#                          deriv_inst_a4_bpst.wl      the seven terms of O_4 on BPST (N2b)
#                          deriv_inst_dewitt.wl       DeWitt recursion on BPST, exact, A_2..A_4 (argument 4)
#                          deriv_inst_dewitt_modp.py  DeWitt recursion mod p, exact A_2..A_8 (argument 8; in the background)
#                          deriv_inst_dewitt_num.py   DeWitt recursion in floating point ("4 both": t = 1/2 and 1; "7": A_2..A_7)
#                          deriv_inst_largem_gy.py    the large-mass expansion against results/inst_gy.csv (N2c)
#                          deriv_inst_clover.py       the O(a^2) term of the clover charge, results/inst_lattice.csv (N4)
#   not run here (about 2 hours, 8 processes): run_deriv_inst_a6_check.sh, the m^-8 coefficient A_6 by independent routes:
#                          deriv_inst_gy_hp*.py (high-precision Gel'fand-Yaglom, fits), deriv_inst_fhss.py, deriv_inst_klm.py,
#                          deriv_inst_vdv.py, deriv_inst_planewave.py (with deriv_inst_hk_lib.py); outputs results/deriv_inst_*.txt
#   last, each skipped with a message when its input is missing:
#   app:ir                 deriv_ir_poles.py          one-loop IR poles, gamma_i, tab:scat (needs work/hq/born.m from run_hq_check.sh)
#   app:hq                 deriv_hq_thrlog.py         threshold logarithms of Eq. (hqthr) (needs work/hq/born.m, assemble_*.log)
#                          deriv_hq_thr_cm.wl         the exact f^(1) of Czakon-Mitov near threshold (needs ../Ref/cm08_src, see hq_cm.wl)
# Every script runs in a wolframscript or python process of its own (the FeynCalc scripts never share a kernel with plain Mathematica).
# Needs generated/ (run_model_check.sh) and Kira 3.1 (environment.pdf, Sec. 8).  About 20 minutes (the longest: deriv_vertex_4g.wl,
# deriv_hq_thr_cm.wl, deriv_twoloop_perdiag.wl, deriv_vertex_d1_v3.wl, deriv_ee_sympy.py, 2 to 4 minutes each; deriv_inst_dewitt_modp.py 8,
# about 4 minutes, runs in the background in parallel with the rest).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work/deriv results
FAILED=""
# the check lines of the FeynArts scripts (the loader messages contain temporary paths), and no timings
checklines() { grep -E '^\(' | notime; }
notime() { sed -E -e 's/  \[[0-9]+ s\]$//' -e '/(done|algebra) in [0-9]+ s\)?$/d'; }
# run NAME FILTER COMMAND...: the output (stdout, and the messages of wolframscript) -> results/NAME.txt, also shown here
run() {
  local name=$1 filter=$2; shift 2
  local t0=$SECONDS
  echo "=== $name"
  if [ "$1" = "wolframscript" ]; then
    "$@" > "work/deriv/$name.log" 2>&1
  else
    "$@" > "work/deriv/$name.log"
  fi
  local rc=$?
  $filter < "work/deriv/$name.log" > "results/$name.txt"
  cat "results/$name.txt"
  [ $rc -eq 0 ] || { echo "*** $name: exit code $rc"; FAILED="$FAILED $name"; }
  echo "    ($name: $((SECONDS - t0)) s)"
}

# deriv_inst_dewitt_modp.py 8 (about 4 minutes, python only) in the background: its output is shown at the end
( t0=$SECONDS; "$PY" deriv_inst_dewitt_modp.py 8 > work/deriv/deriv_inst_dewitt_modp.log; echo $? > work/deriv/deriv_inst_dewitt_modp.rc
  echo $((SECONDS - t0)) > work/deriv/deriv_inst_dewitt_modp.time ) &
MODP=$!

echo "##### app:ren, app:os, app:rules, app:st, app:vertex"
run deriv_ren_os cat "$PY" deriv_ren_os.py
run deriv_ren_dirac cat wolframscript -file deriv_ren_dirac.wl
run deriv_rules_brst cat "$PY" deriv_rules_brst.py
run deriv_vertex_bose cat "$PY" deriv_vertex_bose.py
run deriv_vertex_d1_v3 checklines wolframscript -file deriv_vertex_d1_v3.wl
run deriv_vertex_4g checklines wolframscript -file deriv_vertex_4g.wl

echo "##### app:color, app:tree, app:hq (Coulomb)"
run deriv_color cat "$PY" deriv_color.py
run deriv_color_wl cat wolframscript -file deriv_color.wl
run deriv_tree_B cat "$PY" deriv_tree_B.py
run deriv_tree_B_wl cat wolframscript -file deriv_tree_B.wl
run deriv_tree_C cat "$PY" deriv_tree_C.py
run deriv_tree_C_wl cat wolframscript -file deriv_tree_C.wl
run deriv_hq_pwave cat "$PY" deriv_hq_pwave.py

echo "##### app:ee"
run deriv_ee_feyncalc cat wolframscript -file deriv_ee_feyncalc.wl
run deriv_ee_sympy cat "$PY" deriv_ee_sympy.py
run deriv_ee_thrust_rmass cat "$PY" deriv_ee_thrust_rmass.py

echo "##### app:rg (the per-diagram pipeline first)"
run deriv_twoloop_perdiag checklines wolframscript -file deriv_twoloop_perdiag.wl
run deriv_twoloop_export cat wolframscript -file deriv_twoloop_export.wl
run deriv_twoloop_table cat wolframscript -file deriv_twoloop_table.wl
run deriv_twoloop_latex cat "$PY" deriv_twoloop_latex.py
run deriv_twoloop_cftf cat "$PY" deriv_twoloop_cftf.py
run deriv_twoloop_trace cat wolframscript -file deriv_twoloop_trace.wl

echo "##### app:inst"
run deriv_inst_spinor cat "$PY" deriv_inst_spinor.py
run deriv_inst_cn cat "$PY" deriv_inst_cn.py
run deriv_inst_smallmass cat wolframscript -file deriv_inst_smallmass.wl
run deriv_inst_a4_constpot cat "$PY" deriv_inst_a4_constpot.py
run deriv_inst_a4_bpst cat wolframscript -file deriv_inst_a4_bpst.wl
run deriv_inst_dewitt cat wolframscript -file deriv_inst_dewitt.wl 4
run deriv_inst_dewitt_num_4both cat "$PY" deriv_inst_dewitt_num.py 4 both
run deriv_inst_dewitt_num_7 cat "$PY" deriv_inst_dewitt_num.py 7
run deriv_inst_largem_gy cat "$PY" deriv_inst_largem_gy.py
run deriv_inst_clover cat "$PY" deriv_inst_clover.py

echo "##### inputs that are not in the repository"
if [ -f work/hq/born.m ]; then
  run deriv_ir_poles cat "$PY" deriv_ir_poles.py
else
  echo "=== deriv_ir_poles: skipped (work/hq/born.m is missing: run run_hq_check.sh first)"
fi
if [ -f work/hq/born.m ] && [ -f work/hq/assemble_qq.log ] && [ -f work/hq/assemble_gg.log ]; then
  run deriv_hq_thrlog cat "$PY" deriv_hq_thrlog.py
else
  echo "=== deriv_hq_thrlog: skipped (work/hq/born.m or work/hq/assemble_{qq,gg}.log is missing: run run_hq_check.sh first)"
fi
if [ -f ../Ref/cm08_src/x/NLOXSections.m ]; then
  run deriv_hq_thr_cm notime wolframscript -file deriv_hq_thr_cm.wl
else
  echo "=== deriv_hq_thr_cm: skipped (../Ref/cm08_src/x/NLOXSections.m is missing; see hq_cm.wl for the download)"
fi

echo "=== deriv_inst_dewitt_modp (background job)"
wait $MODP
cp work/deriv/deriv_inst_dewitt_modp.log results/deriv_inst_dewitt_modp.txt
cat results/deriv_inst_dewitt_modp.txt
[ "$(cat work/deriv/deriv_inst_dewitt_modp.rc)" = "0" ] || { echo "*** deriv_inst_dewitt_modp: exit code $(cat work/deriv/deriv_inst_dewitt_modp.rc)"; FAILED="$FAILED deriv_inst_dewitt_modp"; }
echo "    (deriv_inst_dewitt_modp: $(cat work/deriv/deriv_inst_dewitt_modp.time) s)"
echo "##### total $SECONDS s"
if [ -n "$FAILED" ]; then echo "FAILED:$FAILED"; exit 1; fi
echo "all scripts ran (exit code 0)"
