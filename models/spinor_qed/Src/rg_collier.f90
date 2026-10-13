! rg_collier.f90 -- the mu-dependence of the one-loop quantities of spinor QED with COLLIER (research note models/spinor_qed,
! step (7)).  e = 1, m_e = 1, m_mu = 1.7, Feynman gauge for the S-matrix element, MS-bar at the scale mu (mu_UV = mu_IR = mu,
! SetMuUV2_cll, SetMuIR2_cll; Delta_UV = Delta_IR = 0).  The functions are those of oneloop_collier.f90 (1PI brackets) and of
! xsec_collier.f90 / scat_collier.f90 (the interference), copied below "contains".
!   1. 1PI brackets (K/e^2 times the note's quantities, MS-bar finite parts) at mu = 1/2, 1, 2:
!      Pi_e, Pi_mu at q^2;  SigV, SigS of e and mu at p^2 for xi = 0, 1, 3;  Mpole = SigV + SigS at p^2 = m^2 (the pole mass,
!      Eq. (os));  R - 1 minus delta2 at p^2 = m^2 (finite part and IR pole) -> the file given as the first argument,
!      rows "func,arg,xi,mu,re_pole,im_pole,re_fin,im_fin".
!   2. K W/e^6 of e+ e- -> mu+ mu- (the total of the classes VP, Le, Lmu, box of Eq. (15), CDR): reads lines "s t mu" from
!      the second argument and writes "s,t,mu,born4,re_pole,im_pole,re_fin,im_fin" to the third (pole = UV + IR; the UV pole
!      is 0 after the counterterms).
! Build and run from Src/ (run_rg_check.sh builds it; rg_numeric.py runs it):
!   gfortran -I$HOME/hep/include rg_collier.f90 -L$HOME/hep/lib -lcollier -o work/rg_collier
!   (cd work && ./rg_collier rg_onepi_collier.csv rg_points.txt rg_amp_collier.csv)
program rg_collier
  use COLLIER
  implicit none
  double precision, parameter :: me = 1d0, mmu = 1.7d0
  double precision, parameter :: mus(3) = [0.5d0, 1d0, 2d0]
  double precision, parameter :: pipts(7) = [-5d0, -1d0, 0.5d0, 2d0, 3.9d0, 6d0, 20d0]
  double precision, parameter :: sigpts(5) = [-5d0, 0.5d0, 2d0, 4d0, 10d0], xis(3) = [0d0, 1d0, 3d0]
  character(len=256) :: f1n, f2n, f3n
  integer :: i, j, k, w, ui, uo, ios
  double precision :: s, t, u, mu, b4
  double complex :: fin, ir, v00(4), vuv(4), vir(4), fv(4), pole

  call get_command_argument(1, f1n); call get_command_argument(2, f2n); call get_command_argument(3, f3n)
  call Init_cll(4, 2, '')

  ! 1. the 1PI brackets
  open(newunit=w, file=trim(f1n), status='replace', action='write')
  write(w, '(a)') 'func,arg,xi,mu,re_pole,im_pole,re_fin,im_fin'
  do k = 1, size(mus)
    call setmu(mus(k))
    do i = 1, size(pipts)
      call row('Pi_e', pipts(i), 0d0, mus(k), (0d0, 0d0), pif(pipts(i), me))
      call row('Pi_mu', pipts(i), 0d0, mus(k), (0d0, 0d0), pif(pipts(i), mmu))
    end do
    do i = 1, size(sigpts)
      do j = 1, size(xis)
        call row('SigV_e', sigpts(i), xis(j), mus(k), (0d0, 0d0), sigv(sigpts(i), me, xis(j)))
        call row('SigS_e', sigpts(i), xis(j), mus(k), (0d0, 0d0), sigs(sigpts(i), me, xis(j)))
        call row('SigV_mu', sigpts(i), xis(j), mus(k), (0d0, 0d0), sigv(sigpts(i), mmu, xis(j)))
        call row('SigS_mu', sigpts(i), xis(j), mus(k), (0d0, 0d0), sigs(sigpts(i), mmu, xis(j)))
      end do
    end do
    do j = 1, size(xis)
      call row('Mpole_e', me, xis(j), mus(k), (0d0, 0d0), sigv(me**2, me, xis(j)) + sigs(me**2, me, xis(j)))
      call row('Mpole_mu', mmu, xis(j), mus(k), (0d0, 0d0), sigv(mmu**2, mmu, xis(j)) + sigs(mmu**2, mmu, xis(j)))
      call rres(me, xis(j), fin, ir)
      call row('R_e', me, xis(j), mus(k), ir, fin)
      call rres(mmu, xis(j), fin, ir)
      call row('R_mu', mmu, xis(j), mus(k), ir, fin)
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(f1n)

  ! 2. the interference at the given points and scales
  open(newunit=ui, file=trim(f2n), status='old', action='read')
  open(newunit=uo, file=trim(f3n), status='replace', action='write')
  write(uo, '(a)') 's,t,mu,born4,re_pole,im_pole,re_fin,im_fin'
  do
    read(ui, *, iostat=ios) s, t, mu
    if (ios /= 0) exit
    call setmu(mu)
    u = 2 * me**2 + 2 * mmu**2 - s - t
    b4 = 8 / s**2 * ((t - me**2 - mmu**2)**2 + (u - me**2 - mmu**2)**2 + 2 * s * (me**2 + mmu**2))
    call classes(s, t, u, 0d0, 0d0, v00)
    call classes(s, t, u, 1d0, 0d0, vuv)
    call classes(s, t, u, 0d0, 1d0, vir)
    call cdr(s, t, u, b4, fv)
    pole = sum(vuv - v00) + sum(vir - v00)
    write(uo, '(g0,7(",",es24.16e3))') s, t, mu, b4, dble(pole), aimag(pole), dble(sum(fv)), aimag(sum(fv))
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(f3n)

contains

  subroutine setmu(mu)
    double precision, intent(in) :: mu
    call SetMuUV2_cll(mu**2)
    call SetMuIR2_cll(mu**2)
  end subroutine setmu

  subroutine row(name, x1, x2, x3, pl, val)
    character(len=*), intent(in) :: name
    double precision, intent(in) :: x1, x2, x3
    double complex, intent(in) :: pl, val
    write(w, '(a,3(",",g0),4(",",es24.16e3))') name, x1, x2, x3, dble(pl), aimag(pl), dble(val), aimag(val)
  end subroutine row

  subroutine setdelta(duv, dir)
    double precision, intent(in) :: duv, dir
    call SetDeltaUV_cll(duv)
    call SetDeltaIR_cll(dir, 0d0)
  end subroutine setdelta

  ! ---- 1PI brackets (oneloop_collier.f90) ----

  double complex function sigv(p2, m, xi)
    double precision, intent(in) :: p2, m, xi
    double complex :: bb(0:0, 0:1), bbuv(0:0, 0:1)
    call B_cll(bb, bbuv, dcmplx(p2, 0d0), dcmplx(m**2, 0d0), (0d0, 0d0), 1)
    sigv = xi * (1 + 2 * bb(0, 1))
  end function sigv

  double complex function sigs(p2, m, xi)
    double precision, intent(in) :: p2, m, xi
    sigs = (3 + xi) * b0f(p2, m**2, 0d0) - 2
  end function sigs

  subroutine rres(m, xi, fin, ir)
    ! K (R - 1)/e^2 at p^2 = m^2 minus delta2 (removes the UV pole -xi): finite part and IR pole coefficient
    double precision, intent(in) :: m, xi
    double complex, intent(out) :: fin, ir
    double complex :: bb(0:0, 0:1), bbuv(0:0, 0:1), db0a, db0b, db1a, db1b, rb0, rb1
    double precision :: m2
    m2 = m**2
    call B_cll(bb, bbuv, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0), 1)
    call SetDeltaIR_cll(0d0, 0d0)
    call DB0_cll(db0a, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call DB1_cll(db1a, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call SetDeltaIR_cll(1d0, 0d0)
    call DB0_cll(db0b, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call DB1_cll(db1b, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call SetDeltaIR_cll(0d0, 0d0)
    rb0 = db0b - db0a
    rb1 = db1b - db1a
    fin = xi * (1 + 2 * bb(0, 1)) + 2 * m2 * (xi * (2 * db1a - 2 * rb1) + (3 + xi) * db0a - 2 * rb0)
    ir = 2 * m2 * (xi * 2 * rb1 + (3 + xi) * rb0)
  end subroutine rres

  ! ---- the interference (xsec_collier.f90, scat_collier.f90) ----

  ! K W/e^6 of the four classes for D -> 4 (b(4) B(4) and the D = 4 box) at the current Delta_UV, Delta_IR
  subroutine classes(s, t, u, duv, dir, v)
    double precision, intent(in) :: s, t, u, duv, dir
    double complex, intent(out) :: v(4)
    double precision :: b4
    double complex :: c0(15), c1(15), ints(15)
    call setdelta(duv, dir)
    b4 = 8 / s**2 * ((t - me**2 - mmu**2)**2 + (u - me**2 - mmu**2)**2 + 2 * s * (me**2 + mmu**2))
    v(1) = (pif(s, me) + pif(s, mmu) + 8d0 / 3d0 * duv) * b4
    v(2) = (f1(s, me) + rm1(me)) * b4 + f2(s, me) * 8 * (s + 2 * mmu**2) / s
    v(3) = (f1(s, mmu) + rm1(mmu)) * b4 + f2(s, mmu) * 8 * (s + 2 * me**2) / s
    call boxtab(s, t, c0, c1, ints)
    v(4) = 4 * sum((c0 + 4 * c1) * ints) / s
    call boxtab(s, u, c0, c1, ints)
    v(4) = v(4) - 4 * sum((c0 + 4 * c1) * ints) / s
    call setdelta(0d0, 0d0)
  end subroutine classes

  ! MS-bar finite parts in CDR: D = 4 values at Delta = 0 plus the rational terms of (D - 4) x poles
  subroutine cdr(s, t, u, b4, f)
    double precision, intent(in) :: s, t, u, b4
    double complex, intent(out) :: f(4)
    double complex :: br0(3), bru(3), bri(3), c0(15), c1(15), i0(15), iu(15), ii(15)
    double precision :: x
    integer :: k
    call brackets(s, 0d0, 0d0, br0)
    call brackets(s, 1d0, 0d0, bru)
    call brackets(s, 0d0, 1d0, bri)
    call setdelta(0d0, 0d0)
    f(1) = br0(1) * b4 - 8 * ((bru(1) - br0(1)) + (bri(1) - br0(1)))
    f(2) = br0(2) * b4 - 8 * ((bru(2) - br0(2)) + (bri(2) - br0(2))) + f2(s, me) * 8 * (s + 2 * mmu**2) / s
    f(3) = br0(3) * b4 - 8 * ((bru(3) - br0(3)) + (bri(3) - br0(3))) + f2(s, mmu) * 8 * (s + 2 * me**2) / s
    f(4) = 0
    do k = 1, 2
      x = t; if (k == 2) x = u
      call setdelta(0d0, 0d0); call boxtab(s, x, c0, c1, i0)
      call setdelta(1d0, 0d0); call boxtab(s, x, c0, c1, iu)
      call setdelta(0d0, 1d0); call boxtab(s, x, c0, c1, ii)
      call setdelta(0d0, 0d0)
      f(4) = f(4) + (3 - 2 * k) * 4 * sum((c0 + 4 * c1) * i0 - 2 * c1 * ((iu - i0) + (ii - i0))) / s
    end do
  end subroutine cdr

  ! the brackets multiplying B(D) (K/e^2 units): VP with -delta3, F1^Lambda + R - 1 for e and mu
  subroutine brackets(s, duv, dir, br)
    double precision, intent(in) :: s, duv, dir
    double complex, intent(out) :: br(3)
    call setdelta(duv, dir)
    br(1) = pif(s, me) + pif(s, mmu) + 8d0 / 3d0 * duv
    br(2) = f1(s, me) + rm1(me)
    br(3) = f1(s, mmu) + rm1(mmu)
    call setdelta(0d0, 0d0)
  end subroutine brackets

  ! Table 2 (c(D) = c0 + c1 D, the overall 4 of N not included) and the integrals of App. H for the direct box at (s, x),
  ! x = t; the crossed box is the direct box at x = u with the opposite sign.  Monomials in the order
  ! 1, d0, d1, d2, d3, d0^2, d1^2, d2^2, d3^2, d0d1, d0d2, d0d3, d1d2, d1d3, d2d3
  subroutine boxtab(s, x, c0, c1, ints)
    double precision, intent(in) :: s, x
    double complex, intent(out) :: c0(15), c1(15), ints(15)
    double precision :: mm, mmm, tau, sig
    double complex :: d0v, cc(0:0, 0:1, 0:1), ccuv(0:0, 0:1, 0:1), ca(0:0, 0:1, 0:1), cb(0:0, 0:1, 0:1), cd(0:0, 0:1, 0:1)
    mm = me**2; mmm = mmu**2; tau = mm + mmm - x; sig = mm + mmm
    c0 = 0; c1 = 0
    c0(1) = 4 * tau * (sig * s - s**2 - s * tau + 2 * tau**2);  c1(1) = 1.5d0 * s**2 * tau
    c0(2) = 4 * tau * (sig + s - tau);                          c1(2) = -s * tau
    c0(3) = 2 * (2 * sig * s - 2 * s**2 - 4 * mmm * tau - 3 * s * tau + 4 * tau**2); c1(3) = s * (3 * s + 2 * tau) / 2
    c0(4) = 2 * (2 * sig * s - 2 * s**2 - 4 * mm * tau - 3 * s * tau + 4 * tau**2);  c1(4) = s * (3 * s + 2 * tau) / 2
    c0(5) = c0(2);                                              c1(5) = c1(2)
    c0(6) = -4 * tau;                                           c1(6) = 1.5d0 * tau
    c0(7) = -2 * s;                                             c1(7) = s
    c0(8) = -2 * s;                                             c1(8) = s
    c0(9) = -4 * tau;                                           c1(9) = 1.5d0 * tau
    c0(10) = 2 * (2 * s + tau);                                 c1(10) = -(3 * s + 2 * tau) / 2
    c0(11) = c0(10);                                            c1(11) = c1(10)
    c0(12) = -4 * (2 * s - tau);                                c1(12) = 3 * s - tau
    c0(13) = -4 * (s + tau);                                    c1(13) = s + 2 * tau
    c0(14) = c0(10);                                            c1(14) = c1(10)
    c0(15) = c0(10);                                            c1(15) = c1(10)
    call D0_cll(d0v, dcmplx(mm), dcmplx(mm), dcmplx(mmm), dcmplx(mmm), dcmplx(s), dcmplx(x), &
        (0d0, 0d0), dcmplx(mm), (0d0, 0d0), dcmplx(mmm))
    ints(1) = d0v
    call C_cll(cc, ccuv, dcmplx(mm), dcmplx(mmm), dcmplx(x), dcmplx(mm), (0d0, 0d0), dcmplx(mmm), 1)  ! d0 removed
    call C_cll(ca, ccuv, dcmplx(mmm), dcmplx(mmm), dcmplx(s), (0d0, 0d0), dcmplx(mmm), (0d0, 0d0), 1) ! d1 removed
    call C_cll(cb, ccuv, dcmplx(mm), dcmplx(mm), dcmplx(s), (0d0, 0d0), dcmplx(mm), (0d0, 0d0), 1)    ! d2 removed
    call C_cll(cd, ccuv, dcmplx(mm), dcmplx(x), dcmplx(mmm), (0d0, 0d0), dcmplx(mm), dcmplx(mmm), 1)  ! d3 removed
    ints(2) = cc(0, 0, 0)
    ints(3) = ca(0, 0, 0)
    ints(4) = cb(0, 0, 0)
    ints(5) = cd(0, 0, 0)
    ints(6) = b0f(mmm, mmm, 0d0) + 2 * mm * cc(0, 0, 0) - (s - 2 * mm) * cc(0, 1, 0) - (mmm - mm - x) * cc(0, 0, 1)
    ints(7) = b0f(mmm, mmm, 0d0) + (mm + mmm - x) * ca(0, 1, 0) + s * ca(0, 0, 1)
    ints(8) = b0f(mm, mm, 0d0) + (mm + mmm - x) * cb(0, 1, 0) + s * cb(0, 0, 1)
    ints(9) = b0f(x, mm, mmm) + s * (cd(0, 0, 0) + cd(0, 1, 0) + cd(0, 0, 1))
    ints(10) = b0f(mmm, mmm, 0d0)
    ints(11) = b0f(mm, mm, 0d0)
    ints(12) = b0f(x, mm, mmm)
    ints(13) = b0f(s, 0d0, 0d0)
    ints(14) = b0f(mmm, 0d0, mmm)
    ints(15) = b0f(mm, 0d0, mm)
  end subroutine boxtab

  double complex function b0f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    call B0_cll(b0f, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
  end function b0f

  double complex function pif(q2, m)
    double precision, intent(in) :: q2, m
    pif = -4d0 / 3d0 * ((1 + 2 * m**2 / q2) * b0f(q2, m**2, m**2) - 2 * m**2 / q2 * b0f(0d0, m**2, m**2) - 1d0 / 3d0)
  end function pif

  ! K F1^Lambda/e^2 (bare, Feynman gauge): UV pole 1 plus the IR pole of C0
  double complex function f1(q2, m)
    double precision, intent(in) :: q2, m
    double complex :: a0, c0v
    double precision :: m2
    m2 = m**2
    call A0_cll(a0, dcmplx(m2, 0d0))
    call C0_cll(c0v, dcmplx(m2, 0d0), dcmplx(q2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0), dcmplx(m2, 0d0), dcmplx(m2, 0d0))
    f1 = (4 * a0 - 4 * m2 + 4 * (2 * m2 - q2) * b0f(m2, m2, 0d0) - (8 * m2 - 3 * q2) * b0f(q2, m2, m2) + 2 * q2 &
          + 2 * (2 * m2 - q2) * (4 * m2 - q2) * c0v) / (4 * m2 - q2)
  end function f1

  double complex function f2(q2, m)
    double precision, intent(in) :: q2, m
    f2 = -4 * m**2 * (b0f(q2, m**2, m**2) - b0f(0d0, m**2, m**2) - 2) / (4 * m**2 - q2)
  end function f2

  ! K (R - 1)/e^2 at xi = 1 before -delta2: B1 + 2 m^2 [B1' + B0'] with the D-dimensional coefficients expanded,
  ! (D-2) B1 -> 2 B1 + 1, (D-2) B1' -> 2 B1' - 2 Res(B1'), D B0' -> 4 B0' - 2 Res(B0')  (oneloop_collier.f90, rres)
  double complex function rm1(m)
    double precision, intent(in) :: m
    double complex :: bb(0:0, 0:1), bbuv(0:0, 0:1), db0, db1, db0p, db1p
    double precision :: m2, duv, dir1, dir2
    m2 = m**2
    call B_cll(bb, bbuv, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0), 1)
    call DB0_cll(db0, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call DB1_cll(db1, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    ! the IR residues of B0', B1' (independent of the current Delta_IR)
    call GetDeltaUV_cll(duv)
    call GetDeltaIR_cll(dir1, dir2)
    call SetDeltaIR_cll(dir1 + 1, dir2)
    call DB0_cll(db0p, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call DB1_cll(db1p, dcmplx(m2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0))
    call SetDeltaIR_cll(dir1, dir2)
    rm1 = 1 + 2 * bb(0, 1) + 2 * m2 * (2 * db1 - 2 * (db1p - db1) + 4 * db0 - 2 * (db0p - db0))
  end function rm1

end program
