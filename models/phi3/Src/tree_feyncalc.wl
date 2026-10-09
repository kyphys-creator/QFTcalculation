(* ::Package:: *)

(* tree_feyncalc.wl -- tree-level phi phi -> phi phi with FeynArts + FeynCalc
   (research note, step (2): compare with Eq. (11), M = -g^2 [1/(s-m^2)+1/(t-m^2)+1/(u-m^2)]).

   Usage:  wolframscript -file tree_feyncalc.wl     (run generate_Phi3.wl first)
   Uses the FeynArts model in Src/generated/Phi3_FA.  A copy is patched with FAPatch in a
   temporary directory, so the committed files are not modified.
   Momenta: p1 p2 -> k1 k2;  s = (p1+p2)^2, t = (p1-k1)^2, u = (p1-k2)^2.
   FeynArts' default PreFactor -I turns the sum of diagrams (i M) into M itself. *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];

srcDirTree$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ---------- patched copy of the FeynRules-generated FeynArts model ---------- *)
modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirTree$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "Phi3_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "Phi3_FA", "Phi3_FA"}];

(* ---------- diagrams and amplitude ---------- *)
diagsTree$ = InsertFields[CreateTopologies[0, 2 -> 2], {S[1], S[1]} -> {S[1], S[1]},
   InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$];

ampTree$ = FCFAConvert[CreateFeynAmp[diagsTree$], IncomingMomenta -> {p1, p2},
   OutgoingMomenta -> {k1, k2}, ChangeDimension -> 4, List -> True, SMP -> False];
Print["number of tree diagrams (expect 3): ", Length[ampTree$]];
Print["amplitudes per diagram: ", InputForm /@ ampTree$];

FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
mTreeFC$ = Simplify[FeynAmpDenominatorExplicit[Total[ampTree$]]];
Print["M (FeynCalc) = ", InputForm[mTreeFC$]];

(* ---------- comparison with the note, Eq. (11) ---------- *)
mTreeNote$ = -gphi^2 (1/(s - m^2) + 1/(t - m^2) + 1/(u - m^2));
Print["M(FeynCalc) - M(note, Eq. 11) = ", Simplify[mTreeFC$ - mTreeNote$], "   (expect 0)"];

(* one numerical point for the MadGraph / Python comparison: sqrt(s) = 5, cos(theta) = 0.3, m = g = 1 *)
With[{sv = 25., mv = 1., c = 0.3},
  Module[{p2cm = sv/4 - mv^2, tv, uv},
    tv = -2 p2cm (1 - c); uv = -2 p2cm (1 + c);
    Print["M at sqrt(s)=5, cos(theta)=0.3, m=g=1: ", mTreeFC$ /. {s -> sv, t -> tv, u -> uv, m -> mv, gphi -> 1.}]]];

DeleteDirectory[modelTmpDirTree$, DeleteContents -> True];
