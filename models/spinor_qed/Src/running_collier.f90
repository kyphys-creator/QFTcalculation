! running_collier.f90 -- the vacuum polarization of one flavour with COLLIER for step (9) (research note models/spinor_qed,
! Eqs. (eq:disp), (eq:aeff), (eq:uehling), App. run).  MS-bar at mu = m = 1 (COLLIER defaults), so Pi^R(0) = 0 and the
! bracket K Pi_f^R/e^2 = -(4/3) [(1 + 2/q^2) B0(q^2; 1, 1) - (2/q^2) B0(0; 1, 1) - 1/3] (Eq. (7)) equals K Pibar/e^2.
! Reads q^2 values (one per line, timelike above threshold with +i0) from the first argument and writes "q2,re,im" of
! K Pibar/e^2 to the second.
! Build and run from Src/ (run_running_check.sh builds it; running_numeric.py runs it):
!   gfortran -I$HOME/hep/include running_collier.f90 -L$HOME/hep/lib -lcollier -o work/running_collier
!   (cd work && ./running_collier running_q2.txt ../results/running_collier.csv)
program running_collier
  use COLLIER
  implicit none
  character(len=256) :: f1n, f2n
  integer :: ui, uo, ios
  double precision :: q2
  double complex :: v, b0q, b00

  call get_command_argument(1, f1n); call get_command_argument(2, f2n)
  call Init_cll(2, 1, '')
  open(newunit=ui, file=trim(f1n), status='old', action='read')
  open(newunit=uo, file=trim(f2n), status='replace', action='write')
  write(uo, '(a)') 'q2,re,im'
  call B0_cll(b00, (0d0, 0d0), (1d0, 0d0), (1d0, 0d0))
  do
    read(ui, *, iostat=ios) q2
    if (ios /= 0) exit
    call B0_cll(b0q, dcmplx(q2, 0d0), (1d0, 0d0), (1d0, 0d0))
    v = -4d0 / 3d0 * ((1 + 2 / q2) * b0q - 2 / q2 * b00 - 1d0 / 3d0)
    write(uo, '(es25.17e3,2(",",es25.17e3))') q2, dble(v), aimag(v)
  end do
  close(uo)
  print '(a,a)', 'wrote ', trim(f2n)
end program
