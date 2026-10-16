(* ::Package:: *)

(* ::Title:: *)
(*Step (6): checks of the one-loop muon decay (results/mudecay_deltahat.m), without FeynCalc (SM note)*)


(* ::Text:: *)
(*The quantities are K times Sigma^WW(0)/MW^2, dV, dB, dWF in A0(m^2), B0(0, a, b), DB0(0, a, b) and D (K = 16 pi^2).*)
(*Exact closed forms of the vacuum integrals (MS-bar, Delta -> 1/eps):*)
(*  A0(m^2) = m^2 (1/eps + 1 - ln(m^2/mu^2)),   B0(0, a, b) = 1/eps + 1 - (a ln(a/mu^2) - b ln(b/mu^2))/(a - b),*)
(*  B0(0, a, a) = 1/eps - ln(a/mu^2),  B0(0, 0, b) = 1/eps + 1 - ln(b/mu^2),  DB0(0, a, b) = (a^2 - b^2 - 2 a b ln(a/b))/(2 (a - b)^3).*)
(*  (a) UV pole of the bracket = (K/2) dln v^2/dln mu (Eq. (vrun));  (b) no ln MA as MA -> 0;  (c) the finite part DeltaHat*)
(*  does not depend on xiA, xiZ, xiW;  (d) Feynman gauge: K (dV + dB + dWF) = (e^2/sw^2)[4 B0(0, MW^2, MW^2) + 6 +*)
(*  (7 - 4 sw^2)/(2 sw^2) ln cw^2] to O(eps^0);  (e) DeltaHat at the benchmark and its parts.*)
(*All masses are positive, so the logarithms are split (PowerExpand) and the coefficients of the independent logarithms*)
(*are simplified with Together (a plain Simplify of the whole expression takes hours).*)
(*Writes results/mudecay_numeric.csv.  Batch: wolframscript -file mudecay_check.wl*)


srcDirMC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
mu$ = Association[Get[FileNameJoin[{srcDirMC$, "results", "mudecay_deltahat.m"}]]];
KK = 16 Pi^2;
toSw$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];

closed$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]),
   B0[0, 0, 0] -> 0,
   B0[0, a_, a_] :> 1/ep - Log[a/mu^2],
   B0[0, 0, b_] :> 1/ep + 1 - Log[b/mu^2], B0[0, b_, 0] :> 1/ep + 1 - Log[b/mu^2],
   B0[0, a_, b_] :> 1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b),
   DB0[0, 0, b_] :> 1/(2 b), DB0[0, b_, 0] :> 1/(2 b), DB0[0, a_, a_] :> 1/(6 a),
   DB0[0, a_, b_] :> (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3)};
(* logarithms of positive quantities -> sums of Log[mass], Log[xi], Log[1 - sw^2] (no Factor: it would write
   1 - sw^2 as -(-1 + sw)(1 + sw) and PowerExpand would then give i pi) *)
logRule$ = Log[x_] :> PowerExpand[Log[x]];
canon$[x_] := Module[{y = Expand[x /. logRule$], ls},
   ls = Union[Cases[y, _Log, Infinity]];
   If[ls === {}, Together[y], Collect[y, ls, Together]]];
