(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 3 of 3: UFOs with counterterm and R2 vertices (on-shell and MS-bar) for MadLoop*)


(* ::Text:: *)
(*FeynRules: read Src/generated/PsYukawa_CT.nlo, compare NLOCT's counterterms and R2 vertices with the note, and write two*)
(*UFOs (overwritten):*)
(*  Src/generated/PsYukawa_NLO_OS_UFO     NLOCT's counterterms: fields and masses on shell, yps and lamphi MS-bar*)
(*  Src/generated/PsYukawa_NLO_MSbar_UFO  MS-bar: only the poles of the counterterm vertices, i.e. Eq. (5)*)
(*Both carry NLOCT's R2 vertices (MadLoop builds the numerators in four dimensions; R2 restores the rational terms).*)
(*NLOCT's on-shell counterterms are compared numerically (m = mu = 1, M = 0.7, y = lambda = 1) with the hand values*)
(*(App. scat and scatB of the note), in terms of the unrenormalized self-energies with DeltaUV = 1/FR$Eps:*)
(*  deltaZphi = Sigma_phi'(m^2),  2 m deltam = -Sigma_phi(m^2),*)
(*  deltaZpsi = Sigma_V(M^2) + 2 M^2 (Sigma_V' + Sigma_S')(M^2),  deltaM = -M (Sigma_V + Sigma_S)(M^2),*)
(*  deltay = (5/2) y^3 DeltaUV/(4 Pi)^2,  deltalambda = (3 lambda^2/2 - 24 y^4 + 4 lambda y^2) DeltaUV/(4 Pi)^2*)
(*(the coupling counterterms are those of Eq. (5) minus the pole parts of the field renormalization).*)
(*FeynmanGauge = True writes gauge = [0, 1] (the model has no gauge field); MadGraph refuses non-QCD loops for a model*)
(*that does not allow Feynman gauge.*)
(**)
(*Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_ufo.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_ufo.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*FeynRules, the model and the NLOCT counterterms*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["PsYukawa.fr"];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["PsYukawa_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist],
  ";  UV vertices: ", Length[UV$vertlist]];


(* ::Section:: *)
(*R2 vertices against the hand values*)


(* ::Text:: *)
(*R2 = (D-dimensional numerator, NDR) - (4-dimensional numerator); the difference comes from qhat^2 terms, (D-4) times a pole*)
(*(the argument of the note's appendix on the gamma5 scheme):*)
(*  phi phi:  NDR trace minus the 4-dimensional one = -4 qhat^2  ->  I y^2 (6 M^2 - p^2)/(24 Pi^2),*)
(*  phi psibar psi:  -qhat^2 g5  ->  y^3 g5/(32 Pi^2) = y^3 (ProjP - ProjM)/(32 Pi^2),*)
(*  phi^4:  six boxes, (8 q^2 qhat^2 - 4 qhat^4)  ->  20 I y^4/(4 Pi)^2 = (5/4) I y^4/Pi^2.*)


r2NU$[legs_] := First[Cases[R2$vertlist, {legs, v_} :> v]] /. IPL[_] -> 1;
(* ProjP = (1 + g5)/2, ProjM = (1 - g5)/2; pslash ProjP/M = (pslash +- pslash g5)/2, with slash5[k] standing for pslash g5 *)
sp5NU$ = {TensDot[SlashedP[k_], ProjP][a_, b_] :> (SlashedP[k, a, b] + slash5[k, a, b])/2,
   TensDot[SlashedP[k_], ProjM][a_, b_] :> (SlashedP[k, a, b] - slash5[k, a, b])/2,
   ProjP[a_, b_] :> (IndexDelta[a, b] + Ga[5, a, b])/2, ProjM[a_, b_] :> (IndexDelta[a, b] - Ga[5, a, b])/2};
r2phiNU$ = r2NU$[{{phi, 1}, {phi, 2}}];
r2yNU$ = Expand[r2NU$[{{anti[psi], 1}, {psi, 2}, {phi, 3}}] /. sp5NU$];
r24NU$ = r2NU$[{{phi, 1}, {phi, 2}, {phi, 3}, {phi, 4}}];
Print["R2 phi phi (NLOCT) = ", InputForm[r2phiNU$], "  minus I y^2 (6 M^2 - p^2)/(24 Pi^2) -> ",
  Simplify[r2phiNU$ - I yps^2 (6 Mpsi^2 - SP[2, 2])/(24 Pi^2)]];
Print["R2 phi psibar psi (NLOCT) = ", InputForm[r2yNU$], "  minus y^3 g5/(32 Pi^2) -> ",
  Simplify[r2yNU$ - yps^3 Ga[5, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]/(32 Pi^2)]];
Print["R2 phi^4 (NLOCT) = ", InputForm[r24NU$], "  minus 20 I y^4/(4 Pi)^2 -> ", Simplify[r24NU$ - 20 I yps^4/(4 Pi)^2]];


(* ::Section:: *)
(*UV counterterms against the hand values*)


(* ::Text:: *)
(*Hand values: B functions in MS-bar with mu = FR$MU from their Feynman-parameter integrals (NIntegrate), the self-energies*)
(*with the pole DeltaUV = 1/FR$Eps.  Each NLOCT vertex is compared at m = mu = 1, M = 0.7, y = lambda = 1, coefficient by*)
(*coefficient of 1/FR$Eps and of FR$Eps^0.*)


numNU$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1, FR$MU -> 1};
dxNU$[p2_, ma2_, mb2_, x_] := x mb2 + (1 - x) ma2 - x (1 - x) p2;
b0NU$[p2_?NumericQ, ma2_, mb2_] := -NIntegrate[Log[dxNU$[p2, ma2, mb2, x]], {x, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 20];
b1NU$[p2_?NumericQ, ma2_, mb2_] := NIntegrate[x Log[dxNU$[p2, ma2, mb2, x]], {x, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 20];
b0pNU$[p2_?NumericQ, ma2_, mb2_] := NIntegrate[x (1 - x)/dxNU$[p2, ma2, mb2, x], {x, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 20];
b1pNU$[p2_?NumericQ, ma2_, mb2_] := -NIntegrate[x^2 (1 - x)/dxNU$[p2, ma2, mb2, x], {x, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 20];
a0NU$[m2_] := m2 (1 - Log[m2]);
kNU$ = (4 Pi)^2; dUV$ = 1/FR$Eps;
With[{m2 = 1, bm2 = 49/100, M = 7/10, y = 1, lam = 1},
  handNU$ = <|
    "dZphi" -> -2 y^2/kNU$ (dUV$ + b0NU$[m2, bm2, bm2] + m2 b0pNU$[m2, bm2, bm2]),
    "2mdm" -> (2 y^2 (m2 (dUV$ + b0NU$[m2, bm2, bm2]) - 2 (bm2 dUV$ + a0NU$[bm2])) + lam/2 (m2 dUV$ + a0NU$[m2]))/kNU$,
    "dZpsi" -> y^2/kNU$ (b1NU$[bm2, bm2, m2] - dUV$/2 + 2 bm2 (b1pNU$[bm2, bm2, m2] + b0pNU$[bm2, bm2, m2])),
    "dM" -> -y^2 M/kNU$ (b0NU$[bm2, bm2, m2] + b1NU$[bm2, bm2, m2] + dUV$/2),
    "dy" -> 5/2 y^3 dUV$/kNU$,
    "dlam" -> (3 lam^2/2 - 24 y^4 + 4 lam y^2) dUV$/kNU$|>];
uvNU$[legs_] := First[Cases[UV$vertlist, {legs, v_} :> v]] /. IPL[_] -> 1;
uvPhiNU$ = uvNU$[{{phi, 1}, {phi, 2}}];
uvPsiNU$ = Expand[uvNU$[{{anti[psi], 1}, {psi, 2}}] /. sp5NU$];
uvYNU$ = Expand[uvNU$[{{anti[psi], 1}, {psi, 2}, {phi, 3}}] /. sp5NU$];
uv4NU$ = uvNU$[{{phi, 1}, {phi, 2}, {phi, 3}, {phi, 4}}];
(* NLOCT's vertex forms: phi phi: I [dZphi (p^2 - m^2) - 2 m dm];  psibar psi: I [dZpsi (pslash - M) - dM];
   phi psibar psi: (dy + y dZpsi + y dZphi/2) g5;  phi^4: -I (dlam + 2 lam dZphi) *)
nlNU$ = <|
   "dZphi" -> Coefficient[Expand[uvPhiNU$], SP[2, 2]]/I,
   "2mdm" -> -(Expand[uvPhiNU$] /. SP[2, 2] -> mphi^2)/I,
   "dZpsi" -> Coefficient[uvPsiNU$, SlashedP[2, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]]/I,
   "dM" -> -(Coefficient[uvPsiNU$, IndexDelta[Index[Spin, Ext[1]], Index[Spin, Ext[2]]]]/I + Mpsi Coefficient[uvPsiNU$, SlashedP[2, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]]/I),
   "yvertex" -> Coefficient[uvYNU$, Ga[5, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]],
   "4vertex" -> uv4NU$ I|>;
If[! FreeQ[uvPsiNU$, TensDot], Print["(warning) TensDot left in the psi psi vertex: ", InputForm[uvPsiNU$]]];
Print["UV psibar psi: coefficients of g5 and pslash g5 (parity: expect 0, 0): ",
  Chop[N[{Coefficient[uvPsiNU$, Ga[5, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]],
     Coefficient[uvPsiNU$, slash5[2, Index[Spin, Ext[1]], Index[Spin, Ext[2]]]]} /. numNU$ /. FR$Eps -> 1/3]]];
cmpNU$[x_, h_] := Module[{d = Expand[(x - h) /. numNU$]}, N[{Coefficient[d, FR$Eps, -1], d /. FR$Eps -> Infinity}, 20]];
Print["UV deltaZphi:  NLOCT - hand (1/eps, eps^0) = ", cmpNU$[nlNU$["dZphi"], handNU$["dZphi"]]];
Print["UV 2 m deltam: NLOCT - hand (1/eps, eps^0) = ", cmpNU$[nlNU$["2mdm"], handNU$["2mdm"]]];
Print["UV deltaZpsi:  NLOCT - hand (1/eps, eps^0) = ", cmpNU$[nlNU$["dZpsi"], handNU$["dZpsi"]]];
Print["UV deltaM:     NLOCT - hand (1/eps, eps^0) = ", cmpNU$[nlNU$["dM"], handNU$["dM"]]];
Print["UV Yukawa vertex: NLOCT - (dy + y dZpsi + y dZphi/2) = ",
  cmpNU$[nlNU$["yvertex"], handNU$["dy"] + handNU$["dZpsi"] + handNU$["dZphi"]/2]];
Print["UV phi^4 vertex:  NLOCT - (dlam + 2 lam dZphi) = ", cmpNU$[nlNU$["4vertex"], handNU$["dlam"] + 2 handNU$["dZphi"]]];


(* ::Subsubsection:: *)
(*Inspect: NLOCT's vertices*)


If[$Notebooks,
  TableForm[{{"R2 phi phi", TraditionalForm[r2phiNU$]}, {"R2 phi psibar psi", TraditionalForm[r2yNU$]}, {"R2 phi^4", TraditionalForm[r24NU$]},
    {"UV psibar psi (numerical)", TraditionalForm[N[uvPsiNU$ /. numNU$, 8]]}}]
]


(* ::Section:: *)
(*UFO outputs*)


FeynmanGauge = True;
uvOSNU$ = UV$vertlist;
(* MS-bar: the 1/FR$Eps parts of the counterterm vertices *)
uvMSNU$ = {#[[1]], Coefficient[Expand[#[[2]]], FR$Eps, -1]/FR$Eps} & /@ uvOSNU$;
Print["MS-bar counterterm vertices: ", InputForm[uvMSNU$ /. IPL[_] -> 1]];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"PsYukawa_NLO_OS_UFO", "PsYukawa_NLO_MSbar_UFO"}];
WriteUFO[LPsYukawa, UVCounterterms -> uvOSNU$, R2Vertices -> R2$vertlist, Output -> "PsYukawa_NLO_OS_UFO"];
WriteUFO[LPsYukawa, UVCounterterms -> uvMSNU$, R2Vertices -> R2$vertlist, Output -> "PsYukawa_NLO_MSbar_UFO"];
Print["written: ", FileNames["PsYukawa_NLO_*_UFO"]];
