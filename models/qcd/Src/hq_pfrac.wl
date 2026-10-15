(* ::Package:: *)

(* ::Title:: *)
(*Step (9): partial fractions on the three-body cut and the integral families (library for hq_reduce.wl, hq_amflow.wl)*)


(* ::Text:: *)
(*Research note models/qcd, step (9), App. L.  On the cut k1^2 = k2^2 = m^2, (p1 + p2 - k1 - k2)^2 = 0 (m = 1 after the reduction) the free*)
(*variables are x1 = -2 p1.k1, x2 = -2 p2.k1, x3 = -2 p2.k2, x4 = -2 p1.k2, and k1.k2 = -(s + 2 m^2 + x1 + x2 + x3 + x4)/2.  Every*)
(*denominator of the 2 -> 3 amplitudes is one of ten affine forms in x (formsPF): t- and u-channel heavy quarks T1, U1, T2, U2, emission from*)
(*the initial state A, B, the s-channel gluon C (and Cs = C - s, from partial fractions), emission from the final state E, F.  Five or more*)
(*forms are always linearly dependent: pfDen applies Leinartas' algorithm (a relation sum lam_i L_i = K; for K != 0 multiply by*)
(*sum lam_i L_i/K, for K = 0 write one L_k by the others) until the denominators of every term are independent.  A family = the three cut*)
(*propagators + four independent forms; k1 <-> k2 (x1 <-> x4, x2 <-> x3) maps a set onto an equivalent one.*)


(* ::Section:: *)
(*Forms*)


xs = {x1, x2, x3, x4};
formsPF = <|"T1" -> x1, "U1" -> x2, "T2" -> x3, "U2" -> x4,
   "A" -> -(s + x1 + x4), "B" -> -(s + x2 + x3), "C" -> -(s + x1 + x2 + x3 + x4), "Cs" -> -(2 s + x1 + x2 + x3 + x4),
   "E" -> s + x3 + x4, "F" -> s + x1 + x2|>;
(* momentum form {q, mass^2} of each denominator q^2 - mass^2 (loop momenta k1, k2; p1, p2 incoming) *)
momPF = <|"T1" -> {p1 - k1, mt2}, "U1" -> {p2 - k1, mt2}, "T2" -> {p2 - k2, mt2}, "U2" -> {p1 - k2, mt2},
   "A" -> {k1 + k2 - p2, 0}, "B" -> {k1 + k2 - p1, 0}, "C" -> {k1 + k2, 0}, "Cs" -> {k1 + k2, s},
   "E" -> {p1 + p2 - k2, mt2}, "F" -> {p1 + p2 - k1, mt2}|>;
