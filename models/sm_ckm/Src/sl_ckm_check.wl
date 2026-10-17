(* ::Package:: *)

(* ::Title:: *)
(*Step (6) of the CKM note: semileptonic decays relative to muon decay, and the relation of |V_ij| to the MS-bar V(mu) (no FeynCalc)*)


(* ::Text:: *)
(*Reads results/sl_ckm_amp.m (sl_ckm_feyncalc.wl: K dV, K dB of d_j -> u_i e nubar_e per V_ij and of muon decay, K Sigma^L(0)*)
(*of mu and nu_mu) and the quark self-energies of step (3) (results/oneloop_ckm_sigma.m; gluon parts dropped).  At zero*)
(*momentum with massless external fermions and massless light quarks (the top keeps its mass), the semileptonic*)
(*amplitude over V_ij times the muon-decay amplitude is 1 + R_ij with (K = 16 pi^2)*)
(*  K R_ij = K(dV_sl - dV_mu) + K(dB_sl - dB_mu) - (1/2) K(Sigma^uL_ii(0) + Sigma^dL_jj(0) - Sigma^L_mu(0) - Sigma^L_numu(0))*)
(*           + (1/2)[dZ^uL+ V + V dZ^dL]^{off-diagonal}_ij / V_ij + K dV_ij / V_ij,*)
(*(the W self-energy, the e nu_e vertex and legs and dg cancel in the ratio).  The off-diagonal on-shell field constants*)
(*(note Eq. (dZos)) in the limit of hierarchical light masses: dZ^L_kj = 2 Sigma^S_kj(0) if m_k >> m_j and*)
(*-2 (Sigma^L_kj(0) + Sigma^S_kj(0)) if m_k << m_j; the MS-bar dV of Eq. (dV), (Vrun) in the same limit (A_u = 0,*)
(*K (A_d)_kj = -(3/2) s_kj (V^+ D_u V)_kj with s_kj = +1 if m_dj > m_dk and -1 otherwise).  Checks:*)
(*  (a) the UV pole of K R_ij vanishes (exact, rational unitary V; Sirlin's universality with the CKM counterterm);*)
(*  (b) the coefficient of ln MA (MA -> 0) is the same for the six channels: the Fermi-theory QED log;*)
(*  (c) R_ij does not depend on xiA, xiZ, xiW;*)
(*  (d) R_ij(MT -> 0) is the same for all channels, free of V, and equal to (alpha/pi) ln(MZ/MA) (Sirlin's universal*)
(*      short-distance factor); the top-mass dependence Delta_ij = R_ij - R_ij(MT -> 0), where R_ij(MT -> 0) is the same for all channels and*)
(*      free of V, is G times a CKM factor (|V_tb|^2 for j = b, -|V_td|^2 for j = d, |V_ts|^2 +*)
(*      2 V_ib V_tb^* V_ts / V_is for j = s), with one function G(mu) of MT, MW; G is gauge independent and*)
(*      K dG/dln mu = -(3/2) y_t^2, so that |V_ij(mu)| (1 + Re Delta_ij) does not depend on mu (Eq. (Vrun));*)
(*  (e) numbers at the benchmark, and G against the Denner-Sack shift of step (3).*)
(*Exact closed forms of the vacuum integrals as in the SM note's mudecay_check.wl.  Writes results/sl_ckm_check.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file sl_ckm_check.wl  (run sl_ckm_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirSC$ = FileNameJoin[{srcDirSC$, "results"}];
t0SC$ = AbsoluteTime[];
amp$ = Association[Get[FileNameJoin[{resDirSC$, "sl_ckm_amp.m"}]]];
sig3$ = Association[Get[FileNameJoin[{resDirSC$, "oneloop_ckm_sigma.m"}]]];
KK = 16 Pi^2;
kRuleSC$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toCKSC$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
light0SC$ = {MU -> 0, MC -> 0, MD -> 0, MS -> 0, MB -> 0};
(* exact D-dimensional relations of the zero-momentum B0 to A0 (they cancel the 1/k^2 terms of the self-energies) *)
b0toA0$ = {B0[0, a_, b_] :> Which[a === 0 && b === 0, 0, a === b, (D - 2)/(2 a) A0[a], True, (A0[a] - A0[b])/(a - b)]};
(* K Sigma^n_kj(0) of step (3) (1PI + tadpole, electroweak) with the light quarks massless *)
sig0SC$[sec_, k_, j_, n_] := Module[{x = Total[sig3$[sec][[k, j, All, n]]] /. kRuleSC$ /. toCKSC$ /. gS -> 0},
   x = x /. B0[pp_, a_, b_] /; ! FreeQ[pp, kk2] :> B0[0, a, b] + pp DB0[0, a, b];
   x = x /. light0SC$ /. A0[0] -> 0 /. b0toA0$ /. A0[0] -> 0;
   Normal[Series[x, {kk2, 0, 0}]]];
closed$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]),
   DB0[0, 0, b_] :> 1/(2 b), DB0[0, b_, 0] :> 1/(2 b), DB0[0, a_, a_] :> 1/(6 a),
   DB0[0, a_, b_] :> (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3)};
toSwSC$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];
logRuleSC$ = Log[x_] :> PowerExpand[Log[x]];
canonSC$[x_] := Module[{y = Expand[x /. logRuleSC$], ls},
   ls = Union[Cases[y, _Log, Infinity]];
   If[ls === {}, Together[y], Collect[y, ls, Together]]];
