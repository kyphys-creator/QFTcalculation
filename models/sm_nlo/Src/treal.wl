(* ::Package:: *)

(* ::Title:: *)
(*Step (4c) of the NLO note: the hard photon of t -> d_j W+ gamma and the electroweak correction to the top width*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4c), as wreal.wl for W+ -> f fbar'.  For t -> d_j W+ (j = d, s, b):*)
(*  the tree t(pt) -> d_j(p1) W+(p2) gamma(p3) of the note's FeynArts model (the photon from the top, the d_j and the W, and the*)
(*  Goldstone diagram; Feynman gauge), sum|M_R|^2 in 4 dimensions (W: -g + p2 p2/M_W^2, photon -g), R = sum|M_R|^2/(e^2 sum|M_0|^2);*)
(*  checks: (a) the Ward identity of the photon (its polarization replaced by p3 in the amplitude and its conjugate, the W*)
(*  polarizations summed: the square must vanish); (b) R against the eikonal factor of the three charges near E -> 0;*)
(*  the hard part E_gamma > Delta E = delta E_max (top rest frame), K_H = int ds12 ds13 R/(32 pi m_t^2 Phi_2), Gauss-Legendre in*)
(*  logarithmic variables (wreal.wl's hardKWR$); with tweak.wl (results/tweak_vs.csv) the electroweak correction*)
(*    delta_EW = [delta_V + (alpha/pi) K_S] + (alpha/pi) K_H,  which must not depend on delta beyond O(delta);*)
(*  (c) t -> b W+ at m_b/3, m_b/10: delta_EW must not depend on m_b beyond powers of m_b/m_t (the collinear logarithm of the b*)
(*  cancels between the virtual + soft and the hard photon), and K_H must change by the collinear coefficient.*)
(*Writes results/treal.csv (and work/me_treal.txt, R and the Born sum of t -> b W+ for treal_mg5.py).*)
(*Batch:  wolframscript -file treal.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirTR$ = DirectoryName[$InputFileName];
resDirTR$ = FileNameJoin[{srcDirTR$, "results"}];
t0WR$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0WR$], " s] ", s];
trEvalWR$[x_] := x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
modelTmpWR$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTR$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpWR$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpWR$, "SM_CKM_FA"}], Quiet -> True];
modelWR$ = FileNameJoin[{modelTmpWR$, "SM_CKM_FA", "SM_CKM_FA"}];
lepMWR$ = {Me, MMU, MTA}; upMWR$ = {MU, MC, MT}; dnMWR$ = {MD, MS, MB};
convWR$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV[x_String] :> ToExpression[x],
   Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
yukWR$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMWR$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMWR$[[i]]/vev, 0], yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMWR$[[i]]/vev, 0]};
chansWR$ = {{3, 3, 1}, {3, 3, 2}, {3, 3, 3}};
(* name, outgoing fields, m1 (the d_j), m2 (the W), their charges *)
chanInfoWR$[ch_] := {"t" <> {"d", "s", "b"}[[ch[[3]]]] <> "W", {F[4, {ch[[3]]}], V[3]}, dnMWR$[[ch[[3]]]], MW, {-1/3, 1}};
faAmpWR$[out_, ext_] := Module[{d},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> Length[out]], {F[3, {3}]} -> out, InsertionLevel -> {Particles},
       Model -> modelWR$, GenericModel -> modelWR$], RuleDelayed::rhs];
   (* the generation sums of the Goldstone couplings expanded before the Yukawa rules (DropIndexSum -> False, as zff_feyncalc.wl) *)
   Module[{a = Quiet[FCFAConvert[CreateFeynAmp[d] /. M$FACouplings, IncomingMomenta -> {pt}, OutgoingMomenta -> ext, ChangeDimension -> 4,
        List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False,
        TransversePolarizationVectors -> {}], RuleDelayed::rhs]},
    a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
    a = (sumOverWR$ /@ a) /. convWR$ /. yukWR$ /. vev -> 2 MW sw/ee /. SUNFDelta[__] -> 1;
    If[! FreeQ[a, CKM | IndexSum | yd | yu | yl], Print["   WARNING: CKM, IndexSum or a Yukawa left"]];
    a]];
