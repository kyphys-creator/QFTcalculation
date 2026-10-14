(* ::Package:: *)

(* ::Title:: *)
(*Step (4): renormalized one-loop q qbar -> Q Qbar and g g -> Q Qbar -- masters, counterterms, IR poles, xi, cross-checks*)


(* ::Text:: *)
(*Research note models/qcd, step (4), last stage (after scat_feyncalc.wl, scat_litered.wl, scat_formcalc.wl).  Compares with*)
(*Eqs. (16) (eq:irpole) and (17) (eq:colcorr).  m = mu = 1, s = 10, t = -3, g = 1, general xi; K = (4 Pi)^2.*)
(*(a) master integrals in the MS-bar normalization e^(eps gamma_E) int d^D l/(i pi^(D/2)): A0, B0 exactly in eps up to eps^2*)
(*    (Gamma functions, or Feynman-parameter integrals of ln^n Delta to 40 digits; needed because the IBP coefficients of*)
(*    the soft triangles contain 1/(D - 4)), C0 and D0 from LoopTools; A0, B0 also from LoopTools and Package-X, C0 from*)
(*    Package-X.  The FeynArts amplitude has I/(16 Pi^4) int d^D l, so W = sum (coefficient) x I Pi^2 x master is already*)
(*    in the MS-bar normalization (FeynHelpers returns (1/(i pi^2)) int d^D l; MS-bar = (2 pi)^(2 eps) e^(-eps(ln 4pi -*)
(*    gamma_E)) times that, which is how the LoopTools and Package-X values are converted).*)
(*(b) W = sum M0^* M1 = loops + counterterms + residues:  MS-bar counterterms of Eq. (7) with n_f = 6 (vertex factors 1 +*)
(*    delta, propagator -delta_3, -delta_2), the on-shell top mass counterterm delta_m^OS = -C_F (D-1)(D-2) A0/(2(D-3)m^2)*)
(*    times d/dm of the internal top line, the residues R_q - 1 = xi C_F/eps, R_Q - 1 (Eq. (5) at p^2 = m^2, exact in D),*)
(*    R_G - 1 = Pi_t(0) - delta_3 = -(2/3) T_F (D-2) A0/m^2 - delta_3.  The 1/eps^2 and 1/eps coefficients are compared*)
(*    with Eq. (16) built from the D-dimensional Born and colour correlations of scat_feyncalc.wl (b); the finite part must*)
(*    not depend on xi.  Colour: C_F -> (N^2 - 1)/(2N) before comparing (FeynCalc's SUNSimplify mixes C_A^3 and C_F forms).*)
(*(c) Feynman gauge, diagram by diagram: IBP route ((b) at xi = 1), TID route (scat_feyncalc.wl (d)) and FormCalc*)
(*    (scat_formcalc.wl), SU(3).*)
(*(d) unitarity of (A): Im W of the diagram groups with the two-particle intermediate states n = d dbar (the d-quark loop),*)
(*    u ubar (u loop + abelian u vertex), t tbar (t loop + abelian t vertex), g g (the rest) against (1/2) S_eps^-1 int dPhi_2*)
(*    sum M0^*(i->f) M0(i->n) M0(n->f) in D dims; the collinear (q1 || p1, p2) and Coulomb (q1 || k1) directions are*)
(*    subtracted, their residues integrated in D dims (int dOmega_(D-2)/(1 - cos) = Omega_(D-3) 2^(D-4) Gamma((D-4)/2)*)
(*    Gamma((D-2)/2)/Gamma(D-3)), the rest numerically in four dims.  Gluing FeynArts trees with spin sums misses the sign*)
(*    of the closed fermion line: sigma = -1 for the quark pairs (the d dbar cut, Im of the vacuum polarization, fixes it).*)
(*-> results/scat_mathematica.csv, results/scat_perdiagram.csv, results/scat_unitarity.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_eval.wl.  Interactive:  ~/hep/bin/wopen scat_eval.wl, then "Run All Code"; the Inspect cells run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirEV$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirEV$ = FileNameJoin[{srcDirEV$, "work", "scat"}];
resDirEV$ = FileNameJoin[{srcDirEV$, "results"}];
Quiet[CreateDirectory[resDirEV$]];
sv = 10; tv = -3; uv = 2 - sv - tv; m = 1;
FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k1, k1] = 1; SPD[k2, k2] = 1;
SPD[p1, p2] = sv/2; SPD[k1, k2] = (sv - 2)/2; SPD[p1, k1] = (1 - tv)/2; SPD[p2, k2] = (1 - tv)/2;
SPD[p1, k2] = (1 - uv)/2; SPD[p2, k1] = (1 - uv)/2;
famDefsEV$ = {
   "F1" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-p1 - p2 + k1, 1}},
   "F2" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-k1, 1}},
   "F3" -> {{0, 0}, {k1, 1}, {-p1 - p2 + k1, 1}, {-p1, 0}},
   "G1" -> {{0, 1}, {-p1, 1}, {-p1 + k1, 0}, {p2, 1}},
   "G2" -> {{0, 0}, {-p1, 0}, {-p1 + k1, 1}, {p2, 0}},
   "G3" -> {{0, 1}, {-p1, 1}, {p2, 1}, {p2 - k1, 0}},
   "G4" -> {{0, 0}, {-p1, 0}, {p2, 0}, {p2 - k1, 1}},
   "G5" -> {{0, 1}, {-k1, 0}, {-p1, 1}, {p2 - k1, 0}},
   "G6" -> {{0, 0}, {-k1, 1}, {-p1, 0}, {p2 - k1, 1}}};
