(* ::Package:: *)

(* ::Title:: *)
(*Step (4a) of the NLO note: the weak correction to Z -> f fbar (MS-bar couplings, FJ tadpoles, general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4a).  Reads work/zff_<t><g>.m (zff_feyncalc.wl: the weak 1PI vertex {K FL, K FR, K HL, K HR} in*)
(*units of g_Z = e/(sw cw) and the weak self-energy {K SL, K SR, K SSL, K SSR} of f) and the SM note's Sigma^ZZ, Sigma^AZ*)
(*(models/sm/Src/results/oneloop_sigma.m; general R_xi, all fermion masses; they do not depend on V at one loop).  The*)
(*S-matrix element is the bare amputated vertex times the on-shell LSZ factors, with the bare couplings g0 = g + dg:*)
(*  FL = FL0 + FL_vertex + FL0 [dZ_ZZ/2 + dZ^L_f] - (Sigma^AZ_T(MZ^2)/MZ^2) FL^gamma + dFL(MS-bar),  and FR with R,*)
(*  dZ_ZZ = -Sigma^ZZ_T'(MZ^2),  dZ^L = -SL - m^2 (SL' + SR' + 2 SSL') at p^2 = m^2 (Denner's on-shell form, the CKM note's*)
(*  wud_renormalized.wl), both legs together;  FL^gamma: the photon tree amplitude Z -> gamma* -> f fbar of the mixing in the*)
(*  same units (FeynArts, with its sign);  dFL: g_L = (g^2 T3 - g'^2 (Q - T3))/sqrt(g^2 + g'^2), g_R = -g'^2 Q/sqrt(g^2 + g'^2) with*)
(*  K dg/g = (Delta/2)(-19/6) g^2, K dg'/g' = (Delta/2)(41/6) g'^2.  The tadpoles (FJ) only shift masses here.*)
(*  (a) UV finiteness of FL, FR for the eleven fermions (symbolic masses and gauge parameters, the explicit rational unitary V*)
(*      of the CKM note);*)
(*  (b) delta_weak = 2 Re(M0^* M1)/|M0|^2 (the sums over spins and Z polarizations in 4 dimensions) with the loop functions of*)
(*      Package-X (FeynHelpers; MS-bar: ScaleMu^2 = pi e^gamma_E mu^2, the 1/eps dropped) at the note's MS-bar couplings at*)
(*      mu = M_Z and the pole masses (in the loops M_W = M_Z c-hat, the tree relations), for (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4);*)
(*  (c) mu = M_Z/2, 2 M_Z with the couplings run to mu: Gamma_0 (1 + delta_weak) against Gamma_0 alone.*)
(*Writes results/zweak.csv.  Batch:  wolframscript -file zweak.wl  (after zff_feyncalc.wl for the eleven fermions)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirZW$ = DirectoryName[$InputFileName];
workDirZW$ = FileNameJoin[{srcDirZW$, "work"}];
resDirZW$ = FileNameJoin[{srcDirZW$, "results"}];
t0ZW$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0ZW$], " s] ", s];
KK = 16 Pi^2;
chansZW$ = {{1, 1}, {1, 2}, {1, 3}, {2, 1}, {2, 2}, {2, 3}, {3, 1}, {3, 2}, {4, 1}, {4, 2}, {4, 3}};
(* the colour delta of the quark tree (SDF) cancels in the ratio vertex/tree: set to 1 *)
zffZW$ = Association[(# -> (Get[FileNameJoin[{workDirZW$, "zff_" <> ToString[#[[1]]] <> ToString[#[[2]]] <> ".m"}]] /.
       {SDF[__] -> 1, SUNFDelta[__] -> 1})) & /@ chansZW$];
