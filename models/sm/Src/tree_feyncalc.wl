(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level amplitudes, spin sums and widths with FeynArts + FeynCalc (Standard Model)*)


(* ::Text:: *)
(*Research note models/sm, step (2).  Checks, symbolically unless stated:*)
(*  (a) sign conventions: truncated three- and four-point amplitudes of the FeynRules model (Peskin signs) against*)
(*      FeynArts' SM.mod (Denner's signs); the ratio must be (-1)^(number of photon legs) times -i for each incoming G+*)
(*      (outgoing G-) and +i for each outgoing G+ (incoming G-), from A_Denner = -A and phi+_Denner = -i G+;*)
(*  (b) muon decay: sum|M|^2 (q^2 - M_W^2)^2 = 4 e^4 (p.k3)(k1.k2)/s_W^4 exactly (m_e = 0), i.e. 128 G_F^2 (p.k3)(k1.k2)*)
(*      in the Fermi limit (Eq. (8));*)
(*  (c) the two-body widths W+ -> l+ nu, Z -> f fbar (f = nu, l, u, d), H -> f fbar, t -> b W+ with all masses*)
(*      against Eqs. (9), (10) and their massive forms (App. B);*)
(*  (d) e+ e- -> mu+ mu- (photon and Z, Gamma_Z = 0): sum|M|^2 against Eq. (11);*)
(*  (e) e+ e- -> W+ W-: sum|M|^2 over spins and W polarizations (-g + k k/M_W^2), numbers at six points written to*)
(*      results/tree_feyncalc_ww.csv for the explicit-matrix comparison of tree_numeric.py.*)
(*FeynCalc's FeynArts needs a patched copy of the FeynRules-generated model (FAPatch).  Field codes: F[1..4] = nu, l, u, d;*)
(*V[1..3] = A, Z, W (FeynRules model: V[3] = W+, S[3] = G+;  SM.mod: V[3] = W-, S[3] = G-), S[1] = H, S[2] = G0.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
$FAVerbose = 0;

srcDirTr$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirTr$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTr$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirTr$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTr$, "SM_FA"}], Quiet -> True];
frModel$ = FileNameJoin[{modelTmpDirTr$, "SM_FA", "SM_FA"}];


(* ::Text:: *)
(*Common symbols: e, sw, cw, MW, MZ, MH and masses mf[class, generation].  FeynRules model: M$FACouplings, then the*)
(*diagonal Yukawa couplings y = sqrt2 m/v with v = 2 MW sw/e, lam = MH^2/(2 v^2), CKM = 1.  SM.mod: FCGV symbols.*)


