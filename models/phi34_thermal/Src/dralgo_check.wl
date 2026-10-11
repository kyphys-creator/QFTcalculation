(* ::Package:: *)

(* ::Title:: *)
(*Step (8a): the single-field thermal potential against DRalgo (dimensional reduction)*)


(* ::Text:: *)
(*Research note models/phi34_thermal, step (8).  The phi^3 + phi^4 model V = t phi + m^2 phi^2/2 + g phi^3/6 + lambda phi^4/24*)
(*(the model file RealScalar.m of the DRalgo examples, with our symbols) is reduced with DRalgo 1.5.0 to the 3D EFT at*)
(*LO and NLO.  (a) the 3D parameters and the 4D beta functions (zero-temperature note: beta_lambda = 3 lambda^2/(4 Pi)^2,*)
(*beta_g = 3 g lambda/(4 Pi)^2, mu dm^2/dmu = (g^2 + lambda m^2)/(4 Pi)^2).  (b) the 4D potential rebuilt from the 3D EFT*)
(*at one-loop accuracy (LO + one-loop matching + the 3D one-loop term -(1/12 Pi) m3^(3/2)) against Eq. (13) of the note,*)
(*V + t phi + (T^2/24) M^2 - (T/12 Pi)(M^2 + Pi)^(3/2) - (M^4/64 Pi^2) L_b, L_b = 2 ln(mubar/T) + 2 gamma_E - 2 ln 4 Pi:*)
(*the phi-derivative of the difference must vanish identically.  (c) the size of the two-loop (NLO) thermal mass and its*)
(*effect on the leading-order spinodal temperature (alpha = 0.9, kappa_4 = 1).  Writes Src/results/dralgo_check.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file dralgo_check.wl ; only the lines starting with (a), (b), (c) are printed.  Interactive:  ~/hep/bin/wopen dralgo_check.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).  DRalgo needs GroupMath (in ~/Library/Wolfram/Applications).  Run in a kernel of its own (not together with Matchete).*)


(* ::Section:: *)
(*Setup*)


DRalgo`DRalgo`$LoadGroupMath = True;
Quiet[Get["DRalgo`DRalgo`"]];
srcDirDR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*(a) the model and the dimensional reduction*)


Group = {"U1"}; CouplingName = {g1}; RepAdjoint = {0}; RepScalar = {{{0}, "R"}}; RepFermion = {};
{gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJC, \[Mu]IJ, Ysff, YsffC} =
  AllocateTensors[Group, RepAdjoint, CouplingName, RepFermion, RepScalar];
InputInv = {{1}, {True}}; LinearTerm = CreateInvariant[Group, RepScalar, InputInv][[1]];
\[Lambda]1 = GradTadpole[tt LinearTerm];
InputInv = {{1, 1}, {True, True}}; MassTerm = CreateInvariant[Group, RepScalar, InputInv][[1]];
\[Mu]ij = GradMass[msq/2 MassTerm] // SparseArray;
InputInv = {{1, 1, 1}, {True, True, True}}; CubicTerm = CreateInvariant[Group, RepScalar, InputInv][[1]];
\[Lambda]3 = GradCubic[gg/6 CubicTerm];
\[Lambda]4 = GradQuartic[lam/24 MassTerm^2];
ImportModelDRalgo[Group, gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJ, \[Mu]IJC, Ysff, YsffC, Verbose -> False];
PerformDRhard[];
cpl$ = Association[PrintCouplings[]];
mLO$ = msq3d /. PrintScalarMass["LO"]; mNLO$ = msq3d /. PrintScalarMass["NLO"];
tLO$ = tt3d /. PrintTadpoles["LO"]; tNLO$ = tt3d /. PrintTadpoles["NLO"];
beta$ = Association[BetaFunctions4D[]];
Print["(a) 3D couplings: lambda3 = ", InputForm[cpl$[lam3d]], ", gamma3 = ", InputForm[Expand[cpl$[gg3d]]]];
Print["(a) 3D mass^2: LO ", InputForm[mLO$], "; NLO ", InputForm[mNLO$]];
Print["(a) 3D tadpole: LO ", InputForm[Expand[tLO$]], "; NLO ", InputForm[tNLO$]];
betaOK$ = Simplify[{beta$[lam] - 3 lam^2/(4 Pi)^2, beta$[gg] - 3 gg lam/(4 Pi)^2, beta$[msq] - (gg^2 + lam msq)/(4 Pi)^2}] === {0, 0, 0};
Print["(a) 4D beta functions ", InputForm[Normal[beta$]], " equal those of the zero-temperature note: ", betaOK$];


(* ::Subsubsection:: *)
(*Inspect: the DRalgo output*)


If[$Notebooks, {PrintCouplings[], PrintScalarMass["LO"], PrintScalarMass["NLO"], PrintTadpoles["LO"], PrintTadpoles["NLO"]}]


(* ::Section:: *)
(*(b) the 4D potential from the 3D EFT at one-loop accuracy, against Eq. (13)*)


