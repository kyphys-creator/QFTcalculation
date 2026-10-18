(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 3 of 7: the counterterm Feynman rules of the note's CKM model with symbolic renormalization constants*)


(* ::Text:: *)
(*As the SM note's nlo_ctrules.wl, for SM_CKM.fr (FeynRules + NLOCT, Feynman gauge):*)
(*  ctSym:  the Feynman rules of the first order in FR$CT of the renormalized Lagrangian of nlo_ckm_renormalize.wl (the*)
(*          same quark mixing pairs), in terms of FR$delta[{p}] (aEWM1, aS, MZ, MW, MH, the fermion masses) and*)
(*          FR$deltaZ[{f1, f2}, ...] (fields, with the off-diagonal quark constants).  NLOCT's constants of the CKM*)
(*          parameters s12, s23, s13, dCKM are set to 0: the CKM counterterm of the note is a general matrix dV (Eq. (dV),*)
(*          the phase convention of Eq. (Vrun)), which is not a change of the four standard parameters;*)
(*  dvSym:  the Feynman rules of the CKM counterterm, the first order in eps of L(V -> V + eps dVsym) (the charged*)
(*          currents and the charged Yukawa couplings; the neutral ones contain V^dagger V = 1 and get none, as*)
(*          V^dagger dV is anti-hermitian);*)
(*  tadSym: the Feynman rules of dL/dH (H -> H + dvT), the tadpoles of the FJ scheme in counterterm form.*)
(*Writes Src/generated/SM_CKM_CTsym.m for nlo_ckm_dz.wl and nlo_ckm_ufo.wl.*)
(*Batch: wolframscript -file nlo_ckm_ctrules.wl  (in a fresh kernel)*)


srcDirCR$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirCR$];
LoadModel["SM_CKM.fr"];
t0CR$ = AbsoluteTime[];
xi1CR$ = {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
lagCR$ = LSM /. xi1CR$;
mixCR$ = {{u, c}, {u, t}, {c, t}, {d, s}, {d, b}, {s, b}};
ckmParCR$ = {s12, s23, s13, dCKM};
lagRenCR$ = OnShellRenormalization[lagCR$, FlavorMixing -> mixCR$] /. FR$deltat[_] -> 0;
lagCTCR$ = Coefficient[Expand[lagRenCR$], FR$CT] /. (FR$delta[{#}, {}] -> 0 & /@ ckmParCR$);
Print["counterterm Lagrangian: ", Round[AbsoluteTime[] - t0CR$], " s;  constants left: ",
  Union[Cases[lagCTCR$, FR$delta[{p_}, ___] :> p, Infinity]]];
ctSymCR$ = FeynmanRules[lagCTCR$, FlavorExpand -> True, ScreenOutput -> False];
Print["counterterm vertices: ", Length[ctSymCR$], ";  ", Round[AbsoluteTime[] - t0CR$], " s"];

(* the CKM counterterm: V -> V + eps dVsym in the parts of the Lagrangian with V (Conjugate[V] first) *)
lagDVCR$ = Coefficient[Expand[(LFermionSM + LYukawaSM) /. xi1CR$ /. {Conjugate[CKM[a_, b_]] :> Conjugate[CKM[a, b]] + epsCR$ Conjugate[dVsym[a, b]],
       CKM[a_, b_] :> CKM[a, b] + epsCR$ dVsym[a, b]}], epsCR$];
dvSymCR$ = FeynmanRules[lagDVCR$, FlavorExpand -> True, ScreenOutput -> False];
Print["CKM counterterm vertices: ", Length[dvSymCR$], " (fields ", Union[Sort /@ (dvSymCR$[[All, 1, All, 1]] /. anti[x_] :> x)], ");  ",
  Round[AbsoluteTime[] - t0CR$], " s"];
(* check: the tree vertices with V, differentiated, are the same (W u d, G u d and conjugates) *)
treeCR$ = FeynmanRules[(LFermionSM + LYukawaSM) /. xi1CR$, FlavorExpand -> True, ScreenOutput -> False];
withVCR$ = Select[treeCR$, !FreeQ[#[[2]], CKM] &];
(* FeynRules writes the matrix entries as CKM[Index[Generation, i], Index[Generation, j]] (dVsym likewise) *)
genCR$[i_] := Index[Generation, i];
(* V and V^* as independent variables for the derivatives *)
derivCR$ = Module[{x = #[[2]] /. Conjugate[CKM[a_, b_]] :> ckmC$[a, b]},
     {#[[1]], Sum[D[x, CKM[genCR$[i], genCR$[j]]] dVsym[genCR$[i], genCR$[j]] +
         D[x, ckmC$[genCR$[i], genCR$[j]]] Conjugate[dVsym[genCR$[i], genCR$[j]]], {i, 3}, {j, 3}] /.
       ckmC$[a_, b_] :> Conjugate[CKM[a, b]]}] & /@ withVCR$;
Print["check: CKM counterterm vertices minus derivatives of the tree vertices (expect {0}): ",
  Union[Simplify /@ (MergeVertices[dvSymCR$, {#[[1]], -#[[2]]} & /@ derivCR$][[All, 2]])], ";  tree vertices with V: ", Length[withVCR$]];

(* the shift of the Higgs field in the expanded Lagrangian (derivatives of H are not shifted) *)
lagExpCR$ = ExpandIndices[lagCR$, FlavorExpand -> True];
lagTadCR$ = Coefficient[Expand[(lagExpCR$ /. del[H, mu_] :> dH$[mu]) /. H -> H + dvT /. dH$[mu_] :> del[H, mu]], dvT];
tadSymCR$ = FeynmanRules[lagTadCR$, FlavorExpand -> True, ScreenOutput -> False];
Print["tadpole counterterm vertices: ", Length[tadSymCR$], " (legs ", Union[Length /@ tadSymCR$[[All, 1]]], ");  ",
  Round[AbsoluteTime[] - t0CR$], " s"];
Print["the one-leg vertex (expect -I MH^2 = -2 I lam vev^2: times dvT the tadpole -I T itself, left out of the UFO): ",
  Simplify[Select[tadSymCR$, Length[#[[1]]] == 1 &] /. muH2 -> lam vev^2]];
Put[<|"ctSym" -> ctSymCR$, "dvSym" -> dvSymCR$, "tadSym" -> tadSymCR$|>, FileNameJoin[{srcDirCR$, "generated", "SM_CKM_CTsym.m"}]];
Print["written: generated/SM_CKM_CTsym.m;  ", Round[AbsoluteTime[] - t0CR$], " s"];
