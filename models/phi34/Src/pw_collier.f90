! pw_collier.f90 -- the three coupling structures of the MS-bar one-loop phi phi -> phi phi amplitude of phi^3 + phi^4
! (note models/phi34, Eq. (9); mu = m), M1 = g^4 P + g^2 lambda Q + lambda^2 R, at the quadrature nodes of the partial-wave
! projection (step (8)).  m = mu = 1, Delta_UV = 0.  Reads lines "sqrts costheta" from the file given as the first argument
! and writes "sqrts,costheta,s,t,u,re_p,im_p,re_q,im_q,re_r,im_r" to the second.  The structures are those of
! rg_collier.f90 (and scat_collier.f90 with g = lambda = 1).
!
! Build and run from Src/ (run_pw_check.sh does this; pw_numeric.py calls it):
!   gfortran -I$HOME/hep/include pw_collier.f90 -L$HOME/hep/lib -lcollier -o work/pw_collier
!   (cd work && ./pw_collier nodes.txt structures.csv)
program pw_collier
  use COLLIER
  implicit none
  double precision, parameter :: pi = 3.14159265358979323846d0
  character(len=256) :: infile, outfile
  double precision :: rs, ct, s, t, u, p2
  double complex :: parts(3)
  integer :: ui, uo, ios

  call get_command_argument(1, infile)
  call get_command_argument(2, outfile)
  call Init_cll(4, 0, '')
  open(newunit=ui, file=trim(infile), status='old', action='read')
  open(newunit=uo, file=trim(outfile), status='replace', action='write')
  write(uo, '(a)') 'sqrts,costheta,s,t,u,re_p,im_p,re_q,im_q,re_r,im_r'
  do
    read(ui, *, iostat=ios) rs, ct
    if (ios /= 0) exit
    s = rs**2
    p2 = s/4d0 - 1d0
    t = -2d0*p2*(1d0 - ct)
    u = -2d0*p2*(1d0 + ct)
    call structures(s, t, u, parts)
    write(uo, '(11(es24.16e3,:,","))') rs, ct, s, t, u, dble(parts(1)), aimag(parts(1)), dble(parts(2)), &
      aimag(parts(2)), dble(parts(3)), aimag(parts(3))
  end do
  close(ui)
  close(uo)

contains

  double complex function d0f(x, y)
    double precision, intent(in) :: x, y
    double complex, parameter :: one = (1d0, 0d0)
    call D0_cll(d0f, one, one, one, one, dcmplx(x, 0d0), dcmplx(y, 0d0), one, one, one, one)
  end function

  double complex function c0f(x)
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    call C0_cll(c0f, one, one, dcmplx(x, 0d0), one, one, one)
  end function

  double complex function b0f(x)
    double precision, intent(in) :: x
    double complex, parameter :: one = (1d0, 0d0)
    call B0_cll(b0f, dcmplx(x, 0d0), one, one)
  end function

  subroutine structures(s, t, u, parts)
    ! parts = (P, Q, R): the coefficients of g^4, g^2 lambda, lambda^2 in M1, each including the 1/(4 pi)^2
    double precision, intent(in) :: s, t, u
    double complex, intent(out) :: parts(3)
    double complex, parameter :: one = (1d0, 0d0)
    double precision :: xs(3)
    double complex :: a0, b0m, g4, g2l, l2
    integer :: n
    xs = [s, t, u]
    call A0_cll(a0, one)
    b0m = b0f(1d0)
    g4 = d0f(s, t) + d0f(s, u) + d0f(t, u)
    g2l = (0d0, 0d0)
    l2 = (0d0, 0d0)
    do n = 1, 3
      g4 = g4 + 2d0*c0f(xs(n))/(xs(n) - 1d0) + b0f(xs(n))/(2d0*(xs(n) - 1d0)**2)
      g2l = g2l + 2d0*c0f(xs(n)) + (b0f(xs(n)) + 2d0*b0m)/(xs(n) - 1d0) + a0/(2d0*(xs(n) - 1d0)**2)
      l2 = l2 + b0f(xs(n))/2d0
    end do
    parts = [g4, g2l, l2]/(16d0*pi**2)
  end subroutine

end program
