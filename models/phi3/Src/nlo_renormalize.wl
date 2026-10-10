(* ::Package:: *)

(* nlo_renormalize.wl -- step 1 of 3 of the NLO UFO generation (research note, step (6)).
   FeynRules + NLOCT: OnShellRenormalization[LPhi3] adds the counterterm Lagrangian
     phi -> (1 + deltaZ/2) phi,  m -> m + deltam,  gphi -> gphi + deltag   (first order in FR$CT),
   which is written as a FeynArts model, Src/generated/Phi3_ren/ (overwritten).
   FlavorExpand -> True makes FeynRules write FR$ClassesTranslation = {phi -> S[1]}; without it the
   translation is empty and NLOCT sets deltaZ of phi to zero in the phi-phi vertex (it does not
   recognize S[1] as phi), leaving deltaZ undetermined.
   Needs the local patch of FeynRules/Core/Loop.m (see ~/hep/README.md): unpatched,
   OnShellRenormalization aborts for a model without any field mixing.

   Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl;
           generate_Phi3_NLO.sh runs all three) *)

srcDirNR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["Phi3.fr"];

lagRenNR$ = OnShellRenormalization[LPhi3];
Print["renormalized Lagrangian: ", InputForm[lagRenNR$]];

Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["Phi3_ren"], DeleteDirectory["Phi3_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "Phi3_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "Phi3_ren"]];
