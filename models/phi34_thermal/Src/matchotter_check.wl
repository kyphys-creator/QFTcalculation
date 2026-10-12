(* ::Package:: *)

(* ::Title:: *)
(*Step (8b): the single-field thermal potential against Matchotter (Matchete 0.6.0, dimensional reduction)*)


(* ::Text:: *)
(*Research note models/phi34_thermal, step (8).  The same model as dralgo_check.wl, written as a Lagrangian, is reduced with*)
(*DRMatch of Matchete 0.6.0 (the Matchotter module) at one loop.  Matchotter writes hbar for 1/(4 Pi)^2, Lambda_T = 4 Pi T*)
(*(DimensionalReduction.m), and the logarithm log(Lambdabar^2/Lambda_T^2); the poles 1/epsilon are removed by the MS-bar*)
(*counterterms.  (a) the one-loop 3D Lagrangian.  (b) the 4D potential T V_3(phi/sqrt(T)) against the analytic part of Eq. (13)*)
(*of the note, V + t phi + (T^2/24) M^2 - (M^4/64 Pi^2) L_b, with log(Lambdabar^2/Lambda_T^2) read as L_b (i.e.*)
(*Lambdabar = mubar e^gamma_E): the phi-derivative of the difference must vanish.  Writes Src/results/matchotter_check.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file matchotter_check.wl ; only the lines starting with (a), (b) are printed.  Interactive:  ~/hep/bin/wopen matchotter_check.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook.  Run in a kernel of its own (not together with DRalgo).  Without a front end Matchete prints "Loading failed!" for its logo; the computation is not affected.*)


(* ::Section:: *)
(*Setup*)


Quiet[Get["Matchete`"]];
srcDirMT$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Subsubsection:: *)
(*Inspect: the one-loop diagrams of the matching (hard modes in the loop; DRMatch evaluates them by the functional method), drawn by diagrams_thermal.wl*)


If[$Notebooks,
  With[{f = FileNameJoin[{srcDirMT$, "..", "figs", "diagrams", #}] & /@ {"oneloop.png"}},
    If[And @@ FileExistsQ /@ f, Column[Import /@ f, Spacings -> 2], "run diagrams_thermal.wl first (writes ../figs/diagrams/*.png)"]]
]


(* ::Section:: *)
(*(a) the model and DRMatch*)


DefineField[\[Phi], Scalar, Mass -> 0, SelfConjugate -> True];
DefineCoupling[mm, SelfConjugate -> True, EFTOrder -> 1];
DefineCoupling[gg, SelfConjugate -> True, EFTOrder -> 1];
DefineCoupling[tt, SelfConjugate -> True, EFTOrder -> 3];
DefineCoupling[lam, SelfConjugate -> True];
lagMT$ = FreeLag[\[Phi]] - tt[] \[Phi][] - mm[]^2/2 \[Phi][]^2 - gg[]/6 \[Phi][]^3 - lam[]/24 \[Phi][]^4;
ldrMT$ = Quiet[DRMatch[lagMT$, EFTOrder -> 4]];
(* static Euclidean Lagrangian: kinetic term + V_3; keep the field-dependent, non-derivative part *)
v3MT$ = Expand[ldrMT$ /. Field[_, _, _, {__}] -> 0 /. Field[\[Phi]0, Scalar, {}, {}] -> x] /. {
    Coupling[mm, {}, 1] -> Sqrt[msq], Coupling[gg, {}, 1] -> gg, Coupling[tt, {}, 3] -> tt, Coupling[lam, {}, 0] -> lam};
v3MT$ = v3MT$ - (v3MT$ /. x -> 0);
v3MS$ = Expand[v3MT$ /. {hbar -> 1/(16 Pi^2), \[CapitalLambda]\[CapitalTau] -> 4 Pi T, \[CapitalTau] -> T,
      Log[\[CapitalLambda]bar2/(16 Pi^2 T^2)] -> Lb, Log[\[CapitalLambda]bar2/\[CapitalLambda]\[CapitalTau]^2] -> Lb}];
v3MS$ = Expand[v3MS$ /. Log[\[CapitalLambda]bar2/(16 Pi^2 T^2)] -> Lb] /. \[Epsilon] -> Infinity;   (* MS-bar: drop 1/epsilon *)
coef$ = Table[Simplify[Coefficient[v3MS$, x, n]], {n, 1, 4}];
Print["(a) Matchotter V_3 coefficients of phi0^1..4 (MS-bar, hbar = 1/(4 Pi)^2, Lambda_T = 4 Pi T, log -> Lb): ", InputForm[coef$]];


(* ::Subsubsection:: *)
(*Inspect: the 3D Lagrangian of DRMatch*)


If[$Notebooks, NiceForm[ldrMT$]]


(* ::Section:: *)
(*(b) against Eq. (13)*)


V4MT$ = T v3MS$ /. x -> \[Phi]/Sqrt[T];
M2$ = msq + gg \[Phi] + lam \[Phi]^2/2;
VNoteAnalytic$ = tt \[Phi] + msq \[Phi]^2/2 + gg \[Phi]^3/6 + lam \[Phi]^4/24 + T^2/24 M2$ - M2$^2/(64 Pi^2) Lb;
diffMT$ = Simplify[D[VNoteAnalytic$ - V4MT$, \[Phi]]];
Print["(b) d/dphi [Eq. (13) without the zero-mode term - T V_3(phi/sqrt(T))] = ", diffMT$];
(* the same coefficients as DRalgo: lambda_3 = T (lam - 3 lam^2 Lb/(32 Pi^2)), gamma_3 = sqrt(T) (gg - 3 gg lam Lb/(32 Pi^2)),
   m_3^2 = msq + lam T^2/24 - (gg^2 + lam msq) Lb/(32 Pi^2), t_3 = (tt + gg T^2/24 - gg msq Lb/(32 Pi^2))/sqrt(T) *)
dr$ = {(tt + gg T^2/24 - gg msq Lb/(32 Pi^2))/Sqrt[T], (msq + lam T^2/24 - (gg^2 + lam msq) Lb/(32 Pi^2))/2,
   Sqrt[T] (gg - 3 gg lam Lb/(32 Pi^2))/6, T (lam - 3 lam^2 Lb/(32 Pi^2))/24};
Print["(b) coefficients minus those of DRalgo (dralgo_check.wl): ", Simplify[coef$ - dr$]];


(* ::Section:: *)
(*Output*)


(* CSV writer: a field is quoted only when it contains a comma or a quote *)
csvField$[x_] := Module[{s = Which[StringQ[x], x, NumberQ[x], ToString[N[x], CForm], True, ToString[x, InputForm]]},
   If[StringContainsQ[s, "," | "\""], "\"" <> StringReplace[s, "\"" -> "\"\""] <> "\"", s]];
writeCSV$[file_, rows_] := Export[file, StringRiffle[StringRiffle[csvField$ /@ #, ","] & /@ rows, "\n"] <> "\n", "Text"];
writeCSV$[FileNameJoin[{srcDirMT$, "results", "matchotter_check.csv"}],
  {{"quantity", "value"},
   Sequence @@ Table[{"V3_coefficient_phi0^" <> ToString[n], ToString[InputForm[coef$[[n]]]]}, {n, 4}],
   {"dV_difference_dphi", ToString[InputForm[diffMT$]]},
   {"minus_DRalgo", ToString[InputForm[Simplify[coef$ - dr$]]]}}];
Print["(b) wrote results/matchotter_check.csv"];
