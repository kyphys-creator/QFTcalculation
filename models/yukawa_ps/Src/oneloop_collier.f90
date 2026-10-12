! oneloop_collier.f90 -- the brackets of the one-loop 1PI functions of the pseudoscalar Yukawa + phi^4 model
! (research note models/yukawa_ps, Eqs. (6), (7)) from COLLIER, at m = mu = 1, M = 0.7, y = lambda = 1 and the points of
! oneloop_feyncalc.wl.  COLLIER's defaults (Delta_UV = 0, mu^2 = 1) give the MS-bar finite parts.
!   b_phi   = 2 y^2 (p^2 B0(p^2; M^2, M^2) - 2 A0(M^2)) + lambda/2 A0(m^2)
!   b_psi^V = -y^2 B1(p^2; M^2, m^2),   b_psi^S = -y^2 M B0(p^2; M^2, m^2)
!   b_y     = -y^3 (B0(p'^2; M^2, m^2) + k^2 C1),  -y^3 M C0,  0,  y^3 C2   for gamma5, kslash gamma5, pslash gamma5,
!             kslash pslash gamma5, with C_i = C_i(k^2, p'^2, p^2; M^2, M^2, m^2)
!   b_4     = lambda^2/2 sum_x B0(x; m^2, m^2) - 2 y^4 sum_(x,x') F(x, x'),
!   F(x,x') = (2 m^4 - x x') D0(x, x') + 2 [B0(x) + B0(x')] + 2 (x - 2 m^2) C0(m^2, m^2, x) + 2 (x' - 2 m^2) C0(m^2, m^2, x')
!             (internal mass M in F)
! Writes results/oneloop_collier.csv (same rows as results/oneloop_mathematica.csv).  Build and run from Src/
! (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   (cd work && ./oneloop_collier ../results/oneloop_collier.csv)
program oneloop_collier
  use COLLIER
  implicit none
  double precision, parameter :: mphi = 1d0, mpsi = 0.7d0, y = 1d0, lam = 1d0
  double complex, parameter :: m2 = (mphi**2) * (1d0, 0d0), bm2 = (mpsi**2) * (1d0, 0d0)
  double precision, parameter :: phipts(6) = [-5d0, 0d0, 1d0, 2d0, 5d0, 10d0]
  double precision, parameter :: psipts(6) = [-5d0, 0.25d0, 0.49d0, 1d0, 4d0, 10d0]
  ! (p^2, k^2, p'^2)
  double precision, parameter :: ypts(3,6) = reshape([0.49d0,1d0,0.49d0, 0.49d0,-2d0,0.49d0, 0.49d0,5d0,0.49d0, &
                                                     -1d0,-2d0,-3d0, 1d0,0.5d0,4d0, 0.3d0,0d0,2d0], [3,6])
  double precision, parameter :: rs(3) = [2.5d0, 5d0, 10d0], cs(2) = [0.3d0, 0.9d0]
  double complex :: a0m, a0bm, bb(0:0,0:1), bbuv(0:0,0:1), cc(0:0,0:1,0:1), ccuv(0:0,0:1,0:1)
  double complex :: b0, res, inv(3), fsum, bsum
  double precision :: s, t, u, p2, pp, kk, ppr
  character(len=256) :: outfile
  integer :: i, j, w

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop_collier.csv'
  call Init_cll(4, 1, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'func,arg1,arg2,arg3,re_collier,im_collier'
  call A0_cll(a0m, m2)
  call A0_cll(a0bm, bm2)

  do i = 1, size(phipts)
    call B0_cll(b0, dcmplx(phipts(i), 0d0), bm2, bm2)
    res = 2 * y**2 * (phipts(i) * b0 - 2 * a0bm) + lam / 2 * a0m
    call row('Vphi', phipts(i), 0d0, 0d0, res)
  end do

  do i = 1, size(psipts)
    call B_cll(bb, bbuv, dcmplx(psipts(i), 0d0), bm2, m2, 1)
    call row('Vpsi_V', psipts(i), 0d0, 0d0, -y**2 * bb(0,1))
    call row('Vpsi_S', psipts(i), 0d0, 0d0, -y**2 * mpsi * bb(0,0))
  end do

  do i = 1, size(ypts, 2)
    pp = ypts(1, i); kk = ypts(2, i); ppr = ypts(3, i)
    ! C_cll(C, Cuv, p10, p21, p20, m02, m12, m22, rmax): p1 = k, p2 = -p, so p10 = k^2, p21 = p'^2, p20 = p^2
    call C_cll(cc, ccuv, dcmplx(kk, 0d0), dcmplx(ppr, 0d0), dcmplx(pp, 0d0), bm2, bm2, m2, 1)
    call B0_cll(b0, dcmplx(ppr, 0d0), bm2, m2)
    call row('Vy_1', pp, kk, ppr, -y**3 * (b0 + kk * cc(0,1,0)))
    call row('Vy_k', pp, kk, ppr, -y**3 * mpsi * cc(0,0,0))
    call row('Vy_p', pp, kk, ppr, (0d0, 0d0))
    call row('Vy_kp', pp, kk, ppr, y**3 * cc(0,0,1))
  end do

  do i = 1, size(rs)
    do j = 1, size(cs)
      s = rs(i)**2
      p2 = s / 4 - mphi**2
      t = -2 * p2 * (1 - cs(j))
      u = -2 * p2 * (1 + cs(j))
      inv = [dcmplx(s, 0d0), dcmplx(t, 0d0), dcmplx(u, 0d0)]
      bsum = bphi(inv(1)) + bphi(inv(2)) + bphi(inv(3))
      fsum = fbox(inv(1), inv(2)) + fbox(inv(2), inv(3)) + fbox(inv(3), inv(1))
      res = lam**2 / 2 * bsum - 2 * y**4 * fsum
      call row('V4', s, t, 0d0, res)
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine row(name, x1, x2, x3, val)
    character(len=*), intent(in) :: name
    double precision, intent(in) :: x1, x2, x3
    double complex, intent(in) :: val
    write(w, '(a,3(",",g0),2(",",es24.16e3))') name, x1, x2, x3, dble(val), aimag(val)
  end subroutine row

  double complex function bphi(x)
    double complex, intent(in) :: x
    call B0_cll(bphi, x, m2, m2)
  end function bphi

  double complex function fbox(x, xp)
    ! F(x, x') of Eq. (7): on-shell external phi (mass m), internal fermion mass M
    double complex, intent(in) :: x, xp
    double complex :: d0, c0x, c0xp, b0x, b0xp
    ! D0_cll(D0, p10, p21, p32, p30, p20, p31, m02, m12, m22, m32): p20, p31 are the two channel invariants
    call D0_cll(d0, m2, m2, m2, m2, x, xp, bm2, bm2, bm2, bm2)
    call C0_cll(c0x, m2, m2, x, bm2, bm2, bm2)
    call C0_cll(c0xp, m2, m2, xp, bm2, bm2, bm2)
    call B0_cll(b0x, x, bm2, bm2)
    call B0_cll(b0xp, xp, bm2, bm2)
    fbox = (2 * m2**2 - x * xp) * d0 + 2 * (b0x + b0xp) + 2 * (x - 2 * m2) * c0x + 2 * (xp - 2 * m2) * c0xp
  end function fbox

end program
