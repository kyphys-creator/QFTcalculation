(* ::Package:: *)

(* ::Title:: *)
(*S-matrix element and scheme conversion for phi phi -> phi phi of phi^3 + phi^4: symbolic checks (note, App. H)*)


(* ::Text:: *)
(*Research note models/phi34, step (5), Eqs. (11)-(12) (eq:mpole, eq:Mphys) and App. H.  Package-X (through FeynHelpers)*)
(*supplies the MS-bar B0(p^2; m, m) as an explicit function; A0(m^2) = m^2 (1 - Log[m^2/mu^2]).*)
(**)
(*(1) B0(m^2) = -L + 2 - Pi/Sqrt[3] and m^2 B0'(m^2) = 2 Pi/(3 Sqrt[3]) - 1, L = Log[m^2/mu^2].*)
(*(2) m_p^2 = m^2 - [g^2 B0(m^2) + lambda A0(m^2)]/(2 (4 Pi)^2) and R = 1 - g^2 B0'(m^2)/(2 (4 Pi)^2) do not depend on mu at*)
(*    one loop, using mu dm^2/dmu = (g^2 + lambda m^2)/(4 Pi)^2.*)
(*(3) the A0/B0 part of M_phys from the MS-bar amplitude (R^2, m -> m_p) equals the on-shell-scheme computation (field and*)
(*    mass on shell, couplings MS-bar: vertex counterterms -I (deltag + 3/2 g deltaZ) and -I (deltalambda + 2 lambda deltaZ)),*)
(*    and both equal tree(m_p) + M1(m_p) + Delta M of Eq. (12).  C0 and D0 are common to both routes and drop out.*)
(*(4) at fixed m_p, d M_phys/dln(mu) = 0 at one loop with beta_g, beta_lambda (Eq. (7)); the MS-bar M0(m(mu)) + M1(mu) too.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file onshell_check.wl.  Interactive:  ~/hep/bin/wopen onshell_check.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];

k4 = (4 Pi)^2;
b0Expr = Module[{v = Series[(2 Pi)^(2 Epsilon) PaXEvaluate[I Pi^2 B0[pp, mm^2, mm^2]]/(2 Pi)^4, {Epsilon, 0, 0}]},
   Simplify[(SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma))/(I/k4) /. ScaleMu -> mu,
    mm > 0 && mu > 0]];
b0[p2_, mass_] := b0Expr /. {pp -> p2, mm -> mass};
b0p[p2_, mass_] := (D[b0Expr, pp] /. {pp -> p2, mm -> mass});
a0[mass_] := mass^2 (1 - Log[mass^2/mu^2]);
logRules = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
zeroQ[expr_] := Simplify[PowerExpand[expr /. logRules], m > 0 && mu > 0 && mp > 0] === 0;
xs = {s, t, u};


(* ::Section:: *)
(*(1) B0 and B0' at p^2 = m^2*)


b0AtM = Limit[b0[pp, m], pp -> m^2, Assumptions -> m > 0 && mu > 0];
b0pAtM = Limit[b0p[pp, m], pp -> m^2, Assumptions -> m > 0 && mu > 0];
Print["(1) B0(m^2) = -L + 2 - Pi/Sqrt[3]: ", zeroQ[b0AtM - (-Log[m^2/mu^2] + 2 - Pi/Sqrt[3])],
  ";  m^2 B0'(m^2) = 2 Pi/(3 Sqrt[3]) - 1: ", zeroQ[m^2 b0pAtM - (2 Pi/(3 Sqrt[3]) - 1)]];


(* ::Section:: *)
(*(2) pole mass and residue: mu-independence at one loop*)


(* d/dln(mu) at fixed bare quantities: explicit mu, and m^2 through gamma; the running of g, lambda inside an O(coupling^2)
   term is of higher order *)
gammaM = (g^2 + lam m^2)/k4;
dLnMuMS[expr_] := mu D[expr, mu] + (D[expr /. m -> Sqrt[msq], msq] /. msq -> m^2) gammaM;
mp2 = m^2 - (g^2 b0AtM + lam a0[m])/(2 k4);
res = 1 - g^2/(2 k4) b0pAtM;
Print["(2) d m_p^2/dln(mu) = ", Simplify[Normal[Series[dLnMuMS[mp2] /. {g -> kk g, lam -> kk^2 lam}, {kk, 0, 2}]] /. kk -> 1],
  ";  d R/dln(mu) = ", Simplify[Normal[Series[dLnMuMS[res] /. {g -> kk g, lam -> kk^2 lam}, {kk, 0, 2}]] /. kk -> 1], "  (expect 0, 0)"];


(* ::Subsubsection:: *)
(*Inspect: the pole mass and the residue*)


If[$Notebooks,
  TableForm[{{"m_p^2", TraditionalForm[mp2]}, {"R", TraditionalForm[res]}}]
]


(* ::Section:: *)
(*(3) MS-bar route vs on-shell route*)


(* B0 is kept as an unspecified function bb (bb' = B0') and A0(m_p^2) as a symbol aa; kk counts the loop order
   (g ~ kk, lambda ~ kk^2).  Unrenormalized B0 = DeltaUV + B0, A0 = m_p^2 DeltaUV + A0. *)
routes[bf_, af_] := Module[{rule = {g -> kk g, lam -> kk^2 lam}, mMS2, treeMS, m1MS, r2, routeMS, sigma0, dZ, dmOS,
    sigmaOS, dgt, dlt, routeOS, deltaM, formula},
   mMS2 = mp^2 + (g^2 bf[mp^2] + lam af)/(2 k4);
   treeMS = -g^2 Sum[1/(x - mMS2), {x, xs}] - lam;
   m1MS = (g^4 Sum[bf[x]/(2 (x - mp^2)^2), {x, xs}] +
      g^2 lam Sum[(bf[x] + 2 bf[mp^2])/(x - mp^2) + af/(2 (x - mp^2)^2), {x, xs}] + lam^2/2 Sum[bf[x], {x, xs}])/k4;
   r2 = 1 - g^2 bf'[mp^2]/k4;
   routeMS = Normal[Series[(r2 (treeMS + m1MS)) /. rule, {kk, 0, 4}]] /. kk -> 1;
   sigma0[p2_] := -(g^2 (deltaUV + bf[p2]) + lam (mp^2 deltaUV + af))/(2 k4);
   dZ = -g^2 bf'[mp^2]/(2 k4);
   dmOS = -sigma0[mp^2] + dZ mp^2;
   sigmaOS[p2_] := sigma0[p2] - dZ p2 + dmOS;
   dgt = 3 g lam deltaUV/(2 k4) + 3/2 g dZ;          (* deltag (MS-bar) + 3/2 g deltaZ *)
   dlt = 3 lam^2 deltaUV/(2 k4) + 2 lam dZ;         (* deltalambda (MS-bar) + 2 lambda deltaZ *)
   routeOS = -g^2 Sum[1/(x - mp^2), {x, xs}] - lam - g^2 Sum[sigmaOS[x]/(x - mp^2)^2, {x, xs}] +
     Sum[2 g/(x - mp^2) (g lam/2 (3 deltaUV + bf[x] + 2 bf[mp^2])/k4 - dgt), {x, xs}] +
     lam^2/2 Sum[deltaUV + bf[x], {x, xs}]/k4 - dlt;
   deltaM = g^2/(2 k4) Sum[2 g^2 bf'[mp^2]/(x - mp^2) - (g^2 bf[mp^2] + lam af)/(x - mp^2)^2, {x, xs}] + g^2 lam bf'[mp^2]/k4;
   formula = -g^2 Sum[1/(x - mp^2), {x, xs}] - lam + m1MS + deltaM;
   {Simplify[{sigmaOS[mp^2], sigmaOS'[mp^2]}], routeMS, routeOS, formula, deltaM}];
{osCond, rMS, rOS, rForm, dM} = routes[bb, aa];
Print["(3) Sigma_OS(m_p^2), Sigma_OS'(m_p^2) = ", osCond, "  (expect {0, 0})"];
Print["(3) MS-bar route - on-shell route = ", Simplify[rMS - rOS], "  (expect 0)"];
Print["(3) on-shell route - [tree(m_p) + M1(m_p) + Delta M of Eq. (12)] = ", Simplify[rOS - rForm], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the conversion term Delta M (B0 kept as a function bb, A0 as aa)*)


If[$Notebooks,
  TraditionalForm[dM]
]


(* ::Section:: *)
(*(4) mu-dependence*)


(* at fixed m_p, g = g(mu), lambda = lambda(mu): d/dln(mu) = explicit + beta_g d/dg + beta_lambda d/dlambda *)
betaG = 3 g lam/k4; betaL = 3 lam^2/k4;
dLnMuOS[expr_] := mu D[expr, mu] + D[expr, g] betaG + D[expr, lam] betaL;
b0mp[p2_] := b0Expr /. {pp -> p2, mm -> mp};
mPhys = routes[b0mp, a0[mp]][[4]];
Print["(4) d M_phys/dln(mu) at one loop (fixed m_p) = 0: ",
  zeroQ[Normal[Series[dLnMuOS[mPhys] /. {g -> kk g, lam -> kk^2 lam}, {kk, 0, 4}]] /. kk -> 1]];
mMS = -g^2 Sum[1/(x - m^2), {x, xs}] - lam + (g^4 Sum[b0[x, m]/(2 (x - m^2)^2), {x, xs}] +
     g^2 lam Sum[(b0[x, m] + 2 b0AtM)/(x - m^2) + a0[m]/(2 (x - m^2)^2), {x, xs}] + lam^2/2 Sum[b0[x, m], {x, xs}])/k4;
dLnMuFull[expr_] := dLnMuMS[expr] + D[expr, g] betaG + D[expr, lam] betaL;
Print["(4) d[M0(m(mu), g(mu), lambda(mu)) + M1(mu)]/dln(mu) at one loop = 0: ",
  zeroQ[Normal[Series[dLnMuFull[mMS] /. {g -> kk g, lam -> kk^2 lam}, {kk, 0, 4}]] /. kk -> 1]];
Print["(4) mu d(M1 + Delta M)/dmu at fixed couplings = (6 g^2 lam sum_x 1/(x - m_p^2) + 3 lam^2)/(4 Pi)^2: ",
  zeroQ[mu D[mPhys, mu] - (6 g^2 lam Sum[1/(x - mp^2), {x, xs}] + 3 lam^2)/k4]];
