(* ::Package:: *)

(* ::Title:: *)
(*Step (10): the abelian Higgs model against DRalgo (dimensional reduction)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (10).  The U(1) gauge field with one complex scalar of charge 1,*)
(*V = msq Phi^+ Phi + lam (Phi^+ Phi)^2 (msq = -m^2; DRalgo's real components Phi = (phi1 + i psi1)/sqrt 2), reduced with*)
(*DRalgo 1.5.0 to the 3D EFT (soft: A_i, A_0, Phi) and to the ultrasoft EFT (A_0 integrated out).*)
(*  (a) LO 3D parameters against the hand values: g3^2 = e^2 T, lam3 = lam T, msq3 = msq + (lam/3 + e^2/4) T^2, Debye mass*)
(*      e^2 T^2/3, A_0 - Phi coupling lamVL = 2 e^2 T (the A_0 mass m_D^2 + e^2 T phi3^2 = m_D^2 + e^2 phi^2);*)
(*  (b) the 4D beta functions against Eq. (rge);*)
(*  (c) the 4D potential rebuilt from the 3D EFT at one-loop accuracy (LO + one-loop matching + 3D one-loop, with the*)
(*      hard-mode field normalization phi3^2 = (1 + delta) phi^2/T, delta = -3 e^2 L_b/K) against the daisy-resummed*)
(*      high-T potential of thermal.wl (Arnold-Espinosa, Landau gauge): the phi-derivative of the difference vanishes;*)
(*  (d) the ultrasoft EFT: msq_US = msq3 - m_D lamVL/(8 pi), lam_US = lam3 - lamVL^2/(32 pi m_D): the general form with*)
(*      D - e^3/(8 sqrt3 pi), 2E/3, lam_T - sqrt3 e^3/(8 pi); T_c and phi_c/T_c at leading order against the daisy*)
(*      potential of thermal.wl (results/thermal.csv) for MH = 5/2 and 1/2;*)
(*  results/thermal_dralgo.csv.*)
(*Batch: wolframscript -file thermal_dralgo.wl (DRalgo needs GroupMath; run in a kernel of its own).*)


DRalgo`DRalgo`$LoadGroupMath = True;
Quiet[Get["DRalgo`DRalgo`"]];
srcDirTD$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTD$ = FileNameJoin[{srcDirTD$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;


(* ::Section:: *)
(*(a) the model and the dimensional reduction*)


Group = {"U1"}; CouplingName = {g1}; RepAdjoint = {0}; RepScalar = {{{1}, "C"}}; RepFermion = {};
{gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJC, \[Mu]IJ, Ysff, YsffC} =
  AllocateTensors[Group, RepAdjoint, CouplingName, RepFermion, RepScalar];
InputInv = {{1, 1}, {True, False}};
massTerm$ = CreateInvariant[Group, RepScalar, InputInv][[1]] // Simplify;
\[Mu]ij = GradMass[msq massTerm$] // Simplify // SparseArray;
\[Lambda]4 = GradQuartic[lam massTerm$^2];
ImportModelDRalgo[Group, gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJ, \[Mu]IJC, Ysff, YsffC, Verbose -> False];
PerformDRhard[];
cpl$ = Association[PrintCouplings[]];
tmp$ = Association[PrintTemporalScalarCouplings[]];
mdLO$ = First[Values[PrintDebyeMass["LO"]]];
mLO$ = msq3d /. PrintScalarMass["LO"]; mNLO$ = msq3d /. PrintScalarMass["NLO"];
lamVL$ = First[Select[Normal[tmp$], ! FreeQ[#[[1]], \[Lambda]VL] &]][[2]];
Print["(a) mass invariant Phi^+ Phi = ", massTerm$];
lo$[x_] := Total[Select[List @@ Expand[x], FreeQ[#, Pi] &]];     (* tree-level part: the one-loop matching carries 1/pi^2 *)
Print["(a) LO: g3^2 = ", lo$[cpl$[g13d^2]], ", lam3 = ", lo$[cpl$[lam3d]], ", msq3 = ", mLO$, ", Debye mass^2 = ", mdLO$,
  ", lamVL = ", lo$[lamVL$]];
Print["(a) against the hand values (expect 0): ", Simplify[{lo$[cpl$[g13d^2]] - g1^2 T, lo$[cpl$[lam3d]] - lam T,
    mLO$ - (msq + (lam/3 + g1^2/4) T^2), mdLO$ - g1^2 T^2/3, lo$[lamVL$] - 2 g1^2 T}]];


(* ::Section:: *)
(*(b) 4D beta functions*)


beta$ = Association[BetaFunctions4D[]];
Print["(b) DRalgo: ", InputForm[Normal[beta$]]];
Print["(b) against Eq. (rge) (d e^2/d ln mu = 2 e beta_e = 2 e^4/(3K), beta_lam, d msq/d ln mu = msq (8 lam - 6 e^2)/K)",
  " (expect 0): ", Simplify[{beta$[g1^2] - 2 g1^4/(3 KK), beta$[lam] - (20 lam^2 - 12 g1^2 lam + 6 g1^4)/KK,
     beta$[msq] - msq (8 lam - 6 g1^2)/KK}]];


(* ::Section:: *)
(*(c) the 4D potential from the 3D EFT at one-loop accuracy*)


(* one-loop part of the NLO 3D mass: drop the two-loop terms (proportional to T^2 or to the 3D couplings) *)
oneLoop$[x_] := (x /. {lam3d -> 0, g13d -> 0, \[Lambda]VL[_] -> 0}) /. T -> 0;
m3one$ = Simplify[oneLoop$[mNLO$]];
lam3$ = cpl$[lam3d];
Print["(c) one-loop part of the NLO 3D mass: ", InputForm[m3one$]];
(* hbar counts the one-loop pieces: the thermal masses (T^2), the matching (L_b), the field normalization and the 3D loop;
   delta times the thermal mass is of two-loop order *)
delta$ = -3 g1^2 Lb/KK;
phi3$ = phi Sqrt[(1 + hb delta$)/T];
lam3h$ = lo$[lam3$] + hb (lam3$ - lo$[lam3$]);
piS$ = (lam/3 + g1^2/4) T^2;
cube3$ = -1/(12 Pi) (2 (g1^2 T phi3^2)^(3/2) + (mdLO$ + (2 g1^2 T) phi3^2/2)^(3/2) +
      (mLO$ + 3 lam T phi3^2)^(3/2) + (mLO$ + lam T phi3^2)^(3/2));
vDR$ = T ((msq + hb piS$ + hb m3one$) phi3$^2/2 + lam3h$ phi3$^4/4) + hb T (cube3$ /. phi3 -> phi/Sqrt[T]);
(* the hand potential of thermal.wl (daisy, Landau), msq = -m2, one-loop pieces times hb *)
mh2$ = msq + 3 lam phi^2; mG2$ = msq + lam phi^2; mA2$ = g1^2 phi^2;
hT0$[x_, c_] := hb x T^2/24 + hb x^2/(64 Pi^2) (3/2 - Lb - c);
cubeH$[x_] := -hb T/(12 Pi) x^(3/2);
vHand$ = msq phi^2/2 + lam phi^4/4 + hT0$[mh2$, 3/2] + hT0$[mG2$, 3/2] + 3 hT0$[mA2$, 5/6] +
   cubeH$[mh2$ + (lam/3 + g1^2/4) T^2] + cubeH$[mG2$ + (lam/3 + g1^2/4) T^2] + 2 cubeH$[mA2$] + cubeH$[mA2$ + g1^2 T^2/3];
diffTD$ = Simplify[PowerExpand[Normal[Series[D[vHand$ - vDR$, phi], {hb, 0, 1}]]], T > 0 && phi > 0 && g1 > 0];
Print["(c) d/dphi [thermal.wl daisy potential - (DRalgo LO + one-loop matching + 3D one loop)] to one-loop order: ", diffTD$];
Print["(c) the same without the field normalization (delta = 0): ",
  InputForm[Factor[Simplify[PowerExpand[Normal[Series[D[vHand$ - (vDR$ /. delta$ -> 0 /. phi3$ -> phi/Sqrt[T]), phi],
        {hb, 0, 1}]]] /. hb -> 1]]]];


(* ::Section:: *)
(*(d) the ultrasoft EFT*)


PerformDRsoft[{}];
cplUS$ = Association[PrintCouplingsUS[]];
mUS$ = msq3dUS /. PrintScalarMassUS["LO"];
lead$ = {lam3d -> lam T, g13d -> g1 Sqrt[T], \[Lambda]VL[1] -> 2 g1^2 T, \[Mu]sqU1 -> g1^2 T^2/3, msq3d -> mLO$};
mUSlo$ = Simplify[mUS$ /. lead$, T > 0 && g1 > 0];
lamUSlo$ = Simplify[cplUS$[lam3dUS] /. lead$, T > 0 && g1 > 0];
Print["(d) LO ultrasoft: msq_US = ", InputForm[mUSlo$], ", lam_US = ", InputForm[lamUSlo$]];
Print["(d) against the screened general form (expect 0): D shift ",
  Simplify[(mUSlo$ - mLO$)/(2 T^2) + g1^3/(8 Sqrt[3] Pi), g1 > 0], ", lam shift ",
  Simplify[lamUSlo$/T - lam + Sqrt[3] g1^3/(8 Pi), g1 > 0 && T > 0]];
(* T_c, phi_c/T_c of the LO ultrasoft general form (with lam_T of Eq. (b) of thermal.wl), against thermal.wl *)
lbOf$[mu_, tt_] := 2 Log[mu/tt] + 2 EulerGamma - 2 Log[4 Pi];
ref$ = Import[FileNameJoin[{resDirTD$, "thermal.csv"}], "CSV", "HeaderLines" -> 1];
rowsTD$ = Table[Module[{e = 1/2, mh = r[[1]], lamv, m2v, dd, ee, lt, t0, tc, pc},
    lamv = e^2 mh^2/2; m2v = 4 lamv;
    dd = (4 lamv + 3 e^2)/24 - e^3/(8 Sqrt[3] Pi); ee = 2/3 e^3/(4 Pi); t0 = Sqrt[m2v/(2 dd)]; tc = t0;
    Do[lt = lamv + 3 e^4/KK (2/3 - lbOf$[1, tc]) - Sqrt[3] e^3/(8 Pi); tc = Sqrt[t0^2/(1 - ee^2/(lt dd))], {8}];
    pc = 2 ee tc/lt;
    Print["(d) MH = ", mh, ": ultrasoft general form T_c = ", N[tc, 8], ", phi_c/T_c = ", N[pc/tc, 6],
      ";  thermal.wl daisy ", N[r[[7]], 8], ", ", N[r[[8]], 6], ";  without screening ", N[r[[3]], 8], ", ", N[r[[4]], 6]];
    {mh, N[tc], N[pc/tc], r[[7]], r[[8]]}], {r, ref$}];
Export[FileNameJoin[{resDirTD$, "thermal_dralgo.csv"}],
  Prepend[Map[ToString[CForm[N[#, 12]]] &, rowsTD$, {2}], {"MH", "Tc_US_general", "phic_Tc_US_general", "Tc_daisy", "phic_Tc_daisy"}],
  "CSV"];
Print["(d) written results/thermal_dralgo.csv"];
