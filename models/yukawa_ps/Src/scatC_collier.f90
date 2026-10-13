! scatC_collier.f90 -- loop integrals of the one-loop psi(p1) psibar(p2) -> psi(p3) psibar(p4) amplitude of the pseudoscalar
! Yukawa + phi^4 model (research note models/yukawa_ps, step (12), Eq. (MC1), App. scatC), MS-bar finite parts (Delta_UV = 0,
! mu^2 set with SetMuUV2_cll), m = 1, M = 0.7 (the pole masses, used also in the loops).
! Reads lines "sqrts costheta mu" from the file given as the first argument and writes to the second, per line:
!   sqrts, costheta, mu, s, t, u and, as real and imaginary parts,
!   b0s, b0t, b0m:  B0(x; M^2, M^2) at x = s, t, m^2 (phi self-energy);  b0v: B0(M^2; M^2, m^2)
!   vertex in the routing of the hand formula (denominators D_phi(l) D_psi(l - p) D_psi(l - p'), p^2 = p'^2 = M^2,
!     (p - p')^2 = x):  C(M^2, x, M^2; m^2, M^2, M^2), offsets k1 = -p, k2 = -p':  v{s,t}_{c0,c1,c2,c00,c11,c12,c22}
!   vertex in the convention of the note's V_y (Eq. (VR)):  C(x, M^2, M^2; M^2, M^2, m^2):  n{s,t}_{c0,c1,c2}
!   boxes (rank 2, numerator l^mu l^nu), offsets (k1, k2, k3), masses (m, M, m, M):
!     td: (-p1, p3 - p1, p2), D(M^2, M^2, M^2, M^2, t, s)      tx: (-p1, p3 - p1, -p4), D(M^2, M^2, M^2, M^2, t, u)
!     sd: (-p1, -p1 - p2, -p3), D(M^2, M^2, M^2, M^2, s, t)    sx: (-p1, -p1 - p2, -p4), D(M^2, M^2, M^2, M^2, s, u)
!     {td,tx,sd,sx}_{d00,d11,d12,d13,d22,d23,d33}
! Build and run from Src/ (run_scatC_check.sh builds it, scatC_numeric.py runs it):
!   gfortran -I$HOME/hep/include scatC_collier.f90 -L$HOME/hep/lib -lcollier -o work/scatC_collier
program scatC_collier
  use COLLIER
  implicit none
  double precision, parameter :: mphi = 1d0, mpsi = 0.7d0
  double complex, parameter :: m2 = (mphi**2) * (1d0, 0d0), bm2 = (mpsi**2) * (1d0, 0d0)
  double precision :: rs, ct, mu, s, t, u, p2
  double complex :: vals(52)
  character(len=256) :: f1, f2
  character(len=4096) :: head
  character(len=16) :: names(52)
  integer :: ui, uo, ios, i, n

  call get_command_argument(1, f1); call get_command_argument(2, f2)
  call Init_cll(4, 2, '')
  n = 0
  call addn('b0s'); call addn('b0t'); call addn('b0m'); call addn('b0v')
  call addv('vs'); call addv('vt')
  call addc('ns'); call addc('nt')
  call addd('td'); call addd('tx'); call addd('sd'); call addd('sx')
  head = 'sqrts,costheta,mu,s,t,u'
  do i = 1, n
    head = trim(head) // ',re_' // trim(names(i)) // ',im_' // trim(names(i))
  end do
  open(newunit=ui, file=trim(f1), status='old', action='read')
  open(newunit=uo, file=trim(f2), status='replace', action='write')
  write(uo, '(a)') trim(head)
  do
    read(ui, *, iostat=ios) rs, ct, mu
    if (ios /= 0) exit
    call SetMuUV2_cll(mu**2)
    s = rs**2; p2 = s / 4 - mpsi**2
    t = -2 * p2 * (1 - ct); u = -2 * p2 * (1 + ct)
    call B0_cll(vals(1), dcmplx(s, 0d0), bm2, bm2)
    call B0_cll(vals(2), dcmplx(t, 0d0), bm2, bm2)
    call B0_cll(vals(3), m2, bm2, bm2)
    call B0_cll(vals(4), bm2, bm2, m2)
    call vert(s, vals(5:11)); call vert(t, vals(12:18))
    call vnote(s, vals(19:21)); call vnote(t, vals(22:24))
    call box(t, s, vals(25:31)); call box(t, u, vals(32:38))
    call box(s, t, vals(39:45)); call box(s, u, vals(46:52))
    write(uo, '(6(es24.16e3,","),103(es24.16e3,","),es24.16e3)') rs, ct, mu, s, t, u, (dble(vals(i)), aimag(vals(i)), i = 1, n)
  end do
  close(ui); close(uo)

contains

  subroutine addn(a)
    character(len=*), intent(in) :: a
    n = n + 1; names(n) = a
  end subroutine addn

  subroutine addv(a)
    character(len=*), intent(in) :: a
    call addn(a // '_c0'); call addn(a // '_c1'); call addn(a // '_c2'); call addn(a // '_c00')
    call addn(a // '_c11'); call addn(a // '_c12'); call addn(a // '_c22')
  end subroutine addv

  subroutine addc(a)
    character(len=*), intent(in) :: a
    call addn(a // '_c0'); call addn(a // '_c1'); call addn(a // '_c2')
  end subroutine addc

  subroutine addd(a)
    character(len=*), intent(in) :: a
    call addn(a // '_d00'); call addn(a // '_d11'); call addn(a // '_d12'); call addn(a // '_d13')
    call addn(a // '_d22'); call addn(a // '_d23'); call addn(a // '_d33')
  end subroutine addd

  subroutine vert(x, v)
    ! C(p10 = M^2, p21 = x, p20 = M^2; m^2, M^2, M^2), rank 2
    double precision, intent(in) :: x
    double complex, intent(out) :: v(7)
    double complex :: c(0:1,0:2,0:2), cuv(0:1,0:2,0:2)
    call C_cll(c, cuv, bm2, dcmplx(x, 0d0), bm2, m2, bm2, bm2, 2)
    v = [c(0,0,0), c(0,1,0), c(0,0,1), c(1,0,0), c(0,2,0), c(0,1,1), c(0,0,2)]
  end subroutine vert

  subroutine vnote(x, v)
    ! C_i(x, M^2, M^2; M^2, M^2, m^2) of the note (LoopTools argument order)
    double precision, intent(in) :: x
    double complex, intent(out) :: v(3)
    double complex :: c(0:0,0:1,0:1), cuv(0:0,0:1,0:1)
    call C_cll(c, cuv, dcmplx(x, 0d0), bm2, bm2, bm2, bm2, m2, 1)
    v = [c(0,0,0), c(0,1,0), c(0,0,1)]
  end subroutine vnote

  subroutine box(x20, x31, v)
    ! D(p10, p21, p32, p30, p20, p31; m^2, M^2, m^2, M^2) with all external masses M^2, rank 2
    double precision, intent(in) :: x20, x31
    double complex, intent(out) :: v(7)
    double complex :: d(0:1,0:2,0:2,0:2), duv(0:1,0:2,0:2,0:2)
    call D_cll(d, duv, bm2, bm2, bm2, bm2, dcmplx(x20, 0d0), dcmplx(x31, 0d0), m2, bm2, m2, bm2, 2)
    v = [d(1,0,0,0), d(0,2,0,0), d(0,1,1,0), d(0,1,0,1), d(0,0,2,0), d(0,0,1,1), d(0,0,0,2)]
  end subroutine box

end program
