# %% [markdown]
# # Appendix check: the thrust distribution and the limits of the massive R ratio
#
# Research note models/qcd, derivations of the appendices (sympy, mpmath).
#   app:ee 「thrust（式 (thrust)）。」 (E3): the partial fractions, the closed form of Eq. (thrust) against the direct integral and
#       against a two-dimensional integral over the Dalitz region, and the cumulative form (right equation of Eq. (thrust));
#   app:ee 「重いクォーク。」 (E5): Eq. (rmass) near threshold (B -> pi^2/2 - 8 beta, Delta -> pi^2/(2 beta) - 4, series in beta with
#       ln beta) and for beta -> 1 (Delta -> 3/4), the bracket of B reduced with the dilogarithm reflection.
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ee_thrust_rmass.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_ee_thrust_rmass.py   (about 10 s)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import sympy as sp
import mpmath as mp
INTERACTIVE = "ipykernel" in sys.modules


def ok(name, expr):
    e = sp.simplify(expr)
    print(f"{name}: {'OK (0)' if e == 0 else e}")


# %% [markdown]
# ## E3: thrust, Eq. (thrust)

# %%
print("==== E3: thrust ====")
T, x, u, v = sp.symbols('T x u v', positive=True)
f1 = (T**2 + x**2)/(1 - x)
ok("(T^2+x^2)/(1-x) = (1+T^2)/(1-x) - (1+x)", f1 - ((1 + T**2)/(1 - x) - (1 + x)))
ok("x^2 = (1-x)^2 - 2(1-x) + 1", x**2 - ((1 - x)**2 - 2*(1 - x) + 1))
g = (x**2 + (2 - T - x)**2)/((1 - x)*(x + T - 1))
ok("g = (T^2-2T+2)/T (1/(1-x) + 1/(x+T-1)) - 2", g - ((T**2 - 2*T + 2)/T*(1/(1 - x) + 1/(x + T - 1)) - 2))
ok("numerator with u=1-x, v=x+T-1: (1-u)^2+(1-v)^2 = T^2-2T+2-2uv (u+v=T)",
   ((1 - u)**2 + (1 - v)**2 - (T**2 - 2*T + 2 - 2*u*v)).subs(v, T - u))
ok("1/(uv) = (1/T)(1/u+1/v) (u+v=T)", (1/(u*v) - (1/u + 1/v)/T).subs(v, T - u))
lo, hi = 2 - 2*T, T
ell = sp.log((2*T - 1)/(1 - T))
I1 = sp.integrate(1/(1 - x), (x, lo, hi))
I2 = sp.integrate(1/(x + T - 1), (x, lo, hi))
I3 = sp.integrate(1 + x, (x, lo, hi))
print("   int 1/(1-x) =", sp.simplify(I1), "; int 1/(x+T-1) =", sp.simplify(I2))
Tn = sp.Rational(5, 6)
print("   numeric at T=5/6: int 1/(1-x) - ell =", sp.N((I1 - ell).subs(T, Tn)), "; int 1/(x+T-1) - ell =", sp.N((I2 - ell).subs(T, Tn)))
ok("int (1+x) = (3T-2)(4-T)/2", I3 - (3*T - 2)*(4 - T)/2)
ok("int 1 = 3T-2", (hi - lo) - (3*T - 2))
coef = 2*(1 + T**2)/(1 - T) + 2*(T**2 - 2*T + 2)/T
ok("ell coefficient = 2(3T^2-3T+2)/(T(1-T))", coef - 2*(3*T**2 - 3*T + 2)/(T*(1 - T)))
rem = -(3*T - 2)*(4 - T)/(1 - T) - 2*(3*T - 2)
ok("remainder = -3(3T-2)(2-T)/(1-T)", rem - (-3*(3*T - 2)*(2 - T)/(1 - T)))

# %% [markdown]
# ### The closed form against the direct integral

# %%
closed = 2*(3*T**2 - 3*T + 2)/(T*(1 - T))*ell - 3*(3*T - 2)*(2 - T)/(1 - T)
full = 2*sp.integrate(f1/(1 - T), (x, lo, hi)) + sp.integrate(g, (x, lo, hi))
for tv in [sp.Rational(7, 10), sp.Rational(4, 5), sp.Rational(9, 10), sp.Rational(99, 100)]:
    print(f"   T={tv}: direct integral - closed = {sp.N((full - closed).subs(T, tv), 20)}")
