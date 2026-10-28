#!/bin/bash
# Step (6) of the two-loop note: the phase transition at the next order in the 3D EFT (lam ~ e^3).
#   thermal_nlo.wl : DRalgo 1.5.0 NLO dimensional reduction against Kajantie et al. (hep-lat/9711048) App. B, the soft
#                    two-loop potential in the strict limit against Hirvonen et al. (arXiv:2112.08912), T_c and the
#                    condensate at LO and NLO (gauge invariant), the Landau one- and two-loop potentials for comparison
#                    -> results/thermal_nlo.csv
cd "$(dirname "$0")"
mkdir -p results
wolframscript -file thermal_nlo.wl 2>&1 | grep -E "^\(|written"
