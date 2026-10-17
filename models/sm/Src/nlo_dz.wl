(* ::Package:: *)

(* ::Title:: *)
(*Step (9d): NLOCT's on-shell field constants of the note's model, from its two-point UV vertices*)


(* ::Text:: *)
(*NLOCT writes its UV vertices with the renormalization constants already inserted.  The field constants dZ (on shell,*)
(*from the 1PI self-energies, Feynman gauge) are recovered by matching each two-point vertex of SM_CT.nlo with the symbolic*)
(*counterterm vertex of SM_CTsym.m (nlo_ctrules.wl), which is linear in FR$deltaZ and FR$delta:*)
(*  - the two vertices are matched by their set of fields (the order of the legs differs; NLOCT does not write the*)
(*    vanishing mixings), with p2 = -p1;*)
(*  - the internal parameters are written in the external ones on both sides (NLOCT keeps vev, the Yukawa couplings and*)
(*    sw, cw next to MW, MZ: the photon self-energy is transverse only with vev = 2 MW sw/ee);*)
(*  - the coefficients of the tensor structures (g^{mu nu}, k^mu k^nu, pslash P_L/R, P_L/R) and of the powers of k^2 are taken*)
(*    by differentiation (NLOCT's expressions are large and full of If[m == 0, ...] branches, and are not expanded) and kept*)
(*    as opaque symbols in the linear solve; the equations not used for the solve are checked numerically.*)
(*Only the field constants are used (nlo_ctparams.wl, the Goldstone ones set to 0); the on-shell mass constants are kept for a check.*)
(*Writes Src/generated/SM_dZ.m.  Batch: wolframscript -file nlo_dz.wl  (plain kernel)*)


srcDirDZ$ = DirectoryName[$InputFileName];
t0DZ$ = AbsoluteTime[];
sym$ = Get[FileNameJoin[{srcDirDZ$, "generated", "SM_CTsym.m"}]];
Get[FileNameJoin[{srcDirDZ$, "generated", "SM_CT.nlo"}]];
Print["NLOCT UV vertices: ", Length[UV$vertlist], ";  symbolic counterterm vertices: ", Length[sym$["ctSym"]], ";  ",
  Round[AbsoluteTime[] - t0DZ$], " s"];
barName$[p_] := ToExpression[ToString[p] <> "bar"];
fieldsOf$[legs_] := Sort[legs[[All, 1]] /. anti[p_] :> barName$[p]];
nloct2$ = Association[(fieldsOf$[#[[1]]] -> #[[2]]) & /@ Select[UV$vertlist, Length[#[[1]]] == 2 &]];
ct2$ = Association[(fieldsOf$[#[[1]]] -> #[[2]]) & /@ Select[sym$["ctSym"], Length[#[[1]]] == 2 &]];
Print["two-point vertices: NLOCT ", Length[nloct2$], ", symbolic ", Length[ct2$], ";  symbolic only: ",
  Complement[Keys[ct2$], Keys[nloct2$]]];

(* internal parameters in terms of the external ones (as in SM.fr) *)
vevE$ = 2 MW sw/ee;
yuk$ = {ye -> Sqrt[2] Me/vevE$, ym -> Sqrt[2] MMU/vevE$, ytau -> Sqrt[2] MTA/vevE$, yup -> Sqrt[2] MU/vevE$,
   yc -> Sqrt[2] MC/vevE$, yt -> Sqrt[2] MT/vevE$, ydo -> Sqrt[2] MD/vevE$, ys -> Sqrt[2] MS/vevE$, yb -> Sqrt[2] MB/vevE$};
intern$[x_] := x /. yuk$ /. {lam -> MH^2/(2 vevE$^2), muH2 -> MH^2/2} /. vev -> vevE$ /. {cw -> MW/MZ} /.
   sw -> Sqrt[1 - MW^2/MZ^2];
(* structures: momentum 2 = -momentum 1 *)
lor1$ = Index[Lorentz, Ext[1]]; lor2$ = Index[Lorentz, Ext[2]];
struct$[x_] := x /. {IndexDelta[Index[Colour | Gluon, __], Index[Colour | Gluon, __]] -> 1} /. {FV[1, i_] :> -FV[2, i], SP[1, 2] -> -SP[2, 2], SP[2, 1] -> -SP[2, 2], SP[1, 1] -> SP[2, 2],
      SlashedP[1] -> -SlashedP[2]} /. {
     ME[lor1$, lor2$] -> sME, ME[lor2$, lor1$] -> sME, FV[2, lor1$] FV[2, lor2$] -> sKK,
     TensDot[SlashedP[2], ProjM][__] -> sPM, TensDot[SlashedP[2], ProjP][__] -> sPP, ProjM[__] -> sM, ProjP[__] -> sP,
     SP[2, 2] -> kk};
(* the coefficients of s kk^n, n = 0, 1 (s = 1 for scalars), by differentiation *)
(* (the iterator is a Module variable: a plain s would also replace the strange quark in FR$deltaZ[{s, s}, ...]) *)
coefs$[x_] := Module[{y = struct$[x], ss, sv},
   ss = Select[{sME, sKK, sPM, sPP, sM, sP}, !FreeQ[y, #] &];
   If[ss === {}, {{"1", 0} -> (y /. kk -> 0), {"1", 1} -> (D[y, kk] /. kk -> 0)},
    Flatten[Table[{{ToString[sv], 0} -> (D[y, sv] /. kk -> 0 /. Thread[ss -> 0]), {ToString[sv], 1} -> (D[y, sv, kk] /. kk -> 0 /. Thread[ss -> 0])}, {sv, ss}]]]];
(* a numerical point for the consistency checks (light masses small but nonzero; If[m == 0, ...] take the m != 0 branch;*)
(* no threshold relations such as MD = 2 MU, where NLOCT's expressions are 0/0) *)
ptDZ$ = {ee -> Sqrt[4 Pi/128], MZ -> 911876/10000, MW -> 80369/1000, MH -> 1252/10, MT -> 17257/100, MB -> 3, MC -> 3/2,
   MS -> 1/10, MD -> 1/200, MU -> 1/300, Me -> 1/2000, MMU -> 1/10, MTA -> 18/10, FR$MU -> 100, FR$Eps -> 1/3, aS -> 118/1000,
   gs -> Sqrt[4 Pi 118/1000]};
numv$[x_] := Quiet[N[(x /. IPL[_] -> 1) /. ptDZ$, 30]];
solveVertex$[f_] := Module[{a, b, cA, cB, keys, unk, eqs, sol, opaque, rest, chk},
   a = Expand[intern$[ct2$[f]]];
   b = intern$[nloct2$[f]];
   cA = Association[coefs$[a]]; cB = Association[coefs$[b]];
   keys = Union[Keys[cA], Keys[cB]];
   unk = Union[Cases[a, (FR$delta | FR$deltaZ)[__], Infinity]];
   opaque = Table[k -> bb[k], {k, keys}];
   eqs = Table[(Lookup[cA, Key[k], 0] == bb[k]), {k, keys}];
   (* as many equations as unknowns (the first subset with a unique solution); the others are checked below *)
   sol = {};
   Do[Module[{s0 = Quiet[Solve[sub, unk]]},
      If[Length[s0] == 1 && SubsetQ[s0[[1, All, 1]], unk], sol = First[s0]; Break[]]],
    {sub, Subsets[Select[eqs, !FreeQ[#[[1]], Alternatives @@ unk] &], {Length[unk]}]}];
   If[sol === {}, Print["   no solution for ", f, " (unknowns ", unk, ")"]; Return[{}]];
   (* the remaining equations, numerically with NLOCT's values *)
   rest = Select[eqs /. sol, # =!= True &];
   chk = Max[Abs[numv$[(#[[1]] - #[[2]]) /. bb[k_] :> Lookup[cB, Key[k], 0]]] & /@ rest, 0];
   If[chk > 10^-12, Print["   ", f, ": equations not used violated by ", ScientificForm[chk, 3]]];
   sol /. bb[k_] :> Lookup[cB, Key[k], 0]];
(* the Goldstone bosons are internal only: their field constants cancel between the vertices and the propagators of any*)
(* amplitude and are set to 0.  (NLOCT's G0 G0 and G+ G- vertices also have a constant term that is not in the counterterm*)
(* Lagrangian, which has no Goldstone mass term in Feynman gauge with FR$deltat = 0; it is not used.) *)
goldstone$ = {{G0, G0}, {G0, H}, {GP, GPbar}};
sols$ = Association[Table[f -> solveVertex$[f], {f, Complement[Intersection[Keys[ct2$], Keys[nloct2$]], goldstone$]}]];
Print["solved ", Length[sols$], " two-point vertices;  ", Round[AbsoluteTime[] - t0DZ$], " s"];
all$ = Flatten[Values[sols$]];
dZ$ = Join[DeleteDuplicatesBy[Select[all$, MatchQ[#, FR$deltaZ[__] -> _] &], First],
   (# -> 0) & /@ Union[Cases[ct2$ /@ goldstone$, FR$deltaZ[{G0 | GP, _}, __] | FR$deltaZ[{_, G0 | GP}, __], Infinity]]];
dM$ = DeleteDuplicatesBy[Select[all$, MatchQ[#, FR$delta[__] -> _] &], First];
need$ = Union[Cases[sym$["ctSym"], FR$deltaZ[__], Infinity]];
Print["field constants recovered: ", Length[dZ$], " of ", Length[need$], ";  missing: ", Complement[need$, dZ$[[All, 1]]]];
(* the same constant from two vertices (e.g. dZ_W from W Wbar and from mixings) must agree numerically *)
dups$ = Select[GroupBy[Select[all$, MatchQ[#, FR$deltaZ[__] -> _] &], First -> Last], Length[#] > 1 &];
Print["constants from more than one vertex, largest numerical difference: ",
  Max[Join[{0}, Flatten[(Abs[numv$[# - First[#]]] & /@ Values[dups$])]]]];
Put[<|"dZ" -> dZ$, "dMOS" -> dM$|>, FileNameJoin[{srcDirDZ$, "generated", "SM_dZ.m"}]];
Print["field constants (numbers, FR$Eps = 1/3, FR$MU = 100):"];
Scan[Print["   ", #[[1, 1]], " ", Last[#[[1]]] /. {{{}} -> ""}, ":  ", N[numv$[#[[2]]], 8]] &, SortBy[dZ$, ToString]];
Print["written: generated/SM_dZ.m;  ", Round[AbsoluteTime[] - t0DZ$], " s"];