closed          # inspect: the closed form of Eq. (thrust)

# %% [markdown]
# ### Against a two-dimensional integral over the Dalitz region; the cumulative form

# %%
# brute-force: dsigma/dT from the 2D Dalitz density f(x1,x2), cumulative in T, compared with the closed form
mp.mp.dps = 20
fD = lambda x1, x2: (x1**2 + x2**2)/((1 - x1)*(1 - x2))
clo = lambda t: 2*(3*t**2 - 3*t + 2)/(t*(1 - t))*mp.log((2*t - 1)/(1 - t)) - 3*(3*t - 2)*(2 - t)/(1 - t)


def cum2d(t0, t1):
    # integral of f over the Dalitz region with t0 < max(x1,x2,x3) < t1, x3 = 2-x1-x2, x_i <= 1
    def inner(x1):
        # x2 range: x1+x2 >= 1 (x3<=1), x2 <= 1; condition on max
        def h(x2):
            m = max(x1, x2, 2 - x1 - x2)
            return fD(x1, x2) if (t0 < m < t1) else 0
        a = 1 - x1; b = mp.mpf(1)
        # breakpoints where the max switches
        pts = sorted(set([a, b] + [p for p in [x1, 2 - 2*x1, (2 - x1)/2, 2 - x1 - t0, 2 - x1 - t1, t0, t1] if a < p < b]))
        return mp.quad(h, pts)
    pts1 = sorted(set([0, 1] + [p for p in [t0, t1, mp.mpf(2)/3, 2 - 2*t0, 2 - 2*t1, 1 - t0, 1 - t1, (2 - t0)/2, (2 - t1)/2] if 0 < p < 1]))
    return mp.quad(inner, pts1)


for (t0, t1) in [(mp.mpf('0.70'), mp.mpf('0.80')), (mp.mpf('0.80'), mp.mpf('0.95'))]:
    print(f"   Dalitz region {t0}<T<{t1}: 2D integral {mp.nstr(cum2d(t0, t1), 10)}  vs  int closed dT {mp.nstr(mp.quad(clo, [t0, t1]), 10)}")
# right equation of eq:thrust: int_{2/3}^{1-y} = F(y)
Fy = lambda y: (3 - 6*y)*mp.log(y/(1 - 2*y)) + 2*mp.log(y/(1 - y))**2 + mp.mpf(5)/2 - 6*y - mp.mpf(9)/2*y**2 + 4*mp.polylog(2, y/(1 - y)) - mp.pi**2/3
for y in [mp.mpf('0.1'), mp.mpf('0.01'), mp.mpf('0.001')]:
    print(f"   y={y}: int_(2/3)^(1-y) closed - F(y) = {mp.nstr(mp.quad(clo, [mp.mpf(2)/3, 1 - y]) - Fy(y), 5)}")


# %% [markdown]
# ## E5: the limits of Eq. (rmass)

# %%
print("==== E5: heavy quark, eq:rmass ====")
mp.mp.dps = 50


def calB(b):
    p = (1 - b)/(1 + b)
    return ((1 + b**2)*(2*mp.log(1 - p)*mp.log(p) + mp.log(1 + p)*mp.log(p) + 2*mp.polylog(2, p) + mp.polylog(2, p**2))
            - 2*b*(2*mp.log(1 - p) + mp.log(1 + p)))


def lnpterm(b):
    p = (1 - b)/(1 + b)
    return -(1 - b)/16*(33 - 39*b - 17*b**2 + 7*b**3)*mp.log(p)


def bracket(b):
    return (3 - b**2)/2*calB(b) + lnpterm(b) + mp.mpf(3)/8*b*(5 - 3*b**2)


def Delta(b):
    return 2/(b*(3 - b**2))*bracket(b)


print("   beta, B - (pi^2/2 - 8 beta), [..]/beta^2 ; lnp-term - 33/8 beta ; bracket - (3pi^2/4 - 6beta) ; Delta - (pi^2/(2beta) - 4)")
for b in ['1e-1', '1e-2', '1e-3', '1e-4', '1e-5']:
    b = mp.mpf(b)
    dB = calB(b) - (mp.pi**2/2 - 8*b)
    dl = lnpterm(b) - mp.mpf(33)/8*b
    dbr = bracket(b) - (3*mp.pi**2/4 - 6*b)
    dD = Delta(b) - (mp.pi**2/(2*b) - 4)
    print(f"   {mp.nstr(b,3):>7}  {mp.nstr(dB,8):>14} {mp.nstr(dB/b**2,10):>14} ; {mp.nstr(dl,8):>14} ; {mp.nstr(dbr,8):>14} ; {mp.nstr(dD,8):>14} (/beta {mp.nstr(dD/b,8)})")
