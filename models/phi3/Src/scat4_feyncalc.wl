(* ::Package:: *)

(* scat4_feyncalc.wl -- one-loop phi phi -> phi phi in d = 4 (research note, step (5)).

   (a) FeynArts diagrams from Src/generated/Phi3_FA: one loop, 2 -> 2, without tadpoles (cancelled by Y)
       and without external-leg corrections (truncated amplitude): 3 boxes, 6 triangles, 3 bubbles on
       the internal line.  With PreFactor -> 1 the sum of diagrams is A = i M (2 Pi)^D, i.e.
       M = -I A/(2 Pi)^D.  The amplitude is compared symbolically with the note's Eq. (17) (eq:M1),
         M1 = g^4/(4 Pi)^2 [ D0(s,t) + D0(s,u) + D0(t,u) + sum_x ( 2 C0(x)/(x - m^2) + B0(x)/(2 (x - m^2)^2) ) ],
       using FeynCalc's normalization (int d^D q = I Pi^2 PaVe).  For equal masses and p_i^2 = m^2,
       D0 depends only on its two invariants (symmetrically), C0 only on the off-shell invariant.
   (b) UV poles (Package-X) and the MS-bar mass counterterm on the internal lines,
       M_CT = -g^2 deltam sum_x 1/(x - m^2)^2 with deltam = g^2 DeltaUV/(2 (4 Pi)^2) (Eq. (7)).
   (c) the MS-bar amplitude M1 at the comparison points (m = g = mu = 1) with Package-X (B0 analytic,
       C0 and D0 from Package-X's numerical ScalarC0 and ScalarD0) and with LoopTools (LToolsEvaluate),
       written to Src/results/scat4_feyncalc.csv.  LoopTools' C0 is wrong below threshold for
       p^2 != 0 (step (3)), which affects the t- and u-channel triangles here.

   Usage:  wolframscript -file scat4_feyncalc.wl      (run generate_Phi3.wl first) *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirS4$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ---------- patched copy of the FeynRules-generated FeynArts model ---------- *)
modelTmpDirS4$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirS4$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirS4$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirS4$, "Phi3_FA"}], Quiet -> True];
modelS4$ = FileNameJoin[{modelTmpDirS4$, "Phi3_FA", "Phi3_FA"}];

(* ---------- (a) diagrams and amplitude ---------- *)
diagsS4$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelS4$, GenericModel -> modelS4$];
Print["(a) number of diagrams (expect 12: 3 boxes, 6 triangles, 3 bubbles): ", Length[CreateFeynAmp[diagsS4$]]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
ampS4$ = FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diagsS4$, Truncated -> True, PreFactor -> 1],
      IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D,
      List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2;
(* SetMandelstam leaves k2^2 as s + t + u - 3 m^2, which is m^2 on shell (s + t + u = 4 m^2) *)
(* canonical names, valid for equal masses m and p_i^2 = m^2 *)
canonS4$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x], B0[x_, m^2, m^2] :> b0[x]};
handS4$ = I Pi^2 gphi^4 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]] +
    Sum[2 c0[x]/(x - m^2) + b0[x]/(2 (x - m^2)^2), {x, {s, t, u}}]);
Print["(a) PaVe functions in the amplitude: ", Union[Cases[ampS4$, _D0 | _C0 | _B0, Infinity] /. canonS4$]];
Print["(a) A - I Pi^2 g^4 [Eq. (17) (eq:M1)] = ", Simplify[(ampS4$ /. canonS4$) - handS4$], "  (expect 0)"];

