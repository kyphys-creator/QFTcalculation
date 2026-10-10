(* ::Package:: *)

(* af6_feyncalc.wl -- one-loop phi phi -> phi phi in d = 6 at high energies with Package-X's analytic C0 and D0,
   for asymptotic freedom in scattering (research note, step (11)).

   M1 (MS-bar, note Eq. (22) (eq:M6); m = g = 1) is assembled from the d = 6 finite parts X_N = -2 T00 (note, App. H)
   of B00, C00, D00 in D = 4 - 2 Epsilon.  T00 is the MS-bar (LoopTools/COLLIER) value: FeynCalc's PaVe is normalized
   with d^D q/(I Pi^2), so T = P_0 + (EulerGamma + Log[Pi]) P_{-1} from its Laurent coefficients (note, Sec. 4).  With PaXC0Expand/PaXD0Expand -> True the C0 and D0 inside are
   explicit logarithms and dilogarithms, which are evaluated with 30 digits: COLLIER's box loses precision at s >> m^2
   (note, step (11)), so these values are the reference.  LoopTools (machine precision) is evaluated as a third tool.
   90-degree scattering at sqrt(s) = 2.5 * 4000^(k/40), k = 0 ... 64 (sqrt(s) = 2.5 ... 1.45e6), mu = 1 and mu = sqrt(s);
   LoopTools for k <= 40; plus sqrt(s) = 5, cos(theta) = 0.3, mu = 1 (step (8) regression).
   -> Src/results/af6_feyncalc.csv

   Usage:  wolframscript -file af6_feyncalc.wl *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];

srcDirAF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

finAF$[expr_] := SeriesCoefficient[expr, {Epsilon, 0, 0}] + (EulerGamma + Log[Pi]) SeriesCoefficient[expr, {Epsilon, 0, -1}];
(* the d = 6 MS-bar finite parts as functions of the invariants and mu (X_N = -2 T00) *)
b06AF$ = -2 finAF$[PaXEvaluate[PaVe[0, 0, {x}, {1, 1}]]] /. ScaleMu -> mu;
c06AF$ = -2 finAF$[PaXEvaluate[PaVe[0, 0, {1, 1, x}, {1, 1, 1}], PaXC0Expand -> True]] /. ScaleMu -> mu;
d06AF$ = -2 finAF$[PaXEvaluate[PaVe[0, 0, {1, 1, 1, 1, x, y}, {1, 1, 1, 1}], PaXD0Expand -> True, PaXC0Expand -> True]] /. ScaleMu -> mu;
Print["(a) leaf counts of B0^(6), C0^(6), D0^(6): ", LeafCount /@ {b06AF$, c06AF$, d06AF$}];
Print["(a) mu d/dmu of B0^(6), C0^(6), D0^(6) (note: -2 (1 - x/6), -1, 0): ",
  InputForm /@ Simplify[Normal /@ {mu D[b06AF$, mu], mu D[c06AF$, mu], mu D[d06AF$, mu]}]];

Print["(a) B0^(6)(1), C0^(6)(1,1,1), C0^(6)(1,1,5) at mu = 1 (step (10): -0.9819892067718, -0.1455982473842, -0.5746357444754 - 0.1597522094015 I): ",
  N[{b06AF$ /. {x -> 1, mu -> 1}, Normal[c06AF$] /. {x -> 1, mu -> 1}, Normal[c06AF$] /. {x -> 5, mu -> 1}}, 13]];
kAF$ = (4 Pi)^3;
amp1AF$[ss_, tt_, muv_] := Module[{uu = 4 - ss - tt, xs, val},
   xs = {ss, tt, uu};
   val = (d06AF$ /. {x -> ss, y -> tt}) + (d06AF$ /. {x -> ss, y -> uu}) + (d06AF$ /. {x -> tt, y -> uu}) +
     Sum[2 (c06AF$ /. x -> xx)/(xx - 1) + (b06AF$ /. x -> xx)/(2 (xx - 1)^2), {xx, xs}];
   N[Normal[val] /. mu -> muv, 30]/kAF$];

(* LoopTools: the same finite parts from its PaVe00 (Delta = 0, mu^2 = LToolsSetMudim) *)
ltX$[pave_, muv_] := -2 Chop[finAF$[LToolsEvaluate[pave, LToolsSetMudim -> muv^2]]];
amp1LT$[ss_, tt_, muv_] := Module[{uu = 4. - ss - tt, xs},
   xs = {ss, tt, uu};
   (ltX$[PaVe[0, 0, {1, 1, 1, 1, ss, tt}, {1, 1, 1, 1}], muv] + ltX$[PaVe[0, 0, {1, 1, 1, 1, ss, uu}, {1, 1, 1, 1}], muv] +
      ltX$[PaVe[0, 0, {1, 1, 1, 1, tt, uu}, {1, 1, 1, 1}], muv] +
      Sum[2 ltX$[PaVe[0, 0, {1, 1, xx}, {1, 1, 1}], muv]/(xx - 1) + ltX$[PaVe[0, 0, {xx}, {1, 1}], muv]/(2 (xx - 1)^2), {xx, xs}])/N[kAF$]];

kin$[rs_, ct_] := Module[{s = rs^2, p2}, p2 = s/4 - 1; {s, -2 p2 (1 - ct)}];
rows$ = {};
Do[Module[{rs = SetPrecision[25/10 4000^(k/40), 50], st, mus},
   st = kin$[rs, 0];
   Do[Module[{px = amp1AF$[st[[1]], st[[2]], muv], lt},
      lt = If[k <= 40, amp1LT$[N[st[[1]]], N[st[[2]]], N[muv]], Indeterminate];
      AppendTo[rows$, {k, rs, 0, muv, px, lt}]], {muv, {1, rs}}]], {k, 0, 64}];
Module[{st = kin$[5, 3/10]},
  AppendTo[rows$, {-1, 5, 3/10, 1, amp1AF$[st[[1]], st[[2]], 1], amp1LT$[N[st[[1]]], N[st[[2]]], 1.]}]];
Print["(b) all Package-X values numeric: ", And @@ (NumericQ[#[[5]]] & /@ rows$),
  ";  smallest precision ", Min[Precision[#[[5]]] & /@ rows$]];

num$[x_] := If[x === Indeterminate, "nan", ToString[NumberForm[N[x, 20], 20, NumberFormat -> (Row[{#1, If[#3 === "", "", "e" <> #3]}] &)]]];
csv$ = Prepend[StringRiffle[{ToString[#[[1]]], num$[#[[2]]], num$[#[[3]]], num$[#[[4]]], num$[Re[#[[5]]]], num$[Im[#[[5]]]],
       If[#[[6]] === Indeterminate, "nan", num$[Re[#[[6]]]]], If[#[[6]] === Indeterminate, "nan", num$[Im[#[[6]]]]]}, ","] & /@ rows$,
   "k,sqrts,costheta,mu,re_packagex,im_packagex,re_looptools,im_looptools"];
Quiet[CreateDirectory[FileNameJoin[{srcDirAF$, "results"}]]];
Export[FileNameJoin[{srcDirAF$, "results", "af6_feyncalc.csv"}], StringRiffle[csv$, "\n"] <> "\n", "Text"];
Print["(b) wrote ", Length[rows$], " rows to results/af6_feyncalc.csv"];
LToolsUnLoadLibrary[];
