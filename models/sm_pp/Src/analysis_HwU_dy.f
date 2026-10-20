c
c Research note models/sm_pp, step (1): the fixed-order analysis for p p > e+ e- [QCD], p p > e+ ve [QCD], p p > e- ve~ [QCD]
c (the lepton pair V = particles 3 + 4, no cuts).  Copied by dy_mg5.sh into the process's FixedOrderAnalysis/.
c   1 total;  2 m_V 50-150 GeV (20 bins);  3 m_V 500-3500 GeV (15 bins);  4 y_V (40 bins in -5, 5);
c   5 m_V in 66-116 GeV (1 bin);  6 y_V with 66 < m_V < 116 GeV;  7 pT_V 0-250 GeV (50 bins);  8 m_V 60-100 GeV (W, 1 bin);
c   9 log10(m_V/GeV) in -3, 4.2 (36 bins);  10-13 m_V in 0-1, 1-10, 10-50, 150-13000 GeV (1 bin each; the W tails)
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_begin(nwgt,weights_info)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      implicit none
      integer nwgt
      character*(*) weights_info(*)
      call HwU_inithist(nwgt,weights_info)
      call HwU_book(1,'total               ',1,-1.d0,1.d0)
      call HwU_book(2,'mV 50-150           ',20,50.d0,150.d0)
      call HwU_book(3,'mV 500-3500         ',15,500.d0,3500.d0)
      call HwU_book(4,'yV                  ',40,-5.d0,5.d0)
      call HwU_book(5,'mV 66-116           ',1,66.d0,116.d0)
      call HwU_book(6,'yV 66-116           ',40,-5.d0,5.d0)
      call HwU_book(7,'ptV                 ',50,0.d0,250.d0)
      call HwU_book(8,'mV 60-100           ',1,60.d0,100.d0)
      call HwU_book(9,'log10 mV            ',36,-3.d0,4.2d0)
      call HwU_book(10,'mV 0-1              ',1,0.d0,1.d0)
      call HwU_book(11,'mV 1-10             ',1,1.d0,10.d0)
      call HwU_book(12,'mV 10-50            ',1,10.d0,50.d0)
      call HwU_book(13,'mV 150-13000        ',1,150.d0,13000.d0)
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
      double precision ppv(0:3),xmv,yv,ptv
      double precision getrapidity,getinvm
      external getrapidity,getinvm
      if (nexternal.ne.5) then
         write (*,*) 'analysis_HwU_dy: expects 2 -> 2 Born + 1 parton'
         stop 1
      endif
      do i=0,3
         ppv(i)=p(i,3)+p(i,4)
      enddo
      xmv=getinvm(ppv(0),ppv(1),ppv(2),ppv(3))
      yv=getrapidity(ppv(0),ppv(3))
      ptv=sqrt(ppv(1)**2+ppv(2)**2)
      call HwU_fill(1,0d0,wgts)
      call HwU_fill(2,xmv,wgts)
      call HwU_fill(3,xmv,wgts)
      call HwU_fill(4,yv,wgts)
      call HwU_fill(5,xmv,wgts)
      if (xmv.gt.66d0.and.xmv.lt.116d0) call HwU_fill(6,yv,wgts)
      call HwU_fill(7,ptv,wgts)
      call HwU_fill(8,xmv,wgts)
      if (xmv.gt.0d0) call HwU_fill(9,log10(xmv),wgts)
      call HwU_fill(10,xmv,wgts)
      call HwU_fill(11,xmv,wgts)
      call HwU_fill(12,xmv,wgts)
      call HwU_fill(13,xmv,wgts)
      return
      end


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