swapPF = <|"T1" -> "U2", "U2" -> "T1", "U1" -> "T2", "T2" -> "U1", "A" -> "A", "B" -> "B", "C" -> "C", "Cs" -> "Cs", "E" -> "F", "F" -> "E"|>;
swapX = {x1 -> x4, x4 -> x1, x2 -> x3, x3 -> x2};
(* p1 <-> p2: a symmetry of every integral (they depend on s only), used by hq_reduce.wl to identify masters *)
pswapPF = <|"T1" -> "U1", "U1" -> "T1", "T2" -> "U2", "U2" -> "T2", "A" -> "B", "B" -> "A", "C" -> "C", "Cs" -> "Cs", "E" -> "E", "F" -> "F"|>;
linPF[L_] := Coefficient[formsPF[L], #] & /@ xs;
cstPF[L_] := formsPF[L] /. Thread[xs -> 0];
identPF[f_] := Module[{hit = Select[Keys[formsPF], Function[L, FreeQ[Together[f/formsPF[L]], Alternatives @@ xs]]]},
   If[hit === {}, Print["unknown factor ", f]; Abort[]];
   {First[hit], Together[f/formsPF[First[hit]]]}];


(* ::Section:: *)
(*Partial fractions (Leinartas)*)


ClearAll[pfDen];
pfDen[dens_Association] := pfDen[dens] = Module[{S = Keys[dens], vec, lam, K, ks, res},
   If[Length[S] == 0, Return[{{1, dens}}]];
   vec = linPF /@ S;
   If[MatrixRank[vec] == Length[S], Return[{{1, dens}}]];
   lam = First[NullSpace[Transpose[vec]]];
   K = Together[lam . (cstPF /@ S)];
   res = If[K =!= 0,
     Flatten[Table[If[lam[[i]] === 0, Nothing,
        Module[{d2 = dens}, d2[S[[i]]] = d2[S[[i]]] - 1; If[d2[S[[i]]] == 0, d2 = KeyDrop[d2, S[[i]]]];
          {#[[1]] lam[[i]]/K, #[[2]]} & /@ pfDen[d2]]], {i, Length[S]}], 1],
     ks = First[MaximalBy[Select[Range[Length[S]], lam[[#]] =!= 0 &], dens[S[[#]]] &]];
     Flatten[Table[If[i == ks || lam[[i]] === 0, Nothing,
        Module[{d2 = dens}, d2[S[[i]]] = d2[S[[i]]] - 1; If[d2[S[[i]]] == 0, d2 = KeyDrop[d2, S[[i]]]];
          d2[S[[ks]]] = d2[S[[ks]]] + 1;
          {#[[1]] (-lam[[i]]/lam[[ks]]), #[[2]]} & /@ pfDen[d2]]], {i, Length[S]}], 1]];
   {Together[Total[#[[All, 1]]]], #[[1, 2]]} & /@ GatherBy[res, Last]];
(* r = num/den -> {num, {{coefficient, dens}, ...}}: the numerator is kept apart (the coefficients depend on s only) *)
pfRationalSplit[r_] := Module[{t = Together[r], num, fl, pre = 1, dens = <||>, id},
   num = Numerator[t]; fl = FactorList[Denominator[t]];
   Do[If[FreeQ[f[[1]], Alternatives @@ xs], pre = pre/f[[1]]^f[[2]],
      id = identPF[f[[1]]]; pre = pre/id[[2]]^f[[2]]; dens[id[[1]]] = Lookup[dens, id[[1]], 0] + f[[2]]], {f, fl}];
   {pre num, pfDen[dens]}];


(* ::Section:: *)
(*Families and the map to GLI*)


completionPF = {"T1", "U1", "T2", "U2", "C", "E", "F", "A", "B"};
makeFamilies[sets_] := Module[{fams = {}, covered},
   covered[S_] := AnyTrue[fams, SubsetQ[#, S] || SubsetQ[#, swapPF /@ S] &];
   Do[If[!covered[S],
      Module[{f = S}, Do[If[Length[f] < 4 && !MemberQ[f, c] && MatrixRank[linPF /@ Append[f, c]] == Length[f] + 1, AppendTo[f, c]], {c, completionPF}];
        AppendTo[fams, f]]], {S, SortBy[sets, -Length[#] &]}];
   fams];
ClearAll[numInFam];
numInFam[num_, f_, sw_] := Module[{sol = First[Solve[Thread[Array[LL, 4] == (formsPF /@ f)], xs]]}, Expand[If[sw, num /. swapX, num] /. sol]];
(* pieces grouped by (family, k1 <-> k2) into a polynomial in YY[j] = 1/L_j, multiplied once by the numerator in the family's forms *)
famPrefix = "R";
toGLIgroup[num_, pieces_, fams_] := Module[{groups = <||>, res = 0},
   Do[Module[{S = Keys[pc[[2]]], i, sw = False, d = pc[[2]], c = pc[[1]], f},
      i = FirstPosition[fams, _?(SubsetQ[#, S] &), {0}, {1}, Heads -> False][[1]];
      If[i == 0, sw = True; i = FirstPosition[fams, _?(SubsetQ[#, swapPF /@ S] &), {0}, {1}, Heads -> False][[1]];
        d = KeyMap[swapPF, d]; c = c /. swapX];
      If[i == 0, Print["no family for ", S]; Abort[]];
      f = fams[[i]];
      groups[{i, sw}] = Lookup[groups, Key[{i, sw}], 0] + c Product[YY[j]^Lookup[d, f[[j]], 0], {j, 4}]], {pc, pieces}];
   KeyValueMap[Function[{key, pden}, Module[{pn, cr},
       pn = numInFam[num, fams[[key[[1]]]], key[[2]]] /. LL[j_] :> 1/YY[j];
       cr = CoefficientRules[Expand[pden pn] Product[YY[j]^40, {j, 4}], Array[YY, 4]];
       res += Total[(Together[#[[2]]] GLI[famPrefix <> ToString[key[[1]]], Join[{1, 1, 1}, #[[1]] - 40]]) & /@ cr]]], groups];
   res];
