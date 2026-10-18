(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 2 of 7: NLOCT's R2 vertices and on-shell UV counterterms of the note's CKM model*)


(* ::Text:: *)
(*As the SM note's nlo_writect.wl.  Unpatched FeynArts 3.12 + NLOCT 1.02 in a kernel without FeynRules: WriteCT computes*)
(*the one-loop UV counterterms of Src/generated/SM_CKM_ren (NLOCT's on-shell conditions, with the off-diagonal quark field*)
(*constants) and the R2 vertices in Feynman gauge at order QED (electroweak), and writes Src/generated/SM_CKM_CT.nlo (not*)
(*in git) and its R2 vertices to Src/generated/SM_CKM_R2.m.  nlo_ckm_ufo.wl uses the R2 vertices, nlo_ckm_dz.wl NLOCT's*)
(*on-shell field constants from its two-point UV vertices.  Batch: wolframscript -file nlo_ckm_writect.wl*)
(*(after nlo_ckm_renormalize.wl).  With the argument nomix: the model without quark mixing (SM_CKM_ren0 -> SM_CKM_CT0.nlo,*)
(*SM_CKM_R2_0.m; the R2 vertices do not depend on the renormalization).  With the argument msbar: the model without mixing*)
(*and NLOCT's MS-bar counterterms (MSbar -> True: no on-shell conditions to solve; only the R2 vertices are used),*)
(*SM_CKM_ren0 -> SM_CKM_CTms.nlo, SM_CKM_R2.m.*)


srcDirNC$ = DirectoryName[$InputFileName];
SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0NC$ = AbsoluteTime[];
argNC$ = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], ""];
{inNC$, ctNC$, r2NC$} = Switch[argNC$, "nomix", {"SM_CKM_ren0", "SM_CKM_CT0", "SM_CKM_R2_0.m"}, "msbar", {"SM_CKM_ren0", "SM_CKM_CTms", "SM_CKM_R2.m"},
   _, {"SM_CKM_ren", "SM_CKM_CT", "SM_CKM_R2.m"}];
WriteCT[FileNameJoin[{Directory[], inNC$, inNC$}], "Lorentz", Output -> ctNC$, MSbar -> (argNC$ === "msbar")];
Print["written: ", FileNames[ctNC$ <> ".nlo"], ";  ", Round[AbsoluteTime[] - t0NC$], " s"];
Get[ctNC$ <> ".nlo"];
Put[DeleteCases[R2$vertlist, Last[{}]], r2NC$];
Print["written: ", r2NC$, " (", Length[DeleteCases[R2$vertlist, Last[{}]]], " R2 vertices);  UV vertices: ",
  Length[UV$vertlist], ";  ", Round[AbsoluteTime[] - t0NC$], " s"];
