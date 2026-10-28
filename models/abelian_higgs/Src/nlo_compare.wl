(* ::Package:: *)

(* ::Title:: *)
(*Step (4), 3 of 3: the UV poles of NLOCT's counterterm vertices against the note (Feynman gauge)*)


(* ::Text:: *)
(*Reads Src/generated/AbelianHiggs_CT.nlo (nlo_nloct.wl) and takes the coefficient of 1/FR$Eps of every UV vertex (the*)
(*loop-particle tags IPL[...] set to 1).  NLOCT's on-shell constants are written as a pole part plus a finite part, so this*)
(*coefficient is the whole UV pole of the counterterm vertex.  It is compared, at xi = 1, with*)
(*  (a) the note's FJ counterterm vertex (Eqs. (ctse), (ctv)), which cancels the pole of the 1PI diagrams plus the*)
(*      tadpole-attached diagrams (steps (3), (4)), and*)
(*  (b) minus the pole of the 1PI diagrams alone (what a calculation without tadpole diagrams, such as MadLoop's, needs).*)
(*For the four-point vertices and the A G h vertex there are no tadpole-attached diagrams and (a) = (b).*)
(*Units: K x (coefficient of 1/eps), K = 16 pi^2, divided by i where the Feynman rule carries i, written in e, lam, MA.*)
(*Batch: wolframscript -file nlo_compare.wl  (no FeynCalc, no FeynRules)*)


srcDirNX$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
Get[FileNameJoin[{srcDirNX$, "generated", "AbelianHiggs_CT.nlo"}]];
KK = 16 Pi^2;

(* everything in e, lam, MA (v = MA/e, MH^2 = 2 lam v^2) *)
toCoup$ = {vev -> MA/ee, MH -> Sqrt[2 lam] MA/ee};
pole$[expr_] := Simplify[KK Coefficient[Expand[expr /. IPL[_] -> 1], FR$Eps, -1] /. toCoup$ /. ee -> e, MA > 0 && lam > 0 && e > 0];
uvList$ = Association[Rule @@@ (UV$vertlist /. {f_, n_Integer} :> f)];
Print["NLOCT UV vertices: ", Keys[uvList$]];
Print["constants of NLOCT's counterterm Lagrangian: ", Union[Cases[Get[FileNameJoin[{srcDirNX$, "generated", "AbelianHiggs_ctlag.m"}]],
    (h_Symbol)[_List, _List] /; StringStartsQ[SymbolName[h], "FR$delta"], Infinity]]];

(* the note at xi = 1 (K x Delta coefficients) *)
xi1$ = 1;
v$ = MA/e; mh2$ = 2 lam v$^2;
dZPhi$ = (3 - xi1$) e^2; dm2$ = 4 lam - 3 e^2; dlam$ = 10 lam - 6 e^2 + 3 e^4/lam; dZA$ = -e^2/3;
c3$ = (dlam$ + 3 dZPhi$ + dm2$)/2; c4$ = dlam$ + 2 dZPhi$; cA$ = (dZPhi$ + dm2$ - dlam$)/2;
tUV$ = (6 MA^4 + 3 mh2$^2 + xi1$ MA^2 mh2$)/(2 v$);         (* K T pole, Eq. (uv) *)
(* 1PI-only poles (steps (3), (4)) at xi = 1 *)
uv1PI$ = <|
   "HH" -> (xi1$ - 3) e^2 p2 + (18 MA^4 + 13 mh2$^2 + xi1$ MA^2 mh2$)/(2 v$^2),
   "GG" -> (xi1$ - 3) e^2 p2 + tUV$/v$,
   "AAT" -> e^2 p2/3 + (3 + xi1$) e^2 MA^2,
   "HHH" -> 3 (6 MA^4 + 5 mh2$^2 - xi1$ MA^2 mh2$)/v$^3,
   "HGG" -> (6 MA^4 + 5 mh2$^2 - xi1$ MA^2 mh2$)/v$^3,
   "AAH" -> -6 MA^4/v$^3|>;

(* each row: name, NLOCT key, NLOCT pole (in the normalization of the column), (a) FJ, (b) -1PI *)
rows$ = {};
add$[name_, nlo_, fj_, opi_] := AppendTo[rows$, {name, Simplify[nlo], Simplify[fj], Simplify[opi]}];

(* two-point vertices: the Feynman rule is i Sigma_ct (h, G) and -i [g Sigma_T,ct + ...] (A) *)
hh$ = pole$[uvList$[{H, H}]/I /. SP[_, _] -> p2];
add$["h h: Sigma^H_ct", hh$, dZPhi$ (p2 - mh2$) - dm2$ mh2$, -uv1PI$["HH"]];
gg$ = pole$[uvList$[{G0, G0}]/I /. SP[_, _] -> p2];
add$["G G: Sigma^GG_ct", gg$, dZPhi$ p2, -uv1PI$["GG"]];
aa$ = uvList$[{A, A}] /. {ME[__] -> gMet, FV[i_, _] :> pv} /. SP[_, _] -> p2;
aaT$ = pole$[-Coefficient[Expand[aa$], gMet]/I];
add$["A A: Sigma_T,ct (coefficient of g)", aaT$, dZA$ p2 - (dm2$ - dlam$) MA^2, -uv1PI$["AAT"]];
(* NLOCT writes no A G vertex, although its counterterm Lagrangian (generated/AbelianHiggs_ctlag.m) has
   -(dMA + MA (dZ_A + dZ_G)/2) A.dG0.  The poles of dZ_A, dMA^2 = 2 MA dMA and dZ_G are read from NLOCT's own A A and
   G G vertices: the g term of A A is i[-dZ_A p^2 + dMA^2 + dZ_A MA^2] = -i aaT, G G = i[dZ_G p^2 + ...] *)
dZAn$ = Simplify[Coefficient[aaT$, p2]];
dMA2n$ = Simplify[-(aaT$ /. p2 -> 0) - dZAn$ MA^2];
dZGn$ = Simplify[Coefficient[gg$, p2]];
mixN$ = Simplify[-(dMA2n$/(2 MA) + MA (dZAn$ + dZGn$)/2)];
Print["NLOCT constants (K x pole): dZ_A = ", dZAn$, ", dMA^2 = ", dMA2n$, ", dZ_G = ", dZGn$,
  ";  A.dG0 coefficient of its counterterm Lagrangian = ", mixN$];
add$["A G: Sigma^AG_ct (NLOCT: from its Lagrangian, no vertex written)", mixN$, -(dZPhi$ + dm2$ - dlam$) MA/2, -3 e^2 MA];

(* three-point vertices: counterterm = c x tree; tree rules -6 i lam v, -2 i lam v, 2 i e MA g, e (p_h - p_G) *)
add$["h h h: c3", pole$[uvList$[{H, H, H}]]/(-6 I lam v$), c3$, -(-uv1PI$["HHH"])/(6 lam v$) /. {} -> 0];
add$["h G G: c3", pole$[uvList$[{H, G0, G0}]]/(-2 I lam v$), c3$, uv1PI$["HGG"]/(2 lam v$)];
aah$ = uvList$[{A, A, H}] /. ME[__] -> gMet;
add$["A A h: cA", pole$[Coefficient[Expand[aah$], gMet]]/(2 I e MA), cA$, -uv1PI$["AAH"]/(2 e MA)];
agh$ = uvList$[{A, H, G0}] /. {FV[2, _] -> ph, FV[3, _] -> pG};
(* the pole is c e (p_h - p_G): the coefficients of p_h and -p_G must agree *)
aghH$ = pole$[Coefficient[Expand[agh$], ph]]/e; aghG$ = -pole$[Coefficient[Expand[agh$], pG]]/e;
Print["A h G: coefficient of p_h and of -p_G (expect equal): ", {aghH$, aghG$}];
add$["A h G: dZ_Phi (coefficient of e (p_h - p_G))", aghH$, dZPhi$, dZPhi$];

(* four-point vertices: counterterm = c x contact vertex *)
add$["h h h h: c4", pole$[uvList$[{H, H, H, H}]]/(-6 I lam), c4$, c4$];
add$["h h G G: c4", pole$[uvList$[{H, H, G0, G0}]]/(-2 I lam), c4$, c4$];
add$["G G G G: c4", pole$[uvList$[{G0, G0, G0, G0}]]/(-6 I lam), c4$, c4$];
add$["A A h h: dZ_Phi", pole$[Coefficient[Expand[uvList$[{A, A, H, H}] /. ME[__] -> gMet], gMet]]/(2 I e^2), dZPhi$, dZPhi$];
add$["A A G G: dZ_Phi", pole$[Coefficient[Expand[uvList$[{A, A, G0, G0}] /. ME[__] -> gMet], gMet]]/(2 I e^2), dZPhi$, dZPhi$];
add$["A A A A (no counterterm)", If[KeyExistsQ[uvList$, {A, A, A, A}], pole$[uvList$[{A, A, A, A}] /. {ME[__] -> 1}], 0], 0, 0];

Print["vertex | NLOCT pole | (a) FJ (note) | (b) -1PI only | NLOCT - (a) | NLOCT - (b)"];
Scan[Print[#[[1]], " | ", InputForm[#[[2]]], " | ", InputForm[#[[3]]], " | ", InputForm[#[[4]]], " | ",
    If[StringQ[#[[2]]], "-", InputForm[Simplify[#[[2]] - #[[3]]]]], " | ", If[StringQ[#[[2]]], "-", InputForm[Simplify[#[[2]] - #[[4]]]]]] &, rows$];
r2T$ = If[MemberQ[First /@ (R2$vertlist /. {f_, n_Integer} :> f), {H}],
    Simplify[KK (Association[Rule @@@ (R2$vertlist /. {f_, n_Integer} :> f)][{H}] /. IPL[_] -> 1) /. toCoup$ /. ee -> e], "none"];
(* the rational term of K T: (D - 1) A0(MA^2) MA^2/v gives -2 MA^4/v = -2 e MA^3; the R2 vertex is i times it *)
Print["tadpole: K T pole at xi = 1 = ", Simplify[tUV$], ";  R2 one-point vertex of NLOCT (K x) ", r2T$,
  ", i x the rational term of Eq. (T) ", -2 I e MA^3, "  (difference ", Simplify[r2T$ + 2 I e MA^3], ")"];
Export[FileNameJoin[{srcDirNX$, "results", "nlo_compare.csv"}],
  Prepend[Map[ToString[InputForm[#]] &, {#[[1]], #[[2]], #[[3]], #[[4]], If[StringQ[#[[2]]], "-", Simplify[#[[2]] - #[[3]]]],
       If[StringQ[#[[2]]], "-", Simplify[#[[2]] - #[[4]]]]} & /@ rows$, {2}],
   {"vertex", "NLOCT_pole", "FJ_note", "minus_1PI_only", "NLOCT_minus_FJ", "NLOCT_minus_1PI_only"}], "CSV"];
Print["written results/nlo_compare.csv"];
