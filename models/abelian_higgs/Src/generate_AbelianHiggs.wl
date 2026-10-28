(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on AbelianHiggs.fr -> FeynArts model and UFO (abelian Higgs model, MS-bar parameters, general R_xi gauge)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_AbelianHiggs.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/abelian_higgs/Src/generate_AbelianHiggs.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/AbelianHiggs_FA/              FeynArts model (AbelianHiggs_FA.mod, .gen, .pars); xiA -> GaugeXi[A]*)
(*  Src/generated/AbelianHiggs_UFO/             UFO for MadGraph (Feynman gauge: xi = 1)*)
(*  Src/generated/FeynmanRules_AbelianHiggs.m   vertex list returned by FeynmanRules*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  10 vertex classes (5 scalar, 4 gauge-scalar, 1 ghost-scalar), every difference from the*)
(*  note's table (Table rules) equal to 0.  The table copy with three deliberate errors gives exactly 3 nonzero*)
(*  differences.  No messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in AH$*)
(*so that they cannot clash with model symbols (ee, MA, MH, vev, lam, A, H, G0, ghA): FeynRules patterns with the*)
(*name of a model symbol leak that symbol into the result.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_AbelianHiggs.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen generate_AbelianHiggs.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*locations*)


startDirAH$ = Directory[];
srcDirAH$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirAH$ = FileNameJoin[{srcDirAH$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirAH$];
LoadModel["AbelianHiggs.fr"];


(* ::Subsubsection:: *)
(*Inspect: the Lagrangian of AbelianHiggs.fr (Eq. (L) without gauge fixing and counterterms, with the ghost term)*)


If[$Notebooks, LAH // TraditionalForm]


(* ::Section:: *)
(*checks of the Lagrangian*)


(* CheckMassSpectrum reports no disagreement.  The Goldstone mass term is not in LAH (it comes from the gauge-fixing
   term, which has no vertices); the ghost mass term xiA MA^2 ghAbar ghA is, and agrees with MA at xiA = 1. *)
Print["Hermiticity (expect {}): ", CheckHermiticity[LAH]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LAH]];
CheckMassSpectrum[LAH];

verticesAH$ = FeynmanRules[LAH, ScreenOutput -> False];
Print["Number of vertex classes (expect 10): ", Length[verticesAH$]];
Print["Field lists: ", First /@ (verticesAH$ /. {{v_List, e_} :> {First /@ v, e}})];


(* ::Section:: *)
(*the note's table*)


(* ::Text:: *)
(*Inert notation for the comparison:  metAH$[i, j] = g^{mu_i mu_j},  momAH$[i, j] = p_i^{mu_j}  (incoming momentum of*)
(*leg i, index of leg j).  The table is written with ee, MA, MH; the FeynRules expressions with ee, vev, lam, muH2 are*)
(*brought to the same variables by vev = MA/ee, lam = ee^2 MH^2/(2 MA^2), muH2 = MH^2/2.*)


toInertAH$[expr_] := expr /. {
   HoldPattern[ME[Index[Lorentz, Ext[i_]], Index[Lorentz, Ext[j_]]]] :> metAH$ @@ Sort[{i, j}],
   HoldPattern[FV[i_, Index[Lorentz, Ext[j_]]]] :> momAH$[i, j]};

paramsAH$ = {vev -> MA/ee, lam -> ee^2 MH^2/(2 MA^2), muH2 -> MH^2/2};
momConsAH$ = {momAH$[3, j_] :> -momAH$[1, j] - momAH$[2, j]};
normAH$[expr_] := Simplify[Together[Expand[expr /. paramsAH$ /. momConsAH$]]];

lamAH$ = ee^2 MH^2/(2 MA^2);
vevAH$ = MA/ee;

(* field lists in FeynRules' order, legs 1, 2, ... *)
tableAH$ = {
  (* scalar self-couplings *)
  {H, H, H} -> -6 I lamAH$ vevAH$,
  {G0, G0, H} -> -2 I lamAH$ vevAH$,
  {H, H, H, H} -> -6 I lamAH$,
  {G0, G0, G0, G0} -> -6 I lamAH$,
  {G0, G0, H, H} -> -2 I lamAH$,
  (* gauge-scalar *)
  {A, A, H} -> 2 I ee MA metAH$[1, 2],
  {A, A, H, H} -> 2 I ee^2 metAH$[1, 2],
  {A, A, G0, G0} -> 2 I ee^2 metAH$[1, 2],
  {A, G0, H} -> ee (momAH$[3, 1] - momAH$[2, 1]),
  (* ghost-scalar *)
  {ghAbar, ghA, H} -> -I xiA ee MA
};


(* ::Section:: *)
(*comparison*)


compareAH$[{flds_, expr_}, table_] := {flds, normAH$[toInertAH$[expr] - (flds /. table)]};

reportAH$[table_, label_] := Module[{rows, bad},
   rows = compareAH$[#, table] & /@ (verticesAH$ /. {{v_List, e_} :> {First /@ v, e}});
   bad = Select[rows, #[[2]] =!= 0 &];
   Print[label, ": ", Length[rows], " classes compared, nonzero differences: ", Length[bad]];
   Scan[Print["   ", #[[1]], "  difference ", InputForm[#[[2]]]] &, bad];
   rows];

rowsAH$ = reportAH$[tableAH$, "Note's table (expect 0)"];
Print["Classes not in the table (expect {}): ",
  Complement[First /@ (verticesAH$ /. {{v_List, e_} :> {First /@ v, e}}), First /@ tableAH$]];
Print["Table entries not produced by FeynRules (expect {}): ",
  Complement[First /@ tableAH$, First /@ (verticesAH$ /. {{v_List, e_} :> {First /@ v, e}})]];

(* control: three deliberate errors (the sign of A G0 H, a factor 2 in G0 G0 H, a missing xi in the ghost vertex) *)
tableBadAH$ = tableAH$ /. {
   ({A, G0, H} -> x_) :> ({A, G0, H} -> -x),
   ({G0, G0, H} -> x_) :> ({G0, G0, H} -> 2 x),
   ({ghAbar, ghA, H} -> x_) :> ({ghAbar, ghA, H} -> (x /. xiA -> 1))};
reportAH$[tableBadAH$, "Table with three deliberate errors (expect 3)"];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesAH$ /. {v_List, c_} :> {First /@ v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirAH$]];
SetDirectory[outDirAH$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"AbelianHiggs_FA", "AbelianHiggs_UFO"}];

Put[verticesAH$, "FeynmanRules_AbelianHiggs.m"];
WriteFeynArtsOutput[LAH, Output -> "AbelianHiggs_FA", GenericFile -> True];
WriteUFO[LAH, Output -> "AbelianHiggs_UFO"];

(* FeynArts: the ghost-scalar coupling carries the gauge parameter of the propagators *)
modFileAH$ = FileNameJoin[{outDirAH$, "AbelianHiggs_FA", "AbelianHiggs_FA.mod"}];
modTextAH$ = Import[modFileAH$, "Text"];
Print["xiA in AbelianHiggs_FA.mod before the replacement: ",
  Length[StringCases[modTextAH$, RegularExpression["\\bxiA\\b"]]]];
modTextAH$ = StringReplace[modTextAH$, RegularExpression["\\bxiA\\b"] -> "GaugeXi[A]"];
Export[modFileAH$, modTextAH$, "Text"];

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirAH$, ": ",
  FileNameTake /@ FileNames["*", outDirAH$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file AbelianHiggs_FA.mod*)


If[$Notebooks,
  StringTake[Import[modFileAH$, "Text"], UpTo[2500]]
]


SetDirectory[startDirAH$];
