/* twoloop4_tsil.c -- step (16): TSIL 1.46 values for the two-loop self-energy of the phi^3 model in d = 4.
 *
 * TSIL (Martin, Robertson, hep-ph/0501132, "MR05") evaluates the MS-bar basis integrals of two-loop self-energies.
 * Its "bold" integrals are the dimensionally regularized ones with the Euclidean measure
 * 16 Pi^2 mu^(2 eps) d^Dk/(2 Pi)^D = E^(eps EulerGamma) Q^(2 eps) d^Dk/Pi^(D/2) per loop and propagators 1/(k^2 + x);
 * for x = m^2 = Q^2 = 1:
 *   A      = -1/eps + A + eps A_eps                (one-loop tadpole)
 *   B      =  1/eps + B + eps B_eps                (one-loop bubble at s)
 *   S, T, U = sunrise, sunrise with one squared propagator, four-propagator integral (bold, eps^-2 ... eps^0)
 *   I      = vacuum sunrise, bold form built as TSIL_SetBoldS does for S at s = 0:
 *            eps^-2: -3/2, eps^-1: -3/2 + 3 A, eps^0: -(3 (1 + Zeta2) + 3 A^2)/2 + I
 *   M      = the five-propagator kite (finite)
 * MR05's two-loop self-energy of a scalar with cubic coupling g (scalarpole.c with lambda = 0):
 *   Pi1 = -(g^2/2) B,  Pi2 = -(g^4/2) (M + V)   (V = renormalized -dU/dy),
 *   s_pole = x + Pi1/(16 Pi^2) + (Pi2 + Pi1 Pi1')/(16 Pi^2)^2,   Pi1' = -(g^2/2) dB/ds at s = x.
 * Output (stdout, CSV): s, function, eps power, real part, imaginary part; then the pole mass rows.
 * With the argument "grid": s, Re and Im of -(M+V)/2 for s = -3.99, -3.89, ..., 15.91 (avoiding the thresholds 4, 9).
 * Compile: cc -DTSIL_SIZE_DOUBLE -I$HOME/hep/include -o twoloop4_tsil twoloop4_tsil.c -L$HOME/hep/lib -ltsil -lm
 */
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "tsil.h"

static void row(double s, const char *name, int k, TSIL_COMPLEX z)
{
  printf("%g,%s,%d,%.17e,%.17e\n", s, name, k, (double) TSIL_CREAL(z), (double) TSIL_CIMAG(z));
}

int main(int argc, char *argv[])
{
  const double pts[4] = {-1.0, 1.0, 5.0, 12.0};
  const double x = 1.0, qq = 1.0, zeta2 = M_PI*M_PI/6.0;
  TSIL_DATA r;
  int i, n;

  TSIL_WarnsOff();
  if (argc > 1 && strcmp(argv[1], "grid") == 0) {
    printf("s,re,im\n");
    for (i = 0; i < 200; i++) {
      const double s = -3.99 + 0.1*i;
      TSIL_SetParameters(&r, x, x, x, x, x, qq);
      TSIL_Evaluate(&r, s);
      TSIL_COMPLEX sh = -0.5*(TSIL_GetFunction(&r, "M") + TSIL_GetFunction(&r, "Vzxyv"));
      printf("%.4f,%.17e,%.17e\n", s, (double) TSIL_CREAL(sh), (double) TSIL_CIMAG(sh));
    }
    return 0;
  }
  printf("s,function,eps_power,re,im\n");
  for (i = 0; i < 4; i++) {
    const double s = pts[i];
    TSIL_SetParameters(&r, x, x, x, x, x, qq);
    TSIL_Evaluate(&r, s);
    TSIL_COMPLEX A = TSIL_A(x, qq), Aeps = TSIL_Aeps(x, qq);
    TSIL_COMPLEX B = TSIL_B(x, x, s, qq), Beps = TSIL_Beps(x, x, s, qq);
    TSIL_COMPLEX Ivac = TSIL_I2(x, x, x, qq);
    row(s, "A", -1, -x); row(s, "A", 0, A); row(s, "A", 1, Aeps);
    row(s, "B", -1, 1.0); row(s, "B", 0, B); row(s, "B", 1, Beps);
    row(s, "I", -2, -1.5*x); row(s, "I", -1, -1.5*x + 3.0*A);
    row(s, "I", 0, -0.5*(3.0*x*(1.0 + zeta2) + 3.0*A*A/x) + Ivac);
    for (n = 2; n >= 0; n--) {
      row(s, "S", -n, TSIL_GetBoldFunction(&r, "Svyz", n));
      row(s, "T", -n, TSIL_GetBoldFunction(&r, "Tvyz", n));
      row(s, "U", -n, TSIL_GetBoldFunction(&r, "Uzxyv", n));
    }
    row(s, "M", 0, TSIL_GetFunction(&r, "M"));
    row(s, "V_renormalized", 0, TSIL_GetFunction(&r, "Vzxyv"));
    row(s, "Shat_MR05", 0, -0.5*(TSIL_GetFunction(&r, "M") + TSIL_GetFunction(&r, "Vzxyv")));
  }
  /* pole mass at g = 1 (m^2 = Q^2 = 1): one and two loops, as scalarpole.c with lambda = 0 */
  {
    const double g = 1.0, f = 1.0/(16.0*M_PI*M_PI);
    TSIL_SetParameters(&r, x, x, x, x, x, qq);
    TSIL_Evaluate(&r, x);
    TSIL_COMPLEX pi1 = -0.5*g*g*TSIL_B(x, x, x, qq), pi1p = -0.5*g*g*TSIL_dBds(x, x, x, qq);
    TSIL_COMPLEX pi2 = -0.5*g*g*g*g*(TSIL_GetFunction(&r, "M") + TSIL_GetFunction(&r, "Vzxyv"));
    row(x, "pole_mass_sq_one_loop", 0, x + f*pi1);
    row(x, "pole_mass_sq_two_loop", 0, x + f*pi1 + f*f*(pi2 + pi1*pi1p));
    row(x, "dBds_at_x", 0, TSIL_dBds(x, x, x, qq));
  }
  return 0;
}
