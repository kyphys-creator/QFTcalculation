! rg4_collier.f90 -- MS-bar one-loop phi phi -> phi phi in d = 4 (note, Eq. (17)) at several mu, for the
! renormalization-group check (research note, step (9)).  m = g = 1, Delta_UV = 0, mu_UV = mu.
! Writes results/rg4_collier.csv (the six points of step (5), mu = 1, 1/2, 2) and
! results/rg4_collier_muscan.csv (sqrt(s) = 5, cos(theta) = 0.3, mu = 1/4 ... 4).  The amplitude is
! assembled as in scat4_collier.f90.
!
! Build and run from Src/ (run_rg4_check.sh does this):
!   gfortran -I$HOME/hep/include rg4_collier.f90 -L$HOME/hep/lib -lcollier -o work/rg4_collier
!   (cd work && ./rg4_collier ../results)
program rg4_collier
  use COLLIER
  implicit none
  double precision, parameter :: pi = 3.14159265358979323846d0
  double precision, parameter :: rts(3) = [2.5d0, 5d0, 10d0], cths(2) = [0.3d0, 0.9d0], mus(3) = [1d0, 0.5d0, 2d0]
  character(len=256) :: dir
  double precision :: s, t, u, mu
  double complex :: m1
  integer :: i, j, k, uo

  call get_command_argument(1, dir)
  if (len_trim(dir) == 0) dir = '.'
  call Init_cll(4, 0, '')

  open(newunit=uo, file=trim(dir)//'/rg4_collier.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier'
  do k = 1, size(mus)
    call SetMuUV2_cll(mus(k)**2)
    do i = 1, size(rts)
      do j = 1, size(cths)
        call kinematics(rts(i), cths(j), s, t, u)
        m1 = amp1(s, t, u)
        write(uo, '(8(g0,:,","))') rts(i), cths(j), mus(k), s, t, u, dble(m1), aimag(m1)
      end do
    end do
  end do
  close(uo)

  open(newunit=uo, file=trim(dir)//'/rg4_collier_muscan.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier'
  do k = 0, 16
    mu = exp(log(0.25d0) + k*log(16d0)/16d0)
    call SetMuUV2_cll(mu**2)
    call kinematics(5d0, 0.3d0, s, t, u)
    m1 = amp1(s, t, u)
    write(uo, '(8(g0,:,","))') 5d0, 0.3d0, mu, s, t, u, dble(m1), aimag(m1)
  end do
  close(uo)
  print '(a,a)', 'wrote rg4_collier*.csv in ', trim(dir)

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
    double precision :: xs(3)
    integer :: n
    xs = [s, t, u]
    amp1 = d0f(s, t) + d0f(s, u) + d0f(t, u)
    do n = 1, 3
      amp1 = amp1 + 2d0*c0f(xs(n))/(xs(n) - 1d0) + b0f(xs(n))/(2d0*(xs(n) - 1d0)**2)
    end do
    amp1 = amp1/(16d0*pi**2)
  end function

end program
