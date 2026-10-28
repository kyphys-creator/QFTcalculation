(* ::Package:: *)

(* ::Title:: *)
(*Step (3): MS-bar finite parts, pole masses and the optical theorem of the abelian Higgs model, without FeynCalc*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (K x the tadpole and the two-point functions from oneloop_feyncalc.wl, in A0, B0 with D*)
(*kept; K = 16 pi^2), at the benchmark of the note (MA = 1, MH = 5/2, v = 2, mu = 1).*)
(*  (a) MS-bar finite parts of Sigma^H(MH^2) and Sigma_T(MA^2) (1PI part and tadpole part) and the one-loop pole masses*)
(*      M_p^2 = M^2 - Re Sigma(M^2) at xi = 0, 1/2, 1, 3, 10, with the B0 values of Package-X (40 digits);*)
(*  (b) the optical theorem Im Sigma^H(MH^2)/MH = Gamma(h -> A A) of Eq. (width);*)
(*  (c) off-shell: Sigma^H(p^2 = 1) depends on xi, Sigma_T(p^2 = 4) does not;*)
(*  (d) the same B0 from LoopTools (MathLink) and COLLIER (results/oneloop_collier_b0.csv from oneloop_collier.f90,*)
(*      written for the list results/oneloop_b0_args.csv), and the pole masses with them;*)
(*  (e) results/oneloop_numeric.csv.*)
(*Finite parts: A0(m^2) = m^2/eps + A0fin, B0 = 1/eps + B0fin, D = 4 - 2 eps, eps^0 coefficient (the D-dependent*)
(*coefficients make the rational terms); A0fin = m^2 (1 - ln(m^2/mu^2)), B0fin = the value with Delta = 0.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_numeric.wl  (run_oneloop_check.sh runs it twice, before and after*)
(*COLLIER).  The LoopTools link prints "libc++abi: terminating ... MathLink::MLException" when the kernel exits; the*)
(*results are written before that.*)


(* ::Section:: *)
(*Setup*)


srcDirON$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirON$ = FileNameJoin[{srcDirON$, "results"}];
sig$ = Association[Get[FileNameJoin[{resDirON$, "oneloop_sigma.m"}]]];
(* printed numbers without precision marks *)
$NumberMarks = False;
KK = 16 Pi^2;
bench$ = {MA -> 1, MH -> 5/2, v -> 2};
muON$ = 1;
xiSet$ = {0, 1/2, 1, 3, 10};

(* the FeynCalc symbols A0, B0 were written with their context; read them as plain symbols here *)
plain$[x_] := x /. {s_Symbol /; SymbolName[s] === "A0" :> A0, s_Symbol /; SymbolName[s] === "B0" :> B0};
sig$ = Map[plain$, sig$];

finON$[x_] := Module[{y = x /. A0[m2_] :> If[PossibleZeroQ[m2], 0, m2/ep + a0f[m2]] /. B0[p2_, a_, b_] :> 1/ep + b0f[p2, a, b] /.
      D -> 4 - 2 ep},
   SeriesCoefficient[Series[y, {ep, 0, 0}], 0]];
(* {1PI part, tadpole part} of K Sigma at p2 for a given xi *)
partsON$[key_, pp_, xv_] := Module[{s = sig$[key]},
   {finON$[Total[s[[1]]] /. p2 -> pp /. xi -> xv /. bench$], finON$[Total[s[[2]]] /. p2 -> pp /. xi -> xv /. bench$]}];

rawFin$ = Association[Flatten[Table[{
      {"H", xv} -> partsON$["H", 25/4, xv],
      {"T2", xv} -> partsON$["T2", 1, xv],
      {"Hoff", xv} -> partsON$["H", 1, xv],
      {"T2off", xv} -> partsON$["T2", 4, xv]}, {xv, xiSet$}]]];
argsB0$ = Union[Cases[Values[rawFin$], b0f[__], Infinity]];
argsA0$ = Union[Cases[Values[rawFin$], a0f[__], Infinity]];
Print["distinct B0 and A0 arguments: ", Length[argsB0$], ", ", Length[argsA0$]];
Export[FileNameJoin[{resDirON$, "oneloop_b0_args.csv"}],
  Prepend[N[List @@@ argsB0$, 20] /. x_Real :> CForm[x], {"p2", "m1sq", "m2sq"}], "CSV"];
a0Val$[x_] := N[x (1 - Log[x/muON$^2]), 40];

(* Package-X: LoopRefine of PVB[0, 0, p2, m1, m2] (masses, not squares) minus its 1/eps pole, mu = muON$ *)
Get["X`"];
pxB0$[{pp_, a_, b_}] := Module[{r = LoopRefine[PVB[0, 0, pp, Sqrt[a], Sqrt[b]]]},
   r = r /. {sy_Symbol /; SymbolName[sy] === "Eps" :> Infinity} /. {sy_Symbol /; SymbolName[sy] === "Mu" :> muON$};
   N[r, 40]];
