! eemm_collier.f90 -- the loop functions of the one-loop e- e+ -> mu- mu+ amplitude of FormCalc (research note models/sm,
! step (6)) from COLLIER: finite part (Delta_UV = Delta_IR = 0), the coefficient of Delta_UV and the coefficient of the
! soft pole Delta_IR1 (photon massless, dimensional regularization), mu_UV = mu_IR given on the command line.
! Input (written by eemm_numeric.py): one function per line, "index kind n x_1 ... x_n" with kind
!   A0 (m^2), B0, B1, B00, B11, DB0, DB1, DB00, DB11 (p^2, m1^2, m2^2), C0 (p1^2, p2^2, (p1+p2)^2, m1^2, m2^2, m3^2),
!   D0 (p1^2, p2^2, p3^2, p4^2, (p1+p2)^2, (p2+p3)^2, m1^2 .. m4^2)
! in LoopTools' order, which is COLLIER's (p10, p21, p20, m02, m12, m22) and (p10, p21, p32, p30, p20, p31, m02 .. m32).
! Output: index, re/im of the finite part, of the UV coefficient and of the IR coefficient.
! Build and run from Src/ (run_eemm_check.sh does this):
!   gfortran -I$HOME/hep/include eemm_collier.f90 -L$HOME/hep/lib -lcollier -o work/eemm_collier
!   (cd work && ./eemm_collier eemm_collier_in.txt ../results/eemm_collier.csv 8315.25...)
program eemm_collier
  use COLLIER
  implicit none
  character(len=512) :: infile, outfile, arg
  character(len=8) :: kind
  integer :: r, w, ios, idx, n, nv, k
  double precision :: x(10), mu2
  double complex :: v(3), f0, f1

  call get_command_argument(1, infile)
  call get_command_argument(2, outfile)
  call get_command_argument(3, arg)
  read(arg, *) mu2
  call Init_cll(4, 2, '')
  call SetMuUV2_cll(mu2)
  call SetMuIR2_cll(mu2)
  open(newunit=r, file=trim(infile), status='old', action='read')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'index,re_fin,im_fin,re_uv,im_uv,re_ir,im_ir'
  n = 0
  do
    read(r, *, iostat=ios) idx, kind, nv, (x(k), k = 1, nv)
    if (ios /= 0) exit
    call SetDeltaUV_cll(0d0)
    call SetDeltaIR_cll(0d0, 0d0)
    f0 = fn(kind, x)
    v(1) = f0
    call SetDeltaUV_cll(1d0)
    f1 = fn(kind, x)
    v(2) = f1 - f0
    call SetDeltaUV_cll(0d0)
    call SetDeltaIR_cll(1d0, 0d0)
    f1 = fn(kind, x)
    v(3) = f1 - f0
    write(w, '(i0,6(",",es24.16e3))') idx, (dble(v(k)), aimag(v(k)), k = 1, 3)
    n = n + 1
  end do
  close(r)
  close(w)
  print '(a,i0,a,a)', 'wrote ', n, ' loop functions to ', trim(outfile)

contains

  double complex function fn(kind, x)
    character(len=*), intent(in) :: kind
    double precision, intent(in) :: x(10)
    double complex :: c(10), b(0:1, 0:2), buv(0:1, 0:2), res
    c = dcmplx(x, 0d0)
    select case (trim(kind))
    case ('A0')
      call A0_cll(res, c(1))
    case ('B0')
      call B0_cll(res, c(1), c(2), c(3))
    case ('B1', 'B00', 'B11')
      call B_cll(b, buv, c(1), c(2), c(3), 2)
      if (trim(kind) == 'B1') res = b(0, 1)
      if (trim(kind) == 'B00') res = b(1, 0)
      if (trim(kind) == 'B11') res = b(0, 2)
    case ('DB0')
      call DB0_cll(res, c(1), c(2), c(3))
    case ('DB1')
      call DB1_cll(res, c(1), c(2), c(3))
    case ('DB00')
      call DB00_cll(res, buv(0, 0), c(1), c(2), c(3))
    case ('DB11')
      call DB11_cll(res, c(1), c(2), c(3))
    case ('C0')
      call C0_cll(res, c(1), c(2), c(3), c(4), c(5), c(6))
    case ('D0')
      call D0_cll(res, c(1), c(2), c(3), c(4), c(5), c(6), c(7), c(8), c(9), c(10))
    case default
      print '(a,a)', 'unknown function ', trim(kind)
      stop 1
    end select
    fn = res
  end function fn

end program eemm_collier
