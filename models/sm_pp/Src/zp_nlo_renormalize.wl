(* ::Package:: *)

(* ::Title:: *)
(*Step (4b), 1 of 3: on-shell renormalization of QCDZp.fr (QCD, an electron and the SSM Z') with FeynRules + NLOCT*)


(* ::Text:: *)
(*Research note models/sm_pp, step (4b), as the QCD note's nlo_renormalize.wl: OnShellRenormalization[LQCDZp, QCDOnly -> True,*)
(*FlavorMixing -> False] adds the counterterm Lagrangian of the strong sector (the gluon, ghost and quark fields, aS); the Z' and*)
(*the electron are not renormalized (QCD corrections only).  The Z' f f vertex is renormalizable, so FeynArts' Lorentz.gen has its*)
(*structure (GenericFile -> False).  -> generated/QCDZp_ren/.  FlavorExpand -> True makes FeynRules write FR$ClassesTranslation*)
(*(NLOCT needs it).  Needs the local patch of FeynRules/Core/Loop.m.*)
(*Batch:  wolframscript -file zp_nlo_renormalize.wl  (zp_generate_nlo.sh runs the three steps)*)


srcDirZR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirZR$];
LoadModel["QCDZp.fr"];
lagRenZR$ = OnShellRenormalization[LQCDZp, QCDOnly -> True, FlavorMixing -> False];
Print["renormalized parameters and fields: ", Union[Cases[lagRenZR$, (FR$deltaZ | FR$delta)[__], Infinity]]];
Quiet[CreateDirectory[FileNameJoin[{srcDirZR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirZR$, "generated"}]];
If[DirectoryQ["QCDZp_ren"], DeleteDirectory["QCDZp_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenZR$, Output -> "QCDZp_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "QCDZp_ren"]];
