#!/bin/bash
# Step (1) of the CKM note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_SM_CKM.wl : checks (hermiticity, normalisation, masses), all 93 vertex classes against the note's
#                           tables with a general V (and a copy with five deliberate errors), the unitarity rules
#                           against the explicit parametrization, V = 1 against the SM note's vertices; writes generated/
#   2. make_restrict.py   : restrict_massless.dat for MadGraph (the SM note's script: all fermions massless except
#                           the top; the CKM parameters keep their values)
#   3. model_mg5.mg5      : 35 processes in unitary and in Feynman gauge (expected counts in the file)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file generate_SM_CKM.wl
python3 ../../sm/Src/make_restrict.py generated/SM_CKM_UFO
grep -A5 "Block CKMBLOCK" generated/SM_CKM_UFO/restrict_massless.dat
mkdir -p work && rm -rf work/SM_CKM_UFO && cp -R generated/SM_CKM_UFO work/
"$HOME/hep/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
if grep -q -E "No model currently active|not allowed for your current model|No amplitudes generated" work/model_mg5.log; then
  echo "ERROR: MadGraph did not use SM_CKM_UFO in both gauges, or a process has no diagrams (see work/model_mg5.log)"; exit 1
fi
python3 - <<'PYEOF'
import re
procs = [l.split("generate ", 1)[1].strip() for l in open("model_mg5.mg5") if l.startswith("generate ")]
counts = [int(n) for n in re.findall(r"Total: 1 processes with (\d+) diagrams", open("work/model_mg5.log").read())]
#        the SM note's 21 processes (u u~ > w+ w-: 5 here, 3 with V = 1)        processes that need the CKM
hand_u = [2, 4, 2, 1, 2, 2, 3, 1, 2, 5, 3, 7, 4, 4, 4, 3, 8, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 2]
hand_f = [2, 4, 2, 1, 2, 2, 3, 1, 2, 5, 5, 7, 6, 6, 6, 3, 8, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 3]
n = len(hand_u)
assert len(procs) == 2 * n, ("expected %d processes, found %d" % (2 * n, len(procs)))
assert len(counts) == 2 * n, ("expected %d counts, found %d" % (2 * n, len(counts)))
bad = 0
for i, p in enumerate(procs[:n]):
    ok = counts[i] == hand_u[i] and counts[i + n] == hand_f[i]
    bad += not ok
    print("%-20s unitary %d (hand %d)   Feynman %d (hand %d)  %s" % (p, counts[i], hand_u[i], counts[i + n], hand_f[i], "" if ok else "DIFFERENT"))
print("processes that differ from the hand counts:", bad)
PYEOF
# 4. No flavour-changing neutral currents at tree level: MadGraph must find no diagrams (it stops a script at the
#    first such process, so each runs alone); the charged-current process u s~ > e+ ve is the control (1 diagram).
for proc in "d s~ > mu+ mu-" "s b~ > z" "b s~ > a g" "u c~ > e+ e-" "c u~ > z h" "u s~ > e+ ve"; do
  printf 'set automatic_html_opening False\nset gauge Feynman\nimport model ./work/SM_CKM_UFO-massless\ngenerate %s\n' "$proc" > work/fcnc_one.mg5
  out=$("$HOME/hep/bin/mg5_aMC" work/fcnc_one.mg5 2>&1)
  if echo "$out" | grep -q "NoDiagramException"; then echo "FCNC check  $proc : no diagrams"
  else echo "FCNC check  $proc : $(echo "$out" | grep -o 'Total: 1 processes with [0-9]* diagrams')"; fi
done
