(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the NLO note: the effective couplings of the Z and sin^2 theta_eff (MS-bar couplings, FJ tadpoles, general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (5).  The renormalized weak form factors FL, FR of Z -> f fbar of zweak.wl (step (4a): the*)
(*bare vertex with the on-shell LSZ factors, the Z-photon mixing and the MS-bar counterterms, the photon and the gluon left out),*)
(*in units of g_Z/2 the effective couplings of Eq. (effcoup),*)
(*  V_f = FL + FR,  A_f = FL - FR  (tree: T3 - 2 Q s^2, T3),   sin^2 theta_eff^f = (1 - Re V_f/A_f)/(4 |Q_f|) = kappa_f(mu) s^2(mu),*)
(*the ratio taken at O(alpha) (linear in the one-loop parts; the full ratio is shown for the size of O(alpha^2)).  The residue of*)
(*the Z (dZ_ZZ/2, common to FL and FR) drops out of the ratio; the photonic and gluonic final-state corrections multiply V and A*)
(*alike for massless f and are left out, as in the LEP definition of the effective couplings (the H_L, H_R terms are O(m_f) and*)
(*are not part of it).  (a) gauge independence: (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4);  (b) mu = M_Z/2, M_Z, 2 M_Z: sin^2 theta_eff*)
(*must not depend on mu at O(alpha), while s^2(mu) and kappa(mu) do;  (c) the parts of sin^2 theta_eff - s^2 from the Z-photon*)
(*mixing, the 1PI vertex and the fermion legs at mu = M_Z (the MS-bar counterterms are pure poles);  (d) the same with the couplings*)
(*of the SM note's alpha scheme (nlo_inputs.at(mu, "PDG2024_alpha_scheme")).  Writes results/zeff.csv, zeff_parts.csv, zeff_alpha.csv.*)
(*Batch:  wolframscript -file zeff.wl  (after zff_feyncalc.wl for the eleven fermions, run_zweak_check.sh)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirZE$ = DirectoryName[$InputFileName];
workDirZW$ = FileNameJoin[{srcDirZE$, "work"}];
resDirZW$ = FileNameJoin[{srcDirZE$, "results"}];
t0ZW$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0ZW$], " s] ", s];
KK = 16 Pi^2;
chansZW$ = {{1, 1}, {1, 2}, {1, 3}, {2, 1}, {2, 2}, {2, 3}, {3, 1}, {3, 2}, {4, 1}, {4, 2}, {4, 3}};
(* the colour delta of the quark tree (SDF) cancels in the ratio vertex/tree: set to 1 *)
zffZW$ = Association[(# -> (Get[FileNameJoin[{workDirZW$, "zff_" <> ToString[#[[1]]] <> ToString[#[[2]]] <> ".m"}]] /.
       {SDF[__] -> 1, SUNFDelta[__] -> 1})) & /@ chansZW$];
smSigZW$ = Association[Get[FileNameJoin[{srcDirZE$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleZW$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
sigZZ$ = Total[smSigZW$["ZZ"]] /. kRuleZW$;    (* 1PI + tadpole (constant in kk2) *)
sigAZ$ = Total[smSigZW$["AZ"]] /. kRuleZW$;

(* ::Section:: *)
(*The photon tree amplitude of the mixing, in the units of the Z tree*)

modelTmpZW$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirZE$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpZW$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpZW$, "SM_CKM_FA"}], Quiet -> True];
modelZW$ = FileNameJoin[{modelTmpZW$, "SM_CKM_FA", "SM_CKM_FA"}];
treeCoefZW$[vb_, t_, g_, m_] := Module[{d, a, sp1 = Spinor[Momentum[p1], m, 1], sp2 = Spinor[-Momentum[p2], m, 1], x},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> 2], {vb} -> {F[t, {g}], -F[t, {g}]}, InsertionLevel -> {Particles},
       Model -> modelZW$, GenericModel -> modelZW$], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d] /. M$FACouplings, IncomingMomenta -> {k}, OutgoingMomenta -> {p1, p2}, ChangeDimension -> 4,
       List -> True, SMP -> False, UndoChiralSplittings -> True], RuleDelayed::rhs] /. {FCGV["EL"] -> ee} /.
     FCGV[x_String] :> ToExpression[x] /. SumOver[__] -> 1 /. Polarization[k, I] -> epsV;
   x = Expand[FCE[DiracSimplify[Contract[Total[a /. SUNFDelta[__] -> 1]]]] /. SDF[__] -> 1 /. {sp1 . GS[epsV] . GA[7] . sp2 -> sEL$, sp1 . GS[epsV] . GA[6] . sp2 -> sER$,
        sp1 . GS[epsV] . sp2 -> sEL$ + sER$}];
   {Coefficient[x, sEL$], Coefficient[x, sER$]}];
