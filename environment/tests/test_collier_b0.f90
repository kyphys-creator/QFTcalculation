! COLLIER test: B0(p^2=2; m0=m1=1) with mu^2=1, Delta_UV=0.  Exact: 2 - pi/2.
program collier_b0
  use COLLIER
  implicit none
  double complex :: B0
  call Init_cll(2, 2, '')
  call B0_cll(B0, (2d0,0d0), (1d0,0d0), (1d0,0d0))
  print '(a,f15.12)', 'COLLIER B0(2;1,1) = ', dble(B0)
end program
