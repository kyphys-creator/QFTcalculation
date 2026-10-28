(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the Nielsen identity of the h two-point function in numbers (abelian Higgs model), without FeynCalc*)


(* ::Text:: *)
(*Reads results/nielsen_k.m (K x the Nielsen functions K_h, K_hh from nielsen_feyncalc.wl, with the C0 of the repeated*)
(*propagator kept) and results/oneloop_sigma.m (K x Sigma^H from step (3)).  With the loop functions of Package-X*)
(*(40 digits) at the benchmark (e = 1/2, MA = 1, MH = 5/2, mu = 1):*)
(*  (a) C0(0, p^2, p^2; x, x, x) against the integration-by-parts relation used in nielsen_feyncalc.wl;*)
(*  (b) d(K Sigma^H)/d xi (MS-bar finite part, central difference in xi of the step (3) result) against*)
(*      2 (p^2 - MH^2) K K_hh (finite part, C0 from Package-X) for xi = 1/2, 1, 3 and p^2 = 0, 1, 3, MH^2, 10 (below*)
(*      and above the threshold 4 xi MA^2); the derivative vanishes at p^2 = MH^2;*)
(*  (c) results/nielsen.csv.*)
(*Batch: wolframscript -file nielsen_numeric.wl*)


srcDirNN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirNN$ = FileNameJoin[{srcDirNN$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;
plain$[y_] := y /. {s_Symbol /; SymbolName[s] === "A0" :> A0, s_Symbol /; SymbolName[s] === "B0" :> B0,
    s_Symbol /; SymbolName[s] === "C0" :> C0};
nk$ = Association[Map[plain$, Get[FileNameJoin[{resDirNN$, "nielsen_k.m"}]]]];
sig$ = Association[Map[plain$, Get[FileNameJoin[{resDirNN$, "oneloop_sigma.m"}]]]];
kSigH$ = Total[sig$["H"][[1]]] + Total[sig$["H"][[2]]];

expandEp$[y_] := Series[y /. A0[m2_] :> m2/ep + a0f[m2] /. B0[pp_, a_, b_] :> 1/ep + b0f[pp, a, b] /. C0[c__] :> c0f[c] /.
     D -> 4 - 2 ep, {ep, 0, 0}];
finOf$[y_] := SeriesCoefficient[expandEp$[y], 0];

Get["X`"];
dropEps$[r_] := r /. {sy_Symbol /; SymbolName[sy] === "Eps" :> Infinity};
muSub$ = {sy_Symbol /; SymbolName[sy] === "Mu" :> 1};
pxB0$[pp_, a_, b_] := N[dropEps$[LoopRefine[PVB[0, 0, pp, Sqrt[a], Sqrt[b]]]] /. muSub$, 40];
pxC0$[a1_, a2_, a3_, m1_, m2_, m3_] := N[LoopRefine[PVC[0, 0, 0, a1, a2, a3, Sqrt[m1], Sqrt[m2], Sqrt[m3]]], 40];
evalPX$[y_, vals_] := N[y /. vals /. {a0f[m2_] :> m2 (1 - Log[m2]), b0f[pp_, a_, b_] :> pxB0$[pp, a, b],
      c0f[c__] :> pxC0$[c]}, 30];

bench$ = {MA -> 1, MH -> 5/2, v -> 2};
(* printing: numbers known to be zero within their accuracy as a bound *)
bnd$[y_] := If[y == 0, "< 10^-" <> ToString[Floor[Accuracy[y]]], N[y, 3]];
cx$[y_] := Chop[N[y, 14], 10^-12];
xis$ = {1/2, 1, 3};
p2s$ = {0, 1, 3, 25/4, 10};


(* ::Section:: *)
(*(a) the C0 of the repeated propagator*)


Do[Module[{xm = xv, c0, ibp},
    c0 = pxC0$[0, pp, pp, xm, xm, xm];
    ibp = N[(pxB0$[pp, xm, xm] - 1 - (xm (1 - Log[xm]))/xm)/(4 xm - pp), 30];
    Print["(a) xi = ", xv, ", p^2 = ", pp, ": C0(0, p^2, p^2; x, x, x) = ", cx$[c0], ", IBP ", cx$[ibp],
      ", difference ", bnd$[Abs[c0 - ibp]]]],
  {xv, xis$}, {pp, {0, 1, 3, 10}}];


(* ::Section:: *)
(*(b) d Sigma^H/d xi against 2 (p^2 - MH^2) K_hh*)


finSig$ = finOf$[kSigH$];
finKhh$ = finOf$[nk$["Khh"]];
hStep$ = 10^-12;
rows$ = {};
Do[Module[{vals, dSig, khh, diff},
    vals = Join[bench$, {p2 -> pp}];
    dSig = (evalPX$[finSig$, Join[vals, {xi -> xv + hStep$}]] - evalPX$[finSig$, Join[vals, {xi -> xv - hStep$}]])/(2 hStep$);
    khh = evalPX$[finKhh$, Join[vals, {xi -> xv}]];
    diff = dSig - 2 (pp - 25/4) khh;
    Print["(b) xi = ", xv, ", p^2 = ", pp, ": d(K Sigma^H)/d xi = ", cx$[dSig], ";  K K_hh = ", cx$[khh],
      ";  difference ", bnd$[Abs[diff]]];
    AppendTo[rows$, {xv, pp, Re[dSig], Im[dSig], Re[khh], Im[khh], Abs[diff]}]],
  {xv, xis$}, {pp, p2s$}];
Print["(b) largest |d(K Sigma^H)/d xi - 2 (p^2 - MH^2) K K_hh| ", bnd$[Max[Last /@ rows$]],
  ";  largest |d(K Sigma^H)/d xi| at p^2 = MH^2 ", bnd$[Max[Abs[#[[3]] + I #[[4]]] & /@ Select[rows$, #[[2]] == 25/4 &]]]];
Print["(b) K K_h (finite part) = ", Table[cx$[evalPX$[finOf$[nk$["Kh"]], Join[bench$, {xi -> xv}]]], {xv, xis$}],
  " for xi = ", xis$, "  ((e^2 v/2) ln(xi MA^2/mu^2) = ln(xi)/4)"];


(* ::Section:: *)
(*(c) output*)


Export[FileNameJoin[{resDirNN$, "nielsen.csv"}],
  Map[If[StringQ[#], #, ToString[CForm[Chop[N[#, 16], 10^-14]]]] &,
   Prepend[rows$, {"xi", "p2", "Re_dKSigmaH_dxi", "Im_dKSigmaH_dxi", "Re_KKhh", "Im_KKhh", "abs_difference"}], {2}], "CSV"];
Print["(c) written results/nielsen.csv"];
