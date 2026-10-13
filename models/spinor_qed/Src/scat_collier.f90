! scat_collier.f90 -- the one-loop interference W = sum_spins M0^* M1 of e+ e- -> mu+ mu- from the note's formulas
! (research note models/spinor_qed, step (4), Eqs. (5), (10), (15), App. H) with COLLIER, in CDR, Feynman gauge, at
! e = 1, m_e = mu = 1, m_mu = 1.7 and the points of scat_feyncalc.wl (f).  K W/e^6 per class (K = (4 pi)^2):
!   VP  = [Pi_e(s) + Pi_mu(s) - delta3] B(D),  K Pi_f/e^2 = -(4/3) [(1 + 2m^2/s) B0(s; m^2, m^2) - (2m^2/s) B0(0; m^2, m^2) - 1/3]
!   Le  = [F1^Lambda_e(s) + R_e - 1] B(D) + K F2^e(s) 8 (s + 2 M^2)/s    (F1^Lambda and R - 1 bare, delta1 = delta2)
!   Lmu = the same with m <-> M
!   box = [N(s, t) - N(s, u)]/s,  N = 4 sum_k (c0_k + c1_k D) I_k  (Table 2 and the integrals of App. H)
! F1^Lambda, F2, R - 1 are the PaVe forms of oneloop_collier.f90.  A bracket b(eps) multiplying B(D) = B(4) - 8 eps
! contributes the pole b_pole B(4) and the finite part b_fin B(4) - 8 b_pole; a box term (c0 + c1 D) I contributes
! (c0 + 4 c1) I_fin - 2 c1 I_pole.  The poles of each integral: UV from Delta_UV = 1 minus 0, IR from Delta_IR = 1 minus 0
! (COLLIER's defaults Delta_UV = Delta_IR = 0, mu_UV = mu_IR = 1 give the MS-bar finite parts).
! Writes results/scat_collier.csv (rows class, sqrt(s), cos, s, t, re/im of the UV pole, the IR pole, the finite part).
! Build and run from Src/ (run_scat_check.sh does this):
!   gfortran -I$HOME/hep/include scat_collier.f90 -L$HOME/hep/lib -lcollier -o work/scat_collier
!   (cd work && ./scat_collier ../results/scat_collier.csv)
program scat_collier
  use COLLIER
  implicit none
  double precision, parameter :: me = 1d0, mmu = 1.7d0
  integer, parameter :: npt = 9
  double precision, parameter :: spts(npt) = [16d0, 16d0, 16d0, 36d0, 36d0, 36d0, 100d0, 100d0, 100d0]
  double precision, parameter :: tpts(npt) = [-6d0, -3d0, -1d0, -20d0, -8d0, -1d0, -70d0, -30d0, -5d0]
  character(len=256) :: outfile
  character(len=5), parameter :: names(5) = ['VP   ', 'Le   ', 'Lmu  ', 'box  ', 'total']
  integer :: i, j, w
  double precision :: s, t, u, b4, ee, pe, pm, cth
  double complex :: v00(4), vuv(4), vir(4), uvp(5), irp(5), fin(5)

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'scat_collier.csv'
  call Init_cll(4, 2, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'class,rs,cos,s,t,re_uv,im_uv,re_ir,im_ir,re_fin,im_fin'

  do i = 1, npt
    s = spts(i); t = tpts(i); u = 2 * me**2 + 2 * mmu**2 - s - t
    b4 = 8 / s**2 * ((t - me**2 - mmu**2)**2 + (u - me**2 - mmu**2)**2 + 2 * s * (me**2 + mmu**2))
    ee = sqrt(s) / 2; pe = sqrt(ee**2 - me**2); pm = sqrt(ee**2 - mmu**2)
    cth = (t - me**2 - mmu**2 + 2 * ee**2) / (2 * pe * pm)
    ! the brackets (VP, Le, Lmu) and the box at the three settings; the CDR rational terms are added in classes()
    call classes(s, t, u, 0d0, 0d0, v00)
    call classes(s, t, u, 1d0, 0d0, vuv)
    call classes(s, t, u, 0d0, 1d0, vir)
    uvp(1:4) = vuv - v00
    irp(1:4) = vir - v00
    call cdr(s, t, u, b4, fin(1:4))
    uvp(5) = sum(uvp(1:4)); irp(5) = sum(irp(1:4)); fin(5) = sum(fin(1:4))
    do j = 1, 5
      write(w, '(a,4(",",g0),6(",",es24.16e3))') trim(names(j)), sqrt(s), cth, s, t, dble(uvp(j)), aimag(uvp(j)), &
          dble(irp(j)), aimag(irp(j)), dble(fin(j)), aimag(fin(j))
    end do
    print '(a,f5.1,a,f6.1,a,2es22.13,a,2es22.13)', 'sqrt(s) =', sqrt(s), '  t =', t, ':  K W_total pole', &
        uvp(5) + irp(5), '  finite', fin(5)
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine setdelta(duv, dir)
    double precision, intent(in) :: duv, dir
    call SetDeltaUV_cll(duv)
    call SetDeltaIR_cll(dir, 0d0)
  end subroutine setdelta

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
