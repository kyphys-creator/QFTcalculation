#!/bin/zsh
# Cross-checks with the remaining thermal tools of the loop-tools review (research note models/phi34_thermal, step (11)):
#   1. review_tools/phasetracer_dine.cpp + bsmpt_dine.cpp, driven by review_tools/review_tools_check.py (env qft)
#        PhaseTracer 2.2.2 (~/hep/PhaseTracer-2.2.2) and BSMPT 3.2.0 (~/hep/BSMPT-3.2.0)  -> results/review_tools_check.csv
#   2. review_tools/transitionlistener_check.py (env tl): TransitionListener 2.1.0        -> results/transitionlistener_check.csv
# Needs results/{dine_form,strong_pt}.csv.  About 5 minutes.
cd "$(dirname "$0")/review_tools"
mkdir -p build ../results
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
P=$HOME/hep/PhaseTracer-2.2.2; B=/opt/homebrew
c++ -O2 -std=c++17 -DBOOST_LOG_DYN_LINK -I$B/include/eigen3 -I$P/EffectivePotential/include/effectivepotential \
  -I$P/EffectivePotential/include -I$HOME/hep/include/alglib -I$P/include -isystem $B/include phasetracer_dine.cpp \
  -o build/phasetracer_dine -Wl,-rpath,$P/lib -Wl,-rpath,$P/EffectivePotential/lib $P/lib/libphasetracer.dylib \
  $P/EffectivePotential/lib/libeffectivepotential.dylib $B/lib/libnlopt.dylib $B/lib/libboost_log-mt.dylib \
  $B/lib/libboost_filesystem-mt.dylib $B/lib/libboost_atomic-mt.dylib $B/lib/libboost_chrono-mt.dylib \
  $B/lib/libboost_thread-mt.dylib $B/lib/libboost_system-mt.dylib $HOME/hep/lib/libalglib.a
S=$HOME/hep/BSMPT-3.2.0; L=$S/build/src
c++ -O2 -std=gnu++17 -DNLOPT_DLL -I$S/include -I$S/build/include -isystem $B/include -isystem $B/include/eigen3 bsmpt_dine.cpp \
  -o build/bsmpt_dine -Wl,-rpath,$B/lib $L/transition_tracer/libTransitionTracer.a $L/gravitational_waves/libGW.a \
  $L/bounce_solution/libBounceSolution.a $L/minimum_tracer/libMinimumTracer.a $L/minimizer/libMinimizer.a \
  $L/models/libModels.a $L/ThermalFunctions/libThermalFunctions.a $L/utility/libUtility.a \
  $L/utility/asciiplotter/libASCIIPlotter.a $L/utility/spline/libSpline.a $B/lib/libgsl.dylib $B/lib/libgslcblas.dylib \
  $B/lib/libnlopt.dylib
~/miniforge3/envs/qft/bin/python review_tools_check.py
~/miniforge3/envs/tl/bin/python transitionlistener_check.py 2>/dev/null | grep -E "^(SM-like|BP[0-9]|wrote)"
