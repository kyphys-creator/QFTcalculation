(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on PsYukawa.fr -> FeynArts model and UFO (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_PsYukawa.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/yukawa_ps/Src/generate_PsYukawa.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/PsYukawa_FA/                FeynArts model (PsYukawa_FA.mod, .gen, .pars)*)
(*  Src/generated/PsYukawa_UFO/               UFO for MadGraph*)
(*  Src/generated/FeynmanRules_PsYukawa.m     vertex list returned by FeynmanRules*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,*)
(*  vertex {{psibar,1},{psi,2},{phi,3}} -> yps gamma5 (note Fig. 1), {{phi,1},...,{phi,4}} -> -I lamphi,*)
(*  no phi^3 and no scalar Yukawa vertex, no messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global*)
(*names below end in PsY$ so that they cannot clash with model symbols (yps, lamphi, mphi, Mpsi, phi, psi).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_PsYukawa.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts).  Interactive:  ~/hep/bin/wopen generate_PsYukawa.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*locations*)


startDirPsY$ = Directory[];
srcDirPsY$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirPsY$ = FileNameJoin[{srcDirPsY$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirPsY$];
LoadModel["PsYukawa.fr"];


(* ::Subsubsection:: *)
(*Inspect: the Lagrangian of PsYukawa.fr (Eq. (1) without counterterms)*)


If[$Notebooks,
  LPsYukawa // TraditionalForm
]


(* ::Section:: *)
(*checks*)


Print["Hermiticity (expect {}): ", CheckHermiticity[LPsYukawa]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LPsYukawa]];
Print["Mass spectrum: ", CheckMassSpectrum[LPsYukawa]];

verticesPsY$ = FeynmanRules[LPsYukawa, ScreenOutput -> False];
Print["Vertices (expect yps gamma5 for psibar psi phi and -I lamphi for 4 phi): ", InputForm[verticesPsY$]];


(* ::Text:: *)
(*The Yukawa vertex must be yps gamma5 (= i * (-i yps gamma5) from L_int).  If FeynRules writes it through the chiral*)
(*projectors ProjP = (1+gamma5)/2 and ProjM = (1-gamma5)/2, rewrite them as gamma5 first.*)


yukVertexPsY$ = Select[verticesPsY$, Sort[First /@ #[[1]]] === Sort[{psibar, psi, phi}] &];
yukCoefPsY$ = Simplify[(yukVertexPsY$[[1, 2]] /. {
      ProjP[a_, b_] :> (IndexDelta[a, b] + Ga[5, a, b])/2,
      ProjM[a_, b_] :> (IndexDelta[a, b] - Ga[5, a, b])/2})];
Print["Yukawa vertex in terms of gamma5 (expect yps Ga[5, s1, s2]): ", InputForm[yukCoefPsY$]];
Print["Number of vertices (expect 2: psibar psi phi, phi^4): ", Length[verticesPsY$]];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesPsY$ /. {v_List, c_} :> {v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirPsY$]];
SetDirectory[outDirPsY$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"PsYukawa_FA", "PsYukawa_UFO"}];

Put[verticesPsY$, "FeynmanRules_PsYukawa.m"];
WriteFeynArtsOutput[LPsYukawa];      (* -> PsYukawa_FA/ *)
WriteUFO[LPsYukawa];                 (* -> PsYukawa_UFO/ *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirPsY$, ": ",
  FileNameTake /@ FileNames["*", outDirPsY$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file PsYukawa_FA.mod*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{outDirPsY$, "PsYukawa_FA", "PsYukawa_FA.mod"}], "Text"], UpTo[2500]]
]


SetDirectory[startDirPsY$];
