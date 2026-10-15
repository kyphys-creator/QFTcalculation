(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop tadpole and self-energies of the Standard Model (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm, step (3).  Compares with Eqs. (T), (SAA)-(SWW), (SH) (eq:T ... eq:SH) and (Pi0).*)
(*(b) Feynman gauge, FeynRules model (generated/SM_FA): the tadpole and the 1PI self-energies AA, AZ, ZZ, WW (transverse)*)
(*    and HH, fermion and boson loops separately, in D dimensions, expanded to d = 4 with the rational terms, against the*)
(*    note's formulas (12 differences).*)
(*(c) The same diagrams from FeynArts' SM.mod (Denner's conventions) at xi = 1, grouped by topology and internal fields,*)
(*    exact in D dimensions, including the longitudinal parts, the vector-Goldstone mixings and the tadpole-attached*)
(*    diagrams; SM.mod is converted with the external-leg factors of oneloop_conv.wl (A -1, incoming G+ -i, outgoing G+ +i).*)
(*(d) General R_xi (xi_A, xi_Z, xi_W) with SM.mod: the Slavnov-Taylor identities of the two-point functions, derived in*)
(*    the note (App. C) from <F F> = free with F = d.V - xi M G and delta G = -M theta,*)
(*      k k X(A->A) = 0,   k k X(A->Z) + i MZ k X(A->G0) = 0,*)
(*      k k X(V->V) + i M k X(V->G) - i M k X(G->V) + M^2 X(G->G) = 0   (V, G = Z, G0 and W+, G+),*)
(*    for the full one-loop two-point functions (1PI + tadpole-attached diagrams), and without the tadpoles; Sigma^AA_T(0)*)
(*    = 0 and Sigma^AZ_T(0) for all xi; the xi dependence of the transverse self-energies on shell; the UV poles (the*)
(*    W self-energy with a photon mass lam as IR regulator, lam -> 0).*)
(*(e) Finite parts (Delta = 0, mu = MZ) of the note's formulas at a numerical point: every B0 from LoopTools and*)
(*    Package-X -> results/oneloop_b0.csv, the coefficients -> results/oneloop_coeffs.csv; oneloop_collier.f90 and*)
(*    oneloop_numeric.py add COLLIER and mpmath integrals.*)
(*Normalization: with PreFactor -> 1, FeynArts' amplitude is A = (2 Pi)^D V (V the one-loop part of the 1PI function) and*)
(*TID writes A = I Pi^2 X with X built from A0, B0.  For the note's definitions (Eq. (Gamma2)): K Sigma_T = -X_T,*)
(*K Sigma_L = -X_L, K Sigma^H = X, K T = X (K = (4 Pi)^2), X_T = (g X - kk X/k^2)/(D - 1), X_L = kk X/k^2.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl.  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$FAVerbose = 0;
(* traces with gamma5 and four or more other matrices give epsilon tensors with at most one external momentum: they*)
(* vanish in two-point functions, and the NDR-Discard scheme drops them *)
FCSetDiracGammaScheme["NDR-Discard"];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirOL$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "SM_FA"}], Quiet -> True];
frModelOL$ = FileNameJoin[{modelTmpDirOL$, "SM_FA", "SM_FA"}];
KK = (4 Pi)^2;


(* ::Text:: *)
(*Rules.  FeynRules model: M$FACouplings, diagonal Yukawas y = sqrt2 m/v, CKM = 1, v = 2 MW sw/e, lam = MH^2 e^2/(8 MW^2 sw^2).*)
(*Class-level insertion: one generation with masses ml, mu, md (m_nu = 0); closed quark loops: the dropped colour sum is Nc.*)
(*SM.mod: MLE, MQU, MQD and CKM likewise.  Gauge parameters xA, xZ, xW.*)


frCoupOL$ = {yl[a_, b_] :> IndexDelta[a, b] Sqrt[2] Ml[a]/vev, yu[a_, b_] :> IndexDelta[a, b] Sqrt[2] Mu[a]/vev,
   yd[a_, b_] :> IndexDelta[a, b] Sqrt[2] Md[a]/vev, CKM[a_, b_] :> IndexDelta[a, b]};
frSumOL$ = IndexSum[x_, {i_, 1, 3}] :> (x /. IndexDelta[i, j_] y_ :> (y /. i -> j) /. IndexDelta[j_, i] y_ :> (y /. i -> j));
frParOL$ = {vev -> 2 MW sw/EL, lam -> MH^2 EL^2/(8 MW^2 sw^2)};
colOL$ = {SumOver[Index[Colour, _], 3, ___] :> Nc, Mu[g_, Index[Colour, _]] :> Mu[g], Md[g_, Index[Colour, _]] :> Md[g]};
xiOL$ = {(GaugeXi | FAGaugeXi)[A | V[1] | U[1]] -> xA, (GaugeXi | FAGaugeXi)[Z | V[2] | S[2] | U[2]] -> xZ,
   (GaugeXi | FAGaugeXi)[W | V[3] | S[3] | U[3] | U[4]] -> xW};
cleanOL$ = {FCGV["EL"] -> e, EL -> e, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH,
   SMP["e"] -> e, SMP["sin_W"] -> sw, SMP["cos_W"] -> cw, SMP["m_W"] -> MW, SMP["m_Z"] -> MZ, SMP["m_H"] -> MH,
   Ml[_] -> ml, Mu[__] -> mu, Md[__] -> md, MLE[_] -> ml, MQU[_] -> mu, MQD[_] -> md,
   CKM[__] -> 1, IndexDelta[__] -> 1};
(* FeynArts 3.12 on Mathematica 14 prints harmless RuleDelayed::rhs messages when it initializes a model *)
insOL$[model_, tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Classes}, Model -> model,
    GenericModel -> If[model === "SM", "Lorentz", model]], RuleDelayed::rhs];
