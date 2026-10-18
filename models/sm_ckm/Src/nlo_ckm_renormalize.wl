(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 1 of 7: the renormalized Lagrangian of the note's CKM model for NLOCT (Feynman gauge)*)


(* ::Text:: *)
(*As the SM note's nlo_renormalize.wl, for SM_CKM.fr.  FeynRules + NLOCT: OnShellRenormalization[LSM] adds the*)
(*counterterm Lagrangian (field constants FR$deltaZ, parameter constants FR$delta for the external parameters, the*)
(*tadpole constant FR$deltat[H], set to 0 here) at first order in FR$CT.  The quark fields may mix within each charge*)
(*(FlavorMixing: the pairs u-c, u-t, c-t, d-s, d-b, s-b), so that NLOCT also fixes the off-diagonal on-shell field*)
(*constants; the leptons and neutrinos are not mixed (no PMNS matrix; the neutrinos are degenerate).  The gauge*)
(*parameters are set to 1 (MadLoop computes in Feynman gauge).  The result is written as a FeynArts model,*)
(*Src/generated/SM_CKM_ren/ (overwritten), for nlo_ckm_writect.wl.  NLOCT's R2 vertices and its on-shell field constants*)
(*are used (nlo_ckm_ufo.wl, nlo_ckm_dz.wl); the other UV counterterms are those of the note's MS-bar (FJ) scheme.*)
(*Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md).*)
(*Batch: wolframscript -file nlo_ckm_renormalize.wl  (in a fresh kernel)*)
(*With the argument nomix: no quark mixing (FlavorMixing -> False, as the SM note), written to SM_CKM_ren0.*)


srcDirNR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["SM_CKM.fr"];
t0NR$ = AbsoluteTime[];
lagNR$ = LSM /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
mixNR$ = {{u, c}, {u, t}, {c, t}, {d, s}, {d, b}, {s, b}};
noMixNR$ = Length[$ScriptCommandLine] >= 2 && $ScriptCommandLine[[2]] === "nomix";
outNR$ = If[noMixNR$, "SM_CKM_ren0", "SM_CKM_ren"];
lagRenNR$ = OnShellRenormalization[lagNR$, FlavorMixing -> If[noMixNR$, False, mixNR$]];
(* the one-point vertex of the tadpole constant has no generic coupling in FeynArts' Lorentz.gen (SM note); MadLoop has
   no tadpole diagrams, and only the R2 vertices and the field constants of NLOCT are used *)
lagRenNR$ = lagRenNR$ /. FR$deltat[_] -> 0;
ctConstNR$ = Union[Cases[Coefficient[Expand[lagRenNR$], FR$CT], (h : FR$delta | FR$deltaZ | FR$deltat)[x___] :> h[x], Infinity]];
Print["renormalized: ", Round[AbsoluteTime[] - t0NR$], " s;  counterterm constants: ", Length[ctConstNR$]];
Print["  parameter constants: ", Cases[ctConstNR$, FR$delta[{p_}, ___] :> p]];
Print["  off-diagonal quark field constants: ", Cases[ctConstNR$, FR$deltaZ[{a_, b_}, ___] /; a =!= b && MemberQ[Flatten[mixNR$], a]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ[outNR$], DeleteDirectory[outNR$, DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> outNR$, GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", outNR$], ";  ", Round[AbsoluteTime[] - t0NR$], " s"];
