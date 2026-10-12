(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop phi phi -> phi phi and psi psibar -> phi phi with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (4); independent of FeynCalc.  Run in its own kernel: the patched (FeynCalc) and*)
(*unpatched FeynArts must not be loaded together.*)
(**)
(*CalcFeynAmp gives the amplitude M in terms of LoopTools' functions (A0, B0i, C0i, D0i), whose normalization makes*)
(*LoopTools' Delta the note's DeltaUV; PaVeReduce -> True reduces the tensor coefficients to scalar functions (FormCalc's*)
(*own reduction, independent of FeynCalc's TID).  The FeynRules couplings gc2L, gc2R are replaced by M$FACouplings.*)
(*(a) phi phi -> phi phi: compared symbolically with Eq. (13) (eq:M1).*)
(*(b) psi psibar -> phi phi: FormCalc writes the amplitude with the spinor chains <1|1|2> and <1|k3slash|2> (named F1, F2 in*)
(*    some order), its fermion line running from k[1] to k[2], i.e. reversed with respect to vbar(p2) ... u(p1); reversing a*)
(*    chain flips*)
(*    the sign of the vector term only, and the tree fixes the common phase: (4 Pi)^2 x (coefficient of <1|1|2>) = -a,*)
(*    (4 Pi)^2 x (coefficient of <1|k3|2>) = b, with a, b of scat_feyncalc.wl.  No gamma5 chain appears (parity).*)
(*(c) LoopTools values at Delta = 0 (MS-bar), m = mu = 1, M = 0.7, y = lambda = 1, the points of scat_feyncalc.wl; the*)
(*    Delta-dependence is checked against the counterterm diagrams of Eq. (5) (evaluating at Delta = 1 as well).*)
(*    Written to Src/results/scat_formcalc.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_formcalc.wl  (in its own kernel: the patched FeynArts of FeynCalc must not be loaded).  Interactive:  ~/hep/bin/wopen scat_formcalc.wl  (in its own kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirFC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelFC$ = FileNameJoin[{srcDirFC$, "generated", "PsYukawa_FA", "PsYukawa_FA"}];   (* FeynRules output, unpatched *)
workDirFC$ = CreateDirectory[];
SetDirectory[workDirFC$];   (* FormCalc writes its FORM files here *)
(* FormCalc's auxiliary denominators: IGram[x] = 1/x (inverse Gram determinant of the reduction), Den[p, m] = 1/(p - m),
   Den[p, m, d] = 1/(p - m)^d *)
denRulesFC$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
insertFC$[proc_] := InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], proc,
   InsertionLevel -> {Particles}, Model -> modelFC$, GenericModel -> modelFC$];


(* ::Section:: *)
(*(a) phi phi -> phi phi*)


diagAFC$ = insertFC$[{S[1], S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams (unpatched FeynArts)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagAFC$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampAFC$ = CalcFeynAmp[CreateFeynAmp[diagAFC$] /. M$FACouplings, Dimension -> D, PaVeReduce -> True];
exprAFC$ = ((Plus @@ ampAFC$) //. Subexpr[]) /. denRulesFC$;
canonAFC$ = {D0i[dd0, mphi^2, mphi^2, mphi^2, mphi^2, a_, b_, Mpsi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> d0M[Sort[{a, b}]],
   C0i[cc0, mphi^2, mphi^2, x_, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], C0i[cc0, mphi^2, x_, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x],
   C0i[cc0, x_, mphi^2, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], B0i[bb0, x_, Mpsi^2, Mpsi^2] :> b0M[x],
   B0i[bb0, x_, mphi^2, mphi^2] :> b0m[x]};
boxFFC$[x_, xp_] := (2 mphi^4 - x xp) d0M[Sort[{x, xp}]] + 2 (b0M[x] + b0M[xp]) + 2 (x - 2 mphi^2) c0M[x] + 2 (xp - 2 mphi^2) c0M[xp];
handAFC$ = 1/(4 Pi)^2 (lamphi^2/2 (b0m[S] + b0m[T] + b0m[U]) - 2 yps^4 (boxFFC$[S, T] + boxFFC$[T, U] + boxFFC$[U, S]));
Print["(a) loop functions in FormCalc's phi phi -> phi phi (canonical names): ",
  Union[Cases[exprAFC$ /. canonAFC$, _A0 | _A0i | _B0i | _C0i | _D0i | _b0M | _b0m | _c0M | _d0M, Infinity]]];
Print["(a) phi phi -> phi phi: number of diagrams (expect 9): ", Length[CreateFeynAmp[diagAFC$]],
  ";  M (FormCalc) - Eq. (13) = ", Simplify[((exprAFC$ /. canonAFC$) - handAFC$) /. U -> 4 mphi^2 - S - T /. d0M[l_] :> d0M[Sort[l]]],
  "  (expect 0)"];


(* ::Section:: *)
(*(b) psi psibar -> phi phi*)


ClearProcess[];   (* FormCalc refuses a second, different process in one session otherwise *)
diagBFC$ = insertFC$[{F[1], -F[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the 11 diagrams (unpatched FeynArts)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagBFC$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


treeBFC$ = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateTopologies[0, 2 -> 2], {F[1], -F[1]} -> {S[1], S[1]},
       InsertionLevel -> {Particles}, Model -> modelFC$, GenericModel -> modelFC$]] /. M$FACouplings, FermionChains -> VA];
ampBFC$ = CalcFeynAmp[CreateFeynAmp[diagBFC$] /. M$FACouplings, FermionChains -> VA, Dimension -> D, PaVeReduce -> True];
exprBFC$ = ((Plus @@ ampBFC$) //. Subexpr[]) /. denRulesFC$;
exprTreeFC$ = ((Plus @@ treeBFC$) //. Subexpr[]) /. denRulesFC$;
chainsFC$ = Abbr[];
(* the names F1, F2 are assigned per session: identify the scalar chain <1|1|2> and the vector chain <1|k3slash|2> *)
fScalar$ = First[Cases[chainsFC$, (f_ -> DiracChain[_Spinor, 1, _Spinor]) :> f]];
fVector$ = First[Cases[chainsFC$, (f_ -> DiracChain[_Spinor, 1, k[3], _Spinor]) :> f]];
Print["(b) psi psibar -> phi phi: number of diagrams (expect 11): ", Length[CreateFeynAmp[diagBFC$]],
  ";  spinor chains: ", InputForm[Select[chainsFC$, ! FreeQ[#, DiracChain] &]]];
Print["(b) chains in the loop amplitude (expect only ", fScalar$, ", ", fVector$, ": no gamma5 chain): ", Union[Cases[exprBFC$, _Mat, Infinity]]];
Print["(b) tree minus y^2 [1/(T-M^2) - 1/(U-M^2)] Mat[<1|k3|2>] = ", Simplify[exprTreeFC$ - yps^2 (1/(T - Mpsi^2) - 1/(U - Mpsi^2)) Mat[fVector$]],
  "  (expect 0)"];
cF1$ = Coefficient[exprBFC$, Mat[fScalar$]];
cF2$ = Coefficient[exprBFC$, Mat[fVector$]];


(* ::Subsubsection:: *)
(*Inspect: the coefficients of F1 and F2*)


If[$Notebooks,
  {cF1$, cF2$} // TraditionalForm
]


(* ::Section:: *)
(*(c) LoopTools values*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[1];
pointsFC$ = Flatten[Table[Module[{ss = rs^2, e = rs/2, pB, kB, tB, p2A, tA},
     pB = Sqrt[e^2 - (7/10)^2]; kB = Sqrt[e^2 - 1]; tB = (7/10)^2 + 1 - 2 (e^2 - pB kB c);
     p2A = ss/4 - 1; tA = -2 p2A (1 - c);
     {rs, c, ss, tB, tA}], {rs, {5/2, 5, 10}}, {c, {3/10, 9/10}}], 1];
coupFC$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1};
evalFC$[x_, ss_, tt_, uu_] := N[x /. coupFC$ /. {S -> N[ss], T -> N[tt], U -> N[uu]}];
valuesFC$[{rs_, c_, ss_, tB_, tA_}] := Module[{uB = 2 (7/10)^2 + 2 - ss - tB, uA = 4 - ss - tA},
   (4 Pi)^2 {-evalFC$[cF1$, ss, tB, uB], evalFC$[cF2$, ss, tB, uB], evalFC$[exprAFC$, ss, tA, uA]}];
SetDelta[0];
rowsFC$ = Table[Join[pt, valuesFC$[pt]], {pt, pointsFC$}];
SetDelta[1];
rowsDelta1FC$ = Table[valuesFC$[pt], {pt, pointsFC$}];
SetDelta[0];
(* Delta coefficient of the loops (in (4 Pi)^2 M) = minus that of the counterterms of Eq. (5):
   a: (M y^4/2) [1/(t - M^2) + 1/(u - M^2)],  b: -2 y^2 b0 - y^4 (t - 3M^2)/(2 (t - M^2)^2) + y^4 (u - 3M^2)/(2 (u - M^2)^2),
   with the tree b0 = y^2 [1/(t - M^2) - 1/(u - M^2)];  phi phi -> phi phi: 3 lambda^2/2 - 24 y^4 *)
ctDeltaFC$[{rs_, c_, ss_, tB_, tA_}] := Module[{t = tB, u = 2 (7/10)^2 + 2 - ss - tB, M = 7/10, b0},
   b0 = 1/(t - M^2) - 1/(u - M^2);
   N[{M/2 (1/(t - M^2) + 1/(u - M^2)), -2 b0 - (t - 3 M^2)/(2 (t - M^2)^2) + (u - 3 M^2)/(2 (u - M^2)^2), 3/2 - 24}]];
deltaCheckFC$ = Table[rowsDelta1FC$[[i]] - rowsFC$[[i, 6 ;; 8]] - ctDeltaFC$[pointsFC$[[i]]], {i, Length[pointsFC$]}];
Print["(c) [M(Delta = 1) - M(Delta = 0)] - (Delta coefficient from the counterterms), (a, b, M1_A) = ",
  Chop[deltaCheckFC$, 10^-12], "  (expect 0)"];
Print["(c) a, b (psi psibar -> phi phi) and (4 Pi)^2 M1 (phi phi -> phi phi), FormCalc + LoopTools, MS-bar: ", rowsFC$[[All, 6 ;; 8]]];


(* ::Subsubsection:: *)
(*Inspect: the values*)


If[$Notebooks,
  TableForm[rowsFC$ /. x_Real :> NumberForm[x, 10], TableHeadings -> {None, {"sqrt(s)", "cos", "s", "t_B", "t_A", "a", "b", "M1_A"}}]
]


resultsDirFC$ = FileNameJoin[{srcDirFC$, "results"}];
Quiet[CreateDirectory[resultsDirFC$]];
numStrFC$[x_] := ToString[CForm[N[x]]];
csvLinesFC$ = Prepend[StringRiffle[numStrFC$ /@ Flatten[{#[[1 ;; 5]], ReIm /@ #[[6 ;; 8]]}], ","] & /@ rowsFC$,
   "sqrts,costheta,s,t_B,t_A,re_a,im_a,re_b,im_b,re_mA,im_mA"];
Export[FileNameJoin[{resultsDirFC$, "scat_formcalc.csv"}], StringRiffle[csvLinesFC$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsFC$], " rows to results/scat_formcalc.csv"];
