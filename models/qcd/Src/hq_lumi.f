C     research note models/qcd, step (9): parton luminosities from the NNPDF2.3 NLO grid shipped with MadGraph5_aMC@NLO
C     (the same driver as pdlabel = nn23nlo; built with MadGraph's NNPDFDriver.f by run_hq_check.sh)
C     stdin: ipbar (0 = p p, 1 = p pbar), mu, n, then n values of tau;  stdout: tau, L_gg, L_qqbar, L_qg  (5 light flavours)
      PROGRAM LUMI
      IMPLICIT NONE
      INTEGER NG, N, I, K, IQ, IPBAR, SG
      PARAMETER (NG=200)
      DOUBLE PRECISION MU, TAU, XG(NG), WG(NG), X1, X2, Y, YMIN
      DOUBLE PRECISION F1(-6:7), F2(-6:7), LGG, LQQ, LQG, W
      CALL NNPDFDriver('NNPDF23nlo_as_0119_qed_mem0.grid')
      CALL NNinitPDF(0)
      CALL GAULEG(-1D0, 1D0, XG, WG, NG)
      READ(*,*) IPBAR
      READ(*,*) MU
      SG = 1
      IF (IPBAR .EQ. 1) SG = -1
      READ(*,*) N
      DO K = 1, N
        READ(*,*) TAU
        LGG = 0D0
        LQQ = 0D0
        LQG = 0D0
        YMIN = LOG(TAU)
        DO I = 1, NG
C         y = ln x1 from ln tau to 0, x2 = tau/x1;  dx1/x1 = dy
          Y = YMIN*(1D0 - XG(I))/2D0
          W = WG(I)*(-YMIN)/2D0
          X1 = EXP(Y)
          X2 = TAU/X1
          CALL NNevolvePDF(X1, MU, F1)
          CALL NNevolvePDF(X2, MU, F2)
          LGG = LGG + W*F1(0)*F2(0)/(X1*X2)
          DO IQ = 1, 5
            LQQ = LQQ + W*(F1(IQ)*F2(-SG*IQ)
     &            + F1(-IQ)*F2(SG*IQ))/(X1*X2)
            LQG = LQG + W*((F1(IQ) + F1(-IQ))*F2(0)
     &            + F1(0)*(F2(IQ) + F2(-IQ)))/(X1*X2)
          ENDDO
        ENDDO
        WRITE(*,'(4E26.16)') TAU, LGG, LQQ, LQG
      ENDDO
      END

      SUBROUTINE GAULEG(X1, X2, X, W, N)
      IMPLICIT NONE
      INTEGER N, I, J, M
      DOUBLE PRECISION X1, X2, X(N), W(N), P1, P2, P3, PP, XL, XM, Z, Z1
      DOUBLE PRECISION PI
      PARAMETER (PI = 3.14159265358979323846D0)
      M = (N + 1)/2
      XM = 0.5D0*(X2 + X1)
      XL = 0.5D0*(X2 - X1)
      DO I = 1, M
        Z = COS(PI*(I - 0.25D0)/(N + 0.5D0))
 1      CONTINUE
        P1 = 1D0
        P2 = 0D0
        DO J = 1, N
          P3 = P2
          P2 = P1
          P1 = ((2D0*J - 1D0)*Z*P2 - (J - 1D0)*P3)/J
        ENDDO
        PP = N*(Z*P1 - P2)/(Z*Z - 1D0)
        Z1 = Z
        Z = Z1 - P1/PP
        IF (ABS(Z - Z1) .GT. 1D-15) GOTO 1
        X(I) = XM - XL*Z
        X(N + 1 - I) = XM + XL*Z
        W(I) = 2D0*XL/((1D0 - Z*Z)*PP*PP)
        W(N + 1 - I) = W(I)
      ENDDO
      END

C     minimal replacement of MadGraph's OpenData: the grid in the current directory on unit IU
      SUBROUTINE OPENDATA(TABLEFILE)
      IMPLICIT NONE
      CHARACTER TABLEFILE*(*)
      INTEGER IU
      COMMON/IU/IU
      IU = 51
      OPEN(IU, FILE=TABLEFILE, STATUS='OLD')
      END
