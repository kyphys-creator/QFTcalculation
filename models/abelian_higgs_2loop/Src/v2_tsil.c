/* v2_tsil.c -- steps (1), (2) of the two-loop note: the MS-bar vacuum sunrise I(x,y,z) and A(x) from TSIL 1.46.
 *
 * TSIL (Martin, Robertson, hep-ph/0501132) evaluates I(x,y,z) analytically (TSIL_I2) in the conventions of Martin's
 * two-loop effective potential (hep-ph/0111209): A(x) = x (ln(x/Q^2) - 1), and the bold (unrenormalized) sunrise
 *   s(x,y,z) = -(x+y+z)/(2 eps^2) + (A(x)+A(y)+A(z) - (x+y+z)/2)/eps + I(x,y,z) + Aeps(x) + Aeps(y) + Aeps(z).
 * Input (stdin): lines "x,y,z" (squared masses, Q^2 = 1) or "x,y,z,qq" (Q^2 = qq).
 * Output (stdout, CSV): x, y, z, qq, I(x,y,z), A(x), A(y), A(z).
 * Compile: cc -DTSIL_SIZE_DOUBLE -I$HOME/hep/include -o work/v2_tsil v2_tsil.c -L$HOME/hep/lib -ltsil -lm
 */
#include <stdio.h>
#include "tsil.h"

int main(void)
{
  char line[512];
  double x, y, z, qq;
  int n;

  TSIL_WarnsOff();
  printf("x,y,z,qq,I,Ax,Ay,Az\n");
  while (fgets(line, sizeof line, stdin) != NULL) {
    n = sscanf(line, "%lf,%lf,%lf,%lf", &x, &y, &z, &qq);
    if (n < 3) continue;
    if (n == 3) qq = 1.0;
    printf("%.17g,%.17g,%.17g,%.17g,%.17e,%.17e,%.17e,%.17e\n", x, y, z, qq,
           (double) TSIL_CREAL(TSIL_I2(x, y, z, qq)),
           x > 0 ? (double) TSIL_CREAL(TSIL_A(x, qq)) : 0.0,
           y > 0 ? (double) TSIL_CREAL(TSIL_A(y, qq)) : 0.0,
           z > 0 ? (double) TSIL_CREAL(TSIL_A(z, qq)) : 0.0);
  }
  return 0;
}
