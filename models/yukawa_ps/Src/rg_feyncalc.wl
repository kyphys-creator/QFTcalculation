(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the mu-dependence of the one-loop amplitudes and self-energies with FeynArts + FeynCalc (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (7).  The MS-bar amplitudes of step (4) (built here exactly as in scat_feyncalc.wl) and*)
(*the self-energies of step (3) (as in oneloop_feyncalc.wl):*)
(*(a) the explicit mu-dependence, mu d/dmu at fixed parameters, from Package-X with a symbolic scale (C0, D0 are UV finite and*)
(*    mu-independent; they are kept as symbols):  (4 Pi)^2 M1 of phi phi -> phi phi gives 3 lambda^2 - 48 y^4;  psi psibar ->*)
(*    phi phi gives d a/d ln mu = y^4 M S+, d b/d ln mu = y^4 sum_x sigma_x [2 M^2/(x - M^2)^2 - 5/(x - M^2)] (S+ = 1/(t-M^2) +*)
(*    1/(u-M^2), sigma_t = 1, sigma_u = -1; note App. rgfit);  (4 Pi)^2 Sigma_phi(m^2) gives -(lambda m^2 + 4 y^2 m^2 - 8 y^2 M^2)*)
(*    = -(4 Pi)^2 gamma_m, (4 Pi)^2 (Sigma_V + Sigma_S)(M^2) gives y^2 = -(4 Pi)^2 gamma_M/M (Eqs. (15), (17)).*)
(*(b) values at the six points of step (4) for mu = 1/2, 1, 2 from Package-X (ScaleMu) and LoopTools (LToolsSetMudim)*)
(*    -> Src/results/rg_feyncalc.csv;  Sigma_phi(m^2), Sigma_V(M^2), Sigma_S(M^2) for the same mu -> results/rg_feyncalc_pole.csv.*)
(*m = 1, M = 0.7, y = lambda = 1.  Normalization as in scat_feyncalc.wl ((4 Pi)^2 M = A/Pi^2) and oneloop_feyncalc.wl*)
(*(Sigma = i V, (4 Pi)^2 Sigma = I (4 Pi)^2 msbar[V]).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file rg_feyncalc.wl  (run generate_PsYukawa.wl first).  Interactive:  ~/hep/bin/wopen rg_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
FCSetDiracGammaScheme["NDR"];
SetOptions[DiracSimplify, ToDiracGamma67 -> False, DiracSubstitute67 -> True];

srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirRG$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRG$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirRG$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRG$, "PsYukawa_FA"}], Quiet -> True];
modelRG$ = FileNameJoin[{modelTmpDirRG$, "PsYukawa_FA", "PsYukawa_FA"}];
insertRG$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelRG$, GenericModel -> modelRG$];
tops22$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}];
tops11$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
chiral$ = {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
conv22$[diags_] := FCFAConvert[CreateFeynAmp[diags, PreFactor -> -I] /. M$FACouplings, IncomingMomenta -> {p1, p2},
    OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
    DropSumOver -> True] /. chiral$;
conv11$[diags_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1] /. M$FACouplings,
    IncomingMomenta -> {p}, OutgoingMomenta -> {p}, LoopMomenta -> {q}, ChangeDimension -> D, List -> False, SMP -> False,
    DropSumOver -> True] /. chiral$;
reduceRG$[x_] := FCE[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], q, ToPaVe -> True]]];


(* ::Section:: *)
(*Diagrams*)


