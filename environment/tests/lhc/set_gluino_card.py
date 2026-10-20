"""Set the param_card of the stage-4 gluino benchmark (run_stage4.sh) in an MG5 MSSM_SLHA2 process directory.

  masses: gluino 1000 GeV, chi0_1 825 GeV, the squarks, sleptons, other neutralinos and charginos and the heavy Higgs bosons
  4500 GeV (the light Higgs as in the model's card);
  the squark widths: Auto, for MadWidth at the launch (run_stage4.sh: two-body decays; about 200 GeV at 4.5 TeV, mostly
  q~ -> q g~).  The model's card has the widths of its own spectrum (0.29 to 7.4 GeV), and with them the on-shell squark
  in q g -> q~ g~ -> q g~ g~ (in p p > go go j, j j) is weighted by Gamma(q~ -> q g~)/Gamma(card) = 37 to 715 (u, d, s,
  c): a false hard jet (the Jacobian peak at pT = 2.1 TeV) in 5% of the events.  The other heavy states do not enter the
  diagrams of the process or of the gluino decay and keep the card's widths;
  the gluino decay table: MG5's MadWidth gives the partial widths of g~ -> q qbar chi0_1 at these masses (8.8695e-9 (u),
  8.8553e-9 (c), 3.0487e-9 (d), 3.0476e-9 (s), 2.9704e-9 (b) GeV, with the alpha_s = 0.130 of nn23lo1 that MG5 writes
  into the card at the launch) but sets each to zero as below the QCD scale (0.1 GeV for a coloured particle), so that
  MadSpin could not decay the gluino.  The total width (their sum, 2.6792e-8 GeV) and the branching ratios are written
  here instead.  MadSpin computes the partial width itself and multiplies the cross section by its ratio to the card's
  total for each gluino: the total must be the one of the run's alpha_s (with the model's 0.118 it came out 7% lower,
  and the cross section 15% higher).
Usage: python3 set_gluino_card.py <process directory>
"""
import re
import sys
from pathlib import Path

PARTIAL = {2: 8.86950021975e-09, 4: 8.85530072475e-09, 1: 3.0487012344e-09, 3: 3.04760010375e-09, 5: 2.9704003965e-09}
SQUARKS = [1000001, 1000002, 1000003, 1000004, 1000005, 1000006, 2000001, 2000002, 2000003, 2000004, 2000005, 2000006]
HEAVY = SQUARKS + [1000011, 1000012, 1000013, 1000014, 1000015, 1000016, 2000011, 2000013, 2000015,
         1000023, 1000025, 1000035, 1000024, 1000037, 35, 36, 37]
MASS = {1000021: 1000.0, 1000022: 825.0, **{p: 4500.0 for p in HEAVY}}

card = Path(sys.argv[1]) / "Cards" / "param_card.dat"
lines = card.read_text().splitlines()
out, block, skip, seen = [], "", False, set()
for line in lines:
    s = line.strip()
    if skip:                                   # drop the old BR lines of the gluino
        if s and not s.upper().startswith(("DECAY", "BLOCK")):
            continue
        skip = False
    if s.upper().startswith("BLOCK"):
        block = s.split()[1].upper()
    m = re.match(r"\s*(\d+)\s+([-+0-9.eE]+)(\s*#.*)?$", line)
    if block == "MASS" and m and int(m.group(1)) in MASS:
        pid = int(m.group(1))
        line = "  %d %.6e %s" % (pid, MASS[pid], (m.group(3) or "").strip())
        seen.add(pid)
    if s.upper().startswith("DECAY") and int(s.split()[1]) in SQUARKS:
        out.append("DECAY %d Auto # (set_gluino_card.py: MadWidth at the launch)" % int(s.split()[1]))
        seen.add(-int(s.split()[1]))
        skip = True
        block = ""
        continue
    if s.upper().startswith("DECAY") and int(s.split()[1]) == 1000021:
        tot = sum(PARTIAL.values())
        out.append("DECAY 1000021 %.6e # wgo (the sum of MadWidth's partial widths, set_gluino_card.py)" % tot)
        for q, w in PARTIAL.items():
            out.append("   %.6e   3   1000022   %d   %d   # BR(go -> n1 q qbar)" % (w / tot, q, -q))
        skip = True
        block = ""
        continue
    out.append(line)
missing = (set(MASS) | {-q for q in SQUARKS}) - seen
if missing:
    sys.exit("masses (pid) or squark widths (-pid) not found in the card: %s" % sorted(missing))
card.write_text("\n".join(out) + "\n")
print("set %d masses, %d squark widths to Auto and the gluino decay table (width %.4e GeV) in %s"
      % (len(MASS), len(SQUARKS), sum(PARTIAL.values()), card))
