      program alfas_mg5
c     MG5_aMC's ALPHAS(Q) (Template/LO/Source/alfas_functions.f) at the scales read from stdin;
c     the number of loops is the first command-line argument (default 1)
      implicit none
      include 'alfas.inc'
      double precision alphas, q
      external alphas
      integer ios
      character*8 arg
      asmz = 0.118d0
      nloop = 1
      call get_command_argument(1, arg)
      if (len_trim(arg) .gt. 0) read(arg, *) nloop
      do
        read(*, *, iostat=ios) q
        if (ios .ne. 0) exit
        write(*, '(es24.16e3, 1x, es24.16e3)') q, alphas(q)
      end do
      end
