(* ::Package:: *)

(* ::Title:: *)
(*Step (9): this note's on-shell quark field constants at the UFO's point (for the UFO and for the check of NLOCT's)*)


(* ::Text:: *)
(*From the quark self-energies of step (3) (results/oneloop_ckm_sigma.m: 1PI + tadpole, electroweak, general R_xi), in*)
(*Feynman gauge with the photon-mass limit MA -> 0 taken coefficient by coefficient (wud_madloop_ref.wl):*)
(*  off-diagonal (i != j): dZ^L of note Eq. (dZos) and dZ^R of Eq. (dZRos), at p^2 = m_j^2 (no photon: IR finite);*)
(*  diagonal: dZ^L = -Sigma^L - m^2 (Sigma^L' + Sigma^R' + 2 Sigma^S'), dZ^R likewise with L <-> R (Denner); the IR*)
(*  divergent B0' with the photon mass lambda^2 = mu^2 (dimensional regularization at mu) and its IR pole from the*)
(*  coefficient of ln lambda^2;*)
(*dZ_W = -Sigma_T^WW'(MW^2), and the bosons that do not depend on V at one loop, from the SM note's step (3)*)
(*(models/sm/Src/results/oneloop_sigma.m): dZ_ZZ = -Sigma_T^ZZ'(MZ^2), dZ_AA = -Sigma_T^AA'(0), dZ_HH = -Sigma^HH'(MH^2), and*)
(*the photon-Z mixing Sigma_T^AZ(0)/MZ^2, Sigma_T^AZ(MZ^2)/MZ^2 (combined into dZ_AZ, dZ_ZA with the convention of the*)
(*FeynRules counterterm Lagrangian in nlo_ckm_dz.wl, which matches it against NLOCT).  The tadpole is momentum independent and diagonal: it does not enter.  The loop integrals*)
(*are taken real (Re-tilde): the quark self-energies at p^2 = m_j^2 of the light quarks have no threshold; for the top*)
(*(p^2 = m_t^2 > (MW + m_b)^2) the real part is the on-shell condition used by MadLoop's LSZ factor only through dZ_tj,*)
(*which no process here has on an external leg.  The point is that of nlo_ckm_dz.wl.  Numbers {pole (UV + IR), finite*)
(*at 91 GeV} in the convention of the UFO's CT parameters (NLOCT's FR$Eps = eps).*)
(*Writes Src/generated/SM_CKM_dZown.m.  Batch: wolframscript -file nlo_ckm_dzown.wl*)
(*With the argument ms0: the same point with m_s = 0 (the flavour-changing processes of steps (7), (8)), written to*)
(*SM_CKM_dZown_ms0.m; the scalar self-energy of a massless quark i is then taken from the P_R part (SSR, as step (7)),*)
(*and the diagonal constants of the s quark (IR and collinear divergent, not used by those processes) are set to 0.*)


srcDirZO$ = DirectoryName[$InputFileName];
ms0ZO$ = Length[$ScriptCommandLine] >= 2 && $ScriptCommandLine[[2]] === "ms0";
zeroZO$ = If[ms0ZO$, {MS}, {}];
t0ZO$ = AbsoluteTime[];
renZO$ = {A0 -> fA0$, B0 -> fB0$, C0 -> fC0$};
sig3ZO$ = Association[Get[FileNameJoin[{srcDirZO$, "results", "oneloop_ckm_sigma.m"}]]] /. renZO$;
kRuleZO$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toCKZO$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
upZO$ = {MU, MC, MT}; dnZO$ = {MD, MS, MB};
sgZO$[sec_, i_, j_, n_] := Total[sig3ZO$[sec][[i, j, All, n]]] /. kRuleZO$ /. toCKZO$ /. gS -> 0;
limitZO$[x_] := Module[{y = x /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1}, fs, cs, c0},
   fs = Union[Cases[y, fA0$[__] | fB0$[__] | fC0$[__] | Derivative[1, 0, 0][fB0$][__], Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   If[! FreeQ[Denominator /@ Append[cs, c0], MA], Print["   WARNING: 1/MA left"]];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {fA0$[0] -> 0, fB0$[0, 0, 0] -> 0}];
(* note Eqs. (dZos), (dZRos) and Denner's diagonal constants; n = 1 SL, 2 SR, 3 SS (Sigma^S with m_i P_L + m_j P_R) *)
dZZO$[sec_, ch_, i_, j_] := Module[{ms = If[sec === "U", upZO$, dnZO$], mi, mj, sl, sr, ss, a, b},
   mi = ms[[i]]; mj = ms[[j]];
   If[i === j && MemberQ[zeroZO$, mi], Return[0]];
   {sl, sr, ss} = sgZO$[sec, i, j, #] & /@ {1, 2, If[MemberQ[zeroZO$, mi], 4, 3]};
   {sl, sr, ss} = {sl, sr, ss} /. Thread[zeroZO$ -> 0];
   If[MemberQ[zeroZO$, mi], mi = 0]; If[MemberQ[zeroZO$, mj], mj = 0];
   {a, b} = If[ch === "L", {sl, sr}, {sr, sl}];
   limitZO$[If[i =!= j,
     2/(mi^2 - mj^2) (mj^2 a + mi mj b + If[ch === "L", mi^2 + mj^2, 2 mi mj] ss) /. kk2 -> mj^2,
     (-a - mi^2 D[sl + sr + 2 ss, kk2]) /. kk2 -> mi^2]]];
symZO$ = Join[
   Flatten[Table[{"U", ch, i, j} -> dZZO$["U", ch, i, j], {ch, {"L", "R"}}, {i, 3}, {j, 3}], 2],
   Flatten[Table[{"D", ch, i, j} -> dZZO$["D", ch, i, j], {ch, {"L", "R"}}, {i, 3}, {j, 3}], 2],
   {"W" -> limitZO$[-D[Total[sig3ZO$["WW"]] /. kRuleZO$ /. toCKZO$, kk2] /. kk2 -> MW^2]},
   (* the SM note's boson self-energies (K times, 1PI + tadpole; V does not enter) *)
   Module[{sm = Association[Get[FileNameJoin[{ParentDirectory[srcDirZO$], "..", "sm", "Src", "results", "oneloop_sigma.m"}]]] /. renZO$,
      tot},
     tot[key_] := Total[sm[key]] /. kRuleZO$;
     (* at k^2 = 0 the photon self-energies have 1/k^2 terms (the reduction): kept as functions of kk2 here, expanded
        in numZO$ (the closed Taylor coefficients of B0, as wud_renormalized.wl) *)
     {"Z" -> limitZO$[-D[tot["ZZ"], kk2] /. kk2 -> MZ^2], "A" -> smallK$[limitZO$[tot["AA"]], 1, -1],
      "H" -> limitZO$[-D[tot["HH"], kk2] /. kk2 -> MH^2],
      "AZ0" -> smallK$[limitZO$[tot["AZ"]]/MZ^2, 0, 1], "AZMZ" -> limitZO$[tot["AZ"] /. kk2 -> MZ^2]/MZ^2}]];
Print["constants built: ", Length[symZO$], ";  ", Round[AbsoluteTime[] - t0ZO$], " s"];

(* the point *)
pointZO$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MS -> If[ms0ZO$, 0, 546/10000], MD -> 271/10000, MU -> 127/10000, MTA -> 1746/1000,
   MMU -> 1027/10000, Me -> 487/1000000};
vStdZO$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
vRulesZO$ = {cK[i_, j_] :> N[vStdZO$[[i, j]], 30], cKc[i_, j_] :> Conjugate[N[vStdZO$[[i, j]], 30]]};
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.]; SetMudim[91.^2];
KK = 16 Pi^2;
laurZO$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
       Derivative[1, 0, 0][fB0$][pp_, a_, b_] :> db0f$[pp, a, b], fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep},
   {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
valZO$[x_, lam2_] := (SetLambda[N[lam2]]; x /. {a0f$[m2_] :> If[m2 == 0, 0, m2 (1 - Log[m2/91^2])], b0f$[pp_, a_, b_] :> Re[LoopTools`B0[pp, a, b]],
     db0f$[pp_, a_, b_] :> Re[LoopTools`DB0[pp, a, b]], c0f$[a__] :> Re[LoopTools`C0[a]]});
(* {pole (UV + IR), finite at 91 GeV} of K dZ, divided by K *)
numZO$[0] := {0, 0};
(* sign times the coefficient of kk2^order of a k^2 -> 0 expansion: B0(k^2; a, b) = B0(0; a, b) + sum_n c_n k^(2n),
   c_n = int (x(1-x))^n/(x a + (1-x) b)^n dx / n *)
cnZO$[n_, a_, b_] := Which[a == b, (n!)^2/((2 n + 1)! n a^n), n == 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, NIntegrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}, WorkingPrecision -> 40]/n];
(* exact until the series is taken: the 1/k^2 terms cancel, and floating point would lose half the digits *)
numZO$[smallK$[x_, order_, sign_]] := Module[{y = x /. pointZO$, s},
   y = y /. fB0$[kk_, a_, b_] /; ! FreeQ[kk, kk2] :> fB0$[0, a, b] + Sum[kk^n cnZO$[n, a, b], {n, 1, 3}];
   y = y /. {fA0$[m2_] :> If[m2 == 0, 0, m2 (1/ep + 1 - Log[m2/91^2])],
       fB0$[0, a_, b_] :> Which[a == 0 && b == 0, 0, a == b, 1/ep - Log[a/91^2], True, 1/ep + 1 - (a Log[a/91^2] - b Log[b/91^2])/(a - b)]} /.
     D -> 4 - 2 ep;
   s = Normal[Series[y, {kk2, 0, order}]];
   N[sign {SeriesCoefficient[Coefficient[s, kk2, order], {ep, 0, -1}], SeriesCoefficient[Coefficient[s, kk2, order], {ep, 0, 0}]}/KK, 40]];
numZO$[x_] := Module[{l = laurZO$[N[x /. vRulesZO$ /. pointZO$, 30]], f1, f2},
   f1 = valZO$[l[[2]], 91^2]; f2 = valZO$[l[[2]], 2 91^2];
   {l[[1]] + (f2 - f1)/Log[2], f1}/KK];
resZO$ = (#[[1]] -> numZO$[#[[2]]]) & /@ symZO$;
Print["this note's on-shell constants at the point (pole, finite at 91 GeV):"];
Scan[Print["   ", #[[1]], ":  ", N[#[[2, 1]], 8], ",  ", N[#[[2, 2]], 8]] &, resZO$];
outZO$ = If[ms0ZO$, "SM_CKM_dZown_ms0.m", "SM_CKM_dZown.m"];
Put[<|"dZ" -> resZO$, "mu0" -> 91|>, FileNameJoin[{srcDirZO$, "generated", outZO$}]];
Print["written: generated/", outZO$, ";  ", Round[AbsoluteTime[] - t0ZO$], " s"];
Uninstall[First[Select[Links[], StringContainsQ[First[#], "LoopTools"] &]]];
