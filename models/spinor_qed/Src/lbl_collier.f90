! lbl_collier.f90 -- photon-photon scattering at one loop with COLLIER tensor integrals and explicit Dirac matrices for
! step (10) (research note models/spinor_qed, Eqs. (eq:lblamp)-(eq:lbllow), App. lbl).  Independent of FeynCalc: the
! fermion trace is built numerically from 4x4 Dirac matrices with a four-dimensional loop momentum in the numerator, the
! loop integrals are COLLIER's tensor components (D-dimensional integrals, four-dimensional indices), and the rational
! term the four-dimensional numerator misses is added as the R2 vertex derived in App. ren,
!   X_R2 = (4/3) (e1.e2 e3*.e4* + e1.e3* e2.e4* + e1.e4* e2.e3*)  per flavour.
! Kinematics (all tools of step (10) use the same): gamma(k1, l1) gamma(k2, l2) -> gamma(k3, l3) gamma(k4, l4) in the
! centre-of-mass frame, k1 along +z, k3 at polar angle theta in the xz plane (phi = 0), k4 = -k3 in space; the photon
! with direction (theta, phi) and helicity l has eps_l = (-l e_theta - i e_phi)/sqrt(2), outgoing photons eps_l^*.
! Output: X = M/alpha^2 (M from iM = the sum of the diagrams) for the electron loop (m = 1) and the muon loop (m = 1.7),
! each with its R2 part, for the 16 helicity configurations in MadGraph's order (l1 slowest, -1 before +1).
! Each of the 6 orderings of the photons around the loop is computed; the two orientations of the same cyclic order
! (charge conjugates) must agree, and the largest relative difference is written as cdiff.
! Reads "s cos nf" per line from the first argument (nf = 1: the electron loop only, the muon columns are 0; nf = 2: both),
! writes CSV to the second.  Build and run from Src/:
!   gfortran -O2 -I$HOME/hep/include lbl_collier.f90 -L$HOME/hep/lib -lcollier -o work/lbl_collier
!   work/lbl_collier work/lbl_points.txt work/lbl_collier.csv   (lbl_numeric.py runs it)
program lbl_collier
  use COLLIER
  implicit none
  character(len=256) :: f1n, f2n
  integer :: ui, uo, ios, h, i, j, f, io, nf
  double precision :: s, c, w, sn, mf(2)
  double precision :: lam(4)
  double complex :: gam(4,4,0:3), glow(4,4,0:3), one4(4,4)
  double complex :: kv(0:3,4), qv(0:3,4), ev(0:3,4)
  double complex :: xf(2), xr2, ordv(6)
  double precision :: cdiff, pi
  integer :: perms(3,6)
  ! the six orderings (1, b, c, d); (1, b, c, d) and (1, d, c, b) are charge conjugates
  data perms /2,3,4, 4,3,2, 3,4,2, 2,4,3, 4,2,3, 3,2,4/

  pi = acos(-1d0)
  mf = (/ 1d0, 1.7d0 /)
  call get_command_argument(1, f1n); call get_command_argument(2, f2n)
  call Init_cll(4, 4, '')
  call dirac_matrices(gam, glow, one4)
  open(newunit=ui, file=trim(f1n), status='old', action='read')
  open(newunit=uo, file=trim(f2n), status='replace', action='write')
  write(uo, '(a)') 's,cos,h,l1,l2,l3,l4,re_e,im_e,re_mu,im_mu,re_r2,im_r2,cdiff'
  do
    read(ui, *, iostat=ios) s, c, nf
    if (ios /= 0) exit
    w = sqrt(s)/2; sn = sqrt(max(0d0, 1d0 - c*c))
    kv(:,1) = (/ w, 0d0, 0d0, w /)
    kv(:,2) = (/ w, 0d0, 0d0, -w /)
    kv(:,3) = (/ w, w*sn, 0d0, w*c /)
    kv(:,4) = (/ w, -w*sn, 0d0, -w*c /)
    ! all-incoming momenta
    qv(:,1) = kv(:,1); qv(:,2) = kv(:,2); qv(:,3) = -kv(:,3); qv(:,4) = -kv(:,4)
    do h = 1, 16
      do i = 1, 4
        lam(i) = merge(1d0, -1d0, btest(h-1, 4-i))
      end do
      ev(:,1) = polvec(1d0, 0d0, 0d0, lam(1))       ! theta = 0
      ev(:,2) = polvec(-1d0, 0d0, 0d0, lam(2))       ! theta = pi, phi = 0
      ev(:,3) = conjg(polvec(c, sn, 0d0, lam(3)))
      ev(:,4) = conjg(polvec(-c, sn, 1d0, lam(4)))   ! theta = pi - theta, phi = pi
      xr2 = 4d0/3d0*(mdot(ev(:,1),ev(:,2))*mdot(ev(:,3),ev(:,4)) + mdot(ev(:,1),ev(:,3))*mdot(ev(:,2),ev(:,4)) &
            + mdot(ev(:,1),ev(:,4))*mdot(ev(:,2),ev(:,3)))
      cdiff = 0d0
      xf = (0d0, 0d0)
      do f = 1, nf
        do io = 1, 6
          ordv(io) = ordering(1, perms(1,io), perms(2,io), perms(3,io), mf(f))
        end do
        do io = 1, 6, 2
          cdiff = max(cdiff, abs(ordv(io) - ordv(io+1))/max(abs(ordv(io)), 1d-300))
        end do
        xf(f) = sum(ordv) + xr2
      end do
      write(uo, '(es25.17e3,",",es25.17e3,",",i3,4(",",i3),7(",",es25.17e3))') s, c, h, (nint(lam(j)), j=1,4), &
        dble(xf(1)), aimag(xf(1)), dble(xf(2)), aimag(xf(2)), dble(xr2), aimag(xr2), cdiff
    end do
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(f2n)

