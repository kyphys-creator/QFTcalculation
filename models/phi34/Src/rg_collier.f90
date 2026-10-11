! rg_collier.f90 -- MS-bar one-loop phi phi -> phi phi of phi^3 + phi^4 in d = 4 (note, Eq. (9) (eq:M1)) at several mu,
! for the renormalization-group check (research note models/phi34, step (7)).  m = g = lambda = 1, Delta_UV = 0,
! mu_UV = mu.  Writes results/rg_collier.csv (the six points of step (4), mu = 1, 1/2, 2) and
! results/rg_collier_muscan.csv (sqrt(s) = 5, cos(theta) = 0.3, mu = 1/4 ... 4).  The amplitude is assembled as in
! scat_collier.f90; rg_collier.csv also has the real parts of its three coupling structures, M1 = g^4 P + g^2 lambda Q
! + lambda^2 R (columns re_p, re_q, re_r), for the four-coefficient fit of rg_numeric.py.
!
! Build and run from Src/ (run_rg_check.sh does this):
!   gfortran -I$HOME/hep/include rg_collier.f90 -L$HOME/hep/lib -lcollier -o work/rg_collier
!   (cd work && ./rg_collier ../results)
program rg_collier
  use COLLIER
  implicit none
  double precision, parameter :: pi = 3.14159265358979323846d0
  double precision, parameter :: rts(3) = [2.5d0, 5d0, 10d0], cths(2) = [0.3d0, 0.9d0], mus(3) = [1d0, 0.5d0, 2d0]
  character(len=256) :: dir
  double precision :: s, t, u, mu
  double complex :: m1, parts(3)
  integer :: i, j, k, uo

  call get_command_argument(1, dir)
  if (len_trim(dir) == 0) dir = '.'
  call Init_cll(4, 0, '')

  open(newunit=uo, file=trim(dir)//'/rg_collier.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier,re_p,re_q,re_r'
  do k = 1, size(mus)
    call SetMuUV2_cll(mus(k)**2)
    do i = 1, size(rts)
      do j = 1, size(cths)
        call kinematics(rts(i), cths(j), s, t, u)
        call structures(s, t, u, parts)
        m1 = sum(parts)
        write(uo, '(11(g0,:,","))') rts(i), cths(j), mus(k), s, t, u, dble(m1), aimag(m1), dble(parts)
      end do
    end do
  end do
  close(uo)

  open(newunit=uo, file=trim(dir)//'/rg_collier_muscan.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier'
  do k = 0, 16
    mu = exp(log(0.25d0) + k*log(16d0)/16d0)
    call SetMuUV2_cll(mu**2)
    call kinematics(5d0, 0.3d0, s, t, u)
    m1 = amp1(s, t, u)
    write(uo, '(8(g0,:,","))') 5d0, 0.3d0, mu, s, t, u, dble(m1), aimag(m1)
  end do
  close(uo)
  print '(a,a)', 'wrote rg_collier*.csv in ', trim(dir)

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

  double complex function d0f(x, y)
    double precision, intent(in) :: x, y
    double complex, parameter :: one = (1d0, 0d0)
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
    double complex :: parts(3)
    call structures(s, t, u, parts)
    amp1 = sum(parts)
  end function

  subroutine structures(s, t, u, parts)
    ! parts = (g^4 P, g^2 lambda Q, lambda^2 R) at g = lambda = 1, each divided by (4 pi)^2
    double precision, intent(in) :: s, t, u
    double complex, intent(out) :: parts(3)
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
    parts = [g**4*g4, g**2*lam*g2l, lam**2*l2]/(16d0*pi**2)
  end subroutine

end program