print("   15/8 beta: (3/8)beta(5-3beta^2) - 15/8 beta at beta=1e-3:", mp.nstr(mp.mpf(3)/8*mp.mpf('1e-3')*(5 - 3*mp.mpf('1e-6')) - mp.mpf(15)/8*mp.mpf('1e-3'), 5))
print("   step (8) numbers: Delta - (pi^2/(2b) - 4) at 0.1, 0.01, 0.001:",
      [mp.nstr(Delta(mp.mpf(b)) - (mp.pi**2/(2*mp.mpf(b)) - 4), 3) for b in ['0.1', '0.01', '0.001']])
print("   beta -> 1:")
for b in ['0.9', '0.99', '0.999', '0.99999']:
    b = mp.mpf(b)
    print(f"     beta={mp.nstr(b,6)}: B={mp.nstr(calB(b),8)}, lnp-term={mp.nstr(lnpterm(b),8)}, (3/8)b(5-3b^2)={mp.nstr(mp.mpf(3)/8*b*(5-3*b**2),8)}, Delta={mp.nstr(Delta(b),12)}")

{bv: mp.nstr(Delta(mp.mpf(bv)), 12) for bv in ('0.01', '0.5', '0.99')}          # inspect: Delta of Eq. (rmass) at three velocities

# %% [markdown]
# ### Series at threshold

# %%
# symbolic expansion of B at threshold: Li2(p) = pi^2/6 - ln p ln(1-p) - Li2(1-p) (reflection),
# Li2(1-p), Li2(1-p^2) as power series in their (small) arguments; ln(1-p) = ln 2 + Lb - ln(1+beta), Lb = ln beta
b, Lb = sp.symbols('beta L_beta')
N = 6
p = (1 - b)/(1 + b)
lnp = sp.log(1 - b) - sp.log(1 + b)
ln1mp = sp.log(2) + Lb - sp.log(1 + b)
ln1pp = sp.log(2) - sp.log(1 + b)
dlt = 2*b/(1 + b)          # 1 - p
d2 = 4*b/(1 + b)**2        # 1 - p^2
Li2s = lambda z: sum(z**n/sp.Integer(n)**2 for n in range(1, N + 1))
Li2p = sp.pi**2/6 - lnp*ln1mp - Li2s(dlt)
Li2p2 = sp.pi**2/6 - 2*lnp*(ln1mp + ln1pp) - Li2s(d2)
Bsym = (1 + b**2)*(2*ln1mp*lnp + ln1pp*lnp + 2*Li2p + Li2p2) - 2*b*(2*ln1mp + ln1pp)
Bser = sp.expand(sp.series(Bsym, b, 0, 4).removeO())
print("   B series (L_beta = ln beta):", sp.collect(Bser, [b, Lb]))
brs = sp.expand(sp.series((3 - b**2)/2*Bsym - (1 - b)/16*(33 - 39*b - 17*b**2 + 7*b**3)*lnp + sp.Rational(3, 8)*b*(5 - 3*b**2), b, 0, 3).removeO())
print("   bracket series:", sp.collect(brs, [b, Lb]))
Dser = sp.expand(sp.series(2/(b*(3 - b**2))*((3 - b**2)/2*Bsym - (1 - b)/16*(33 - 39*b - 17*b**2 + 7*b**3)*lnp + sp.Rational(3, 8)*b*(5 - 3*b**2)), b, 0, 2).removeO())
print("   Delta series:", sp.collect(Dser, [b, Lb]))
print("   ln p series:", sp.series(lnp, b, 0, 5))
# the log terms in B: check the cancellation of beta*ln(1-p) and beta*ln(1+p) terms at O(beta)
inner = 2*ln1mp*lnp + ln1pp*lnp + 2*Li2p + Li2p2
print("   bracket of B, reduced: pi^2/2 - 2 lnp ln(1-p) - lnp ln(1+p) - 2Li2(1-p) - Li2(1-p^2) ? ->",
      sp.simplify(sp.expand(inner - (sp.pi**2/2 - 2*lnp*ln1mp - lnp*ln1pp - 2*Li2s(dlt) - Li2s(d2)))))
Dser          # inspect: Delta near threshold
