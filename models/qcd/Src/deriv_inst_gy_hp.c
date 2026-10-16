/* deriv_inst_gy_hp.c -- research note models/qcd, app:inst 「大きい質量の展開。」, step (10) checks (the m^-8 coefficient c8 = -6 A_6).
   u = m^2 derivatives (orders 0..3) of the Gel'fand-Yaglom mass correction of one partial wave of -D^2 + m^2
   in the BPST background (rho = 1, regular gauge), isospin t = 1/2 or 1.
   Built and called by deriv_inst_gy_hp_lib.py (build(): cc -O3 -ffp-contract=off -shared -fPIC -I work/inst_gy_hp, with the DOP853
   weights written by write_coef() to work/inst_gy_hp/dop853coef.h; the library is work/inst_gy_hp/libgyd.dylib).

   Formulation (as in inst_gylib.py, extended by sensitivity equations):
     tau = ln r, x = r^2.  massless exact solution psi0 with r psi0'/psi0 = 2k + g(x)  (k = large-r angular momentum)
     free reference psi_f = I_nu(m r)/r, nu = 2k+1:  Pf = r psi_f'/psi_f - 2k
     Q = r d/dr [ln(psi/psi0) - ln(psi_f/r^{2k})],   Delta(u) = int_0^inf Q dtau  (mass correction of the wave)
     E = Q + g = w - w_f  (w = r psi'/psi),  yf = Pf + 2k + 1,  W = E + yf = w + 1.
     dPf = u x - Pf^2 - (4k+2) Pf
     dQ  = -(2Pf + Q) Q - 2(g + 2k + 1) Q - 2 g Pf
     u-derivatives F_n = d^n Pf/du^n, E_n = d^n Q/du^n = d^n E/du^n:
     dF1 = x - 2 yf F1,  dF2 = -2 F1^2 - 2 yf F2,  dF3 = -6 F1 F2 - 2 yf F3
     dE1 = -2 W E1 - 2 E F1
     dE2 = -2 E1 (E1 + 2 F1) - 2 W E2 - 2 E F2
     dE3 = -6 (E1 E2 + E1 F2 + F1 E2) - 2 W E3 - 2 E F3
     I_n = int E_n dtau  (I_0 = int Q dtau).
   Tail r > R (linear response in dV = 4 l(l+1) + r^2 U - 4 k(k+1) = -4c/(1+x) - 4t(t+1) x/(1+x)^2, exact Green function I_nu K_nu):
     int_R^inf E dtau = E(R) IK(mR) + int_R^inf (dr/r) [dV - E^2] IK(m r),  E^2 ~ (dV IK)^2 (second order),  IK by the uniform (Debye) expansion
     IK = 1/(2P) + 1/(16 P^3) - 6 nu^2/(16 P^5) + 5 nu^4/(16 P^7),  P = sqrt(nu^2 + u r^2);  d^n/du^n at fixed r, R.
     (n = 0 additionally -int_R^inf g dtau.)
   Integrator: fixed-step 8th-order Runge-Kutta (DOP853 weights), step h = min(hmax, hfac / yf).                              */
#include <math.h>
#include <string.h>
#include "dop853coef.h"

#define NY 12
typedef struct { int type; double l, k, c, tt, A, B, C, u; } chan_t;

static double gfun(const chan_t *p, double x) {
    double l = p->l;
    switch (p->type) {
    case 0: return -((2*l + 2) + (2*l + 3)*x)/(((2*l + 2) + (2*l + 1)*x)*(1 + x));   /* t=1/2 (l, l+1/2) */
    case 1: return 1.0/(1 + x);                                                      /* t=1/2 (l+1/2, l) */
    case 2: return -2*(p->A + 2*p->A*x + (p->B - p->C)*x*x)/((p->A + p->B*x + p->C*x*x)*(1 + x)); /* t=1 (l, l+1) */
    case 3: return 2.0/(1 + x);                                                      /* t=1 (l+1, l) */
    case 4: return -4*x/(((2*l + 2) + 2*l*x)*(1 + x));                               /* t=1 (l, l) */
    }
    return 0;
}
static double dVfun(const chan_t *p, double x) {
    return -4*p->c/(1 + x) - 4*p->tt*(p->tt + 1)*x/((1 + x)*(1 + x));
}

static void rhs(const chan_t *p, double tau, const double *y, double *f) {
    double x = exp(2*tau), k = p->k, u = p->u;
    double gg = gfun(p, x);
    double Pf = y[0], Q = y[1], F1 = y[2], F2 = y[3], F3 = y[4], E1 = y[5], E2 = y[6], E3 = y[7];
    double yf = Pf + 2*k + 1, E = Q + gg, W = E + yf;
    f[0] = u*x - Pf*(Pf + 4*k + 2);
    f[1] = -(2*Pf + Q)*Q - 2*(gg + 2*k + 1)*Q - 2*gg*Pf;
    f[2] = x - 2*yf*F1;
    f[3] = -2*F1*F1 - 2*yf*F2;
    f[4] = -6*F1*F2 - 2*yf*F3;
    f[5] = -2*W*E1 - 2*E*F1;
    f[6] = -2*E1*(E1 + 2*F1) - 2*W*E2 - 2*E*F2;
    f[7] = -6*(E1*E2 + E1*F2 + F1*E2) - 2*W*E3 - 2*E*F3;
    f[8] = Q; f[9] = E1; f[10] = E2; f[11] = E3;
}