pxVals$ = Association[(# -> pxB0$[List @@ #]) & /@ argsB0$];
evalWith$[expr_, vals_] := N[expr /. a0f[x_] :> a0Val$[x] /. b0f[x__] :> vals[b0f[x]], 30];


(* ::Section:: *)
(*(a) finite parts and pole masses (Package-X)*)


rowsON$ = {};
poleOf$[vals_, xv_] := Module[{h = evalWith$[Total[rawFin$[{"H", xv}]], vals], t = evalWith$[Total[rawFin$[{"T2", xv}]], vals]},
   {Sqrt[25/4 - Re[h]/KK], Sqrt[1 - Re[t]/KK]}];
Do[Module[{h = evalWith$[#, pxVals$] & /@ rawFin$[{"H", xv}], t = evalWith$[#, pxVals$] & /@ rawFin$[{"T2", xv}], pm},
    pm = poleOf$[pxVals$, xv];
    Print["(a) xi = ", xv, ": Re Sigma^H(MH^2)/MH^2 1PI ", N[Re[h[[1]]]/KK/(25/4), 10], ", tadpole ", N[Re[h[[2]]]/KK/(25/4), 10],
      ", sum ", N[Re[Total[h]]/KK/(25/4), 16], ";  Re Sigma_T(MA^2) 1PI ", N[Re[t[[1]]]/KK, 10], ", tadpole ", N[Re[t[[2]]]/KK, 10],
      ", sum ", N[Re[Total[t]]/KK, 16]];
    Print["      pole masses M_h,p = ", N[pm[[1]], 16], ", M_A,p = ", N[pm[[2]], 16],
      ";  with the 1PI part only: ", N[Sqrt[25/4 - Re[h[[1]]]/KK], 10], ", ", N[Sqrt[1 - Re[t[[1]]]/KK], 10]];
    AppendTo[rowsON$, {xv, Re[h[[1]]]/KK, Re[h[[2]]]/KK, Re[t[[1]]]/KK, Re[t[[2]]]/KK, pm[[1]], pm[[2]]}]],
  {xv, xiSet$}];
(* a difference that is 0 to the working precision is printed as 0 *)
zero$[x_] := If[x == 0, 0, N[x, 3]];
spread$[i_] := zero$[Max[#[[i]] & /@ rowsON$] - Min[#[[i]] & /@ rowsON$]];
Print["(a) spread over xi of M_h,p and M_A,p (expect 0 to the working precision): ", {spread$[6], spread$[7]},
  ";  of the 1PI parts of Re Sigma^H/K and Re Sigma_T/K: ", {spread$[2], spread$[4]}];


(* ::Section:: *)
(*(b) optical theorem*)


imH$ = Im[evalWith$[Total[rawFin$[{"H", 1}]], pxVals$]]/KK/(5/2);
gamma$ = N[(1/2)^2 (5/2)^3/(32 Pi) (3/5) (1 - 4 (4/25) + 12 (4/25)^2), 30];
Print["(b) Im Sigma^H(MH^2)/MH = ", N[imH$, 20], ",  Gamma(h -> A A) of Eq. (width) = ", N[gamma$, 20],
  ",  rel. diff ", zero$[imH$/gamma$ - 1]];
Print["(b) the same at xi = 10 (MH^2 > 4 xi MA^2 is false; at xi = 1/2 the xi-dependent B0 has a cut): ",
  N[Im[evalWith$[Total[rawFin$[{"H", 10}]], pxVals$]]/KK/(5/2), 20], ", ", N[Im[evalWith$[Total[rawFin$[{"H", 1/2}]], pxVals$]]/KK/(5/2), 20]];


(* ::Section:: *)
(*(c) off shell*)


offH$ = Table[N[Re[evalWith$[Total[rawFin$[{"Hoff", xv}]], pxVals$]], 12], {xv, xiSet$}];
offT$ = Table[N[Re[evalWith$[Total[rawFin$[{"T2off", xv}]], pxVals$]], 12], {xv, xiSet$}];
Print["(c) K Re Sigma^H(p^2 = 1) at xi = ", xiSet$, ": ", offH$];
Print["(c) K Re Sigma_T(p^2 = 4) at xi = ", xiSet$, ": ", offT$];


(* ::Section:: *)
(*(d) LoopTools and COLLIER*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[N[muON$^2]]; SetDelta[0.];
ltVals$ = Association[(# -> (LoopTools`B0 @@ N[List @@ #])) & /@ argsB0$];
colFile$ = FileNameJoin[{resDirON$, "oneloop_collier_b0.csv"}];
colVals$ = If[FileExistsQ[colFile$],
   Association[MapThread[#1 -> #2[[4]] + I #2[[5]] &, {argsB0$, Rest[Import[colFile$, "CSV"]]}]], None];
relLib$[vals_] := Max[Abs[(Values[vals] - Values[pxVals$])/Values[pxVals$]]];
Print["(d) B0 (", Length[argsB0$], " values): max relative difference LoopTools - Package-X ", N[relLib$[ltVals$], 3],
  If[colVals$ =!= None, Row[{",  COLLIER - Package-X ", N[relLib$[colVals$], 3]}], "  (COLLIER not run yet)"]];
pmPX$ = poleOf$[pxVals$, 1]; pmLT$ = poleOf$[ltVals$, 1];
Print["(d) pole masses at xi = 1: Package-X ", N[pmPX$, 16], ",  LoopTools - Package-X ", N[pmLT$ - pmPX$, 3],
  If[colVals$ =!= None, Row[{",  COLLIER - Package-X ", N[poleOf$[colVals$, 1] - pmPX$, 3]}], ""]];


(* ::Section:: *)
(*(e) output*)


Export[FileNameJoin[{resDirON$, "oneloop_numeric.csv"}],
  Join[{{"xi", "ReSigmaH_1PI", "ReSigmaH_tadpole", "ReSigmaT_1PI", "ReSigmaT_tadpole", "MH_pole", "MA_pole"}},
    Map[If[NumericQ[#], CForm[N[#, 17]], #] &, rowsON$, {2}],
    {{"ImSigmaH_over_MH", CForm[N[imH$, 17]], "Gamma_h_AA", CForm[N[gamma$, 17]]},
     {"pole_masses_lt_xi1", CForm[N[pmLT$[[1]], 17]], CForm[N[pmLT$[[2]], 17]]}}], "CSV"];
Print["(e) written ", FileNameJoin[{resDirON$, "oneloop_numeric.csv"}]];