frRules$ = {yl[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[2, a]/vev, yu[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[3, a]/vev,
   yd[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[4, a]/vev, CKM[a_, b_] :> IndexDelta[a, b]};
frSum$ = IndexSum[x_, {i_, 1, 3}] :> Sum[x, {i, 1, 3}];
frPar$ = {vev -> 2 MW sw/e, lam -> MH^2 e^2/(8 MW^2 sw^2)};
common$ = {FCGV["EL"] -> e, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH,
   FCGV["ME"] -> mf[2, 1], FCGV["MM"] -> mf[2, 2], FCGV["ML"] -> mf[2, 3], FCGV["MU"] -> mf[3, 1], FCGV["MC"] -> mf[3, 2],
   FCGV["MT"] -> mf[3, 3], FCGV["MD"] -> mf[4, 1], FCGV["MS"] -> mf[4, 2], FCGV["MB"] -> mf[4, 3],
   FCGV["Ml"] -> ml, FCGV["Mu"] -> mu, FCGV["Md"] -> md, EL -> e, SMP["e"] -> e, SMP["sin_W"] -> sw, SMP["cos_W"] -> cw,
   SMP["m_W"] -> MW, SMP["m_Z"] -> MZ, SMP["m_H"] -> MH};
fixMass$ = {ml[{g_}] :> mf[2, g], mu[{g_, ___}] :> mf[3, g], md[{g_, ___}] :> mf[4, g], ml[g_Integer] :> mf[2, g],
   mu[g_Integer, ___] :> mf[3, g], md[g_Integer, ___] :> mf[4, g],
   Ml[g_Integer] :> mf[2, g], Mu[g_Integer, ___] :> mf[3, g], Md[g_Integer, ___] :> mf[4, g],
   FCGV["Ml"][g_] :> mf[2, g], FCGV["Mu"][g_, ___] :> mf[3, g], FCGV["Md"][g_, ___] :> mf[4, g]};
frMass$ = {Me -> mf[2, 1], MMU -> mf[2, 2], MTA -> mf[2, 3], MU -> mf[3, 1], MC -> mf[3, 2], MT -> mf[3, 3],
   MD -> mf[4, 1], MS -> mf[4, 2], MB -> mf[4, 3]};
realPar$ = Conjugate[x_] :> x;
chiral$ = {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
trEval$[x_] := Contract[x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
(* colour: |delta_{c c'}|^2 summed over both colours = Nc = 3 (FeynCalc 10 has no SUNFSimplify) *)
colour$[x_] := x /. {SUNFDelta[a_, b_]^2 :> 3, SUNFDelta[a_, b_] SUNFDelta[b_, a_] :> 3};
(* momentum conservation of the 1 -> n vertices: q = k1 + ... *)
momCons$[x_, n_] := Expand[ExpandScalarProduct[MomentumExpand[FCI[x]] /. Momentum[q, d___] :> Sum[Momentum[ToExpression["k" <> ToString[i]], d], {i, n}]]];
(* FeynArts 3.12 on Mathematica 14 prints harmless RuleDelayed::rhs messages when it initializes a model *)
ins$[model_, tops_, proc_, opts___] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> model,
   GenericModel -> If[model === "SM", "Lorentz", model], opts], RuleDelayed::rhs];
amp$[model_, diags_, in_, out_, lor_, opts___] := FCFAConvert[
     Quiet[CreateFeynAmp[diags, opts], RuleDelayed::rhs] /. If[model === "SM", {}, M$FACouplings] /. frRules$ //. frSum$ /. frPar$,
     IncomingMomenta -> in, OutgoingMomenta -> out, LorentzIndexNames -> lor, ChangeDimension -> 4, List -> False,
     SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True, TransversePolarizationVectors -> {}] /. common$ /. fixMass$ /.
   frMass$ /. realPar$;
nDiag$[diags_] := Length[Quiet[CreateFeynAmp[diags], RuleDelayed::rhs]];


(* ::Section:: *)
(*(a) Sign conventions: FeynRules model against SM.mod*)


(* ::Text:: *)
(*Each entry: label, fields in the FeynRules model, fields in SM.mod (W+ = V[3] and -V[3], G+ = S[3] and -S[3]),*)
(*expected ratio FR/SM.mod.  Three-point vertices as 1 -> 2, four-point vertices as 1 -> 3 with one vertex.*)


t12$ = CreateTopologies[0, 1 -> 2];
t13$ = CreateTopologies[0, 1 -> 3, Adjacencies -> {4}];
conv$ = {
   {"A -> e- e+", {V[1]} -> {F[2, {1}], -F[2, {1}]}, {V[1]} -> {F[2, {1}], -F[2, {1}]}, -1},
   {"A -> u ubar", {V[1]} -> {F[3, {1}], -F[3, {1}]}, {V[1]} -> {F[3, {1}], -F[3, {1}]}, -1},
   {"A -> d dbar", {V[1]} -> {F[4, {1}], -F[4, {1}]}, {V[1]} -> {F[4, {1}], -F[4, {1}]}, -1},
   {"Z -> nu nubar", {V[2]} -> {F[1, {1}], -F[1, {1}]}, {V[2]} -> {F[1, {1}], -F[1, {1}]}, 1},
   {"Z -> e- e+", {V[2]} -> {F[2, {1}], -F[2, {1}]}, {V[2]} -> {F[2, {1}], -F[2, {1}]}, 1},
   {"Z -> u ubar", {V[2]} -> {F[3, {1}], -F[3, {1}]}, {V[2]} -> {F[3, {1}], -F[3, {1}]}, 1},
   {"Z -> d dbar", {V[2]} -> {F[4, {1}], -F[4, {1}]}, {V[2]} -> {F[4, {1}], -F[4, {1}]}, 1},
   {"W+ -> e+ nu", {V[3]} -> {-F[2, {1}], F[1, {1}]}, {-V[3]} -> {-F[2, {1}], F[1, {1}]}, 1},
   {"W+ -> u dbar", {V[3]} -> {F[3, {1}], -F[4, {1}]}, {-V[3]} -> {F[3, {1}], -F[4, {1}]}, 1},
   {"H -> e- e+", {S[1]} -> {F[2, {1}], -F[2, {1}]}, {S[1]} -> {F[2, {1}], -F[2, {1}]}, 1},
   {"H -> u ubar", {S[1]} -> {F[3, {1}], -F[3, {1}]}, {S[1]} -> {F[3, {1}], -F[3, {1}]}, 1},
   {"H -> d dbar", {S[1]} -> {F[4, {1}], -F[4, {1}]}, {S[1]} -> {F[4, {1}], -F[4, {1}]}, 1},
   {"G0 -> e- e+", {S[2]} -> {F[2, {1}], -F[2, {1}]}, {S[2]} -> {F[2, {1}], -F[2, {1}]}, 1},
   {"G0 -> u ubar", {S[2]} -> {F[3, {1}], -F[3, {1}]}, {S[2]} -> {F[3, {1}], -F[3, {1}]}, 1},
   {"G+ -> e+ nu", {S[3]} -> {-F[2, {1}], F[1, {1}]}, {-S[3]} -> {-F[2, {1}], F[1, {1}]}, -I},
   {"G+ -> u dbar", {S[3]} -> {F[3, {1}], -F[4, {1}]}, {-S[3]} -> {F[3, {1}], -F[4, {1}]}, -I},
   {"A -> W+ W-", {V[1]} -> {V[3], -V[3]}, {V[1]} -> {-V[3], V[3]}, -1},
   {"Z -> W+ W-", {V[2]} -> {V[3], -V[3]}, {V[2]} -> {-V[3], V[3]}, 1},
   {"H -> W+ W-", {S[1]} -> {V[3], -V[3]}, {S[1]} -> {-V[3], V[3]}, 1},
   {"H -> Z Z", {S[1]} -> {V[2], V[2]}, {S[1]} -> {V[2], V[2]}, 1},
   {"H -> H H", {S[1]} -> {S[1], S[1]}, {S[1]} -> {S[1], S[1]}, 1},
   {"H -> G0 G0", {S[1]} -> {S[2], S[2]}, {S[1]} -> {S[2], S[2]}, 1},
   {"H -> G+ G-", {S[1]} -> {S[3], -S[3]}, {S[1]} -> {-S[3], S[3]}, 1},
   {"A -> G+ G-", {V[1]} -> {S[3], -S[3]}, {V[1]} -> {-S[3], S[3]}, -1},
   {"Z -> G+ G-", {V[2]} -> {S[3], -S[3]}, {V[2]} -> {-S[3], S[3]}, 1},
   {"Z -> G0 H", {V[2]} -> {S[2], S[1]}, {V[2]} -> {S[2], S[1]}, 1},
   {"W+ -> G+ H", {V[3]} -> {S[3], S[1]}, {-V[3]} -> {-S[3], S[1]}, I},
   {"W+ -> G+ G0", {V[3]} -> {S[3], S[2]}, {-V[3]} -> {-S[3], S[2]}, I},
   {"W+ -> G+ A", {V[3]} -> {S[3], V[1]}, {-V[3]} -> {-S[3], V[1]}, -I},
   {"W+ -> G+ Z", {V[3]} -> {S[3], V[2]}, {-V[3]} -> {-S[3], V[2]}, I},
   {"A -> W+ W- A", {V[1]} -> {V[3], -V[3], V[1]}, {V[1]} -> {-V[3], V[3], V[1]}, 1},
   {"A -> W+ W- Z", {V[1]} -> {V[3], -V[3], V[2]}, {V[1]} -> {-V[3], V[3], V[2]}, -1},
   {"Z -> W+ W- Z", {V[2]} -> {V[3], -V[3], V[2]}, {V[2]} -> {-V[3], V[3], V[2]}, 1},
   {"W+ -> W+ W+ W-", {V[3]} -> {V[3], V[3], -V[3]}, {-V[3]} -> {-V[3], -V[3], V[3]}, 1},
   {"H -> H W+ W-", {S[1]} -> {S[1], V[3], -V[3]}, {S[1]} -> {S[1], -V[3], V[3]}, 1},
   {"H -> H Z Z", {S[1]} -> {S[1], V[2], V[2]}, {S[1]} -> {S[1], V[2], V[2]}, 1},
   {"H -> H H H", {S[1]} -> {S[1], S[1], S[1]}, {S[1]} -> {S[1], S[1], S[1]}, 1},
   {"A -> A G+ G-", {V[1]} -> {V[1], S[3], -S[3]}, {V[1]} -> {V[1], -S[3], S[3]}, 1}};
convRes$ = Table[Module[{tops = If[Length[c[[2, 2]]] == 3, t13$, t12$], dFR, dSM, aFR, aSM, nout = Length[c[[2, 2]]], lor, d},
    lor = Take[{mu, nu, rho, si}, nout + 1];
    dFR = ins$[frModel$, tops, c[[2]]]; dSM = ins$["SM", tops, c[[3]]];
    aFR = amp$[frModel$, dFR, {q}, Take[{k1, k2, k3}, nout], lor, Truncated -> True];
    aSM = amp$["SM", dSM, {q}, Take[{k1, k2, k3}, nout], lor, Truncated -> True, GaugeRules -> {_GaugeXi -> 1}];
    d = Simplify[Expand[FCE[momCons$[DiracSimplify[aFR - c[[4]] aSM], nout] /. chiral$] /. cw -> Sqrt[1 - sw^2] /. MZ -> MW/Sqrt[1 - sw^2]]];
    {c[[1]], nDiag$[dFR], nDiag$[dSM], c[[4]], d, aFR =!= 0}], {c, conv$}];
Print["(a) FR/SM.mod vertex classes compared: ", Length[convRes$], ";  nonzero FR - ratio x SM.mod (expect none): ",
  Select[convRes$, #[[5]] =!= 0 &]];
Print["(a) classes with the photon-sign rule -1: ", Count[convRes$, {_, _, _, -1, 0, True}], ", with +1: ",
  Count[convRes$, {_, _, _, 1, 0, True}], ", with the G+ phase -+i: ", Count[convRes$, {_, _, _, I | -I, 0, True}],
  ";  all amplitudes nonzero: ", And @@ convRes$[[All, 6]]];


(* ::Subsubsection:: *)
(*Inspect: the table (label, FR diagrams, SM.mod diagrams, expected ratio, difference)*)


If[$Notebooks, TableForm[convRes$[[All, 1 ;; 5]]]]


(* ::Section:: *)
(*(b) Muon decay*)


diagsMu$ = ins$[frModel$, CreateTopologies[0, 1 -> 3], {F[2, {2}]} -> {F[1, {2}], F[2, {1}], -F[1, {1}]}, ExcludeParticles -> {S[_]}];
ampMu$ = amp$[frModel$, diagsMu$, {p}, {k1, k2, k3}, {}] /. mf[2, 1] -> 0 /. mf[2, 2] -> mmu;
Print["(b) muon decay: diagrams (expect 1, W exchange; G+- exchange is excluded, it is proportional to m_e = 0): ", nDiag$[diagsMu$]];
(* independent invariants a = k1.k2, b = k1.k3, c = k2.k3 (massless final state), p = k1 + k2 + k3, m_mu^2 = 2(a+b+c) *)
FCClearScalarProducts[];
ScalarProduct[k1, k1] = 0; ScalarProduct[k2, k2] = 0; ScalarProduct[k3, k3] = 0;
ScalarProduct[k1, k2] = a; ScalarProduct[k1, k3] = b; ScalarProduct[k2, k3] = c;
ScalarProduct[p, k1] = a + b; ScalarProduct[p, k2] = a + c; ScalarProduct[p, k3] = b + c; ScalarProduct[p, p] = 2 (a + b + c);
sqMu$ = Simplify[FeynAmpDenominatorExplicit[DiracSimplify[trEval$[FermionSpinSum[ComplexConjugate[ampMu$] ampMu$]]]] /.
    mmu -> Sqrt[2 (a + b + c)]];
dMu$ = Simplify[sqMu$ (2 c - MW^2)^2 - 4 e^4/sw^4 (b + c) a];
Print["(b) sum|M|^2 (q^2 - M_W^2)^2 - 4 e^4 (p.k3)(k1.k2)/s_W^4 with q^2 = 2 k2.k3 (expect 0): ", dMu$];
Print["(b) Fermi limit: 4 e^4/(s_W^4 M_W^4) / (128 G_F^2) with G_F/sqrt2 = e^2/(8 s_W^2 M_W^2) (expect 1): ",
  Simplify[4 e^4/(sw^4 MW^4)/(128 (Sqrt[2] e^2/(8 sw^2 MW^2))^2)]];


(* ::Section:: *)
(*(c) Two-body widths*)


(* Gamma = |p|/(8 pi M^2) <sum|M|^2>, averaged over the initial polarizations (vector: 3, fermion: 2) *)
pcm$[M_, m1_, m2_] := Sqrt[(M^2 - (m1 + m2)^2) (M^2 - (m1 - m2)^2)]/(2 M);
width$[model_, proc_, M_, m1_, m2_, kind_, colour_] := Module[{d, a, sq},
   d = ins$[model, t12$, proc];
   a = amp$[model, d, {q}, {k1, k2}, {}];
   FCClearScalarProducts[];
   ScalarProduct[q, q] = M^2; ScalarProduct[k1, k1] = m1^2; ScalarProduct[k2, k2] = m2^2;
   ScalarProduct[k1, k2] = (M^2 - m1^2 - m2^2)/2; ScalarProduct[q, k1] = (M^2 + m1^2 - m2^2)/2; ScalarProduct[q, k2] = (M^2 - m1^2 + m2^2)/2;
   sq = FermionSpinSum[ComplexConjugate[a] a];
   (* "V": decaying vector (average over 3 polarizations); "S": scalar; "F": decaying fermion (average over 2 spins)
      to a fermion (k1) and a vector (k2), summed over the vector's polarizations *)
   sq = Which[kind === "V", DoPolarizationSums[sq, q]/3, kind === "S", sq, kind === "F", DoPolarizationSums[sq, k2]/2];
   sq = Simplify[colour$[trEval$[DiracSimplify[sq]]]];
   colour pcm$[M, m1, m2]/(8 Pi M^2) sq];
gV$[Q_, T3_] := (T3 - 2 Q sw^2)/(2 sw cw); gA$[T3_] := T3/(2 sw cw);
zNote$[Q_, T3_, Nc_, m_] := Nc e^2/(4 Pi) MZ/3 Sqrt[1 - 4 m^2/MZ^2] (gV$[Q, T3]^2 (1 + 2 m^2/MZ^2) + gA$[T3]^2 (1 - 4 m^2/MZ^2));
cmp$[x_, y_] := Simplify[(x - y) /. cw -> MW/MZ /. sw -> Sqrt[1 - MW^2/MZ^2], MZ > MW > 0 && MZ > 2 m > 0 && MW > ml > 0];
Print["(c) Z -> nu nubar, e- e+, u ubar, d dbar minus Eq. (9) with masses (expect 0, 0, 0, 0): ",
  {cmp$[width$[frModel$, {V[2]} -> {F[1, {1}], -F[1, {1}]}, MZ, 0, 0, "V", 1], zNote$[0, 1/2, 1, 0]],
   cmp$[width$[frModel$, {V[2]} -> {F[2, {1}], -F[2, {1}]}, MZ, m, m, "V", 1] /. mf[2, 1] -> m, zNote$[-1, -1/2, 1, m]],
   cmp$[width$[frModel$, {V[2]} -> {F[3, {1}], -F[3, {1}]}, MZ, m, m, "V", 1] /. mf[3, 1] -> m, zNote$[2/3, 1/2, 3, m]],
   cmp$[width$[frModel$, {V[2]} -> {F[4, {1}], -F[4, {1}]}, MZ, m, m, "V", 1] /. mf[4, 1] -> m, zNote$[-1/3, -1/2, 3, m]]}];
wNote$ = e^2/(4 Pi) MW/(12 sw^2) (1 - ml^2/MW^2)^2 (1 + ml^2/(2 MW^2));
Print["(c) W+ -> l+ nu minus alpha MW/(12 s^2) (1 - x)^2 (1 + x/2), x = m_l^2/MW^2 (expect 0): ",
  cmp$[width$[frModel$, {V[3]} -> {-F[2, {1}], F[1, {1}]}, MW, ml, 0, "V", 1] /. mf[2, 1] -> ml, wNote$]];
hNote$[Nc_] := Nc e^2/(4 Pi) MH m^2/(8 sw^2 MW^2) (1 - 4 m^2/MH^2)^(3/2);
Print["(c) H -> l l, u u, d d minus Eq. (10) (expect 0, 0, 0): ",
  Simplify[#, MH > 2 m > 0] & /@ {
   cmp$[width$[frModel$, {S[1]} -> {F[2, {1}], -F[2, {1}]}, MH, m, m, "S", 1] /. mf[2, 1] -> m, hNote$[1]],
   cmp$[width$[frModel$, {S[1]} -> {F[3, {1}], -F[3, {1}]}, MH, m, m, "S", 1] /. mf[3, 1] -> m, hNote$[3]],
   cmp$[width$[frModel$, {S[1]} -> {F[4, {1}], -F[4, {1}]}, MH, m, m, "S", 1] /. mf[4, 1] -> m, hNote$[3]]}];
tNote$ = Module[{rb = mb^2/mt^2, rw = MW^2/mt^2},
   (Pi e^2/(4 Pi)/(Sqrt[2] sw^2 MW^2)) mt^3/(8 Sqrt[2] Pi) Sqrt[(1 - rb - rw)^2 - 4 rb rw] ((1 - rb)^2 + rw (1 + rb) - 2 rw^2)];
(* the top colour is averaged: 1/Nc *)
tFC$ = width$[frModel$, {F[3, {3}]} -> {F[4, {3}], V[3]}, mt, mb, MW, "F", 1/3] /. mf[3, 3] -> mt /. mf[4, 3] -> mb;
Print["(c) t -> b W+ (m_b kept) minus G_F m_t^3/(8 sqrt2 pi) lambda^(1/2) [(1-rb)^2 + rw(1+rb) - 2 rw^2] (expect 0): ",
  Simplify[(tFC$ - tNote$) /. cw -> MW/MZ /. sw -> Sqrt[1 - MW^2/MZ^2], mt > mb + MW && mb > 0 && MW > 0 && MZ > MW]];


(* ::Section:: *)
(*(d) e+ e- -> mu+ mu-*)


diagsEE$ = ins$[frModel$, CreateTopologies[0, 2 -> 2], {F[2, {1}], -F[2, {1}]} -> {F[2, {2}], -F[2, {2}]}, ExcludeParticles -> {S[_]}];
ampEE$ = amp$[frModel$, diagsEE$, {p1, p2}, {k1, k2}, {}] /. mf[2, _] -> 0;
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, 0, 0];
sqEE$ = Simplify[FeynAmpDenominatorExplicit[DiracSimplify[trEval$[FermionSpinSum[ComplexConjugate[ampEE$] ampEE$]]]]];
gLR$[Q_, T3_] := {(T3 - Q sw^2)/(sw cw), -Q sw/cw};
chi$ = s/(s - MZ^2);
A$[i_, j_] := (-1) (-1) + gLR$[-1, -1/2][[i]] gLR$[-1, -1/2][[j]] chi$;
eeNote$ = 4 e^4 ((A$[1, 1]^2 + A$[2, 2]^2) u^2 + (A$[1, 2]^2 + A$[2, 1]^2) t^2)/s^2;
Print["(d) e+e- -> mu+mu- (gamma, Z; Gamma_Z = 0): diagrams ", nDiag$[diagsEE$],
  ";  sum|M|^2 - 4 e^4 [sum|A_ii|^2 u^2 + sum|A_ij|^2 t^2]/s^2 from Eq. (11) (expect 0): ",
  Simplify[(sqEE$ - eeNote$) /. u -> -s - t /. cw -> Sqrt[1 - sw^2]]];


(* ::Section:: *)
(*(e) e+ e- -> W+ W-: sum over spins and polarizations at six points*)


diagsWW$ = ins$[frModel$, CreateTopologies[0, 2 -> 2], {F[2, {1}], -F[2, {1}]} -> {-V[3], V[3]}, ExcludeParticles -> {S[_]}];
ampWW$ = amp$[frModel$, diagsWW$, {p1, p2}, {k1, k2}, {mu, nu}] /. mf[2, _] -> 0;
Print["(e) e+e- -> W- W+: diagrams (expect 3: t-channel nu, s-channel photon and Z): ", nDiag$[diagsWW$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, MW, MW];
sqWW$ = trEval$[FermionSpinSum[ComplexConjugate[ampWW$] ampWW$]];
sqWW$ = DoPolarizationSums[DoPolarizationSums[sqWW$, k1], k2];
sqWW$ = Simplify[FeynAmpDenominatorExplicit[trEval$[DiracSimplify[Contract[sqWW$]]]] /. u -> 2 MW^2 - s - t];
(* parameters of the UFO card and the six points (sqrt s, cos theta) *)
parWW$ = Module[{aew = 1/127.9, gf = 1.16637*^-5, mz = 91.1876, mw},
   mw = Sqrt[mz^2/2 + Sqrt[mz^4/4 - Pi/Sqrt[2] aew/gf mz^2]];
   {e -> Sqrt[4 Pi aew], MZ -> mz, MW -> mw, sw -> Sqrt[1 - mw^2/mz^2], cw -> mw/mz}];
ptsWW$ = Flatten[Table[{rs, c}, {rs, {200., 500., 1000.}}, {c, {-0.5, 0.3}}], 1];
valsWW$ = Table[Module[{mw = MW /. parWW$, ss = pt[[1]]^2, beta},
     beta = Sqrt[1 - 4 mw^2/ss];
     {pt[[1]], pt[[2]], sqWW$ /. s -> ss /. t -> mw^2 - ss/2 (1 - beta pt[[2]]) /. parWW$}], {pt, ptsWW$}];
Quiet[CreateDirectory[FileNameJoin[{srcDirTr$, "results"}]]];
Export[FileNameJoin[{srcDirTr$, "results", "tree_feyncalc_ww.csv"}],
  StringRiffle[Prepend[Map[ToString[CForm[#]] &, valsWW$, {2}], {"sqrt_s", "cos_theta", "sum_M2"}], "\n", ","] <> "\n", "Text"];
Print["(e) sum|M|^2 at (sqrt s, cos theta) = ", InputForm[valsWW$], "  -> results/tree_feyncalc_ww.csv"];

DeleteDirectory[modelTmpDirTr$, DeleteContents -> True];
