#!/bin/bash
# Step (7) of the Higgs note: H -> W W*, Z Z* (after run_lo_check.sh: generated/SM_CKM_FA).
#   1. hvv_scheme.wl  : the H H V V tadpole vertex against the tadpole parts of the V self-energies (symbolic, general R_xi);
#                       dW, dZ, DeltaHat and their tadpole parts at mu = M_t; the tree ratio of the FJ v and G_F    (~15 s)
#   2. hvv_widths.py  : the four-fermion widths with the G_mu couplings, the pole masses and the QCD factors of the V decays
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
[ -e generated/SM_CKM_FA ] || { echo "run run_lo_check.sh first"; exit 1; }
wolframscript -file hvv_scheme.wl > work/hvv_scheme.log 2>&1 || { echo "hvv_scheme.wl failed"; exit 1; }
grep -E "^H ->|^\(a\)|^\(b\)|^    [a-z]" work/hvv_scheme.log | cut -c1-250
python3 hvv_widths.py
