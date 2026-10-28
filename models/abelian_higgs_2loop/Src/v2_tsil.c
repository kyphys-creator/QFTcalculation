/* v2_tsil.c -- step (1) of the two-loop note: the MS-bar vacuum sunrise I(x,y,z) and A(x) from TSIL 1.46.
 *
 * TSIL (Martin, Robertson, hep-ph/0501132) evaluates I(x,y,z) analytically (TSIL_I2) in the conventions of Martin's
 * two-loop effective potential (hep-ph/0111209): A(x) = x (ln(x/Q^2) - 1), and the bold (unrenormalized) sunrise
 *   s(x,y,z) = -(x+y+z)/(2 eps^2) + (A(x)+A(y)+A(z) - (x+y+z)/2)/eps + I(x,y,z) + Aeps(x) + Aeps(y) + Aeps(z).
 * Input (stdin): lines "x,y,z" (squared masses, Q^2 = 1).  Output (stdout, CSV): x, y, z, I(x,y,z), A(x), A(y), A(z).
 * Compile: cc -DTSIL_SIZE_DOUBLE -I$HOME/hep/include -o work/v2_tsil v2_tsil.c -L$HOME/hep/lib -ltsil -lm
 */
#include <stdio.h>
#include "tsil.h"

int main(void)
{
  double x, y, z;
  const double qq = 1.0;

  TSIL_WarnsOff();
  printf("x,y,z,I,Ax,Ay,Az\n");
  while (scanf("%lf,%lf,%lf", &x, &y, &z) == 3) {
    printf("%.17g,%.17g,%.17g,%.17e,%.17e,%.17e,%.17e\n", x, y, z,
           (double) TSIL_CREAL(TSIL_I2(x, y, z, qq)),
           x > 0 ? (double) TSIL_CREAL(TSIL_A(x, qq)) : 0.0,
           y > 0 ? (double) TSIL_CREAL(TSIL_A(y, qq)) : 0.0,
           z > 0 ? (double) TSIL_CREAL(TSIL_A(z, qq)) : 0.0);
  }
  return 0;
}
