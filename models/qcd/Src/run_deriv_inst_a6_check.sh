#!/bin/bash
# Research note models/qcd: the checks of the m^-8 coefficient of the large-mass expansion of the instanton determinant (app:inst
# 「大きい質量の展開。」, step (10) checks 「文献との食い違い。」, app:details): A_6 = 25624/571725, i.e. c8 = -6 A_6 = -51248/190575, against the
# literature A_6 = 3958/444675 (c8 = -7916/148225).  The printed output of every script is saved as results/deriv_inst_<name>.txt; the scripts
# print no paths or timings there (timings go to stderr, shown here and kept in work/deriv/<name>.err).
#   deriv_inst_gy_hp.py (+ deriv_inst_gy_hp.c,   high-precision Gel'fand-Yaglom: Gamma~ and its u = m^2 derivatives Gamma~'', Gamma~''' at 23
#     deriv_inst_gy_hp_lib.py)                  masses (sensitivity equations) -> results/inst_gy_hp.csv          (about 18 min on 8 processes)
#   deriv_inst_gy_hp_fit.py                     fits for c8, c10, ...: c8 in [-0.2701, -0.2685], chi^2 of both candidates, recursion values
#                                               c8..c14 fixed, c16 against -Gamma(8) A_10                         (seconds)
#   deriv_inst_fhss.py                          FHSS O_2..O_6: constant potentials, rank tests in d = 4, 5, 6, exact BPST A_2..A_6 for
#                                               t = 1/2 and 1        (about 90 min on 8 processes, almost all for the O_6 rank test in d = 6)
#   deriv_inst_klm.py                           KLM's printed a_6 density against the correct one, the 86418 -> 86148 typo (about 1.5 min)
#   deriv_inst_vdv.py                           van de Ven's a_6: passes a_2..a_5, fails a_6 on constant potentials, agrees on BPST
#                                               (about 1 min)
#   deriv_inst_planewave.py 9                   plane-wave expansion mod primes: exact A_2..A_9 against the recursion (about 17 min on
#                                               8 processes)
#   deriv_inst_hk_lib.py                        the shared heat-kernel code (no output of its own)
# With the argument "dewitt10" also deriv_inst_dewitt_modp.py 10 (the recursion values A_9, A_10 used by deriv_inst_gy_hp_fit.py and
# deriv_inst_planewave.py; about 80 minutes, one process) -> results/deriv_inst_dewitt_modp_10.txt.
# The arXiv sources (FHSS hep-th/9707189, van de Ven hep-th/9708152, KLM hep-ph/0008028, DHLM hep-th/0502087) are not in the repository:
# the scripts download them into work/arxiv/<id>/ when missing and only read them (the scripts that read them run with python -I).
# About 2 hours 10 minutes in total (without dewitt10; 7756 s on 2026-10-16).  Not part of run_deriv_check.sh.
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work/deriv results
FAILED=""
# run NAME COMMAND...: stdout -> results/NAME.txt (also shown here), stderr -> work/deriv/NAME.err
run() {
  local name=$1; shift
  local t0=$SECONDS
  echo "=== $name"
  "$@" > "results/$name.txt" 2> "work/deriv/$name.err"
  local rc=$?
  cat "results/$name.txt"
  [ -s "work/deriv/$name.err" ] && sed 's/^/    stderr: /' "work/deriv/$name.err" | tail -n 30
  [ $rc -eq 0 ] || { echo "*** $name: exit code $rc"; FAILED="$FAILED $name"; }
  echo "    ($name: $((SECONDS - t0)) s)"
}

run deriv_inst_gy_hp "$PY" deriv_inst_gy_hp.py
run deriv_inst_gy_hp_fit "$PY" deriv_inst_gy_hp_fit.py
run deriv_inst_fhss "$PY" -I deriv_inst_fhss.py
run deriv_inst_klm "$PY" -I deriv_inst_klm.py
run deriv_inst_vdv "$PY" -I deriv_inst_vdv.py
run deriv_inst_planewave "$PY" deriv_inst_planewave.py 9
if [ "$1" = "dewitt10" ]; then
  run deriv_inst_dewitt_modp_10 "$PY" deriv_inst_dewitt_modp.py 10
fi
echo "##### total $SECONDS s"
if [ -n "$FAILED" ]; then echo "FAILED:$FAILED"; exit 1; fi
echo "all scripts ran (exit code 0)"
