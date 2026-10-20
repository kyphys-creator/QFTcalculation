#!/bin/bash
# Stage 4 of the LHC tools (environment.pdf): MadAnalysis5 1.11.0 with its FastJet 3.4.1 and the PADForSFS analyses.
#   The benchmark of Sec. 5.2 of Araz, Fuks, Polykratis (arXiv:2006.09387): a 1 TeV gluino and an 825 GeV lightest
#   neutralino, everything else at 4.5 TeV, g~ -> q q~ chi0_1 with a branching ratio of 1.
#   1. MG5 (MSSM_SLHA2): p p > go go + 0, 1, 2 jets, MLM (xqcut 125 GeV, qCut 187.5 GeV), nn23lo1 (= Pythia's default ISR
#      PDF), the masses and the gluino decay table of set_gluino_card.py, the squark widths (Auto in the card) from MadWidth
#      with the two-body decays only (compute_widths --body_decay=2 at the card prompt: MG5's own Auto goes to four-body
#      decays, and integrates hundreds of channels for nothing here), MadSpin: decay go > q q n1 (q = u, c, d, s, b),
#      Pythia 8, 50000 events (out/gluino_proc);
#   2. MadAnalysis5 (PADForSFS, recast mode, with Spey in ~/hep/opt/lhc): atlas_susy_2016_07 with its ATLAS SFS card
#      (out/ma5_gluino);
#   3. test_ma5.py: the cutflows of the three signal regions of Table 9 of the paper (Meff-3j-1300, Meff-4j-1400,
#      Meff-6j-1200), normalized to its 7262.2 initial events, against the paper's PAD and SFS columns (references).
# With --controls, also three samples of 20000 events through the same analysis: p p > go go alone (the jets from
#   Pythia's shower; out/gluino0_proc), + 0, 1 jet (MLM as above; out/gluino1_proc), and + 0, 1, 2 jets with twice the
#   matching scales (xqcut 250 GeV, qCut 375 GeV; out/gluino2x_proc).
# Output in ./out.  About 16 minutes (40 with --controls; 2.7 GB of HepMC, 7 GB with --controls).  With --reuse, a sample
# is not generated again when its HepMC file exists, nor analysed again when its cutflows exist.
cd "$(dirname "$0")"
HERE=$(pwd)
export ROOTSYS="$HOME/hep/root-6.32.14"
MA5="$HOME/hep/MG5_aMC_v3_8_1/HEPTools/madanalysis5/madanalysis5"
# MadSpin builds its decay matrix elements with numpy's f2py, which needs meson and ninja (environment.pdf: buildtools)
export PATH="$HOME/hep/opt/meson-ninja/bin:$PATH"
REUSE=0; CONTROLS=0
for a in "$@"; do
  case "$a" in
    --reuse) REUSE=1 ;;
    --controls) CONTROLS=1 ;;
  esac
done
mkdir -p out

# 1. a signal sample: sample <tag> <jets from the matrix elements: 0, 1, 2> <events> [<xqcut in GeV, 125 by default>]
sample () {
  local tag=$1 nj=$2 nev=$3 xq=${4:-125}
  if [ "$REUSE" = 1 ] && ls out/${tag}_proc/Events/run_01_decayed_1/*.hepmc.gz > /dev/null 2>&1; then return 0; fi
  { echo "import model MSSM_SLHA2"; echo "generate p p > go go @0"
    [ "$nj" -ge 1 ] && echo "add process p p > go go j @1"
    [ "$nj" -ge 2 ] && echo "add process p p > go go j j @2"
    echo "output $HERE/out/${tag}_proc -f"; } > out/${tag}_output.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/${tag}_output.mg5") > out/${tag}_output.log 2>&1 \
    || { echo "MG5 output failed: out/${tag}_output.log"; return 1; }
  python3 set_gluino_card.py out/${tag}_proc || return 1
  cat > out/${tag}_proc/Cards/madspin_card.dat <<'CARD'
set max_weight_ps_point 400
set Nevents_for_max_weight 250
define q = u c d s b u~ c~ d~ s~ b~
decay go > q q n1
launch
CARD
  { echo "launch $HERE/out/${tag}_proc"; echo "shower=Pythia8"; echo "madspin=ON"; echo "done"
    echo "set nevents $nev"; echo "set ebeam1 6500"; echo "set ebeam2 6500"; echo "set use_syst False"
    [ "$nj" -ge 1 ] && { echo "set ickkw 1"; echo "set xqcut $xq"; echo "set JetMatching:qCut $(echo "1.5 * $xq" | bc)"; }
    echo "set HEPMCoutput:file hepmc.gz"; echo "compute_widths --body_decay=2"; echo "done"; } > out/${tag}_launch.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/${tag}_launch.mg5") > out/${tag}_launch.log 2>&1 \
    || { echo "MG5 launch failed: out/${tag}_launch.log"; return 1; }
}

# 2. MadAnalysis5, PADForSFS: recast <tag>
#   with the Python of ~/hep/opt/lhc (Spey, which its recast mode requires), in the reco mode (-R: the recast mode, which
#   then reads the HepMC events); g++ etc. from ~/hep/opt/apple-cc/bin (Apple clang, not MESA's GCC first in PATH).
#   After a change of MA5's installation_options.dat, add -b once (rebuild SampleAnalyzer)
recast () {
  local tag=$1 hep
  if [ "$REUSE" = 1 ] && ls out/ma5_${tag}/Output/SAF/*/atlas_susy_2016_07/Cutflows/*.saf > /dev/null 2>&1; then return 0; fi
  hep=$(ls out/${tag}_proc/Events/run_01_decayed_1/*.hepmc.gz 2>/dev/null | head -1)
  [ -n "$hep" ] || { echo "no HepMC file of the decayed run of $tag"; return 1; }
  python3 make_recast.py "$HERE/out/${tag}_launch.log" "$HERE/$hep" "$HERE/out/ma5_${tag}.ma5" "$HERE/out/ma5_recast_card.dat" \
    "$HERE/out/ma5_${tag}" || return 1
  (cd "$MA5" && PATH="$HOME/hep/opt/apple-cc/bin:$ROOTSYS/bin:$HOME/hep/opt/lhc/bin:$PATH" \
     ~/hep/opt/lhc/bin/python -W ignore bin/ma5 -R -f -s "$HERE/out/ma5_${tag}.ma5") > out/ma5_${tag}.log 2>&1 \
    || { echo "MadAnalysis5 failed: out/ma5_${tag}.log"; return 1; }
}

sample gluino 2 50000 && recast gluino || exit 1
if [ "$CONTROLS" = 1 ]; then
  sample gluino0 0 20000 && recast gluino0 || exit 1
  sample gluino1 1 20000 && recast gluino1 || exit 1
  sample gluino2x 2 20000 250 && recast gluino2x || exit 1
fi
# 3. the cutflows
python3 test_ma5.py