(* ---------- (b) UV poles and the MS-bar counterterm ---------- *)
(* M = -I A/(2 Pi)^D with D = 4 - 2 Epsilon *)
mBareS4$[ampValue_] := (2 Pi)^(2 Epsilon) (-I) ampValue/(2 Pi)^4;
mCTS4$ = -gphi^2 (gphi^2 (1/Epsilon - EulerGamma + Log[4 Pi])/(2 (4 Pi)^2)) Sum[1/(x - m^2)^2, {x, {s, t, u}}];
paxS4$ = PaXEvaluate[ampS4$ /. canonS4$ /. {b0[x_] :> B0[x, m^2, m^2]}];   (* c0, d0 are finite *)
poleS4$ = Simplify[SeriesCoefficient[mBareS4$[paxS4$], {Epsilon, 0, -1}]];
Print["(b) 1/eps coefficient of M (bare) = ", InputForm[poleS4$]];
Print["(b) 1/eps coefficient of M + M_CT = ", Simplify[poleS4$ + SeriesCoefficient[mCTS4$, {Epsilon, 0, -1}]], "  (expect 0)"];
(* MS-bar amplitude in terms of the MS-bar B0 of Eq. (10): compare with Eq. (17) (eq:M1) *)
mMSS4$ = Simplify[SeriesCoefficient[mBareS4$[paxS4$] + mCTS4$, {Epsilon, 0, 0}] /. ScaleMu -> mu];
b0MSS4$[x_] := Module[{v = Series[(2 Pi)^(2 Epsilon) PaXEvaluate[I Pi^2 gphi^2/2 B0[x, m^2, m^2]]/(2 Pi)^4, {Epsilon, 0, 0}]},
   (SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma))/(I gphi^2/(2 (4 Pi)^2)) /. ScaleMu -> mu];
handMSS4$ = gphi^4/(4 Pi)^2 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]] +
    Sum[2 c0[x]/(x - m^2) + b0MSS4$[x]/(2 (x - m^2)^2), {x, {s, t, u}}]);
Print["(b) MS-bar M - Eq. (17) (eq:M1) with the MS-bar B0 = ",
  Simplify[PowerExpand[mMSS4$ - handMSS4$ /. {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]}]], "  (expect 0)"];

(* ---------- (c) numerical values ---------- *)
pointsS4$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
(* Package-X's numerical functions take masses (FeynCalc: squared masses) and machine numbers *)
numRulesPXS4$ = {d0[{a_, b_}] :> X`ScalarD0[1., 1., 1., 1., N[a], N[b], 1., 1., 1., 1.],
   c0[x_] :> X`ScalarC0[1., 1., N[x], 1., 1., 1.]};
pxS4$[{rs_, ct_, ss_, tt_, uu_}] := Module[{v},
   v = mMSS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, mu -> 1, gphi -> 1};
   Chop[N[v /. numRulesPXS4$], 10^-18]];
(* the kinematics are passed as exact rationals: with machine-number prefactors in front of B0,
   LToolsEvaluate wrongly warns that the input contains tensor integrals (::tens) *)
ltS4$[{rs_, ct_, ss_, tt_, uu_}] := Module[{v},
   v = LToolsEvaluate[ampS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1}];
   Chop[SeriesCoefficient[mBareS4$[v] + (mCTS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1}), {Epsilon, 0, 0}]]];
rowsS4$ = Join[#, {pxS4$[#], ltS4$[#]}] & /@ pointsS4$;

resultsDirS4$ = FileNameJoin[{srcDirS4$, "results"}];
Quiet[CreateDirectory[resultsDirS4$]];
numStrS4$[x_] := ToString[CForm[N[x]]];
csvLinesS4$ = Prepend[
   StringRiffle[numStrS4$ /@ {#[[1]], #[[2]], #[[3]], #[[4]], #[[5]], Re[#[[6]]], Im[#[[6]]], Re[#[[7]]], Im[#[[7]]]}, ","] & /@ rowsS4$,
   "sqrts,costheta,s,t,u,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirS4$, "scat4_feyncalc.csv"}], StringRiffle[csvLinesS4$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsS4$], " rows to results/scat4_feyncalc.csv"];
Print["(c) M1 (Package-X) = ", rowsS4$[[All, 6]]];
Print["(c) M1 (LoopTools) = ", rowsS4$[[All, 7]]];

LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirS4$, DeleteContents -> True];
