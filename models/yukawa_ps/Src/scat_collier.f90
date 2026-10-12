! scat_collier.f90 -- one-loop phi phi -> phi phi and psi psibar -> phi phi of the pseudoscalar Yukawa + phi^4 model
! (research note models/yukawa_ps, eq:M1 and eq:M1B) from COLLIER, at m = mu = 1, M = 0.7, y = lambda = 1.
! COLLIER's defaults (Delta_UV = 0, mu^2 = 1) give the MS-bar finite parts.
!   (A) (4 pi)^2 M1 = lambda^2/2 sum_x B0(x; m^2, m^2) - 2 y^4 sum_(x,x') F(x, x')                       (Eq. (13))
!   (B) (4 pi)^2 M1 = a vbar(p2) u(p1) + b vbar(p2) k1slash u(p1), a and b the sum of the hand formulas for the self-energy,
!       vertex, box and lambda-triangle diagrams (note eq:M1B; the same formulas as handSE$, handV1$, handV2$, handBox$,
!       handLtri$ in scat_feyncalc.wl, here with COLLIER's tensor coefficients B1, C1, C2, D1, D2, D3).
! Writes results/scat_collier.csv at the points of scat_feyncalc.wl and results/scat_collier_scan.csv (cos(theta) scan at
! sqrt(s) = 5).  Build and run from Src/ (run_scat_check.sh does this):
!   gfortran -I$HOME/hep/include scat_collier.f90 -L$HOME/hep/lib -lcollier -o work/scat_collier
!   (cd work && ./scat_collier ../results/scat_collier.csv ../results/scat_collier_scan.csv)
program scat_collier
  use COLLIER
  implicit none
  double precision, parameter :: mphi = 1d0, mpsi = 0.7d0, y = 1d0, lam = 1d0
  double complex, parameter :: m2 = (mphi**2) * (1d0, 0d0), bm2 = (mpsi**2) * (1d0, 0d0)
  double precision, parameter :: rs(3) = [2.5d0, 5d0, 10d0], cs(2) = [0.3d0, 0.9d0]
  double precision :: sqs, c, s, tb, ub, ta, ua
  double complex :: a, b, ma
  character(len=256) :: f1, f2
  integer :: i, j, w

  call get_command_argument(1, f1); call get_command_argument(2, f2)
  if (len_trim(f1) == 0) f1 = 'scat_collier.csv'
  if (len_trim(f2) == 0) f2 = 'scat_collier_scan.csv'
  call Init_cll(4, 1, '')

  open(newunit=w, file=trim(f1), status='replace', action='write')
  write(w, '(a)') 'sqrts,costheta,s,t_B,t_A,re_a,im_a,re_b,im_b,re_mA,im_mA'
  do i = 1, size(rs)
    do j = 1, size(cs)
      call kin(rs(i), cs(j))
      call amp_b(a, b); ma = amp_a()
      write(w, '(5(g0,","),5(es24.16e3,","),es24.16e3)') rs(i), cs(j), s, tb, ta, dble(a), aimag(a), dble(b), aimag(b), &
        dble(ma), aimag(ma)
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(f1)

  open(newunit=w, file=trim(f2), status='replace', action='write')
  write(w, '(a)') 'sqrts,costheta,s,t_B,t_A,re_a,im_a,re_b,im_b,re_mA,im_mA'
  do i = -38, 38
    c = i / 40d0
    call kin(5d0, c)
    call amp_b(a, b); ma = amp_a()
    write(w, '(5(g0,","),5(es24.16e3,","),es24.16e3)') 5d0, c, s, tb, ta, dble(a), aimag(a), dble(b), aimag(b), &
      dble(ma), aimag(ma)
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(f2)

contains

  subroutine kin(sq, ct)
    ! (B): psi psibar -> phi phi, |p| = sqrt(E^2 - M^2), |k| = sqrt(E^2 - m^2);  (A): phi phi -> phi phi, |p| = sqrt(E^2 - m^2)
    double precision, intent(in) :: sq, ct
    double precision :: e, pb, kb, pa
    sqs = sq; c = ct; s = sq**2; e = sq / 2
    pb = sqrt(e**2 - mpsi**2); kb = sqrt(e**2 - mphi**2)
    tb = mpsi**2 + mphi**2 - 2 * (e**2 - pb * kb * ct)
    ub = 2 * mpsi**2 + 2 * mphi**2 - s - tb
    pa = sqrt(e**2 - mphi**2)
    ta = -2 * pa**2 * (1 - ct); ua = -2 * pa**2 * (1 + ct)
  end subroutine kin

  double complex function amp_a()
    double complex :: x(3)
    x = [dcmplx(s, 0d0), dcmplx(ta, 0d0), dcmplx(ua, 0d0)]
    amp_a = lam**2 / 2 * (b0mm(x(1)) + b0mm(x(2)) + b0mm(x(3))) &
          - 2 * y**4 * (fbox(x(1), x(2)) + fbox(x(2), x(3)) + fbox(x(3), x(1)))
  end function amp_a

  double complex function b0mm(x)
    double complex, intent(in) :: x
    call B0_cll(b0mm, x, m2, m2)
  end function b0mm

  double complex function fbox(x, xp)
    double complex, intent(in) :: x, xp
    double complex :: d0, c0x, c0xp, b0x, b0xp
    call D0_cll(d0, m2, m2, m2, m2, x, xp, bm2, bm2, bm2, bm2)
    call C0_cll(c0x, m2, m2, x, bm2, bm2, bm2)
    call C0_cll(c0xp, m2, m2, xp, bm2, bm2, bm2)
    call B0_cll(b0x, x, bm2, bm2)
    call B0_cll(b0xp, xp, bm2, bm2)
    fbox = (2 * m2**2 - x * xp) * d0 + 2 * (b0x + b0xp) + 2 * (x - 2 * m2) * c0x + 2 * (xp - 2 * m2) * c0xp
  end function fbox

  subroutine amp_b(a, b)
    double complex, intent(out) :: a, b
    double complex :: aa, bb
    a = (0d0, 0d0); b = (0d0, 0d0)
    call piece_se(tb, 1d0, aa, bb); a = a + aa; b = b + bb
    call piece_se(ub, -1d0, aa, bb); a = a + aa; b = b + bb
    call piece_v1(tb, 1d0, aa, bb); a = a + aa; b = b + bb
    call piece_v1(ub, -1d0, aa, bb); a = a + aa; b = b + bb
    call piece_v2(tb, 1d0, aa, bb); a = a + aa; b = b + bb
    call piece_v2(ub, -1d0, aa, bb); a = a + aa; b = b + bb
    call piece_box(tb, 1d0, aa, bb); a = a + aa; b = b + bb
    call piece_box(ub, -1d0, aa, bb); a = a + aa; b = b + bb
    call piece_ltri(aa); a = a + aa
  end subroutine amp_b

  subroutine piece_se(x, sg, aa, bb)
    ! internal fermion self-energy, B(x; M^2, m^2)
    double precision, intent(in) :: x, sg
    double complex, intent(out) :: aa, bb
    double complex :: bt(0:0,0:1), btuv(0:0,0:1)
    call B_cll(bt, btuv, dcmplx(x, 0d0), bm2, m2, 1)
    aa = y**4 * mpsi * (bt(0,0) + bt(0,1)) / (x - mpsi**2)
    bb = sg * y**4 * ((x + mpsi**2) * bt(0,1) + 2 * mpsi**2 * bt(0,0)) / (x - mpsi**2)**2
  end subroutine piece_se

  subroutine piece_v1(x, sg, aa, bb)
    ! vertex correction at the psi(p1) end: C(m^2, x, M^2; M^2, M^2, m^2)
    double precision, intent(in) :: x, sg
    double complex, intent(out) :: aa, bb
    double complex :: ct(0:0,0:1,0:1), ctuv(0:0,0:1,0:1), b0, al, be
    call C_cll(ct, ctuv, m2, dcmplx(x, 0d0), bm2, bm2, bm2, m2, 1)
    call B0_cll(b0, dcmplx(x, 0d0), bm2, m2)
    al = b0 + mphi**2 * ct(0,1,0)
    be = mpsi * (ct(0,0,0) + ct(0,0,1))
    aa = -y**4 * be
    bb = -sg * y**4 * (al + 2 * mpsi * be) / (x - mpsi**2)
  end subroutine piece_v1

  subroutine piece_v2(x, sg, aa, bb)
    ! vertex correction at the psibar(p2) end: C(m^2, M^2, x; M^2, M^2, m^2)
    double precision, intent(in) :: x, sg
    double complex, intent(out) :: aa, bb
    double complex :: ct(0:0,0:1,0:1), ctuv(0:0,0:1,0:1), b0, al
    call C_cll(ct, ctuv, m2, bm2, dcmplx(x, 0d0), bm2, bm2, m2, 1)
    call B0_cll(b0, bm2, bm2, m2)
    al = b0 + mphi**2 * ct(0,1,0)
    aa = -y**4 * mpsi * (ct(0,0,0) + ct(0,0,1))
    bb = -sg * y**4 * (al + 2 * mpsi**2 * ct(0,0,0) + (x + mpsi**2) * ct(0,0,1)) / (x - mpsi**2)
  end subroutine piece_v2

  subroutine piece_box(x, sg, aa, bb)
    ! box: D(M^2, m^2, m^2, M^2, x, s; m^2, M^2, M^2, M^2), Cs = C(M^2, s, M^2; m^2, M^2, M^2), C0(m^2, m^2, s; M^2, M^2, M^2)
    double precision, intent(in) :: x, sg
    double complex, intent(out) :: aa, bb
    double complex :: dt(0:0,0:1,0:1,0:1), dtuv(0:0,0:1,0:1,0:1), ct(0:0,0:1,0:1), ctuv(0:0,0:1,0:1), c0m
    call D_cll(dt, dtuv, bm2, m2, m2, bm2, dcmplx(x, 0d0), dcmplx(s, 0d0), m2, bm2, bm2, bm2, 1)
    call C_cll(ct, ctuv, bm2, dcmplx(s, 0d0), bm2, m2, bm2, bm2, 1)
    call C0_cll(c0m, m2, m2, dcmplx(s, 0d0), bm2, bm2, bm2)
    aa = -y**4 * mpsi * ((x - mpsi**2) * (dt(0,1,0,0) + dt(0,0,1,0) + dt(0,0,0,1)) - (ct(0,1,0) + ct(0,0,1)))
    bb = sg * y**4 * (mphi**2 * dt(0,0,0,0) + c0m + (x - mpsi**2) * dt(0,0,1,0))
  end subroutine piece_box

  subroutine piece_ltri(aa)
    ! lambda triangle: lambda y^2 M C1(M^2, M^2, s; m^2, M^2, m^2)
    double complex, intent(out) :: aa
    double complex :: ct(0:0,0:1,0:1), ctuv(0:0,0:1,0:1)
    call C_cll(ct, ctuv, bm2, bm2, dcmplx(s, 0d0), m2, bm2, m2, 1)
    aa = lam * y**2 * mpsi * ct(0,1,0)
  end subroutine piece_ltri

end program