/* d^n/du^n of IK(P), P = sqrt(nu^2 + u r^2), n = 0..3, at fixed r */
static void IKder(double nu, double u, double r, double *d) {
    static const int a[4] = {1, 3, 5, 7};
    double cf[4] = {0.5, 1.0/16, -6*nu*nu/16, 5*nu*nu*nu*nu/16};
    double P2 = nu*nu + u*r*r, P = sqrt(P2), r2 = r*r;
    d[0] = d[1] = d[2] = d[3] = 0;
    for (int i = 0; i < 4; i++) {
        double ai = a[i], Pa = pow(P, -ai);
        d[0] += cf[i]*Pa;
        d[1] += cf[i]*(-ai/2)*r2*Pa/P2;
        d[2] += cf[i]*(ai/2)*((ai + 2)/2)*r2*r2*Pa/(P2*P2);
        d[3] += cf[i]*(-(ai/2)*((ai + 2)/2)*((ai + 4)/2))*r2*r2*r2*Pa/(P2*P2*P2);
    }
}

/* out: [0..3] Delta^(n) total, [4..7] I_n(R), [8..11] tails, [12] steps, [13] E(R), [14] R */
int gy_wave(int type, double l, double k, double c, double tt, double A, double B, double C,
            double u, double R, double r0, double hfac, double hmax,
            int ngl, const double *sgl, const double *wgl, double *out) {
    chan_t p = {type, l, k, c, tt, A, B, C, u};
    double y[NY], Kst[12][NY], yt[NY];
    memset(y, 0, sizeof y);
    double x0 = r0*r0, g0 = gfun(&p, 0.0);
    double pp = u/(4*k + 4);
    double q = -g0*pp/(2*k + g0 + 2);
    double e1 = -g0/((4*k + 4)*(2*k + 2 + g0));
    double a2 = -2/((4*k + 4)*(4*k + 4)*(4*k + 6));
    double lw = k + g0/2;   /* angular momentum at the origin */
    double b2 = (-2*e1*(e1 + 2/(4*k + 4)) - 2*g0*a2)/(4*lw + 6);
    y[0] = pp*x0; y[1] = q*x0; y[2] = x0/(4*k + 4); y[3] = a2*x0*x0; y[4] = 0;
    y[5] = e1*x0; y[6] = b2*x0*x0; y[7] = 0;
    y[8] = q*x0/2; y[9] = e1*x0/2; y[10] = b2*x0*x0/4; y[11] = 0;
    double tau = log(r0), tau1 = log(R);
    long nst = 0;
    while (tau < tau1) {
        double yf = y[0] + 2*k + 1;
        double h = hfac/fabs(yf);
        if (h > hmax) h = hmax;
        if (tau + h > tau1) h = tau1 - tau;
        for (int s = 0; s < 12; s++) {
            for (int i = 0; i < NY; i++) {
                double acc = 0;
                for (int j = 0; j < s; j++) acc += RKA[s][j]*Kst[j][i];
                yt[i] = y[i] + h*acc;
            }
            rhs(&p, tau + RKC[s]*h, yt, Kst[s]);
        }
        for (int i = 0; i < NY; i++) {
            double acc = 0;
            for (int s = 0; s < 12; s++) acc += RKB[s]*Kst[s][i];
            y[i] += h*acc;
        }
        tau += h; nst++;
    }
    /* tails */
    double nu = 2*k + 1, xR = R*R;
    double gR = gfun(&p, xR);
    double En[4] = {y[1] + gR, y[5], y[6], y[7]};
    double dR[4]; IKder(nu, u, R, dR);
    double T[4];
    T[0] = En[0]*dR[0];
    T[1] = En[1]*dR[0] + En[0]*dR[1];
    T[2] = En[2]*dR[0] + 2*En[1]*dR[1] + En[0]*dR[2];
    T[3] = En[3]*dR[0] + 3*En[2]*dR[1] + 3*En[1]*dR[2] + En[0]*dR[3];
    double gint = 0;
    for (int i = 0; i < ngl; i++) {
        double s = sgl[i], w = wgl[i];
        double r = R/s, x = r*r, d[4];
        IKder(nu, u, r, d);
        double dv = dVfun(&p, x);
        for (int n = 0; n < 4; n++) T[n] += w/s*dv*d[n];
        /* second order in dV: source -E^2 with E ~ dV IK (quasi-static), i.e. -dV^2 IK^3 */
        double c3[4];
        c3[0] = d[0]*d[0]*d[0];
        c3[1] = 3*d[0]*d[0]*d[1];
        c3[2] = 6*d[0]*d[1]*d[1] + 3*d[0]*d[0]*d[2];
        c3[3] = 6*d[1]*d[1]*d[1] + 18*d[0]*d[1]*d[2] + 3*d[0]*d[0]*d[3];
        for (int n = 0; n < 4; n++) T[n] -= w/s*dv*dv*c3[n];
        gint += w/s*gfun(&p, x);
    }
    T[0] -= gint;
    for (int n = 0; n < 4; n++) { out[4 + n] = y[8 + n]; out[8 + n] = T[n]; out[n] = y[8 + n] + T[n]; }
    out[12] = (double)nst; out[13] = En[0]; out[14] = R;
    return 0;
}