contains

  ! eps_l for the direction with cos(theta) = ct, sin(theta) = st and phi = 0 (cp = 0) or pi (cp = 1)
  function polvec(ct, st, cp, l) result(e)
    double precision, intent(in) :: ct, st, cp, l
    double complex :: e(0:3)
    double precision :: cph, eth(3), eph(3)
    cph = merge(-1d0, 1d0, cp > 0.5d0)
    eth = (/ ct*cph, 0d0, -st /)
    eph = (/ 0d0, cph, 0d0 /)
    e(0) = (0d0, 0d0)
    e(1:3) = (-l*eth - (0d0, 1d0)*eph)/sqrt(2d0)
  end function

  double complex function mdot(a, b)
    double complex, intent(in) :: a(0:3), b(0:3)
    mdot = a(0)*b(0) - a(1)*b(1) - a(2)*b(2) - a(3)*b(3)
  end function

  function slash(v) result(m)
    double complex, intent(in) :: v(0:3)
    double complex :: m(4,4)
    integer :: mu
    m = (0d0, 0d0)
    do mu = 0, 3
      m = m + glow(:,:,mu)*v(mu)
    end do
  end function

  double complex function trace(m)
    double complex, intent(in) :: m(4,4)
    integer :: k
    trace = (0d0, 0d0)
    do k = 1, 4
      trace = trace + m(k,k)
    end do
  end function

  ! X of one ordering: the photons a, b, c, d attached in this order along the Dirac chain of the trace
  !   -tr[e_a S(l) e_b S(l - q_b) e_c S(l - q_b - q_c) e_d S(l + q_a)],  S(p) = (pslash + m)/(p^2 - m^2),
  ! X = M/alpha^2 = -(sum of C_{mu...} T^{mu...}) with COLLIER's T = (1/(i pi^2)) int d^Dl (...) (iM = -e^4 int/(2 pi)^D).
  double complex function ordering(a, b, cc, d, m)
    integer, intent(in) :: a, b, cc, d
    double precision, intent(in) :: m
    double complex :: mom(0:3,3), inv(6), m2(0:3)
    double complex :: td(0:4,0:4,0:4,0:4), tduv(0:4,0:4,0:4,0:4)
    double complex :: amat(4,4,4), ea(4,4), eb(4,4), ec(4,4), ed(4,4), prod(4,4), xm(4,4,4)
    integer :: sub, r, nt, t, k, idx(4), cnt(0:3), pos(4), mu
    double complex :: acc
    mom(:,1) = -qv(:,b)
    mom(:,2) = -qv(:,b) - qv(:,cc)
    mom(:,3) = qv(:,a)
    inv(1) = mdot(mom(:,1), mom(:,1))
    inv(2) = mdot(mom(:,2)-mom(:,1), mom(:,2)-mom(:,1))
    inv(3) = mdot(mom(:,3)-mom(:,2), mom(:,3)-mom(:,2))
    inv(4) = mdot(mom(:,3), mom(:,3))
    inv(5) = mdot(mom(:,2), mom(:,2))
    inv(6) = mdot(mom(:,3)-mom(:,1), mom(:,3)-mom(:,1))
    ! the external photons are massless: invariants that vanish exactly must be passed as 0 (rounding gives ~1e-16 s)
    do k = 1, 6
      inv(k) = dcmplx(merge(0d0, dble(inv(k)), abs(dble(inv(k))) < 1d-10*(abs(inv(5))+abs(inv(6)))), 0d0)
    end do
    m2 = dcmplx(m*m, 0d0)
    call Dten_cll(td, tduv, mom, inv, m2, 4)
    ! shifts of the four propagators: 0, -q_b, -q_b - q_c, +q_a
    amat(:,:,1) = m*one4
    amat(:,:,2) = slash(mom(:,1)) + m*one4
    amat(:,:,3) = slash(mom(:,2)) + m*one4
    amat(:,:,4) = slash(mom(:,3)) + m*one4
    ea = slash(ev(:,a)); eb = slash(ev(:,b)); ec = slash(ev(:,cc)); ed = slash(ev(:,d))
    acc = (0d0, 0d0)
    do sub = 0, 15                      ! propagators that contribute lslash
      r = 0
      do k = 1, 4
        if (btest(sub, k-1)) then
          r = r + 1; pos(r) = k
        end if
      end do
      nt = 4**r
      do t = 0, nt - 1                  ! ordered tuples of Lorentz indices
        cnt = 0
        do k = 1, r
          idx(k) = mod(t/4**(k-1), 4)
          cnt(idx(k)) = cnt(idx(k)) + 1
        end do
        xm = amat
        do k = 1, r
          xm(:,:,pos(k)) = glow(:,:,idx(k))
        end do
        prod = matmul(ea, matmul(xm(:,:,1), matmul(eb, matmul(xm(:,:,2), matmul(ec, matmul(xm(:,:,3), &
               matmul(ed, xm(:,:,4))))))))
        acc = acc + trace(prod)*td(cnt(0), cnt(1), cnt(2), cnt(3))
      end do
    end do
    ordering = -acc
  end function

  ! Dirac representation; glow(mu) = gamma_mu = g_{mu mu} gamma^mu, so that vslash = sum_mu glow(mu) v^mu
  subroutine dirac_matrices(g, gl, id)
    double complex, intent(out) :: g(4,4,0:3), gl(4,4,0:3), id(4,4)
    double complex :: sig(2,2,3), z
    integer :: k
    z = (0d0, 0d0)
    id = z
    do k = 1, 4
      id(k,k) = (1d0, 0d0)
    end do
    sig(:,:,1) = reshape((/ z, (1d0,0d0), (1d0,0d0), z /), (/2,2/))
    sig(:,:,2) = reshape((/ z, (0d0,1d0), (0d0,-1d0), z /), (/2,2/))
    sig(:,:,3) = reshape((/ (1d0,0d0), z, z, (-1d0,0d0) /), (/2,2/))
    g = z
    g(1,1,0) = 1; g(2,2,0) = 1; g(3,3,0) = -1; g(4,4,0) = -1
    do k = 1, 3
      g(1:2,3:4,k) = sig(:,:,k)
      g(3:4,1:2,k) = -sig(:,:,k)
    end do
    gl(:,:,0) = g(:,:,0)
    do k = 1, 3
      gl(:,:,k) = -g(:,:,k)
    end do
  end subroutine

end program
