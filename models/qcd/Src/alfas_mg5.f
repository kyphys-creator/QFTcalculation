      program alfas_mg5
c     MG5_aMC's ALPHAS(Q) (Template/LO/Source/alfas_functions.f) at the scales read from stdin
      implicit none
      include 'alfas.inc'
      double precision alphas, q
      external alphas
      integer ios
      asmz = 0.118d0
      nloop = 1
      do
        read(*, *, iostat=ios) q
        if (ios .ne. 0) exit
        write(*, '(es24.16e3, 1x, es24.16e3)') q, alphas(q)
      end do
      end
