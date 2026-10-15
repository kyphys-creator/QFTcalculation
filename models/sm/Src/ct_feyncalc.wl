(* ::Package:: *)

(* ::Title:: *)
(*Step (4): on-shell counterterms, charge renormalization in R_xi gauge, tadpole schemes (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm, step (4).  Compares with Eqs. (ct), (dsw), (dZe), (Pi0), (Txi).*)
(*(a) Pi^AA(0) and Sigma^AZ_T(0) from the self-energy diagrams expanded in the external momentum: k -> t k, every*)
(*    propagator 1/((q + b k)^2 - m^2) expanded to t^2, the numerators averaged over the directions of q*)
(*    ((q.k)^2 -> q^2 k^2/D, (q.k)^4 -> 3 q^4 k^4/(D(D+2))), partial fractions in q^2 and the vacuum integrals*)
(*    int 1/(q^2 - M)^n = [prod_{j=1}^{n-1} (D/2 - j)]/(n-1)! A0(M)/M^(n-1) (zero for M = 0), exact in D.  Feynman gauge*)
(*    (FeynRules model) against Eq. (Pi0) and Eq. (dZe); general R_xi (SM.mod): delta Z_e = Pi^AA(0)/2 + (s/c)*)
(*    Sigma^AZ_T(0)/MZ^2 must not depend on xi, while Pi^AA(0) and Sigma^AZ_T(0) do.*)
(*(b) Tadpole schemes: the tadpole-attached diagrams of the W, Z, H self-energies are c_V T; the mass counterterms of*)
(*    the scheme delta t = -T (Eq. (ct)) and of Fleischer-Jegerlehner (tadpoles included, xi independent, step (3))*)
(*    differ by c_V T.  c_W/MW^2 = c_Z/MZ^2, so delta s_W^2 (Eq. (dsw)) is the same in both and does not depend on xi;*)
(*    the tadpole of SM.mod in general xi against Eq. (Txi).*)
(*(c) The note's counterterms (Feynman gauge, Eqs. (ct), (dsw), (dZe), with Eqs. (T)-(SH), (Pi0)) at the numerical point*)
(*    of step (3), as A0/B0/DB0 expressions -> results/ct_note.m, evaluated against FormCalc's RenConst in*)
(*    ct_formcalc.wl.*)
(*Normalization as in oneloop_feyncalc.wl: X = (FeynArts amplitude with PreFactor -> 1)/(I Pi^2), K Sigma_T = -X_T,*)
(*K Sigma^H = X, K T = X (K = (4 Pi)^2), X_T = (g X - kk X/k^2)/(D - 1).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file ct_feyncalc.wl.  Interactive:  ~/hep/bin/wopen ct_feyncalc.wl, then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
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
(*The note's formulas*)


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
sigTOL$[list_, sel_] := Module[{xs = sumOL$[list, sel]}, Together[-(xs[[1]] - xs[[2]]/kk)/(D - 1)]];
to4OL$[x_] := Module[{y = Expand[x], fs, c},
   fs = Union[Cases[y, _A0OL | _B0OL, Infinity]];
   Sum[c = Together[Coefficient[y, f]]; (c /. D -> 4) f - 2 (D[c, D] /. D -> 4) If[Head[f] === A0OL, f[[1]], 1], {f, fs}] +
    (y /. {_A0OL -> 0, _B0OL -> 0} /. D -> 4)];
fin4OL$[x_] := Expand[to4OL$[x] /. A0OL[m2_] :> m2 (B0OL[0, m2, m2] + 1)];


(* ::Section:: *)
(*(a) Pi^AA(0), Sigma^AZ_T(0) and delta Z_e*)


(* ::Text:: *)
(*Expansion in the external momentum.  After the traces and the projection the integrand depends on q.k, q^2, k^2;*)
(*den[m] = 1/(q^2 - m^2).  tt counts the powers of k (also in the projector).*)


DataType[tt, FCVariable] = True;
expDenCT$[PropagatorDenominator[mom_, m_], n_] := Module[{mm = MomentumExpand[mom], a, b, y},
   a = Coefficient[mm, Momentum[q, D]]; b = Coefficient[mm, Momentum[k, D]];
   y = 2 a b tt qkCT + b^2 tt^2 kk;
   If[b === 0, denCT[m], Sum[(-y)^j denCT[m]^(j + 1), {j, 0, n}]]];
angCT$[x_] := Expand[x] /. qkCT^j_. :> If[OddQ[j], 0, (q2CT kk)^(j/2) (j - 1)!!/Product[D + 2 i, {i, 0, j/2 - 1}]];
vacCT$[mm_, n_] := If[mm === 0, 0, Product[D/2 - j, {j, 1, n - 1}]/(n - 1)! A0OL[mm]/mm^(n - 1)];
(* the coefficient of tt^order of the projected integrand, integrated: X in units of I Pi^2 *)
expandCT$[amp_, proj_, order_] := Module[{y, terms},
   y = FCI[amp] /. zeroPropOL$ /. FeynAmpDenominator[] -> 1;
   y = y /. DiracTrace[t_] :> DiracTrace[t, DiracTraceEvaluate -> True];
   y = ExpandScalarProduct[Contract[y proj]];
   y = y /. {Pair[Momentum[q, D], Momentum[k, D]] | Pair[Momentum[k, D], Momentum[q, D]] -> tt qkCT,
       Pair[Momentum[k, D], Momentum[k, D]] -> tt^2 kk, Pair[Momentum[q, D], Momentum[q, D]] -> q2CT};
   If[!FreeQ[y, Pair], Print["   expandCT: scalar products left: ", Union[Cases[y, _Pair, Infinity]]]];
   y = y /. FeynAmpDenominator[pds__] :> Times @@ (expDenCT$[#, 2] & /@ {pds});
   y = Coefficient[Expand[y], tt, order];
   y = Expand[angCT$[y] /. denCT[m_] :> 1/(q2CT - m^2)];
   terms = If[Head[y] === Plus, List @@ y, {y}];
   (* partial fractions in q^2 term by term; (alpha q^2 + beta)^p -> alpha^p vac(-beta/alpha, -p); polynomials in q^2 are scaleless *)
   terms = Flatten[(If[Head[#] === Plus, List @@ #, {#}] &[Apart[#, q2CT]]) & /@ terms];
   terms = terms /. Power[sq_, p_?Negative] /; !FreeQ[sq, q2CT] && Exponent[sq, q2CT] == 1 :>
       Coefficient[sq, q2CT]^p vacCT[-(sq /. q2CT -> 0)/Coefficient[sq, q2CT], -p];
   Together[Total[Select[terms, !FreeQ[#, vacCT] &]] /. vacCT -> vacCT$]];
(* K Sigma_T(0) and K Pi(0) = d K Sigma_T/dk^2 at 0, in the note's convention *)
zeroCT$[model_, key_] := Module[{proc = procsOL$[key][[1]], d, amps, xg0, xkk1, xg1, xkk2},
   If[model =!= frModelOL$, proc = toSMOL$[proc]];
   d = insOL$[If[model === frModelOL$, model, "SM"], t1PIOL$, proc];
   amps = ampOL$[model, d, {k}, {k}, {li1, li2}];
   xg0 = Total[expandCT$[#, projVVg$, 0] & /@ amps];
   xkk1 = Total[expandCT$[#, projVVkk$, 2] & /@ amps]/kk;
   xg1 = Total[expandCT$[#, projVVg$, 2] & /@ amps]/kk;
   xkk2 = Total[expandCT$[#, projVVkk$, 4] & /@ amps]/kk^2;
   (* SM.mod results are converted to the note's convention with the external-leg factor *)
   If[model === frModelOL$, 1, procsOL$[key][[2]]] Simplify /@ {-(xg0 - xkk1)/(D - 1), -(xg1 - xkk2)/(D - 1)}];
t0CT$ = AbsoluteTime[];
aaFR$ = zeroCT$[frModelOL$, "AA"]; azFR$ = zeroCT$[frModelOL$, "AZ"];
Print["(a) Feynman gauge (FeynRules model): K Sigma^AA_T(0) = ", InputForm[aaFR$[[1]]], " (expect 0);  time ", Round[AbsoluteTime[] - t0CT$], " s"];
(* Eq. (Pi0) per generation, times K: K Pi^AA(0) = -e^2 [-(4/3) sum Nc Q^2 B0(0,m,m) + 3 B0(0,MW,MW) + 2/3],
   K Sigma^AZ_T(0) = -e^2 2 MW^2/(s c) B0(0,MW,MW) *)
piNote$ = -e^2 (-(4/3) (b00OL[ml^2] + Nc (4/9) b00OL[mu^2] + Nc (1/9) b00OL[md^2]) + 3 b00OL[MW^2] + 2/3);
azNote$ = -e^2 2 MW^2/(sN c) b00OL[MW^2];
dZeNote$ = -e^2 (-(2/3) (b00OL[ml^2] + Nc (4/9) b00OL[mu^2] + Nc (1/9) b00OL[md^2]) + (7/2) b00OL[MW^2] + 1/3);
Print["(a) Feynman gauge minus Eq. (Pi0) (d = 4 with rational terms): K Pi^AA(0): ", InputForm[diffOL$[fin4OL$[aaFR$[[2]]], piNote$]],
  ",  K Sigma^AZ_T(0): ", InputForm[diffOL$[fin4OL$[azFR$[[1]]], azNote$]], "   (expect 0, 0)"];
dZeFR$ = Together[aaFR$[[2]]/2 + (sw/cw) azFR$[[1]]/MZ^2];
Print["(a) K delta Z_e = K Pi^AA(0)/2 + (s/c) K Sigma^AZ_T(0)/MZ^2 minus Eq. (dZe): ", InputForm[diffOL$[fin4OL$[dZeFR$], dZeNote$]], "   (expect 0)"];
aaXi$ = zeroCT$["SMxi", "AA"]; azXi$ = zeroCT$["SMxi", "AZ"];
scaleCT$ = {A0OL[MW^2 xW] -> xW^(D/2 - 1) A0OL[MW^2], A0OL[MZ^2 xZ] -> xZ^(D/2 - 1) A0OL[MZ^2]};
normCT$[x_] := Simplify[Together[x /. scaleCT$ /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}], MZ > MW > 0];
dZeXi$ = Together[aaXi$[[2]]/2 + (sw/cw) azXi$[[1]]/MZ^2];
Print["(a) general xi (SM.mod), D dimensions: K Sigma^AA_T(0) = ", InputForm[normCT$[aaXi$[[1]]]],
  ";  K Pi^AA(0) - (xi = 1, FeynRules) = ", InputForm[Factor[normCT$[aaXi$[[2]] - aaFR$[[2]]]]],
  ";  K delta Z_e - (xi = 1, FeynRules) = ", InputForm[normCT$[dZeXi$ - dZeFR$]], "   (expect 0, nonzero, 0);  time ", Round[AbsoluteTime[] - t0CT$], " s"];


(* ::Section:: *)
(*(b) Tadpole schemes*)


(* ::Text:: *)
(*K Sigma_tad = c_V K T for the tadpole-attached diagrams (FeynRules model, Feynman gauge; the coefficient is a tree*)
(*coupling times the H propagator at zero momentum and does not depend on xi).*)


tadSE$[key_] := Module[{l = seOL$[frModelOL$, key, "tad"]},
   If[kindOL$[key] === "VV", Together[-(Total[l[[All, 2]]] - Total[l[[All, 3]]]/kk)/(D - 1)], Together[Total[l[[All, 2]]]]]];
kTfr$ = Together[sumOL$[tadOL$[frModelOL$], True &][[1]]];
cV$ = Simplify[{tadSE$["WW"], tadSE$["ZZ"], tadSE$["HH"]}/kTfr$ /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}, MZ > MW > 0];
Print["(b) K Sigma_tad / K T for W, Z, H: ", InputForm[cV$], ";  c_W/MW^2 - c_Z/MZ^2 = ", InputForm[Simplify[cV$[[1]]/MW^2 - cV$[[2]]/MZ^2]],
  "   (expect 0: delta s_W^2 is the same with and without the tadpoles)"];
kTxi$ = Together[sumOL$[tadOL$["SMxi"], True &][[1]]];
kTnote$ = e/(4 sw MW) (-8 (ml^2 A0OL[ml^2] + Nc mu^2 A0OL[mu^2] + Nc md^2 A0OL[md^2]) + 3 MH^2 A0OL[MH^2] + 4 (D - 1) MW^2 A0OL[MW^2] +
     2 (D - 1) MZ^2 A0OL[MZ^2] + 2 MH^2 A0OL[MW^2 xW] + MH^2 A0OL[MZ^2 xZ]);
Print["(b) K T in general xi (SM.mod) minus Eq. (Txi): ", InputForm[normCT$[kTxi$ - kTnote$]], "   (expect 0)"];
Print["(b) xi dependence of the mass counterterms of the scheme delta t = -T: K(delta M_V^2(xi) - delta M_V^2(1)) = -c_V K(T(xi) - T(1)), with",
  " K(T(xi) - T(1)) = ", InputForm[Factor[normCT$[kTxi$ - (kTxi$ /. {xW -> 1, xZ -> 1})]]]];


(* ::Section:: *)
(*(c) The note's counterterms at the numerical point (Feynman gauge) -> results/ct_note.m*)


(* ::Text:: *)
(*Point of oneloop_feyncalc.wl, section (e): alpha = 1/137.035999177, MW = 80.3692, MZ = 91.1880, MH = 125.20 GeV, PDG 2024*)
(*fermion masses.  Sigma = (noteF + noteB)/K summed over the generations; derivatives d/dk^2 B0 -> DB0.  Real parts are*)
(*taken after the numerical evaluation.  Names: dMWsq, dZW, dMZsq, dZZZ, dZAA, dZZA, dZAZ, dMHsq, dZH, dt, dsw2 (delta*)
(*s_W^2/s_W^2), dZe.*)


numCT$ = Module[{mw = 803692/10000, mz = 911880/10000},
   {e -> Sqrt[4 Pi 1000000000/137035999177], c -> mw/mz, MW -> mw, MZ -> mz, MH -> 12520/100, Nc -> 3}];
gensCT$ = {{51099895/10^11, 216/10^5, 470/10^5}, {1056583755/10^10, 12730/10^4, 935/10^4}, {177686/10^5, 17257/100, 4183/10^3}};
sigCT$[key_] := (Sum[noteF[key] /. {ml -> g[[1]], mu -> g[[2]], md -> g[[3]]}, {g, gensCT$}] + noteB[key])/KK;
dsigCT$[key_] := D[sigCT$[key], kk] /. Derivative[1, 0, 0][B0OL][a__] :> DB0OL[a];
gen0CT$[x_] := Sum[x /. {ml -> g[[1]], mu -> g[[2]], md -> g[[3]]}, {g, gensCT$}];
piCT$ = gen0CT$[-e^2 (-(4/3) (b00OL[ml^2] + Nc (4/9) b00OL[mu^2] + Nc (1/9) b00OL[md^2]))]/KK - e^2 (3 b00OL[MW^2] + 2/3)/KK;
az0CT$ = azNote$/KK;
mw2CT$ = MW^2 /. numCT$; mz2CT$ = MZ^2 /. numCT$; mh2CT$ = MH^2 /. numCT$;
ctNote$ = {
   {"dMWsq", sigCT$["WW"] /. kk -> mw2CT$}, {"dZW", -dsigCT$["WW"] /. kk -> mw2CT$},
   {"dMZsq", sigCT$["ZZ"] /. kk -> mz2CT$}, {"dZZZ", -dsigCT$["ZZ"] /. kk -> mz2CT$},
   {"dZAA", -piCT$}, {"dZZA", 2 az0CT$/MZ^2}, {"dZAZ", -2 (sigCT$["AZ"] /. kk -> mz2CT$)/MZ^2},
   {"dMHsq", sigCT$["HH"] /. kk -> mh2CT$}, {"dZH", -dsigCT$["HH"] /. kk -> mh2CT$},
   {"dt", -sigCT$["T"]}};
ctNote$ = {#[[1]], Expand[#[[2]] /. numCT$]} & /@ ctNote$;
Put[ctNote$, FileNameJoin[{srcDirOL$, "results", "ct_note.m"}]];
Print["(c) wrote ", Length[ctNote$], " counterterms of the note to results/ct_note.m (B0OL, DB0OL with squared masses);  functions: ",
  Length[Union[Cases[ctNote$, _B0OL | _DB0OL, Infinity]]], ";  symbols left: ",
  Complement[Union[Cases[ctNote$[[All, 2]], _Symbol, Infinity]], {Pi}]];
Print["   time ", Round[AbsoluteTime[] - t0CT$], " s"];

DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
