! oneloop_collier.f90 -- the B0 functions of the note's self-energy formulas (research note models/sm, step (3)) from
! COLLIER, with Delta_UV = 0 and mu^2 given on the command line (oneloop_feyncalc.wl uses mu = MZ).
! Reads results/oneloop_b0.csv (index, p2, m1sq, m2sq, ...; written by oneloop_feyncalc.wl, section (e)) and writes
! index, re, im of B0(p2; m1sq, m2sq).  Build and run from Src/ (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   (cd work && ./oneloop_collier ../results/oneloop_b0.csv ../results/oneloop_collier.csv 8315.25...)
program oneloop_collier
  use COLLIER
  implicit none
  character(len=512) :: infile, outfile, arg, line
  integer :: r, w, ios, idx, n
  double precision :: p2, m1, m2, mu2
  double complex :: b0

  call get_command_argument(1, infile)
  call get_command_argument(2, outfile)
  call get_command_argument(3, arg)
  read(arg, *) mu2
  call Init_cll(2, 1, '')
  call SetMuUV2_cll(mu2)
  call SetMuIR2_cll(mu2)
  call SetDeltaUV_cll(0d0)
  open(newunit=r, file=trim(infile), status='old', action='read')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'index,re_collier,im_collier'
  read(r, '(a)') line
  n = 0
  do
    read(r, '(a)', iostat=ios) line
    if (ios /= 0) exit
    if (len_trim(line) == 0) cycle
    read(line, *) idx, p2, m1, m2
    call B0_cll(b0, dcmplx(p2, 0d0), dcmplx(m1, 0d0), dcmplx(m2, 0d0))
    write(w, '(i0,2(",",es24.16e3))') idx, dble(b0), aimag(b0)
    n = n + 1
  end do
  close(r)
  close(w)
  print '(a,i0,a,a)', 'wrote ', n, ' B0 values to ', trim(outfile)
end program oneloop_collier
