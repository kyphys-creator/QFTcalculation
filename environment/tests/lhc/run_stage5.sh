#!/bin/bash
# Stage 5 of the LHC tools (environment.pdf): pyhf 0.7.6, SModelS 3.2.1, HiggsTools 1.3, in the virtual environment ~/hep/opt/lhc.
#   1. test_pyhf.py: pyhf against own one-bin formulas and MadAnalysis5's limit of stage 4 (Spey), and on the ATLAS 1Lbb full
#      likelihood (HEPData ins1755298, ~/hep/data/hepdata-ins1755298): the post-fit backgrounds, CLs on the published contours,
#      the upper limits against the published ones (about 7 minutes, 14 processes; --reuse reads out/stage5_1lbb.csv);
#   2. test_smodels.py: SModelS with the local database subset ~/hep/data/smodels-db-3.2.1 on the gluino point of stage 4
#      (ATLAS-SUSY-2016-07) and a 1Lbb point (ATLAS-SUSY-2019-08), against own interpolation, MadAnalysis5 and own pyhf
#      (about 3 minutes);
#   3. test_higgstools.py: HiggsSignals with HSDataSet v1.1 (~/hep/data/hsdataset-v1.1): the SM chi^2 and the one with the
#      partial widths of the Higgs note (models/sm_higgs).
# Needs stage 4 (out/ma5_gluino, out/ma5_gluino0: run_stage4.sh --controls).  PYTHONNOUSERSITE keeps ~/.local out; the proxy
# variables block the network, so nothing is downloaded (SModelS can fetch databases and resummino by itself).
cd "$(dirname "$0")"
mkdir -p out
[ -d out/ma5_gluino ] || { echo "stage 4 first: ./run_stage4.sh --controls"; exit 1; }
export PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 HTTPS_PROXY=http://127.0.0.1:9 HTTP_PROXY=http://127.0.0.1:9
export SMODELS_CACHEDIR="$PWD/out/smodels-cache"
PY=~/hep/opt/lhc/bin/python
$PY test_pyhf.py "$@" 2>&1 | grep -v "^Thanks for using Spey\|Please make sure to cite\|SciPost Phys\|arxiv.org/abs/arXiv:2307\|^ *$"
$PY test_smodels.py 2>&1 | grep -v "^ *$"
$PY test_higgstools.py 2>&1 | grep -v "\[warning\]\|\[info\]"
