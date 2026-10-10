! anom6_collier.f90 -- d = 6 MS-bar finite parts B0^(6), C0^(6) from COLLIER at several mu, for the field
! anomalous dimension (research note, step (10)).  As in oneloop6_collier.f90, X_N = -2 T00 with COLLIER's
! g^{mu nu} coefficients B00, C00 in D = 4 - 2 eps (Delta_UV = 0), now with mu_UV^2 = mu^2.
! m = 1.  Writes results/anom6_collier.csv with the points of anom6_feyncalc.wl for mu = 1, 1/2, 2.
!
! Build and run from Src/ (run_anom6_check.sh does this):
!   gfortran -I$HOME/hep/include anom6_collier.f90 -L$HOME/hep/lib -lcollier -o work/anom6_collier
!   (cd work && ./anom6_collier ../results/anom6_collier.csv)
program anom6_collier
  use COLLIER
  implicit none
  double precision, parameter :: p2list(8) = [-5d0, -1d0, 0d0, 1d0, 2d0, 3d0, 5d0, 8d0]
  double precision, parameter :: c0inv(3,4) = reshape([0d0,0d0,0d0, 1d0,1d0,1d0, 1d0,1d0,3.5d0, &
                                                        1d0,1d0,5d0], [3,4])
  double precision, parameter :: mulist(3) = [1d0, 0.5d0, 2d0]
  double complex, parameter :: one = (1d0, 0d0)
  double complex :: b(0:1,0:2), buv(0:1,0:2), c(0:1,0:2,0:2), cuv(0:1,0:2,0:2)
  character(len=256) :: outfile
  integer :: i, j, u

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'anom6_collier.csv'
  call Init_cll(3, 2, '')

  open(newunit=u, file=trim(outfile), status='replace', action='write')
  write(u, '(a)') 'func,arg1,arg2,arg3,mu,re_collier,im_collier'
  do j = 1, size(mulist)
    call SetMuUV2_cll(mulist(j)**2)
    do i = 1, size(p2list)
      call B_cll(b, buv, dcmplx(p2list(i), 0d0), one, one, 2)
      write(u, '(a,4(",",g0),2(",",es24.16e3))') 'B06', p2list(i), 1d0, 1d0, mulist(j), &
           dble(-2*b(1,0)), aimag(-2*b(1,0))
    end do
    do i = 1, size(c0inv, 2)
      call C_cll(c, cuv, dcmplx(c0inv(1,i), 0d0), dcmplx(c0inv(2,i), 0d0), dcmplx(c0inv(3,i), 0d0), &
                 one, one, one, 2)
      write(u, '(a,4(",",g0),2(",",es24.16e3))') 'C06', c0inv(1,i), c0inv(2,i), c0inv(3,i), mulist(j), &
           dble(-2*c(1,0,0)), aimag(-2*c(1,0,0))
    end do
  end do
  close(u)
  print '(a,a)', 'wrote ', trim(outfile)
end program
