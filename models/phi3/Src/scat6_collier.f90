! scat6_collier.f90 -- one-loop phi phi -> phi phi in d = 6 from COLLIER (research note, step (8)).
! m = g = 1, MS-bar.  The d = 6 MS-bar finite parts follow from the D = 4 - 2 eps tensor coefficients
! (note, App. H):  X_N = -2 T00(Delta_UV = 0, mu_UV = mu), i.e. D0^(6) = -2 D00, C0^(6) = -2 C00,
! B0^(6) = -2 B00, and
!   M1 = 1/(4 pi)^3 [ D0^(6)(s,t) + D0^(6)(s,u) + D0^(6)(t,u)
!                     + sum_x ( 2 C0^(6)(x)/(x - m^2) + B0^(6)(x)/(2 (x - m^2)^2) ) ]      (note, Eq. (22) (eq:M6)).
! Writes results/scat6_collier.csv (the six points, mu = 1, 1/2, 2), results/scat6_collier_scan.csv
! (sqrt(s) = 5, cos(theta) = 0 ... 0.98, mu = 1) and results/scat6_collier_muscan.csv
! (sqrt(s) = 5, cos(theta) = 0.3, mu = 1/4 ... 4).
!
! Build and run from Src/ (run_scat6_check.sh does this):
!   gfortran -I$HOME/hep/include scat6_collier.f90 -L$HOME/hep/lib -lcollier -o work/scat6_collier
!   (cd work && ./scat6_collier ../results)
program scat6_collier
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
  call Init_cll(4, 2, '')

  open(newunit=uo, file=trim(dir)//'/scat6_collier.csv', status='replace', action='write')
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

  call SetMuUV2_cll(1d0)
  open(newunit=uo, file=trim(dir)//'/scat6_collier_scan.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier'
  do k = 0, 49
    call kinematics(5d0, 0.02d0*k, s, t, u)
    m1 = amp1(s, t, u)
    write(uo, '(8(g0,:,","))') 5d0, 0.02d0*k, 1d0, s, t, u, dble(m1), aimag(m1)
  end do
  close(uo)

  open(newunit=uo, file=trim(dir)//'/scat6_collier_muscan.csv', status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t,u,re_collier,im_collier'
  do k = 0, 16
    mu = exp(log(0.25d0) + k*log(16d0)/16d0)
    call SetMuUV2_cll(mu**2)
    call kinematics(5d0, 0.3d0, s, t, u)
    m1 = amp1(s, t, u)
    write(uo, '(8(g0,:,","))') 5d0, 0.3d0, mu, s, t, u, dble(m1), aimag(m1)
  end do
  close(uo)
  print '(a,a)', 'wrote scat6_collier*.csv in ', trim(dir)

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
