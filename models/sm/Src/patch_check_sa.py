"""Edit MadLoop's generated check_sa.f: read the phase-space point from PS.input, one point per run, and take MU_R from
MU_R.input (check_sa.f otherwise sets MU_R = sqrt(s) for every point).  Research note models/sm, step (9).
Usage: python3 patch_check_sa.py <path to check_sa.f>"""
import sys

p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/sm, step (9): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1, "MU_R=SQRTS not found once"
open(p, "w").write(s.replace(old, new))
