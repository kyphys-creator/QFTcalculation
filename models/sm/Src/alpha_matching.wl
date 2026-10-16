(* ::Package:: *)

(* ::Title:: *)
(*Step (6b): alpha(0) and the MS-bar charge e(mu) from the photon two-point functions of step (3) (SM note)*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (K Sigma_T in A0, B0, D; general xiA, xiZ, xiW).  On-shell charge renormalization in the*)
(*note's convention (A = -A_Denner, so the mixing term has the opposite sign to Denner's):*)
(*  e(mu)/e_OS - 1 = delta_e = [Pi^AA(0)/2 + (sw/cw) Sigma_T^AZ(0)/MZ^2]_fin,   Pi^AA(0) = d Sigma_T^AA/dk^2 at k^2 = 0.*)
(*  (a) Sigma_T^AA(0) = 0, and the fermion loops give nothing to Sigma_T^AZ(0);*)
(*  (b) the fermion part of Pi^AA(0) is (e^2/K)(4/3) Nc Q^2 [B0(0, m, m) + 2 m^2 DB0(0, m, m) - 1/3] for each fermion;*)
(*  (c) the UV pole of delta_e is (11/6) e^2/K (Eq. (dZe)) and the finite part of delta_e does not depend on xiA, xiZ, xiW;*)
(*  (d) the bosonic part of 2 delta_e at mu = MZ is (alpha/pi)[-1/6 - (7/4) ln(MZ^2/MW^2)] (PDG electroweak review);*)
(*  (e) alpha-hat(MZ) from alpha(0), Delta alpha_lep and Delta alpha_had^(5): the light fermions (all but the top) enter*)
(*      through Pi_f(0) = Re Pi_f(MZ^2) + Delta alpha_f, with the massless Re Pi_f,fin(MZ^2) = (e^2/K)(4/3) Nc Q^2 (5/3 -*)
(*      ln(MZ^2/mu^2)); 1/alpha-hat(mu) = (1 - 2 delta_e)/alpha(0).  Without the top this is the one-loop part of the*)
(*      PDG relation (PDG 2024, Eq. (10.13), 1/alpha-hat^(5)(MZ) = 127.930(8)).*)
(*Writes results/alpha_matching.csv.  No FeynCalc needed.  Batch: wolframscript -file alpha_matching.wl*)


srcDirAM$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
sig$ = Association[Get[FileNameJoin[{srcDirAM$, "results", "oneloop_sigma.m"}]]];
KK = 16 Pi^2;
kRule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
toSw$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];

(* B0(k^2, a, b) = B0(0, a, b) + sum_n (k^2)^n DnB0(0, a, b), DnB0 = (1/n) int_0^1 dx [x(1-x)/(x a + (1-x) b)]^n *)
taylorB0$ = B0[kk_, a_, b_] /; !FreeQ[kk, kk2] :>
   B0[0, a, b] + Sum[(kk)^n dnB0[n, a, b], {n, 1, 3}];
dnB0Closed$[n_, a_, b_] := Which[
   a === b, (n!)^2/((2 n + 1)! n a^n),
   a === 0, 1/(n (n + 1) b^n), b === 0, 1/(n (n + 1) a^n),
   n === 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, Integrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}, Assumptions -> a > 0 && b > 0,
     GenerateConditions -> False]/n];
closed$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]),
   B0[0, 0, 0] -> 0,
   B0[0, a_, a_] :> 1/ep - Log[a/mu^2],
   B0[0, 0, b_] :> 1/ep + 1 - Log[b/mu^2], B0[0, b_, 0] :> 1/ep + 1 - Log[b/mu^2],
   B0[0, a_, b_] :> 1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b),
   dnB0[n_, a_, b_] :> dnB0Closed$[n, a, b]};
logRule$ = Log[x_] :> PowerExpand[Log[x]];
canon$[x_] := Module[{y = Expand[x /. logRule$], ls},
   ls = Union[Cases[y, _Log, Infinity]];
   If[ls === {}, Together[y], Collect[y, ls, Together]]];