laurSC$[x_] := Module[{y = toSwSC$[x] /. b0toA0$ /. A0[0] -> 0 /. closed$ /. D -> 4 - 2 ep},
   canonSC$ /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
chansSC$ = Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1];
chanNameSC$[{i_, j_}] := {"u", "c"}[[i]] <> {"d", "s", "b"}[[j]];


(* ::Section:: *)
(*The quark legs and the CKM counterterm in the light-quark limit*)


sigDSC$ = Table[sig0SC$["D", k, j, n], {k, 3}, {j, 3}, {n, {1, 3}}];   (* {Sigma^L, Sigma^S} *)
sigUSC$ = Table[sig0SC$["U", k, j, n], {k, 3}, {j, 3}, {n, {1, 3}}];
Print["light masses and k^2 left in the quark self-energies (expect False): ", ! FreeQ[{sigDSC$, sigUSC$}, MU | MC | MD | MS | MB | kk2],
  ";  ", Round[AbsoluteTime[] - t0SC$], " s"];
(* hierarchical off-diagonal field constants: generation k heavier than j if k > j *)
dZoffSC$[s_] := Table[If[k == j, 0, If[k > j, 2 s[[k, j, 2]], -2 (s[[k, j, 1]] + s[[k, j, 2]])]], {k, 3}, {j, 3}];
dZdOffSC$ = dZoffSC$[sigDSC$]; dZuOffSC$ = dZoffSC$[sigUSC$];
hermSC$[m_] := Transpose[m /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b]];
vMSC$ = Array[cK, {3, 3}]; vMcSC$ = Array[cKc, {3, 3}];
ytSqSC$ = 2 MT^2/(2 MW sw/ee)^2;
(* K A_d in the light-quark limit (y_t only) and K dV = (1/(2 eps)) V K A_d *)
kAdSC$ = Table[If[k == j, 0, -3/2 If[j > k, 1, -1] ytSqSC$ (Transpose[vMcSC$] . DiagonalMatrix[{0, 0, 1}] . vMSC$)[[k, j]]], {k, 3}, {j, 3}];
kdVSC$ = (vMSC$ . kAdSC$)/(2 ep);
kRSC$[{i_, j_}] := amp$["dVsl"] - amp$["dVmu"] + amp$["dBsl"] - amp$["dBmu"] -
   1/2 (sigUSC$[[i, i, 1]] + sigDSC$[[j, j, 1]] - amp$["sLmu"] - amp$["sLnumu"]) +
   ((hermSC$[dZuOffSC$] . vMSC$)[[i, j]] + (vMSC$ . dZdOffSC$)[[i, j]])/(2 cK[i, j]) + kdVSC$[[i, j]]/cK[i, j];


(* ::Section:: *)
(*(a)-(c) UV pole, photon mass, gauge independence*)


vStdSC$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
angPySC$ = {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5};
vPySC$ = vStdSC$ /. angPySC$ /. Exp[I dl] -> ph /. Exp[-I dl] -> 1/ph;
vPycSC$ = vStdSC$ /. angPySC$ /. Exp[I dl] -> 1/ph /. Exp[-I dl] -> ph;
explicitSC$ = {cK[i_, j_] :> vPySC$[[i, j]], cKc[i_, j_] :> vPycSC$[[i, j]]};
(* {pole, finite} with the rational V *)
lrSC$ = Association[Table[ch -> (canonSC$ /@ (laurSC$[kRSC$[ch]] /. explicitSC$)), {ch, chansSC$}]];
poleSC$ = Table[canonSC$[lrSC$[ch][[1]] /. MA -> 0], {ch, chansSC$}];
Print["(a) UV pole of K R_ij at MA -> 0, six channels (expect all 0): ", poleSC$, ";  MA^2 terms of the pole: ",
  Union[Table[Factor[lrSC$[ch][[1]]], {ch, chansSC$}]], ";  ", Round[AbsoluteTime[] - t0SC$], " s"];
