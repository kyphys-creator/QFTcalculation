#!/bin/bash
# Step (1) of the SM note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_SM.wl   : checks (hermiticity, normalisation, masses), all 93 vertex classes against the note's
#                         tables (and a copy with three deliberate errors), writes generated/
#   2. make_restrict.py : restrict_massless.dat for MadGraph (all fermions massless except the top)
#   3. model_mg5.mg5    : 21 processes in unitary and in Feynman gauge (expected counts in the file)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file generate_SM.wl
python3 make_restrict.py generated/SM_UFO
mkdir -p work && rm -rf work/SM_UFO && cp -R generated/SM_UFO work/
"$HOME/hep/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
if grep -q -E "No model currently active|not allowed for your current model" work/model_mg5.log; then
  echo "ERROR: MadGraph did not use SM_UFO in both gauges (see work/model_mg5.log)"; exit 1
fi
python3 - <<'PYEOF'
import re
procs = [l.split("generate ", 1)[1].strip() for l in open("model_mg5.mg5") if l.startswith("generate ")]
counts = [int(n) for n in re.findall(r"Total: 1 processes with (\d+) diagrams", open("work/model_mg5.log").read())]
hand_u = [2, 4, 2, 1, 2, 2, 3, 1, 2, 3, 3, 7, 4, 4, 4, 3, 8, 1, 1, 1, 1]
hand_f = [2, 4, 2, 1, 2, 2, 3, 1, 2, 3, 5, 7, 6, 6, 6, 3, 8, 1, 1, 1, 1]
n = len(hand_u)
assert len(counts) == 2 * n, ("expected %d counts, found %d" % (2 * n, len(counts)))
bad = 0
for i, p in enumerate(procs[:n]):
    ok = counts[i] == hand_u[i] and counts[i + n] == hand_f[i]
    bad += not ok
    print("%-20s unitary %d (hand %d)   Feynman %d (hand %d)  %s" % (p, counts[i], hand_u[i], counts[i + n], hand_f[i], "" if ok else "DIFFERENT"))
print("processes that differ from the hand counts:", bad)
PYEOF
