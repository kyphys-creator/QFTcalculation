      PROGRAM LBL_DRIVER
C     lbl_madloop_driver.f -- MadLoop driver for step (10) (research note models/spinor_qed, photon-photon
C     scattering).  run_lbl_check.sh copies it over the check_sa.f of the loop-induced standalone output of
C     "generate a a > a a QED=4 [sqrvirt=QED]" and builds it with "make check".  It reads points.input (the number of
C     points, then four lines E px py pz per point) and writes, per point, the helicity-summed and averaged squared
C     loop amplitude (MadLoop's answer array, index 0 of the squared orders) and then the same for each of the 16
C     helicity configurations of MadLoop5_resources/ML5_0_HelConfigs.dat (physical helicities of the incoming and
C     outgoing photons):
C       TOT  k  a0 a1 a2 a3  returncode
C       HEL  k  h  l1 l2 l3 l4  a0 a1 a2 a3  returncode
      IMPLICIT NONE
      REAL*8 ZERO
      PARAMETER (ZERO=0D0)
      INTEGER NEXTERNAL, NCOMB
      PARAMETER (NEXTERNAL=4, NCOMB=16)
      INCLUDE 'coupl.inc'
      INCLUDE 'nsquaredSO.inc'
      REAL*8 PMASS(NEXTERNAL)
      REAL*8 P(0:3,NEXTERNAL)
      INTEGER MATELEM_ARRAY_DIM, NSQUAREDSO_LOOP
      REAL*8, ALLOCATABLE :: MATELEM(:,:)
      REAL*8, ALLOCATABLE :: PREC_FOUND(:)
      INTEGER I, J, K, H, NPTS, RETURNCODE
      INTEGER HELC(NEXTERNAL,NCOMB)

      CALL ML5_0_GET_ANSWER_DIMENSION(MATELEM_ARRAY_DIM)
      ALLOCATE(MATELEM(0:3,0:MATELEM_ARRAY_DIM))
      CALL ML5_0_GET_NSQSO_LOOP(NSQUAREDSO_LOOP)
      ALLOCATE(PREC_FOUND(0:NSQUAREDSO_LOOP))
      CALL SETPARA('param_card.dat')
      INCLUDE 'pmass.inc'

      OPEN(1, FILE='MadLoop5_resources/ML5_0_HelConfigs.dat',
     $  STATUS='OLD', ACTION='READ')
      DO H=1,NCOMB
        READ(1,*) (HELC(I,H),I=1,NEXTERNAL)
      ENDDO
      CLOSE(1)

      OPEN(2, FILE='points.input', STATUS='OLD', ACTION='READ')
      READ(2,*) NPTS
      DO K=1,NPTS
        DO I=1,NEXTERNAL
          READ(2,*) P(0,I),P(1,I),P(2,I),P(3,I)
        ENDDO
        CALL ML5_0_SLOOPMATRIX_THRES(P,MATELEM,-1.0D0,PREC_FOUND,
     $    RETURNCODE)
        WRITE(*,'(A4,I6,4ES26.17E3,I6)') 'TOT ', K,
     $    (MATELEM(J,0),J=0,3), RETURNCODE
        DO H=1,NCOMB
          CALL ML5_0_SLOOPMATRIXHEL_THRES(P,H,MATELEM,-1.0D0,
     $      PREC_FOUND,RETURNCODE)
          WRITE(*,'(A4,I6,I4,4I3,4ES26.17E3,I6)') 'HEL ', K, H,
     $      (HELC(I,H),I=1,NEXTERNAL), (MATELEM(J,0),J=0,3),
     $      RETURNCODE
        ENDDO
      ENDDO
      CLOSE(2)
      END