photonZW$ = Association[Table[ch -> Module[{t = ch[[1]], g = ch[[2]], m = zffZW$[ch]["mass"], tz, ta, tau},
      If[t == 1, {0, 0},
       tz = treeCoefZW$[V[2], t, g, m]; ta = treeCoefZW$[V[1], t, g, m];
       tau = tz[[1]]/(zffZW$[ch]["T3"] - zffZW$[ch]["Q"] sw^2);
       Simplify[ta/tau /. cw -> Sqrt[1 - sw^2], 0 < sw < 1]]], {ch, chansZW$}]];
DeleteDirectory[modelTmpZW$, DeleteContents -> True];
Print["photon tree {FL, FR} in units of the Z tree (expect +-Q sw cw (1, 1)): ",
  Table[zffZW$[ch]["name"] -> photonZW$[ch], {ch, chansZW$}]];
tick$["photon tree"];

(* ::Section:: *)
(*The renormalized form factors*)

gLR$[t3_, q_] := {(g^2 t3 - gp^2 (q - t3))/Sqrt[g^2 + gp^2], -gp^2 q/Sqrt[g^2 + gp^2]};
(* K dF(MS-bar) in units of g_Z, 1/ep the UV pole *)
kdFms$[t3_, q_] := Module[{gl = gLR$[t3, q], d},
   d = (D[#, g] g (-19/12) g^2 + D[#, gp] gp (41/12) gp^2) & /@ gl;
   Simplify[d/Sqrt[g^2 + gp^2] /. {g -> ee/sw, gp -> ee/cw} /. cw -> Sqrt[1 - sw^2], 0 < sw < 1]/ep];
dZfZW$[se_, m_] := Module[{sl, sr, ss},
   {sl, sr, ss} = (se[[{1, 2, 3}]] /. {SPD[p, p] -> pp2, Pair[Momentum[p, D], Momentum[p, D]] -> pp2, SPD[p] -> pp2});
   If[m === 0, {-sl, -sr} /. pp2 -> 0,
    {-sl - m^2 D[sl + sr + 2 ss, pp2], -sr - m^2 D[sl + sr + 2 ss, pp2]} /. pp2 -> m^2]];
piecesZW$ = Association[Table[ch -> Module[{z = zffZW$[ch], f0, dzf, dzz, mix},
      f0 = {z["T3"] - z["Q"] sw^2, -z["Q"] sw^2};
      dzf = dZfZW$[z["SE"], z["mass"]];
      dzz = -D[sigZZ$, kk2] /. kk2 -> MZ^2;
      mix = -(sigAZ$ /. kk2 -> MZ^2)/MZ^2;
      <|"vertex" -> z["F"], "f legs" -> Join[f0 dzf, {0, 0}], "Z leg" -> Join[f0 dzz/2, {0, 0}],
       "mixing" -> Join[mix photonZW$[ch], {0, 0}], "MS-bar" -> Join[kdFms$[z["T3"], z["Q"]], {0, 0}]|>], {ch, chansZW$}]];
totalZW$[ch_] := Total[Values[piecesZW$[ch]]];
(* for the numbers: the fermion legs with p^2 = pp2 kept, the limit pp2 -> m^2 taken after Package-X (0/0 at m = 0) *)
dZfSymZW$[se_, m_] := Module[{sl, sr, ss},
   {sl, sr, ss} = (se[[{1, 2, 3}]] /. {SPD[p, p] -> pp2, Pair[Momentum[p, D], Momentum[p, D]] -> pp2, SPD[p] -> pp2});
   {-sl - m^2 D[sl + sr + 2 ss, pp2], -sr - m^2 D[sl + sr + 2 ss, pp2]}];
totalNumZW$[ch_] := Module[{z = zffZW$[ch], f0},
   f0 = {z["T3"] - z["Q"] sw^2, -z["Q"] sw^2};
   Total[Values[KeyDrop[piecesZW$[ch], "f legs"]]] + Join[f0 dZfSymZW$[z["SE"], z["mass"]], {0, 0}]];
tick$["pieces"];

(* ::Section:: *)
(*Inputs and loop functions (as zweak.wl)*)

(* the inputs: MS-bar at mu from nlo_inputs.py, pole masses; exact rationals for Package-X *)
inputsZW$[mu_, case_: "PDG2024_MW_scheme"] := Module[{out = RunProcess[{"python3", "-c",
       "import sys; sys.path.insert(0, '" <> srcDirZE$ <> "'); from nlo_inputs import at, POLE; p = at(" <> ToString[CForm[N[mu, 17]]] <>
        ", '" <> case <> "'); V = p['V']; print(' '.join('%.17e' % float(x) for x in [p['s2'], p['e']] + list(V.real.ravel()) + list(V.imag.ravel())))"},
      ProcessDirectory -> srcDirZE$]["StandardOutput"], nums},
   nums = ToExpression[StringReplace[#, "e" -> "*^"]] & /@ StringSplit[out];
   <|"s2" -> nums[[1]], "e" -> nums[[2]], "V" -> Partition[nums[[3 ;; 11]], 3] + I Partition[nums[[12 ;; 20]], 3]|>];
(* u, d, s: massless in the note (POLE of nlo_inputs.py); here 0.1 MeV, because the light-quark mass symbols sit in denominators of
   the stored self-energy pieces (0/0 at m = 0); the change of delta_weak is of order m^2/M_Z^2 ~ 1e-12 *)
poleMassesZW$ = {MZ -> 911876/10000, MH -> 12520/100, MT -> 17257/100, MB -> 478/100, MC -> 167/100, MS -> 1/10000, MD -> 1/10000, MU -> 1/10000,
   MTA -> 177693/100000, MMU -> 1056584/10000000, Me -> 510999/1000000000};
(* the loop functions with Package-X: {1/eps coefficient, MS-bar finite part} for exact numerical arguments *)
pxCache$ = <||>;
pxVal$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity};
   pxCache$[key] = If[FreeQ[y, pp2], N[y, 60], y]];
(* d/dp^2 B0(p^2, a, b) at p^2 = s: the Package-X form in a symbol, differentiated *)
pxDB0$[s_, a_, b_, mu_] := Module[{key = {"DB0", s, a, b, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[B0[xx$, a, b]] /. ConditionalExpression[a1_, _] :> a1;
   y = Normal[Series[D[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, xx$] /. xx$ -> s, {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity};
   pxCache$[key] = If[FreeQ[y, pp2], N[y, 60], y]];
(* an expression in A0, B0, B0', C0 and D: its 1/eps and MS-bar parts *)
numericZW$[x_, mu_, m2_] := Module[{fs, vals, y, sym},
   fs = Union[Cases[x, A0[__] | B0[__] | C0[__] | DB0[__] | Derivative[1, 0, 0][B0][__], Infinity]];
   vals = Function[f, Module[{v = If[MatchQ[f, DB0[__] | Derivative[1, 0, 0][B0][__]], pxDB0$[Sequence @@ f, mu], pxVal$[f, mu]]},
        v[[1]]/ep + v[[2]]]] /@ fs;
   y = x /. Thread[fs -> vals] /. D -> 4 - 2 ep;
   y = Expand[Normal[Series[y, {ep, 0, 0}]]];
   y = {Coefficient[y, ep, -1], Coefficient[y, ep, 0]};
   If[FreeQ[y, pp2], N[y, 50], N[Normal[Series[#, {pp2, m2, 0}]] & /@ y, 50]]];

(* ::Section:: *)
(*The effective couplings*)

(* {Re V/A at O(alpha), Re V/A of the full ratio, the one-loop {FL, FR} (finite, MS-bar), the largest UV pole left} *)
effZE$[ch_, mu_, xis_, inp_, keys_: All, masses_: poleMassesZW$] := Module[{z = zffZW$[ch], s2 = Rationalize[inp["s2"], 10^-14], e2, rules,
    f1, f0, pole, fin, m, mz = MZ /. masses, v0, a0, v1, a1, pcs},
   e2 = Rationalize[inp["e"]^2, 10^-14];
   m = z["mass"] /. masses;
   rules = Join[{sw -> Sqrt[s2], cw -> Sqrt[1 - s2], ee -> Sqrt[e2]}, xis, masses, {MW -> Sqrt[mz^2 (1 - s2)]},
     {cK[i_, j_] :> inp["V"][[i, j]], cKc[i_, j_] :> Conjugate[inp["V"][[i, j]]]}];
   f0 = {z["T3"] - z["Q"] s2, -z["Q"] s2};
   pcs = Append[KeyDrop[piecesZW$[ch], "f legs"], "f legs" -> Join[{z["T3"] - z["Q"] sw^2, -z["Q"] sw^2} dZfSymZW$[z["SE"], z["mass"]], {0, 0}]];
   f1 = If[keys === All, Total[Values[pcs]], Total[Values[KeyTake[pcs, keys]]]][[1 ;; 2]] /. rules;
   If[m =!= 0, f1 = f1 /. pp2 -> m^2];
   {pole, fin} = Transpose[numericZW$[#, mu, m^2] & /@ f1];
   fin = fin/KK;
   {v0, a0} = {f0[[1]] + f0[[2]], f0[[1]] - f0[[2]]}; {v1, a1} = {fin[[1]] + fin[[2]], fin[[1]] - fin[[2]]};
   {v0/a0 + Re[v1 a0 - v0 a1]/a0^2, Re[(v0 + v1)/(a0 + a1)], fin, Max[Abs[pole]]}];
s2effZE$[ch_, x_] := (1 - x)/(4 Abs[zffZW$[ch]["Q"]]);
chargedZE$ = Select[chansZW$, zffZW$[#]["Q"] != 0 &];
xiSetsZE$ = {{xiZ -> 1, xiW -> 1}, {xiZ -> 2, xiW -> 3}, {xiZ -> 1/2, xiW -> 4}};
rowsZE$ = {};

(* (a) gauge independence at mu = M_Z *)
inpMZ$ = inputsZW$[911876/10000];
Do[Module[{r = effZE$[ch, 911876/10000, #, inpMZ$] & /@ xiSetsZE$, s2e},
   s2e = s2effZE$[ch, #] & /@ r[[All, 1]];
   Print["(a) ", zffZW$[ch]["name"], ": sin^2 theta_eff at (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4): ", NumberForm[#, 12] & /@ s2e,
    ";  spread ", ScientificForm[N[Max[s2e] - Min[s2e]], 2], ";  UV pole left ", ScientificForm[N[Max[r[[All, 4]]]], 2],
    ";  full ratio minus O(alpha): ", ScientificForm[N[s2effZE$[ch, r[[1, 2]]] - s2e[[1]]], 2]];
   AppendTo[rowsZE$, {zffZW$[ch]["name"], N[911876/10000], ToString[CForm[N[inpMZ$["s2"], 17]]], ToString[CForm[N[s2e[[1]], 17]]],
     ToString[CForm[N[s2effZE$[ch, r[[1, 2]]], 17]]], ToString[CForm[N[Max[s2e] - Min[s2e], 3]]]}]], {ch, chargedZE$}];
tick$["(a)"];

(* (b) mu = M_Z/2, 2 M_Z *)
Do[Module[{inp = inputsZW$[mu]},
   Do[Module[{r = effZE$[ch, mu, xiSetsZE$[[1]], inp]},
      AppendTo[rowsZE$, {zffZW$[ch]["name"], N[mu], ToString[CForm[N[inp["s2"], 17]]], ToString[CForm[N[s2effZE$[ch, r[[1]]], 17]]],
        ToString[CForm[N[s2effZE$[ch, r[[2]]], 17]]], ""}]], {ch, chargedZE$}]], {mu, {911876/20000, 911876/5000}}];
Do[Module[{rs = Select[rowsZE$, #[[1]] == zffZW$[ch]["name"] &]},
   Print["(b) ", zffZW$[ch]["name"], ": mu = ", rs[[All, 2]], ";  s^2(mu) ", NumberForm[ToExpression[#], 8] & /@ rs[[All, 3]],
    ";  sin^2 theta_eff ", NumberForm[ToExpression[#], 8] & /@ rs[[All, 4]]]], {ch, chargedZE$}];
tick$["(b)"];
Export[FileNameJoin[{resDirZW$, "zeff.csv"}], Prepend[rowsZE$, {"fermion", "mu", "s2_msbar", "s2eff", "s2eff_full_ratio", "xi_spread"}], "CSV"];

(* (c) the parts at mu = M_Z: Delta sin^2 = -(Re V/A of the part - v0/a0)/(4 |Q|) *)
partsZE$ = {"mixing", "vertex", "f legs", "Z leg", "MS-bar"};
partRowsZE$ = {};
Do[Module[{z = zffZW$[ch], s2 = inpMZ$["s2"], x0, d},
   x0 = (z["T3"] - 2 z["Q"] s2)/z["T3"];
   d = Table[-(effZE$[ch, 911876/10000, xiSetsZE$[[1]], inpMZ$, {p}][[1]] - x0)/(4 Abs[z["Q"]]), {p, partsZE$}];
   Print["(c) ", z["name"], ": sin^2 theta_eff - s^2(M_Z) from ", Thread[partsZE$ -> (NumberForm[N[#], 6] & /@ d)], ";  sum ", NumberForm[N[Total[d]], 8]];
   AppendTo[partRowsZE$, Prepend[ToString[CForm[N[#, 12]]] & /@ d, z["name"]]]], {ch, chargedZE$}];
Export[FileNameJoin[{resDirZW$, "zeff_parts.csv"}], Prepend[partRowsZE$, Prepend[partsZE$, "fermion"]], "CSV"];
tick$["(c); written results/zeff.csv, results/zeff_parts.csv"];

(* (d) the inputs of the SM note's alpha scheme (alpha(0), G_F, M_Z in place of M_W; its M_W is a prediction): the same one-loop
   sin^2 theta_eff from a different one-loop determination of g, g' -- the difference is of higher order *)
alphaRowsZE$ = {};
Do[Module[{inp = inputsZW$[mu, "PDG2024_alpha_scheme"]},
   Do[Module[{r = effZE$[ch, mu, xiSetsZE$[[1]], inp]},
      AppendTo[alphaRowsZE$, {zffZW$[ch]["name"], N[mu], ToString[CForm[N[inp["s2"], 17]]], ToString[CForm[N[s2effZE$[ch, r[[1]]], 17]]],
        ToString[CForm[N[s2effZE$[ch, r[[2]]], 17]]], ""}]], {ch, chargedZE$}]], {mu, {911876/10000, 911876/20000, 911876/5000}}];
Print["(d) alpha scheme, mu = M_Z: s^2 ", alphaRowsZE$[[1, 3]], ";  sin^2 theta_eff ", Thread[alphaRowsZE$[[1 ;; Length[chargedZE$], 1]] ->
    (NumberForm[ToExpression[#], 8] & /@ alphaRowsZE$[[1 ;; Length[chargedZE$], 4]])]];
Export[FileNameJoin[{resDirZW$, "zeff_alpha.csv"}], Prepend[alphaRowsZE$, {"fermion", "mu", "s2_msbar", "s2eff", "s2eff_full_ratio", "xi_spread"}], "CSV"];
tick$["(d); written results/zeff_alpha.csv"];