sumOverWR$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
kin3WR$[m1_, m2_] := (FCClearScalarProducts[];
   SP[p1, p1] = m1^2; SP[p2, p2] = m2^2; SP[p3, p3] = 0; SP[pt, pt] = MT^2;
   SP[p1, p2] = (s12 - m1^2 - m2^2)/2; SP[p1, p3] = (s13 - m1^2)/2; SP[p2, p3] = (MT^2 + m1^2 - s12 - s13)/2;
   SP[pt, p1] = m1^2 + (s12 - m1^2 - m2^2)/2 + (s13 - m1^2)/2; SP[pt, p2] = m2^2 + (s12 - m1^2 - m2^2)/2 + (MT^2 + m1^2 - s12 - s13)/2;
   SP[pt, p3] = (MT^2 - s12)/2;);
sqWR$[a_, vecs_] := Module[{x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1]},
   x = trEvalWR$[x];
   Do[x = DoPolarizationSums[x, Sequence @@ v], {v, vecs}];
   Simplify[Contract[FeynAmpDenominatorExplicit[DiracSimplify[x]]]]];
rWR$ = <||>; b0WR$ = <||>; wardWR$ = <||>;
Do[Module[{info = chanInfoWR$[ch], m1, m2, a3},
   {m1, m2} = info[[3 ;; 4]];
   a3 = faAmpWR$[Append[info[[2]], V[1]], {p1, p2, p3}];
   kin3WR$[m1, m2];
   (* (a) the Ward identity: the photon polarization -> p3 in the amplitude and its conjugate, the W polarizations summed *)
   wardWR$[ch] = sqWR$[a3 /. Polarization[p3, _] -> p3, {{p2}}];
   rWR$[ch] = sqWR$[a3, {{p2}, {p3, 0, VirtualBoson -> True}}];
   FCClearScalarProducts[];
   SP[p1, p1] = m1^2; SP[p2, p2] = m2^2; SP[pt, pt] = MT^2; SP[p1, p2] = (MT^2 - m1^2 - m2^2)/2;
   SP[pt, p1] = (MT^2 + m1^2 - m2^2)/2; SP[pt, p2] = (MT^2 - m1^2 + m2^2)/2;
   b0WR$[ch] = sqWR$[faAmpWR$[info[[2]], {p1, p2}], {{p2}}];
   rWR$[ch] = Together[rWR$[ch]/(ee^2 b0WR$[ch])];
   Print[info[[1]], ": ", Length[a3], " diagrams;  Ward identity (expect 0): ", Simplify[wardWR$[ch]], ";  R free of the couplings: ",
    FreeQ[rWR$[ch], ee | sw | cK | cKc]]], {ch, chansWR$}];
DeleteDirectory[modelTmpWR$, DeleteContents -> True];
tick$["(a) squared amplitudes"];
(* for treal_mg5.py: R in s12, s13 and the Born sum (|V| = 1, one colour) of t -> b W+, CForm *)
Export[FileNameJoin[{srcDirTR$, "work", "me_treal.txt"}], StringRiffle[Flatten[Table[{chanInfoWR$[ch][[1]] <> "|" <> ToString[CForm[rWR$[ch]]],
      chanInfoWR$[ch][[1]] <> "_B|" <> ToString[CForm[b0WR$[ch] /. {cK[__] -> 1, cKc[__] -> 1}]]}, {ch, chansWR$[[{3}]]}]], "\n"],
  "Text"];

(* (b) the soft limit: R -> -sum eta_i eta_j e_i e_j p_i.p_j/((p_i.p3)(p_j.p3)), the top incoming *)
eikWR$[m1_, m2_, e1_, e2_] := Module[{pp12 = (s12 - m1^2 - m2^2)/2, pp13 = (s13 - m1^2)/2, pp23 = (MT^2 + m1^2 - s12 - s13)/2,
    pk1, pk2, pk3, eW = e1 + e2},
   pk3 = (MT^2 - s12)/2; pk1 = m1^2 + pp12 + pp13; pk2 = m2^2 + pp12 + pp23;
   -(eW^2 MT^2/pk3^2 + e1^2 m1^2/pp13^2 + e2^2 m2^2/pp23^2 - 2 eW e1 pk1/(pk3 pp13) - 2 eW e2 pk2/(pk3 pp23) + 2 e1 e2 pp12/(pp13 pp23))];
softPtWR$[mw_, m1_, m2_, eg_] := Module[{s = mw^2 - 2 mw eg, e1, e3},
   e1 = (s + m1^2 - m2^2)/(2 Sqrt[s]); e3 = (mw^2 - s)/(2 Sqrt[s]);
   {s12 -> s, s13 -> m1^2 + 2 e3 e1}];
