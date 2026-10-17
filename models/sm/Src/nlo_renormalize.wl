(* ::Package:: *)

(* ::Title:: *)
(*Step (9b), 1 of 3: the renormalized Lagrangian of the note's model for NLOCT (Feynman gauge)*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LSM] adds the counterterm Lagrangian (field constants FR$deltaZ, parameter*)
(*constants FR$delta for the external parameters aEWM1, aS, MZ, MW, MH and the fermion masses, the tadpole constant*)
(*FR$deltat[H], set to 0 here) at first order in FR$CT.  The gauge parameters are set to 1 first (MadLoop computes in Feynman gauge;*)
(*otherwise NLOCT also renormalizes xiZ and xiW).  The result is written as a FeynArts model, Src/generated/SM_ren/*)
(*(overwritten), for nlo_writect.wl.  Only NLOCT's R2 vertices are used (nlo_ufo.wl); the UV counterterms of the FJ*)
(*scheme are written by hand.  Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md).*)
(*Batch: wolframscript -file nlo_renormalize.wl  (in a fresh kernel)*)


srcDirNR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["SM.fr"];
t0NR$ = AbsoluteTime[];
lagNR$ = LSM /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
lagRenNR$ = OnShellRenormalization[lagNR$, FlavorMixing -> False];
(* the one-point vertex of the tadpole constant has no generic coupling in FeynArts' Lorentz.gen (InitializeModel::nogeneric,
   and then the model does not load); MadLoop has no tadpole diagrams, and only the R2 vertices are used *)
lagRenNR$ = lagRenNR$ /. FR$deltat[_] -> 0;
Print["renormalized: ", Round[AbsoluteTime[] - t0NR$], " s;  counterterm constants: ",
  Union[Cases[Coefficient[Expand[lagRenNR$], FR$CT], (h : FR$delta | FR$deltaZ | FR$deltat)[x___] :> h[x], Infinity]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["SM_ren"], DeleteDirectory["SM_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "SM_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "SM_ren"]];
