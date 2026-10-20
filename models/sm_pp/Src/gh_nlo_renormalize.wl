(* ::Package:: *)

(* ::Title:: *)
(*Step (2b), 1 of 3: on-shell renormalization of QCDH.fr (QCD and the g g H operator) with FeynRules + NLOCT*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2b), as the QCD note's nlo_renormalize.wl: OnShellRenormalization[LQCDH, QCDOnly -> True,*)
(*FlavorMixing -> False] adds the counterterm Lagrangian of the strong sector (gluon, ghost and quark fields, aS -> aS + deltaaS).*)
(*The operator is written with aS, so its counterterm comes with deltaaS and the gluon field constants.  -> generated/QCDH_ren/.*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation (NLOCT needs it).  Needs the local patch of FeynRules/Core/Loop.m.*)
(*Batch:  wolframscript -file gh_nlo_renormalize.wl  (gh_generate_nlo.sh runs the three steps)*)


srcDirGR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirGR$];
LoadModel["QCDH.fr"];
lagRenGR$ = OnShellRenormalization[LQCDH, QCDOnly -> True, FlavorMixing -> False];
Print["renormalized parameters and fields: ", Union[Cases[lagRenGR$, (FR$deltaZ | FR$delta)[__], Infinity]]];
Print["counterterms of the H G G vertex (first order in FR$CT, with H): ",
  Length[Select[List @@ Expand[Coefficient[Expand[lagRenGR$], FR$CT]], ! FreeQ[#, H] &]], " terms"];
Quiet[CreateDirectory[FileNameJoin[{srcDirGR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirGR$, "generated"}]];
If[DirectoryQ["QCDH_ren"], DeleteDirectory["QCDH_ren", DeleteContents -> True]];
(* the operator's H G G G and H G G G G vertices have no structure in FeynArts' Lorentz.gen: FeynRules writes its own generic
   file QCDH_ren.gen, which WriteCT then uses *)
WriteFeynArtsOutput[lagRenGR$, Output -> "QCDH_ren", GenericFile -> True, FlavorExpand -> True];
Print["written: ", FileNames["*", "QCDH_ren"]];