laur$[x_] := Module[{y = toSw$[x] /. closed$ /. D -> 4 - 2 ep},
   canon$ /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
isZero$[x_] := canon$[x] === 0;

parts$ = <|"W" -> mu$["sigW0"]/MW^2, "V" -> mu$["dV"], "B" -> mu$["dB"], "WF" -> mu$["dWF"]|>;
lp$ = laur$ /@ parts$;
br$ = canon$ /@ Total[Values[lp$]];


(* ::Section:: *)
(*(a) UV pole*)


vev$ = 2 MW sw/ee;
gSq$ = ee^2/sw^2; gpSq$ = ee^2/(1 - sw^2); lam$ = MH^2/(2 vev$^2);
yf$[m_] := Sqrt[2] m/vev$;
(* the leptons of the process (e, mu) are massless; the other fermions keep their masses *)
ups$ = {{MU, MD}, {MC, MS}, {MT, MB}}; leps$ = {MTA};
TT$ = Sum[3 yf$[p[[1]]]^2 + 3 yf$[p[[2]]]^2, {p, ups$}] + Sum[yf$[m]^2, {m, leps$}];
NY4$ = Sum[3 yf$[p[[1]]]^4 + 3 yf$[p[[2]]]^4, {p, ups$}] + Sum[yf$[m]^4, {m, leps$}];
dlnv2K$ = -12 lam$ - 2 TT$ + 9/2 gSq$ + 3/2 gpSq$ + 2/lam$ NY4$ - 3/(8 lam$) (2 gSq$^2 + (gSq$ + gpSq$)^2);
(* the photon mass is a soft breaking: the poles carry MA^2/MW^2 terms, which vanish as MA -> 0 *)
uvAll$ = canon$[br$[[1]] - dlnv2K$/2];
uvRes$ = canon$[uvAll$ /. MA -> 0];
Print["(a) UV pole of K (Sigma^W(0)/MW^2 + dV + dB + dWF) - (K/2) dln v^2/dln mu at MA -> 0 = ", uvRes$,
  "   (expect 0, independent xi's);  the MA^2 terms: ", Factor[uvAll$]];
Print["    UV poles of the parts (W, V, B, WF): ", Factor[#[[1]]] & /@ Values[lp$]];


(* ::Section:: *)
(*(b), (c) photon mass and gauge independence of the finite part*)


(* coefficients of Log[MA] and the rest, then MA -> 0 *)
fin$ = br$[[2]];
cLogMA$ = Together[Coefficient[fin$, Log[MA]]];
restMA$ = canon$[fin$ /. Log[MA] -> 0];
leadLogMA$ = Normal[Series[cLogMA$, {MA, 0, 0}]];
Print["(b) coefficient of ln MA as MA -> 0 (expect 0): ", Together[leadLogMA$]];
dHat$ = canon$[Normal[Series[restMA$, {MA, 0, 0}]]];
Print["(b) MA left in the limit (expect False): ", !FreeQ[dHat$, MA]];
Print["(c) d(DeltaHat)/d xiA, xiZ, xiW vanish (expect True, True, True): ", isZero$[D[dHat$, #]] & /@ {xiA, xiZ, xiW}];
(* also each part separately: which ones depend on the gauge *)
finParts$ = AssociationMap[canon$[Normal[Series[lp$[#][[2]], {MA, 0, 0}]]] &, Keys[lp$]];
Print["    parts with ln MA (W, V, B, WF): ", !FreeQ[finParts$[#], Log[MA]] & /@ Keys[finParts$]];
Print["    parts depending on xiW (W, V, B, WF): ", !isZero$[D[finParts$[#], xiW]] & /@ Keys[finParts$]];


(* ::Section:: *)
(*(d) Feynman gauge*)


feyn$ = {xiA -> 1, xiZ -> 1, xiW -> 1};
vbwPole$ = canon$[Total[lp$[#][[1]] & /@ {"V", "B", "WF"}] /. feyn$];
vbwFin$ = canon$[Total[finParts$ /@ {"V", "B", "WF"}] /. feyn$];
sirlin$ = gSq$ {4, -4 Log[MW^2/mu^2] + 6 + (7 - 4 sw^2)/(2 sw^2) Log[1 - sw^2]};
Print["(d) Feynman gauge, K (dV + dB + dWF) - (e^2/sw^2)[4 B0(0, MW, MW) + 6 + (7 - 4 sw^2)/(2 sw^2) ln cw^2]: pole ",
  canon$[vbwPole$ - sirlin$[[1]]], ", finite ", canon$[vbwFin$ - sirlin$[[2]]], "   (expect 0, 0)"];


(* ::Section:: *)
(*(e) numbers at the benchmark*)


bench$ = {ee -> Sqrt[4 Pi/128], MW -> 80, sw -> Sqrt[1 - 80^2/91^2], MH -> 125, MT -> 165, MB -> 286/100,
   MC -> 619/1000, MS -> 546/10000, MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000, mu -> 91};
dHatN$ = N[N[dHat$/KK /. bench$, 20]];
(* the box and the external legs have ln MA separately; their sum does not *)
partsN$ = N[N[{finParts$["W"], finParts$["V"], canon$[finParts$["B"] + finParts$["WF"]]}/KK /. feyn$ /. bench$, 20]];
sirlinN$ = N[N[sirlin$[[2]]/KK /. bench$, 20]];
Print["(e) DeltaHat at the benchmark (mu = MZ, any gauge) = ", ToString[NumberForm[dHatN$, 10]]];
Print["    Feynman-gauge parts Sigma^W(0)/MW^2, V, B + WF: ", partsN$, ";  sum ", Total[partsN$],
  ";  Sirlin's V + B + WF: ", sirlinN$];
Export[FileNameJoin[{srcDirMC$, "results", "mudecay_numeric.csv"}],
  {{"quantity", "value"}, {"DeltaHat_benchmark", ToString[CForm[dHatN$]]},
   {"part_SigmaW0_over_MW2_feynman", ToString[CForm[partsN$[[1]]]]}, {"part_vertex_feynman", ToString[CForm[partsN$[[2]]]]},
   {"part_box_plus_wf_feynman", ToString[CForm[partsN$[[3]]]]}, {"sirlin_vbwf", ToString[CForm[sirlinN$]]}}, "CSV"];
Put[dHat$, FileNameJoin[{srcDirMC$, "results", "mudecay_deltahat_finite.m"}]];
Print["Summary: ", {uvRes$, Together[leadLogMA$], isZero$[D[dHat$, #]] & /@ {xiA, xiZ, xiW},
   canon$[vbwFin$ - sirlin$[[2]]]}];
