! af6_collier.f90 -- one-loop phi phi -> phi phi in d = 6 at high energies, for asymptotic freedom in scattering
! (research note, step (11)).  m = g = 1, MS-bar; the amplitude M1 (note, Eq. (22) (eq:M6)) is assembled as in
! scat6_collier.f90 from D0^(6) = -2 D00, C0^(6) = -2 C00, B0^(6) = -2 B00 (Delta_UV = 0, mu_UV = mu).
! Writes results/af6_collier.csv: 90-degree scattering (cos(theta) = 0) at 41 values of sqrt(s) from 2.5 to 10^4,
! each with mu = 1 and mu = sqrt(s), computed with both COLLIER branches (mode 1: COLI, mode 2: DD) as a
! stability check; plus the step (8) point sqrt(s) = 5, cos(theta) = 0.3, mu = 1 as a regression check.
!
! Build and run from Src/ (run_af6_check.sh does this):
!   gfortran -I$HOME/hep/include af6_collier.f90 -L$HOME/hep/lib -lcollier -o work/af6_collier
!   (cd work && ./af6_collier ../results/af6_collier.csv)
program af6_collier
  use COLLIER
  implicit none
  double precision, parameter :: pi = 3.14159265358979323846d0
  integer, parameter :: npts = 41
  character(len=256) :: outfile
  double precision :: rs, s, t, u, mu
  double complex :: m1
  integer :: i, j, mode, uo

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'af6_collier.csv'
  call Init_cll(4, 2, '')

  open(newunit=uo, file=trim(outfile), status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,mode,s,t,u,re_collier,im_collier'
  do mode = 1, 2
    call SetMode_cll(mode)
    do i = 0, npts - 1
      rs = exp(log(2.5d0) + i*log(1d4/2.5d0)/(npts - 1))
      call kinematics(rs, 0d0, s, t, u)
      do j = 1, 2
        mu = merge(1d0, rs, j == 1)
        call SetMuUV2_cll(mu**2)
        m1 = amp1(s, t, u)
        write(uo, '(3(g0,","),i0,",",5(g0,:,","))') rs, 0d0, mu, mode, s, t, u, dble(m1), aimag(m1)
      end do
    end do
    call SetMuUV2_cll(1d0)
    call kinematics(5d0, 0.3d0, s, t, u)
    m1 = amp1(s, t, u)
    write(uo, '(3(g0,","),i0,",",5(g0,:,","))') 5d0, 0.3d0, 1d0, mode, s, t, u, dble(m1), aimag(m1)
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine kinematics(rs, ct, s, t, u)
    double precision, intent(in) :: rs, ct
    double precision, intent(out) :: s, t, u
    double precision :: p2
    s = rs**2
    p2 = s/4d0 - 1d0
    t = -2d0*p2*(1d0 - ct)
    u = -2d0*p2*(1d0 + ct)
  end subroutine

  double complex function d06(x, y)      ! D0^(6) = -2 D00
    double precision, intent(in) :: x, y
    double complex, parameter :: one = (1d0, 0d0)
    double complex :: d(0:1,0:2,0:2,0:2), duv(0:1,0:2,0:2,0:2)
    call D_cll(d, duv, one, one, one, one, dcmplx(x, 0d0), dcmplx(y, 0d0), one, one, one, one, 2)
    d06 = -2d0*d(1,0,0,0)
  end function

  double complex function c06(x)         ! C0^(6)(m^2, m^2, x) = -2 C00
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    double complex :: c(0:1,0:2,0:2), cuv(0:1,0:2,0:2)
    call C_cll(c, cuv, one, one, dcmplx(x, 0d0), one, one, one, 2)
    c06 = -2d0*c(1,0,0)
  end function

  double complex function b06(x)         ! B0^(6)(x) = -2 B00
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    double complex :: b(0:1,0:2), buv(0:1,0:2)
    call B_cll(b, buv, dcmplx(x, 0d0), one, one, 2)
    b06 = -2d0*b(1,0)
  end function

  double complex function amp1(s, t, u)
    double precision, intent(in) :: s, t, u
    double precision :: xs(3)
    integer :: n
    xs = [s, t, u]
    amp1 = d06(s, t) + d06(s, u) + d06(t, u)
    do n = 1, 3
      amp1 = amp1 + 2d0*c06(xs(n))/(xs(n) - 1d0) + b06(xs(n))/(2d0*(xs(n) - 1d0)**2)
    end do
    amp1 = amp1/(64d0*pi**3)
  end function

end program
