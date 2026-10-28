      PROGRAM ME_POINTS
C     tree_me_points.f -- driver for the MadGraph standalone matrix element of a 2 -> 2 process
C     (research note models/abelian_higgs, step (2); built by run_tree_check.sh in
C     work/sa_*/SubProcesses/P1_* and run from there).
C     Reads lines "E1 px1 py1 pz1 ... E4 px4 py4 pz4" (two incoming, two outgoing) and prints
C     SMATRIX = |M|^2 averaged over the initial and summed over the final helicities.
      IMPLICIT NONE
      INCLUDE 'nexternal.inc'
      REAL*8 P(0:3,NEXTERNAL), ANS
      INTEGER I, J, IOS
      CALL SETPARA('../../Cards/param_card.dat')
 10   READ(*,*,IOSTAT=IOS) ((P(I,J),I=0,3),J=1,NEXTERNAL)
      IF (IOS.NE.0) GOTO 20
      CALL SMATRIX(P,ANS)
      WRITE(*,'(ES24.16)') ANS
      GOTO 10
 20   CONTINUE
      END
