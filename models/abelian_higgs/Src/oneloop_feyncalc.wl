(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop tadpole and two-point functions in a general R_xi gauge with FeynArts + FeynCalc (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (3).  Uses the FeynArts model of this note (Src/generated/AbelianHiggs_FA,*)
(*propagators with GaugeXi[A], ghost-h coupling with the same symbol), at particle level.*)
(*  (a) the tadpole T against Eq. (T), exact in D;*)
(*  (b) the 1PI two-point functions Sigma^H, Sigma_T, Sigma_L, Sigma^AG, Sigma^GG, Sigma^c and the diagrams with the*)
(*      tadpole attached through a zero-momentum h line, against Eq. (se) and App. D (exact in D); Sigma^H diagram by*)
(*      diagram against Table seh;*)
(*  (c) the Slavnov-Taylor identity p^2 Sigma_L - 2 MA p^2 Sigma^AG - MA^2 Sigma^GG = 0 (and -MA^2 T/v without the*)
(*      tadpole-attached diagrams), Sigma^GG(0) = 0, d Sigma_T/d xi = 0, the xi dependence of Sigma^H;*)
(*  (d) the UV poles against Eq. (uv), and finiteness with the counterterms (ctse), (ct);*)
(*  (e) results/oneloop_sigma.m for oneloop_numeric.wl.*)
(*Conventions (note Eq. (Gamma2)): the product of Feynman rules is i Sigma^H, -i[(g - kk/k^2) Sigma_T + kk/k^2 Sigma_L],*)
(*k_mu Sigma^AG (G in, A out), i Sigma^GG, i Sigma^c, i T.  FeynArts' CreateFeynAmp returns that product divided by i;*)
(*FCFAConvert supplies 1/(2 pi)^4 and TID i pi^2 times the LoopTools-normalized A0, B0, so K x (FeynArts amplitude)*)
(*(K = 16 pi^2) is a combination of A0, B0 with D kept.*)
(*CreateFeynAmp[..., GaugeRules -> {}] keeps GaugeXi: the FeynArts default {_GaugeXi -> 1} is Feynman gauge.*)
(*Tadpole-attached diagrams: FeynArts also inserts G and A lines between the tadpole loop and the two-point vertex;*)
(*their one-point loops vanish (C and Lorentz invariance) and they are checked to be 0.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (about 1 minute).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resDirOL$]];
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "AbelianHiggs_FA"}], FileNameJoin[{modelTmpDirOL$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "AbelianHiggs_FA"}], Quiet -> True];
modelFileOL$ = FileNameJoin[{modelTmpDirOL$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];


(* ::Text:: *)
(*Field codes: V[1] = A, S[1] = h, S[2] = G, U[1] = ghost.  Everything is written in MA, MH, v and xi:*)
(*EL -> ee -> MA/v, vev -> v, lam -> MH^2/(2 v^2).*)


convOL$ = {FCGV["EL"] -> MA/v, FCGV["MA"] -> MA, FCGV["MH"] -> MH, GaugeXi[A] -> xi, GaugeXi[V[1, ___]] -> xi,
   GaugeXi[S[2, ___]] -> xi, GaugeXi[U[1, ___]] -> xi, GaugeXi[S[1, ___]] -> 1, vev -> v, lam -> MH^2/(2 v^2)};

insertOL$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles},
    Model -> modelFileOL$, GenericModel -> modelFileOL$], RuleDelayed::rhs];
convertOL$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
       DropSumOver -> True], RuleDelayed::rhs];
   (* the zero-momentum h propagator of the tadpole-attached diagrams is the number 1/(0 - MH^2) *)
   a /. convOL$ /. FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2];

(* reduction to A0, B0 with D kept; FDS first (repeated denominators) *)
reduceOL$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[Contract[r], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r = r /. {A0[0] -> 0, B0[0, 0, 0] -> 0} /. {Pair[Momentum[k, ___], Momentum[k, ___]] -> p2, SPD[k, k] -> p2} /.
     B0[pp_, a_, b_] :> B0[pp /. {Pair[Momentum[k, ___], Momentum[k, ___]] -> p2, SPD[k, k] -> p2}, a, b];
   Simplify[r]];

KK = (4 Pi)^2;
uvOL$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep, {ep, 0, -1}]];
lK$[a_, b_, c_] := a^2 + b^2 + c^2 - 2 a b - 2 b c - 2 c a;
eeN$ = MA/v;

topsT$ = CreateTopologies[1, 1 -> 0];
topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
topsTad$ = Complement[CreateTopologies[1, 1 -> 1], topsOPI$];


(* ::Section:: *)
(*(a) Tadpole*)


