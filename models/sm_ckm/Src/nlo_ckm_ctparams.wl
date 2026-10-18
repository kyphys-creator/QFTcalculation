(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 6 of 7: the counterterm parameters of the CKM NLO UFO (numbers at the note's point)*)


(* ::Text:: *)
(*As the SM note's nlo_ctparams.wl, but the constants are numbers at one point (the light quarks are massive; see*)
(*nlo_ckm_dz.wl): the UFO is valid for the param_card of that point, with MU_R free.  The constants:*)
(*  - NLOCT's on-shell field constants (nlo_ckm_dz.wl; the off-diagonal quark ones complex), the Goldstone ones 0;*)
(*  - the MS-bar (FJ) parameter constants FR$delta[{p}] and the CKM counterterm dV (pure poles; nlo_ckm_fjdelta.wl);*)
(*  - the tadpole shift dvT = T/MH^2.*)
(*Each becomes real CT parameters (real and imaginary parts; electroweak and QCD parts separately, coupling order QED 2*)
(*or QCD 2, dvT QED 1) with the value {-1: pole, 0: finite(91 GeV) + pole ln(MU_R^2/91^2)} (each pole comes with*)
(*ln mu^2, nlo_ckm_dz.wl).  The numbers are written as sums of 7-digit integers times powers of ten: MadGraph writes the*)
(*numbers of a UFO expression into Fortran with 7 significant digits (environment notes).*)
(*Writes Src/generated/SM_CKM_FJct.fr, Src/generated/SM_CKM_FJctpar.m and the UFO's CT_parameters.py*)
(*(Src/generated/SM_CKM_CT_parameters.py, copied into the UFO by nlo_ckm_ufo.wl).  Batch: wolframscript -file nlo_ckm_ctparams.wl*)
(*With the argument ms0: the same point with m_s = 0 (SM_CKM_dZ_ms0.m): only SM_CKM_CT_parameters_ms0.py, with the*)
(*names of the main point (the UFO's couplings are the same; a constant that vanishes here is written as 0), for a copy of*)
(*the UFO used by the flavour-changing processes of steps (7), (8), which have m_s = 0.*)


srcDirCP$ = DirectoryName[$InputFileName];
ms0CP$ = Length[$ScriptCommandLine] >= 2 && $ScriptCommandLine[[2]] === "ms0";
dzCP$ = Get[FileNameJoin[{srcDirCP$, "generated", If[ms0CP$, "SM_CKM_dZ_ms0.m", "SM_CKM_dZ.m"]}]];
fdCP$ = Get[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJdelta.m"}]];
mu0CP$ = dzCP$["mu0"];
KK = 16 Pi^2;
(* the point (as nlo_ckm_dz.wl); the UFO's external parameters *)
vStdCP$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
extCP$ = {aEWM1 -> 128, ee -> Sqrt[4 Pi/128], MZ -> 91, MW -> 80, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000,
   MS -> If[ms0CP$, 0, 546/10000], MD -> 271/10000, MU -> 127/10000, MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
(* aS is kept: the QCD parts are split off first *)
exactCP$[x_] := x /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ} /. CKM[i_, j_] :> vStdCP$[[i, j]] /. extCP$ /. FR$MU -> mu0CP$;
numCP$[x_] := N[exactCP$[x], 40];
splitCP$[x_] := Module[{y = Expand[x /. aS -> gs^2/(4 Pi)]},
   If[Expand[y - Coefficient[y, gs, 0] - gs^2 Coefficient[y, gs, 2]] =!= 0, Print["   not of order gs^0 + gs^2"]];
   {Coefficient[y, gs, 0], gs^2 Coefficient[y, gs, 2] /. gs -> Sqrt[4 Pi 118/1000]}];
laurCP$[x_] := Module[{y = Normal[Series[x, {FR$Eps, 0, 0}]]}, {Coefficient[y, FR$Eps, -1], Coefficient[y, FR$Eps, 0]}];

(* the CT parameters: {name, {order, power}, pole, finite at mu0}, real *)
parsCP$ = {};
rulesCP$ = {};
(* runs: the constant is computed from loop integrals at the scale mu (field constants, dvT), its finite part is then
   finite(mu0) + pole ln(mu^2/mu0^2); the MS-bar constants (FR$delta, dV) are pure poles at every scale *)
addParCP$[name_, ord_, {pole_, fin_}, runs_ : True] := Module[{p = Chop[N[pole, 40], 10^-35], f = Chop[N[fin, 40], 10^-35], out = 0},
   If[Re[p] != 0 || Re[f] != 0, AppendTo[parsCP$, {name <> "re", ord, Re[p], Re[f], runs}]; out += ToExpression[name <> "re"]];
   If[Im[p] != 0 || Im[f] != 0, AppendTo[parsCP$, {name <> "im", ord, Im[p], Im[f], runs}]; out += I ToExpression[name <> "im"]];
   out];
(* the field constants *)
nameZ$[FR$deltaZ[{f1_, f2_}, {{}}]] := "FJdZ" <> ToString[f1] <> ToString[f2];
nameZ$[FR$deltaZ[{f1_, f2_}, {{}}, ch_]] := "FJdZ" <> ToString[f1] <> ToString[f2] <> ToString[ch];
Do[Module[{k = r[[1]], v = r[[2]], n},
   n = nameZ$[k];
   AppendTo[rulesCP$, k -> addParCP$[n, {QED, 2}, v[[1 ;; 2]]] + addParCP$[n <> "qcd", {QCD, 2}, v[[3 ;; 4]]]]],
  {r, dzCP$["dZ"]}];
Print["field constants: ", Length[dzCP$["dZ"]], " -> CT parameters ", Length[parsCP$], " (imaginary parts: ",
  Count[parsCP$[[All, 1]], s_ /; StringEndsQ[s, "im"]], ")"];
(* the MS-bar parameter constants (pure poles), EW and QCD parts.  As in the SM note, FR$delta[{aEWM1}] = -2 aEWM1 FJdlne and
   FR$delta[{aS}] = 2 aS FJdlngs (FJdlne = de/e of order e^2, FJdlngs = dgs/gs of order gs^2: the coupling orders of the
   counterterm vertices are then those of the tree vertex plus 2) *)
deltaOf$[p_] := FR$delta[{p}, {}] /. fdCP$["delta"];
qcdSplit$[x_] := splitCP$[PowerExpand[x /. aS -> gs^2/(4 Pi)]];
Module[{pl},
  pl = laurCP$[numCP$[deltaOf$[aEWM1]/(-2 aEWM1)] /. aEWM1 -> 128];
  If[pl[[2]] =!= 0, Print["   aEWM1: the MS-bar constant has a finite part"]];
  AppendTo[rulesCP$, FR$delta[{aEWM1}, {}] -> -2 aEWM1 addParCP$["FJdlne", {QED, 2}, {pl[[1]], 0}, False]];
  pl = laurCP$[N[PowerExpand[exactCP$[deltaOf$[aS]/(2 aS)] /. aS -> gs^2/(4 Pi)] /. gs -> Sqrt[4 Pi 118/1000], 40]];
  If[pl[[2]] =!= 0, Print["   aS: the MS-bar constant has a finite part"]];
  AppendTo[rulesCP$, FR$delta[{aS}, {}] -> 2 aS addParCP$["FJdlngs", {QCD, 2}, {pl[[1]], 0}, False]]];
Do[Module[{x = exactCP$[deltaOf$[p]], n = "FJd" <> ToString[p], pl, sp},
   pl = laurCP$[x];
   If[pl[[2]] =!= 0, Print["   ", p, ": the MS-bar constant has a finite part"]];
   sp = qcdSplit$[pl[[1]]];
   AppendTo[rulesCP$, FR$delta[{p}, {}] -> addParCP$[n, {QED, 2}, {sp[[1]], 0}, False] + addParCP$[n <> "qcd", {QCD, 2}, {sp[[2]], 0}, False]]],
  {p, {MZ, MW, MH, MT, MB, MC, MS, MD, MU, MTA, MMU, Me}}];
(* the CKM counterterm dV (pure poles, EW) *)
Do[Module[{x = laurCP$[numCP$[fdCP$["dV"][[i, j]]]]},
   AppendTo[rulesCP$, dVsym[Index[Generation, i], Index[Generation, j]] ->
     addParCP$["FJdV" <> ToString[i] <> ToString[j], {QED, 2}, {x[[1]], 0}, False]]], {i, 3}, {j, 3}];
(* dvT *)
(* with m_s = 0, the m_s^4 ln m_s^2 of T is its limit 0 (m_s = 10^-20 GeV) *)
dvtCP$ = laurCP$[numCP$[fdCP$["dvT"] /. If[ms0CP$, MS -> 10^-20, {}]]];
AppendTo[rulesCP$, FJdvT -> addParCP$["FJdvT", {QED, 1}, dvtCP$]];
Print["CT parameters: ", Length[parsCP$], " (", Count[parsCP$[[All, 2, 1]], QCD], " QCD)"];
Print["  dV poles (K x): ", N[KK numCP$[fdCP$["dV"]] FR$Eps // Simplify, 6] // MatrixForm // ToString];
Print["  dvT: pole ", N[dvtCP$[[1]], 10], ", finite (91 GeV) ", N[dvtCP$[[2]], 10]];

(* numbers as sums of 7-digit integers times powers of ten (MadGraph keeps 7 significant digits of each number) *)
pyNum$[x_] := Module[{y = N[x, 30], e, m, a, b, c},
   If[y == 0, Return["0."]];
   e = Floor[Log10[Abs[y]]] - 16;
   m = Round[Abs[y]/10^e];                      (* 17 digits *)
   {a, b, c} = {Quotient[m, 10^10], Quotient[Mod[m, 10^10], 10^3], Mod[m, 10^3]};
   "(" <> If[y < 0, "-", ""] <> "(" <> StringRiffle[MapThread[ToString[#1] <> ".*1e" <> ToString[#2] &, {{a, b, c}, e + {10, 3, 0}}], " + "] <> "))"];
valueCP$[p_] := Module[{pole = p[[3]], fin = p[[4]], runs = p[[5]], d},
   d = {};
   If[pole != 0, AppendTo[d, "-1:'" <> pyNum$[pole] <> "'"]];
   If[fin != 0 || (runs && pole != 0), AppendTo[d, "0:'" <> pyNum$[fin] <> If[runs && pole != 0,
       " + " <> pyNum$[pole] <> "*reglog(MU_R**2/" <> ToString[mu0CP$^2] <> ".)", ""] <> "'"]];
   "{" <> StringRiffle[d, ","] <> "}"];
Print["  check of the 7-digit split: ", Max[Abs[(ToExpression[StringReplace[pyNum$[#], {"e" -> "*^", ".*" -> "*"}]] - #)/#] & /@
     Select[Flatten[parsCP$[[All, 3 ;; 4]]], # != 0 &]] // N];

(* the UFO's CT_parameters.py *)
ctParText$[vals_] := "# This file was generated by nlo_ckm_ctparams.wl: the counterterm parameters of the CKM NLO UFO\n" <>
   "# (MS-bar FJ parameter constants, the CKM counterterm, the on-shell field constants, dvT; numbers at the note's point" <>
   If[ms0CP$, " with m_s = 0", ""] <> ",\n# poles in 1/eps and finite parts at the scale MU_R)\n\n" <>
   "from object_library import all_CTparameters, CTParameter\n\n" <>
   "from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot, reglog\n\n" <>
   StringJoin[(#[[1]] <> " = CTParameter(name = '" <> #[[1]] <> "',\n    type = 'real',\n    value = " <> #[[2]] <>
        ",\n    texname = '" <> #[[1]] <> "')\n\n") & /@ vals];
If[ms0CP$,
  (* the names of the main point; the values of this one, 0 where this point has none *)
  Module[{main = Get[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJctpar.m"}]]["values"][[All, 1]], here = Association[(#[[1]] -> valueCP$[#]) & /@ parsCP$]},
   If[! SubsetQ[main, Keys[here]], Print["   names that the main point does not have: ", Complement[Keys[here], main]]; Abort[]];
   Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_CT_parameters_ms0.py"}], ctParText$[(# -> Lookup[here, #, "{0:'0.'}"]) & /@ main /. Rule -> List], "Text"];
   Print["written: generated/SM_CKM_CT_parameters_ms0.py (", Length[main], " parameters, ", Length[main] - Length[here], " zero here)"]];
  Abort[]];

(* FeynRules: the parameters as external real parameters with their coupling orders (block FJCT; moved to CT_parameters.py
   by nlo_ckm_ufo.wl) *)
frCP$ = "(* generated by nlo_ckm_ctparams.wl: the counterterm parameters of the CKM NLO UFO as FeynRules parameters *)\n\nM$Parameters = {\n" <>
   StringRiffle[MapIndexed[Function[{p, i},
      "  " <> p[[1]] <> " == {\n    ParameterType -> External,\n    BlockName -> FJCT,\n    OrderBlock -> " <> ToString[i[[1]]] <>
       ",\n    Value -> " <> ToString[i[[1]]] <> "/1000,\n    InteractionOrder -> {" <> ToString[p[[2, 1]]] <> ", " <>
       ToString[p[[2, 2]]] <> "},\n    Description -> \"FJ counterterm parameter\"}"], parsCP$], ",\n"] <> "\n};\n";
Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJct.fr"}], frCP$, "Text"];
Put[<|"rules" -> rulesCP$, "values" -> ((#[[1]] -> valueCP$[#]) & /@ parsCP$), "numbers" -> parsCP$, "mu0" -> mu0CP$|>,
  FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJctpar.m"}]];
Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_CT_parameters.py"}], ctParText$[{#[[1]], valueCP$[#]} & /@ parsCP$], "Text"];
Print["written: generated/SM_CKM_FJct.fr, generated/SM_CKM_FJctpar.m, generated/SM_CKM_CT_parameters.py"];
