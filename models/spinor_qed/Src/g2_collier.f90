! g2_collier.f90 -- the one-loop functions of step (8) with COLLIER (research note models/spinor_qed, Eqs. (eq:g2vp), App. g2).
! MS-bar at mu = 1 (COLLIER defaults), e = 1.
!   1. (pi/alpha) Pibar(t) = (K/(4 e^2)) [Pi^R(t) - Pi^R(0)] of a fermion of mass 1 (Pi^R(0) = -(4/3) B0(0; 1, 1) e^2/K, App. g2)
!      at the t values read from the first argument (one per line); written as "t,pibar" to the second, "nan" for |t| < 0.05
!      (the 1/t terms of the PaVe form cancel there; g2_numeric.py uses the series).
!   2. K F2(q^2)/e^2 = -4 m^2 [B0(q^2; m^2, m^2) - B0(0; m^2, m^2) - 2]/(4 m^2 - q^2) of e (m = 1) and mu (m = 1.7) at the points
!      of step (3) -> the third argument, "func,q2,re_f2,im_f2".
! Build and run from Src/ (run_g2_check.sh builds it; g2_numeric.py runs it):
!   gfortran -I$HOME/hep/include g2_collier.f90 -L$HOME/hep/lib -lcollier -o work/g2_collier
!   (cd work && ./g2_collier g2_nodes.txt ../results/g2_collier_pibar.csv ../results/g2_collier_f2.csv)
program g2_collier
  use COLLIER
  implicit none
  double precision, parameter :: q2pts(8) = [-5d0, -1d0, 0d0, 0.5d0, 2d0, 3.9d0, 6d0, 10d0], ms(2) = [1d0, 1.7d0]
  character(len=256) :: f1n, f2n, f3n
  integer :: ui, uo, ios, i, j
  double precision :: t
  double complex :: v

  call get_command_argument(1, f1n); call get_command_argument(2, f2n); call get_command_argument(3, f3n)
  call Init_cll(2, 1, '')
  open(newunit=ui, file=trim(f1n), status='old', action='read')
  open(newunit=uo, file=trim(f2n), status='replace', action='write')
  write(uo, '(a)') 't,pibar'
  do
    read(ui, *, iostat=ios) t
    if (ios /= 0) exit
    if (abs(t) < 0.05d0) then
      write(uo, '(es25.17e3,a)') t, ',nan'
    else
      v = (pif(t, 1d0) + 4d0 / 3d0 * b0f(0d0, 1d0, 1d0)) / 4
      write(uo, '(es25.17e3,",",es25.17e3)') t, dble(v)
    end if
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(f2n)

  open(newunit=uo, file=trim(f3n), status='replace', action='write')
  write(uo, '(a)') 'func,q2,re_f2,im_f2'
  do j = 1, 2
    do i = 1, size(q2pts)
      v = -4 * ms(j)**2 * (b0f(q2pts(i), ms(j)**2, ms(j)**2) - b0f(0d0, ms(j)**2, ms(j)**2) - 2) / (4 * ms(j)**2 - q2pts(i))
      if (j == 1) then
        write(uo, '(a,",",g0,2(",",es25.17e3))') 'F2_e', q2pts(i), dble(v), aimag(v)
      else
        write(uo, '(a,",",g0,2(",",es25.17e3))') 'F2_mu', q2pts(i), dble(v), aimag(v)
      end if
    end do
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(f3n)

contains

  double complex function b0f(p2, ma2, mb2)
    double precision, intent(in) :: p2, ma2, mb2
    call B0_cll(b0f, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
  end function b0f

  ! K Pi_f^R/e^2 (Eq. (7)), MS-bar finite part
  double complex function pif(q2, m)
    double precision, intent(in) :: q2, m
    pif = -4d0 / 3d0 * ((1 + 2 * m**2 / q2) * b0f(q2, m**2, m**2) - 2 * m**2 / q2 * b0f(0d0, m**2, m**2) - 1d0 / 3d0)
  end function pif

end program