diagsT$ = insertOL$[topsT$, {S[1]} -> {}];
ampsT$ = convertOL$[CreateFeynAmp[diagsT$, GaugeRules -> {}], {}, {}];
Print["(a) tadpole diagrams (expect 4: h, G, A, ghost): ", Length[ampsT$]];
tDiag$ = Simplify[KK reduceOL$[#]] & /@ ampsT$;
tOL$ = Simplify[Total[tDiag$]];
tNote$ = 1/v ((D - 1) MA^2 A0[MA^2] + 3/2 MH^2 A0[MH^2] + MH^2/2 A0[xi MA^2]);
dT$ = Simplify[tOL$ - tNote$];
Print["(a) K T (FeynCalc) - Eq. (T), exact in D (expect 0): ", dT$];
Print["(a) diagrams (K T, App. D: h, G, A (U+X), ghost): ", InputForm /@ tDiag$];


(* ::Section:: *)
(*(b) Two-point functions*)


(* proc, external momentum k; returns {list of K x (1PI diagrams), list of K x (tadpole-attached diagrams with the h line)}
   after the projection proj (a function of the FeynCalc amplitude) *)
twoPoint$[proc_, proj_] := Module[{d1, a1, dT, faT, isH, keep, drop, aK, aD, r1, rT, rD},
   d1 = insertOL$[topsOPI$, proc];
   a1 = convertOL$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   dT = insertOL$[topsTad$, proc];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   isH = ! FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &;
   keep = Select[List @@ faT, isH]; drop = Select[List @@ faT, ! isH[#] &];
   aK = If[keep === {}, {}, convertOL$[faT[[0]] @@ keep, {k}, {k}]];
   aD = If[drop === {}, {}, convertOL$[faT[[0]] @@ drop, {k}, {k}]];
   r1 = Simplify[KK reduceOL$[proj[#]]] & /@ a1;
   rT = Simplify[KK reduceOL$[proj[#]]] & /@ aK;
   rD = Simplify[KK reduceOL$[proj[#]]] & /@ aD;
   Print["   ", proc, ": 1PI diagrams ", Length[a1], ", tadpole-attached with the h line ", Length[aK],
     ", with a G or A line ", Length[aD], " (their sum, expect 0: ", Simplify[Total[rD]], ")"];
   {r1, rT}];

pT$[x_] := Contract[-1/(D - 1) (MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]) x];
pL$[x_] := Contract[-FVD[k, mu] FVD[k, nu]/SPD[k, k] x];
pAG$[x_] := Contract[I FVD[k, mu] x/SPD[k, k]];

FCClearScalarProducts[];
Print["(b) h self-energy"];   sH$ = twoPoint$[{S[1]} -> {S[1]}, Identity];
Print["(b) A self-energy, T"]; sT$ = twoPoint$[{V[1]} -> {V[1]}, pT$];
Print["(b) A self-energy, L"]; sL$ = twoPoint$[{V[1]} -> {V[1]}, pL$];
Print["(b) G -> A mixing"];   sAG$ = twoPoint$[{S[2]} -> {V[1]}, pAG$];
Print["(b) G self-energy"];   sGG$ = twoPoint$[{S[2]} -> {S[2]}, Identity];
Print["(b) ghost self-energy"]; sC$ = twoPoint$[{U[1]} -> {U[1]}, Identity];

tot$[s_] := Simplify[Total[s[[1]]] + Total[s[[2]]]];
noteH$ = 1/v^2 (1/2 (4 (D - 1) MA^4 - 4 MA^2 p2 + p2^2) B0[p2, MA^2, MA^2] + 9/2 MH^4 B0[p2, MH^2, MH^2] -
     (2 (D - 1) MA^2 + p2) A0[MA^2] - 3 MH^2 A0[MH^2] + (p2 - MH^2) (A0[xi MA^2] - (p2 + MH^2)/2 B0[p2, xi MA^2, xi MA^2]));
noteT$ = eeN$^2/((D - 1) p2) ((lK$[p2, MA^2, MH^2] + 4 (D - 1) MA^2 p2) B0[p2, MA^2, MH^2] - (p2 + MA^2 - MH^2) A0[MA^2] -
      ((2 D - 1) p2 - MA^2 + MH^2) A0[MH^2]) - 2 (D - 1) eeN$^2 MA^2/MH^2 A0[MA^2];
noteL$ = eeN$^2/p2 (-lK$[p2, MA^2, MH^2] B0[p2, MA^2, MH^2] + (p2 + MA^2 - MH^2) A0[MA^2] - (3 p2 + MA^2 - MH^2) A0[MH^2]) +
   eeN$^2 (p2 - 2 MH^2 + 2 xi MA^2) B0[p2, MH^2, xi MA^2] - 2 eeN$^2 A0[xi MA^2] - 2 (D - 1) eeN$^2 MA^2/MH^2 A0[MA^2];
noteAG$ = eeN$^2/(MA p2) (-lK$[p2, MA^2, MH^2] B0[p2, MA^2, MH^2] + (p2 + MA^2 - MH^2) A0[MA^2] -
      (3/2 p2 + MA^2 - MH^2) A0[MH^2]) + eeN$^2/MA (p2 - 2 MH^2 + xi MA^2) B0[p2, MH^2, xi MA^2] -
   3 eeN$^2/(2 MA) A0[xi MA^2] - (D - 1) eeN$^2 MA/MH^2 A0[MA^2];
noteGG$ = 1/v^2 (lK$[p2, MA^2, MH^2] B0[p2, MA^2, MH^2] + p2 (2 MH^2 - p2) B0[p2, MH^2, xi MA^2] -
     (p2 + MA^2 - MH^2) A0[MA^2] + (MA^2 - MH^2) A0[MH^2] + p2 A0[xi MA^2]);
noteC$ = xi^2 eeN$^2 MA^2 B0[p2, MH^2, xi MA^2];

(* B0 is symmetric in its masses; FeynCalc may write either order *)
symB0$ = B0[pp_, a_, b_] :> B0[pp, Sequence @@ Sort[{a, b}]];
diffOL$[x_] := Simplify[x /. symB0$];
resB$ = {
   "Sigma^H" -> diffOL$[tot$[sH$] - noteH$],
   "Sigma_T" -> diffOL$[tot$[sT$] - noteT$],
   "Sigma_L" -> diffOL$[tot$[sL$] - noteL$],
   "Sigma^AG" -> diffOL$[tot$[sAG$] - noteAG$],
   "Sigma^GG" -> diffOL$[tot$[sGG$] - noteGG$],
   "Sigma^c (1PI)" -> diffOL$[Total[sC$[[1]]] - noteC$],
   "Sigma^c tadpole part + xi MA^2 Dv/v" -> diffOL$[Total[sC$[[2]]] + xi MA^2/v tNote$/MH^2]};
Scan[Print["(b) ", #[[1]], ": FeynCalc - note = ", #[[2]], "   (expect 0)"] &, resB$];


(* ::Text:: *)
(*Sigma^H diagram by diagram (Table seh): every FeynArts diagram must equal one group of the table (the A A bubble*)
(*is the sum of the UU, UX + XU and XX rows, the A G bubble the sum of its U and X rows).*)


tableSeh$ = 1/v^2 {
   9/2 MH^4 B0[p2, MH^2, MH^2],
   1/2 MH^4 B0[p2, xi MA^2, xi MA^2],
   1/2 (4 (D - 1) MA^4 - 4 MA^2 p2 + p2^2) B0[p2, MA^2, MA^2] - p2 A0[MA^2] +
     (MA^2 - xi MA^2 + p2) A0[MA^2] - (MA^2 + 3 xi MA^2 - p2) A0[xi MA^2] - lK$[p2, MA^2, xi MA^2] B0[p2, MA^2, xi MA^2] +
     1/2 (2 xi MA^2 - p2)^2 B0[p2, xi MA^2, xi MA^2] + (4 xi MA^2 - p2) A0[xi MA^2],
   -(MA^2 - xi MA^2 + p2) A0[MA^2] + MA^2 A0[xi MA^2] + lK$[p2, MA^2, xi MA^2] B0[p2, MA^2, xi MA^2] -
     (xi MA^2 - p2)^2 B0[p2, xi MA^2, xi MA^2] - (2 xi MA^2 - p2) A0[xi MA^2],
   -xi^2 MA^4 B0[p2, xi MA^2, xi MA^2],
   3/2 MH^2 A0[MH^2], 1/2 MH^2 A0[xi MA^2], (D - 1) MA^2 A0[MA^2] + xi MA^2 A0[xi MA^2]};
labelsSeh$ = {"(d) hh", "(d) GG", "(e) AA", "(f) AG", "(g) ghost", "(h) h seagull", "(h) G seagull", "(h) A seagull"};
matchSeh$ = Table[Module[{hits = Select[Range[Length[sH$[[1]]]], diffOL$[sH$[[1, #]] - tableSeh$[[i]]] === 0 &]},
    {labelsSeh$[[i]], hits}], {i, Length[tableSeh$]}];
Print["(b) Sigma^H, FeynArts diagram matching each row group of Table seh (expect one each, all different): ", matchSeh$];
Print["(b) Sigma^H, tadpole-attached part + 3 T/v (expect 0): ", diffOL$[Total[sH$[[2]]] + 3 tNote$/v]];


(* ::Section:: *)
(*(c) Slavnov-Taylor identity and gauge dependence*)


stFull$ = diffOL$[p2 tot$[sL$] - 2 MA p2 tot$[sAG$] - MA^2 tot$[sGG$]];
st1PI$ = diffOL$[p2 Total[sL$[[1]]] - 2 MA p2 Total[sAG$[[1]]] - MA^2 Total[sGG$[[1]]] + MA^2 tNote$/v];
Print["(c) p^2 Sigma_L - 2 MA p^2 Sigma^AG - MA^2 Sigma^GG (expect 0): ", stFull$];
Print["(c) the same with the 1PI parts only, + MA^2 T/v (expect 0): ", st1PI$];
gg0$ = Simplify[(tot$[sGG$] /. p2 -> 0) /. B0[0, a_, b_] /; a =!= b :> (A0[a] - A0[b])/(a - b)];
Print["(c) Sigma^GG(0) (expect 0): ", gg0$];
Print["(c) d Sigma_T/d xi (expect 0): ", Simplify[D[tot$[sT$] /. A0[x_] :> a0F[x] /. B0[x__] :> b0F[x], xi]]];
xiH$ = Simplify[tot$[sH$] - (tot$[sH$] /. xi -> 1) /. symB0$];
Print["(c) Sigma^H(xi) - Sigma^H(1) is proportional to (p^2 - MH^2): ", Simplify[(xiH$ /. p2 -> MH^2)] === 0];
Print["(c) Sigma_T, xi dependence of the 1PI part alone: ", Simplify[D[Total[sT$[[1]]] /. A0[x_] :> a0F[x], xi]]];


(* ::Section:: *)
(*(d) UV poles and counterterms*)


lamN$ = MH^2/(2 v^2);
uvNote$ = {
   "T" -> (6 MA^4 + 3 MH^4 + xi MA^2 MH^2)/(2 v),
   "Sigma^H" -> (xi - 3) eeN$^2 p2 + MH^2 (2 MH^2 - xi MA^2)/v^2,
   "Sigma_T" -> eeN$^2/3 p2 - MA^2 (6 lamN$ - 3 eeN$^2 + 3 eeN$^4/lamN$),
   "Sigma_L" -> -MA^2 (6 lamN$ - 3 eeN$^2 + 3 eeN$^4/lamN$),
   "Sigma^AG" -> -MA/2 (6 lamN$ - 6 eeN$^2 + 3 eeN$^4/lamN$ + xi eeN$^2),
   "Sigma^GG" -> (xi - 3) eeN$^2 p2,
   "Sigma^c" -> xi^2 eeN$^2 MA^2};
uvGot$ = {"T" -> uvOL$[tOL$], "Sigma^H" -> uvOL$[tot$[sH$]], "Sigma_T" -> uvOL$[tot$[sT$]], "Sigma_L" -> uvOL$[tot$[sL$]],
   "Sigma^AG" -> uvOL$[tot$[sAG$]], "Sigma^GG" -> uvOL$[tot$[sGG$]], "Sigma^c" -> uvOL$[Total[sC$[[1]]]]};
resD$ = Table[Simplify[(name /. uvGot$) - (name /. uvNote$)], {name, First /@ uvNote$}];
Print["(d) UV poles (K x Delta coefficient) - Eq. (uv) (expect all 0): ", Thread[(First /@ uvNote$) -> resD$]];
(* counterterms (ct), (ctse): K x Delta coefficients *)
dZA$ = -eeN$^2/3; dZPhi$ = (3 - xi) eeN$^2; dm2$ = 4 lamN$ - 3 eeN$^2; dlam$ = 10 lamN$ - 6 eeN$^2 + 3 eeN$^4/lamN$;
ctse$ = {"Sigma^H" -> dZPhi$ (p2 - MH^2) - dm2$ MH^2, "Sigma_T" -> dZA$ p2 - (dm2$ - dlam$) MA^2,
   "Sigma_L" -> -(dm2$ - dlam$) MA^2, "Sigma^AG" -> -1/2 (dZPhi$ + dm2$ - dlam$) MA, "Sigma^GG" -> dZPhi$ p2};
resCt$ = Table[Simplify[(name /. uvGot$) + (name /. ctse$)], {name, First /@ ctse$}];
Print["(d) UV poles + counterterms (expect all 0): ", Thread[(First /@ ctse$) -> resCt$]];


(* ::Section:: *)
(*(e) Output for oneloop_numeric.wl*)


Put[{"T" -> tOL$, "TDiagrams" -> tDiag$, "H" -> sH$, "T2" -> sT$, "L" -> sL$, "AG" -> sAG$, "GG" -> sGG$, "C" -> sC$},
  FileNameJoin[{resDirOL$, "oneloop_sigma.m"}]];
Print["Summary (expect all 0): tadpole ", dT$, ", two-point ", Last /@ resB$, ", ST ", {stFull$, st1PI$},
  ", Sigma^GG(0) ", gg0$, ", UV ", resD$, ", UV + ct ", resCt$];
