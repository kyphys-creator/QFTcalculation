#!/bin/bash
# Step (6) of the SM note: the one-loop e- e+ -> mu- mu+ virtual correction, MadLoop against FormCalc (on-shell, alpha(0)),
# at the note's point and, as a cross-check, with heavier leptons (m_e = 2, m_mu = 3 GeV; files *_heavy); and MadGraph's own
# electroweak NLO models loop_qcd_qed_sm (alpha(MZ)) and loop_qcd_qed_sm_Gmu (G_mu) against FormCalc in the same schemes
# (massless fermions but the top; files *_ml_aMZ, *_ml_Gmu).
#   0. generate_SM_NLO.sh (once): FeynRules + NLOCT -> generated/SM_NLO_a0_UFO, SM_NLO_a0_heavy_UFO
#   1. eemm_numeric.py --points: the phase-space points -> work/eemm_points{,_heavy,_ml}.csv
#   2. eemm_formcalc.wl [massless]: FormCalc (SM.mod) coefficients and LoopTools values -> results/eemm_{coeffs,functions,
#      renconst}*.csv; with "massless" the fermions but the top are massless from the start (MadGraph's models)
#   3. eemm_collier.f90: the same loop functions from COLLIER -> results/eemm_collier*.csv;  eemm_softc0.wl: the soft-photon
#      C0 from LoopTools, Package-X and COLLIER with a photon mass and dimensionally regularized -> results/eemm_softc0*.csv
#   4. MadLoop standalone from each NLO UFO -> work/ml_eemm{,_heavy} (param_card set to the point, widths 0; check_sa.f
#      reads the point from PS.input and mu_R from MU_R.input; at the note's point COLLIER reduction, OSThres = 1e-4 and
#      a local change of COLLIER_interface.f so that m_e^2 is not set to zero; the heavier leptons with MadLoop's defaults);
#      MadGraph's models -> work/ml_eemm_ml_{aMZ,Gmu} (MadLoop's defaults)
#   5. eemm_numeric.py [--heavy | --ml_aMZ | --ml_Gmu]: MadLoop at the points against FormCalc -> results/eemm_comparison*.csv
#      (COLLIER's poles in MadLoop's normalization r_Gamma; for the massless sets FormCalc's finite part converted from
#      dimensional reduction on the massless legs to CDR, MadLoop's scheme)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
MU2=8315.251344   # MZ^2 = 91.1880^2
mkdir -p work results

echo "=== points"
"$PY" eemm_numeric.py --points

echo "=== FormCalc (SM.mod): the note's point and heavier leptons; massless fermions but the top (MadGraph's models)"
wolframscript -file eemm_formcalc.wl > work/eemm_formcalc.log 2>&1
grep -E '^\((a|b|c|d)\)' work/eemm_formcalc.log | grep -v 'renormalization constants (Delta' | cut -c1-300
wolframscript -file eemm_formcalc.wl massless > work/eemm_formcalc_ml.log 2>&1
grep -E '^\((a|b|c|d)\)' work/eemm_formcalc_ml.log | grep -v 'renormalization constants (Delta' | cut -c1-300

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" eemm_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/eemm_collier || exit 1
for tag in "" _heavy _ml_aMZ _ml_Gmu; do
  "$PY" eemm_numeric.py --collier-input ${tag:+--${tag#_}}
  (cd work && ./eemm_collier "eemm_collier_in$tag.txt" "../results/eemm_collier$tag.csv" "$MU2" | grep wrote)
done

echo "=== the soft-photon C0: LoopTools, Package-X, COLLIER (dimensional regularization and photon mass)"
wolframscript -file eemm_softc0.wl 2>&1 | grep -E '^\(a\)|difference' | cut -c1-260
(cd work && ./eemm_collier eemm_softc0_in.txt ../results/eemm_softc0_collier.csv 1.0 | grep wrote && cat ../results/eemm_softc0_collier.csv)

for tag in "" _heavy _ml_aMZ _ml_Gmu; do
  echo "=== MadLoop$tag"
  out="work/ml_eemm$tag"
  rm -rf "$out"
  case "$tag" in
    _ml_aMZ) model=loop_qcd_qed_sm ;;          # MadGraph's electroweak NLO models (restrict_default: massless fermions
    _ml_Gmu) model=loop_qcd_qed_sm_Gmu ;;      # but the top), from MadGraph's model database
    *) ufo="SM_NLO_a0${tag}_UFO"; rm -rf "work/$ufo"; cp -r "generated/$ufo" work/; model="./work/$ufo" ;;
  esac
  printf 'import model %s\ngenerate e- e+ > mu- mu+ [virt=QED]\noutput standalone ./%s\n' "$model" "$out" > "$out.mg5"
  mg5_aMC "$out.mg5" > "$out.log" 2>&1
  grep -E 'Contributing diagrams|Error|error' "$out.log" | head -5
  P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
  "$PY" - "$P/check_sa.f" "$out/Cards/param_card.dat" "$tag" "$P/COLLIER_interface.f" "$out/Cards/MadLoopParams.dat" <<'PYEOF'
