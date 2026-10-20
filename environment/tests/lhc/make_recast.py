"""Write the MadAnalysis5 script and recasting card of stage 4 (run_stage4.sh).

Usage: python3 make_recast.py <MG5 launch log> <hepmc.gz> <script.ma5> <recasting_card.dat> <work directory>
The cross section of the sample is MG5's last 'Matched cross-section' of the launch log, or its last 'Cross-section' for a
sample without matching (MadSpin keeps it: the gluino decays into j j n1 only).  The card turns on atlas_susy_2016_07 of
PADForSFS with its ATLAS SFS card.
"""
import re
import sys
from pathlib import Path

log, hep, script, card, work = sys.argv[1:6]
txt = Path(log).read_text(errors="replace")
sig = re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)\s+\+-", txt) or re.findall(r"Cross-section :\s+([0-9.eE+-]+)\s+\+-", txt)
sig = float(sig[-1])
Path(card).write_text("# MadAnalysis5 recasting card of stage 4: analysis, version, on/off, detector card\n"
                      "atlas_susy_2016_07   vSFS   on   sfs_card_atlas_susy_2016_07.ma5\n")
Path(script).write_text("\n".join([
    "set main.recast = on",
    "set main.recast.card_path = %s" % card,
    "import %s as signal" % hep,
    "set signal.xsection = %.6g" % sig,
    "submit %s" % work,
]) + "\n")
print("MadAnalysis5 script %s (sigma = %.6g pb)" % (script, sig))