Do[Module[{info = chanInfoWR$[ch], num = {MT -> 173, MW -> 80, MD -> 1, MS -> 3/2, MB -> 5}, m1, m2},
   {m1, m2} = info[[3 ;; 4]] /. num;
   Print[info[[1]], ": R/eik - 1 at E = 1e-4, 1e-6 E_max: ",
    N[Table[(rWR$[ch]/eikWR$[m1, m2, info[[5, 1]], info[[5, 2]]] - 1) /. num /. softPtWR$[173, m1, m2, ef (173^2 - (m1 + m2)^2)/346],
      {ef, {10^-4, 10^-6}}], 4]]],
  {ch, chansWR$}];
tick$["(b) soft limit"];

(* ::Section:: *)
(*Hard integrals*)

glRuleWR$[npan_, npt_] := Module[{g = NIntegrate`GaussRuleData[npt, MachinePrecision]},
   {Flatten[Table[(i - 1 + g[[1]])/npan, {i, npan}]], Flatten[Table[g[[2]]/npan, {i, npan}]]}];
(* rexpr = {R in xx = M^2 - s12 and ww = 2 p1.p3, R in xx and wq = 2 p2.p3}: each edge with its own small variable, so that
   2 p2.p3 near the edge along particle 2 is not formed as a difference x - w (for the electron it is 1e-11 x); the edge along
   particle 1 logarithmic for m1 > 0, linear for the massless neutral neutrino *)
hardKWR$[rexpr_, Mv_, m1v_, m2v_, dl_, npan_, npt_: 20] := Module[
   {xhi = Mv^2 - (m1v + m2v)^2, xlo, xc, phi2, U, WU, uu, vv, wgt, pieces},
   xlo = dl xhi; xc = xhi/2;
   phi2 = Sqrt[(Mv^2 - (m1v + m2v)^2) (Mv^2 - (m1v - m2v)^2)]/(8 Pi Mv^2);
   {U, WU} = glRuleWR$[npan, npt];
   uu = Flatten[Transpose[ConstantArray[U, Length[U]]]]; vv = Flatten[ConstantArray[U, Length[U]]];
   wgt = Flatten[Outer[Times, WU, WU]];
   pieces = {{xlo Exp[uu Log[xc/xlo]], xhi - xlo Exp[uu Log[xc/xlo]], xlo Exp[uu Log[xc/xlo]] Log[xc/xlo]}, {xhi - xc uu^2, xc uu^2, 2 xc uu}};
   Total[Function[pc, Module[{x = pc[[1]], xmx = pc[[2]], jac = pc[[3]], s, e1, e2, p1s, e3, wlo, whi, wm, wa, ja, wplo, wpm, wb, ra, rb},
       s = Mv^2 - x;
       e1 = (s + m1v^2 - m2v^2)/(2 Sqrt[s]); e2 = (s + m2v^2 - m1v^2)/(2 Sqrt[s]);
       p1s = Sqrt[xmx (s - (m1v - m2v)^2)]/(2 Sqrt[s]); e3 = x/(2 Sqrt[s]);
       wlo = 2 e3 m1v^2/(e1 + p1s); whi = 2 e3 (e1 + p1s); wm = (wlo + whi)/2;
       If[m1v == 0, wa = wm vv; ja = wm, wa = wlo (wm/wlo)^vv; ja = wa Log[wm/wlo]];
       wplo = 2 e3 m2v^2/(e2 + p1s); wpm = x - wm; wb = wplo (wpm/wplo)^vv;
       ra = rexpr[[1]] /. {xx -> x, ww -> wa};
       rb = rexpr[[2]] /. {xx -> x, wq -> wb};
       Total[wgt jac (ra ja + rb wb Log[wpm/wplo])]]] /@ pieces]/(32 Pi Mv^2 phi2)];
massesWR$ = {MT -> 17257/100, MW -> 803692/10000, MD -> 271/100000, MS -> 546/10000, MB -> 478/100};
vs$ = GroupBy[Rest[Import[FileNameJoin[{resDirTR$, "tweak_vs.csv"}], "CSV"]], {#[[1]], #[[2]]} &];
fmtWR$[l_, n_: 12] := StringRiffle[ToString[NumberForm[#, n, NumberFormat -> (If[#3 === "", #1, #1 <> "e" <> #3] &),
       ExponentFunction -> (If[-5 < # < 5, Null, #] &)]] & /@ l, ", "];
rowsWR$ = {};
khWR$ = <||>;
(* the channels, and t -> b W+ at m_b/3, m_b/10 (tweak.wl's tbW_mb3, tbW_mb10) *)
runsWR$ = Join[{#, chanInfoWR$[#][[1]], massesWR$} & /@ chansWR$,
   {{{3, 3, 3}, "tbW_mb3", massesWR$ /. (MB -> _) -> (MB -> 478/300)}, {{3, 3, 3}, "tbW_mb10", massesWR$ /. (MB -> _) -> (MB -> 478/1000)}}];
Do[Module[{ch = run[[1]], name = run[[2]], ms = run[[3]], info, m1, m2, mt, rx, kh, conv, mus},
   info = chanInfoWR$[ch]; mt = N[MT /. ms];
   {m1, m2} = N[info[[3 ;; 4]] /. ms];
   rx = {Together[rWR$[ch] /. {s12 -> MT^2 - xx, s13 -> info[[3]]^2 + ww}], Together[rWR$[ch] /. {s12 -> MT^2 - xx, s13 -> info[[3]]^2 + xx - wq}]} /.
     ms /. MT -> mt;
   kh = Table[hardKWR$[rx, mt, m1, m2, N[dl], 24], {dl, {10^-4, 10^-5, 10^-6, 10^-7, 10^-8}}];
   khWR$[name] = kh;
   conv = kh[[-1]] - hardKWR$[rx, mt, m1, m2, 10.^-8, 16];
   mus = Union[#[[2]] & /@ Flatten[Values[KeySelect[vs$, First[#] == name &]], 1]];
   Do[Module[{vsl = SortBy[vs$[{name, mu}], -#[[3]] &], tot},
      tot = Table[ToExpression[vsl[[i, 4]]] + ToExpression[vsl[[i, 5]]] kh[[i]], {i, 5}];
      Print[name, ", mu = ", mu, ": delta_EW at delta = 1e-4 ... 1e-8: ", fmtWR$[tot], ";  minus the value at 1e-8: ",
       fmtWR$[tot - Last[tot], 2], ";  24 - 16 panels (K_H): ", fmtWR$[{conv}, 2]];
      AppendTo[rowsWR$, {name, mu, ToString[CForm[tot[[-1]] - (tot[[-2]] - tot[[-1]])/9]], ToString[CForm[kh[[-1]]]]}]], {mu, mus}]],
  {run, runsWR$}];
tick$["hard integrals"];
(* (c) the b mass: delta_EW at m_b, m_b/3, m_b/10 (mu = m_t), and K_H(m_b/f) - K_H(m_b) against the collinear coefficient
   Q_b^2 (-ln delta' - 3/4) ln f^2, delta' = Delta E/E_pair (E_pair the energy of the b + photon pair, (m_t^2 + m_b^2 - M_W^2)/(2 m_t)) *)
Module[{d = Association[(#[[1]] -> ToExpression[#[[3]]]) & /@ Select[rowsWR$, #[[2]] == N[17257/100] &]], pred},
  Print["(c) delta_EW of t -> b W+ at m_b, m_b/3, m_b/10 (mu = m_t): ", fmtWR$[{d["tbW"], d["tbW_mb3"], d["tbW_mb10"]}],
   ";  minus the value at m_b: ", fmtWR$[{d["tbW_mb3"] - d["tbW"], d["tbW_mb10"] - d["tbW"]}, 2]];
  pred[f_] := Module[{mb = 478/100/f, mt = 17257/100, mw = 803692/10000, emax, epair},
    emax = (mt^2 - (mb + mw)^2)/(2 mt); epair = (mt^2 + mb^2 - mw^2)/(2 mt);
    N[(1/9) (-Log[10^-8 emax/epair] - 3/4) Log[f^2]]];
  Print["    K_H(m_b/f) - K_H(m_b) at delta = 1e-8, f = 3, 10: ", fmtWR$[{khWR$["tbW_mb3"][[-1]] - khWR$["tbW"][[-1]],
      khWR$["tbW_mb10"][[-1]] - khWR$["tbW"][[-1]]}], ";  the collinear coefficient: ", fmtWR$[{pred[3], pred[10]}]]];
Export[FileNameJoin[{resDirTR$, "treal.csv"}], Prepend[rowsWR$, {"channel", "mu", "delta_EW", "KH_at_1e-8"}], "CSV"];
Print["written: results/treal.csv"];
