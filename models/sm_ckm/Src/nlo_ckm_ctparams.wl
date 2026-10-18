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

(* the four-point R2 vertices of NLOCT (generated/SM_CKM_R2.m) as numbers at the point: FeynRules' WriteUFO does not finish
   splitting them symbolically (the largest, W W G+ G-, expands to 3e6 leaves in 64 loop-particle sets).  Each vertex is
   written as sum over (loop particles IPL, structure ME/IndexDelta/Eps, coupling order) of a complex CT parameter FJR2...
   times that structure; the order (QED a, QCD b) is read off from the powers of ee, the Yukawa couplings, lam (QED) and
   gs (QCD; gs^b is kept in the vertex, the parameter carries the QED order).  R2 terms are finite and do not depend on
   MU_R. *)
(* N must not turn the integers of Index[Gluon, Ext[1]] into reals (MadGraph then reads the colour structure
   Identity(1.,2.) and stops; environment notes, SM) *)
SetAttributes[{Index, Ext}, NHoldAll];
r2allCP$ = Get[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_R2.m"}]];
r2fourCP$ = Select[r2allCP$, Length[#[[1]]] == 4 &];
vevCP$ = 2 MW sw/ee;
r2NumRules$ = Join[{yup -> Sqrt[2] MU/vevCP$, yc -> Sqrt[2] MC/vevCP$, yt -> Sqrt[2] MT/vevCP$, ydo -> Sqrt[2] MD/vevCP$,
    ys -> Sqrt[2] MS/vevCP$, yb -> Sqrt[2] MB/vevCP$, ye -> Sqrt[2] Me/vevCP$, ym -> Sqrt[2] MMU/vevCP$, ytau -> Sqrt[2] MTA/vevCP$,
    lam -> MH^2/(2 vevCP$^2), gs -> Sqrt[4 Pi 118/1000], s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dCKM -> 1147/1000},
   Flatten[Table[ToExpression["CKM" <> ToString[i] <> "x" <> ToString[j]] -> vStdCP$[[i, j]], {i, 3}, {j, 3}]]];
structQ$[x_] := MatchQ[x, (IPL | ME | IndexDelta | Eps)[__] | Power[(IPL | ME | IndexDelta | Eps)[__], _]];
r2fourOut$ = {};
r2fourCount$ = 0;
r2keys$ = {};
(* the names follow the groups of the main point (generated/SM_CKM_FJctpar.m, "r2keys"); with ms0 the same names are used *)
r2mainKeys$ = If[ms0CP$, Association[Reverse /@ Get[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJctpar.m"}]]["r2keys"]], <||>];
Do[Module[{x = v[[2]], xs, terms, groups, newExpr = 0},
   (* scale the couplings to read off the orders, then numbers *)
   xs = x /. {ee -> tt$ ee, yup -> tt$ yup, yc -> tt$ yc, yt -> tt$ yt, ydo -> tt$ ydo, ys -> tt$ ys, yb -> tt$ yb, ye -> tt$ ye,
       ym -> tt$ ym, ytau -> tt$ ytau, lam -> tt$^2 lam, gs -> uu$ gs};
   xs = Expand[N[xs //. r2NumRules$ /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ} /. extCP$, 30]];
   terms = If[Head[xs] === Plus, List @@ xs, {xs}];
   groups = GroupBy[terms, Function[tm, Module[{f = If[Head[tm] === Times, List @@ tm, {tm}]},
        {Times @@ Select[f, structQ$], {Exponent[tm, tt$], Exponent[tm, uu$]}}]] -> Function[tm,
       tm /. {(IPL | ME | IndexDelta | Eps)[__] -> 1, tt$ -> 1, uu$ -> 1}], Total];
   KeyValueMap[Function[{key, c}, Module[{cc = Chop[c, 10^-28], name},
       If[cc != 0,
        r2fourCount$++;
        name = If[ms0CP$, Lookup[r2mainKeys$, Key[{v[[1]], key}], Print["   an R2 group that the main point does not have: ", v[[1, All, 1]]]; Abort[]],
          "FJRtwo" <> ToString[r2fourCount$]];
        AppendTo[r2keys$, name -> {v[[1]], key}];
        (* the QCD order is carried by gs^b kept in the vertex, the QED order by the parameter *)
        AppendTo[parsCP$, {name, {QED, key[[2, 1]]}, 0, cc/N[Sqrt[4 Pi 118/1000], 30]^key[[2, 2]], False, key[[2]]}];
        newExpr += ToExpression[name] gs^key[[2, 2]] key[[1]]]]], groups];
   AppendTo[r2fourOut$, {v[[1]], newExpr}]], {v, r2fourCP$}];
Print["four-point R2 vertices: ", Length[r2fourCP$], " -> CT parameters ", r2fourCount$, " (orders ",
  Union[Select[parsCP$, StringStartsQ[#[[1]], "FJRtwo"] &][[All, 6]]], ")"];

(* numbers as sums of 7-digit integers times powers of ten (MadGraph keeps 7 significant digits of each number) *)
pyNum$[x_] := Module[{y = N[x, 30], e, m, a, b, c},
   If[y == 0, Return["0."]];
   e = Floor[Log10[Abs[y]]] - 16;
   m = Round[Abs[y]/10^e];                      (* 17 digits *)
   {a, b, c} = {Quotient[m, 10^10], Quotient[Mod[m, 10^10], 10^3], Mod[m, 10^3]};
   "(" <> If[y < 0, "-", ""] <> "(" <> StringRiffle[MapThread[ToString[#1] <> ".*1e" <> ToString[#2] &, {{a, b, c}, e + {10, 3, 0}}], " + "] <> "))"];
pyNumC$[z_] := If[Im[z] == 0, pyNum$[Re[z]], "(" <> pyNum$[Re[z]] <> " + complex(0,1)*" <> pyNum$[Im[z]] <> ")"];
valueCP$[p_] /; StringStartsQ[p[[1]], "FJRtwo"] := "{0:'" <> pyNumC$[p[[4]]] <> "'}";
valueCP$[p_] := Module[{pole = p[[3]], fin = p[[4]], runs = p[[5]], d},
   d = {};
   If[pole != 0, AppendTo[d, "-1:'" <> pyNum$[pole] <> "'"]];
   If[fin != 0 || (runs && pole != 0), AppendTo[d, "0:'" <> pyNum$[fin] <> If[runs && pole != 0,
       " + " <> pyNum$[pole] <> "*reglog(MU_R**2/" <> ToString[mu0CP$^2] <> ".)", ""] <> "'"]];
   "{" <> StringRiffle[d, ","] <> "}"];
Print["  check of the 7-digit split: ", Max[Abs[(ToExpression[StringReplace[pyNum$[#], {"e" -> "*^", ".*" -> "*"}]] - #)/#] & /@
     Select[Flatten[Re[parsCP$[[All, 3 ;; 4]]]], # != 0 &]] // N];

(* the UFO's CT_parameters.py *)
ctParText$[vals_] := "# This file was generated by nlo_ckm_ctparams.wl: the counterterm parameters of the CKM NLO UFO\n" <>
   "# (MS-bar FJ parameter constants, the CKM counterterm, the on-shell field constants, dvT; numbers at the note's point" <>
   If[ms0CP$, " with m_s = 0", ""] <> ",\n# poles in 1/eps and finite parts at the scale MU_R)\n\n" <>
   "from object_library import all_CTparameters, CTParameter\n\n" <>
   "from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot, reglog\n\n" <>
   StringJoin[(#[[1]] <> " = CTParameter(name = '" <> #[[1]] <> "',\n    type = 'real',\n    value = " <> #[[2]] <>
        ",\n    texname = '" <> #[[1]] <> "')\n\n") & /@ vals];
(* the four-point R2 numbers are finite and do not depend on MU_R: they are ordinary internal parameters of the UFO
   (R2four_parameters.py), not CT parameters (MadGraph's UFO reader scans every CT coupling against every CT parameter
   with a regular expression; with 1137 more CT parameters it did not finish loading the model in 48 minutes) *)
r2ParText$[vals_] := "# This file was generated by nlo_ckm_ctparams.wl: the four-point R2 vertices of NLOCT as numbers at the note's point" <>
   If[ms0CP$, " with m_s = 0", ""] <> "\n# (internal parameters of the UFO, used by CT_couplings.py)\n\n" <>
   "from object_library import all_parameters, Parameter\n\n" <>
   StringJoin[(#[[1]] <> " = Parameter(name = '" <> #[[1]] <> "',\n    nature = 'internal',\n    type = 'complex',\n    value = '" <> #[[2]] <>
        "',\n    texname = '" <> #[[1]] <> "')\n\n") & /@ vals];
isR2$[name_] := StringStartsQ[name, "FJRtwo"];
valueR2$[p_] := pyNumC$[p[[4]]];
If[ms0CP$,
  (* the names of the main point; the values of this one, 0 where this point has none *)
  Module[{main = Get[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJctpar.m"}]]["values"][[All, 1]],
    here = Association[(#[[1]] -> If[isR2$[#[[1]]], valueR2$[#], valueCP$[#]]) & /@ parsCP$]},
   If[! SubsetQ[main, Keys[here]], Print["   names that the main point does not have: ", Complement[Keys[here], main]]; Abort[]];
   Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_CT_parameters_ms0.py"}],
    ctParText$[(# -> Lookup[here, #, "{0:'0.'}"]) & /@ Select[main, ! isR2$[#] &] /. Rule -> List], "Text"];
   Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_R2four_parameters_ms0.py"}],
    r2ParText$[(# -> Lookup[here, #, "0."]) & /@ Select[main, isR2$] /. Rule -> List], "Text"];
   Print["written: generated/SM_CKM_CT_parameters_ms0.py, SM_CKM_R2four_parameters_ms0.py (", Length[main], " parameters, ",
     Length[main] - Length[here], " zero here)"]];
  Abort[]];

(* FeynRules: the parameters as external real parameters with their coupling orders (block FJCT; moved to CT_parameters.py
   by nlo_ckm_ufo.wl) *)
frCP$ = "(* generated by nlo_ckm_ctparams.wl: the counterterm parameters of the CKM NLO UFO as FeynRules parameters *)\n\nM$Parameters = {\n" <>
   StringRiffle[MapIndexed[Function[{p, i},
      "  " <> p[[1]] <> " == {\n    ParameterType -> External,\n    BlockName -> FJCT,\n    OrderBlock -> " <> ToString[i[[1]]] <>
       ",\n    Value -> " <> ToString[i[[1]]] <> "/1000,\n    InteractionOrder -> {" <> ToString[p[[2, 1]]] <> ", " <>
       ToString[p[[2, 2]]] <> "},\n    Description -> \"FJ counterterm parameter\"}"], parsCP$], ",\n"] <> "\n};\n";
Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJct.fr"}], frCP$, "Text"];
Put[<|"rules" -> rulesCP$, "values" -> ((#[[1]] -> valueCP$[#]) & /@ parsCP$), "numbers" -> parsCP$, "mu0" -> mu0CP$, "r2four" -> r2fourOut$,
   "r2keys" -> r2keys$|>,
  FileNameJoin[{srcDirCP$, "generated", "SM_CKM_FJctpar.m"}]];
Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_CT_parameters.py"}], ctParText$[{#[[1]], valueCP$[#]} & /@ Select[parsCP$, ! isR2$[#[[1]]] &]], "Text"];
Export[FileNameJoin[{srcDirCP$, "generated", "SM_CKM_R2four_parameters.py"}], r2ParText$[{#[[1]], valueR2$[#]} & /@ Select[parsCP$, isR2$[#[[1]]] &]], "Text"];
Print["written: generated/SM_CKM_FJct.fr, generated/SM_CKM_FJctpar.m, generated/SM_CKM_CT_parameters.py, generated/SM_CKM_R2four_parameters.py"];