import math, re, sys
# MadLoop's COLLIER interface sets an external invariant p^2 to zero when |p^2|/E^2 < OSThres (default 1e-8): the electron's
# m_e^2/E^2 ~ 4e-12 becomes 0 and the soft singularities change.  p^2 = E^2 - |p|^2 from double-precision momenta is off
# by ~2e-5 relative, so the snap to the internal mass m_e^2 needs OSThres = 1e-4; the snap to zero is then skipped for an
# invariant already set to a mass (local change of the generated COLLIER_interface.f).  COLLIER does the reduction.
ci, tag = sys.argv[4], sys.argv[3]
s = open(ci).read() if tag == "" else None   # only at the note's point: the heavier leptons need no change
old = """          DO K=1,NLOOPLINE
            IF(ABS(M2L(K)).NE.0.0D0) THEN
              IF(ABS((MOMINV(CURR_INDEX)-M2L(K))/M2L(K)).LT.OSTHRES)
     $          THEN
                MOMINV(CURR_INDEX)=DCMPLX(M2L(K))
              ENDIF
            ENDIF
          ENDDO"""
new = """          SNAPPED_RN = .FALSE.
          DO K=1,NLOOPLINE
            IF(ABS(M2L(K)).NE.0.0D0) THEN
              IF(ABS((MOMINV(CURR_INDEX)-M2L(K))/M2L(K)).LT.OSTHRES)
     $          THEN
                MOMINV(CURR_INDEX)=DCMPLX(M2L(K))
                SNAPPED_RN = .TRUE.
              ENDIF
            ENDIF
          ENDDO"""
if tag == "":
  assert s.count(old) == 1
  s = s.replace(old, new)
old2 = """          IF(REF_NORMALIZATION.NE.0.0D0)THEN
            IF(ABS(MOMINV(CURR_INDEX)/REF_NORMALIZATION).LT.OSTHRES)"""
if tag == "":
  assert s.count(old2) == 1
  s = s.replace(old2, old2.replace("NE.0.0D0)THEN", "NE.0.0D0.AND..NOT.SNAPPED_RN)THEN"))
  i = s.index(new)
  j = s.rfind("      SUBROUTINE", 0, i)
  k = s.index("\n", s.index("INTEGER", j))
  s = s[:k + 1] + "C     research note models/sm, step (6): no massless snap after a massive one\n      LOGICAL SNAPPED_RN\n" + s[k + 1:]
  open(ci, "w").write(s)
  mlp = sys.argv[5]
  lines = open(mlp).read().split("\n")
  for key, val in (("#MLReductionLib", "7"), ("#OSThres", "1.000000d-04")):
      lines[lines.index(key) + 1] = val
  open(mlp, "w").write("\n".join(lines))
# check_sa.f: one point from PS.input per run, mu_R from MU_R.input (check_sa.f otherwise sets MU_R = sqrt(s))
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/sm, step (6): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
# param_card: the point of the UFO's counterterms (assumption 7 / step (3)), widths zero
card, tag = sys.argv[2], sys.argv[3]
alpha_inv = 128.93 if tag == "_ml_aMZ" else 137.035999177
mz, mw = 91.1880, 80.3692
me, mmu = (2.0, 3.0) if tag == "_heavy" else (0.00051099895, 0.1056583755)
vals = {"aEWM1": alpha_inv, "MZ": mz, "MH": 125.20, "Me": me, "MMU": mmu, "MTA": 1.77686,
        "MU": 0.00216, "MC": 1.2730, "MT": 172.57, "MD": 0.00470, "MS": 0.0935, "MB": 4.183,
        "ymup": 0.00216, "ymc": 1.2730, "ymt": 172.57, "ymdo": 0.00470, "yms": 0.0935, "ymb": 4.183,
        "yme": me, "ymm": mmu, "ymtau": 1.77686, "aS": 0.118,
        "WZ": 0.0, "WW": 0.0, "WT": 0.0, "WH": 0.0, "MU_R": mz}
txt = open(card).read()
names = set(re.findall(r"#\s*(\w+)\s*$", txt, re.M))
if tag == "_ml_Gmu":   # G_mu scheme: G_F and MW are inputs
    vals["Gf"] = 1.1663788e-5
if "MW" in names:
    vals["MW"] = mw
else:          # MW internal: G_F such that MW comes out at the point
    vals["Gf"] = math.pi / (math.sqrt(2) * alpha_inv) * mz ** 2 / (mw ** 2 * (mz ** 2 - mw ** 2))
lines = []
for line in txt.splitlines():
    m = re.match(r"^(\s*(?:DECAY\s+)?[\d\s]+?)(\s[-+0-9.eE]+)(\s*#\s*(\w+)\s*)$", line)
    if m and m.group(4) in vals:
        line = f"{m.group(1)} {vals[m.group(4)]:.10e}{m.group(3)}"
    lines.append(line)
open(card, "w").write("\n".join(lines) + "\n")
print("param_card set:", ", ".join(sorted(k for k in vals if k in names)), "| not in the card:", ", ".join(sorted(k for k in vals if k not in names)))
PYEOF
  (cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
done

echo "=== comparison"
"$PY" eemm_numeric.py
"$PY" eemm_numeric.py --heavy
"$PY" eemm_numeric.py --ml_aMZ
"$PY" eemm_numeric.py --ml_Gmu
