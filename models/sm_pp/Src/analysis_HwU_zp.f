c
c Research note models/sm_pp, step (4c): the fixed-order analysis for p p > e+ e- [QCD] through the SSM Z' (the lepton pair
c V = particles 3 + 4, generation cut m_ee > 225 GeV).  Copied by zp_mg5.sh into the process's FixedOrderAnalysis/.
c   1 total;  2-4 m_V in |m_V - M| < 2 Gamma for M = 1, 3, 5 TeV (one bin each; Gamma of stage 6's MadWidth);
c   5 log10(m_V/GeV) in 2.3, 4.1 (36 bins)
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_begin(nwgt,weights_info)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
      integer nwgt
      character*(*) weights_info(*)
      call HwU_inithist(nwgt,weights_info)
      call HwU_book(1,'total               ',1,-1.d0,1.d0)
      call HwU_book(2,'window 1000         ',1,941.7218d0,1058.2782d0)
      call HwU_book(3,'window 3000         ',1,2822.6542d0,3177.3458d0)
      call HwU_book(4,'window 5000         ',1,4704.0800d0,5295.9200d0)
      call HwU_book(5,'log10 mV            ',36,2.3d0,4.1d0)
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
      integer i
      double precision ppv(0:3),xmv
      double precision getinvm
      external getinvm
      if (nexternal.ne.5) then
         write (*,*) 'analysis_HwU_zp: expects 2 -> 2 Born + 1 parton'
         stop 1
      endif
      do i=0,3
         ppv(i)=p(i,3)+p(i,4)
      enddo
      xmv=getinvm(ppv(0),ppv(1),ppv(2),ppv(3))
      call HwU_fill(1,0d0,wgts)
      call HwU_fill(2,xmv,wgts)
      call HwU_fill(3,xmv,wgts)
      call HwU_fill(4,xmv,wgts)
      if (xmv.gt.0d0) call HwU_fill(5,log10(xmv),wgts)
      return
      end


      function getinvm(en,ptx,pty,pl)
      implicit none
      real*8 getinvm,en,ptx,pty,pl,tiny,tmp
      parameter (tiny=1.d-5)
      tmp=en**2-ptx**2-pty**2-pl**2
      if(tmp.gt.0.d0)then
        tmp=sqrt(tmp)
      elseif(tmp.gt.-tiny)then
        tmp=0.d0
      else
        write(*,*)'Attempt to compute a negative mass'
        stop
      endif
      getinvm=tmp
      return
      end
