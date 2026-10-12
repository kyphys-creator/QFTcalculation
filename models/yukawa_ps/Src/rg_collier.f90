! rg_collier.f90 -- the one-loop amplitudes of the pseudoscalar Yukawa + phi^4 model (research note models/yukawa_ps,
! Eqs. (13) and (18), MS-bar) at several renormalization scales mu (step (7)), and the loop functions of the pole masses.
! m = 1, M = 0.7, y = lambda = 1, Delta_UV = 0, mu^2 set with SetMuUV2_cll.  The amplitudes are assembled exactly as in
! scat_collier.f90 and xsec_collier.f90 (same functions).
!   1. Reads lines "sqrts costheta mu" from the file given as the first argument and writes
!      "sqrts,costheta,mu,s,t_B,t_A,re_a,im_a,re_b,im_b,re_mA,im_mA,re_mA_lam,re_mA_y4" to the second:
!      a, b: (4 pi)^2 M1 = a vbar u + b vbar k1slash u (psi psibar <-> phi phi);  mA: (4 pi)^2 M1 of phi phi -> phi phi,
!      split into the phi bubbles (mA_lam, lambda^2) and the fermion boxes (mA_y4, y^4).
!   2. Reads lines "mu" from the third file and writes the loop functions of Eqs. (15) and (17) (eq:mpole, eq:Mpole) to the
!      fourth: "mu,re_A0m,re_A0M,re_B0MM_m2,re_B0Mm_M2,re_B1Mm_M2" = A0(m^2), A0(M^2), B0(m^2; M^2, M^2), B0(M^2; M^2, m^2),
!      B1(M^2; M^2, m^2) (real at these points).
! Build and run from Src/ (run_rg_check.sh):
!   gfortran -I$HOME/hep/include rg_collier.f90 -L$HOME/hep/lib -lcollier -o work/rg_collier
!   (cd work && ./rg_collier rg_nodes.txt rg_amp.csv rg_mus.txt rg_pole.csv)
program rg_collier
  use COLLIER
  implicit none
  double precision, parameter :: mphi = 1d0, mpsi = 0.7d0, y = 1d0, lam = 1d0
  double complex, parameter :: m2 = (mphi**2) * (1d0, 0d0), bm2 = (mpsi**2) * (1d0, 0d0)
  double precision :: sqs, c, s, tb, ub, ta, ua, rs, ct, mu
  double complex :: a, b, ma, mlam, my4, a0m, a0bm, b0mm_m2, bt(0:0,0:1), btuv(0:0,0:1)
  character(len=256) :: f1, f2, f3, f4
  integer :: ui, uo, ios

  call get_command_argument(1, f1); call get_command_argument(2, f2)
  call get_command_argument(3, f3); call get_command_argument(4, f4)
  call Init_cll(4, 1, '')
  open(newunit=ui, file=trim(f1), status='old', action='read')
  open(newunit=uo, file=trim(f2), status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,s,t_B,t_A,re_a,im_a,re_b,im_b,re_mA,im_mA,re_mA_lam,re_mA_y4'
  do
    read(ui, *, iostat=ios) rs, ct, mu
    if (ios /= 0) exit
    call SetMuUV2_cll(mu**2)
    call kin(rs, ct)
    call amp_b(a, b); ma = amp_a(); call amp_a_split(mlam, my4)
    write(uo, '(13(es24.16e3,","),es24.16e3)') rs, ct, mu, s, tb, ta, dble(a), aimag(a), dble(b), aimag(b), &
      dble(ma), aimag(ma), dble(mlam), dble(my4)
  end do
  close(ui); close(uo)
  open(newunit=ui, file=trim(f3), status='old', action='read')
  open(newunit=uo, file=trim(f4), status='replace', action='write')
  write(uo, '(a)') 'mu,re_A0m,re_A0M,re_B0MM_m2,re_B0Mm_M2,re_B1Mm_M2'
  do
    read(ui, *, iostat=ios) mu
    if (ios /= 0) exit
    call SetMuUV2_cll(mu**2)
    call A0_cll(a0m, m2)
    call A0_cll(a0bm, bm2)
    call B0_cll(b0mm_m2, m2, bm2, bm2)
    call B_cll(bt, btuv, bm2, bm2, m2, 1)
    write(uo, '(5(es24.16e3,","),es24.16e3)') mu, dble(a0m), dble(a0bm), dble(b0mm_m2), dble(bt(0,0)), dble(bt(0,1))
  end do
  close(ui); close(uo)

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

  subroutine amp_a_split(mlam, my4)
    ! the two coupling structures of (4 pi)^2 M1 of phi phi -> phi phi: phi bubbles (lambda^2) and fermion boxes (y^4)
    double complex, intent(out) :: mlam, my4
    double complex :: x(3)
    x = [dcmplx(s, 0d0), dcmplx(ta, 0d0), dcmplx(ua, 0d0)]
    mlam = lam**2 / 2 * (b0mm(x(1)) + b0mm(x(2)) + b0mm(x(3)))
    my4 = -2 * y**4 * (fbox(x(1), x(2)) + fbox(x(2), x(3)) + fbox(x(3), x(1)))
  end subroutine amp_a_split

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
