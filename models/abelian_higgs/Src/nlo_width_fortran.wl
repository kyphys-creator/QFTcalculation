(* ::Package:: *)

(* ::Title:: *)
(*Step (5), FormCalc's Fortran code: the NLO width of h -> A A compiled and run with LoopTools*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (5); a check of FormCalc's code generation (WriteSquaredME, WriteRenConst,*)
(*SetupCodeDir and its driver programs).  Unpatched FeynArts 3.12 and FormCalc 9.10, Feynman gauge (FeynArts' default*)
(*GaugeRules), the FeynRules model Src/generated/AbelianHiggs_FA; run in its own kernel.*)
(*  - tree: the A A h vertex; loop: the 14 diagrams of nlo_width_formcalc.wl (10 1PI, 4 tadpole-attached), with the tensor*)
(*    coefficients left to LoopTools (no PaVeReduce);*)
(*  - counterterm: the tree amplitude times the renormalization constant dCTAAh, so that 2 Re(M0* M1)/|M0|^2 is delta_OS*)
(*    of Eq. (nlowidth):*)
(*        dCTAAh = c_A + (1/2) dR_h + dR_A + Re Sigma_T(MA^2)|_MS-bar / (2 MA^2),*)
(*    dR_h = -Re Sigma^H'(MH^2) - dZ_Phi,  dR_A = -Re Sigma_T'(MA^2) - dZ_A  (FormCalc's FieldRC, transverse part),*)
(*    the MS-bar mass shift from FormCalc's MassRC minus its UVDivergentPart (the tadpole-attached diagrams included), and*)
(*    the MS-bar poles of the note at xi = 1 (Eqs. (ct), (ctv)), with FormCalc's Divergence (LoopTools' Delta):*)
(*        K c_A = (5/2 e^2 - 3 lam - 3 e^4/(2 lam)) Delta,  K dZ_Phi = 2 e^2 Delta,  K dZ_A = -(1/3) e^2 Delta,  K = 16 pi^2;*)
(*    the result is Delta independent only if the poles of the generated loop code are those of the note;*)
(*  - writes the code to Src/work/fc_haa (SetupCodeDir builds the model files from AbelianHiggs_FA.pars).*)
(*run_width_check.sh then compiles it against LoopTools and runs it (fc_haa_run.sh).*)
(*Batch: wolframscript -file nlo_width_fortran.wl  (in its own kernel)*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirWX$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
faDirWX$ = FileNameJoin[{srcDirWX$, "generated", "AbelianHiggs_FA"}];
modelWX$ = FileNameJoin[{faDirWX$, "AbelianHiggs_FA"}];
codeDirWX$ = FileNameJoin[{srcDirWX$, "work", "fc_haa"}];
Quiet[DeleteDirectory[codeDirWX$, DeleteContents -> True]];
AppendTo[$ModelPath, faDirWX$];   (* SetupCodeDir reads AbelianHiggs_FA.pars from the model path *)
SetOptions[InsertFields, Model -> modelWX$, GenericModel -> modelWX$, InsertionLevel -> {Particles}];
(* FeynArts does not apply the model's coupling table by itself; the self-energies of the renormalization constants go
   through this hook *)
CreateFeynAmpHook[args__] := CreateFeynAmp[args] /. M$FACouplings;
workDirWX$ = CreateDirectory[];
SetDirectory[workDirWX$];   (* FormCalc writes its FORM files here *)


(* ::Section:: *)
(*Amplitudes*)


procWX$ = {S[1]} -> {V[1], V[1]};
diag0WX$ = InsertFields[CreateTopologies[0, 1 -> 2], procWX$];
diag1WX$ = InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {WFCorrections}], procWX$];
Print["one-loop diagrams (expect 14): ", Length[CreateFeynAmp[diag1WX$]]];
treeWX$ = CalcFeynAmp[CreateFeynAmp[diag0WX$] /. M$FACouplings];
loopWX$ = CalcFeynAmp[CreateFeynAmp[diag1WX$] /. M$FACouplings];
ctWX$ = treeWX$ /. Amp[p_][x___] :> Amp[p] @@ (dCTAAh # & /@ {x});


(* ::Section:: *)
(*The renormalization constant*)


lamWX$ = EL^2 MH^2/(2 MA^2);
(* FormCalc computes a renormalization constant with ExcludeTopologies -> Internal (= Irreducible), i.e. without the
   tadpole-attached self-energy diagrams, unless Options[constant] say otherwise; FJ needs them in Sigma_T(MA^2) (the
   derivatives do not depend on them) *)
Options[dCTAAh] = {ExcludeTopologies -> {}};
RenConst[dCTAAh] := Module[{kk = 16 Pi^2, sT = MassRC[V[1]]},
   (5/2 EL^2 - 3 lamWX$ - 3 EL^4/(2 lamWX$)) Divergence/kk +
    1/2 (FieldRC[S[1]] - 2 EL^2 Divergence/kk) +
    (FieldRC[V[1]] + EL^2 Divergence/(3 kk)) +
    (sT - UVDivergentPart[sT])/(2 MA^2)];


(* ::Section:: *)
(*Code*)


SetupCodeDir[codeDirWX$, Model -> "AbelianHiggs_FA"];
(* the model declarations come from AbelianHiggs_FA.pars, which names the charge ee; the code uses FeynArts' EL (also
   in the coupling gc9 = EL) and FormCalc's Alfa = EL^2/(4 pi), Alfa2 = Alfa^2 *)
With[{fh = FileNameJoin[{codeDirWX$, "models", "AbelianHiggs_FA.Fh"}]},
  Export[fh, Import[fh, "Text"] <> "\n\tRealType EL, Alfa, Alfa2\n\tparameter (EL = ee)\n" <>
     "\tparameter (Alfa = EL**2/(4*3.1415926535897932384626433832795029D0))\n\tparameter (Alfa2 = Alfa**2)\n",
    "Text"]];
(* GCC 16 has Fortran 2023's intrinsic subroutine SPLIT, which takes the place of FormCalc's kinematics routine Split in
   the drivers ("Too many arguments in call to 'split'"); declare Split external in the copies of the drivers *)
Scan[With[{f = FileNameJoin[{codeDirWX$, "F", #}]},
    Export[f, StringReplace[Import[f, "Text"],
      "\tsubroutine Kinematics(fac)\n\timplicit none\n" -> "\tsubroutine Kinematics(fac)\n\timplicit none\n\texternal Split\n"],
     "Text"]] &,
  {"1to2.F", "1to3.F", "2to2.F", "2to3.F", "2to4.F"}];
(* FormCalc names the generated subroutines after the variables that hold the amplitudes, and Fortran names cannot
   contain $ *)
haaTree = treeWX$; haaLoop = loopWX$; haaCT = ctWX$;
WriteSquaredME[haaTree, {haaLoop, haaCT}, Abbr[], Subexpr[], codeDirWX$];
WriteRenConst[{haaTree, haaLoop, haaCT}, codeDirWX$];
Print["written ", codeDirWX$];
