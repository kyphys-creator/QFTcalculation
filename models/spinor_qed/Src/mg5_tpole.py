# mg5_tpole.py -- copy a MadEvent process directory and start the VEGAS grid of every massive t-channel invariant
# logarithmic around its pole (research note models/spinor_qed, step (6)).
# Usage (from Src/):   python mg5_tpole.py work/mg5_xsec3 work/mg5_xsec3_tpole     (run_xsec_check.sh does this)
#
# MadEvent samples a t-channel invariant as x = -t/s on a 96-bin VEGAS grid over [-1, 1] (SubProcesses/genps.f).  set_peaks
# (SubProcesses/myamp.f) starts that grid with setgrid(j, x_o, a, 1) (Source/dsample.f): 86 bins logarithmic in x from
# x_o = (smallest energy allowed by the cuts)^2/s up to 1, 9 linear bins mirrored below x_o, and the first bin down to -1.
# The pole offset a = -m^2/s of the propagator is passed but not used.  For a massless propagator the pole is at x = 0 and
# the grid fits; for a massive one (the electron, pole at t = m^2) the quasi-collinear peak x in (a, 0) starts in the first
# bin [-1, ~0].  The patch adds setgrid itype = 3, the same grid logarithmic in x - a from x - a = XO_REL, and calls it for
# t-channel propagators with nonzero mass.  Nothing else changes (Jacobians, channels, cuts, adaptation).
import os
import shutil
import subprocess
import sys

XO_REL = "1d-7"     # lowest grid edge in x - a = (m^2 - t)/s; 86 logarithmic bins from there to 1 - a

SETGRID_OLD = """         elseif (itype .eq. 2) then
            do i=2,ng-1"""
SETGRID_NEW = """         elseif (itype .eq. 3) then
c           mg5_tpole.py: logarithmic in x-a, for a massive t-channel pole at x=a
            ngu = ng *0.9
            ngd = ng-ngu
            do i=1,ngu-1
               grid(2,i+ngd,j) = a + (xo-a)**(1-dble(i)/dble(ngu))
     $              *(1d0-a)**(dble(i)/dble(ngu))
            enddo
            grid(2,ngd,j) =  xo
            do i=1,ngd-1
               grid(2,ngd-i,j) = xo-(grid(2,ngd+i,j)-xo)
            enddo
         elseif (itype .eq. 2) then
            do i=2,ng-1"""
PEAKS_OLD = "             if (i .ne. -1 .or. .true.) call setgrid(-i,xo,a,1)\n"
PEAKS_NEW = f"""c            mg5_tpole.py: a massive t-channel propagator gets a grid logarithmic around its pole
             if (prmass(i,iconfig).gt.0d0) then
                call setgrid(-i,a+{XO_REL},a,3)
             else
                call setgrid(-i,xo,a,1)
             endif
"""


def patch(path, old, new):
    text = open(path).read()
    if text.count(old) != 1:
        sys.exit(f"mg5_tpole.py: the expected code is not in {path} (MadGraph version?)")
    open(path, "w").write(text.replace(old, new))


src, dst = sys.argv[1], sys.argv[2]
shutil.rmtree(dst, ignore_errors=True)
skip = shutil.ignore_patterns("run_[0-9]*", "G[0-9]*", "*.o", "*.a", "ajob*")      # objects and libraries are rebuilt
shutil.copytree(src, dst, symlinks=True, ignore=skip)
for d in os.listdir(os.path.join(dst, "SubProcesses")):
    if d.startswith("P") and os.path.exists(os.path.join(dst, "SubProcesses", d, "madevent")):
        os.remove(os.path.join(dst, "SubProcesses", d, "madevent"))    # MadEvent relinks it at launch
patch(os.path.join(dst, "Source", "dsample.f"), SETGRID_OLD, SETGRID_NEW)
patch(os.path.join(dst, "SubProcesses", "myamp.f"), PEAKS_OLD, PEAKS_NEW)
env = dict(os.environ)
env.setdefault("SDKROOT", subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip())
subprocess.run(["make"], cwd=os.path.join(dst, "Source"), env=env, check=True, capture_output=True)   # the libraries
print(f"mg5_tpole.py: {dst} patched (setgrid itype 3 for massive t-channel propagators), libraries built "
      "(MadEvent builds the process directories at launch)")
