(* ::Package:: *)

(* ::Title:: *)
(*Step (9) of the CKM note: this note's W+ -> u_i dbar_j at one loop in MadLoop's conventions (the reference for MadLoop)*)


(* ::Text:: *)
(*The renormalized amplitude of step (5) (wud_renormalized.wl: the 1PI vertex of wud_vertex_feyncalc.wl, the on-shell LSZ*)
(*factors of the external legs with the off-diagonal ones of note Eq. (dZos), the MS-bar counterterms dg/g and dV of*)
(*Eqs. (dV), (Vrun)) in Feynman gauge, written as MadLoop gives it:*)
(*  - the relative virtual correction 2 Re(M0^* M1)/|M0|^2 (sum over spins and W polarizations), electroweak loops only;*)
(*  - the photon-mass limit MA -> 0 coefficient by coefficient, then the IR-divergent integrals with LoopTools' lambda^2 =*)
(*    mu^2: for soft singularities of massive particles ln lambda^2 -> ln mu^2 turns the photon-mass result into the eps^0*)
(*    coefficient of dimensional regularization at the scale mu (single IR poles only: the quarks are massive);*)
(*  - the IR pole: the coefficient of ln lambda^2 (from lambda^2 = mu^2 and 2 mu^2), for MadLoop's single pole.*)
(*The point is the benchmark of step (5) with m_u, m_d ten times larger (its "_h" point; MadLoop sets invariants with*)
(*p^2/E^2 < 1e-8 to 0, environment notes), mu = MZ and 500 GeV.  Writes results/wud_madloop_ref.csv.*)
(*Batch:  wolframscript -file wud_madloop_ref.wl  (after wud_vertex_feyncalc.wl, oneloop_ckm_feyncalc.wl)*)


(* ::Section:: *)
(*Setup (as wud_renormalized.wl)*)


srcDirMR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirMR$ = FileNameJoin[{srcDirMR$, "results"}];
workDirMR$ = FileNameJoin[{srcDirMR$, "work"}];
t0MR$ = AbsoluteTime[];
chansMR$ = Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1];
chanNameMR$[{i_, j_}] := {"u", "c"}[[i]] <> {"d", "s", "b"}[[j]];
renMR$ = {A0 -> fA0$, B0 -> fB0$, C0 -> fC0$};
vtxMR$ = Association[Table[ch -> (Get[FileNameJoin[{workDirMR$, "wud_vertex_" <> ToString[ch[[1]]] <> ToString[ch[[2]]] <> ".m"}]]["F"] /. renMR$),
    {ch, chansMR$}]];
sig3MR$ = Association[Get[FileNameJoin[{resDirMR$, "oneloop_ckm_sigma.m"}]]] /. renMR$;
KK = 16 Pi^2;
kRuleMR$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toCKMR$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
upMMR$ = {MU, MC, MT}; dnMMR$ = {MD, MS, MB};
sgMR$[sec_, i_, j_, n_] := Total[sig3MR$[sec][[i, j, All, n]]] /. kRuleMR$ /. toCKMR$ /. gS -> 0;
dZLMR$[sec_, i_, j_] := Module[{ms = If[sec === "U", upMMR$, dnMMR$], mi, mj, sl, sr, ss},
   mi = ms[[i]]; mj = ms[[j]];
   {sl, sr, ss} = sgMR$[sec, i, j, #] & /@ {1, 2, 3};
   If[i =!= j,
    2/(mi^2 - mj^2) (mj^2 sl + mi mj sr + (mi^2 + mj^2) ss) /. kk2 -> mj^2,
    (-sl - mi^2 D[sl + sr + 2 ss, kk2]) /. kk2 -> mi^2]];
(* Feynman gauge, then MA -> 0 coefficient by coefficient (wud_renormalized.wl, limitWR$) *)
limitMR$[x_] := Module[{y = x /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1}, fs, cs, c0},
   fs = Union[Cases[y, fA0$[__] | fB0$[__] | fC0$[__] | Derivative[1, 0, 0][fB0$][__], Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   If[! FreeQ[Denominator /@ Append[cs, c0], MA], Print["   WARNING: 1/MA left"]];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {fA0$[0] -> 0, fB0$[0, 0, 0] -> 0}];
zuMR$ = Table[limitMR$[dZLMR$["U", i, j]], {i, 3}, {j, 3}];
zdMR$ = Table[limitMR$[dZLMR$["D", i, j]], {i, 3}, {j, 3}];
zWMR$ = limitMR$[-D[Total[sig3MR$["WW"]] /. kRuleMR$ /. toCKMR$, kk2] /. kk2 -> MW^2];
vtxLMR$ = Map[limitMR$, vtxMR$, {2}];
vevMR$ = 2 MW sw/ee; yMR$[m_] := Sqrt[2] m/vevMR$;
vMMR$ = Array[cK, {3, 3}]; vMcMR$ = Array[cKc, {3, 3}];
kdVdlnmuMR$ = Module[{yu = yMR$ /@ upMMR$, yd = yMR$ /@ dnMMR$, hd, hu, au, ad},
   hd = vMMR$ . DiagonalMatrix[yd^2] . Transpose[vMcMR$]; hu = Transpose[vMcMR$] . DiagonalMatrix[yu^2] . vMMR$;
   au = Table[If[i == k, 0, -3/2 (yu[[i]]^2 + yu[[k]]^2)/(yu[[k]]^2 - yu[[i]]^2) hd[[i, k]]], {i, 3}, {k, 3}];
   ad = Table[If[k == j, 0, -3/2 (yd[[k]]^2 + yd[[j]]^2)/(yd[[j]]^2 - yd[[k]]^2) hu[[k, j]]], {k, 3}, {j, 3}];
   -au . vMMR$ + vMMR$ . ad];
Print["setup and the photon-mass limit;  ", Round[AbsoluteTime[] - t0MR$], " s"];


(* ::Section:: *)
(*Numbers*)


pointMR$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/10000, MU -> 127/10000, MTA -> 1746/1000,
   MMU -> 1027/10000, Me -> 487/1000000};
vStdMR$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
vNumMR$ = N[vStdMR$, 30];
vRulesMR$ = {cK[i_, j_] :> vNumMR$[[i, j]], cKc[i_, j_] :> Conjugate[vNumMR$[[i, j]]]};
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.];
(* {pole (UV), finite} with LoopTools at mu^2 and lambda^2 *)
laurMR$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
       Derivative[1, 0, 0][fB0$][pp_, a_, b_] :> db0f$[pp, a, b], fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep},
   {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
loopValMR$[x_, mu_, re_] := Module[{f = If[re, Re, Identity]},
   x /. {a0f$[m2_] :> If[m2 == 0, 0, f[m2 (1 - Log[m2/mu^2])]], b0f$[pp_, a_, b_] :> f[LoopTools`B0[pp, a, b]],
     db0f$[pp_, a_, b_] :> f[LoopTools`DB0[pp, a, b]], c0f$[a__] :> f[LoopTools`C0[a]]}];
numMR$[x_, mu_, re_ : False] := Module[{l = laurMR$[N[x /. vRulesMR$ /. pointMR$, 30]]}, {l[[1]], loopValMR$[l[[2]], mu, re]}];
(* 2 Re(M0^* M1)/|M0|^2 from the form factors (wud_renormalized.wl, ratioWR$) *)
ratioMR$[{i_, j_}] := Module[{a = upMMR$[[i]], b = dnMMR$[[j]], s = MW^2, pp, kp1, kp2, t0},
   pp = (s - a^2 - b^2)/2; kp1 = a^2 + pp; kp2 = b^2 + pp; t0 = 2 (pp + 2 kp1 kp2/s);
   N[{1, 6 a b/t0, 2 a (-pp + kp1 kp2/s)/t0, -2 b (-a^2 + kp1^2/s)/t0} /. pointMR$, 30]];
(* one scale: lambda^2 = lam2 in the IR-divergent integrals; the loop integrals of the quark dZ real (Re-tilde: no
   threshold for these external quarks, checked in step (5)) *)
deltaMR$[mu_, lam2_] := Module[{zu, zd, zw, dg, dv, rows},
   SetMudim[N[mu^2]]; SetLambda[N[lam2]];
   zu = Map[numMR$[#, mu, True] &, zuMR$, {2}]; zd = Map[numMR$[#, mu, True] &, zdMR$, {2}];
   zw = numMR$[zWMR$, mu, True];
   dg = N[-19/12 ee^2/sw^2 /. pointMR$, 30];
   dv = N[(kdVdlnmuMR$/2) /. vRulesMR$ /. pointMR$, 30];
   Table[Module[{i = ch[[1]], j = ch[[2]], v = vNumMR$[[ch[[1]], ch[[2]]]], vert, fl, polesFL},
      vert = numMR$[cK[i, j] #, mu] & /@ vtxLMR$[ch];
      (* K FL^(1): the finite parts; the UV poles cancel (dg, dV are pure poles: their poles are added to the check) *)
      fl = vert[[1, 2]] + v zw[[2]]/2 + (ConjugateTranspose[zu[[All, All, 2]]] . vNumMR$)[[i, j]]/2 + (vNumMR$ . zd[[All, All, 2]])[[i, j]]/2;
      polesFL = vert[[1, 1]] + v zw[[1]]/2 + (ConjugateTranspose[zu[[All, All, 1]]] . vNumMR$)[[i, j]]/2 + (vNumMR$ . zd[[All, All, 1]])[[i, j]]/2 +
        v dg + dv[[i, j]];
      {chanNameMR$[ch], 2 Re[Conjugate[v] ({fl, vert[[2, 2]], vert[[3, 2]], vert[[4, 2]]} . ratioMR$[ch])]/Abs[v]^2/KK,
       Abs[polesFL]/Abs[v], Max[Abs[vert[[2 ;; 4, 1]]]]}], {ch, chansMR$}]];
rowsMR$ = {};
Do[Module[{r1 = deltaMR$[mu, mu^2], r2 = deltaMR$[mu, 2 mu^2]},
   Print["mu = ", mu, " GeV:"];
   Do[Module[{fin = r1[[n, 2]], ir = (r2[[n, 2]] - r1[[n, 2]])/Log[2]},
      Print["   ", r1[[n, 1]], ":  2 Re(M0^* M1)/|M0|^2 = ", ToString[NumberForm[fin, 16]], ",  IR pole (coefficient of ln lambda^2) ",
        ToString[NumberForm[ir, 12]], ";  UV poles |FL|/|V| ", ToString[N[r1[[n, 3]]]], ", FR, HL, HR ", ToString[N[r1[[n, 4]]]]];
      AppendTo[rowsMR$, {r1[[n, 1]], mu, ToString[CForm[fin]], ToString[CForm[ir]]}]], {n, Length[r1]}]],
  {mu, {91, 500}}];
Export[FileNameJoin[{resDirMR$, "wud_madloop_ref.csv"}], Prepend[rowsMR$, {"channel", "mu", "delta_fin", "delta_IRpole"}], "CSV"];
Print["written: results/wud_madloop_ref.csv;  ", Round[AbsoluteTime[] - t0MR$], " s"];
Uninstall[First[Select[Links[], StringContainsQ[First[#], "LoopTools"] &]]];
