! oneloop4_collier.f90 -- A0, B0 and C0 from COLLIER for the d = 4 one-loop check
! (research note, step (3)).  m = 1, mu^2 = 1, Delta_UV = 0 (COLLIER defaults), i.e. the same
! convention as LoopTools.  Writes results/oneloop4_collier.csv with the same points as
! oneloop4_feyncalc.wl.
!
! Build and run from Src/ (run_oneloop4_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop4_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop4_collier
!   (cd work && ./oneloop4_collier ../results/oneloop4_collier.csv)
program oneloop4_collier
  use COLLIER
  implicit none
  double precision, parameter :: p2list(15) = [-10d0, -5d0, -1d0, 0d0, 1d0, 2d0, 3d0, 3.9d0, &
                                               4d0, 4.1d0, 5d0, 8d0, 12d0, 20d0, 30d0]
  double precision, parameter :: c0inv(3,5) = reshape([0d0,0d0,0d0, 1d0,1d0,1d0, 1d0,1d0,3.5d0, &
                                                        1d0,1d0,5d0, 1d0,1d0,10d0], [3,5])
  double complex, parameter :: one = (1d0, 0d0)
  double complex :: a0, b0, c0
  character(len=256) :: outfile
  integer :: i, u

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop4_collier.csv'
  call Init_cll(3, 3, '')

  open(newunit=u, file=trim(outfile), status='replace', action='write')
  write(u, '(a)') 'func,arg1,arg2,arg3,re_collier,im_collier'
  call A0_cll(a0, one)
  write(u, '(a,3(",",g0),2(",",es24.16e3))') 'A0', 1d0, 0d0, 0d0, dble(a0), aimag(a0)
  do i = 1, size(p2list)
    call B0_cll(b0, dcmplx(p2list(i), 0d0), one, one)
    write(u, '(a,3(",",g0),2(",",es24.16e3))') 'B0', p2list(i), 1d0, 1d0, dble(b0), aimag(b0)
  end do
  do i = 1, size(c0inv, 2)
    call C0_cll(c0, dcmplx(c0inv(1,i), 0d0), dcmplx(c0inv(2,i), 0d0), dcmplx(c0inv(3,i), 0d0), one, one, one)
    write(u, '(a,3(",",g0),2(",",es24.16e3))') 'C0', c0inv(1,i), c0inv(2,i), c0inv(3,i), dble(c0), aimag(c0)
  end do
  close(u)
  print '(a,a)', 'wrote ', trim(outfile)
end program
