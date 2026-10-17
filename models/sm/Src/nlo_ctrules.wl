(* ::Package:: *)

(* ::Title:: *)
(*Step (9d): the counterterm Feynman rules of the note's model with symbolic renormalization constants (FeynRules)*)


(* ::Text:: *)
(*FeynRules + NLOCT: the renormalized Lagrangian of nlo_renormalize.wl (Feynman gauge, the tadpole constant set to 0) and*)
(*  ctSym:  the Feynman rules of its first order in FR$CT, in terms of FR$delta[{p}] (parameters aEWM1, aS, MZ, MW, MH, the*)
(*          fermion masses) and FR$deltaZ[{f1, f2}, ...] (fields);*)
(*  tadSym: the Feynman rules of dL/dH (H -> H + dvT in the expanded Lagrangian, first order in dvT): with dvT = T/M_H^2*)
(*          (iT the tadpole) they are the tadpole diagrams that MadLoop does not generate, the FJ scheme in counterterm form.*)
(*Writes Src/generated/SM_CTsym.m for nlo_dz.wl and nlo_ufo.wl.  Batch: wolframscript -file nlo_ctrules.wl  (in a fresh kernel)*)


srcDirCR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirCR$];
LoadModel["SM.fr"];
t0CR$ = AbsoluteTime[];
lagCR$ = LSM /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
lagRenCR$ = OnShellRenormalization[lagCR$, FlavorMixing -> False] /. FR$deltat[_] -> 0;
lagCTCR$ = Coefficient[Expand[lagRenCR$], FR$CT];
Print["counterterm Lagrangian: ", Round[AbsoluteTime[] - t0CR$], " s"];
ctSymCR$ = FeynmanRules[lagCTCR$, FlavorExpand -> True, ScreenOutput -> False];
Print["counterterm vertices: ", Length[ctSymCR$], ";  ", Round[AbsoluteTime[] - t0CR$], " s"];
(* the shift of the Higgs field in the expanded Lagrangian (derivatives of H are not shifted) *)
lagExpCR$ = ExpandIndices[lagCR$, FlavorExpand -> True];
lagTadCR$ = Coefficient[Expand[(lagExpCR$ /. del[H, mu_] :> dH$[mu]) /. H -> H + dvT /. dH$[mu_] :> del[H, mu]], dvT];
tadSymCR$ = FeynmanRules[lagTadCR$, FlavorExpand -> True, ScreenOutput -> False];
Print["tadpole counterterm vertices: ", Length[tadSymCR$], " (legs ", Union[Length /@ tadSymCR$[[All, 1]]], ");  ",
  Round[AbsoluteTime[] - t0CR$], " s"];
Print["the one-leg vertex (expect -I MH^2 = -2 I lam vev^2: times dvT the tadpole -I T itself, left out of the UFO): ",
  Simplify[Select[tadSymCR$, Length[#[[1]]] == 1 &] /. muH2 -> lam vev^2]];
Put[<|"ctSym" -> ctSymCR$, "tadSym" -> tadSymCR$|>, FileNameJoin[{srcDirCR$, "generated", "SM_CTsym.m"}]];
Print["written: generated/SM_CTsym.m"];
