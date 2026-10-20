#!/bin/bash
# Stage 1 of the EFT and dark-matter tools (environment.pdf): wilson and DsixTools.
#   1. wilson's own unit tests, from a copy of its source tree (the installed package lacks two test modules)
#   2. test_eft_stage1.py prepare: the common input (out/stage1_in.json, out/caseA_wcxf.json)
#   3. stage1_dsixtools.wl: the DsixTools side (out/dsix_*.json)
#   4. test_eft_stage1.py check: both tools against own formulas and against each other
# About 3 minutes.
cd "$(dirname "$0")"
PY=~/miniforge3/envs/qft/bin/python
mkdir -p out
rm -rf out/wilson-src && cp -R ~/hep/src/wilson-dl/x/wilson-d21596fa1e10a3018c24208f02c8681dea25e709 out/wilson-src
(cd out/wilson-src && PATH=~/miniforge3/envs/qft/bin:$PATH $PY -m unittest discover -s wilson -t . -p 'test*.py' > ../wilson_unittest.log 2>&1)
echo "wilson unit tests: $(grep -E '^Ran' out/wilson_unittest.log), $(tail -1 out/wilson_unittest.log)"
grep -E '^(FAIL|ERROR):' out/wilson_unittest.log
$PY test_eft_stage1.py prepare
~/hep/bin/wolframscript -file stage1_dsixtools.wl > out/stage1_dsixtools.log 2>&1
grep -E 'done' out/stage1_dsixtools.log
$PY test_eft_stage1.py check