(* the coefficient of ln MA and the rest at MA -> 0 *)
logMASC$ = Table[Together[Normal[Series[Coefficient[lrSC$[ch][[2]], Log[MA]], {MA, 0, 0}]]], {ch, chansSC$}];
finSC$ = Association[Table[ch -> canonSC$[Normal[Series[lrSC$[ch][[2]] /. Log[MA] -> 0, {MA, 0, 0}]]], {ch, chansSC$}]];
Print["(b) K x coefficient of ln MA, six channels (expect one value): ", Union[canonSC$ /@ logMASC$],
  "   (Fermi theory: amplitude 1 + (alpha/pi) ln(MZ/MA) + ... would give -4 e^2)"];
Print["(b) MA left in the finite parts (expect False): ", ! FreeQ[Values[finSC$], MA]];
xiFreeSC$ = Table[canonSC$[D[finSC$[ch], x]] === 0, {ch, chansSC$}, {x, {xiA, xiZ, xiW}}];
Print["(c) K R_ij free of xiA, xiZ, xiW (expect all True): ", Union[Flatten[xiFreeSC$]]];
(* which parts depend on the gauge: the quark legs with the top separately *)
Print["(c) the d-type legs alone (diagonal + off-diagonal + dV) depend on xiW (expect True): ",
  ! (canonSC$[D[Normal[Series[laurSC$[(-sigDSC$[[3, 3, 1]]/2 + (vMSC$ . dZdOffSC$)[[2, 3]]/(2 cK[2, 3]) + kdVSC$[[2, 3]]/cK[2, 3])][[2]] /.
          explicitSC$ /. Log[MA] -> 0, {MA, 0, 0}]], xiW]] === 0)];


(* ::Section:: *)
(*(d) The top-mass dependence and G(mu)*)


(* MT -> 0 as a series (the loop functions have ln MT) *)
univSC$ = Table[canonSC$[Normal[Series[finSC$[ch], {MT, 0, 0}]]], {ch, chansSC$}];
Print["(d) R_ij(MT -> 0): one value for the six channels and free of V (expect 1, False): ", Length[Union[univSC$]], ", ",
  ! FreeQ[univSC$, ph]];
(* with the ln MA term: K R_univ = 2 e^2 ln(MZ^2/MA^2), i.e. R_univ = (alpha/pi) ln(MZ/MA) exactly (Sirlin) *)
sirlinSC$ = canonSC$[univSC$[[1]] + logMASC$[[1]] Log[MA] - 2 ee^2 Log[toSwSC$[MZ]^2/MA^2]];
Print["(d) K R_univ + K (ln MA term) - 2 e^2 ln(MZ^2/MA^2) (expect 0): ", sirlinSC$];
deltaSC$ = Association[Table[chansSC$[[n]] -> canonSC$[finSC$[chansSC$[[n]]] - univSC$[[n]]], {n, 6}]];
(* the CKM factors with the rational V *)
cFacSC$[{i_, j_}] := Together[Which[
    j == 3, vPySC$[[3, 3]] vPycSC$[[3, 3]],
    j == 1, -vPySC$[[3, 1]] vPycSC$[[3, 1]],
    j == 2, vPySC$[[3, 2]] vPycSC$[[3, 2]] + 2 vPySC$[[i, 3]] vPycSC$[[3, 3]] vPySC$[[3, 2]]/vPySC$[[i, 2]]]];
gSC$ = canonSC$[deltaSC$[chansSC$[[1]]]/cFacSC$[chansSC$[[1]]]];
gOfSC$ = Table[canonSC$[deltaSC$[ch] - gSC$ cFacSC$[ch]], {ch, chansSC$}];
Print["(d) Delta_ij - G x (CKM factor) with G from the u dbar channel, six channels (expect all 0): ", gOfSC$];
xt$ = MT^2/MW^2;
(* the closed form found: K G = (y_t^2/8) [-(5 x_t - 11)/(x_t - 1) + 6 x_t (x_t - 2) ln x_t/(x_t - 1)^2] - (3/4) y_t^2 ln(mu^2/MW^2) *)
gClosedSC$ = toSwSC$[ytSqSC$/8 (-(5 xt$ - 11)/(xt$ - 1) + 6 xt$ (xt$ - 2) Log[xt$]/(xt$ - 1)^2) - 3/4 ytSqSC$ Log[mu^2/MW^2]];
Print["(d) K G minus the closed form (expect 0): ", canonSC$[gSC$ - gClosedSC$], ";  gauge parameters in G (expect False): ",
  ! FreeQ[gSC$, xiA | xiZ | xiW], ";  K dG/dln mu + (3/2) y_t^2 (expect 0): ", canonSC$[mu D[gSC$, mu] + 3/2 toSwSC$[ytSqSC$]]];


