c Research note models/sm_pp, step (3): the Pythia 8 analysis of the MC@NLO runs (mc_mg5.sh), HwU histograms, after the template
c py8an_HwU_pp_h.f of MG5_aMC.  The colour-singlet boson B is the Higgs (pdg 25, its final copy; h_stable = T) if there is one,
c else the final-state e+ e- pair (QED shower and hadronization off: one e+ and one e-; the initial-state recoil boosts the pair
c as a whole, so m_ee is that of the hard event).  The histograms as analysis_HwU_dy.f and analysis_HwU_gh.f of the fixed order:
c   total, yB, ptB (0-250 GeV in 5 GeV), ptB 0-30 (1 GeV), mB 66-116 (one bin), yB 66-116.
C----------------------------------------------------------------------
      SUBROUTINE RCLOS()
C     DUMMY IF HBOOK IS USED
C----------------------------------------------------------------------
      END


C----------------------------------------------------------------------
      SUBROUTINE PYABEG(nnn,wwwi)
C     USER''S ROUTINE FOR INITIALIZATION
C----------------------------------------------------------------------
      use HwU_wgts_info_len
      INCLUDE 'HEPMC.INC'
      include 'reweight0.inc'
      integer i,nnn
      character*(wgts_info_len) weights_info(max_weight_shower)
     $     ,wwwi(max_weight_shower)
      integer nwgt_analysis
      common/c_analysis/nwgt_analysis
      do i=1,nnn
         weights_info(i)=wwwi(i)
      enddo
      nwgt=nnn
      call HwU_inithist(nwgt,weights_info)
      call set_error_estimation(0)
      nwgt_analysis=nwgt
      call HwU_book(1,'total               ',1,-1.d0,1.d0)
      call HwU_book(2,'yB                  ',40,-5.d0,5.d0)
      call HwU_book(3,'ptB                 ',50,0.d0,250.d0)
      call HwU_book(4,'ptB 0-30            ',30,0.d0,30.d0)
      call HwU_book(5,'mB 66-116           ',1,66.d0,116.d0)
      call HwU_book(6,'yB 66-116           ',40,-5.d0,5.d0)
      END


C----------------------------------------------------------------------
      SUBROUTINE PYAEND(IEVTTOT)
C     USER''S ROUTINE FOR TERMINAL CALCULATIONS, HISTOGRAM OUTPUT, ETC
C----------------------------------------------------------------------
      INCLUDE 'HEPMC.INC'
      REAL*8 XNORM,IEVTTOT
      xnorm=ievttot
      call finalize_histograms(nevhep)
      open (unit=99,file='MADatNLO.HwU',status='unknown')
      call HwU_output(99,xnorm)
      close (99)
      END


C----------------------------------------------------------------------
      SUBROUTINE PYANAL(nnn,xww)
C     USER''S ROUTINE TO ANALYSE DATA FROM EVENT
C----------------------------------------------------------------------
      INCLUDE 'HEPMC.INC'
      include 'reweight0.inc'
      DOUBLE PRECISION PH(4),PL(4),PB(4),getrapidity,YB,PTB,XMB
      INTEGER IHEP,IST,ID,I,NEP,NEM,IFH,nnn
      integer nwgt_analysis,max_weight
      common/c_analysis/nwgt_analysis
      integer maxRWGT
      parameter (maxRWGT=100)
      parameter (max_weight=maxscales*maxscales+maxpdfs+maxRWGT+1)
      double precision ww(max_weight),www(max_weight),xww(max_weight)
      common/cww/ww
c
      if(nnn.eq.0)ww(1)=1d0
      do i=1,nnn
         ww(i)=xww(i)
      enddo
      IF (WW(1).EQ.0D0) THEN
         WRITE(*,*)'WW(1) = 0. Stopping'
         STOP
      ENDIF
C INCOMING PARTONS MAY TRAVEL IN THE SAME DIRECTION: IT''S A POWER-SUPPRESSED
C EFFECT, SO THROW THE EVENT AWAY (AS THE TEMPLATE)
      IF(SIGN(1.D0,PHEP(3,1)).EQ.SIGN(1.D0,PHEP(3,2)))THEN
         WRITE(*,*)'WARNING 502 IN PYANAL'
         GOTO 999
      ENDIF
      DO I=1,nwgt_analysis
         WWW(I)=EVWGT*ww(i)/ww(1)
      ENDDO
      IFH=0
      NEP=0
      NEM=0
      DO I=1,4
         PH(I)=0D0
         PL(I)=0D0
      ENDDO
      DO 100 IHEP=1,NHEP
         IST=ISTHEP(IHEP)
         ID=IDHEP(IHEP)
         IF(IST.NE.1)GOTO 100
         IF(ID.EQ.25)THEN
            IFH=IFH+1
            DO I=1,4
               PH(I)=PHEP(I,IHEP)
            ENDDO
         ELSEIF(ABS(ID).EQ.11)THEN
            IF(ID.EQ.11)THEN
               NEM=NEM+1
            ELSE
               NEP=NEP+1
            ENDIF
            DO I=1,4
               PL(I)=PL(I)+PHEP(I,IHEP)
            ENDDO
         ENDIF
 100  CONTINUE
      IF(IFH.EQ.1)THEN
         DO I=1,4
            PB(I)=PH(I)
         ENDDO
      ELSEIF(IFH.EQ.0.AND.NEP.EQ.1.AND.NEM.EQ.1)THEN
         DO I=1,4
            PB(I)=PL(I)
         ENDDO
      ELSE
         WRITE(*,*)'WARNING 503 IN PYANAL: H, e+, e- ',IFH,NEP,NEM
         GOTO 999
      ENDIF
      XMB=SQRT(MAX(PB(4)**2-PB(1)**2-PB(2)**2-PB(3)**2,0D0))
      YB=getrapidity(PB(4),PB(3))
      PTB=SQRT(PB(1)**2+PB(2)**2)
      call HwU_fill(1,0d0,WWW)
      call HwU_fill(2,YB,WWW)
      call HwU_fill(3,PTB,WWW)
      call HwU_fill(4,PTB,WWW)
      if(XMB.gt.66d0.and.XMB.lt.116d0)then
         call HwU_fill(5,XMB,WWW)
         call HwU_fill(6,YB,WWW)
      endif
      call HwU_add_points
 999  END


      function getrapidity(en,pl)
      implicit none
      real*8 getrapidity,en,pl,tiny,xplus,xminus,y
      parameter (tiny=1.d-8)
      xplus=en+pl
      xminus=en-pl
      if(xplus.gt.tiny.and.xminus.gt.tiny)then
         if( (xplus/xminus).gt.tiny.and.(xminus/xplus).gt.tiny)then
            y=0.5d0*log( xplus/xminus  )
         else
            y=sign(1.d0,pl)*1.d8
         endif
      else
         y=sign(1.d0,pl)*1.d8
      endif
      getrapidity=y
      end
