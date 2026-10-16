(* ::Package:: *)

(* ::Title:: *)
(*Step (4): charge renormalization and the running of v_beta from the one-loop functions of step (3) (SM note)*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (K Sigma in A0, B0, D; general xiA, xiZ, xiW; photon mass MA).*)
(*  (a) MS-bar charge renormalization from the two-point functions: dZAA = -d(Sigma_T^AA)/dk^2|UV,*)
(*      dZZA = 2 Sigma_T^AZ(0)|UV/MZ^2, and dZe = -dZAA/2 + (sw/(2 cw)) dZZA (the sign of the mixing term is the*)
(*      opposite of Denner's, A = -A_Denner) must be (11/6) e^2/K Delta for independent xi's (Eq. (erun)).*)
(*  (b) Eq. (vbeta): d ln v_beta/dln mu = (1/2) dln v^2/dln mu (Eq. (vrun)) + d(Delta v/v)/dln mu with Delta v = T/MH^2*)
(*      from the computed T (its ln mu^2 dependence: d A0(m^2)/dln mu = 2 m^2), against -gamma_Phi^L +*)
(*      [xiZ (g^2 + g'^2) + 2 xiW g^2]/(4 K).*)
(*No FeynCalc needed.  Batch: wolframscript -file rg_feyncalc_check.wl*)


srcDirRC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
sig$ = Association[Get[FileNameJoin[{srcDirRC$, "results", "oneloop_sigma.m"}]]];
KK = 16 Pi^2;
kRule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
uv$[x_] := Simplify[SeriesCoefficient[(x /. kRule$) /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep,
     {ep, 0, -1}]];
(* sequential: MZ -> MW/cw introduces cw *)
toSw$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];


(* ::Section:: *)
(*(a) charge*)


uvAA$ = Simplify[uv$[sig$["AA"][[1]]] /. MA -> 0 // toSw$];
uvAZ0$ = Simplify[(uv$[sig$["AZ"][[1]]] /. MA -> 0 // toSw$) /. kk2 -> 0];
dZAA$ = -D[uvAA$, kk2];                         (* K times the Delta coefficients *)
dZZA$ = 2 uvAZ0$/(MW^2/(1 - sw^2));
dZe$ = Simplify[-dZAA$/2 + sw/(2 Sqrt[1 - sw^2]) dZZA$, 0 < sw < 1];
Print["(a) K dZAA = ", Simplify[dZAA$], ",  K dZZA = ", Simplify[dZZA$, 0 < sw < 1]];
Print["(a) K dZe = ", dZe$, "   (expect 11/6 e^2 for independent xiA, xiZ, xiW)"];
Print["(a) the same with Denner's sign of the mixing term (-): ",
  Simplify[-dZAA$/2 - sw/(2 Sqrt[1 - sw^2]) dZZA$, 0 < sw < 1]];


(* ::Section:: *)
(*(b) v_beta*)


tK$ = sig$["T"];                                (* K T, exact in D *)
(* d/dln mu of the MS-bar finite part of K T: each A0(m^2) gives 2 m^2 *)
dTK$ = Simplify[(tK$ /. D -> 4) /. A0[m2_] :> 2 m2];
vev$ = 2 MW sw/ee;
gSq$ = ee^2/sw^2; gpSq$ = ee^2/(1 - sw^2); lam$ = MH^2/(2 vev$^2);
yf$[m_] := Sqrt[2] m/vev$;
ups$ = {{MU, MD}, {MC, MS}, {MT, MB}}; leps$ = {Me, MMU, MTA};
TT$ = Sum[3 yf$[p[[1]]]^2 + 3 yf$[p[[2]]]^2, {p, ups$}] + Sum[yf$[m]^2, {m, leps$}];
NY4$ = Sum[3 yf$[p[[1]]]^4 + 3 yf$[p[[2]]]^4, {p, ups$}] + Sum[yf$[m]^4, {m, leps$}];
dlnv2$ = (-12 lam$ - 2 TT$ + 9/2 gSq$ + 3/2 gpSq$ + 2/lam$ NY4$ - 3/(8 lam$) (2 gSq$^2 + (gSq$ + gpSq$)^2))/KK;
dlnvb$ = dlnv2$/2 + (dTK$/KK)/(MH^2 vev$);
gammaPhiL$ = (TT$ - 9/4 gSq$ - 3/4 gpSq$)/KK;
predVb$ = -gammaPhiL$ + (xiZ (gSq$ + gpSq$) + 2 xiW gSq$)/(4 KK);
dVb$ = Simplify[toSw$[dlnvb$ - predVb$], 0 < sw < 1];
Print["(b) d ln v_beta/dln mu from T - Eq. (vbeta) = ", dVb$, "   (expect 0)"];
Print["(b) d ln v_beta/dln mu in Landau gauge + gamma_Phi^L = ", Simplify[toSw$[(dlnvb$ /. {xiZ -> 0, xiW -> 0}) + gammaPhiL$], 0 < sw < 1],
  "   (expect 0)"];
Print["Summary: ", {Simplify[dZe$ - 11/6 ee^2], dVb$}];