laur$[x_] := Module[{y = toSw$[x] /. closed$ /. D -> 4 - 2 ep},
   canon$ /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
isZero$[x_] := canon$[x] === 0;

(* coefficients of (k^2)^-1, (k^2)^0 and (k^2)^1, each as {UV pole, finite part}; the closed forms go in first, since
   the 1/k^2 terms of the projection cancel only through A0(a) - A0(b) = (a - b) B0(0, a, b).  The tadpole-attached
   parts vanish (no H A A, H A Z vertex). *)
kSeries$[x_] := Module[{y = toSw$[Total[x] /. kRule$ /. MA -> 0 /. taylorB0$] /. closed$ /. D -> 4 - 2 ep},
   Table[canon$ /@ {SeriesCoefficient[y, {kk2, 0, n}, {ep, 0, -1}], SeriesCoefficient[y, {kk2, 0, n}, {ep, 0, 0}]},
    {n, -1, 1}]];
{laaM$, laa0$, lpi$} = kSeries$[sig$["AA"]];
{lazM$, laz$, lazP$} = kSeries$[sig$["AZ"]];
Print["    1/k^2 terms of K Sigma_T^AA, K Sigma_T^AZ (expect {0, 0}, {0, 0}): ", {laaM$, lazM$}];


(* ::Section:: *)
(*(a), (b) Sigma^AA(0), the fermion loops*)


fermions$ = {{MU, 3, 2/3}, {MC, 3, 2/3}, {MT, 3, 2/3}, {MD, 3, -1/3}, {MS, 3, -1/3}, {MB, 3, -1/3},
   {Me, 1, -1}, {MMU, 1, -1}, {MTA, 1, -1}};
fmass$ = fermions$[[All, 1]];
Print["(a) K Sigma_T^AA(0) = ", laa0$, "   (expect {0, 0})"];
Print["(a) Sigma_T^AZ(0) free of fermion masses (expect True): ", FreeQ[laz$, Alternatives @@ fmass$]];
piHand$[{m_, nc_, q_}] := ee^2 4/3 nc q^2 (B0[0, m^2, m^2] + 2 m^2 dnB0[1, m^2, m^2] - 1/3);
piF$ = Total[piHand$ /@ fermions$];
lpiF$ = laur$[piF$];
lpiBos$ = canon$ /@ (lpi$ - lpiF$);
Print["(b) K Pi^AA(0) - fermion loops by hand: free of fermion masses (expect True, True): ",
  FreeQ[#, Alternatives @@ fmass$] & /@ lpiBos$];


(* ::Section:: *)
(*(c) UV pole and gauge independence*)


sOverC$ = sw/Sqrt[1 - sw^2]; mz2$ = MW^2/(1 - sw^2);
de$ = canon$ /@ (lpi$/2 + sOverC$ laz$/mz2$);
deBos$ = canon$ /@ (lpiBos$/2 + sOverC$ laz$/mz2$);
Print["(c) K delta_e: UV pole - 11/6 e^2 = ", canon$[de$[[1]] - 11/6 ee^2], "   (expect 0)"];
Print["(c) the finite part of delta_e does not depend on xiA, xiZ, xiW (expect True, True, True): ",
  isZero$[D[de$[[2]], #]] & /@ {xiA, xiZ, xiW}];
Print["    Pi^AA(0) and Sigma^AZ(0) separately depend on xiW (expect True, True): ",
  !isZero$[D[#[[2]], xiW]] & /@ {lpiBos$, laz$}];


(* ::Section:: *)
(*(d) the bosonic part against the literature*)


(* alpha/pi = 4 e^2/K, i.e. in K units (alpha/pi) -> 4 ee^2 *)
pdgBos$ = 4 ee^2 (-1/6 - 7/4 Log[1/(1 - sw^2)]);
Print["(d) K 2 delta_e(bosonic) at mu = MZ - K (alpha/pi)[-1/6 - (7/4) ln(MZ^2/MW^2)] = ",
  canon$[(2 deBos$[[2]] /. mu -> MW/Sqrt[1 - sw^2]) - pdgBos$], "   (expect 0)"];
Print["    K 2 delta_e(bosonic) at general mu: ", canon$[2 deBos$[[2]]]];


(* ::Section:: *)
(*(e) alpha-hat(MZ) from the measured alpha(0)*)


(* PDG 2024 (the note's inputs); Delta alpha_lep(MZ^2) at three loops from Steinhauser, PLB 429 (1998) 158 *)
alpha0$ = 1/137035999177*10^9; dalLep$ = 0.03149769; dalHad$ = 0.02783;
pdgIn$ = {MW -> 803692/10000, sw -> Sqrt[1 - (803692/911880)^2], ee -> Sqrt[4 Pi alpha0$], MT -> 17257/100};
light$ = DeleteCases[fermions$, {MT, __}];
rePiLight$[mu0_] := ee^2 4/3 Total[#[[2]] #[[3]]^2 & /@ light$] (5/3 - Log[mz2$/mu0^2]);
piTop$ = laur$[piHand$[{MT, 3, 2/3}]][[2]];
twoDe$[mu0_] := (2 deBos$[[2]] + piTop$ + rePiLight$[mu0] /. mu -> mu0)/KK + dalLep$ + dalHad$;
alInv$[mu0_] := N[(1 - twoDe$[mu0] /. pdgIn$)/alpha0$];
alInvDec$[mu0_] := N[(1 - (twoDe$[mu0] - piTop$/KK /. mu -> mu0) /. pdgIn$)/alpha0$];
mzN$ = 91188/1000;
nf$[x_, n_] := ToString[NumberForm[x, n]];
(* PDG 2024, Eq. (10.13): Delta alpha-hat(MZ) - Delta alpha(MZ) = 0.007122 with the QCD corrections to the quark loops
   (top decoupled); its one-loop part is (alpha/pi)[100/27 - 1/6 - (7/4) ln(MZ^2/MW^2)] *)
pdgShift$ = 0.007122;
oneLoopShift$ = N[(2 deBos$[[2]] + rePiLight$[mzN$])/KK /. mu -> mzN$ /. pdgIn$];
Print["(e) 1/alpha-hat(MZ): full SM (top not decoupled) ", nf$[alInv$[mzN$], 8],
  ";  without the top loop ", nf$[alInvDec$[mzN$], 8], ";  1/alpha(MZ^2) on-shell ",
  nf$[N[(1 - dalLep$ - dalHad$)/alpha0$], 8]];
Print["    Delta alpha-hat - Delta alpha at mu = MZ (top decoupled): one loop ", nf$[oneLoopShift$, 6],
  ", against (alpha/pi)[100/27 - 1/6 - (7/4) ln(MZ^2/MW^2)] = ",
  nf$[N[alpha0$/Pi (100/27 - 1/6 - 7/4 Log[(911880/803692)^2])], 6], ";  PDG with QCD ", pdgShift$,
  " -> 1/alpha-hat^(5)(MZ) = ", nf$[N[(1 - dalLep$ - dalHad$ - pdgShift$)/alpha0$], 8], " (PDG: 127.930(8))"];
Print["    parts of 2 delta_e at mu = MZ (bosonic, top, Re Pi_light(MZ^2), Delta alpha): ",
  N[{2 deBos$[[2]]/KK, piTop$/KK, rePiLight$[mzN$]/KK} /. mu -> mzN$ /. pdgIn$], ", ", dalLep$ + dalHad$];
Print["    d(1/alpha-hat)/dln mu at mu = MZ (numerical) and -b/(2 pi) with b = 11/3: ",
  N[(alInv$[mzN$ 1.0001] - alInv$[mzN$/1.0001])/(2 Log[1.0001])], ", ", N[-11/3/(2 Pi)]];
Export[FileNameJoin[{srcDirAM$, "results", "alpha_matching.csv"}],
  {{"quantity", "value"},
   {"alphahat_inv_MZ_fullSM", ToString[CForm[alInv$[mzN$]]]},
   {"alphahat_inv_MZ_no_top", ToString[CForm[alInvDec$[mzN$]]]},
   {"alpha_inv_MZ2_onshell", ToString[CForm[N[(1 - dalLep$ - dalHad$)/alpha0$]]]},
   {"shift_alphahat_minus_alpha_one_loop_MZ", ToString[CForm[oneLoopShift$]]},
   {"two_delta_e_bosonic_MZ", ToString[CForm[N[2 deBos$[[2]]/KK /. mu -> mzN$ /. pdgIn$]]]},
   {"two_delta_e_top_MZ", ToString[CForm[N[piTop$/KK /. mu -> mzN$ /. pdgIn$]]]}}, "CSV"];
Put[{"deltaE_bosonic_finite" -> deBos$[[2]], "deltaE_finite" -> de$[[2]]},
  FileNameJoin[{srcDirAM$, "results", "alpha_deltae.m"}]];
Print["Summary: ", {canon$[de$[[1]] - 11/6 ee^2], isZero$[D[de$[[2]], #]] & /@ {xiA, xiZ, xiW},
   canon$[(2 deBos$[[2]] /. mu -> MW/Sqrt[1 - sw^2]) - pdgBos$]}];
