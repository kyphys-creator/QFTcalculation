(* ::Package:: *)

(* ::Title:: *)
(*Step (9): the on-shell field constants for the CKM NLO UFO, as numbers at the UFO's point*)


(* ::Text:: *)
(*The UV counterterm vertices of the UFO (nlo_ckm_ctrules.wl) contain the field constants FR$deltaZ of all fields, with*)
(*the off-diagonal quark ones.  They are the LSZ factors of the external legs (MadLoop does not dress them with*)
(*self-energies; the internal ones cancel).  NLOCT does not solve the on-shell conditions of the off-diagonal quark*)
(*constants in reasonable time with the complex CKM matrix (nlo_ckm_writect.wl with mixing ran for 47 minutes on the*)
(*two-point fermion vertices), so:*)
(*  - the quark constants (diagonal and off-diagonal, L and R) and dZ_W are this note's (nlo_ckm_dzown.wl: step (3)*)
(*    self-energies, Eqs. (dZos), (dZRos), Denner's diagonal constants), electroweak;*)
(*  - the other fields (A, Z, A-Z, H, leptons, neutrinos) take NLOCT's on-shell constants of the model without quark*)
(*    mixing (SM_CKM_CT0.nlo of nlo_ckm_writect.wl nomix), recovered from its two-point UV vertices as in the SM note's*)
(*    nlo_dz.wl, if that file exists; otherwise 0 (then the UFO is only for processes whose external particles are*)
(*    quarks, W and photons or Z bosons of loop-induced processes, which get no counterterm);*)
(*  - where both exist (the diagonal quark constants, dZ_W), NLOCT's are compared with this note's.*)
(*Numbers at the point of nlo_ckm_dzown.wl, 40 digits, the scale 91 GeV ({pole, finite}; each pole comes with ln mu^2).*)
(*Writes Src/generated/SM_CKM_dZ.m.  Batch: wolframscript -file nlo_ckm_dz.wl  (after nlo_ckm_ctrules.wl, nlo_ckm_dzown.wl)*)
(*With the argument ms0: this note's constants at m_s = 0 (SM_CKM_dZown_ms0.m) -> SM_CKM_dZ_ms0.m.*)


srcDirDZ$ = DirectoryName[$InputFileName];
t0DZ$ = AbsoluteTime[];
sym$ = Get[FileNameJoin[{srcDirDZ$, "generated", "SM_CKM_CTsym.m"}]];
ms0DZ$ = Length[$ScriptCommandLine] >= 2 && $ScriptCommandLine[[2]] === "ms0";
own$ = Association[Get[FileNameJoin[{srcDirDZ$, "generated", If[ms0DZ$, "SM_CKM_dZown_ms0.m", "SM_CKM_dZown.m"]}]]["dZ"]];
nloFile$ = FileNameJoin[{srcDirDZ$, "generated", "SM_CKM_CT0.nlo"}];
haveNLO$ = FileExistsQ[nloFile$];
need$ = Union[Cases[sym$["ctSym"], FR$deltaZ[__], Infinity]];
Print["field constants in the counterterm vertices: ", Length[need$], ";  NLOCT's on-shell file: ", If[haveNLO$, "yes", "no"]];

(* this note's constants: the quarks and W *)
gen2$ = <|u -> {"U", 1}, c -> {"U", 2}, t -> {"U", 3}, d -> {"D", 1}, s -> {"D", 2}, b -> {"D", 3}|>;
ownKey$[FR$deltaZ[{f1_, f2_}, {{}}, ch_]] /; KeyExistsQ[gen2$, f1] && KeyExistsQ[gen2$, f2] && gen2$[f1][[1]] === gen2$[f2][[1]] :=
  {gen2$[f1][[1]], ToString[ch], gen2$[f1][[2]], gen2$[f2][[2]]};
ownKey$[FR$deltaZ[{W, W}, {{}}]] := "W";
ownKey$[_] := None;
(* {EW pole, EW finite, QCD pole, QCD finite} at 91 GeV *)
dZown$ = Table[k -> {own$[ownKey$[k]][[1]], own$[ownKey$[k]][[2]], 0, 0}, {k, Select[need$, ownKey$[#] =!= None &]}];
Print["this note's constants (quarks, W): ", Length[dZown$]];

(* NLOCT's constants of the model without quark mixing, from its two-point UV vertices (SM note, nlo_dz.wl) *)
dZnlo$ = {};
If[haveNLO$,
  Get[nloFile$];
  barName$[p_] := ToExpression[ToString[p] <> "bar"];
  fieldsOf$[legs_] := Sort[legs[[All, 1]] /. anti[p_] :> barName$[p]];
  nloct2$ = Association[(fieldsOf$[#[[1]]] -> #[[2]]) & /@ Select[UV$vertlist, Length[#[[1]]] == 2 &]];
  ct2$ = Association[(fieldsOf$[#[[1]]] -> #[[2]]) & /@ Select[sym$["ctSym"], Length[#[[1]]] == 2 &]];
  (* the point and the internal parameters (as nlo_ckm_dzown.wl) *)
  gen$[i_] := Index[Generation, i];
  vStd$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
     {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
     {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
      {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
  ext$ = {ee -> Sqrt[4 Pi/128], MZ -> 91, MW -> 80, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000,
     MD -> 271/10000, MU -> 127/10000, MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000, aS -> 118/1000,
     s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dCKM -> 1147/1000};
  vevE$ = 2 MW sw/ee;
  int$ = Join[{sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ, vev -> vevE$, lam -> MH^2/(2 vevE$^2), muH2 -> MH^2/2,
      gw -> ee/sw, g1 -> ee/cw, aEW -> ee^2/(4 Pi), c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2],
      ye -> Sqrt[2] Me/vevE$, ym -> Sqrt[2] MMU/vevE$, ytau -> Sqrt[2] MTA/vevE$, yup -> Sqrt[2] MU/vevE$,
      yc -> Sqrt[2] MC/vevE$, yt -> Sqrt[2] MT/vevE$, ydo -> Sqrt[2] MD/vevE$, ys -> Sqrt[2] MS/vevE$, yb -> Sqrt[2] MB/vevE$},
     Flatten[Table[{CKM[gen$[i], gen$[j]] -> vStd$[[i, j]], CKM[i, j] -> vStd$[[i, j]],
        ToExpression["CKM" <> ToString[i] <> "x" <> ToString[j]] -> vStd$[[i, j]]}, {i, 3}, {j, 3}]],
     Flatten[Table[{yu[gen$[i], gen$[j]] -> If[i == j, Sqrt[2] {MU, MC, MT}[[i]]/vevE$, 0],
        yd[gen$[i], gen$[j]] -> If[i == j, Sqrt[2] {MD, MS, MB}[[i]]/vevE$, 0],
        yl[gen$[i], gen$[j]] -> If[i == j, Sqrt[2] {Me, MMU, MTA}[[i]]/vevE$, 0]}, {i, 3}, {j, 3}]]];
  numAt$[x_, mu_] := N[(x /. IPL[_] -> 1) //. int$ /. ext$ /. FR$MU -> mu, 40];
  (* {EW pole, EW finite, QCD pole, QCD finite} at the scale mu *)
  laur$[x_, mu_] := Module[{y = numAt$[x /. gs -> gsSym$ /. G -> gsSym$ /. aS -> gsSym$^2/(4 Pi), mu], ew, qcd},
     y = Normal[Series[y, {FR$Eps, 0, 0}]];
     ew = y /. gsSym$ -> 0; qcd = Expand[y - ew] /. gsSym$ -> Sqrt[4 Pi 118/1000];
     {Coefficient[ew, FR$Eps, -1], Coefficient[ew, FR$Eps, 0], Coefficient[qcd, FR$Eps, -1], Coefficient[qcd, FR$Eps, 0]}];
  lor1$ = Index[Lorentz, Ext[1]]; lor2$ = Index[Lorentz, Ext[2]];
  struct$[x_] := x /. {IndexDelta[Index[Colour | Gluon, __], Index[Colour | Gluon, __]] -> 1} /. {FV[1, i_] :> -FV[2, i], SP[1, 2] -> -SP[2, 2],
        SP[2, 1] -> -SP[2, 2], SP[1, 1] -> SP[2, 2], SlashedP[1] -> -SlashedP[2]} /. {
       ME[lor1$, lor2$] -> sME, ME[lor2$, lor1$] -> sME, FV[2, lor1$] FV[2, lor2$] -> sKK,
       TensDot[SlashedP[2], ProjM][__] -> sPM, TensDot[SlashedP[2], ProjP][__] -> sPP, ProjM[__] -> sM, ProjP[__] -> sP,
       SP[2, 2] -> kk};
  coefs$[x_] := Module[{y = struct$[x], ss, sv},
     ss = Select[{sME, sKK, sPM, sPP, sM, sP}, ! FreeQ[y, #] &];
     If[ss === {}, {{"1", 0} -> (y /. kk -> 0), {"1", 1} -> (D[y, kk] /. kk -> 0)},
      Flatten[Table[{{ToString[sv], 0} -> (D[y, sv] /. kk -> 0 /. Thread[ss -> 0]), {ToString[sv], 1} -> (D[y, sv, kk] /. kk -> 0 /. Thread[ss -> 0])}, {sv, ss}]]]];
  (* the off-diagonal quark vertices carry no constant in this model; the diagonal ones are solved as in the SM note
     (real constants: NLOCT's diagonal field constants are real) *)
  solveVertex$[f_] := Module[{a, b, cA, cB, keys, unk, eqs, sol, rest, chk},
     a = Expand[(ct2$[f] /. Conjugate[x : FR$deltaZ[{p_, p_}, ___]] :> x) //. int$];
     b = nloct2$[f];
     cA = Association[coefs$[a]]; cB = Association[coefs$[b]];
     keys = Union[Keys[cA], Keys[cB]];
     unk = Union[Cases[a, (FR$delta | FR$deltaZ)[__], Infinity]];
     eqs = Table[(Lookup[cA, Key[k], 0] == bb[k]), {k, keys}];
     sol = {};
     Do[Module[{s0 = Quiet[Solve[sub, unk]]},
        If[Length[s0] == 1 && SubsetQ[s0[[1, All, 1]], unk], sol = First[s0]; Break[]]],
      {sub, Subsets[Select[eqs, ! FreeQ[#[[1]], Alternatives @@ unk] &], {Length[unk]}]}];
     If[sol === {}, Print["   no solution for ", f, " (unknowns ", unk, ")"]; Return[{}]];
     rest = Select[eqs /. sol, # =!= True &];
     chk = Max[Abs[Flatten[laur$[(#[[1]] - #[[2]]) /. bb[k_] :> Lookup[cB, Key[k], 0], 91] & /@ rest]], 0];
     If[chk > 10^-25, Print["   ", f, ": equations not used violated by ", ScientificForm[N[chk], 3]]];
     sol /. bb[k_] :> Lookup[cB, Key[k], 0]];
  quarks$ = {u, c, t, d, s, b, ubar, cbar, tbar, dbar, sbar, bbar};
  offQ$[f_] := Length[f] == 2 && SubsetQ[quarks$, f] && StringReplace[ToString[f[[1]]], "bar" -> ""] =!= StringReplace[ToString[f[[2]]], "bar" -> ""];
  goldstone$ = {{G0, G0}, {G0, H}, {GP, GPbar}};
  keysV$ = Select[Complement[Intersection[Keys[ct2$], Keys[nloct2$]], goldstone$], ! offQ$[#] &];
  sols$ = Association[Table[f -> solveVertex$[f], {f, keysV$}]];
  Print["NLOCT: solved ", Length[sols$], " two-point vertices;  ", Round[AbsoluteTime[] - t0DZ$], " s"];
  allNum$ = (#[[1]] -> {laur$[#[[2]], 91], laur$[#[[2]], 500]}) & /@ Flatten[Values[sols$]];
  Print["NLOCT: finite(500) - finite(91) - pole ln(500^2/91^2), max (expect ~1e-30): ",
    N[Max[Abs[Flatten[Table[{r[[2, 2, 2]] - r[[2, 1, 2]] - r[[2, 1, 1]] Log[500^2/91^2], r[[2, 2, 4]] - r[[2, 1, 4]] - r[[2, 1, 3]] Log[500^2/91^2]},
          {r, allNum$}]]]], 3]];
  dups$ = Select[GroupBy[Select[allNum$, MatchQ[#, FR$deltaZ[__] -> _] &], First -> (#[[2, 1]] &)], Length[#] > 1 &];
  Print["NLOCT: constants from more than one vertex, largest difference: ", N[Max[Join[{0}, Flatten[Abs[# - First[#]] & /@ Values[dups$]]]], 3]];
  dZnlo$ = (#[[1]] -> #[[2, 1]]) & /@ DeleteDuplicatesBy[Select[allNum$, MatchQ[#, FR$deltaZ[__] -> _] &], First];
  (* NLOCT against this note (EW parts) *)
  cmp$ = Select[dZnlo$, ownKey$[#[[1]]] =!= None &];
  Print["NLOCT against this note's constants (", Length[cmp$], "): |difference| of {pole, finite}, relative to |finite|:"];
  Scan[Module[{o = own$[ownKey$[#[[1]]]], n = #[[2]]},
      Print["   ", #[[1]], ":  ", ScientificForm[N[Abs[n[[1]] - o[[1]]]/Abs[o[[2]]]], 2], ",  ", ScientificForm[N[Abs[n[[2]] - o[[2]]]/Abs[o[[2]]]], 2],
        "   (finite ", N[o[[2]], 8], ")"]] &, cmp$];
  ];

(* the constants of the UFO: this note's for the quarks and W, NLOCT's for the others, 0 for the Goldstone bosons *)
dZ$ = Table[k -> Which[ownKey$[k] =!= None, Association[dZown$][k],
     KeyExistsQ[Association[dZnlo$], k], Association[dZnlo$][k],
     True, {0, 0, 0, 0}], {k, need$}];
Print["field constants of the UFO: ", Length[dZ$], ";  this note's ", Length[dZown$], ", NLOCT's ",
  Count[need$, k_ /; ownKey$[k] === None && KeyExistsQ[Association[dZnlo$], k]], ", zero: ",
  Select[need$, ownKey$[#] === None && ! KeyExistsQ[Association[dZnlo$], #] &]];
outDZ$ = If[ms0DZ$, "SM_CKM_dZ_ms0.m", "SM_CKM_dZ.m"];
Put[<|"dZ" -> dZ$, "mu0" -> 91|>, FileNameJoin[{srcDirDZ$, "generated", outDZ$}]];
Print["written: generated/", outDZ$, ";  ", Round[AbsoluteTime[] - t0DZ$], " s"];
