! rg_collier.f90 -- the mu-dependence of the renormalized one-loop two-point functions of QCD with COLLIER (research note
! models/qcd, step (6)).  g = 1, m = 1, C_A = 3, C_F = 4/3, T_F = 1/2, MS-bar at the scale mu (mu_UV = mu_IR = mu, SetMuUV2_cll,
! SetMuIR2_cll; Delta_UV = Delta_IR = 0).  The brackets (K/g^2 times the note's quantities, Eq. (8)) are those of
! oneloop_collier.f90, at the points of rg_feyncalc.wl (c), for mu = 1/2, 1, 2:
!   PiYM, Ghost (xi = 0, 1, 3), PiQ0 (one massless flavour), PiT (the t loop), SigV_t, SigS_t, SigV_u;
!   Mpole = SigV_t + SigS_t at p^2 = m^2 (the pole mass, Eq. (11));  R_Q = K (R_t - 1) before -delta2 (finite part; the pole
!   column is UV + IR pole minus the expected -3 C_F);  PiT0 = K Pi_t(0) = -(4/3) T_F B0(0; m^2, m^2) (the t part of R_G);
!   PiTsub = K [Pi_t(k^2) - Pi_t(0)] (decoupling: -(4/3) T_F [k^2/(5 m^2) + ...], no mu).
! Writes rows "func,arg,xi,mu,re_pole,im_pole,re_fin,im_fin" to the file given as the first argument.
! Build and run from Src/ (run_rg_check.sh does this):
!   gfortran -I$HOME/hep/include rg_collier.f90 -L$HOME/hep/lib -lcollier -o work/rg_collier
!   (cd work && ./rg_collier ../results/rg_collier_onepi.csv)
program rg_collier
  use COLLIER
  implicit none
  double precision, parameter :: m = 1d0, ca = 3d0, cf = 4d0 / 3d0, tf = 0.5d0
  double precision, parameter :: mus(3) = [0.5d0, 1d0, 2d0]
  double precision, parameter :: gpts(6) = [-5d0, -1d0, 0.5d0, 2d0, 6d0, 20d0]
  double precision, parameter :: qpts(7) = [-5d0, -1d0, 0.5d0, 2d0, 3.9d0, 6d0, 20d0]
  double precision, parameter :: spts(5) = [-5d0, 0.5d0, 2d0, 4d0, 10d0], upts(3) = [-5d0, 0.5d0, 2d0]
  double precision, parameter :: dpts(8) = [-1d0, -0.1d0, -0.01d0, -0.001d0, 0.001d0, 0.01d0, 0.1d0, 1d0]
  double precision, parameter :: xis(3) = [0d0, 1d0, 3d0]
  character(len=256) :: outfile
  integer :: i, j, k, w
  double precision :: eta, xi
  double complex :: fin, ir

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'rg_collier_onepi.csv'
  call Init_cll(2, 1, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'func,arg,xi,mu,re_pole,im_pole,re_fin,im_fin'

  do k = 1, size(mus)
    call SetMuUV2_cll(mus(k)**2)
    call SetMuIR2_cll(mus(k)**2)
    do i = 1, size(gpts)
      do j = 1, size(xis)
        xi = xis(j)
        eta = 1d0 - xi
        call row('PiYM', gpts(i), xi, mus(k), (0d0, 0d0), ca * ((5d0 / 3d0 + eta / 2) * b0f(gpts(i), 0d0, 0d0) + 1d0 / 9d0 &
                 - 2 * eta + eta**2 / 4))
        call row('Ghost', gpts(i), xi, mus(k), (0d0, 0d0), -ca * ((3d0 - xi) / 4 * b0f(gpts(i), 0d0, 0d0) - (1d0 - xi) / 2))
      end do
      call row('PiQ0', gpts(i), 0d0, mus(k), (0d0, 0d0), -4d0 / 3d0 * tf * (b0f(gpts(i), 0d0, 0d0) - 1d0 / 3d0))
    end do
    do i = 1, size(qpts)
      call row('PiT', qpts(i), 0d0, mus(k), (0d0, 0d0), pit(qpts(i)))
    end do
    do i = 1, size(spts)
      do j = 1, size(xis)
        call row('SigV_t', spts(i), xis(j), mus(k), (0d0, 0d0), xis(j) * cf * (1 + 2 * b1f(spts(i), m**2, 0d0)))
        call row('SigS_t', spts(i), xis(j), mus(k), (0d0, 0d0), cf * ((3 + xis(j)) * b0f(spts(i), m**2, 0d0) - 2))
      end do
    end do
    do i = 1, size(upts)
      do j = 1, size(xis)
        call row('SigV_u', upts(i), xis(j), mus(k), (0d0, 0d0), xis(j) * cf * (1 + 2 * b1f(upts(i), 0d0, 0d0)))
      end do
    end do
    do j = 1, size(xis)
      xi = xis(j)
      call row('Mpole', m, xi, mus(k), (0d0, 0d0), xi * cf * (1 + 2 * b1f(m**2, m**2, 0d0)) + cf * ((3 + xi) * b0f(m**2, m**2, 0d0) - 2))
      call rres(xi, fin, ir)
      call row('R_Q', m, xi, mus(k), cf * (ir - xi) + 3 * cf, cf * fin)
    end do
    call row('PiT0', 0d0, 0d0, mus(k), (0d0, 0d0), pit0())
    do i = 1, size(dpts)
      call row('PiTsub', dpts(i), 0d0, mus(k), (0d0, 0d0), pit(dpts(i)) - pit0())
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)

contains

  subroutine row(name, x1, x2, x3, pl, val)
    character(len=*), intent(in) :: name
    double precision, intent(in) :: x1, x2, x3
    double complex, intent(in) :: pl, val
    write(w, '(a,3(",",g0),4(",",es24.16e3))') name, x1, x2, x3, dble(pl), aimag(pl), dble(val), aimag(val)
  end subroutine row

  double complex function pit(q2)
    double precision, intent(in) :: q2
    pit = -4d0 / 3d0 * tf * ((1 + 2 * m**2 / q2) * b0f(q2, m**2, m**2) - 2 * m**2 / q2 * b0f(0d0, m**2, m**2) - 1d0 / 3d0)
  end function pit

  double complex function pit0()
    pit0 = -4d0 / 3d0 * tf * b0f(0d0, m**2, m**2)
  end function pit0

  subroutine rres(xi, fin, ir)
    ! K (R_t - 1)/(g^2 C_F) at p^2 = m^2 before -delta2: MS-bar finite part and IR pole coefficient (the UV pole is -xi);
    ! (D - 2) and (D - 1 + xi) multiply B1 (UV pole -1/2) and the IR poles of DB0, DB1 (spinor QED note, rg_collier.f90)
    double precision, intent(in) :: xi
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

  double complex function b0f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    call B0_cll(b0f, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
  end function b0f

  double complex function b1f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    double complex :: bb(0:0, 0:1), bbuv(0:0, 0:1)
    call B_cll(bb, bbuv, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0), 1)
    b1f = bb(0, 1)
  end function b1f

end program rg_collier
