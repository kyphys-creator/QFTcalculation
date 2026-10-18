(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 5 of 7: the MS-bar (FJ) parameter counterterms, the CKM counterterm and the tadpole shift for the CKM UFO*)


(* ::Text:: *)
(*As the SM note's nlo_fjdelta.wl, with the CKM matrix.  The UFO's external parameters p = aEWM1, aS, MZ, MW, MH and the*)
(*fermion masses get the MS-bar counterterms of the FJ scheme, p0 = p + FR$delta[{p}], FR$delta[{p}] = (1/FR$Eps)(1/2)*)
(*dp/dln mu, the one-loop running by the chain rule (g = e/sw, g' = e/cw, v = 2 MW sw/e, lambda = MH^2/(2 v^2),*)
(*mu^2 = MH^2/2, y_f = sqrt(2) m_f/v; FJ: v^2 = mu^2/lambda runs with its 1/lambda terms).  With the CKM matrix the quark*)
(*masses run as in note Eq. (yrun) (the partner of the SM note is replaced by sum_k |V_ik|^2 y_dk^2, sum_k |V_kj|^2 y_uk^2);*)
(*the gauge couplings, lambda and mu^2 do not depend on V at one loop.  The CKM counterterm is dV = (1/FR$Eps)(1/2)*)
(*dV/dln mu of Eq. (Vrun) (the phase convention of the note), a general complex matrix.  The tadpole shift is*)
(*dvT = T/MH^2 with T of the SM note's step (3) (V does not enter T), Feynman gauge.  Checks: K de/e = 11/6 e^2; the*)
(*poles of the quark masses against the diagonal self-energies of step (3) (the condition of the SM note's Eq. (26):*)
(*K (Sigma^V + Sigma^S)|pole = (1/4) dln m^2/dln mu, with Sigma^V = (Sigma^L + Sigma^R)/2), with the CKM matrix.*)
(*Writes Src/generated/SM_CKM_FJdelta.m.  Batch: wolframscript -file nlo_ckm_fjdelta.wl*)


srcDirFD$ = DirectoryName[$InputFileName];
KK = 16 Pi^2;
upF$ = {MU, MC, MT}; dnF$ = {MD, MS, MB}; lepF$ = {Me, MMU, MTA};
vv$ = 2 MW sw/ee; gg$ = ee/sw; gp$ = ee/cw; la$ = MH^2/(2 vv$^2); mu2$ = MH^2/2;
yf$[m_] := Sqrt[2] m/vv$;
gs$ = Sqrt[4 Pi aS];
vM$ = Array[CKM, {3, 3}]; vMc$ = Conjugate[vM$];
abs2$[i_, j_] := CKM[i, j] Conjugate[CKM[i, j]];
Tsum$ = Sum[3 yf$[m]^2, {m, Join[upF$, dnF$]}] + Sum[yf$[m]^2, {m, lepF$}];
(* the SM note's Eq. (beta), times K *)
bg$ = -19/6 gg$^3; bgp$ = 41/6 gp$^3; bgs$ = -7 gs$^3;
bla$ = 24 la$^2 + 4 la$ Tsum$ - 2 (Sum[3 yf$[m]^4, {m, Join[upF$, dnF$]}] + Sum[yf$[m]^4, {m, lepF$}]) -
   3 la$ (3 gg$^2 + gp$^2) + 3/8 (2 gg$^4 + (gg$^2 + gp$^2)^2);
gmu2$ = mu2$ (12 la$ + 2 Tsum$ - 9/2 gg$^2 - 3/2 gp$^2);
(* note Eq. (yrun), K d ln y/d ln mu *)
dlny$[m_] := Module[{y = yf$[m], i},
   Which[
    MemberQ[upF$, m], i = Position[upF$, m][[1, 1]];
     3/2 y^2 - 3/2 Sum[abs2$[i, k] yf$[dnF$[[k]]]^2, {k, 3}] + Tsum$ - 8 gs$^2 - 9/4 gg$^2 - 17/12 gp$^2,
    MemberQ[dnF$, m], i = Position[dnF$, m][[1, 1]];
     3/2 y^2 - 3/2 Sum[abs2$[k, i] yf$[upF$[[k]]]^2, {k, 3}] + Tsum$ - 8 gs$^2 - 9/4 gg$^2 - 5/12 gp$^2,
    True, 3/2 y^2 + Tsum$ - 9/4 gg$^2 - 15/4 gp$^2]];
dlnv2$ = gmu2$/mu2$ - bla$/la$;
dlne$ = sw^2 bg$/gg$ + cw^2 bgp$/gp$;
run$ = <|
   aEWM1 -> -2 (4 Pi/ee^2) dlne$,
   aS -> 2 gs$ bgs$/(4 Pi),
   MW -> MW (bg$/gg$ + dlnv2$/2),
   MZ -> MZ ((gg$ bg$ + gp$ bgp$)/(gg$^2 + gp$^2) + dlnv2$/2),
   MH -> MH gmu2$/(2 mu2$),
   Splice[Table[m -> m (dlny$[m] + dlnv2$/2), {m, Join[upF$, dnF$, lepF$]}]]|>;
swcw$ = {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]};
simp$[x_] := Simplify[x /. swcw$, Assumptions -> MZ > MW > 0];
deltaRules$ = Normal[KeyValueMap[FR$delta[{#1}, {}] -> 1/FR$Eps (1/2) #2/KK &, run$]];
Print["K de/e = ", simp$[dlne$/2], "  (expect 11/6 ee^2)"];
Print["V = 1: the down-quark running is the SM note's (expect 0): ",
  Simplify[(dlny$[MB] - (3/2 (yf$[MB]^2 - yf$[MT]^2) + Tsum$ - 8 gs$^2 - 9/4 gg$^2 - 5/12 gp$^2)) /. CKM[i_, j_] :> KroneckerDelta[i, j] /.
     Conjugate[KroneckerDelta[__]] -> KroneckerDelta[3, 3]]];

(* the CKM counterterm, note Eqs. (dV), (Vrun): K dV/dln mu, as wud_renormalized.wl *)
kdVdlnmu$ = Module[{yu = yf$ /@ upF$, yd = yf$ /@ dnF$, hd, hu, au, ad},
   hd = vM$ . DiagonalMatrix[yd^2] . Transpose[vMc$]; hu = Transpose[vMc$] . DiagonalMatrix[yu^2] . vM$;
   au = Table[If[i == k, 0, -3/2 (yu[[i]]^2 + yu[[k]]^2)/(yu[[k]]^2 - yu[[i]]^2) hd[[i, k]]], {i, 3}, {k, 3}];
   ad = Table[If[k == j, 0, -3/2 (yd[[k]]^2 + yd[[j]]^2)/(yd[[j]]^2 - yd[[k]]^2) hu[[k, j]]], {k, 3}, {j, 3}];
   -au . vM$ + vM$ . ad];
dV$ = kdVdlnmu$/(2 KK FR$Eps);

(* check: the quark-mass poles against the diagonal self-energies of step (3) (1PI + tadpole, general R_xi) *)
sig3$ = Association[Get[FileNameJoin[{srcDirFD$, "results", "oneloop_ckm_sigma.m"}]]];
kRule$ = {Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
toCK$ = {vR[i_, j_] :> (CKM[i, j] + Conjugate[CKM[i, j]])/2, vI[i_, j_] :> (CKM[i, j] - Conjugate[CKM[i, j]])/(2 I),
   cK[i_, j_] :> CKM[i, j], cKc[i_, j_] :> Conjugate[CKM[i, j]]};
poleOf$[x_] := SeriesCoefficient[x /. {A0[m2_] :> m2/ep, B0[__] -> 1/ep, C0[__] -> 0, PaVe[__] -> 0} /. D -> 4 - 2 ep, {ep, 0, -1}];
sg$[sec_, i_, n_] := Total[sig3$[sec][[i, i, All, n]]] /. kRule$ /. toCK$ /. gS -> Sqrt[4 Pi aS] /. CF -> 4/3;
(* a unitary V with rational entries (step (5)): the poles are then compared exactly *)
vPy$ = Module[{s12 = 8/17, s23 = 7/25, s13 = 3/5, c12, c23, c13},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13/ph}, {-s12 c23 - c12 s23 s13 ph, c12 c23 - s12 s23 s13 ph, s23 c13},
    {s12 s23 - c12 c23 s13 ph, -c12 s23 - s12 c23 s13 ph, c23 c13}}];
pyRule$ = {Conjugate[CKM[i_, j_]] :> (vPy$[[i, j]] /. ph -> 1/ph), CKM[i_, j_] :> vPy$[[i, j]]};
Print["check: K (Sigma^V + Sigma^S)|pole - (1/4) dln m^2/dln mu for u, c, t, d, s, b (expect all 0): ",
  Table[Simplify[Together[(poleOf$[(sg$[sec, i, 1] + sg$[sec, i, 2])/2 + sg$[sec, i, 3]] - 1/4 2 run$[m]/m) /. pyRule$ /.
        {MZ -> MW/cw} /. cw -> Sqrt[1 - sw^2] /. {vev -> vv$} /. {lam -> la$} /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1}], 0 < sw < 1 && MW > 0],
   {sec, {"U", "D"}}, {i, 3}, {m, {If[sec === "U", upF$[[i]], dnF$[[i]]]}}]];

(* the tadpole shift dvT = T/MH^2 with T of the SM note's step (3), Feynman gauge (V does not enter) *)
sigSM$ = Association[Get[FileNameJoin[{ParentDirectory[srcDirFD$], "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
a0$ = A0[m2_] :> If[m2 === 0, 0, m2 (1/ep + 1 - Log[m2/FR$MU^2])];
tK$ = sigSM$["T"] /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
tLau$ = Module[{y = Simplify[(tK$ /. a0$) /. D -> 4 - 2 ep]}, Simplify /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
dvT$ = (tLau$[[1]]/FR$Eps + tLau$[[2]])/(KK MH^2);
Print["K MH^2 dvT: pole ", Short[Simplify[tLau$[[1]]], 3]];
Put[<|"delta" -> deltaRules$, "dV" -> dV$, "dvT" -> dvT$|>, FileNameJoin[{srcDirFD$, "generated", "SM_CKM_FJdelta.m"}]];
Print["written: generated/SM_CKM_FJdelta.m"];
