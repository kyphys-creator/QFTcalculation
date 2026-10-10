! oneloop6_collier.f90 -- d = 6 finite parts from COLLIER for the d = 6 one-loop check
! (research note, step (4)).  COLLIER works in D = 4 - 2 eps, but the D = 6 - 2 eps scalar integrals
! follow from the g^{mu nu} coefficients A00, B00, C00 in D = 4 - 2 eps (note, App. H):
!   mu^(2 eps) I_N(D = 6 - 2 eps) = i/(4 pi)^3 [c_N DeltaUV + X_N],   X_N = -2 T00,
! where T00 is COLLIER's coefficient with Delta_UV = 0 (its MS-bar value) and mu^2 = 1.
! m = 1.  Writes X_N = A0^(6), B0^(6), C0^(6) to results/oneloop6_collier.csv with the same points
! as oneloop6_feyncalc.wl.
!
! Build and run from Src/ (run_oneloop6_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop6_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop6_collier
!   (cd work && ./oneloop6_collier ../results/oneloop6_collier.csv)
program oneloop6_collier
  use COLLIER
  implicit none
  double precision, parameter :: p2list(15) = [-10d0, -5d0, -1d0, 0d0, 1d0, 2d0, 3d0, 3.9d0, &
                                               4d0, 4.1d0, 5d0, 8d0, 12d0, 20d0, 30d0]
  double precision, parameter :: c0inv(3,5) = reshape([0d0,0d0,0d0, 1d0,1d0,1d0, 1d0,1d0,3.5d0, &
                                                        1d0,1d0,5d0, 1d0,1d0,10d0], [3,5])
  double complex, parameter :: one = (1d0, 0d0)
  double complex :: a(0:1), auv(0:1), b(0:1,0:2), buv(0:1,0:2), c(0:1,0:2,0:2), cuv(0:1,0:2,0:2)
  character(len=256) :: outfile
  integer :: i, u

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop6_collier.csv'
  call Init_cll(3, 2, '')

  open(newunit=u, file=trim(outfile), status='replace', action='write')
  write(u, '(a)') 'func,arg1,arg2,arg3,re_collier,im_collier'
  ! A(1) = A00, B(1,0) = B00, C(1,0,0) = C00
  call A_cll(a, auv, one, 2)
  write(u, '(a,3(",",g0),2(",",es24.16e3))') 'A06', 1d0, 0d0, 0d0, dble(-2*a(1)), aimag(-2*a(1))
  do i = 1, size(p2list)
    call B_cll(b, buv, dcmplx(p2list(i), 0d0), one, one, 2)
    write(u, '(a,3(",",g0),2(",",es24.16e3))') 'B06', p2list(i), 1d0, 1d0, dble(-2*b(1,0)), aimag(-2*b(1,0))
  end do
  do i = 1, size(c0inv, 2)
    ! C_cll(C, Cuv, p10, p21, p20, m02, m12, m22, rank) with p10 = k1^2, p21 = k2^2, p20 = (k1 + k2)^2
    call C_cll(c, cuv, dcmplx(c0inv(1,i), 0d0), dcmplx(c0inv(2,i), 0d0), dcmplx(c0inv(3,i), 0d0), &
               one, one, one, 2)
    write(u, '(a,3(",",g0),2(",",es24.16e3))') 'C06', c0inv(1,i), c0inv(2,i), c0inv(3,i), &
         dble(-2*c(1,0,0)), aimag(-2*c(1,0,0))
  end do
  close(u)
  print '(a,a)', 'wrote ', trim(outfile)
end program
