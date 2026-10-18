(* ::Package:: *)

(* ::Title:: *)
(*Step (9) of the CKM note: processes with external leptons and Z bosons with FeynArts' SM.mod and FormCalc, in the scheme of the note's UFO*)


(* ::Text:: *)
(*The reference for the field constants of the note's NLO UFO that steps (5)-(9) did not use (Z, photon-Z mixing, leptons,*)
(*neutrinos; the diagonal quark constants with the CKM matrix in Z -> b bbar).  FeynArts 3.12 SM.mod ($CKM = True;*)
(*Denner's conventions and his on-shell counterterms), FormCalc 9.10, Feynman gauge, electroweak loops, for*)
(*  W+ -> tau+ nu_tau, W+ -> mu+ nu_mu, Z -> nu_tau nubar_tau, Z -> tau- tau+, Z -> b bbar:*)
(*  - 2 Re(M0^* M1)/|M0|^2 of the 1PI vertex plus the vertex counterterm, summed over spins and polarizations;*)
(*  - the counterterm with SM.mod's on-shell field constants (dZW1, dZZZ1, dZAZ1, dZfL1, dZfR1) and the coupling*)
(*    constants dZe1 = dSW1 = 0: the couplings are then MS-bar (their counterterms are pure poles, whose finite part at*)
(*    LoopTools' Delta = 0 is 0), i.e. the scheme of the note's UFO, whose field constants are on-shell too;*)
(*  - the IR divergences with the photon mass lambda^2 = mu^2 (dimensional regularization at mu, massive charged*)
(*    particles), the IR pole from lambda^2 = 2 mu^2 (wud_madloop_ref.wl).*)
(*The point of the UFO (nlo_ckm_ctparams.wl), mu = 91 and 500 GeV.  Writes results/ext_formcalc.csv.*)
(*Batch:  wolframscript -file ext_formcalc.wl  (in its own kernel: the patched FeynArts of FeynCalc must not be loaded)*)


Get["FeynArts`"];
Get["FormCalc`"];
$CKM = True;
t0EF$ = AbsoluteTime[];
srcDirEF$ = DirectoryName[$InputFileName];
resDirEF$ = FileNameJoin[{srcDirEF$, "results"}];
workDirEF$ = CreateDirectory[];
SetDirectory[workDirEF$];
SetOptions[InsertFields, Model -> "SM", GenericModel -> "Lorentz", InsertionLevel -> {Particles}];
denRulesEF$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
vStdEF$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
vNumEF$ = N[vStdEF$, 30];
valEF$ = Module[{e = Sqrt[4 Pi/128], mz = 91, mw = 80, sw, m},
   sw = Sqrt[1 - mw^2/mz^2];
   m = <|"MZ" -> mz, "MW" -> mw, "MH" -> 125, "MT" -> 165, "MB" -> 286/100, "MC" -> 619/1000, "MS" -> 546/10000,
     "MD" -> 271/10000, "MU" -> 127/10000, "ML" -> 1746/1000, "MM" -> 1027/10000, "ME" -> 487/1000000|>;
   Join[m, Association[(# <> "2" -> m[#]^2) & /@ Keys[m]],
    <|"EL" -> e, "Alfa" -> e^2/(4 Pi), "Alfa2" -> e^4/(4 Pi)^2, "SW" -> sw, "CW" -> mw/mz, "SW2" -> sw^2,
     "CW2" -> mw^2/mz^2, "Finite" -> 1|>]];
byNameEF$ = s_Symbol /; KeyExistsQ[valEF$, SymbolName[s]] :> valEF$[SymbolName[s]];
ckmEF$ = {Conjugate[(c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer]] :> Conjugate[vNumEF$[[i, j]]],
   (c_Symbol /; SymbolName[c] === "CKMC")[i_Integer, j_Integer] :> Conjugate[vNumEF$[[i, j]]],
   (c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer] :> vNumEF$[[i, j]]};
numEF$[x_] := Module[{y = (x //. Subexpr[] //. Abbr[]) /. denRulesEF$, left},
   y = y /. ckmEF$ //. byNameEF$;
   left = Union[Cases[y, s_Symbol /; ! MemberQ[{"System`"}, Context[s]] && ! NumericQ[s], Infinity]];
   If[left =!= {}, Print["   symbols left before N: ", left]];
   N[y]];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.];
sumOverEF$[x_] := Expand[x] /. Times[a___, SumOver[g_, n_Integer, ___], b___] :> Sum[Times[a, b], {g, 1, n}];

procsEF$ = <|"w_taunu" -> ({-V[3]} -> {-F[2, {3}], F[1, {3}]}), "w_munu" -> ({-V[3]} -> {-F[2, {2}], F[1, {2}]}),
   "z_nunu" -> ({V[2]} -> {F[1, {3}], -F[1, {3}]}), "z_tautau" -> ({V[2]} -> {F[2, {3}], -F[2, {3}]}),
   "z_bb" -> ({V[2]} -> {F[4, {3}], -F[4, {3}]})|>;
_Hel = 0;
evalSqEF$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];
(* per process: the squared matrix elements (tree, vertex, counterterm) and the renormalization constants *)
dataEF$ = Association[KeyValueMap[Function[{name, proc}, name -> Module[{tree, vert, ct, hel, col, nd, rc, sq},
      ClearProcess[];
      tree = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateTopologies[0, 1 -> 2], proc]], FermionChains -> VA];
      nd = Length[CreateFeynAmp[InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], proc]]];
      vert = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
           proc]], Dimension -> D, FermionChains -> VA];
      ct = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateCTTopologies[1, 1 -> 2, ExcludeTopologies -> {TadpoleCTs,
             WFCorrectionCTs}], proc]], FermionChains -> VA];
      hel = HelicityME[tree, Join[tree, vert, ct]];
      col = ColourME[tree, Join[tree, vert, ct]];
      sq = Table[(PolarizationSum[evalSqEF$[SquaredME[tree, a]] /. hel /. col] //. Subexpr[] //. Abbr[]), {a, {tree, vert, ct}}];
      (* the renormalization constants of the counterterm: in terms of loop integrals only *)
      rc = Cases[Flatten[{CalcRenConst[FindRenConst[ct]] //. Subexpr[] //. Abbr[]} /. RenConstList[_][x___] :> {x}], _Rule | _RuleDelayed];
      rc = (#[[1]] -> (#[[2]] //. rc)) & /@ rc;
      Print["   ", name, ": ", nd, " vertex diagrams;  renormalization constants ", Union[Replace[#, h_[__] :> h] & /@ rc[[All, 1]]], ";  ",
        Round[AbsoluteTime[] - t0EF$], " s"];
      ClearProcess[];
      <|"sq" -> sq, "rc" -> rc|>]], procsEF$]];

(* MS-bar couplings: dZe1 = dSW1 = 0 *)
deltaEF$[name_, mu_, lam2_] := Module[{d = dataEF$[name], rc, b0, wv, wc},
   SetMudim[N[mu^2]]; SetLambda[N[lam2]];
   rc = Join[{dZe1 -> 0, dSW1 -> 0}, (#[[1]] -> numEF$[#[[2]]]) & /@ DeleteCases[d["rc"], (dZe1 | dSW1) -> _]];
   b0 = numEF$[d["sq"][[1]]]; wv = numEF$[d["sq"][[2]]]; wc = numEF$[sumOverEF$[d["sq"][[3]]] /. rc];
   2 Re[wv + wc]/b0];
rowsEF$ = {};
Do[Module[{f1 = deltaEF$[name, mu, mu^2], f2 = deltaEF$[name, mu, 2 mu^2]},
   Print["   ", name, "  mu = ", mu, ":  2 Re(M0^* M1)/|M0|^2 = ", ToString[NumberForm[f1, 16]], ",  IR pole ", ToString[NumberForm[(f2 - f1)/Log[2], 12]]];
   AppendTo[rowsEF$, {name, mu, ToString[CForm[f1]], ToString[CForm[(f2 - f1)/Log[2]]]}]],
  {name, Keys[procsEF$]}, {mu, {91, 500}}];
(* UV finiteness: Delta = 1000 against 0 (the MS-bar couplings' poles are not in the counterterm, so only the field
   constants and the vertex enter: the difference is the UV pole of the coupling counterterms, printed for the record) *)
uvEF$ = Table[Module[{a, b}, SetDelta[1000.]; a = deltaEF$[name, 91, 91^2]; SetDelta[0.]; b = deltaEF$[name, 91, 91^2];
    name -> (a - b)/1000], {name, Keys[procsEF$]}];
Print["UV check, ((Delta = 1000) - (Delta = 0))/1000: the UV pole without the MS-bar coupling counterterms, i.e. minus their pole ",
  "(W: 2 x 19/12 g^2/K = ", N[2 19/12 valEF$["EL"]^2/valEF$["SW"]^2/(16 Pi^2)], "): ", uvEF$];
Export[FileNameJoin[{resDirEF$, "ext_formcalc.csv"}], Prepend[rowsEF$, {"process", "mu", "delta_fin", "delta_IRpole"}], "CSV"];
Print["written: results/ext_formcalc.csv;  ", Round[AbsoluteTime[] - t0EF$], " s"];
ResetDirectory[];
Quiet[DeleteDirectory[workDirEF$, DeleteContents -> True]];
