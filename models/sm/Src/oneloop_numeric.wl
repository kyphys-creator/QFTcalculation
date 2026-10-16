(* ::Package:: *)

(* ::Title:: *)
(*Step (3): k^2 structure of the UV poles and MS-bar finite parts of the self-energies (SM note), without FeynCalc*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (K Sigma from oneloop_feyncalc.wl, in A0, B0 with D kept; K = 16 pi^2).*)
(*  (a) UV poles as functions of k^2 against the symmetric MS-bar field renormalization (note Sec. tadpole):*)
(*        Sigma_T^AA = -dZAA k^2,  Sigma_T^AZ = -(dZAZ/2) k^2 - (dZZA/2)(k^2 - MZ^2),  Sigma_T^ZZ = -dZZZ (k^2 - MZ^2) + dMZ2,*)
(*        Sigma_T^WW = -dZW (k^2 - MW^2) + dMW2,  with  dZW = (g^2/K)(1/6 - xi), dZB = -(41/6)(g'^2/K),*)
(*        dZAA = s^2 dZW + c^2 dZB, dZZZ = c^2 dZW + s^2 dZB, dZZA = 2 s c (dg/g + dZW/2), dZAZ = s c (4 dg'/g' + dZW - 2 dg/g)*)
(*      (coefficients of Delta), first with xiA = xiZ = xiW = xi, then printing what remains for independent xi's;*)
(*  (b) MS-bar finite parts at the benchmark of the note: Sigma(M^2) + tadpole part and the one-loop pole masses*)
(*      M_p^2 = M^2 - Sigma_T(M^2), m_p = m (1 - SigmaV - SigmaS) for W, Z, H, t at xiZ, xiW in {1/3, 1, 2, 3} (xiA = 1,*)
(*      photon mass MA -> 0), with the B0 values of LoopTools, Package-X (30 digits) and COLLIER (results/*)
(*      oneloop_collier_b0.csv from oneloop_collier.f90, written for the list results/oneloop_b0_args.csv);*)
(*  (c) results/oneloop_numeric.csv.*)
(*Finite parts: A0(m^2) = m^2/eps + A0fin, B0 = 1/eps + B0fin, D = 4 - 2 eps, eps^0 coefficient (the D-dependent*)
(*coefficients make the rational terms); A0fin = m^2 (1 - ln(m^2/mu^2)), B0fin = LoopTools' value with Delta = 0.*)


(* ::Section:: *)
(*Setup*)


srcDirON$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirON$ = FileNameJoin[{srcDirON$, "results"}];
sig$ = Association[Get[FileNameJoin[{resDirON$, "oneloop_sigma.m"}]]];
KK = 16 Pi^2;

kk2Rule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
uvON$[x_] := Simplify[SeriesCoefficient[(x /. kk2Rule$) /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep,
     {ep, 0, -1}]];
(* applied in sequence: MZ -> MW/cw introduces cw *)
sw2Rule$ = Dispatch[{MZ -> MW/Sqrt[1 - sw^2], cw -> Sqrt[1 - sw^2]}];
cwS$ = Sqrt[1 - sw^2];
gSq$ = ee^2/sw^2; gpSq$ = ee^2/(1 - sw^2);


(* ::Section:: *)
(*(a) k^2 structure of the UV poles*)


dZW$[xi_] := gSq$ (1/6 - xi); dZB$ = -41/6 gpSq$;
dg$ = -19/12 gSq$; dgp$ = 41/12 gpSq$;
dZAA$[xi_] := sw^2 dZW$[xi] + (1 - sw^2) dZB$;
dZZZ$[xi_] := (1 - sw^2) dZW$[xi] + sw^2 dZB$;
dZZA$[xi_] := 2 sw cwS$ (dg$ + dZW$[xi]/2);
dZAZ$[xi_] := sw cwS$ (4 dgp$ + dZW$[xi] - 2 dg$);
mz2$ = MW^2/(1 - sw^2);
(* dM^2 of the note (K times the Delta coefficient) are the on-shell values already checked in oneloop_feyncalc.wl;
   here only the k^2 dependence and the k^2 = 0 values of the neutral sector are compared *)
uvAA$ = Simplify[uvON$[sig$["AA"][[1]]] /. MA -> 0 /. sw2Rule$];
uvAZ$ = Simplify[uvON$[sig$["AZ"][[1]]] /. MA -> 0 /. sw2Rule$];
uvZZ$ = Simplify[uvON$[Total[sig$["ZZ"]]] /. MA -> 0 /. sw2Rule$];
uvWW$ = Simplify[uvON$[Total[sig$["WW"]]] /. MA -> 0 /. sw2Rule$];
same$ = {xiA -> xx, xiZ -> xx, xiW -> xx};
chkAA$ = Simplify[uvAA$ + dZAA$[xiW] kk2];
chkAZ$ = Simplify[(uvAZ$ + dZAZ$[xx]/2 kk2 + dZZA$[xx]/2 (kk2 - mz2$)) /. same$];
chkZZk$ = Simplify[D[uvZZ$, kk2] + dZZZ$[xx] /. same$];
chkWWk$ = Simplify[D[uvWW$, kk2] + dZW$[xx] /. same$];
Print["(a) Sigma^AA:  UV pole + dZAA(xiW) k^2 = ", chkAA$, "   (expect 0, for independent xiA, xiZ, xiW)"];
Print["(a) Sigma^AZ:  UV pole + dZAZ k^2/2 + dZZA (k^2 - MZ^2)/2 at xiA = xiZ = xiW = xi: ", chkAZ$, "   (expect 0)"];
Print["(a) Sigma^ZZ:  d(UV pole)/dk^2 + dZZZ at equal xi: ", chkZZk$, "   (expect 0)"];
Print["(a) Sigma^WW:  d(UV pole)/dk^2 + dZW at equal xi: ", chkWWk$, "   (expect 0)"];
Print["(a) independent xi's: Sigma^AZ UV pole at k^2 = 0 (K Delta coefficient): ", Simplify[uvAZ$ /. kk2 -> 0],
  ";  d/dk^2 of the W and Z poles: ", Simplify[{D[uvWW$, kk2], D[uvZZ$, kk2]}]];


(* ::Section:: *)
(*(b) finite parts at the benchmark*)


finON$[x_] := Module[{y = (x /. kk2Rule$) /. {A0[m2_] :> m2/ep + a0f[m2], B0[p2_, a_, b_] :> 1/ep + b0f[p2, a, b]} /.
      D -> 4 - 2 ep},
   SeriesCoefficient[Series[y, {ep, 0, 0}], 0]];

bench$ = {ee -> Sqrt[4 Pi/128], MW -> 80, sw -> Sqrt[1 - 80^2/91^2], MH -> 125, MT -> 165, MB -> 286/100,
   MC -> 619/1000, MS -> 546/10000, MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000, MMU -> 1027/10000,
   Me -> 487/1000000, gS -> Sqrt[4 Pi 118/1000], CF -> 4/3, CA -> 3, xiG -> 1};
muON$ = 91;
mBench$ = <|"W" -> 80, "Z" -> 91, "H" -> 125, "T" -> 165|>;

(* the top's gluon loop with xiG keeps C0(0, k^2, k^2; 0, 0, m^2) times (m^2 - k^2)^2 (repeated massless propagator);
   the identity of the QCD note turns it into A0, B0 exactly in D, and the factor cancels before k^2 -> m^2 *)
ibpON$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
(* MS-bar finite part of K Sigma(M^2) (1PI part, tadpole part) for given xiZ, xiW (xiA = 1, MA -> 0) *)
onshellFin$[key_, m_, xz_, xw_] := Module[{s = sig$[key]},
   s = s /. {xiA -> 1, xiZ -> xz, xiW -> xw} /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. bench$;
   s = Map[Together, s /. kk2Rule$ /. ibpON$, {If[key === "TT", 2, 1]}] /. kk2 -> m^2;
   s = Map[finON$, s, {If[key === "TT", 2, 1]}] /. {a0f[x_] :> If[PossibleZeroQ[x /. MA -> 0], 0, a0f[x /. MA -> 0]]} /.
     {b0f[p_, a_, b_] :> b0f[p, a /. MA -> 0, b /. MA -> 0]} /. MA -> 0;
   s];

xiSet$ = {{1/3, 1/3}, {1, 1}, {2, 2}, {3, 3}, {1/3, 3}, {3, 1/3}};
(* exact Feynman gauge has 0/0 in the reduced expressions; xi = 1 is approached as 1 + 10^-20 at 40 digits *)
xiNum$[x_] := If[x === 1, 1 + 10^-20, x];
rawFin$ = Association[Table[{key, xs} -> onshellFin$[key, mBench$[key /. {"WW" -> "W", "ZZ" -> "Z", "HH" -> "H", "TT" -> "T"}],
      xiNum$[xs[[1]]], xiNum$[xs[[2]]]], {key, {"WW", "ZZ", "HH", "TT"}}, {xs, xiSet$}]];

argsB0$ = Union[Cases[Values[rawFin$], b0f[__], Infinity]];
argsA0$ = Union[Cases[Values[rawFin$], a0f[__], Infinity]];
Print["(b) distinct B0 and A0 arguments: ", Length[argsB0$], ", ", Length[argsA0$]];
Export[FileNameJoin[{resDirON$, "oneloop_b0_args.csv"}],
  Prepend[N[List @@@ argsB0$, 20] /. x_Real :> CForm[x], {"p2", "m1sq", "m2sq"}], "CSV"];

a0Val$[x_] := N[x (1 - Log[x/muON$^2]), 40];

(* Package-X: LoopRefine of PVB[0, 0, p2, m1, m2] (masses, not squares) minus its 1/eps pole, mu = muON$ *)
Get["X`"];
(* LoopRefine gives 1/Eps + finite with the scale Mu (Package-X's symbols); the pole is dropped *)
pxB0$[{p2_, a_, b_}] := Module[{r = LoopRefine[PVB[0, 0, p2, Sqrt[a], Sqrt[b]]]},
   r = r /. {sy_Symbol /; SymbolName[sy] === "Eps" :> Infinity} /. {sy_Symbol /; SymbolName[sy] === "Mu" :> muON$};
   N[r, 40]];
pxVals$ = Association[(# -> pxB0$[List @@ #]) & /@ argsB0$];

(* LoopTools (MathLink), double precision; installed after Package-X so that its B0 does not clash *)
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[N[muON$^2]]; SetDelta[0.];
ltVals$ = Association[(# -> (LoopTools`B0 @@ N[List @@ #])) & /@ argsB0$];
ltVals$ = Map[If[NumberQ[#], #, Indeterminate] &, ltVals$];

(* COLLIER values, if oneloop_collier has been run *)
colFile$ = FileNameJoin[{resDirON$, "oneloop_collier_b0.csv"}];
colVals$ = If[FileExistsQ[colFile$],
   Association[MapThread[#1 -> #2[[4]] + I #2[[5]] &, {argsB0$, Rest[Import[colFile$, "CSV"]]}]], None];

worstLib$ = {Max[Abs[(Values[ltVals$] - Values[pxVals$])/Values[pxVals$]]],
   If[colVals$ === None, Missing[], Max[Abs[(Values[colVals$] - Values[pxVals$])/Values[pxVals$]]]]};
Print["(b) B0: max relative difference LoopTools - Package-X, COLLIER - Package-X: ", N[worstLib$, 3]];

evalWith$[expr_, vals_] := N[expr /. a0f[x_] :> a0Val$[x] /. b0f[x__] :> vals[b0f[x]], 30];

rowsON$ = {};
Do[Module[{key = kx[[1]], m = kx[[2]], tag = kx[[3]], v1, vT, vals, line},
    vals = Table[Module[{r = rawFin$[{key, xs}], f1, fT},
        If[key === "TT",
          (* SigmaV + SigmaS: m_p = m (1 - SigmaV - SigmaS) *)
          f1 = evalWith$[r[[1, 1]] + r[[1, 2]], pxVals$]; fT = evalWith$[r[[2, 1]] + r[[2, 2]], pxVals$],
          f1 = evalWith$[r[[1]], pxVals$]; fT = evalWith$[r[[2]], pxVals$]];
        {xs, Re[f1]/KK, Re[fT]/KK}], {xs, xiSet$}];
    Print["(b) ", tag, ": xi_Z, xi_W, Re Sigma 1PI, tadpole part, sum (finite, at k^2 = M^2):"];
    Scan[Print["      ", N[#[[1]], 3], "  ", N[#[[2]], 12], "  ", N[#[[3]], 12], "  ", N[#[[2]] + #[[3]], 16]] &, vals];
    Print["      spread of the sum over the gauges: ", N[Max[#[[2]] + #[[3]] & /@ vals] - Min[#[[2]] + #[[3]] & /@ vals], 3],
      ",  spread of the 1PI part: ", N[Max[#[[2]] & /@ vals] - Min[#[[2]] & /@ vals], 3]];
    Scan[AppendTo[rowsON$, {tag, N[#[[1, 1]]], N[#[[1, 2]]], #[[2]], #[[3]], #[[2]] + #[[3]]}] &, vals]],
  {kx, {{"WW", 80, "W"}, {"ZZ", 91, "Z"}, {"HH", 125, "H"}, {"TT", 165, "t"}}}];

(* pole masses at the benchmark (mu = MZ) from the Feynman-gauge row, and the same with the LoopTools and COLLIER B0 *)
(* xiZ = xiW = 2 for the library comparison: at xi = 1 + 10^-20 the double-precision B0 cannot cancel 1/(1 - xi) *)
poleON$[vals_] := Module[{w, z, h, t},
   w = Sqrt[80^2 - Re[evalWith$[Total[rawFin$[{"WW", {2, 2}}]], vals]]/KK];
   z = Sqrt[91^2 - Re[evalWith$[Total[rawFin$[{"ZZ", {2, 2}}]], vals]]/KK];
   h = Sqrt[125^2 - Re[evalWith$[Total[rawFin$[{"HH", {2, 2}}]], vals]]/KK];
   t = 165 (1 - Re[evalWith$[Total[Flatten[rawFin$[{"TT", {2, 2}}]]], vals]]/KK);
   {w, z, h, t}];
polePX$ = poleON$[pxVals$];
poleLT$ = poleON$[ltVals$];
Print["(b) one-loop pole masses at the benchmark (Package-X): M_W, M_Z, M_H, m_t = ", N[polePX$, 12]];
Print["    LoopTools - Package-X: ", N[poleLT$ - polePX$, 3],
  If[colVals$ =!= None, Row[{",  COLLIER - Package-X: ", N[poleON$[colVals$] - polePX$, 3]}], ""]];

Export[FileNameJoin[{resDirON$, "oneloop_numeric.csv"}],
  Join[{{"particle", "xiZ", "xiW", "ReSigma_1PI_finite", "ReSigma_tadpole_finite", "sum"}},
    rowsON$ /. x_Real :> CForm[x],
    {{"pole_masses_px", Sequence @@ (CForm /@ N[polePX$, 16])}, {"pole_masses_lt", Sequence @@ (CForm /@ N[poleLT$, 16])}}],
  "CSV"];
