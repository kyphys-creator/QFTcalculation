(* ::Package:: *)

(* generate_Phi3.wl -- run FeynRules on Phi3.fr and write the FeynArts model and the UFO.

   Usage
     terminal :  wolframscript -file generate_Phi3.wl      (from any directory)
     notebook :  Get["<path>/models/phi3/Src/generate_Phi3.wl"]
                 or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])

   Output (overwritten on each run)
     Src/generated/Phi3_FA/                FeynArts model (Phi3_FA.mod, .gen, .pars)
     Src/generated/Phi3_UFO/               UFO for MadGraph
     Src/generated/FeynmanRules_Phi3.m     vertex list returned by FeynmanRules

   Expected results
     CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,
     vertex {{phi,1},{phi,2},{phi,3}} -> -I gphi,  no messages.

   Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global
   names below end in Phi3$ so that they cannot clash with model symbols (gphi, m, phi). *)

(* ---------- locations ---------- *)
startDirPhi3$ = Directory[];
srcDirPhi3$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirPhi3$ = FileNameJoin[{srcDirPhi3$, "generated"}];

(* ---------- FeynRules ---------- *)
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirPhi3$];
LoadModel["Phi3.fr"];

(* ---------- checks ---------- *)
Print["Hermiticity (expect {}): ", CheckHermiticity[LPhi3]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LPhi3]];
Print["Mass spectrum: ", CheckMassSpectrum[LPhi3]];

verticesPhi3$ = FeynmanRules[LPhi3, ScreenOutput -> False];
Print["Vertices (expect {{phi,1},{phi,2},{phi,3}} -> -I gphi): ", verticesPhi3$];

(* ---------- write outputs ---------- *)
Quiet[CreateDirectory[outDirPhi3$]];
SetDirectory[outDirPhi3$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"Phi3_FA", "Phi3_UFO"}];

Put[verticesPhi3$, "FeynmanRules_Phi3.m"];
WriteFeynArtsOutput[LPhi3];      (* -> Phi3_FA/ *)
WriteUFO[LPhi3];                 (* -> Phi3_UFO/ *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirPhi3$, ": ",
  FileNameTake /@ FileNames["*", outDirPhi3$]];

SetDirectory[startDirPhi3$];
