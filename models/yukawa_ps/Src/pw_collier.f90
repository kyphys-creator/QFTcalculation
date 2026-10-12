! pw_collier.f90 -- the one-loop amplitudes of the pseudoscalar Yukawa + phi^4 model (research note models/yukawa_ps,
! Eqs. (13) and (18), MS-bar) split into coupling structures, for the partial waves of step (8).
! m = 1, M = 0.7, y = lambda = 1 in the loops (the structures are rescaled by the couplings in pw_numeric.py), Delta_UV = 0,
! mu^2 set with SetMuUV2_cll.  The functions are those of scat_collier.f90, xsec_collier.f90 and rg_collier.f90.
! Reads lines "sqrts costheta mu" from the file given as the first argument and writes to the second
!   "sqrts,costheta,mu,re_ay,im_ay,re_al,im_al,re_b,im_b,re_mAl,im_mAl,re_mAy,im_mAy":
!   (4 pi)^2 M1(psi psibar -> phi phi) = (y^4 ay + lambda y^2 al) vbar u + y^4 b vbar k1slash u  (al: the lambda triangle),
!   (4 pi)^2 M1(phi phi -> phi phi) = lambda^2 mAl + y^4 mAy  (phi bubbles, fermion boxes).
! Build and run from Src/ (run_pw_check.sh builds it, pw_numeric.py runs it):
!   gfortran -I$HOME/hep/include pw_collier.f90 -L$HOME/hep/lib -lcollier -o work/pw_collier
program pw_collier
  use COLLIER
  implicit none
  double precision, parameter :: mphi = 1d0, mpsi = 0.7d0, y = 1d0, lam = 1d0
  double complex, parameter :: m2 = (mphi**2) * (1d0, 0d0), bm2 = (mpsi**2) * (1d0, 0d0)
  double precision :: sqs, c, s, tb, ub, ta, ua, rs, ct, mu
  double complex :: a, b, al, mlam, my4
  character(len=256) :: f1, f2
  integer :: ui, uo, ios

  call get_command_argument(1, f1); call get_command_argument(2, f2)
  call Init_cll(4, 1, '')
  open(newunit=ui, file=trim(f1), status='old', action='read')
  open(newunit=uo, file=trim(f2), status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,mu,re_ay,im_ay,re_al,im_al,re_b,im_b,re_mAl,im_mAl,re_mAy,im_mAy'
  do
    read(ui, *, iostat=ios) rs, ct, mu
    if (ios /= 0) exit
    call SetMuUV2_cll(mu**2)
    call kin(rs, ct)
    call amp_b(a, b); call piece_ltri(al); call amp_a_split(mlam, my4)
    write(uo, '(12(es24.16e3,","),es24.16e3)') rs, ct, mu, dble(a - al), aimag(a - al), dble(al), aimag(al), &
      dble(b), aimag(b), dble(mlam), aimag(mlam), dble(my4), aimag(my4)
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