(* one-loop part of the NLO pieces: drop the two-loop terms (proportional to T^2 or to the 3D couplings) *)
oneLoop$[x_] := (x /. {lam3d -> 0, gg3d -> 0}) /. T -> 0;
m3$ = mLO$ + oneLoop$[mNLO$];
t3$ = tLO$ + oneLoop$[tNLO$ Sqrt[T]]/Sqrt[T];
VDR$ = T (t3$ \[Phi]3 + m3$ \[Phi]3^2/2 + cpl$[gg3d] \[Phi]3^3/6 + cpl$[lam3d] \[Phi]3^4/24) /. \[Phi]3 -> \[Phi]/Sqrt[T];
m3field$ = D[T (tLO$ \[Phi]3 + mLO$ \[Phi]3^2/2 + gg Sqrt[T] \[Phi]3^3/6 + lam T \[Phi]3^4/24), {\[Phi]3, 2}]/T /. \[Phi]3 -> \[Phi]/Sqrt[T];
VDR$ = VDR$ - T/(12 Pi) m3field$^(3/2);
M2$ = msq + gg \[Phi] + lam \[Phi]^2/2;
VNote$ = tt \[Phi] + msq \[Phi]^2/2 + gg \[Phi]^3/6 + lam \[Phi]^4/24 + T^2/24 M2$ - T/(12 Pi) (M2$ + lam T^2/24)^(3/2) - M2$^2/(64 Pi^2) Lb;
diff$ = Simplify[D[VNote$ - VDR$, \[Phi]]];
Print["(b) 3D field-dependent mass^2 (LO) = M^2 + lambda T^2/24: ", Simplify[m3field$ - (M2$ + lam T^2/24)] === 0];
Print["(b) d/dphi [Eq. (13) - (DRalgo LO + one-loop matching + 3D one-loop)] = ", diff$];
num$ = Table[N[D[VNote$ - VDR$, \[Phi]] /. {tt -> 0.3, msq -> 1, gg -> 1.6, lam -> 0.7, T -> 3.1, Lb -> -4.2, \[Phi] -> x}, 30], {x, {-3., 0.5, 2.}}];
Print["(b) numerical check at three fields: ", num$];


(* ::Section:: *)
(*(c) the two-loop thermal mass and the spinodal temperature (alpha = 0.9, kappa_4 = 1)*)


(* two-loop part of the NLO mass at mu_3 = mu (no 3D running), relative to Pi = lambda T^2/24 *)
twoLoop$ = Simplify[(mNLO$ - oneLoop$[mNLO$]) /. Log[\[Mu]3/\[Mu]] -> 0 /. lam3d -> lam T];
rel$ = Simplify[twoLoop$/(lam T^2/24)];
Print["(c) two-loop thermal mass / (lambda T^2/24) = ", InputForm[rel$]];
alpha$ = 0.9; gm$ = 1.5261/Sqrt[alpha$]; lamN$ = alpha$ gm$^2/3;    (* units m = 1 *)
LbN$[tT_] := 2 Log[1/tT] + 2 EulerGamma - 2 Log[4 Pi];             (* mubar = m *)
hb$ = 3 (1 - alpha$)/alpha$^2 + gm$^2/(32 Pi^2); A0$ = 1 - 3/(2 alpha$);
(* leading-order spinodal: |b| = (2|a|/3)(6|a|/alpha)^(1/2), a = A0 + (alpha tau^2/72)(1 + delta) *)
spin$[del_] := tau /. FindRoot[(A0$ + alpha$ tau^2/72 (1 + del[tau])) + (1.5 hb$ Sqrt[alpha$/6])^(2/3), {tau, 5.}];
tau0$ = spin$[0 &];
tau2$ = spin$[Function[tau, rel$ /. {lam -> lamN$, Lb -> LbN$[tau/gm$], T -> tau/gm$}]];
Print["(c) leading-order tau_sp without and with the two-loop thermal mass: ", {tau0$, tau2$}, ", relative shift ", tau2$/tau0$ - 1,
  " (delta at tau_sp = ", rel$ /. {lam -> lamN$, Lb -> LbN$[tau0$/gm$]}, ")"];


(* ::Section:: *)
(*Output*)


(* CSV writer: a field is quoted only when it contains a comma or a quote *)
csvField$[x_] := Module[{s = Which[StringQ[x], x, NumberQ[x], ToString[N[x], CForm], True, ToString[x, InputForm]]},
   If[StringContainsQ[s, "," | "\""], "\"" <> StringReplace[s, "\"" -> "\"\""] <> "\"", s]];
writeCSV$[file_, rows_] := Export[file, StringRiffle[StringRiffle[csvField$ /@ #, ","] & /@ rows, "\n"] <> "\n", "Text"];
writeCSV$[FileNameJoin[{srcDirDR$, "results", "dralgo_check.csv"}],
  {{"quantity", "value"},
   {"lambda3d", ToString[InputForm[cpl$[lam3d]]]}, {"gamma3d", ToString[InputForm[Expand[cpl$[gg3d]]]]},
   {"msq3d_LO", ToString[InputForm[mLO$]]}, {"msq3d_NLO", ToString[InputForm[mNLO$]]},
   {"tt3d_LO", ToString[InputForm[Expand[tLO$]]]}, {"tt3d_NLO", ToString[InputForm[tNLO$]]},
   {"beta4D_equal_zeroT_note", betaOK$}, {"dV_difference_dphi", ToString[InputForm[diff$]]},
   {"twoloop_mass_over_Pi", ToString[InputForm[rel$]]},
   {"tau_sp_LO_alpha0.9", tau0$}, {"tau_sp_LO_with_twoloop_mass", tau2$}}];
Print["(c) wrote results/dralgo_check.csv"];
