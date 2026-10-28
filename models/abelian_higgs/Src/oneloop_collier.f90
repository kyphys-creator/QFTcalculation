! oneloop_collier.f90 -- step (3) of the abelian Higgs note: the MS-bar finite parts of the B0 functions of the self-energies
! (list results/oneloop_b0_args.csv written by oneloop_numeric.wl: p2, m1^2, m2^2 in units of MA^2) from COLLIER with
! Delta_UV = 0 and mu_UV = mu = 1 (the benchmark of the note).  Output: results/oneloop_collier_b0.csv with the
! columns p2, m1sq, m2sq, re, im in the order of the input.  Build and run from Src/ (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   work/oneloop_collier results/oneloop_b0_args.csv results/oneloop_collier_b0.csv
program oneloop_collier
  use COLLIER
  implicit none
  character(len=512) :: infile, outfile, line
  integer :: r, w, ios, n
  double precision :: p2, ma2, mb2
  double complex :: b0

  call get_command_argument(1, infile)
  call get_command_argument(2, outfile)
  call Init_cll(2, 1, '')
  call SetMuUV2_cll(1d0)
  call SetMuIR2_cll(1d0)
  call SetDeltaUV_cll(0d0)
  open(newunit=r, file=trim(infile), status='old', action='read')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'p2,m1sq,m2sq,re,im'
  read(r, '(a)') line                      ! header
  n = 0
  do
    read(r, '(a)', iostat=ios) line
    if (ios /= 0) exit
    call clean(line)
    read(line, *) p2, ma2, mb2
    call B0_cll(b0, dcmplx(p2, 0d0), dcmplx(ma2, 0d0), dcmplx(mb2, 0d0))
    write(w, '(3(es26.17e3,","),es26.17e3,",",es26.17e3)') p2, ma2, mb2, dble(b0), aimag(b0)
    n = n + 1
  end do
  close(r); close(w)
  print '(a,i0,a,a)', 'COLLIER: ', n, ' B0 values written to ', trim(outfile)

contains

  subroutine clean(s)                      ! strip the quotes of the CSV
    character(len=*), intent(inout) :: s
    integer :: i
    do i = 1, len(s)
      if (s(i:i) == '"') s(i:i) = ' '
    end do
  end subroutine clean

end program oneloop_collier
