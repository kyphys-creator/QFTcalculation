! scat_collier.f90 -- one-loop phi phi -> phi phi of phi^3 + phi^4 in d = 4 from COLLIER integrals (research note
! models/phi34, step (4)).  m = g = lambda = mu = 1, Delta_UV = 0 (MS-bar).  The MS-bar renormalized, truncated one-loop
! amplitude (no external-leg corrections, tadpoles cancelled by Y; note, Eq. (9) (eq:M1)) is assembled from
!   (4 pi)^2 M1 = g^4 [ D0(s,t) + D0(s,u) + D0(t,u) + sum_x ( 2 C0(x)/(x - m^2) + B0(x)/(2 (x - m^2)^2) ) ]
!               + g^2 lambda sum_x [ 2 C0(x) + (B0(x) + 2 B0(m^2))/(x - m^2) + A0/(2 (x - m^2)^2) ]
!               + lambda^2/2 sum_x B0(x),     C0(x) = C0(m^2, m^2, x),
! with all internal masses m and all external p_i^2 = m^2.
! Writes results/scat_collier.csv (the comparison points) and results/scat_collier_scan.csv
! (sqrt(s) = 5, cos(theta) = 0 ... 0.98, for the figure).
!
! Build and run from Src/ (run_scat_check.sh does this):
!   gfortran -I$HOME/hep/include scat_collier.f90 -L$HOME/hep/lib -lcollier -o work/scat_collier
!   (cd work && ./scat_collier ../results/scat_collier.csv ../results/scat_collier_scan.csv)
program scat_collier
  use COLLIER
  implicit none
  double precision, parameter :: pi = 3.14159265358979323846d0
  double precision, parameter :: rts(3) = [2.5d0, 5d0, 10d0], cths(2) = [0.3d0, 0.9d0]
  character(len=256) :: outfile, scanfile
  double precision :: s, t, u
  double complex :: m1
  integer :: i, j, k, u1, u2

  call get_command_argument(1, outfile)
  call get_command_argument(2, scanfile)
  if (len_trim(outfile) == 0) outfile = 'scat_collier.csv'
  if (len_trim(scanfile) == 0) scanfile = 'scat_collier_scan.csv'
  call Init_cll(4, 0, '')

  open(newunit=u1, file=trim(outfile), status='replace', action='write')
  write(u1, '(a)') 'sqrts,costheta,s,t,u,re_collier,im_collier'
  do i = 1, size(rts)
    do j = 1, size(cths)
      call kinematics(rts(i), cths(j), s, t, u)
      m1 = amp1(s, t, u)
      write(u1, '(7(g0,:,","))') rts(i), cths(j), s, t, u, dble(m1), aimag(m1)
    end do
  end do
  close(u1)

  open(newunit=u2, file=trim(scanfile), status='replace', action='write')
  write(u2, '(a)') 'sqrts,costheta,s,t,u,re_collier,im_collier'
  do k = 0, 49
    call kinematics(5d0, 0.02d0*k, s, t, u)
    m1 = amp1(s, t, u)
    write(u2, '(7(g0,:,","))') 5d0, 0.02d0*k, s, t, u, dble(m1), aimag(m1)
  end do
  close(u2)
  print '(a,a,a,a)', 'wrote ', trim(outfile), ' and ', trim(scanfile)

contains

  subroutine kinematics(rs, ct, s, t, u)
    ! centre-of-mass frame, m = 1: p^2 = s/4 - m^2, t = -2 p^2 (1 - cos), u = -2 p^2 (1 + cos)
    double precision, intent(in) :: rs, ct
    double precision, intent(out) :: s, t, u
    double precision :: p2
    s = rs**2
    p2 = s/4d0 - 1d0
    t = -2d0*p2*(1d0 - ct)
    u = -2d0*p2*(1d0 + ct)
  end subroutine

  double complex function d0f(x, y)
    double precision, intent(in) :: x, y
    double complex, parameter :: one = (1d0, 0d0)
    ! D0_cll(D0, p10, p21, p32, p30, p20, p31, m02, m12, m22, m32): p20 and p31 are the two invariants
    call D0_cll(d0f, one, one, one, one, dcmplx(x, 0d0), dcmplx(y, 0d0), one, one, one, one)
  end function

  double complex function c0f(x)
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    call C0_cll(c0f, one, one, dcmplx(x, 0d0), one, one, one)
  end function

  double complex function b0f(x)
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    call B0_cll(b0f, dcmplx(x, 0d0), one, one)
  end function

  double complex function amp1(s, t, u)
    double precision, intent(in) :: s, t, u
    double precision, parameter :: g = 1d0, lam = 1d0
    double complex, parameter :: one = (1d0, 0d0)
    double precision :: xs(3)
    double complex :: a0, b0m, g4, g2l, l2
    integer :: n
    xs = [s, t, u]
    call A0_cll(a0, one)
    b0m = b0f(1d0)
    g4 = d0f(s, t) + d0f(s, u) + d0f(t, u)
    g2l = (0d0, 0d0)
    l2 = (0d0, 0d0)
    do n = 1, 3
      g4 = g4 + 2d0*c0f(xs(n))/(xs(n) - 1d0) + b0f(xs(n))/(2d0*(xs(n) - 1d0)**2)
      g2l = g2l + 2d0*c0f(xs(n)) + (b0f(xs(n)) + 2d0*b0m)/(xs(n) - 1d0) + a0/(2d0*(xs(n) - 1d0)**2)
      l2 = l2 + b0f(xs(n))/2d0
    end do
    amp1 = (g**4*g4 + g**2*lam*g2l + lam**2*l2)/(16d0*pi**2)
  end function

end program
