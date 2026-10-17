(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the CKM note: the renormalized W+ -> u_i dbar_j amplitude with the MS-bar V and with the Denner-Sack V*)


(* ::Text:: *)
(*Reads work/wud_vertex_<i><j>.m (wud_vertex_feyncalc.wl: the 1PI vertex, K FL, K FR, K HL, K HR per V_ij) and the*)
(*self-energies of step (3) (results/oneloop_ckm_sigma.m; the gluon parts are dropped, gS = 0) and of the SM note*)
(*(models/sm/Src/results/oneloop_sigma.m: Sigma^AA, Sigma^AZ, Sigma^ZZ, which do not depend on V at one loop).*)
(*The S-matrix element is the bare amputated vertex with the on-shell LSZ factors of the external legs (the field*)
(*renormalization cancels): in units of (e/(sqrt2 sw)) ubar epsslash P_L v,*)
(*  FL = V + vertex + V (dg/g + dZ_W/2) + dV + (1/2) [dZ^{uL+} V + V dZ^{dL}],*)
(*with the on-shell dZ^L of Denner (diagonal and off-diagonal, note Eq. (dZos)), dZ_W = -Sigma_T^WW'(MW^2), and the*)
(*counterterms of the parameters: (i) MS-bar: dg/g = (Delta/2) beta_g/g with K beta_g = -(19/6) g^3, and dV of Eq. (dV)*)
(*(Eq. (Vrun)); (ii) Denner-Sack: dV^DS of Eq. (dVds) in place of the MS-bar dV; (iii) on shell (for FormCalc): dg/g ->*)
(*dZ_e - dsw/sw (Thomson limit, MW and MZ on shell) and dV^DS.  FR, HL, HR come from the vertex alone.*)
(*  (a) exact UV finiteness of the MS-bar FL for the six channels (rational unitary V, symbolic masses, couplings and*)
(*      gauge parameters); the UV pole of dV^DS equals that of dV; control without the off-diagonal dZ;*)
(*      FR, HL, HR (vertex only): free of xiA, and their xiZ, xiW dependence (MA -> 0) is of order D - 4 (exact);*)
(*  (b) gauge independence of FL, FR, HL, HR (MS-bar) at the benchmark (LoopTools, mu = MZ), with the size of the*)
(*      gauge dependence of the pieces, and the gauge dependence of the Denner-Sack amplitude: set I, xiA varied with*)
(*      the photon mass MA = 1, 1/10, 1/100 GeV; set II, xiZ and xiW varied with xiA = 1 and MA -> 0 (LoopTools'*)
(*      lambda in the IR-divergent integrals); set IIh, set II with m_u, m_d ten times larger; set III, set II with a*)
(*      photon mass instead (it breaks the cancellation of the xiZ, xiW dependence);*)
(*  (c) Feynman gauge, MA -> 0 (IR divergences regulated by LoopTools' lambda): the relative virtual correction*)
(*      2 Re(M0^* M1)/|M0|^2 (vertex, counterterms with the on-shell scheme) and the renormalization constants, for*)
(*      the comparison with FormCalc (wud_formcalc.wl); at the benchmark and with m_u, m_d ten times larger.*)
(*Complex loop integrals are kept in (a), (b) (no Re-tilde: the gauge cancellation holds for the analytic functions);*)
(*(c) takes the real part of the loop integrals in the renormalization constants as FormCalc does.*)
(*Writes results/wud_numeric.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file wud_renormalized.wl  (run oneloop_ckm_feyncalc.wl and wud_vertex_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


srcDirWR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirWR$ = FileNameJoin[{srcDirWR$, "results"}];
workDirWR$ = FileNameJoin[{srcDirWR$, "work"}];
t0WR$ = AbsoluteTime[];
chansWR$ = Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1];
chanNameWR$[{i_, j_}] := {"u", "c"}[[i]] <> {"d", "s", "b"}[[j]];
(* rename A0, B0, C0 at once: LoopTools' functions would shadow them (environment, SM2) *)
renWR$ = {A0 -> fA0$, B0 -> fB0$, C0 -> fC0$};
vtxWR$ = Association[Table[ch -> (Get[FileNameJoin[{workDirWR$, "wud_vertex_" <> ToString[ch[[1]]] <> ToString[ch[[2]]] <> ".m"}]]["F"] /. renWR$),
    {ch, chansWR$}]];
sig3WR$ = Association[Get[FileNameJoin[{resDirWR$, "oneloop_ckm_sigma.m"}]]] /. renWR$;
smSigWR$ = Association[Get[FileNameJoin[{ParentDirectory[srcDirWR$], "..", "sm", "Src", "results", "oneloop_sigma.m"}]]] /. renWR$;
KK = 16 Pi^2;
kRuleWR$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
(* step (3) wrote V_ij as vR + I vI: the same entries as cK, cKc *)
toCKWR$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
upMWR$ = {MU, MC, MT}; dnMWR$ = {MD, MS, MB};
(* the self-energies (1PI + tadpole) as functions of kk2, electroweak part *)
sgWR$[sec_, i_, j_, n_] := Total[sig3WR$[sec][[i, j, All, n]]] /. kRuleWR$ /. toCKWR$ /. gS -> 0;
Print["gluon C0 left after gS = 0 (expect False): ", ! FreeQ[Table[sgWR$[s, i, j, n], {s, {"U", "D"}}, {i, 3}, {j, 3}, {n, 4}], PaVe]];


(* ::Section:: *)
(*Field renormalization constants, counterterms and the amplitude*)


(* K dZ^L of Denner, on shell (no Re-tilde here; it is applied in (c)) *)
dZLWR$[sec_, i_, j_] := Module[{ms = If[sec === "U", upMWR$, dnMWR$], mi, mj, sl, sr, ss},
   mi = ms[[i]]; mj = ms[[j]];
   {sl, sr, ss} = sgWR$[sec, i, j, #] & /@ {1, 2, 3};
   If[i =!= j,
    2/(mi^2 - mj^2) (mj^2 sl + mi mj sr + (mi^2 + mj^2) ss) /. kk2 -> mj^2,
    (-sl - mi^2 D[sl + sr + 2 ss, kk2]) /. kk2 -> mi^2]];
dZuLWR$ = Table[dZLWR$["U", i, j], {i, 3}, {j, 3}];
dZdLWR$ = Table[dZLWR$["D", i, j], {i, 3}, {j, 3}];
dZWWR$ = -D[Total[sig3WR$["WW"]] /. kRuleWR$ /. toCKWR$, kk2] /. kk2 -> MW^2;
(* hermitian conjugate of the couplings (the loop functions are real for these external quarks, no threshold) *)
hermWR$[m_] := Transpose[m /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b]];
vMWR$ = Array[cK, {3, 3}]; vMcWR$ = Array[cKc, {3, 3}];
vevWR$ = 2 MW sw/ee; yWR$[m_] := Sqrt[2] m/vevWR$;
gSqWR$ = ee^2/sw^2;
(* MS-bar counterterms, K times: dg/g = (Delta/2)(-19/6) g^2, dV = (Delta/2) dV/dln mu (Eq. (Vrun)); Delta <-> 1/ep *)
kdgWR$ = -19/12 gSqWR$/ep;
kdVdlnmuWR$ = Module[{yu = yWR$ /@ upMWR$, yd = yWR$ /@ dnMWR$, hd, hu, au, ad},
   hd = vMWR$ . DiagonalMatrix[yd^2] . Transpose[vMcWR$]; hu = Transpose[vMcWR$] . DiagonalMatrix[yu^2] . vMWR$;
   au = Table[If[i == k, 0, -3/2 (yu[[i]]^2 + yu[[k]]^2)/(yu[[k]]^2 - yu[[i]]^2) hd[[i, k]]], {i, 3}, {k, 3}];
   ad = Table[If[k == j, 0, -3/2 (yd[[k]]^2 + yd[[j]]^2)/(yd[[j]]^2 - yd[[k]]^2) hu[[k, j]]], {k, 3}, {j, 3}];
   -au . vMWR$ + vMWR$ . ad];
kdVmsWR$ = kdVdlnmuWR$/(2 ep);
kdVdsWR$[zu_, zd_] := 1/4 ((zu - hermWR$[zu]) . vMWR$ - vMWR$ . (zd - hermWR$[zd]));
offWR$[m_] := Table[If[i == j, 0, m[[i, j]]], {i, 3}, {j, 3}];
diaWR$[m_] := m - offWR$[m];
(* the pieces of K FL^(1) for channel {i, j}; each multiplies the structure ubar epsslash P_L v *)
piecesWR$[{i_, j_}] := <|
   "vertex" -> cK[i, j] vtxWR$[{i, j}][[1]],
   "W leg" -> cK[i, j] dZWWR$/2,
   "u legs, diagonal" -> (hermWR$[diaWR$[dZuLWR$]] . vMWR$)[[i, j]]/2,
   "d legs, diagonal" -> (vMWR$ . diaWR$[dZdLWR$])[[i, j]]/2,
   "u legs, off-diagonal" -> (hermWR$[offWR$[dZuLWR$]] . vMWR$)[[i, j]]/2,
   "d legs, off-diagonal" -> (vMWR$ . offWR$[dZdLWR$])[[i, j]]/2,
   "dg (MS-bar)" -> cK[i, j] kdgWR$,
   "dV (MS-bar)" -> kdVmsWR$[[i, j]]|>;
pcWR$ = Association[Table[ch -> piecesWR$[ch], {ch, chansWR$}]];
kFLmsWR$[ch_] := Total[Values[pcWR$[ch]]];
Print["pieces built;  ", Round[AbsoluteTime[] - t0WR$], " s"];


(* ::Section:: *)
(*(a) UV finiteness (exact)*)


(* coefficient of 1/eps: A0(m^2) -> m^2/eps, B0 -> 1/eps, B0' and C0 finite, D = 4 - 2 eps *)
poleWR$[x_] := SeriesCoefficient[x /. {fA0$[m2_] :> m2/ep, fB0$[__] -> 1/ep, Derivative[1, 0, 0][fB0$][__] -> 0,
      fC0$[__] -> 0} /. D -> 4 - 2 ep, {ep, 0, -1}];
vStdWR$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
(* rational sines and cosines and the phase ph = e^{i delta} as a symbol (step (4)): zero is decided exactly *)
angPyWR$ = {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5};
vPyWR$ = vStdWR$ /. angPyWR$ /. Exp[I dl] -> ph /. Exp[-I dl] -> 1/ph;
vPycWR$ = vStdWR$ /. angPyWR$ /. Exp[I dl] -> 1/ph /. Exp[-I dl] -> ph;
explicitWR$ = {cK[i_, j_] :> vPyWR$[[i, j]], cKc[i_, j_] :> vPycWR$[[i, j]]};
simpWR$[x_] := Simplify[Together[x /. explicitWR$ /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2]], 0 < sw < 1 && MW > 0];
uvMsWR$ = Table[simpWR$[poleWR$[kFLmsWR$[ch]]], {ch, chansWR$}];
Print["(a) MS-bar: UV pole of K FL for the six channels (expect all 0): ", uvMsWR$, ";  ", Round[AbsoluteTime[] - t0WR$], " s"];
uvDsWR$ = Union[Flatten[simpWR$[poleWR$[#]] & /@ (kdVdsWR$[dZuLWR$, dZdLWR$] - kdVmsWR$)]];
Print["(a) UV pole of K dV^DS - K dV (MS-bar), 9 entries (expect {0}): ", uvDsWR$];
uvNoOffWR$ = Table[simpWR$[poleWR$[kFLmsWR$[ch] - pcWR$[ch]["u legs, off-diagonal"] - pcWR$[ch]["d legs, off-diagonal"]]], {ch, chansWR$}];
Print["(a) control without the off-diagonal dZ: channels with a UV pole left (expect 6): ", Count[uvNoOffWR$, x_ /; x =!= 0]];
xiPoleWR$ = Table[Module[{p = poleWR$[#]}, simpWR$[D[p, #2]]] & @@@ {{pcWR$[ch]["vertex"], xiW}, {pcWR$[ch]["d legs, diagonal"], xiW}},
   {ch, chansWR$}];
Print["(a) the xiW dependence of the UV poles of the vertex and of the diagonal d legs (expect nonzero): ",
  Count[Flatten[xiPoleWR$], x_ /; x =!= 0], " of ", Length[Flatten[xiPoleWR$]]];


(* ::Section:: *)
(*(b) Gauge independence at the benchmark*)


muWR$ = 91;
benchWR$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000,
   MMU -> 1027/10000, Me -> 487/1000000};
vNumWR$ = N[vStdWR$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 30];
vRulesWR$ = {cK[i_, j_] :> vNumWR$[[i, j]], cKc[i_, j_] :> Conjugate[vNumWR$[[i, j]]]};
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.]; SetMudim[N[muWR$^2]];
(* {pole, finite part} of a number-valued expression; the finite part is MS-bar at mu (LoopTools with Delta = 0) *)
laurWR$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
       Derivative[1, 0, 0][fB0$][pp_, a_, b_] :> db0f$[pp, a, b], fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep},
   {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
(* re = True: real part of the loop integrals (Re-tilde) *)
loopValWR$[x_, re_] := Module[{f = If[re, Re, Identity]},
   x /. {a0f$[m2_] :> If[m2 == 0, 0, f[m2 (1 - Log[m2/muWR$^2])]], b0f$[pp_, a_, b_] :> f[LoopTools`B0[pp, a, b]],
     db0f$[pp_, a_, b_] :> f[LoopTools`DB0[pp, a, b]], c0f$[a__] :> f[LoopTools`C0[a]]}];
numWR$[x_, xis_, ma_, re_ : False] := Module[{l = laurWR$[N[x /. vRulesWR$ /. benchWR$ /. xis /. MA -> ma, 30]]},
   {l[[1]], loopValWR$[l[[2]], re]}];
sfWR$[x_, n_ : 3] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
rowsWR$ = {};
addWR$[name_, val_] := AppendTo[rowsWR$, {name, ToString[CForm[N[Re[val]]]], ToString[CForm[N[Im[val]]]]}];

lamWR$ = 1.;   (* lambda^2 of LoopTools: the photon mass squared in the IR-divergent integrals (MA -> 0 only) *)
SetLambda[lamWR$];
(* A photon mass breaks the gauge invariance of the W sector at O(MA^2): the identities that cancel the xiW and xiZ
   dependence contain the photon inverse propagator, whose mass term no vertex supplies.  The check has three parts:
     set I:   xiA varied, xiZ = xiW = 1, photon mass MA = 1 GeV (no IR divergence; the xiA parts cancel by the
              Ward identity of the electric charge, for any MA);
     set II:  xiZ, xiW varied, xiA = 1, MA -> 0 with LoopTools' lambda in the IR-divergent integrals (these come
              with gauge-independent coefficients only: soft photons between the external legs);
     set III: as set II but with the photon mass MA = 1, 1/10, 1/100 GeV (the O(MA^2) breaking). *)
(* xiA = 1, then MA -> 0 coefficient by coefficient of the loop functions; no 1/MA may be left *)
limitWR$[x_] := Module[{y = x /. xiA -> 1, fs, cs, c0},
   fs = Union[Cases[y, fA0$[__] | fB0$[__] | fC0$[__] | Derivative[1, 0, 0][fB0$][__], Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   If[! FreeQ[Denominator /@ Append[cs, c0], MA], Print["   WARNING: 1/MA left after xiA = 1"]];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {fA0$[0] -> 0, fB0$[0, 0, 0] -> 0}];
exFullWR$ = <|"vtx" -> vtxWR$, "zu" -> dZuLWR$, "zd" -> dZdLWR$, "zW" -> dZWWR$|>;
exLimWR$ = <|"vtx" -> Map[limitWR$, vtxWR$, {2}], "zu" -> Map[limitWR$, dZuLWR$, {2}], "zd" -> Map[limitWR$, dZdLWR$, {2}],
   "zW" -> limitWR$[dZWWR$]|>;
Print["(b) the photon-mass limit taken (xiA = 1);  ", Round[AbsoluteTime[] - t0WR$], " s"];
(* after MA -> 0 the xiZ, xiW dependence of FR, HL, HR is of order D - 4: zero in four dimensions, including the rational
   terms from the UV poles.  Exact: the eps^0 coefficient of X(xi) - X(1), as a combination of the finite parts of the
   loop functions, has only zero coefficients. *)
xiFree4WR$[x_] := Module[{d = (x - (x /. {xiZ -> 1, xiW -> 1})) /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2], y, fs},
   y = SeriesCoefficient[d /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
        fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep, {ep, 0, 0}];
   fs = Union[Cases[y, _a0f$ | _b0f$ | _c0f$, Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   {! FreeQ[d, xiZ | xiW], And @@ ((Simplify[Together[Coefficient[y, lf$[#]]], 0 < sw < 1] === 0) & /@ Range[Length[fs]]) &&
     Simplify[Together[y /. lf$[_] -> 0], 0 < sw < 1] === 0}];
Print["(b) K FR, K HL, K HR free of xiA (symbolic, with the photon mass; expect True): ",
  FreeQ[Table[vtxWR$[ch][[2 ;; 4]], {ch, chansWR$}], xiA]];
xiFreeChkWR$ = Table[xiFree4WR$ /@ exLimWR$["vtx"][ch][[2 ;; 4]], {ch, chansWR$}];
Print["(b) after MA -> 0: K FR, K HL, K HR contain xiZ, xiW in D dimensions (expect True): ", And @@ Flatten[xiFreeChkWR$[[All, All, 1]]],
  ";  their xi dependence vanishes in four dimensions (exact; expect True): ", And @@ Flatten[xiFreeChkWR$[[All, All, 2]]],
  ";  the same for K FL of the vertex (expect False): ", Union[Table[xiFree4WR$[exLimWR$["vtx"][ch][[1]]][[2]], {ch, chansWR$}]]];

offNWR$[m_] := Table[If[i == j, 0, m[[i, j]]], {i, 3}, {j, 3}];
(* {pole, finite} of each piece of K FL^(1), and of K FR, K HL, K HR; the quark dZ used here have real loop integrals
   (checked below), so that their hermitian conjugate is ConjugateTranspose *)
piecesFromWR$[{i_, j_}, vert_, zu_, zd_, zw_] := Module[{v = vNumWR$},
   <|"FL" -> <|
      "vertex" -> vert[[1]],
      "W leg" -> v[[i, j]] zw/2,
      "u legs, diagonal" -> Table[(ConjugateTranspose[zu[[All, All, c]] - offNWR$[zu[[All, All, c]]]] . v)[[i, j]]/2, {c, 2}],
      "d legs, diagonal" -> Table[(v . (zd[[All, All, c]] - offNWR$[zd[[All, All, c]]]))[[i, j]]/2, {c, 2}],
      "u legs, off-diagonal" -> Table[(ConjugateTranspose[offNWR$[zu[[All, All, c]]]] . v)[[i, j]]/2, {c, 2}],
      "d legs, off-diagonal" -> Table[(v . offNWR$[zd[[All, All, c]]])[[i, j]]/2, {c, 2}],
      "dg (MS-bar)" -> {N[-19/12 gSqWR$ /. benchWR$, 30] v[[i, j]], 0},
      "dV (MS-bar)" -> {N[(kdVdlnmuWR$/2)[[i, j]] /. vRulesWR$ /. benchWR$, 30], 0}|>,
    "FR,HL,HR" -> Rest[vert]|>];
(* all channels for one gauge set and photon mass; also K dV^DS (finite part, Re-tilde) *)
evalSetWR$[ex_, xis_, ma_, bench_ : benchWR$] := Block[{benchWR$ = bench}, Module[{zu, zd, zw, zuR, zdR},
   zu = Map[numWR$[#, xis, ma] &, ex["zu"], {2}]; zd = Map[numWR$[#, xis, ma] &, ex["zd"], {2}];
   zw = numWR$[ex["zW"], xis, ma];
   zuR = Map[numWR$[#, xis, ma, True][[2]] &, ex["zu"], {2}]; zdR = Map[numWR$[#, xis, ma, True][[2]] &, ex["zd"], {2}];
   Join[Association[Table[ch -> piecesFromWR$[ch, numWR$[cK[ch[[1]], ch[[2]]] #, xis, ma] & /@ ex["vtx"][ch], zu, zd, zw],
       {ch, chansWR$}]],
    <|"dVDS" -> 1/4 ((zuR - ConjugateTranspose[zuR]) . vNumWR$ - vNumWR$ . (zdR - ConjugateTranspose[zdR])),
     "imZ" -> Max[Abs[Im[Flatten[{zu[[All, 1 ;; 2, 2]] - zuR[[All, 1 ;; 2]], zd[[All, All, 2]] - zdR}]]]]|>]]];
xiSetWR$[a_, z_, w_] := {xiA -> a, xiZ -> z, xiW -> w};
setsWR$ = <|
   "I" -> {exFullWR$, {1, 1/10, 1/100}, {xiSetWR$[1, 1, 1], xiSetWR$[1/2, 1, 1], xiSetWR$[3, 1, 1], xiSetWR$[10, 1, 1]}},
   "II" -> {exLimWR$, {0}, {xiSetWR$[1, 1, 1], xiSetWR$[1, 2, 3], xiSetWR$[1, 1/3, 1/2], xiSetWR$[1, 5, 10]}},
   "III" -> {exFullWR$, {1, 1/10, 1/100}, {xiSetWR$[1, 1, 1], xiSetWR$[1, 2, 3]}},
   (* set II with m_u, m_d ten times larger: the residual of the u channels in set II is the double precision of
      LoopTools with m_u^2/MW^2 = 2.5e-10 (gauge independence holds for any masses) *)
   "IIh" -> {exLimWR$, {0}, {xiSetWR$[1, 1, 1], xiSetWR$[1, 2, 3], xiSetWR$[1, 1/3, 1/2], xiSetWR$[1, 5, 10]},
     benchWR$ /. {(MU -> x_) :> (MU -> 10 x), (MD -> x_) :> (MD -> 10 x)}}|>;
evalWR$ = Association[Flatten[Table[With[{st = setsWR$[name]},
      Table[{name, ma, n} -> evalSetWR$[st[[1]], st[[3, n]], ma, If[Length[st] > 3, st[[4]], benchWR$]], {ma, st[[2]]},
       {n, Length[st[[3]]]}]], {name, Keys[setsWR$]}]]];
Print["(b) evaluated;  ", Round[AbsoluteTime[] - t0WR$], " s"];
Print["(b) imaginary part of the loop integrals in the quark dZ that enter (max over all sets; expect 0): ",
  sfWR$[Max[#["imZ"] & /@ Values[evalWR$]]]];
Print["(b) max |UV pole| of K FL (total, MS-bar) and of K FR, K HL, K HR over all sets and channels (expect ~1e-14): ",
  sfWR$[Max[Flatten[Table[Abs[Total[Values[e[ch]["FL"]]][[1]]], {e, Values[evalWR$]}, {ch, chansWR$}]]]], ", ",
  sfWR$[Max[Flatten[Table[Abs[e[ch]["FR,HL,HR"][[All, 1]]], {e, Values[evalWR$]}, {ch, chansWR$}]]]]];

finFLWR$[e_] := Total[Values[e["FL"]]][[2]];
absVWR$[{i_, j_}] := Abs[vNumWR$[[i, j]]];
(* max over the gauge sets of |X(xi) - X(reference)|; FL and its pieces relative to K |V_ij|, FR, HL, HR to |X| *)
spreadWR$[name_, ma_, f_] := Module[{nx = Length[setsWR$[name][[3]]]},
   Max[Table[Abs[f[evalWR$[{name, ma, n}]] - f[evalWR$[{name, ma, 1}]]], {n, 2, nx}]]];
keysWR$ = Keys[evalWR$[{"I", 1, 1}][chansWR$[[1]]]["FL"]];
cleanKeyWR$[s_] := StringReplace[s, {", " -> "_", " " -> "_", "(" -> "", ")" -> "", "-" -> ""}];
tagWR$[name_, ma_] := "set" <> name <> If[MemberQ[{"II", "IIh"}, name], "", "_MA" <> ToString[N[ma]]];
Do[With[{st = setsWR$[name]},
   Print["(b) set ", name, ": ", Rest[st[[3]]], " against ", st[[3, 1]], ";  photon mass ",
     If[MemberQ[{"II", "IIh"}, name], "0 (lambda)", N[st[[2]]]], If[name === "IIh", ";  m_u, m_d x 10", ""]];
   Do[Module[{fl, ffs, pcs, ds},
      fl = spreadWR$[name, ma, finFLWR$[#[ch]] &]/absVWR$[ch]/KK;
      ffs = Table[With[{m = m}, spreadWR$[name, ma, #[ch]["FR,HL,HR"][[m, 2]] &]/Abs[evalWR$[{name, ma, 1}][ch]["FR,HL,HR"][[m, 2]]]], {m, 3}];
      pcs = Table[With[{key = key}, spreadWR$[name, ma, #[ch]["FL"][key][[2]] &]/absVWR$[ch]/KK], {key, keysWR$}];
      (* the Denner-Sack amplitude: FL^DS = FL^MS - dV + dV^DS *)
      ds = spreadWR$[name, ma, finFLWR$[#[ch]] + #["dVDS"][[ch[[1]], ch[[2]]]] &]/absVWR$[ch]/KK;
      Print["   ", chanNameWR$[ch], If[MemberQ[{"I", "III"}, name], " (MA = " <> ToString[N[ma]] <> ")", ""], ":  FL MS-bar ", sfWR$[fl],
        ",  FL Denner-Sack ", sfWR$[ds], " (/|V_ij|);  FR, HL, HR ", sfWR$ /@ ffs, " (relative);  pieces (/|V_ij|) ",
        StringRiffle[MapThread[#1 <> " " <> sfWR$[#2] &, {keysWR$[[1 ;; 6]], pcs[[1 ;; 6]]}], ", "]];
      addWR$["xi_spread_FL_MSbar_" <> tagWR$[name, ma] <> "_" <> chanNameWR$[ch], fl];
      addWR$["xi_spread_FL_DS_" <> tagWR$[name, ma] <> "_" <> chanNameWR$[ch], ds];
      Do[addWR$["xi_spread_" <> {"FR", "HL", "HR"}[[m]] <> "_" <> tagWR$[name, ma] <> "_" <> chanNameWR$[ch], ffs[[m]]], {m, 3}];
      Do[addWR$["xi_spread_piece_" <> cleanKeyWR$[keysWR$[[m]]] <> "_" <> tagWR$[name, ma] <> "_" <> chanNameWR$[ch], pcs[[m]]],
        {m, 6}]],
     {ma, st[[2]]}, {ch, chansWR$}]], {name, Keys[setsWR$]}];

(* the MS-bar one-loop FL / V_ij in Feynman gauge (MA -> 0, lambda^2 = 1 GeV^2; IR sensitive, for orientation) *)
Do[addWR$["FL1_over_V_MSbar_Feynman_" <> chanNameWR$[ch],
   finFLWR$[evalWR$[{"II", 0, 1}][ch]]/vNumWR$[[ch[[1]], ch[[2]]]]/KK], {ch, chansWR$}];


(* ::Section:: *)
(*(c) Feynman gauge, MA -> 0, on-shell scheme: the numbers for FormCalc*)


fgWR$[x_] := limitWR$[x] /. {xiZ -> 1, xiW -> 1};
num0WR$[x_, re_ : False] := numWR$[x, {xiZ -> 1, xiW -> 1}, 0, re];
(* the on-shell charge and mixing-angle counterterms from this note's model: dZ_e = (1/2) Sigma^AA'(0) +
   (sw/cw) Sigma^AZ(0)/MZ^2 (A = -A_Denner), dsw/sw = -(cw^2/(2 sw^2)) Re[Sigma^WW(MW^2)/MW^2 - Sigma^ZZ(MZ^2)/MZ^2].
   Sigma^AA, Sigma^AZ at k^2 -> 0 from the expansion of B0 in k^2 (closed forms, as in oneloop_ckm_numeric.wl). *)
dnB0WR$[n_, a_, b_] := Which[a == b, (n!)^2/((2 n + 1)! n a^n),
   n == 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, NIntegrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}, WorkingPrecision -> 30]/n];
smallKWR$[x_, order_] := Module[{y = fgWR$[x /. kRuleWR$] /. benchWR$, s},
   y = y /. fB0$[kk_, a_, b_] /; ! FreeQ[kk, kk2] :> fB0$[0, a, b] + kk dnB0$[1, a, b] + kk^2 dnB0$[2, a, b];
   y = y /. {fA0$[m2_] :> m2 (1/ep + 1 - Log[m2/muWR$^2]), fB0$[0, a_, b_] :> If[a == b, 1/ep - Log[a/muWR$^2],
         1/ep + 1 - (a Log[a/muWR$^2] - b Log[b/muWR$^2])/(a - b)], dnB0$[n_, a_, b_] :> dnB0WR$[n, a, b]} /. D -> 4 - 2 ep;
   s = Normal[Series[N[y, 30], {kk2, 0, order}]];
   {SeriesCoefficient[Coefficient[s, kk2, order], {ep, 0, -1}], SeriesCoefficient[Coefficient[s, kk2, order], {ep, 0, 0}]}];
(* 2 Re(M0^* M1)/|M0|^2 from the form factors: sum over spins and W polarizations (wud_vertex_feyncalc.wl (d)) *)
ratioWR$[{i_, j_}] := Module[{a = upMWR$[[i]], b = dnMWR$[[j]], s = MW^2, pp, kp1, kp2, t0},
   pp = (s - a^2 - b^2)/2; kp1 = a^2 + pp; kp2 = b^2 + pp; t0 = 2 (pp + 2 kp1 kp2/s);
   N[{1, 6 a b/t0, 2 a (-pp + kp1 kp2/s)/t0, -2 b (-a^2 + kp1^2/s)/t0} /. benchWR$, 30]];
(* everything of (c) for one set of masses; sfx is appended to the names in the output (FormCalc does the same) *)
onShellWR$[bench_, sfx_] := Block[{benchWR$ = bench}, Module[{kAAp, kAZ0, kWW, kZZ, swN, cwN, mwN, mzN, kdZe, kdsw, zuOS,
     zdOS, zWOS, dVds, rows},
   kAAp = smallKWR$[Total[smSigWR$["AA"]], 1];
   kAZ0 = smallKWR$[Total[smSigWR$["AZ"]], 0];
   kWW = numWR$[fgWR$[Total[sig3WR$["WW"]] /. kRuleWR$ /. toCKWR$ /. kk2 -> MW^2], {}, 0, True];
   kZZ = numWR$[fgWR$[Total[smSigWR$["ZZ"]] /. kRuleWR$ /. kk2 -> MZ^2], {}, 0, True];
   {swN, cwN, mwN, mzN} = N[{sw, cw, MW, MZ} /. benchWR$, 30];
   kdZe = kAAp/2 + swN/cwN kAZ0/mzN^2;
   kdsw = -cwN^2/(2 swN^2) (kWW/mwN^2 - kZZ/mzN^2);
   Print["(c)", sfx, " on-shell K (dZ_e - dsw/sw): pole ", sfWR$[Re[kdZe[[1]] - kdsw[[1]]], 6], ",  finite ",
     sfWR$[Re[kdZe[[2]] - kdsw[[2]]], 10]];
   addWR$["K_dZe_minus_dsw_over_sw_fin" <> sfx, kdZe[[2]] - kdsw[[2]]];
   (* renormalization constants with Re-tilde: dZ^L (u, d), dZ_W, dV^DS; {pole, finite} *)
   zuOS = Map[num0WR$[#, True] &, exLimWR$["zu"], {2}];
   zdOS = Map[num0WR$[#, True] &, exLimWR$["zd"], {2}];
   zWOS = num0WR$[exLimWR$["zW"], True];
   Do[addWR$["K_dZuL_" <> ToString[a] <> ToString[b] <> sfx, zuOS[[a, b, 2]]];
     addWR$["K_dZdL_" <> ToString[a] <> ToString[b] <> sfx, zdOS[[a, b, 2]]], {a, 3}, {b, 3}];
   addWR$["K_dZW" <> sfx, zWOS[[2]]];
   dVds = Module[{vn = vNumWR$, zu = zuOS[[All, All, 2]], zd = zdOS[[All, All, 2]]},
     1/4 ((zu - ConjugateTranspose[zu]) . vn - vn . (zd - ConjugateTranspose[zd]))];
   Do[addWR$["K_dVDS_" <> ToString[a] <> ToString[b] <> sfx, dVds[[a, b]]], {a, 3}, {b, 3}];
   rows = Table[Module[{i = ch[[1]], j = ch[[2]], v, r, vert, ct, zu, zd},
      v = vNumWR$[[i, j]]; r = ratioWR$[ch];
      vert = num0WR$[cK[i, j] #][[2]] & /@ exLimWR$["vtx"][ch];
      zu = zuOS[[All, All, 2]]; zd = zdOS[[All, All, 2]];
      ct = v ((kdZe[[2]] - kdsw[[2]]) + zWOS[[2]]/2) + dVds[[i, j]] +
        ((ConjugateTranspose[zu] . vNumWR$)[[i, j]] + (vNumWR$ . zd)[[i, j]])/2;
      {chanNameWR$[ch], 2 Re[Conjugate[v] (vert . r)]/Abs[v]^2/KK, 2 Re[Conjugate[v] ct]/Abs[v]^2/KK}], {ch, chansWR$}];
   Print["(c)", sfx, " Feynman gauge, lambda^2 = ", lamWR$, " GeV^2, mu = MZ: 2 Re(M0^* M1)/|M0|^2 of the vertex and of the",
     " on-shell counterterms:"];
   Scan[(Print["   ", #[[1]], ":  vertex ", sfWR$[#[[2]], 10], ",  counterterms ", sfWR$[#[[3]], 10], ",  sum ",
        sfWR$[#[[2]] + #[[3]], 10]];
      addWR$["delta_vertex_" <> #[[1]] <> sfx, #[[2]]]; addWR$["delta_ct_OS_" <> #[[1]] <> sfx, #[[3]]]) &, rows]]];
(* the benchmark, and m_u, m_d ten times larger (the double precision of the u-quark integrals, as set IIh) *)
onShellWR$[benchWR$, ""];
onShellWR$[benchWR$ /. {(MU -> x_) :> (MU -> 10 x), (MD -> x_) :> (MD -> 10 x)}, "_h"];


(* ::Section:: *)
(*Output*)


Export[FileNameJoin[{resDirWR$, "wud_numeric.csv"}], Prepend[rowsWR$, {"quantity", "re", "im"}], "CSV"];
Print["Summary (expect all 0, {0}, 6): MS-bar UV ", Union[uvMsWR$], ", dV^DS - dV UV ", uvDsWR$, ", control ",
  Count[uvNoOffWR$, x_ /; x =!= 0], ";  total ", Round[AbsoluteTime[] - t0WR$], " s"];