(* ::Section:: *)
(*(e) Numbers*)


benchSC$ = {ee -> Sqrt[4 Pi/128], MW -> 80, sw -> Sqrt[1 - 80^2/91^2], MH -> 125, MT -> 165, MTA -> 1746/1000};
vNumSC$ = N[vStdSC$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 30];
gNumSC$[m_] := N[gSC$/KK /. benchSC$ /. mu -> m, 20];
sfSC$[x_, n_ : 6] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
cFacNumSC$[{i_, j_}] := Module[{v = vNumSC$}, Which[j == 3, Abs[v[[3, 3]]]^2, j == 1, -Abs[v[[3, 1]]]^2,
    j == 2, Abs[v[[3, 2]]]^2 + 2 v[[i, 3]] Conjugate[v[[3, 3]]] v[[3, 2]]/v[[i, 2]]]];
Print["(e) G(mu = MZ) = ", sfSC$[gNumSC$[91], 8], ",  G(mu = 2 MZ) - G(MZ) = ", sfSC$[gNumSC$[182] - gNumSC$[91]],
  "   (-(3/(2K)) y_t^2 ln 2 = ", sfSC$[N[-3/2 ytSqSC$ Log[2]/KK /. benchSC$]], ")"];
deltaNumSC$ = Table[gNumSC$[91] cFacNumSC$[ch], {ch, chansSC$}];
Print["(e) Delta_ij at mu = MZ (Re, Im): ", StringRiffle[MapThread[#1 <> " " <> sfSC$[Re[#2]] <> ", " <> sfSC$[Im[#2]] &,
    {chanNameSC$ /@ chansSC$, deltaNumSC$}], ";  "]];
(* the Denner-Sack shift of step (3): |V^DS|/|V^MSbar| - 1 = -(delta|V|/|V| of dV^DS_fin) *)
ds3SC$ = Association[Rule @@@ Rest[Import[FileNameJoin[{resDirSC$, "oneloop_ckm_numeric.csv"}], "CSV"]]];
dsShiftSC$[name_] := -ToExpression[StringReplace[ds3SC$["dVDS_fin_relabs_" <> name <> "_xiW_half_2_3_10"],
      {"List(" -> "{", ")" -> "}", "e" -> "*^"}]];
Print["(e) |V^phys|/|V(MZ)| - 1 = Re Delta_ij against the Denner-Sack |V^DS|/|V^MSbar| - 1 of step (3) (xiW = 1/2, 2, 3, 10):"];
Do[Print["   ", chanNameSC$[ch], ": ", sfSC$[Re[deltaNumSC$[[n]]]], "   DS: ", sfSC$ /@ dsShiftSC$[chanNameSC$[ch]]],
  {n, 6}, {ch, {chansSC$[[n]]}}];

Export[FileNameJoin[{resDirSC$, "sl_ckm_check.csv"}],
  Join[{{"quantity", "value"}, {"G_muMZ", ToString[CForm[gNumSC$[91]]]}, {"G_mu2MZ", ToString[CForm[gNumSC$[182]]]}},
   Flatten[Table[{{"ReDelta_" <> chanNameSC$[chansSC$[[n]]], ToString[CForm[Re[deltaNumSC$[[n]]]]]},
      {"ImDelta_" <> chanNameSC$[chansSC$[[n]]], ToString[CForm[Im[deltaNumSC$[[n]]]]]}}, {n, 6}], 1]], "CSV"];
Put[{"KG" -> gSC$, "KRuniv" -> univSC$[[1]], "KlogMA" -> logMASC$[[1]]}, FileNameJoin[{resDirSC$, "sl_ckm_G.m"}]];
Print["Summary (expect all 0; one value; True; 1, False, 0; {0}; 0, False, 0): ", Union[poleSC$], "; ", Length[Union[canonSC$ /@ logMASC$]],
  "; ", Union[Flatten[xiFreeSC$]], "; ", Length[Union[univSC$]], ", ", ! FreeQ[univSC$, ph], ", ", sirlinSC$, "; ", Union[gOfSC$], "; ",
  canonSC$[gSC$ - gClosedSC$], ", ", ! FreeQ[gSC$, xiA | xiZ | xiW], ", ", canonSC$[mu D[gSC$, mu] + 3/2 toSwSC$[ytSqSC$]],
  ";  total ", Round[AbsoluteTime[] - t0SC$], " s"];
