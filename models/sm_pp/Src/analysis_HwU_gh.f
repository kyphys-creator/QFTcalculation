c
c Research note models/sm_pp, step (2): the fixed-order analysis for p p > x0 / t [QCD] (HC_NLO_X0-heft): the Higgs is particle 3.
c Copied by gh_mg5.sh into the process's FixedOrderAnalysis/.
c   1 total;  2 y_H (40 bins in -5, 5);  3 pT_H 0-250 GeV (50 bins)
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_begin(nwgt,weights_info)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
      integer nwgt
      character*(*) weights_info(*)
      call HwU_inithist(nwgt,weights_info)
      call HwU_book(1,'total               ',1,-1.d0,1.d0)
      call HwU_book(2,'yH                  ',40,-5.d0,5.d0)
      call HwU_book(3,'ptH                 ',50,0.d0,250.d0)
      return
      end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_end(dummy)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
      double precision dummy
      call HwU_write_file
      return
      end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_fill(p,istatus,ipdg,wgts,ibody)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
      include 'nexternal.inc'
      integer istatus(nexternal)
      integer iPDG(nexternal)
      double precision p(0:4,nexternal)
      double precision wgts(*)
      integer ibody
      double precision yh,pth,xp,xm
      if (nexternal.ne.4) then
         write (*,*) 'analysis_HwU_gh: expects 2 -> 1 Born + 1 parton'
         stop 1
      endif
      xp=p(0,3)+p(3,3)
      xm=p(0,3)-p(3,3)
      yh=0.5d0*log(xp/xm)
      pth=sqrt(p(1,3)**2+p(2,3)**2)
      call HwU_fill(1,0d0,wgts)
      call HwU_fill(2,yh,wgts)
      call HwU_fill(3,pth,wgts)
      return
      end
