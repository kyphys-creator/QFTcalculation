(* ::Package:: *)

(* onshell4_check.wl -- symbolic checks of the S-matrix element and the scheme conversion for
   phi phi -> phi phi in d = 4 (research note, App. J, Eqs. (19)-(20)).  Package-X (through FeynHelpers) supplies
   the MS-bar B0(p^2; m, m) as an explicit function.

   (1) B0(m^2; m, m) = -L + 2 - Pi/Sqrt[3] and m^2 B0'(m^2; m, m) = 2 Pi/(3 Sqrt[3]) - 1, L = Log[m^2/mu^2].
   (2) the pole mass m_p^2 = m^2 - g^2/(2 (4 Pi)^2) B0(m^2) and the residue R = 1 - g^2/(2 (4 Pi)^2) B0'(m^2)
       do not depend on mu at O(g^2), using mu dm^2/dmu = g^2/(4 Pi)^2.
   (3) the B0 part of M_phys from the MS-bar amplitude (R^2, p_i^2 = m_p^2, m -> m_p in the tree)
       equals the on-shell-scheme computation (on-shell self-energy, vertex counterterm 3/2 deltaZ),
       up to O(g^6).
   (4) M_phys^(1) does not depend on mu; the MS-bar M0(m(mu)) + M1(mu) does not either, at O(g^4).

   Usage:  wolframscript -file onshell4_check.wl *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];

k4 = (4 Pi)^2;
(* MS-bar B0(p2; mm, mm) at scale mu (App. G), from Package-X in FeynCalc's normalization *)
b0Expr = Module[{v = Series[(2 Pi)^(2 Epsilon) PaXEvaluate[I Pi^2 B0[pp, mm^2, mm^2]]/(2 Pi)^4, {Epsilon, 0, 0}]},
   Simplify[(SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma))/(I/k4) /. ScaleMu -> mu,
    mm > 0 && mu > 0]];
b0[p2_, mass_] := b0Expr /. {pp -> p2, mm -> mass};
b0p[p2_, mass_] := (D[b0Expr, pp] /. {pp -> p2, mm -> mass});
logRules = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
zeroQ[expr_] := Simplify[PowerExpand[expr /. logRules], m > 0 && mu > 0 && mp > 0] === 0;

