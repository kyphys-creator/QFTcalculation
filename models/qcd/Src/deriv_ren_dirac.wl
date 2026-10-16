(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: D-dimensional Dirac algebra of the quark loop, the quark self-energy and the quark vertex*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1).*)
(*  app:ren 「クォークのループ (a4)。」 (R1): tr[g^mu (l+m) g^nu (l'+m)], its g_{mu nu} and k_mu k_nu contractions;*)
(*  app:ren 「クォークの自己エネルギー (c)。」 (R2): gamma^rho (k+m) gamma_rho = -(D-2) k + D m;*)
(*  app:vertex 「クォークの頂点。」 (R7): the (d1) numerator (gamma^rho l gamma^mu l gamma_rho, symmetric integration l gamma^mu l ->*)
(*      -(D-2)/D l^2 gamma^mu, (D-2)^2/D - (1 - xi) -> xi at D = 4) and the (d2) Dirac structure.*)
(*Each line prints OK or FAIL.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ren_dirac.txt.*)
(*Usage (from Src/): wolframscript -file deriv_ren_dirac.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_ren_dirac.wl.  Interactive:  ~/hep/bin/wopen deriv_ren_dirac.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;
chk[name_, x0_] := With[{x = Simplify[DiracSimplify[ExpandScalarProduct[FCI[x0]]]]}, Print[If[x === 0, "OK   ", "FAIL "], name, If[x === 0, "", {"  residual: ", InputForm[x]}]]];

(* ::Section:: *)
(*(a4) the quark loop: the trace and its contractions*)


tr = DiracSimplify[DiracTrace[GAD[mu].(GSD[l] + m).GAD[nu].(GSD[lp] + m)]];


(* ::Subsubsection:: *)
(*Inspect: the trace tr[g^mu (l+m) g^nu (l'+m)] in D dimensions*)


If[$Notebooks,
  tr
]


chk["tr[g^mu (l+m) g^nu (l'+m)] = 4[l^mu l'^nu + l^nu l'^mu - g^{mu nu}(l.l' - m^2)]",
  Simplify[ExpandScalarProduct[tr - 4 (FVD[l, mu] FVD[lp, nu] + FVD[l, nu] FVD[lp, mu] - MTD[mu, nu] (SPD[l, lp] - m^2))]]];
chk["g_{mu nu} tr = 4[(2-D) l.l' + D m^2]", Simplify[Contract[tr MTD[mu, nu]] - 4 ((2 - D) SPD[l, lp] + D m^2)]];
chk["k_mu k_nu tr = 4[2(k.l)(k.l') - k^2(l.l' - m^2)]",
  Simplify[ExpandScalarProduct[Contract[tr FVD[k, mu] FVD[k, nu]] - 4 (2 SPD[k, l] SPD[k, lp] - SPD[k, k] (SPD[l, lp] - m^2))]]];

(* ::Section:: *)
(*(c) the quark self-energy*)


chk["gamma^rho (k+m) gamma_rho = -(D-2) k + D m", Simplify[DiracSimplify[GAD[rho].(GSD[k] + m).GAD[rho]] - (-(D - 2) GSD[k] + D m)]];

(* ::Section:: *)
(*(d1), (d2) the quark vertex*)


chk["gamma^rho l gamma^mu l gamma_rho = -(D-2) l gamma^mu l",
  Simplify[DiracSimplify[GAD[rho].GSD[l].GAD[mu].GSD[l].GAD[rho] + (D - 2) GSD[l].GAD[mu].GSD[l]]]];
chk["l gamma^mu l = 2 l^mu lslash - l^2 gamma^mu", Simplify[DiracSimplify[GSD[l].GAD[mu].GSD[l] - 2 FVD[l, mu] GSD[l] + SPD[l, l] GAD[mu]]]];
chk["l l gamma^mu l l = l^4 gamma^mu", Simplify[DiracSimplify[GSD[l].GSD[l].GAD[mu].GSD[l].GSD[l] - SPD[l, l]^2 GAD[mu]]]];
(* symmetric integration l^mu l^alpha -> l^2 g^{mu alpha}/D in 2 l^mu lslash - l^2 gamma^mu *)
sym = Simplify[DiracSimplify[Contract[2 SPD[l, l] MTD[mu, al]/D GAD[al]] - SPD[l, l] GAD[mu]]];


(* ::Subsubsection:: *)
(*Inspect: l gamma^mu l after symmetric integration (l^mu l^al -> l^2 g^{mu al}/D)*)


If[$Notebooks,
  sym
]


chk["l gamma^mu l -> -(D-2)/D l^2 gamma^mu", Simplify[sym + (D - 2)/D SPD[l, l] GAD[mu]]];
chk["(d1) Feynman part (D-2)^2/D -> 1 at D=4 and total (D-2)^2/D - eta -> xi", Simplify[((D - 2)^2/D - (1 - xi)) /. D -> 4] - xi];
(* (d2) Dirac structure quoted in app:vertex *)
chk["(d2): gamma^s l gamma^r [g_{mu r} l_s - 2 g_{r s} l_mu + g_{s mu} l_r] = 2 l^2 gamma_mu + 2(D-2) lslash l_mu",
  Simplify[DiracSimplify[Contract[GAD[sg].GSD[l].GAD[rh] (MTD[mu, rh] FVD[l, sg] - 2 MTD[rh, sg] FVD[l, mu] + MTD[sg, mu] FVD[l, rh])]] -
    (2 SPD[l, l] GAD[mu] + 2 (D - 2) GSD[l] FVD[l, mu])]];