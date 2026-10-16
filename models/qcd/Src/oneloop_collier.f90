! oneloop_collier.f90 -- the renormalized one-loop two-point functions of QCD (research note models/qcd, Eq. (VR)) from
! COLLIER, at g = 1, m = mu = 1, C_A = 3, C_F = 4/3, T_F = 1/2 and the points of oneloop_feyncalc.wl.
! All brackets are K/g^2 times the note's quantity (K = (4 pi)^2); COLLIER's defaults (Delta_UV = 0, mu_UV^2 = 1) give the
! MS-bar finite parts:
!   PiYM   = C_A [(5/3 + eta/2) B0(k^2; 0, 0) + 1/9 - 2 eta + eta^2/4],                 eta = 1 - xi
!   PiQ0   = -(4/3) T_F [B0(k^2; 0, 0) - 1/3]                                            (one massless flavour)
!   PiT    = -(4/3) T_F [(1 + 2 m^2/k^2) B0(k^2; m^2, m^2) - (2 m^2/k^2) B0(0; m^2, m^2) - 1/3]
!   Ghost  = -C_A [(3 - xi)/4 B0(p^2; 0, 0) - (1 - xi)/2]
!   SigV_t = xi C_F (1 + 2 B1(p^2; m^2, 0)),   SigS_t = C_F [(3 + xi) B0(p^2; m^2, 0) - 2],   SigV_u = xi C_F (1 + 2 B1(p^2; 0, 0))
! Writes results/oneloop_collier.csv (rows func, arg, xi, re/im of the pole (0) and of the finite part).  Build and run
! from Src/ (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   (cd work && ./oneloop_collier ../results/oneloop_collier.csv)
program oneloop_collier
  use COLLIER
  implicit none
  double precision, parameter :: m = 1d0, ca = 3d0, cf = 4d0 / 3d0, tf = 0.5d0
  double precision, parameter :: gpts(6) = [-5d0, -1d0, 0.5d0, 2d0, 6d0, 20d0]
  double precision, parameter :: qpts(7) = [-5d0, -1d0, 0.5d0, 2d0, 3.9d0, 6d0, 20d0]
  double precision, parameter :: spts(5) = [-5d0, 0.5d0, 2d0, 4d0, 10d0], upts(3) = [-5d0, 0.5d0, 2d0]
  double precision, parameter :: xis(3) = [0d0, 1d0, 3d0]
  character(len=256) :: outfile
  integer :: i, j, w
  double precision :: eta

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop_collier.csv'
  call Init_cll(2, 1, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'func,arg,xi,re_pole,im_pole,re_fin,im_fin'

  do i = 1, size(gpts)
    do j = 1, size(xis)
      eta = 1d0 - xis(j)
      call row('PiYM', gpts(i), xis(j), ca * ((5d0 / 3d0 + eta / 2) * b0f(gpts(i), 0d0, 0d0) + 1d0 / 9d0 - 2 * eta + eta**2 / 4))
      call row('Ghost', gpts(i), xis(j), -ca * ((3d0 - xis(j)) / 4 * b0f(gpts(i), 0d0, 0d0) - (1d0 - xis(j)) / 2))
    end do
  end do
  do i = 1, size(qpts)
    call row('PiQ0', qpts(i), 0d0, -4d0 / 3d0 * tf * (b0f(qpts(i), 0d0, 0d0) - 1d0 / 3d0))
    call row('PiT', qpts(i), 0d0, -4d0 / 3d0 * tf * ((1 + 2 * m**2 / qpts(i)) * b0f(qpts(i), m**2, m**2) &
             - 2 * m**2 / qpts(i) * b0f(0d0, m**2, m**2) - 1d0 / 3d0))
  end do
  do i = 1, size(spts)
    do j = 1, size(xis)
      call row('SigV_t', spts(i), xis(j), xis(j) * cf * (1 + 2 * b1f(spts(i), m**2, 0d0)))
      call row('SigS_t', spts(i), xis(j), cf * ((3 + xis(j)) * b0f(spts(i), m**2, 0d0) - 2))
    end do
  end do
  do i = 1, size(upts)
    do j = 1, size(xis)
      call row('SigV_u', upts(i), xis(j), xis(j) * cf * (1 + 2 * b1f(upts(i), 0d0, 0d0)))
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine row(name, x1, x2, val)
    character(len=*), intent(in) :: name
    double precision, intent(in) :: x1, x2
    double complex, intent(in) :: val
    write(w, '(a,2(",",g0),4(",",es24.16e3))') name, x1, x2, 0d0, 0d0, dble(val), aimag(val)
  end subroutine row

  double complex function b0f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    call B0_cll(b0f, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
  end function b0f

  double complex function b1f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    double complex :: bb(0:0, 0:1), bbuv(0:0, 0:1)
    call B_cll(bb, bbuv, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0), 1)
    b1f = bb(0, 1)
  end function b1f

end program oneloop_collier
