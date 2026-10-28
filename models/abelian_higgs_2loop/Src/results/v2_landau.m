{"V2" -> (lam*A[xg]*A[xh])/2 + 
   (el^2*(2*xa*A[xg] + 3*A[xa]*A[xg] + 2*xa*A[xh] + 3*A[xa]*A[xh]))/2 + 
   (3*lam*(A[xg]^2 + A[xh]^2))/4 + el^4*phi^2*(-2*xa - xh + A[xa] + 2*A[xh] + 
     ((-2*xa + xh)*A[xa]^2 + 2*xa*A[xa]*A[xh] - xh^2*II[0, 0, xh] + 
       2*(xa - xh)^2*II[0, xa, xh] + (-12*xa^2 + 4*xa*xh - xh^2)*
        II[xa, xa, xh])/(4*xa^2)) + 
   (el^2*(2*(-1/3*xa + xg + xh)*A[xa] + ((-xa - xg + xh)*A[xa]*A[xg] + 
        (-xa + xg - xh)*A[xa]*A[xh] + xa*A[xg]*A[xh] + 
        (-xg + xh)^2*II[0, xh, xg] + (-xa^2 + 2*xa*xg - xg^2 + 2*xa*xh + 
          2*xg*xh - xh^2)*II[xh, xg, xa])/xa))/2 - 
   lam^2*phi^2*II[xh, xg, xg] - 3*lam^2*phi^2*II[xh, xh, xh], 
 "masses" -> {xh -> -m2 + 3*lam*phi^2, xg -> -m2 + lam*phi^2, 
   xa -> el^2*phi^2}}