diagA$ = insertRG$[tops22$, {S[1], S[1]} -> {S[1], S[1]}];
diagB$ = insertRG$[tops22$, {F[1], -F[1]} -> {S[1], S[1]}];
diagPhi$ = insertRG$[tops11$, {S[1]} -> {S[1]}];
diagPsi$ = insertRG$[tops11$, {F[1]} -> {F[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams (9 for phi phi -> phi phi, 11 for psi psibar -> phi phi, 2 + 1 self-energies)*)


If[$Notebooks,
  Join @@ (Show[#, ImageSize -> 560] & /@ Render[Paint[#, ColumnsXRows -> {6, 2}, Numbering -> Simple, DisplayFunction -> Identity]] & /@
    {diagA$, diagB$, diagPhi$, diagPsi$})
]


(* ::Section:: *)
(*Amplitudes (as in scat_feyncalc.wl and oneloop_feyncalc.wl)*)


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, mphi, mphi, mphi, mphi];
ampA$ = Total[reduceRG$ /@ conv22$[diagA$]];
FCClearScalarProducts[];

SetMandelstam[s, t, u, p1, p2, -k1, -k2, Mpsi, Mpsi, mphi, mphi, Dimension -> D];
vu$ = Spinor[-Momentum[p2, D], Mpsi, 1] . Spinor[Momentum[p1, D], Mpsi, 1];
vku$ = Spinor[-Momentum[p2, D], Mpsi, 1] . GSD[k1] . Spinor[Momentum[p1, D], Mpsi, 1];
toBasis$[x_] := Module[{y = FCReplaceMomenta[FCI[x], {k2 -> p1 + p2 - k1}], c1, c2, rest},
   y = DiracSimplify[DiracOrder[DiracSimplify[y], {p2, k1, p1}]];
   y = Expand[FCE[y]] /. {FCE[vu$] -> sVU, FCE[vku$] -> sVKU};
   c1 = Coefficient[y, sVU]; c2 = Coefficient[y, sVKU]; rest = Simplify[y - c1 sVU - c2 sVKU];
   If[rest =!= 0, Print["WARNING: structure outside the basis: ", rest]];
   {c1, c2}];
abLoop$ = Total[Table[toBasis$[reduceRG$[x]]/Pi^2, {x, conv22$[diagB$]}]];   (* {a, b} with (4 Pi)^2 M = A/Pi^2 *)
FCClearScalarProducts[];

ampPhi$ = reduceRG$[conv11$[diagPhi$]] /. SPD[p] -> pp;
ampPsi$ = reduceRG$[conv11$[diagPsi$]] /. SPD[p] -> pp;
psiStruct$ = Module[{x = Expand[FCI[ampPsi$]], g = DiracGamma[Momentum[p, D], D], a},
   a = Coefficient[x, g]; {FCE[a], FCE[Simplify[x - a g]]/Mpsi}];      (* Sigma_psi = pslash Sigma_V + M Sigma_S *)
Print["numbers of diagrams (expect 9, 11, 2, 1): ", Length /@ {conv22$[diagA$], conv22$[diagB$], CreateFeynAmp[diagPhi$], CreateFeynAmp[diagPsi$]}];


(* ::Section:: *)
(*(a) explicit mu-dependence (Package-X, symbolic scale)*)


msbarRG$[0] = 0;
msbarRG$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
PaXEvaluate[B0[2, 1, 1]];
finiteSym$ = {C0[a__] :> c0Sym[a], D0[a__] :> d0Sym[a]};
(* mu d/dmu of the MS-bar finite part of A (C0, D0 kept as mu-independent symbols) *)
slopeRG$[x_] := Module[{red = FCE[PaVeReduce[FCI[x], PaVeAutoReduce -> True]] /. finiteSym$, v},
   v = msbarRG$[Quiet[PaXEvaluate[red], PaXEvaluate::tens]];
   Simplify[ScaleMu D[v, ScaleMu]]];
onShellA$ = {u -> 4 mphi^2 - s - t};
onShellB$ = {u -> 2 Mpsi^2 + 2 mphi^2 - s - t};
(* the MS-bar value of (4 Pi)^2 M is (4 Pi)^2 msbar[A] (A = the FeynCalc amplitude, = Pi^2 times the (a, b) coefficients) *)
slopeA$ = (4 Pi)^2 slopeRG$[ampA$] /. onShellA$;
Print["(a) mu d/dmu (4 Pi)^2 M1(phi phi -> phi phi) = ", Simplify[slopeA$], "  (expect 3 lamphi^2 - 48 yps^4)"];
slopeB$ = Simplify[(4 Pi)^2 slopeRG$[Pi^2 #] & /@ abLoop$ /. onShellB$];
handSlopeB$ = {yps^4 Mpsi (1/(t - Mpsi^2) + 1/(u - Mpsi^2)),
    yps^4 ((2 Mpsi^2/(t - Mpsi^2)^2 - 5/(t - Mpsi^2)) - (2 Mpsi^2/(u - Mpsi^2)^2 - 5/(u - Mpsi^2)))} /. onShellB$;
Print["(a) mu d/dmu (a, b)(psi psibar -> phi phi) - hand = ", Simplify[slopeB$ - handSlopeB$], "  (expect {0, 0})"];
slopePhi$ = Simplify[I (4 Pi)^2 slopeRG$[ampPhi$] /. pp -> mphi^2];
slopePsi$ = Simplify[I (4 Pi)^2 (slopeRG$[#] & /@ psiStruct$) /. pp -> Mpsi^2];
Print["(a) mu d/dmu (4 Pi)^2 Sigma_phi(m^2) = ", Expand[slopePhi$], "  (expect -(lamphi mphi^2 + 4 yps^2 mphi^2 - 8 yps^2 Mpsi^2))"];
Print["(a) mu d/dmu (4 Pi)^2 (Sigma_V, Sigma_S)(M^2) = ", slopePsi$, "  (expect {-yps^2, 2 yps^2}, sum yps^2)"];


(* ::Subsubsection:: *)
(*Inspect: the slopes*)


If[$Notebooks,
  TableForm[{{"phi phi -> phi phi", TraditionalForm[slopeA$]}, {"a", TraditionalForm[slopeB$[[1]]]}, {"b", TraditionalForm[Simplify[slopeB$[[2]]]]},
    {"Sigma_phi(m^2)", TraditionalForm[slopePhi$]}, {"Sigma_V, Sigma_S at M^2", TraditionalForm[slopePsi$]}}]
]


(* ::Section:: *)
(*(b) values for mu = 1/2, 1, 2*)


logRulesRG$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
numPXRG$ = {C0[a_, b_, c_, m0_, m1_, m2_] :> X`ScalarC0[N[a], N[b], N[c], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]]],
   D0[a_, b_, c_, d_, e_, f_, m0_, m1_, m2_, m3_] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]], Sqrt[N[m3]]]};
numArgsRG$[x_] := FCI[x] /. (h : A0 | B0 | C0 | D0)[args__] :> h @@ N[{args}] /. PaVe[i__, a_List, b_List] :> PaVe[i, N[a], N[b]];
(* x times fac: fac (4 Pi)^2 msbar[x] is the quantity; Package-X at ScaleMu = mu, LoopTools with mu^2 *)
pxRG$[0, _, _] = 0.; ltRG$[0, _, _] = 0.;
pxRG$[x_, fac_, mu_] := Chop[N[Simplify[fac (4 Pi)^2 msbarRG$[Quiet[PaXEvaluate[x /. numPXRG$], PaXEvaluate::tens] /. ScaleMu -> mu] /. logRulesRG$], 20], 10^-14];
ltRG$[x_, fac_, mu_] := Chop[N[fac (4 Pi)^2 msbarRG$[Quiet[LToolsEvaluate[numArgsRG$[x] /. D -> 4 - 2 Epsilon, LToolsSetMudim -> N[mu^2]], LToolsEvaluate::tens]]], 10^-14];
coupRG$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1};
musRG$ = {1/2, 1, 2};
pointsRG$ = Flatten[Table[Module[{ss = rs^2, e = rs/2, pB, kB, tB, p2A, tA},
     pB = Sqrt[e^2 - (7/10)^2]; kB = Sqrt[e^2 - 1]; tB = (7/10)^2 + 1 - 2 (e^2 - pB kB c);
     p2A = ss/4 - 1; tA = -2 p2A (1 - c);
     {rs, c, ss, tB, tA}], {rs, {5/2, 5, 10}}, {c, {3/10, 9/10}}], 1];
abNum$ = Pi^2 abLoop$ /. coupRG$;     (* the FeynCalc amplitude A of each coefficient; value (4 Pi)^2 msbar[A] *)
rowsRG$ = Flatten[Table[Module[{rs = pt[[1]], c = pt[[2]], ss = pt[[3]], tB = pt[[4]], tA = pt[[5]], ab, mA},
     ab = abNum$ /. {s -> ss, t -> tB, u -> 2 (7/10)^2 + 2 - ss - tB};
     mA = ampA$ /. coupRG$ /. {s -> ss, t -> tA, u -> 4 - ss - tA};
     {rs, c, mu, pxRG$[ab[[1]], 1, mu], pxRG$[ab[[2]], 1, mu], ltRG$[ab[[1]], 1, mu], ltRG$[ab[[2]], 1, mu],
      pxRG$[mA, 1, mu], ltRG$[mA, 1, mu]}], {pt, pointsRG$}, {mu, musRG$}], 1];
poleRowsRG$ = Table[Module[{phi = ampPhi$ /. coupRG$ /. pp -> 1, psi = psiStruct$ /. coupRG$ /. pp -> 49/100},
    {mu, pxRG$[phi, I, mu], ltRG$[phi, I, mu], pxRG$[psi[[1]], I, mu], ltRG$[psi[[1]], I, mu], pxRG$[psi[[2]], I, mu], ltRG$[psi[[2]], I, mu]}],
   {mu, musRG$}];

resultsDirRG$ = FileNameJoin[{srcDirRG$, "results"}];
Quiet[CreateDirectory[resultsDirRG$]];
numStrRG$[x_] := ToString[CForm[N[x]]];
writeCSV$[file_, header_, rows_] := Export[FileNameJoin[{resultsDirRG$, file}],
   StringRiffle[Prepend[StringRiffle[numStrRG$ /@ Flatten[{#[[1 ;; 3]], ReIm /@ #[[4 ;;]]}], ","] & /@ rows, header], "\n"] <> "\n", "Text"];
writeCSV$["rg_feyncalc.csv", "sqrts,costheta,mu,re_a_px,im_a_px,re_b_px,im_b_px,re_a_lt,im_a_lt,re_b_lt,im_b_lt,re_mA_px,im_mA_px,re_mA_lt,im_mA_lt", rowsRG$];
Export[FileNameJoin[{resultsDirRG$, "rg_feyncalc_pole.csv"}],
  StringRiffle[Prepend[StringRiffle[numStrRG$ /@ Flatten[{#[[1]], ReIm /@ #[[2 ;;]]}], ","] & /@ poleRowsRG$,
    "mu,re_sigphi_px,im_sigphi_px,re_sigphi_lt,im_sigphi_lt,re_sigV_px,im_sigV_px,re_sigV_lt,im_sigV_lt,re_sigS_px,im_sigS_px,re_sigS_lt,im_sigS_lt"], "\n"] <> "\n", "Text"];
Print["(b) wrote ", Length[rowsRG$], " rows to results/rg_feyncalc.csv and ", Length[poleRowsRG$], " rows to results/rg_feyncalc_pole.csv"];


(* ::Subsubsection:: *)
(*Inspect: the values*)


If[$Notebooks,
  TableForm[rowsRG$ /. x_Real :> NumberForm[x, 10], TableHeadings -> {None, {"sqrt(s)", "cos", "mu", "a PX", "b PX", "a LT", "b LT", "M1 PX", "M1 LT"}}]
]


(* ::Section:: *)
(*Cleanup*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirRG$, DeleteContents -> True];
