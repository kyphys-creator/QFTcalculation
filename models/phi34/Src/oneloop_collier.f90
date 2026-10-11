! oneloop_collier.f90 -- the brackets b_n = (4 pi)^2 V_n^R / i of the one-loop 1PI functions of phi^3 + phi^4
! (research note models/phi34, Eq. (6)) from COLLIER, at m = mu = g = lambda = 1 and the points of
! oneloop_feyncalc.wl.  COLLIER's defaults (Delta_UV = 0, mu^2 = 1) give the MS-bar finite parts.
!   b2 = [B0(p^2) + A0]/2,   b3 = C0(k1^2, k2^2, p^2) + [B0(p^2) + B0(k1^2) + B0(k2^2)]/2,
!   b4 = [B0(s) + B0(t) + B0(u)]/2 + 2 [C0(1,1,s) + C0(1,1,t) + C0(1,1,u)] + D0(s,t) + D0(s,u) + D0(t,u)
! Writes results/oneloop_collier.csv.  Build and run from Src/ (run_oneloop_check.sh does this):
!   gfortran -I$HOME/hep/include oneloop_collier.f90 -L$HOME/hep/lib -lcollier -o work/oneloop_collier
!   (cd work && ./oneloop_collier ../results/oneloop_collier.csv)
program oneloop_collier
  use COLLIER
  implicit none
  double complex, parameter :: one = (1d0, 0d0)
  double precision, parameter :: v2pts(6) = [-5d0, 0d0, 1d0, 2d0, 5d0, 10d0]
  double precision, parameter :: v3pts(3,5) = reshape([1d0,1d0,-5d0, 1d0,1d0,-1d0, 1d0,1d0,5d0, &
                                                       1d0,1d0,10d0, -1d0,-2d0,-3d0], [3,5])
  double precision, parameter :: rs(3) = [2.5d0, 5d0, 10d0], cs(2) = [0.3d0, 0.9d0]
  double complex :: a0, b, bsum, c, csum, d, dsum, res
  double precision :: s, t, u, p2, inv(3)
  character(len=256) :: outfile
  integer :: i, j, k, w

  call get_command_argument(1, outfile)
  if (len_trim(outfile) == 0) outfile = 'oneloop_collier.csv'
  call Init_cll(4, 0, '')
  open(newunit=w, file=trim(outfile), status='replace', action='write')
  write(w, '(a)') 'func,arg1,arg2,arg3,re_collier,im_collier'
  call A0_cll(a0, one)
  do i = 1, size(v2pts)
    call B0_cll(b, dcmplx(v2pts(i), 0d0), one, one)
    res = (b + a0) / 2
    write(w, '(a,3(",",g0),2(",",es24.16e3))') 'V2', v2pts(i), 0d0, 0d0, dble(res), aimag(res)
  end do
  do i = 1, size(v3pts, 2)
    inv = v3pts(:, i)
    call C0_cll(c, dcmplx(inv(1), 0d0), dcmplx(inv(2), 0d0), dcmplx(inv(3), 0d0), one, one, one)
    bsum = (0d0, 0d0)
    do k = 1, 3
      call B0_cll(b, dcmplx(inv(k), 0d0), one, one)
      bsum = bsum + b
    end do
    res = c + bsum / 2
    write(w, '(a,3(",",g0),2(",",es24.16e3))') 'V3', inv(1), inv(2), inv(3), dble(res), aimag(res)
  end do
  do i = 1, size(rs)
    do j = 1, size(cs)
      s = rs(i)**2
      p2 = s / 4 - 1
      t = -2 * p2 * (1 - cs(j))
      u = -2 * p2 * (1 + cs(j))
      bsum = (0d0, 0d0); csum = (0d0, 0d0); dsum = (0d0, 0d0)
      do k = 1, 3
        inv(1) = merge(s, merge(t, u, k == 2), k == 1)
        call B0_cll(b, dcmplx(inv(1), 0d0), one, one)
        call C0_cll(c, one, one, dcmplx(inv(1), 0d0), one, one, one)
        bsum = bsum + b
        csum = csum + c
      end do
      ! D0_cll(D0, p10, p21, p32, p30, p20, p31, m02, m12, m22, m32): p20, p31 are the two invariants
      call D0_cll(d, one, one, one, one, dcmplx(s, 0d0), dcmplx(t, 0d0), one, one, one, one); dsum = dsum + d
      call D0_cll(d, one, one, one, one, dcmplx(s, 0d0), dcmplx(u, 0d0), one, one, one, one); dsum = dsum + d
      call D0_cll(d, one, one, one, one, dcmplx(t, 0d0), dcmplx(u, 0d0), one, one, one, one); dsum = dsum + d
      res = bsum / 2 + 2 * csum + dsum
      write(w, '(a,3(",",g0),2(",",es24.16e3))') 'V4', s, t, 0d0, dble(res), aimag(res)
    end do
  end do
  close(w)
  print '(a,a)', 'wrote ', trim(outfile)
end program