(* (1) closed forms at p^2 = m^2 (the limit avoids the 0/0 form of Package-X's expression) *)
b0AtM = Limit[b0[pp, m], pp -> m^2, Assumptions -> m > 0 && mu > 0];
b0pAtM = Limit[b0p[pp, m], pp -> m^2, Assumptions -> m > 0 && mu > 0];
Print["(1) B0(m^2) = ", InputForm[Simplify[b0AtM]], " ; expect -L + 2 - Pi/Sqrt[3] -> ",
  zeroQ[b0AtM - (-Log[m^2/mu^2] + 2 - Pi/Sqrt[3])]];
Print["(1) m^2 B0'(m^2) = ", InputForm[Simplify[m^2 b0pAtM]], " ; expect 2 Pi/(3 Sqrt[3]) - 1 -> ",
  zeroQ[m^2 b0pAtM - (2 Pi/(3 Sqrt[3]) - 1)], "  (numerically ", N[2 Pi/(3 Sqrt[3]) - 1], ")"];

(* (2) mu-independence at O(g^2): d/dln(mu) acts explicitly and through m^2(mu), mu dm^2/dmu = g^2/k4 *)
dLnMu[expr_] := mu D[expr, mu] + D[expr /. m -> Sqrt[msq], msq] (g^2/k4) /. msq -> m^2;
mp2 = m^2 - g^2/(2 k4) b0AtM;
res = 1 - g^2/(2 k4) b0pAtM;
Print["(2) d m_p^2/dln(mu) at O(g^2) = ", Simplify[SeriesCoefficient[dLnMu[mp2], {g, 0, 2}]], "  (expect 0)"];
Print["(2) d R/dln(mu) at O(g^2) = ", Simplify[SeriesCoefficient[dLnMu[res], {g, 0, 2}]], "  (expect 0)"];

(* (3) MS-bar route vs on-shell route.  This is algebra in B0, so B0 is kept as an unspecified function
   bb (bb' = B0'); boxes and triangles are common and drop out.  A numerical spot check with the explicit
   Package-X function follows.  Sigma = -g^2/(2 k4) (DeltaUV + B0) unrenormalized (Sigma0), -g^2/(2 k4) B0 (MS-bar). *)
xs = {s, t, u};
routes[bf_] := Module[{mMS2, treeMS, bubMS, r2, routeMS, sigma0, dZ, dmOS, sigmaOS, routeOS, mPhys1},
   (* MS-bar: m^2 = m_p^2 - SigmaMS(m_p^2) = m_p^2 + g^2/(2 k4) B0(m_p^2); R^2 = 1 + 2 SigmaMS'(m_p^2);
      the B0 in the loop is evaluated with m_p (the change is O(g^6)) *)
   mMS2 = mp^2 + g^2/(2 k4) bf[mp^2];
   treeMS = -g^2 Sum[1/(x - mMS2), {x, xs}];
   bubMS = g^4/(2 k4) Sum[bf[x]/(x - mp^2)^2, {x, xs}];
   r2 = 1 + 2 (-g^2/(2 k4) bf'[mp^2]);
   routeMS = Normal[Series[r2 (treeMS + bubMS), {g, 0, 4}]];
   (* on-shell: deltaZ = Sigma0'(m_p^2), deltam_os = -Sigma0(m_p^2) + deltaZ m_p^2,
      SigmaOS(p^2) = Sigma0(p^2) - deltaZ p^2 + deltam_os, vertex counterterm -I (3/2) deltaZ g *)
   sigma0[p2_] := -g^2/(2 k4) (deltaUV + bf[p2]);
   dZ = -g^2/(2 k4) bf'[mp^2];
   dmOS = -sigma0[mp^2] + dZ mp^2;
   sigmaOS[p2_] := sigma0[p2] - dZ p2 + dmOS;
   routeOS = Sum[-g^2/(x - mp^2) - g^2 sigmaOS[x]/(x - mp^2)^2 + 2 (3/2) dZ (-g^2/(x - mp^2)), {x, xs}];
   mPhys1 = g^4/(2 k4) Sum[(bf[x] - bf[mp^2] + 2 (x - mp^2) bf'[mp^2])/(x - mp^2)^2, {x, xs}];
   {Simplify[{sigmaOS[mp^2], sigmaOS'[mp^2]}], routeMS, routeOS, mPhys1}];
{osCond, rMS, rOS, mPh} = routes[bb];
Print["(3) Sigma_OS(m_p^2), Sigma_OS'(m_p^2) = ", osCond, "  (expect {0, 0})"];
Print["(3) MS-bar route - on-shell route = ", Simplify[rMS - rOS], "  (expect 0)"];
Print["(3) on-shell route - tree(m_p) - Eq. (20) (eq:Mphys) B0 terms = ",
  Simplify[rOS - (-g^2 Sum[1/(x - mp^2), {x, xs}]) - mPh], "  (expect 0)"];
(* numerical spot check with the explicit MS-bar B0 (m_p = 1, mu = 1/2, s = 25, t = -7.35) *)
numPt = {mp -> 1, s -> 25, t -> -147/20, u -> 4 - 25 + 147/20, g -> 1};
b0mp[p2_] := b0Expr /. {pp -> p2, mm -> mp};
mPhNum = routes[b0mp][[4]];
Print["(3) Eq. (20) (eq:Mphys) B0 terms at m_p = 1, s = 25, t = -7.35 with mu = 1/2, 1, 2: ",
  N[mPhNum /. numPt /. mu -> #, 15] & /@ {1/2, 1, 2}];

(* (4) mu-independence *)
Print["(4) d M_phys^(1)/d mu = ", zeroQ[D[routes[b0mp][[4]], mu]], " (expect True: no mu dependence)"];
gMS = -g^2 Sum[1/(x - m^2), {x, xs}] + g^4/(2 k4) Sum[b0[x, m]/(x - m^2)^2, {x, xs}];
Print["(4) d[M0(m(mu)) + M1(mu)]/dln(mu) at O(g^4) = ", zeroQ[SeriesCoefficient[dLnMu[gMS], {g, 0, 4}]], " (expect True)"];
