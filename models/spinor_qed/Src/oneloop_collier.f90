! oneloop_collier.f90 -- the brackets of the one-loop 1PI functions of spinor QED (research note models/spinor_qed,
! Eqs. (5), (7), (10)) from COLLIER, at e = 1, m_e = mu = 1, m_mu = 1.7 and the points of oneloop_feyncalc.wl.
! All brackets are K/e^2 times the note's quantity (K = (4 pi)^2); COLLIER's defaults (Delta_UV = Delta_IR = 0,
! mu_UV^2 = mu_IR^2 = 1) give the MS-bar finite parts; the IR pole coefficient is the change under Delta_IR -> 1.
!   Pi_f   = -(4/3) [(1 + 2 m^2/q^2) B0(q^2; m^2, m^2) - (2 m^2/q^2) B0(0; m^2, m^2) - 1/3]
!   SigV   = xi (1 + 2 B1(p^2; m^2, 0)),   SigS = (3 + xi) B0(p^2; m^2, 0) - 2
!   F1     = [4 A0 - 4 m^2 + 4 (2m^2 - q^2) B0(m^2; m^2, 0) - (8 m^2 - 3 q^2) B0(q^2; m^2, m^2) + 2 q^2
!             + 2 (2 m^2 - q^2)(4 m^2 - q^2) C0(m^2, q^2, m^2; 0, m^2, m^2)]/(4 m^2 - q^2)      (F1^Lambda, total pole 1 + IR)
!   F2     = -4 m^2 [B0(q^2; m^2, m^2) - B0(0; m^2, m^2) - 2]/(4 m^2 - q^2)
!   R - 1  = xi (1 + 2 B1(m^2; m^2, 0)) + 2 m^2 [xi (D-2) B1' + (D-1+xi) B0'] at p^2 = m^2, expanded in D = 4 - 2 eps:
!            (D-2) B1' -> 2 B1' - 2 Res(B1'),  (D-1+xi) B0' -> (3+xi) B0' - 2 Res(B0')  (Res = IR pole coefficient), App. F
! Writes results/oneloop_collier.csv (rows func, arg, xi, re/im of the pole and of the finite part).  Build and run from
! Src/ (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   (cd work && ./oneloop_collier ../results/oneloop_collier.csv)
program oneloop_collier
  use COLLIER
  implicit none
  double precision, parameter :: me = 1d0, mmu = 1.7d0
  double precision, parameter :: pipts(7) = [-5d0, -1d0, 0.5d0, 2d0, 3.9d0, 6d0, 20d0]
  double precision, parameter :: sigpts(5) = [-5d0, 0.5d0, 2d0, 4d0, 10d0], xis(3) = [0d0, 1d0, 3d0]
  double precision, parameter :: vpts(8) = [-5d0, -1d0, 0.5d0, 2d0, 3.9d0, 6d0, 10d0, 0d0]
  character(len=256) :: outfile
  integer :: i, j, w
  double complex :: fin, ir

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop_collier.csv'
  call Init_cll(3, 1, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'func,arg,xi,re_pole,im_pole,re_fin,im_fin'

  do i = 1, size(pipts)
    call row('Pi_e', pipts(i), 0d0, (0d0, 0d0), pif(pipts(i), me))
    call row('Pi_mu', pipts(i), 0d0, (0d0, 0d0), pif(pipts(i), mmu))
  end do
  do i = 1, size(sigpts)
    do j = 1, size(xis)
      call row('SigV_e', sigpts(i), xis(j), (0d0, 0d0), sigv(sigpts(i), me, xis(j)))
      call row('SigS_e', sigpts(i), xis(j), (0d0, 0d0), sigs(sigpts(i), me, xis(j)))
      call row('SigV_mu', sigpts(i), xis(j), (0d0, 0d0), sigv(sigpts(i), mmu, xis(j)))
      call row('SigS_mu', sigpts(i), xis(j), (0d0, 0d0), sigs(sigpts(i), mmu, xis(j)))
    end do
  end do
  do i = 1, size(vpts)
    call f1(vpts(i), me, fin, ir)
    call row('F1', vpts(i), 0d0, 1d0 + ir, fin)
    call row('F2', vpts(i), 0d0, (0d0, 0d0), f2(vpts(i), me))
  end do
  do j = 1, size(xis)
    call rres(me, xis(j), fin, ir)
    call row('R_e', me, xis(j), ir, fin)
    call rres(mmu, xis(j), fin, ir)
    call row('R_mu', mmu, xis(j), ir, fin)
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine row(name, x1, x2, pole, val)
    character(len=*), intent(in) :: name
    double precision, intent(in) :: x1, x2
    double complex, intent(in) :: pole, val
    write(w, '(a,2(",",g0),4(",",es24.16e3))') name, x1, x2, dble(pole), aimag(pole), dble(val), aimag(val)
  end subroutine row

  double complex function b0f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    call B0_cll(b0f, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
  end function b0f

  double complex function pif(q2, m)
    double precision, intent(in) :: q2, m
    pif = -4d0 / 3d0 * ((1 + 2 * m**2 / q2) * b0f(q2, m**2, m**2) - 2 * m**2 / q2 * b0f(0d0, m**2, m**2) - 1d0 / 3d0)
  end function pif

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

  subroutine f1(q2, m, fin, ir)
    ! F1^Lambda: finite part (Delta_UV = Delta_IR = 0) and the IR pole coefficient (C0 only)
    double precision, intent(in) :: q2, m
    double complex, intent(out) :: fin, ir
    double complex :: a0, c0a, c0b, num
    double precision :: m2
    m2 = m**2
    call A0_cll(a0, dcmplx(m2, 0d0))
    call SetDeltaIR_cll(0d0, 0d0)
    call C0_cll(c0a, dcmplx(m2, 0d0), dcmplx(q2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0), dcmplx(m2, 0d0), dcmplx(m2, 0d0))
    call SetDeltaIR_cll(1d0, 0d0)
    call C0_cll(c0b, dcmplx(m2, 0d0), dcmplx(q2, 0d0), dcmplx(m2, 0d0), (0d0, 0d0), dcmplx(m2, 0d0), dcmplx(m2, 0d0))
    call SetDeltaIR_cll(0d0, 0d0)
    num = 4 * a0 - 4 * m2 + 4 * (2 * m2 - q2) * b0f(m2, m2, 0d0) - (8 * m2 - 3 * q2) * b0f(q2, m2, m2) + 2 * q2 &
          + 2 * (2 * m2 - q2) * (4 * m2 - q2) * c0a
    fin = num / (4 * m2 - q2)
    ir = 2 * (2 * m2 - q2) * (c0b - c0a)
  end subroutine f1

  double complex function f2(q2, m)
    double precision, intent(in) :: q2, m
    if (q2 == 0d0) then
      f2 = 2d0
    else
      f2 = -4 * m**2 * (b0f(q2, m**2, m**2) - b0f(0d0, m**2, m**2) - 2) / (4 * m**2 - q2)
    end if
  end function f2

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

end program