(* per-diagram amplitudes; xi = 1 ("FR" and "SM1") or general ("SMxi") *)
ampOL$[model_, diags_, in_, out_, lor_] := Module[{a},
   a = Quiet[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> If[model === "SMxi", {}, {_GaugeXi -> 1, _FAGaugeXi -> 1}]],
     RuleDelayed::rhs] /. colOL$;
   If[model === frModelOL$, a = a /. M$FACouplings /. frCoupOL$ //. frSumOL$ /. frParOL$];
   FCFAConvert[a, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, LorentzIndexNames -> lor,
      ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] //.
     Conjugate[x_] :> x /. xiOL$ /. cleanOL$];
(* signature of each diagram: topology number and the internal fields without signs and indices, named alike in both models *)
canonOL$[f_] := (f /. -x_ :> x) /. {F[n_, _] :> F[n], U[3] | U[4] | U[31] | U[32] -> uW};
sigOL$[diags_, next_] := Module[{tops = List @@ diags},
   Flatten[Table[Module[{tn = i},
      {tn, Sort[Cases[#, (Field[n_] -> f_) /; n > next :> canonOL$[f]]]} & /@
       Cases[tops[[i]][[2]], FeynmanGraph[___, Classes == _][r___] :> {r}, Infinity]], {i, Length[tops]}], 1]];


(* ::Text:: *)
(*Reduction to A0, B0: evaluate the fermion traces, project, partial fractions in q (the R_xi propagators carry*)
(*1/((q^2 - M^2)(q^2 - xi M^2))), TID, PaVeReduce; B0 at zero momentum is rewritten with A0 (exact in D),*)
(*B0(0,m,m) = (D-2) A0(m)/(2 m^2), B0(0,0,m) = A0(m)/m^2, B0(0,m1,m2) = (A0(m1) - A0(m2))/(m1^2 - m2^2), A0(0) = B0(0,0,0) = 0.*)
(*The H propagator of the tadpole-attached diagrams carries momentum 0: 1/(0 - MH^2).*)


zeroPropOL$ = {FeynAmpDenominator[a___, PropagatorDenominator[0, m_], b___] :> -1/m^2 FeynAmpDenominator[a, b]};
canonPVOL$ = {PaVe[0, {}, {m2_}] :> A0OL[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0OL[p2, Sequence @@ Sort[{m1, m2}]]};
b0zeroOL$ = {B0OL[0, 0, 0] -> 0, A0OL[0] -> 0, B0OL[0, 0, m_] :> A0OL[m]/m,
   B0OL[0, m_, m_] :> (D - 2) A0OL[m]/(2 m), B0OL[0, m1_, m2_] :> (A0OL[m1] - A0OL[m2])/(m1 - m2)};
redOL$[x_, proj_] := Module[{y},
   y = FCI[x] /. zeroPropOL$ /. FeynAmpDenominator[] -> 1;
   y = y /. DiracTrace[t_] :> DiracTrace[t, DiracTraceEvaluate -> True];
   y = Contract[y proj];
   y = ApartFF[y, {q}];
   (* identical denominators (the xi_A part of the photon propagator, 1/q^4) merged first: TID otherwise treats them*)
   (* as a zero-momentum edge with vanishing Gram determinant and gives wrong poles (QCD note, step (3)) *)
   y = FDS[y, q];
   y = TID[y, q, ToPaVe -> True]/(I Pi^2);
   y = PaVeReduce[FCI[y]];
   y = Expand[FCE[y] /. canonPVOL$ /. b0zeroOL$];
   Collect[y /. SPD[k, k] -> kk /. SP[k, k] -> kk, {_A0OL, _B0OL}, Together]];
projVVg$ = MTD[li1, li2]; projVVkk$ = FVD[k, li1] FVD[k, li2]; projVS$ = FVD[k, li1];
(* the processes (FeynRules fields; SM.mod: V[3] -> -V[3], S[3] -> -S[3]) and the external-leg factors FR/SM.mod *)
procsOL$ = <|"AA" -> {{V[1]} -> {V[1]}, 1}, "AZ" -> {{V[1]} -> {V[2]}, -1}, "ZZ" -> {{V[2]} -> {V[2]}, 1},
   "WW" -> {{V[3]} -> {V[3]}, 1}, "HH" -> {{S[1]} -> {S[1]}, 1}, "AG0" -> {{V[1]} -> {S[2]}, -1},
   "ZG0" -> {{V[2]} -> {S[2]}, 1}, "G0Z" -> {{S[2]} -> {V[2]}, 1}, "G0G0" -> {{S[2]} -> {S[2]}, 1},
   "WG" -> {{V[3]} -> {S[3]}, I}, "GW" -> {{S[3]} -> {V[3]}, -I}, "GG" -> {{S[3]} -> {S[3]}, 1}|>;
toSMOL$[p_] := p /. {V[3] -> -V[3], S[3] -> -S[3]};
kindOL$[key_] := Switch[key, "AA" | "AZ" | "ZZ" | "WW", "VV", "AG0" | "ZG0" | "WG", "VS", "G0Z" | "GW", "SV", _, "SS"];
tAllOL$ = CreateTopologies[1, 1 -> 1];
t1PIOL$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
(* the tadpole-attached topology: a tadpole loop joined to the line by one propagator (Propagator[Internal]).  Only the*)
(* Higgs boson can join it: tadpoles of A, Z (Lorentz invariance), G0 (CP) and G+- (charge) vanish, and a photon line*)
(* at zero momentum would be 1/0 *)
tAttOL$ = tAllOL$[[Flatten[Position[List @@ tAllOL$, t_ /; !MemberQ[List @@ t1PIOL$, t], {1}, Heads -> False]]]];
tTadOL$ = CreateTopologies[1, 1 -> 0];
(* reduced amplitudes of every diagram: {signature, X_g, X_kk} for VV, {signature, X_k} for VS/SV, {signature, X} for SS *)
seOL$[model_, key_, tops_, reg_ : False] := Module[{proc = procsOL$[key][[1]], d, amps, sigs, kind = kindOL$[key]},
   If[model =!= frModelOL$, proc = toSMOL$[proc]];
   d = insOL$[If[model === frModelOL$, model, "SM"], If[tops === "tad", tAttOL$, tops], proc];
   If[Length[d] == 0, Return[{}, Module]];
   If[tops === "tad", Module[{conn = First[Cases[d[[1, 1]], Propagator[Internal][_, _, Field[n_]] :> n, {1}]]},
      d = DiagramSelect[d, MemberQ[#, Field[conn] -> S[1]] &]]];
   sigs = If[tops === "tad", {"tad", Last[#]} & /@ sigOL$[d, 2], sigOL$[d, 2]];
   amps = ampOL$[model, d, {k}, {k}, Switch[kind, "VV", {li1, li2}, "VS" | "SV", {li1}, _, {}]];
   (* IR regulator for the UV poles: every massless propagator gets the mass lam *)
   If[reg, amps = FCI[amps] /. PropagatorDenominator[p_, 0] :> PropagatorDenominator[p, lam]];
   If[Length[amps] =!= Length[sigs], Print["signature mismatch ", key]];
   Table[Module[{r = Check[Switch[kind,
         "VV", {sigs[[i]], redOL$[amps[[i]], projVVg$], redOL$[amps[[i]], projVVkk$]},
         "VS" | "SV", {sigs[[i]], redOL$[amps[[i]], projVS$]},
         _, {sigs[[i]], redOL$[amps[[i]], 1]}], $Failed]},
      If[r === $Failed || !FreeQ[r, Indeterminate | ComplexInfinity | DirectedInfinity],
       Print["   reduction failed: ", model /. frModelOL$ -> "FR", " ", key, " diagram ", i, " ", sigs[[i]], ": ",
        InputForm[Short[FCE[amps[[i]]], 15]]]];
      r], {i, Length[amps]}]];
tadOL$[model_] := Module[{d = insOL$[If[model === frModelOL$, model, "SM"], tTadOL$, {S[1]} -> {}], amps},
   amps = ampOL$[model, d, {k}, {}, {}];
   Transpose[{sigOL$[d, 1], redOL$[#, 1] & /@ amps}]];
fermQOL$[sig_] := !FreeQ[sig, F];
sumOL$[list_, sel_] := Together[Total[Select[list, sel[#[[1]]] &][[All, 2 ;;]]]];


(* ::Section:: *)
(*(b) Feynman gauge (FeynRules model) against the note*)


(* ::Text:: *)
(*K Sigma_T = -X_T, K Sigma^H = X, K T = X;  then D-dimensional coefficients expanded at d = 4 with the rational terms:*)
(*c(D) F -> c(4) F - 2 c'(4) res(F), res(A0(m^2)) = m^2, res(B0) = 1, and A0(m^2) = m^2 (B0(0,m,m) + 1).*)


t0OL$ = AbsoluteTime[];
frSE$ = Association[Table[key -> seOL$[frModelOL$, key, t1PIOL$], {key, {"AA", "AZ", "ZZ", "WW", "HH"}}]];
frTad$ = tadOL$[frModelOL$];
Print["(b) FeynRules model, Feynman gauge: 1PI diagrams (fermion loops at class level, boson loops) AA, AZ, ZZ, WW, HH, tadpole = ",
  {Count[#[[All, 1]], s_ /; fermQOL$[s]], Count[#[[All, 1]], s_ /; !fermQOL$[s]]} & /@ Append[Values[frSE$], frTad$],
  "   (expect {3, 8}, {3, 8}, {4, 12}, {2, 17}, {3, 16}, {3, 8})"];
sigTOL$[list_, sel_] := Module[{xs = sumOL$[list, sel]}, Together[-(xs[[1]] - xs[[2]]/kk)/(D - 1)]];
to4OL$[x_] := Module[{y = Expand[x], fs, c},
   fs = Union[Cases[y, _A0OL | _B0OL, Infinity]];
   Sum[c = Together[Coefficient[y, f]]; (c /. D -> 4) f - 2 (D[c, D] /. D -> 4) If[Head[f] === A0OL, f[[1]], 1], {f, fs}] +
    (y /. {_A0OL -> 0, _B0OL -> 0} /. D -> 4)];
fin4OL$[x_] := Expand[to4OL$[x] /. A0OL[m2_] :> m2 (B0OL[0, m2, m2] + 1)];
fcOL$ = Association[];
Do[fcOL$[key] = fin4OL$ /@ {sigTOL$[frSE$[key], fermQOL$], sigTOL$[frSE$[key], !fermQOL$[#] &]}, {key, {"AA", "AZ", "ZZ", "WW"}}];
fcOL$["HH"] = fin4OL$ /@ {sumOL$[frSE$["HH"], fermQOL$][[1]], sumOL$[frSE$["HH"], !fermQOL$[#] &][[1]]};
fcOL$["T"] = fin4OL$ /@ {sumOL$[frTad$, fermQOL$][[1]], sumOL$[frTad$, !fermQOL$[#] &][[1]]};


(* ::Text:: *)
(*The note's formulas, times K, per generation (ml, mu, md; Nc), with c = MW/MZ, s = sqrt(1 - c^2) and B0OL[k2, m1^2, m2^2].*)


b00OL[m2_] := B0OL[0, m2, m2];
a0nOL[m2_] := m2 (b00OL[m2] + 1);
b0zOL[m1_, m2_] := Which[m1 === m2, b00OL[m1], m1 === 0, b00OL[m2] + 1, m2 === 0, b00OL[m1] + 1, True, (a0nOL[m1] - a0nOL[m2])/(m1 - m2)];
FFOL[k2_, m2_] := -(k2 + 2 m2) B0OL[k2, m2, m2] + 2 m2 b00OL[m2] + k2/3;
GGOL[k2_, m12_, m22_] := (-(k2 - (m12 + m22)/2) B0OL[k2, Sequence @@ Sort[{m12, m22}]] + k2/3 + m12 b00OL[m12] + m22 b00OL[m22] +
    (m12 - m22)^2/(2 k2) (B0OL[k2, Sequence @@ Sort[{m12, m22}]] - b0zOL[m12, m22])) /. b00OL[0] -> 0 /. B0OL[0, 0, 0] -> 0;
sN = Sqrt[1 - c^2]; MZ2N = MW^2/c^2;
fermOL$ = {{1, -1, -1/2, ml^2}, {1, 0, 1/2, 0}, {Nc, 2/3, 1/2, mu^2}, {Nc, -1/3, -1/2, md^2}};
gVN[q_, t3_] := (t3 - 2 q sN^2)/(2 sN c); gAN[t3_] := t3/(2 sN c);
noteF["AA"] = -e^2 (4/3) Sum[f[[1]] f[[2]]^2 FFOL[kk, f[[4]]], {f, fermOL$}];
noteF["AZ"] = -e^2 (4/3) Sum[f[[1]] f[[2]] gVN[f[[2]], f[[3]]] FFOL[kk, f[[4]]], {f, fermOL$}];
noteF["ZZ"] = -e^2 Sum[f[[1]] ((4/3) (gVN[f[[2]], f[[3]]]^2 + gAN[f[[3]]]^2) FFOL[kk, f[[4]]] + f[[4]]/(2 sN^2 c^2) B0OL[kk, f[[4]], f[[4]]]), {f, fermOL$}];
noteF["WW"] = -e^2/(3 sN^2) (GGOL[kk, 0, ml^2] + Nc GGOL[kk, mu^2, md^2]);
noteF["HH"] = -e^2 Sum[f[[1]] f[[4]]/(2 sN^2 MW^2) (2 a0nOL[f[[4]]] + (4 f[[4]] - kk) B0OL[kk, f[[4]], f[[4]]]), {f, fermOL$}];
noteF["T"] = -2 e/(sN MW) Sum[f[[1]] f[[4]] a0nOL[f[[4]]], {f, fermOL$}];
noteB["AA"] = -e^2 ((3 kk + 4 MW^2) B0OL[kk, MW^2, MW^2] - 4 MW^2 b00OL[MW^2]);
noteB["AZ"] = -e^2/(3 sN c) (((9 c^2 + 1/2) kk + (12 c^2 + 4) MW^2) B0OL[kk, MW^2, MW^2] - (12 c^2 - 2) MW^2 b00OL[MW^2] + kk/3);
noteB["ZZ"] = -e^2 (1/(6 sN^2 c^2) (((18 c^4 + 2 c^2 - 1/2) kk + (24 c^4 + 16 c^2 - 10) MW^2) B0OL[kk, MW^2, MW^2] -
       (24 c^4 - 8 c^2 + 2) MW^2 b00OL[MW^2] + (4 c^2 - 1) kk/3) +
     1/(12 sN^2 c^2) ((2 MH^2 - 10 MZ2N - kk) B0OL[kk, Sequence @@ Sort[{MH^2, MZ2N}]] - 2 MZ2N b00OL[MZ2N] - 2 MH^2 b00OL[MH^2] -
       (MZ2N - MH^2)^2/kk (B0OL[kk, Sequence @@ Sort[{MH^2, MZ2N}]] - b0zOL[MZ2N, MH^2]) - 2 kk/3));
noteB["WW"] = -e^2 ((2/3) ((2 MW^2 + 5 kk) B0OL[kk, 0, MW^2] - 2 MW^2 b00OL[MW^2] - MW^4/kk (B0OL[kk, 0, MW^2] - b0zOL[MW^2, 0]) + kk/3) +
     1/(12 sN^2) (((40 c^2 - 1) kk + (16 c^2 + 54 - 10/c^2) MW^2) B0OL[kk, Sequence @@ Sort[{MW^2, MZ2N}]] -
       (16 c^2 + 2) (MW^2 b00OL[MW^2] + MZ2N b00OL[MZ2N]) + (4 c^2 - 1) 2 kk/3 -
       (8 c^2 + 1) (MW^2 - MZ2N)^2/kk (B0OL[kk, Sequence @@ Sort[{MW^2, MZ2N}]] - b0zOL[MW^2, MZ2N])) +
     1/(12 sN^2) ((2 MH^2 - 10 MW^2 - kk) B0OL[kk, Sequence @@ Sort[{MH^2, MW^2}]] - 2 MW^2 b00OL[MW^2] - 2 MH^2 b00OL[MH^2] -
       (MW^2 - MH^2)^2/kk (B0OL[kk, Sequence @@ Sort[{MH^2, MW^2}]] - b0zOL[MW^2, MH^2]) - 2 kk/3));
noteB["HH"] = e^2/(8 sN^2 MW^2) (3 MH^2 a0nOL[MH^2] + 2 (MH^2 + 6 MW^2) a0nOL[MW^2] + (MH^2 + 6 MZ2N) a0nOL[MZ2N] +
     9 MH^4 B0OL[kk, MH^2, MH^2] + 2 (MH^4 - 4 kk MW^2 + 12 MW^4) B0OL[kk, MW^2, MW^2] + (MH^4 - 4 kk MZ2N + 12 MZ2N^2) B0OL[kk, MZ2N, MZ2N] -
     24 MW^4 - 12 MZ2N^2);
noteB["T"] = e/(4 sN MW) (3 MH^2 a0nOL[MH^2] + 2 (MH^2 + 6 MW^2) a0nOL[MW^2] + (MH^2 + 6 MZ2N) a0nOL[MZ2N] - 8 MW^4 - 4 MZ2N^2);
toCOL$[x_] := x /. {cw -> c, sw -> Sqrt[1 - c^2]} /. MZ -> MW/c /. B0OL[p_, m1_, m2_] :> B0OL[p, Sequence @@ Sort[{m1, m2}]];
diffOL$[x_, y_] := Simplify[Expand[toCOL$[x] - toCOL$[y]] /. Sqrt[1 - c^2]^n_ :> (1 - c^2)^(n/2), 0 < c < 1];
noteDiff$ = Table[{key, diffOL$[fcOL$[key][[1]], noteF[key]], diffOL$[fcOL$[key][[2]], noteB[key]]}, {key, {"AA", "AZ", "ZZ", "WW", "HH", "T"}}];
Print["   time ", Round[AbsoluteTime[] - t0OL$], " s"];
Print["(b) FeynCalc (d = 4 with rational terms) minus the note, {fermion loops, boson loops}: ", InputForm[noteDiff$],
  "   (expect all 0)"];


(* ::Section:: *)
(*(c) SM.mod at xi = 1 against the FeynRules model, diagram groups*)


(* ::Text:: *)
(*Every self-energy and mixing with all diagrams (1PI and tadpole-attached), D dimensions, no expansion.  Groups: same*)
(*topology and the same internal fields.  FR = factor x SM.mod with the external-leg factors of procsOL$.*)


cmpKeysOL$ = {"AA", "AZ", "ZZ", "WW", "HH", "AG0", "ZG0", "G0Z", "G0G0", "WG", "GW", "GG"};
allOL$[model_, key_] := Join[seOL$[model, key, t1PIOL$], seOL$[model, key, "tad"]];
frAll$ = Association[Table[key -> allOL$[frModelOL$, key], {key, cmpKeysOL$}]];
sm1All$ = Association[Table[key -> allOL$["SM1", key], {key, cmpKeysOL$}]];
normOL$[x_] := Simplify[Expand[x /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}], MZ > MW > 0];
grpOL$[list_] := Map[Total, GroupBy[list, First -> Rest], {1}];
cmpGroups$ = Table[Module[{gF = grpOL$[frAll$[key]], gS = grpOL$[sm1All$[key]], f = procsOL$[key][[2]], keysAll},
    keysAll = Union[Keys[gF], Keys[gS]];
    {key, Length[keysAll], Select[keysAll, !(KeyExistsQ[gF, #] && KeyExistsQ[gS, #] &&
          And @@ PossibleZeroQ /@ normOL$[gF[#] - f gS[#]]) &]}], {key, cmpKeysOL$}];
tadCmp$ = Module[{gF = grpOL$[frTad$], gS = grpOL$[tadOL$["SM1"]]},
   {Length[Union[Keys[gF], Keys[gS]]], Select[Union[Keys[gF], Keys[gS]], !(KeyExistsQ[gF, #] && KeyExistsQ[gS, #] &&
        And @@ PossibleZeroQ /@ normOL$[gF[#] - gS[#]]) &]}];
Print["(c) FeynRules model vs SM.mod (xi = 1), diagram groups per two-point function {key, groups, groups that differ}: ",
  InputForm[cmpGroups$], ";  tadpole: ", InputForm[tadCmp$], "   (expect no group that differs)"];
Print["   time ", Round[AbsoluteTime[] - t0OL$], " s"];
Print["(c) diagrams (FR, SM.mod) per two-point function: ", InputForm[Table[{key, Length[frAll$[key]], Length[sm1All$[key]]}, {key, cmpKeysOL$}]]];


(* ::Section:: *)
(*(d) General R_xi (SM.mod): Slavnov-Taylor identities, Sigma^AA(0), on-shell xi dependence, UV poles*)


xiAll$ = Association[Table[key -> allOL$["SMxi", key], {key, cmpKeysOL$}]];
xiTad$ = tadOL$["SMxi"];
(* in the FeynRules convention: factor x SM.mod *)
fullX$[key_, sel_] := procsOL$[key][[2]] sumOL$[xiAll$[key], sel];
Print["(d) topologies of 1 -> 1: ", Length[tAllOL$], " (1PI ", Length[t1PIOL$], ", tadpole-attached ", Length[tAttOL$], ")"];
stOL$[sel_] := Module[{kkX, kX, X},
   kkX[key_] := fullX$[key, sel][[2]]; kX[key_] := fullX$[key, sel][[1]]; X[key_] := fullX$[key, sel][[1]];
   {Simplify[kkX["AA"]],
    Simplify[kkX["AZ"] + I MZ kX["AG0"]],
    Simplify[kkX["ZZ"] + I MZ kX["ZG0"] - I MZ kX["G0Z"] + MZ^2 X["G0G0"]],
    Simplify[kkX["WW"] + I MW kX["WG"] - I MW kX["GW"] + MW^2 X["GG"]]} /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ} // Simplify];
stAll$ = stOL$[True &];
st1PI$ = stOL$[#[[1]] =!= "tad" &];
Print["(d) Slavnov-Taylor identities, all diagrams (1PI + tadpole-attached), general xi_A, xi_Z, xi_W: ",
  "{AA, AZ, ZZ-G0, WW-G+} = ", InputForm[stAll$], "   (expect {0, 0, 0, 0})"];
xiT$ = sumOL$[xiTad$, True &][[1]];
Print["(d) without the tadpole-attached diagrams the identities for AA, AZ hold, for ZZ and WW the remainder divided by",
  " K T (general xi) is ", InputForm[Simplify[{st1PI$[[1]], st1PI$[[2]], st1PI$[[3]]/xiT$, st1PI$[[4]]/xiT$} /.
     {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0]], "   (Denner's form of the identities has these T terms)"];


(* ::Text:: *)
(*Self-energies at k = 0 (vacuum integrals, exact in D): Sigma_T(0) = Sigma_L(0) = -g_{mu nu} X^{mu nu}(0)/D (1PI diagrams).*)


zeroOL$[key_] := Module[{proc = toSMOL$[procsOL$[key][[1]]], d, amps},
   d = insOL$["SM", t1PIOL$, proc];
   amps = ampOL$["SMxi", d, {k}, {k}, {li1, li2}];
   Together[-procsOL$[key][[2]] Total[redOL$[FCReplaceMomenta[#, {k -> 0}], projVVg$] & /@ amps]/D]];
sigAA0$ = zeroOL$["AA"]; sigAZ0$ = zeroOL$["AZ"];
Print["(d) K Sigma^AA_T(0), general xi: ", InputForm[Simplify[sigAA0$]], "   (expect 0)"];
sigAZ0n$ = Simplify[sigAZ0$ /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0];
(* A0(xi m^2) = xi^(D/2 - 1) A0(m^2) exactly in dimensional regularization *)
sigAZ0s$ = Simplify[sigAZ0n$ /. A0OL[MW^2 xW] -> xW^(D/2 - 1) A0OL[MW^2]];
Print["(d) K Sigma^AZ_T(0), general xi: ", InputForm[sigAZ0n$], ";  limit xi_W -> 1 minus Eq. (Pi0) (K Sigma = -2 e^2 MW^2/(s c) B0(0,MW,MW)): ",
  InputForm[Simplify[Limit[sigAZ0s$, xW -> 1] - (-2 e^2 MW^2/(Sqrt[1 - MW^2/MZ^2] MW/MZ) (D - 2) A0OL[MW^2]/(2 MW^2)), MZ > MW > 0]],
  ";  its UV pole / Delta: ", InputForm[Factor[Simplify[Coefficient[Expand[sigAZ0n$ /. A0OL[m_] :> m dUV /. D -> 4], dUV], MZ > MW > 0]]]];


(* ::Text:: *)
(*xi dependence on shell: the transverse self-energies with the tadpole-attached diagrams at k^2 = M^2, general xi minus*)
(*xi = 1 (the gauge-independent mass counterterms of the Fleischer-Jegerlehner treatment of the tadpoles).*)


xTOL$[list_] := Module[{xs = sumOL$[list, True &]}, Together[-(xs[[1]] - xs[[2]]/kk)/(D - 1)]];
onShell$ = {Simplify[(xTOL$[xiAll$["ZZ"]] - xTOL$[sm1All$["ZZ"]]) /. kk -> MZ^2 /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0],
   Simplify[(xTOL$[xiAll$["WW"]] - xTOL$[sm1All$["WW"]]) /. kk -> MW^2 /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0],
   Simplify[(sumOL$[xiAll$["HH"], True &][[1]] - sumOL$[sm1All$["HH"], True &][[1]]) /. kk -> MH^2 /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0]};
Print["(d) on shell, general xi minus xi = 1, with the tadpole-attached diagrams: K Sigma^ZZ_T(MZ^2), K Sigma^W_T(MW^2), K Sigma^H(MH^2) = ",
  InputForm[onShell$], "   (expect {0, 0, 0})"];
onePIOL$[list_] := Select[list, #[[1, 1]] =!= "tad" &];
onShell1PI$ = Simplify[(xTOL$[onePIOL$[xiAll$["ZZ"]]] - xTOL$[onePIOL$[sm1All$["ZZ"]]]) /. kk -> MZ^2 /.
     {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0];
Print["(d) the same for Sigma^ZZ_T(MZ^2) without the tadpole-attached diagrams (expect nonzero): ", InputForm[Short[onShell1PI$, 10]]];


(* ::Text:: *)
(*UV poles of the 1PI functions (the note's definitions, no tadpole-attached diagrams), in the note's convention:*)
(*A0(m^2) -> m^2 Delta + finite, B0 -> Delta + finite, the coefficient of Delta at D = 4; the three-point functions*)
(*left by the doubled photon propagator (xi_A) are UV finite.  K Sigma pole / Delta as a function of xi.*)


poleOL$[x_] := Simplify[Coefficient[Expand[x /. {A0OL[m_] :> m dUV + a0fin[m], B0OL[a__] :> dUV + b0fin[a]} /. D -> 4], dUV] /.
     {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0];
(* the W self-energy has internal photons: its xi_A part contains the scaleless 1/q^4, whose UV pole is cancelled by an*)
(* IR pole in dimensional regularization; the photon (and photon-ghost) mass lam separates them, lam -> 0 afterwards *)
wwReg$ = seOL$["SMxi", "WW", t1PIOL$, True];
poleWWnoReg$ = poleOL$[xTOL$[onePIOL$[xiAll$["WW"]]]];
poleWWreg$ = Simplify[Normal[Series[poleOL$[xTOL$[wwReg$]], {lam, 0, 0}]] /. lam -> 0];
Print["(d) W self-energy, 1/eps coefficient without the IR regulator minus the UV pole (IR poles of the xi_A part): ",
  InputForm[Simplify[poleWWnoReg$ - poleWWreg$]]];
poles$ = Association[
   Table[key -> procsOL$[key][[2]] poleOL$[xTOL$[onePIOL$[xiAll$[key]]]], {key, {"AA", "AZ", "ZZ"}}], "WW" -> poleWWreg$,
   "HH" -> poleOL$[sumOL$[onePIOL$[xiAll$["HH"]], True &][[1]]], "T" -> poleOL$[xiT$]];
(* at xi = 1 the poles must be those of the note's formulas *)
notePole$[key_] := Simplify[Coefficient[Expand[(Sum[noteF[key], {1}] + noteB[key]) /.
       {B0OL[a__] :> dUV + b0fin[a]}], dUV] /. c -> MW/MZ, MZ > MW > 0];
Print["(d) UV poles at xi = 1 minus the note's (AA, AZ, ZZ, WW, HH, T): ",
  InputForm[Table[Simplify[(poles$[key] /. {xA -> 1, xZ -> 1, xW -> 1}) - notePole$[key], MZ > MW > 0], {key, Keys[poles$]}]], "   (expect 0)"];
Do[Print["(d) UV pole of K Sigma ", key, " / Delta: ", InputForm[Collect[poles$[key], {xA, xZ, xW, kk}, Simplify]]], {key, Keys[poles$]}];
(* charge renormalization delta Z_e = Pi^AA(0)/2 + (s/c) Sigma^AZ_T(0)/MZ^2 (Eq. (dZe)): its pole must not depend on xi and*)
(* must be ((4/3) sum Nc Q^2 - 7)/2 per generation (Eq. (beta)) *)
dZePole$ = Simplify[(D[poles$["AA"], kk]/2 + (Sqrt[1 - MW^2/MZ^2]/(MW/MZ)) (poles$["AZ"] /. kk -> 0)/MZ^2)/e^2, MZ > MW > 0];
Print["(d) pole of K delta Z_e / e^2, general xi: ", InputForm[dZePole$], ";  minus ((4/3)(1 + 5 Nc/9) - 7)/2: ",
  InputForm[Simplify[dZePole$ - ((4/3) (1 + 5 Nc/9) - 7)/2]], "   (expect 0)"];

Print["   time ", Round[AbsoluteTime[] - t0OL$], " s"];


(* ::Section:: *)
(*(e) Finite parts: every B0 of the note's formulas from LoopTools and Package-X*)


(* ::Text:: *)
(*Point: alpha = 1/137.035999177, MW = 80.3692, MZ = 91.1880, MH = 125.20 GeV, PDG 2024 fermion masses (u, d, s: 2.16,*)
(*4.70, 93.5 MeV), mu = MZ, Delta = 0.  Kinematics as exact rationals (LoopTools warns about floating-point B0 arguments).*)
(*FeynHelpers returns a/Epsilon + b in FeynCalc's normalization; the Delta = 0 value is b + a (EulerGamma + Log[Pi])*)
(*(checked against the Feynman-parameter integral).  Quantities: K Sigma^AA_T, K Sigma^AZ_T, K Sigma^ZZ_T, K Sigma^W_T at*)
(*k^2 = -MZ^2, MW^2, MZ^2, (200 GeV)^2; K Sigma^H at -MH^2, MH^2, (300 GeV)^2; K T.*)


numOL$ = Module[{mw = 803692/10000, mz = 911880/10000},
   {e -> Sqrt[4 Pi 1000000000/137035999177], c -> mw/mz, MW -> mw, MZ -> mz, MH -> 12520/100, Nc -> 3}];
gensOL$ = {{51099895/10^11, 216/10^5, 470/10^5}, {1056583755/10^10, 12730/10^4, 935/10^4}, {177686/10^5, 17257/100, 4183/10^3}};
mu2OL$ = (911880/10000)^2;
ptsOL$ = Module[{mw2 = (803692/10000)^2, mz2 = (911880/10000)^2, mh2 = (12520/100)^2},
   Join[Flatten[Table[{key, x}, {key, {"AA", "AZ", "ZZ", "WW"}}, {x, {-mz2, mw2, mz2, 200^2}}], 1],
    Table[{"HH", x}, {x, {-mh2, mh2, 300^2}}], {{"T", 0}}]];
exprOL$[key_, kkv_] := Expand[(Sum[noteF[key] /. {ml -> g[[1]], mu -> g[[2]], md -> g[[3]]}, {g, gensOL$}] + noteB[key]) /.
     numOL$ /. kk -> kkv];
exprsOL$ = exprOL$ @@@ ptsOL$;
b0ListOL$ = Union[Cases[exprsOL$, _B0OL, Infinity]];
finOL$[v_] := Module[{ser = Series[v, {Epsilon, 0, 0}]}, SeriesCoefficient[ser, 0] + SeriesCoefficient[ser, -1] (EulerGamma + Log[Pi])];
b0ValsOL$ = Table[{N[finOL$[LToolsEvaluate[B0 @@ b, LToolsSetMudim -> mu2OL$]], 20],
     N[finOL$[PaXEvaluate[B0 @@ b] /. ScaleMu -> Sqrt[mu2OL$]], 20]}, {b, List @@@ b0ListOL$}];
Print["(e) ", Length[b0ListOL$], " distinct B0 functions;  max |LoopTools - Package-X| = ", Max[Abs[b0ValsOL$[[All, 1]] - b0ValsOL$[[All, 2]]]]];
coeffsOL$ = Table[Module[{x = exprsOL$[[i]]}, Prepend[Table[{j, N[Coefficient[x, b0ListOL$[[j]]], 20]}, {j, Length[b0ListOL$]}],
      {0, N[x /. _B0OL -> 0, 20]}]], {i, Length[ptsOL$]}];
valsOL$ = Table[Module[{cs = coeffsOL$[[i]]},
    {ptsOL$[[i, 1]], ptsOL$[[i, 2]], cs[[1, 2]] + Sum[cs[[j + 1, 2]] b0ValsOL$[[j, 1]], {j, Length[b0ListOL$]}],
     cs[[1, 2]] + Sum[cs[[j + 1, 2]] b0ValsOL$[[j, 2]], {j, Length[b0ListOL$]}]}], {i, Length[ptsOL$]}];
fmtOL$[x_] := ToString[NumberForm[Chop[N[x], 10^-9], 14], OutputForm];
Do[Print["   ", v[[1]], "  k^2 = ", fmtOL$[v[[2]]], ":  LoopTools ", fmtOL$[v[[3]]], ",  Package-X ", fmtOL$[v[[4]]]], {v, valsOL$}];
Print["(e) max relative |LoopTools - Package-X| of the quantities: ", Max[Abs[(#[[3]] - #[[4]])/#[[3]]] & /@ valsOL$]];
numStrOL$[x_] := ToString[CForm[N[x, 17]]];
Export[FileNameJoin[{srcDirOL$, "results", "oneloop_b0.csv"}], StringRiffle[Prepend[Table[StringRiffle[
       Join[{ToString[j]}, numStrOL$ /@ List @@ b0ListOL$[[j]], numStrOL$ /@ {Re[b0ValsOL$[[j, 1]]], Im[b0ValsOL$[[j, 1]]],
          Re[b0ValsOL$[[j, 2]]], Im[b0ValsOL$[[j, 2]]]}], ","], {j, Length[b0ListOL$]}],
     "index,p2,m1sq,m2sq,re_lt,im_lt,re_px,im_px"], "\n"] <> "\n", "Text"];
Export[FileNameJoin[{srcDirOL$, "results", "oneloop_coeffs.csv"}], StringRiffle[Prepend[Flatten[Table[
       StringRiffle[{ptsOL$[[i, 1]], numStrOL$[ptsOL$[[i, 2]]], ToString[#[[1]]], numStrOL$[#[[2]]]}, ","] & /@
        Select[coeffsOL$[[i]], #[[1]] == 0 || #[[2]] != 0 &], {i, Length[ptsOL$]}]],
     "key,kk,index,coefficient"], "\n"] <> "\n", "Text"];
Print["(e) wrote results/oneloop_b0.csv and results/oneloop_coeffs.csv;  mu^2 = ", ToString[N[mu2OL$, 16], OutputForm]];
DumpSave[FileNameJoin[{srcDirOL$, "work", "oneloop_feyncalc.mx"}], {frSE$, frTad$, frAll$, sm1All$, xiAll$, xiTad$}];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
