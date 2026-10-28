(* ::Package:: *)

(* ::Title:: *)
(*Step (9): longitudinal tree amplitudes for the coupled channels A_L A_L, h h, A_L h (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (9).  Uses the FeynArts model of this note in a general R_xi gauge.*)
(*  (a) A h -> A h: the 6 diagrams against the hand formula of Eq. (Mah) (polarization vectors as symbols), xi*)
(*      independence with transversality;*)
(*  (b) the four processes A_L A_L -> A_L A_L, A_L A_L -> h h, h h -> h h, A_L h -> A_L h with explicit longitudinal*)
(*      polarization vectors in the CM frame (functions of s and c = cos theta): the FeynArts amplitudes (general xi)*)
(*      against Eqs. (MLL), (Mahh), (Mhh), (Mah); xi drops out;*)
(*  (c) the limit s -> infinity at fixed c: the lam terms -6 lam, +2 lam, -6 lam, -2 lam (equivalence theorem,*)
(*      G G -> G G, -(G G -> h h), h h -> h h, G h -> G h) and the remaining e^2 terms;*)
(*  (d) results/unitarity_amps.m (the four M(s, c)) for unitarity_numeric.wl; |M|^2 at 12 points and the momenta*)
(*      for the MadGraph standalone check -> results/unitarity_points.csv, work/me_points_*_L.txt.*)
(*FeynArts' CreateFeynAmp gives M (the product of Feynman rules divided by i), the same normalization as the note.*)
(*Batch: wolframscript -file unitarity_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirUF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirUF$ = FileNameJoin[{srcDirUF$, "results"}];
workDirUF$ = FileNameJoin[{srcDirUF$, "work"}];
Quiet[CreateDirectory[workDirUF$]];
modelTmpDirUF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirUF$, "generated", "AbelianHiggs_FA"}], FileNameJoin[{modelTmpDirUF$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirUF$, "AbelianHiggs_FA"}], Quiet -> True];
modelFileUF$ = FileNameJoin[{modelTmpDirUF$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];

convUF$ = {FCGV["EL"] -> ee, FCGV["MA"] -> MA, FCGV["MH"] -> MH, GaugeXi[A] -> xi, GaugeXi[V[1, ___]] -> xi,
   GaugeXi[S[2, ___]] -> xi, GaugeXi[U[1, ___]] -> xi};
parUF$ = {vev -> MA/ee, lam -> ee^2 MH^2/(2 MA^2)};
treeDiagrams$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelFileUF$, GenericModel -> modelFileUF$], RuleDelayed::rhs];
treeAmp$[in_, out_] := Module[{d = treeDiagrams$[in, out], a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> {k1, k2}, OutgoingMomenta -> {k3, k4}, ChangeDimension -> 4, List -> True, SMP -> False,
       DropSumOver -> True, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   Print["   ", in, " -> ", out, ": ", Length[a], " diagrams"];
   Total[a] /. convUF$ /. parUF$];
lamV$ = ee^2 MH^2/(2 MA^2);


(* ::Section:: *)
(*(a) A h -> A h with symbolic polarization vectors*)


ampAh$ = treeAmp$[{V[1], S[1]}, {V[1], S[1]}];
polSymAh$ = {Momentum[Polarization[k1, I, ___]] -> Momentum[eps1], Momentum[Polarization[k3, -I, ___]] -> Momentum[eps3]};
FCClearScalarProducts[];
SP[k1, k1] = MA^2; SP[k2, k2] = MH^2; SP[k3, k3] = MA^2;
SP[k1, k2] = (s - MA^2 - MH^2)/2; SP[k1, k3] = (2 MA^2 - t)/2; SP[k2, k3] = (MA^2 + MH^2 - (2 MA^2 + 2 MH^2 - s - t))/2;
normAh$[x_] := Simplify[ExpandScalarProduct[FeynAmpDenominatorExplicit[Contract[
       x /. polSymAh$ /. Momentum[q_, dim___] :> Momentum[q /. k4 -> k1 + k2 - k3, dim] /; FreeQ[q, eps1 | eps3]]]] /.
    {Pair[Momentum[eps1], Momentum[k1]] -> 0, Pair[Momentum[eps3], Momentum[k3]] -> 0}];
mAh$ = normAh$[ampAh$];
uAh$ = 2 MA^2 + 2 MH^2 - s - t;
e13$ = SP[eps1, eps3]; e1k2$ = SP[eps1, k2]; e3k2$ = SP[eps3, k2];
e1k4$ = e1k2$ - SP[eps1, k3];       (* eps1.k4 = eps1.(k1 + k2 - k3) *)
e3k4$ = SP[eps3, k1] + SP[eps3, k2];  (* eps3.k4 = eps3.(k1 + k2) *)
handAh$ = 2 ee^2 e13$ + 6 ee^2 MH^2 e13$/(t - MH^2) + 4 ee^2 (MA^2 e13$ - e1k2$ e3k4$)/(s - MA^2) +
   4 ee^2 (MA^2 e13$ - e1k4$ e3k2$)/(uAh$ - MA^2);
Print["(a) A h -> A h: d/dxi of the sum (expect 0): ", Simplify[D[mAh$, xi]]];
Print["(a) A h -> A h: FeynCalc - Eq. (Mah) (expect 0): ", Simplify[ExpandScalarProduct[mAh$ - handAh$]]];


(* ::Section:: *)
(*(b) explicit longitudinal polarization vectors*)


(* CM frame: 1 along +z, 3 at angle theta in the xz plane; c = cos theta, sn = sin theta (sn^2 = 1 - c^2) *)
kinUF$[m1_, m2_, m3_, m4_] := Module[{rs = Sqrt[s], pi, pf, e1, e2, e3, e4},
   pi = Sqrt[(s - (m1 + m2)^2) (s - (m1 - m2)^2)]/(2 rs); pf = Sqrt[(s - (m3 + m4)^2) (s - (m3 - m4)^2)]/(2 rs);
   e1 = (s + m1^2 - m2^2)/(2 rs); e2 = (s + m2^2 - m1^2)/(2 rs); e3 = (s + m3^2 - m4^2)/(2 rs); e4 = (s + m4^2 - m3^2)/(2 rs);
   <|k1 -> {e1, 0, 0, pi}, k2 -> {e2, 0, 0, -pi}, k3 -> {e3, pf sn, 0, pf c}, k4 -> {e4, -pf sn, 0, -pf c},
    "L1" -> {pi, 0, 0, e1}/m1, "L2" -> {pi, 0, 0, -e2}/m2, "L3" -> {pf, e3 sn, 0, e3 c}/m3, "L4" -> {pf, -e4 sn, 0, -e4 c}/m4|>];
dotUF$[a_, b_] := a[[1]] b[[1]] - a[[2]] b[[2]] - a[[3]] b[[3]] - a[[4]] b[[4]];
vecUF$[kin_, Momentum[Polarization[k_, __], ___]] := kin[ToString[k] /. {"k1" -> "L1", "k2" -> "L2", "k3" -> "L3", "k4" -> "L4"}];
vecUF$[kin_, Momentum[k_, ___]] := kin[k];
explicitUF$[x_, kin_] := Module[{y},
   y = ExpandScalarProduct[FeynAmpDenominatorExplicit[Contract[x]]];
   y = y /. Pair[a_Momentum, b_Momentum] :> dotUF$[vecUF$[kin, a], vecUF$[kin, b]];
   Simplify[y /. sn^2 -> 1 - c^2, s > 4 MH^2 && MH > 2 MA && MA > 0 && -1 < c < 1]];
simpl$[x_] := Simplify[x /. sn^2 -> 1 - c^2, s > 4 MH^2 && MH > 2 MA && MA > 0 && -1 < c < 1];

FCClearScalarProducts[];
kinAA$ = kinUF$[MA, MA, MA, MA]; kinAh2$ = kinUF$[MA, MA, MH, MH]; kinHH$ = kinUF$[MH, MH, MH, MH]; kinAh$ = kinUF$[MA, MH, MA, MH];
tOf$[kin_] := dotUF$[kin[k1] - kin[k3], kin[k1] - kin[k3]]; uOf$[kin_] := dotUF$[kin[k1] - kin[k4], kin[k1] - kin[k4]];

mLL$ = explicitUF$[treeAmp$[{V[1], V[1]}, {V[1], V[1]}], kinAA$];
mLh$ = explicitUF$[treeAmp$[{V[1], V[1]}, {S[1], S[1]}], kinAh2$];
mhh$ = explicitUF$[treeAmp$[{S[1], S[1]}, {S[1], S[1]}], kinHH$];
mAhL$ = explicitUF$[ampAh$, kinAh$];
Print["(b) xi dependence of the four longitudinal amplitudes (expect 0): ", Simplify[D[{mLL$, mLh$, mhh$, mAhL$}, xi]]];

(* hand formulas with the same explicit vectors *)
handLL$ = Module[{t = tOf$[kinAA$], u = uOf$[kinAA$]},
   -4 ee^2/MA^2 ((s/2 - MA^2)^2/(s - MH^2) + (t/2 + MA^2 c)^2/(t - MH^2) + (u/2 - MA^2 c)^2/(u - MH^2))];
handLh$ = Module[{kn = kinAh2$, t = tOf$[kinAh2$], u = uOf$[kinAh2$], ep1, ep2},
   ep1 = kn["L1"]; ep2 = kn["L2"];
   2 ee^2 dotUF$[ep1, ep2] (1 + 3 MH^2/(s - MH^2)) +
    4 ee^2 (MA^2 dotUF$[ep1, ep2] + dotUF$[ep1, kn[k3]] dotUF$[ep2, kn[k4]])/(t - MA^2) +
    4 ee^2 (MA^2 dotUF$[ep1, ep2] + dotUF$[ep1, kn[k4]] dotUF$[ep2, kn[k3]])/(u - MA^2)];
handhh$ = Module[{t = tOf$[kinHH$], u = uOf$[kinHH$]},
   -6 lamV$ - 9 MH^4 ee^2/MA^2 (1/(s - MH^2) + 1/(t - MH^2) + 1/(u - MH^2))];
handAhL$ = Module[{kn = kinAh$, t = tOf$[kinAh$], u = uOf$[kinAh$], ep1, ep3},
   ep1 = kn["L1"]; ep3 = kn["L3"];
   2 ee^2 dotUF$[ep1, ep3] + 6 ee^2 MH^2 dotUF$[ep1, ep3]/(t - MH^2) +
    4 ee^2 (MA^2 dotUF$[ep1, ep3] - dotUF$[ep1, kn[k2]] dotUF$[ep3, kn[k4]])/(s - MA^2) +
    4 ee^2 (MA^2 dotUF$[ep1, ep3] - dotUF$[ep1, kn[k4]] dotUF$[ep3, kn[k2]])/(u - MA^2)];
Print["(b) FeynCalc - hand (Eqs. (MLL), (Mahh), (Mhh), (Mah)) with explicit vectors (expect 0): ",
  simpl$[{mLL$ - handLL$, mLh$ - handLh$, mhh$ - handhh$, mAhL$ - handAhL$}]];


(* ::Section:: *)
(*(c) the high-energy limit at fixed c*)


lim$[x_] := Simplify[Limit[x, s -> Infinity, Assumptions -> -1 < c < 1 && MA > 0 && MH > 2 MA && ee > 0],
   -1 < c < 1 && MA > 0 && MH > 0];
limits$ = lim$ /@ {mLL$, mLh$, mhh$, mAhL$};
Print["(c) s -> infinity (fixed c): A_L A_L -> A_L A_L ", InputForm[limits$[[1]]], ";  A_L A_L -> h h ", InputForm[limits$[[2]]],
  ";  h h -> h h ", InputForm[limits$[[3]]], ";  A_L h -> A_L h ", InputForm[limits$[[4]]]];
Print["(c) the same minus the lam terms -6 lam, +2 lam, -6 lam, -2 lam (in units of ee^2): ",
  InputForm[Simplify[(limits$ - {-6, 2, -6, -2} lamV$)/ee^2]]];


(* ::Section:: *)
(*(d) output*)


Put[{"LL" -> mLL$, "LLhh" -> mLh$, "hh" -> mhh$, "Lh" -> mAhL$}, FileNameJoin[{resDirUF$, "unitarity_amps.m"}]];
bench$ = {ee -> 1/2, MA -> 1, MH -> 5/2};
points$ = Flatten[Table[{rs, cv}, {rs, {6, 20}}, {cv, {-3/5, 1/10, 7/10}}], 1];
procs$ = {{"LL", mLL$, kinAA$}, {"LLhh", mLh$, kinAh2$}, {"hh", mhh$, kinHH$}, {"Lh", mAhL$, kinAh$}};
rowsUF$ = {};
Do[Module[{name = pr[[1]], amp = pr[[2]], kn = pr[[3]], lines = {}},
    Do[Module[{vals = Join[bench$, {s -> pt[[1]]^2, c -> pt[[2]], sn -> Sqrt[1 - pt[[2]]^2]}], m2, mom},
       m2 = N[(amp /. vals)^2, 25];
       mom = Flatten[N[{kn[k1], kn[k2], kn[k3], kn[k4]} /. vals, 25]];
       AppendTo[lines, StringRiffle[ToString[CForm[#]] & /@ mom, " "]];
       AppendTo[rowsUF$, {name, pt[[1]], N[pt[[2]]], m2}]], {pt, points$}];
    Export[FileNameJoin[{workDirUF$, "me_points_" <> name <> "_L.txt"}], StringRiffle[lines, "\n"] <> "\n", "Text"]],
  {pr, procs$}];
Export[FileNameJoin[{resDirUF$, "unitarity_points.csv"}],
  Prepend[Map[If[StringQ[#], #, ToString[CForm[N[#, 20]]]] &, rowsUF$, {2}], {"process", "sqrt_s", "cos_theta", "M2"}], "CSV"];
Print["(d) written results/unitarity_amps.m, results/unitarity_points.csv, work/me_points_*_L.txt"];
