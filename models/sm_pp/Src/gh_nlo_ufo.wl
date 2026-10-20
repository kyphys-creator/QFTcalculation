(* ::Package:: *)

(* ::Title:: *)
(*Step (2b), 3 of 3: the NLO UFO of QCDH.fr (NLOCT's QCD counterterms and the note's own g g H vertices)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2b), as the QCD note's nlo_ufo.wl.  The QCD vertices are NLOCT's (the QCD note's, checked there*)
(*against the hand values and DGPP).  NLOCT's vertices with H are not usable: the R2 and UV vertices of g g H keep unevaluated*)
(*Feynman-parameter integrals (Integrate[...]) and the internal momentum, those of q qbar H the internal momentum; g g H H is of order*)
(*kHgg^2.  They are dropped (q qbar H has no tree vertex and does not enter g g -> H at one loop)*)
(*and replaced by the note's own g g H vertices of gh_r2.wl (generated/QCDH_H_CT.m):*)
(*  R2:  i (cHgg/v) g_s^2/(128 pi^2) [-17 k1^2 g - 93 k1.k2 g - 17 k2^2 g + 14 k1^mu k1^nu + k1^mu k2^nu + 89 k2^mu k1^nu + 14 k2^mu k2^nu],*)
(*  UV:  (delta alpha_s/alpha_s) x tree = -beta0 g_s^2/(16 pi^2 eps) x i (cHgg/v)[k1.k2 g - k2^mu k1^nu]   (beta0 = 11 - 2 n_f/3, n_f = 5),*)
(*with cHgg = -(alpha_s/(3 pi)) kHgg, both with the loop particle G only: MadGraph keeps a counterterm only when its loop particles*)
(*appear in the generated loops, and the loops of g g -> H have gluons only (the quark part of delta alpha_s would be dropped, as*)
(*HC_NLO_X0's).  No O(alpha_s) Wilson coefficient: the vertex is the operator's.  The gluon field constant of the on-shell scheme is 0*)
(*(massless).  The tree vertex of FeynRules is checked against gh_r2.wl's.  FeynmanGauge = True (MadGraph's loops need it); the*)
(*decimals NLOCT writes are made exact ratios (MG5 writes 7 digits).  -> generated/QCDH_NLO_UFO.*)
(*Batch:  wolframscript -file gh_nlo_ufo.wl  (gh_r2.wl first)*)


srcDirGU$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirGU$];
LoadModel["QCDH.fr"];
SetDirectory[FileNameJoin[{srcDirGU$, "generated"}]];
Get["QCDH_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist], ";  UV vertices: ",
  Length[UV$vertlist]];
hQ$[v_] := MemberQ[v[[1, All, 1]], H];
Do[If[hQ$[v], Print["NLOCT's ", t, " ", v[[1, All, 1]], " dropped: unevaluated integrals or the internal momentum ",
     !FreeQ[v[[2]], Integrate | FourMomentum[Internal, _]], ", kHgg^2 ", !FreeQ[v[[2]], kHgg^2]]], {t, {"R2", "UV"}},
  {v, If[t === "R2", R2$vertlist, UV$vertlist]}];
r2List$ = DeleteCases[R2$vertlist, _?hQ$];
uvList$ = DeleteCases[UV$vertlist, _?hQ$];


(* ::Section:: *)
(*the own g g H vertices*)


ownGU$ = Get[FileNameJoin[{srcDirGU$, "generated", "QCDH_H_CT.m"}]];
lorGU$[i_] := Index[Lorentz, Ext[i]];
(* gh_r2.wl's basis {g k1^2, g k1.k2, g k2^2, k1^mu k1^nu, k1^mu k2^nu, k2^mu k1^nu, k2^mu k2^nu}: FeynRules' momenta are incoming, FV[i, mu] of leg i *)
basisGU$ = {ME[lorGU$[1], lorGU$[2]] SP[1, 1], ME[lorGU$[1], lorGU$[2]] SP[1, 2], ME[lorGU$[1], lorGU$[2]] SP[2, 2],
   FV[1, lorGU$[1]] FV[1, lorGU$[2]], FV[1, lorGU$[1]] FV[2, lorGU$[2]], FV[2, lorGU$[1]] FV[1, lorGU$[2]], FV[2, lorGU$[1]] FV[2, lorGU$[2]]};
toFRGU$ = {cHgg -> -aS kHgg/(3 Pi), vv -> vev, gS -> gs};
colGU$ = IndexDelta[Index[Gluon, Ext[1]], Index[Gluon, Ext[2]]];
legsGU$ = {{G, 1}, {G, 2}, {H, 3}};
treeFR$ = First[Cases[FeynmanRules[LHggQCDH, ScreenOutput -> False], {lg_, v_} /; lg[[All, 1]] === {G, G, H} :> v]];
Print["tree g g H vertex: FeynRules minus gh_r2.wl's (expect 0): ",
  Simplify[Expand[treeFR$ - colGU$ (ownGU$["tree"] /. toFRGU$) . basisGU$]]];
r2GGH$ = {legsGU$, IPL[{G}] colGU$ Simplify[(ownGU$["r2"] /. toFRGU$) . basisGU$]};
uvGGH$ = {legsGU$, IPL[{G}] colGU$ Simplify[(ownGU$["uv"] /. toFRGU$) . basisGU$]/FR$Eps};
Print["own R2 g g H: ", InputForm[r2GGH$[[2]]]];
Print["own UV g g H: ", InputForm[uvGGH$[[2]]]];
r2List$ = Append[r2List$, r2GGH$];
uvList$ = Append[uvList$, uvGGH$];
Print["vertex legs: R2 ", r2List$[[All, 1, All, 1]], ";  UV ", uvList$[[All, 1, All, 1]]];


(* ::Section:: *)
(*WriteUFO*)


FeynmanGauge = True;
If[DirectoryQ["QCDH_NLO_UFO"], DeleteDirectory["QCDH_NLO_UFO", DeleteContents -> True]];
WriteUFO[LQCDH, UVCounterterms -> uvList$, R2Vertices -> r2List$, Output -> "QCDH_NLO_UFO"];
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact in QCDH_NLO_UFO: ",
  exactUFO$[FileNameJoin[{Directory[], "QCDH_NLO_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["Integrate left in the UFO (expect False): ", AnyTrue[FileNames["*.py", "QCDH_NLO_UFO"], StringContainsQ[Import[#, "Text"], "Integrate"] &]];
Print["written: ", FileNames["QCDH_NLO_UFO"]];