smSigZW$ = Association[Get[FileNameJoin[{srcDirZW$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleZW$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
sigZZ$ = Total[smSigZW$["ZZ"]] /. kRuleZW$;    (* 1PI + tadpole (constant in kk2) *)
sigAZ$ = Total[smSigZW$["AZ"]] /. kRuleZW$;

(* ::Section:: *)
(*The photon tree amplitude of the mixing, in the units of the Z tree*)

modelTmpZW$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirZW$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpZW$, "SM_CKM_FA"}]];
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
(*(a) UV finiteness*)

poleZW$[x_] := SeriesCoefficient[x /. {A0[m2_] :> m2/ep2, B0[__] -> 1/ep2, Derivative[1, 0, 0][B0][__] -> 0, DB0[__] -> 0, C0[__] -> 0} /.
     D -> 4 - 2 ep2 /. ep -> ep2, {ep2, 0, -1}];
vStdZW$ = {{c12 c13, s12 c13, s13/ph}, {-s12 c23 - c12 s23 s13 ph, c12 c23 - s12 s23 s13 ph, s23 c13},
    {s12 s23 - c12 c23 s13 ph, -c12 s23 - s12 c23 s13 ph, c23 c13}} /. {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
vPyZW$ = vStdZW$ /. {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5};
explicitZW$ = {cK[i_, j_] :> vPyZW$[[i, j]], cKc[i_, j_] :> (vPyZW$[[i, j]] /. ph -> 1/ph)};
simpZW$[x_] := Simplify[Together[x /. explicitZW$ /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2]], 0 < sw < 1 && MW > 0];
(* the poles with p^2 = pp2 kept in the fermion legs, then pp2 -> m^2 (a limit for massless f) *)
uvLimZW$[ch_, x_] := Module[{m = zffZW$[ch]["mass"]}, Limit[Together[x], pp2 -> m^2]];
uvZW$ = Table[ch -> simpZW$[uvLimZW$[ch, #] & /@ poleZW$[totalNumZW$[ch][[1 ;; 2]]]], {ch, chansZW$}];
Print["(a) UV pole of K FL, K FR for the eleven fermions (expect all {0, 0}): ", Union[Last /@ uvZW$]];
Print["    without the mixing (expect 8 nonzero, the charged fermions): ",
  Count[Table[simpZW$[uvLimZW$[ch, #] & /@ poleZW$[(totalNumZW$[ch] - piecesZW$[ch]["mixing"])[[1 ;; 2]]]], {ch, chansZW$}], x_ /; x =!= {0, 0}],
  " of 11;  with the photon tree of the opposite sign: ",
  Count[Table[simpZW$[uvLimZW$[ch, #] & /@ poleZW$[(totalNumZW$[ch] - 2 piecesZW$[ch]["mixing"])[[1 ;; 2]]]], {ch, chansZW$}], x_ /; x =!= {0, 0}],
  " of 11 left"];
tick$["(a)"];

(* ::Section:: *)
(*(b) The interference with the Born*)

(* sum over spins and Z polarizations of M0^* S_i, M0 = ubar epsslash (a P_L + b P_R) v, S_i the four structures, 4 dimensions *)
FCClearScalarProducts[];
SP[p1, p1] = mm^2; SP[p2, p2] = mm^2; SP[p1, p2] = (MZ2 - 2 mm^2)/2;
polZW$ = -MT[mu, nu] + (FV[p1, mu] + FV[p2, mu]) (FV[p1, nu] + FV[p2, nu])/MZ2;
m0cZW$ = (GA[nu] . (aa GA[7] + bb GA[6]));   (* (ubar gamma^nu (a P_L + b P_R) v)^* = vbar gamma^nu (a P_L + b P_R) u for real a, b *)
strZW$ = {GA[mu] . GA[7], GA[mu] . GA[6], FV[p1, mu] GA[7], FV[p1, mu] GA[6]};
trZW$ = Simplify[Contract[polZW$ DiracTrace[(GS[p2] - mm) . m0cZW$ . (GS[p1] + mm) . #, DiracTraceEvaluate -> True]]] & /@ strZW$;
bornZW$ = Simplify[trZW$ . {aa, bb, 0, 0}];
Print["(b) Born sum minus 2 [(a^2 + b^2)(MZ^2 - m^2) + 6 a b m^2] (expect 0): ", Simplify[bornZW$ - 2 ((aa^2 + bb^2) (MZ2 - mm^2) + 6 aa bb mm^2)]];

(* the inputs: MS-bar at mu from nlo_inputs.py, pole masses; exact rationals for Package-X *)
inputsZW$[mu_] := Module[{out = RunProcess[{"python3", "-c",
       "import sys; sys.path.insert(0, '" <> srcDirZW$ <> "'); from nlo_inputs import at, POLE; p = at(" <> ToString[CForm[N[mu, 17]]] <>
        "); V = p['V']; print(' '.join('%.17e' % float(x) for x in [p['s2'], p['e']] + list(V.real.ravel()) + list(V.imag.ravel())))"},
      ProcessDirectory -> srcDirZW$]["StandardOutput"], nums},
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
(* the CKM entries are machine numbers: with the cancellations of the light-quark self-energies they leave about 7 digits
   for u, d, s (15 for c, b; the leptons are exact) *)
deltaZW$[ch_, mu_, xis_, inp_, masses_: poleMassesZW$] := Module[{z = zffZW$[ch], s2 = Rationalize[inp["s2"], 10^-14], e2, rules, f1,
    f0, pole, fin, tr, b0, m, mz = MZ /. masses},
   e2 = Rationalize[inp["e"]^2, 10^-14];
   m = z["mass"] /. masses;
   rules = Join[{sw -> Sqrt[s2], cw -> Sqrt[1 - s2], ee -> Sqrt[e2]}, xis, masses, {MW -> Sqrt[mz^2 (1 - s2)]},
     {cK[i_, j_] :> inp["V"][[i, j]], cKc[i_, j_] :> Conjugate[inp["V"][[i, j]]]}];
   f1 = totalNumZW$[ch] /. rules;
   If[m =!= 0, f1 = f1 /. pp2 -> m^2];   (* massive: p^2 = m^2 at once; massless: the limit after Package-X *)
   {pole, fin} = Transpose[numericZW$[#, mu, m^2] & /@ f1];
   f0 = {z["T3"] - z["Q"] s2, -z["Q"] s2};
   tr = trZW$ /. {aa -> f0[[1]], bb -> f0[[2]], mm -> m, MZ2 -> mz^2};
   b0 = bornZW$ /. {aa -> f0[[1]], bb -> f0[[2]], mm -> m, MZ2 -> mz^2};
   {Re[2 tr . fin/b0]/KK, Max[Abs[pole]]}];
inpMZ$ = inputsZW$[911876/10000];
Print["(b) inputs at mu = M_Z: s^2 = ", inpMZ$["s2"], ", 1/alpha = ", 4 Pi/inpMZ$["e"]^2, ", |V_tb| = ", Abs[inpMZ$["V"][[3, 3]]]];
xiSets$ = {{xiZ -> 1, xiW -> 1}, {xiZ -> 2, xiW -> 3}, {xiZ -> 1/2, xiW -> 4}};
rowsZW$ = {};
Do[Module[{r = deltaZW$[ch, 911876/10000, #, inpMZ$] & /@ xiSets$},
   Print["   ", zffZW$[ch]["name"], ": delta_weak at (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4): ",
    NumberForm[#, 12] & /@ r[[All, 1]], ";  spread ", ScientificForm[Max[r[[All, 1]]] - Min[r[[All, 1]]], 2],
    ";  largest UV pole left ", ScientificForm[Max[r[[All, 2]]], 2]];
   AppendTo[rowsZW$, {zffZW$[ch]["name"], 911876/10000 // N, ToString[CForm[r[[1, 1]]]], ToString[CForm[Max[r[[All, 1]]] - Min[r[[All, 1]]]]]}]],
  {ch, chansZW$}];
tick$["(b)"];

(* ::Section:: *)
(*(c) The mu dependence*)

Do[Module[{inp = inputsZW$[mu]},
   Do[Module[{r = deltaZW$[ch, mu, xiSets$[[1]], inp]},
      AppendTo[rowsZW$, {zffZW$[ch]["name"], N[mu], ToString[CForm[r[[1]]]], ""}]], {ch, chansZW$}]],
  {mu, {911876/20000, 911876/5000}}];
Export[FileNameJoin[{resDirZW$, "zweak.csv"}], Prepend[rowsZW$, {"fermion", "mu", "delta_weak", "xi_spread"}], "CSV"];
tick$["(c); written results/zweak.csv"];

(* ::Section:: *)
(*(d) The point of the CKM note's MadLoop check (for zweak_madloop.py)*)

(* the param_card of models/sm_ckm/Src/ckm_madloop_ext.py: 1/alpha = 128, M_Z = 91, M_W = 80 (c_W = M_W/M_Z), ..., read as MS-bar *)
pointMassesZW$ = {MZ -> 91, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/10000, MU -> 127/10000,
   MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
ckmStdZW$[s12_, s23_, s13_, dl_] := Module[{c12 = Sqrt[1 - s12^2], c23 = Sqrt[1 - s23^2], c13 = Sqrt[1 - s13^2], e = Exp[I dl]},
   N[{{c12 c13, s12 c13, s13/e}, {-s12 c23 - c12 s23 s13 e, c12 c23 - s12 s23 s13 e, s23 c13},
     {s12 s23 - c12 c23 s13 e, -c12 s23 - s12 c23 s13 e, c23 c13}}]];
inpPointZW$ = <|"s2" -> 1 - 80^2/91^2, "e" -> Sqrt[4 Pi/128], "V" -> ckmStdZW$[0.22501, 0.04183, 0.003732, 1.147]|>;
mlRowsZW$ = {};
Do[Module[{r = deltaZW$[ch, muR, xiSets$[[1]], inpPointZW$, pointMassesZW$]},
    Print["(d) MadLoop point, ", zffZW$[ch]["name"], ", mu_R = ", muR, ": delta_weak = ", NumberForm[r[[1]], 12]];
    AppendTo[mlRowsZW$, {zffZW$[ch]["name"], muR, ToString[CForm[N[r[[1]], 20]]]}]], {ch, {{1, 3}, {2, 3}, {4, 3}}}, {muR, {91, 500}}];
Export[FileNameJoin[{resDirZW$, "zweak_ml.csv"}], Prepend[mlRowsZW$, {"fermion", "mu_R", "delta_weak"}], "CSV"];
tick$["(d); written results/zweak_ml.csv"];