famsEV$ = FCI[FCTopology[#[[1]], SFAD[{l + #[[1]], #[[2]]}] & /@ #[[2]], {l}, {p1, p2, k1}, {}, {}] & /@ famDefsEV$];
KK = (4 Pi)^2; TF = 1/2; nf = 6; nl = 5;
ep = Epsilon; ordEV$ = 2; Dd = 4 - 2 ep;
sun = CF -> (CA^2 - 1)/(2 CA);
Lms = Log[4 Pi] - EulerGamma;
msLT[x_] := Normal[Series[(2 Pi)^(2 ep) Exp[-ep Lms] LToolsEvaluate[x, LToolsFullResult -> True], {ep, 0, 0}]];
msPX[x_] := Normal[Series[(2 Pi)^(2 ep) Exp[-ep Lms] (PaXEvaluate[x, PaXC0Expand -> True] /. ScaleMu -> 1), {ep, 0, 0}]];
coefs[x_] := Table[Coefficient[x, ep, k], {k, -2, 0}];


(* ::Section:: *)
(*(a) master integrals*)


toPDEV$[x_] := FeynAmpDenominatorCombine[x /. StandardPropagatorDenominator[mom_, 0, mm_, {1, 1}] :> PropagatorDenominator[mom, Sqrt[-mm]]];
mToPaVeEV$[mJ[f_, n_]] := Module[{x = ToPaVe[FDS[toPDEV$[FCLoopFromGLI[GLI[f, n], famsEV$]], l], l]}, Simplify[x/(I Pi^2)]];
msA0[m2_] := Normal[Series[-Exp[ep EulerGamma] Gamma[ep - 1] m2^(1 - ep), {ep, 0, ordEV$}]];
logmEV$[d_?NumericQ] := If[d > 0, Log[d], Log[-d] - I Pi];
bIntEV$[p2_, m0_, m1_, n_] := Module[{x, del, roots},
   del = x m1 + (1 - x) m0 - x (1 - x) p2;
   roots = Sort[Re[Select[Cases[NSolve[del == 0, x, WorkingPrecision -> 40], {x -> r_} :> r], Abs[Im[#]] < 10^-30 && 0 < Re[#] < 1 &]]];
   NIntegrate[logmEV$[del]^n, Evaluate[Join[{x, 0}, roots, {1}]], WorkingPrecision -> 40, PrecisionGoal -> 25, MaxRecursion -> 60]];
msB0[p2_, m0_, m1_] := Which[
   m0 == 0 && m1 == 0 && p2 == 0, 0,
   m0 == 0 && m1 == 0, Normal[Series[Exp[ep EulerGamma] Gamma[ep] Gamma[1 - ep]^2/Gamma[2 - 2 ep] Exp[-ep If[p2 > 0, Log[p2] - I Pi, Log[-p2]]], {ep, 0, ordEV$}]],
   True, Module[{i = Table[bIntEV$[p2, m0, m1, n], {n, 1, ordEV$ + 1}]},
     Normal[Series[Exp[ep EulerGamma] Gamma[ep] (1 + Sum[(-ep)^n/n! i[[n]], {n, 1, ordEV$ + 1}]), {ep, 0, ordEV$}]]]];
masterValueEV$[x_] := Switch[Head[x], A0, msA0[x[[1]]], B0, msB0 @@ x, C0 | D0, Chop[msLT[x], 10^-13], _, $Failed];
redEV$ = <|"A" -> Get[FileNameJoin[{workDirEV$, "A", "ibp.m"}]], "B" -> Get[FileNameJoin[{workDirEV$, "B", "ibp.m"}]]|>;
mastersEV$ = Union[Cases[Join[redEV$["A"], redEV$["B"]][[All, 2]], _mJ, Infinity]];
mPaVeEV$ = Association[# -> mToPaVeEV$[#] & /@ mastersEV$];
mValEV$ = Association[KeyValueMap[#1 -> masterValueEV$[#2] &, mPaVeEV$]];
devEV$ = Flatten[Table[Switch[Head[mPaVeEV$[k]],
     A0 | B0, {Max[Abs[N[coefs[Normal[Series[mValEV$[k], {ep, 0, 0}]] - msLT[mPaVeEV$[k]]]]]], Max[Abs[N[coefs[Normal[Series[mValEV$[k], {ep, 0, 0}]] - msPX[mPaVeEV$[k]]]]]]},
     C0, {Max[Abs[N[coefs[mValEV$[k] - msPX[mPaVeEV$[k]]]]]]}, _, {}], {k, mastersEV$}]];
Print["(a) ", Length[mastersEV$], " masters ", Tally[Head /@ Values[mPaVeEV$]], ";  max |exact - LoopTools|, |exact - Package-X| (A0, B0), ",
  "|LoopTools - Package-X| (C0) over the eps^-2..eps^0 coefficients: ", Max[devEV$], "  (expect ~ 1e-15)"];


(* ::Subsubsection:: *)
(*Inspect: the masters as scalar integrals*)


If[$Notebooks,
  Normal[mPaVeEV$]
]


(* ::Section:: *)
(*(b) poles and finite parts*)


evalProcEV$[key_] := Module[{gl, tree, born, cc, w0, wm, redR, wd, a0, b0m, b1, db0, db1, rT, rU, rG, d1F, d2, d3, d1, dmOS, toD, bornD,
    wCT, wTot, beta, bb, bcoth, lnS, lt, lu, c, b0l, pred, diff, fin, n1},
   n1 = If[key === "A", 15, 46];
   gl = Table[Get[FileNameJoin[{workDirEV$, key, "d" <> ToString[i] <> ".m"}]], {i, n1}];
   {born, cc, w0, wm} = Get[FileNameJoin[{workDirEV$, key, "tree.m"}]];
   redR = Dispatch[(GLI[#[[1, 1]], #[[1, 2]]] -> (#[[2]] /. dd -> D)) & /@ redEV$[key]];
   (* each diagram as a Laurent series in eps *)
   wd = Table[Module[{w = FeynAmpDenominatorExplicit[gl[[i]] /. gS -> 1] /. redR, cM},
      w = Collect[ExpandScalarProduct[w], _mJ, Together];
      If[!FreeQ[w, l | GLI], Print["   (", key, ") diagram ", i, ": loop momentum or GLI left"]];
      Expand[Normal[Series[Sum[(Coefficient[w, k] /. D -> Dd) I Pi^2 mValEV$[k], {k, Union[Cases[w, _mJ, Infinity]]}], {ep, 0, 0}]]]], {i, n1}];
   a0 = msA0[1];
   b0m = (Dd - 2) a0/(2 (Dd - 3)); b1 = (a0 - 2 b0m)/2;
   db0 = -(Dd - 2) a0/(4 (Dd - 3)); db1 = -a0/2 + (Dd - 2) a0/(2 (Dd - 3));
   rT = CF (xi (Dd - 2) b1 + 2 (xi (Dd - 2) db1 + (Dd - 1 + xi) db0)) + xi CF/ep;
   rU = xi CF/ep;
   d1F = -(xi CF + (3 + xi) CA/4); d2 = -xi CF; d3 = CA (13/6 - xi/2) - 4/3 TF nf; d1 = CA (17/12 - 3 xi/4) - 4/3 TF nf;
   rG = -(2/3) TF (Dd - 2) a0 - d3/ep;
   dmOS = -CF (Dd - 1) (Dd - 2) a0/(2 (Dd - 3));
   toD[x_] := x /. D -> Dd;
   bornD = toD[born];
   wCT = If[key === "A",
     ((2 d1F - d3)/ep + rU + rT) bornD/KK,
     ((2 d1F - d2)/ep toD[w0["t"] + w0["u"]] + (d1 + d1F - d3)/ep toD[w0["s"]] + dmOS toD[wm] + (rG + rT) bornD)/KK];
   wCT = Expand[Normal[Series[wCT, {ep, 0, 0}]]];
   wTot = Chop[Expand[Total[wd] + wCT], 10^-12];
   beta = Sqrt[1 - 4 m^2/sv]; bb = Log[(1 + beta)/(1 - beta)];
   bcoth = (sv - 2 m^2)/(sv beta) (bb - I Pi);
   lnS = Log[1/sv] + I Pi; lt = Log[m/(m^2 - tv)]; lu = Log[m/(m^2 - uv)];
   c[i_, j_] := toD[cc[Sort[{i, j}]]];
   b0l = 11/3 CA - 4/3 TF nl;
   pred = (-If[key === "A", 2 CF, 2 CA] bornD/ep^2 + (2 lnS c[1, 2] + If[key === "A", -3 CF, -b0l] bornD - 2 bcoth c[3, 4] - 2 CF bornD +
         2 (c[1, 3] lt + c[1, 4] lu + c[2, 3] lu + c[2, 4] lt))/ep)/KK;
   pred = Expand[Normal[Series[pred, {ep, 0, 0}]]];
   diff = Expand[wTot - pred];
   Print["(b) (", key, ") max |K (W - Eq. (16))| over the 1/eps^2 and 1/eps coefficients (any N, xi): ",
    Max[Abs[N[Flatten[Table[CoefficientList[Numerator[Together[KK Coefficient[diff, ep, k] /. sun]], {CA, xi}], {k, {-2, -1}}]]]]], "  (expect 0)"];
   fin = Together[N[KK Coefficient[wTot, ep, 0]] /. sun];
   Print["(b) (", key, ") xi dependence of the finite part: max |coefficient| = ", Max[Abs[Flatten[CoefficientList[Numerator[Together[fin - (fin /. xi -> 0)]], {CA, xi}]]]], "  (expect 0)"];
   Print["(b) (", key, ") SU(3): K W = ", Chop[N[KK {Coefficient[wTot, ep, -2], Coefficient[wTot, ep, -1], Coefficient[wTot, ep, 0]} /. sun /. CA -> 3 /. xi -> 1], 10^-10],
    "  (1/eps^2, 1/eps, finite);  K Born(4) = ", N[born /. D -> 4 /. sun /. CA -> 3]];
   <|"wd" -> wd, "wTot" -> wTot, "pred" -> pred, "born" -> born|>];
resEV$ = <|"A" -> evalProcEV$["A"], "B" -> evalProcEV$["B"]|>;


(* ::Subsubsection:: *)
(*Inspect: the finite part of (A) as a function of N*)


If[$Notebooks,
  Collect[Chop[N[KK Coefficient[resEV$["A"]["wTot"], ep, 0]] /. sun], CA, Chop[#, 10^-10] &]
]


(* ::Section:: *)
(*(c) Feynman gauge: IBP route, TID route, FormCalc, diagram by diagram (SU(3))*)


su3[x_] := x /. sun /. CA -> 3 /. xi -> 1;
idxEV$[id_] := ToExpression /@ Characters[StringDrop[SymbolName[id], 2]];
fcToPaVeEV$ = {B0i[id_, p_, m1_, m2_] :> PaVe[Sequence @@ idxEV$[id], {p}, {m1, m2}],
   C0i[id_, a_, b_, c_, m1_, m2_, m3_] :> PaVe[Sequence @@ idxEV$[id], {a, b, c}, {m1, m2, m3}],
   D0i[id_, a_, b_, c_, d_, e_, f_, m1_, m2_, m3_, m4_] :> PaVe[Sequence @@ idxEV$[id], {a, b, c, d, e, f}, {m1, m2, m3, m4}]};
perDiagEV$ = Flatten[Table[Module[{tid, fc, ibp, n1 = Length[resEV$[key]["wd"]]},
     tid = Table[Get[FileNameJoin[{workDirEV$, key, "tid_" <> ToString[i] <> ".m"}]], {i, n1}];
     fc = Get[FileNameJoin[{workDirEV$, key, "formcalc.m"}]][[2]];
     Table[Module[{vi = su3[resEV$[key]["wd"][[i]]], vt, vf},
       vt = Expand[msLT[su3[tid[[i]] /. gS -> 1] /. D -> Dd]];
       vf = Expand[msLT[fc[[i]] /. fcToPaVeEV$ /. Dminus4 -> -2 ep]];
       {key, i, N[KK coefs[vi]], N[KK coefs[vt - vi]], N[KK coefs[vf - vi]]}], {i, n1}]], {key, {"A", "B"}}], 1];
Print["(c) Feynman gauge, ", Length[perDiagEV$], " diagrams: max |K (TID - IBP)| = ", Max[Abs[Flatten[perDiagEV$[[All, 4]]]]],
  ",  max |K (FormCalc - IBP)| = ", Max[Abs[Flatten[perDiagEV$[[All, 5]]]]], "  (all eps orders; expect ~ 1e-12)"];


(* ::Section:: *)
(*(d) unitarity of (A)*)


cutsEV$ = Get[FileNameJoin[{workDirEV$, "A", "cuts.m"}]];
rs = Sqrt[sv]; en = rs/2; pk = Sqrt[en^2 - 1]; cth = (en - 4/rs)/pk; sth = Sqrt[1 - cth^2];
pintEV$ = 2 Pi^((dD - 2)/2)/Gamma[(dD - 2)/2] 2^(dD - 4) Gamma[(dD - 4)/2] Gamma[(dD - 2)/2]/Gamma[dD - 3];
cutValEV$[key_, mn_, axis_, ident_] := Module[{f, qq, sing = {}, h, rem, ang, ps, tot, c1, cchi, cp, ph},
   qq = Sqrt[en^2 - mn^2];
   f = Together[cutsEV$[key] /. {CA -> 3, CF -> 4/3} /. {qp1 -> (rs/2) (en - qq c1), qp2 -> (rs/2) (en + qq c1), qk1 -> en en - qq pk cchi}];
   If[PossibleZeroQ[Denominator[f] /. {c1 -> 1, cchi -> cth}], AppendTo[sing, {1 - c1, Together[(1 - c1) f] /. {c1 -> 1, cchi -> cth}}]];
   If[PossibleZeroQ[Denominator[f] /. {c1 -> -1, cchi -> -cth}], AppendTo[sing, {1 + c1, Together[(1 + c1) f] /. {c1 -> -1, cchi -> -cth}}]];
   If[PossibleZeroQ[Denominator[f] /. {cchi -> 1, c1 -> cth}], AppendTo[sing, {1 - cchi, Together[(1 - cchi) f] /. {cchi -> 1, c1 -> cth}}]];
   h = (f /. D -> 4) - Sum[(s[[2]] /. D -> 4)/s[[1]], {s, sing}];
   ang = If[axis === "k", {cchi -> cp, c1 -> cth cp + sth Sqrt[1 - cp^2] Cos[ph]}, {c1 -> cp, cchi -> cth cp + sth Sqrt[1 - cp^2] Cos[ph]}];
   rem = NIntegrate[Evaluate[h /. ang], {cp, -1, 1}, {ph, 0, 2 Pi}, WorkingPrecision -> 20, PrecisionGoal -> 12, MaxRecursion -> 30];
   ps = (4 Pi)^(-ep) Exp[ep EulerGamma] (2 Pi)^(2 - dD) qq^(dD - 3)/(4 rs) If[ident, 1/2, 1];
   tot = (1/2) ps (Sum[s[[2]] /. D -> dD, {s, sing}] pintEV$ + rem) /. dD -> 4 - 2 ep;
   {Length[sing], Chop[N[KK CoefficientList[Normal[Series[tot ep^2, {ep, 0, 2}]], ep], 15], 10^-12]}];
groupsEV$ = <|"dd" -> {8}, "uu" -> {3, 8}, "tt" -> {1, 13}, "gg" -> {2, 4, 5, 6, 7, 14, 15}|>;
unitEV$ = Table[Module[{cv = cutValEV$[k, If[k === "tt", 1, 0], If[k === "tt", "k", "z"], k === "gg"], sg = If[k === "gg", 1, -1], im},
    im = Im[N[KK coefs[su3[Total[resEV$["A"]["wd"][[groupsEV$[k]]]]]]]];
    {k, cv[[1]], sg cv[[2]], im, sg cv[[2]] - im}], {k, Keys[groupsEV$]}];
Do[Print["(d) n = ", u[[1]], " (", u[[2]], " singular directions): sigma (1/2) cut = ", u[[3]], ";  Im K W(group) = ", u[[4]],
   ";  difference ", Chop[u[[5]], 10^-9]], {u, unitEV$}];


(* ::Section:: *)
(*Results*)


strEV$[x_] := ToString[CForm[N[x]]];
Export[FileNameJoin[{resDirEV$, "scat_mathematica.csv"}], StringRiffle[Prepend[Flatten[Table[Module[{w = su3[resEV$[key]["wTot"]], p = su3[resEV$[key]["pred"]]},
       Table[StringRiffle[{key, ToString[k], strEV$[Re[KK Coefficient[w, ep, k]]], strEV$[Im[KK Coefficient[w, ep, k]]],
          strEV$[Re[KK Coefficient[p, ep, k]]], strEV$[Im[KK Coefficient[p, ep, k]]]}, ","], {k, -2, 0}]], {key, {"A", "B"}}]],
    "process,eps_power,re_KW,im_KW,re_K_pred,im_K_pred"], "\n"] <> "\n", "Text"];
Export[FileNameJoin[{resDirEV$, "scat_perdiagram.csv"}], StringRiffle[Prepend[Table[StringRiffle[Join[{r[[1]], ToString[r[[2]]]},
       strEV$ /@ Flatten[ReIm[r[[3]]]], strEV$ /@ {Max[Abs[r[[4]]]], Max[Abs[r[[5]]]]}], ","], {r, perDiagEV$}],
    "process,diagram,re_m2,im_m2,re_m1,im_m1,re_0,im_0,max_tid_minus_ibp,max_formcalc_minus_ibp"], "\n"] <> "\n", "Text"];
Export[FileNameJoin[{resDirEV$, "scat_unitarity.csv"}], StringRiffle[Prepend[Table[StringRiffle[Join[{u[[1]]},
       strEV$ /@ u[[3]], strEV$ /@ u[[4]]], ","], {u, unitEV$}],
    "state,cut_m2,cut_m1,cut_0,imW_m2,imW_m1,imW_0"], "\n"] <> "\n", "Text"];
Print["(e) wrote results/scat_mathematica.csv, scat_perdiagram.csv, scat_unitarity.csv"];
