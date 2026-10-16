(* ::Package:: *)

(* ::Title:: *)
(*Step (6): one-loop e- e+ -> mu- mu+ in the Standard Model with FeynArts' SM.mod and FormCalc (on-shell, alpha(0))*)


(* ::Text:: *)
(*Research note models/sm, step (6).  Run in its own kernel (unpatched FeynArts 3.12, FormCalc 9.10).  SM.mod: Denner's*)
(*conventions, Feynman gauge, CKM = 1, on-shell renormalization with alpha(0) (dZe1 = -(dZAA1 + SW/CW dZZA1)/2), tadpoles*)
(*cancelled by dTH1 (the note's delta t = -T) and left out of the self-energies.  All fermion masses are kept (the electron*)
(*and muon masses regulate nothing: the photon is massless, the soft poles are dimensionally regularized).*)
(*  tree:  the s-channel gamma, Z, H, G0 diagrams;*)
(*  loop:  all one-loop diagrams without tadpoles and without self-energies on the external legs, CalcFeynAmp with*)
(*         Dimension -> D and PaVeReduce -> True (the tensor coefficients reduced to A0, B0, C0, D0: the C0 of this LoopTools*)
(*         build are wrong below threshold, so all loop functions are evaluated with COLLIER as well, eemm_collier.f90);*)
(*  ct:    the counterterm diagrams, with the renormalization constants of CalcRenConst.*)
(*W = sum over all spins of M0^* M1 (= 16 x FormCalc's SquaredME with _Hel = 0, which uses (pslash + m)/2 per fermion),*)
(*B = sum over all spins of |M0|^2.  MadLoop returns born = B/4 and the virtual Re W/2 (spin average 1/4, 2 Re).*)
(*For each point W = c_0 + sum_i c_i f_i (f_i the loop functions, Finite the marker of FormCalc's rational terms); the*)
(*coefficients go to results/eemm_coeffs.csv and the functions with their LoopTools values (finite part at Delta = 0,*)
(*mu = MZ, lambda^2 = 0; UV coefficient from Delta = 1 minus Delta = 0; IR coefficient from lambda^2 = -1 without the UV part)*)
(*to results/eemm_functions.csv.  eemm_numeric.py combines them with COLLIER's values.  Two sets of masses: the note's*)
(*point (files without suffix) and, as a cross-check, heavier leptons m_e = 2, m_mu = 3 GeV (files *_heavy); the amplitudes*)
(*are computed once.  Points: work/eemm_points{,_heavy}.csv (sqrt(s), cos(theta), s, t; eemm_numeric.py --points).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file eemm_formcalc.wl  (in its own kernel).  Interactive:  ~/hep/bin/wopen eemm_formcalc.wl  (in its own kernel), then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];
(* argument massless: MadGraph's electroweak NLO models (massless fermions but the top).  The masses must vanish before the
   amplitudes are reduced: with m_e kept symbolic, the reduction of B1(m_e^2; ...) etc. carries 1/m_e^2 and gives 0/0 at
   m_e = 0.  The scalar couplings of the light fermions are left out (SM.mod's NoLightFHCoupling; their counterterms carry
   dMf1/Mf).  Without it: the note's point and the heavier leptons. *)
masslessEF$ = MemberQ[$ScriptCommandLine, "massless"];   (* wolframscript drops arguments that start with "--" *)
If[masslessEF$, ME = MM = ML = MU = MC = MD = MS = MB = 0; ME2 = MM2 = ML2 = MU2 = MC2 = MD2 = MS2 = MB2 = 0];
restrEF$ = If[masslessEF$, Restrictions -> NoLightFHCoupling, Restrictions -> {}];
srcDirEF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirEF$ = CreateDirectory[];
SetDirectory[workDirEF$];   (* FormCalc writes its FORM files here *)
procEF$ = {F[2, {1}], -F[2, {1}]} -> {F[2, {2}], -F[2, {2}]};   (* e-(k1) e+(k2) -> mu-(k3) mu+(k4) *)


(* ::Section:: *)
(*(a) diagrams and amplitudes*)


t0EF$ = AbsoluteTime[];
d0EF$ = Quiet[InsertFields[CreateTopologies[0, 2 -> 2], procEF$, Model -> SM, restrEF$], RuleDelayed::rhs];
d1EF$ = Quiet[InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procEF$, Model -> SM,
    restrEF$], RuleDelayed::rhs];
dctEF$ = Quiet[InsertFields[CreateCTTopologies[1, 2 -> 2, ExcludeTopologies -> {TadpoleCTs, WFCorrectionCTs}], procEF$,
    Model -> SM, restrEF$], RuleDelayed::rhs];
treeEF$ = CalcFeynAmp[CreateFeynAmp[d0EF$], FermionChains -> Chiral];
loopEF$ = CalcFeynAmp[CreateFeynAmp[d1EF$], Dimension -> D, FermionChains -> Chiral, PaVeReduce -> True];
ctEF$ = CalcFeynAmp[CreateFeynAmp[dctEF$], FermionChains -> Chiral];
Print["(a) diagrams (classes): tree ", Length[CreateFeynAmp[d0EF$]], ", one loop ", Length[CreateFeynAmp[d1EF$]],
  ", counterterms ", Length[CreateFeynAmp[dctEF$]], ";  ", Round[AbsoluteTime[] - t0EF$], " s"];


(* ::Section:: *)
(*(b) spin sums*)


_Hel = 0;
(* one HelicityME per pair: with the three amplitudes joined into one Amp, HelicityME finds no matrix elements *)
helEF$ = Union[HelicityME[treeEF$, treeEF$], HelicityME[treeEF$, loopEF$], HelicityME[treeEF$, ctEF$]];
evalSqEF$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];
bornEF$ = 16 evalSqEF$[SquaredME[treeEF$, treeEF$]];
wLoopEF$ = 16 evalSqEF$[SquaredME[treeEF$, loopEF$]];
wCtEF$ = 16 evalSqEF$[SquaredME[treeEF$, ctEF$]];
Print["(b) helicity matrix elements: ", Length[helEF$], ";  ", Round[AbsoluteTime[] - t0EF$], " s"];
abbrEF$ = Abbr[]; subEF$ = Subexpr[];
(* CalcRenConst only now: it clears the abbreviations of the process (the spinor chains F1, F2, ... become Removed[F1]) *)
rcEF$ = Flatten[Quiet[CalcRenConst[ctEF$]] /. RenConstList[RenConst] -> List];
Print["(b) renormalization constants: ", rcEF$[[All, 1]]];
(* the schemes of MadGraph's electroweak NLO models (massless leptons and light quarks; Denner's signs):
   alpha(MZ):  delta Z_e -> delta Z_e - Delta alpha/2,  Delta alpha = Pi_light(0) - Re Pi_light(MZ^2),
               Pi_f(k^2) = (alpha/4 Pi)(4/3) Nc Q^2 [B0(k^2, 0, 0) - 1/3] for a massless fermion, Pi_f(0) with B0(0, 0, 0);
               light = all fermions but the top: sum Nc Q^2 = 20/3;
   G_mu:       delta Z_e -> delta Z_e - Delta r/2 with Delta r of step (5) (FormCalc's constants, Sirlin's term);
   the Born has two e vertices, so W -> W - B Delta alpha  or  W - B Delta r. *)
sW0EF$ = Quiet[SelfEnergy[V[3] -> V[3], 0, ExcludeTopologies -> Internal]];
dalphaEF$ = Alfa/(4 Pi) (4/3) (20/3) (B0i[bb0, 0, 0, 0] - Re[B0i[bb0, MZ2, 0, 0]] + 1/3);
drEF$ = (sW0EF$ - dMWsq1)/MW2 + 2 dZe1 - 2 dSW1/SW + dZZA1/(SW CW) + Alfa/(4 Pi SW2) (6 + (7 - 4 SW2)/(2 SW2) Log[CW2]);
DumpSave[FileNameJoin[{srcDirEF$, "work", If[masslessEF$, "eemm_amp_ml.mx", "eemm_amp.mx"]}],
  {treeEF$, loopEF$, ctEF$, helEF$, bornEF$, wLoopEF$, wCtEF$, rcEF$, abbrEF$, subEF$, sW0EF$}];


(* ::Section:: *)
(*(c) numbers: the coefficients of the loop functions at each point*)


mzEF$ = 911880/10000; mwEF$ = 803692/10000; mhEF$ = 12520/100;
massPhysEF$ = <|{2, 1} -> 51099895/10^11, {2, 2} -> 1056583755/10^10, {2, 3} -> 177686/10^5,
   {3, 1} -> 216/10^5, {3, 2} -> 12730/10^4, {3, 3} -> 17257/100,
   {4, 1} -> 470/10^5, {4, 2} -> 935/10^4, {4, 3} -> 4183/10^3|>;
(* the cross-check with heavier leptons (m_e = 2, m_mu = 3 GeV): MadLoop's closed-form counterterms of a symbolic UFO
   stay accurate there (nlo_ufo.wl) *)
massHeavyEF$ = Join[massPhysEF$, <|{2, 1} -> 2, {2, 2} -> 3|>];
(* MadGraph's electroweak NLO models (restrict_default): all fermions massless but the top *)
massMlEF$ = Join[massPhysEF$, <|{2, 1} -> 0, {2, 2} -> 0, {2, 3} -> 0, {3, 1} -> 0, {3, 2} -> 0, {4, 1} -> 0, {4, 2} -> 0, {4, 3} -> 0|>];
massEF$ = massPhysEF$;
mfEF[1, _] := 0; mfEF[t_, g_] := massEF$[{t, g}];
cwEF$ = mwEF$/mzEF$; swEF$ = Sqrt[1 - cwEF$^2]; alEF$ = 1000000000/137035999177;
alMZEF$ = 100/12893;   (* alpha(MZ) scheme: aEWM1 = 128.93 *)
gfEF$ = 11663788/10^12; alGmuEF$ = Sqrt[2] gfEF$ mwEF$^2 (1 - mwEF$^2/mzEF$^2)/Pi;   (* G_mu scheme *)
parOfEF$[alEF$_] := Join[{Alfa -> alEF$, Alfa2 -> alEF$^2, EL -> Sqrt[4 Pi alEF$], MW -> mwEF$, MW2 -> mwEF$^2, MZ -> mzEF$, MZ2 -> mzEF$^2,
    MH -> mhEF$, MH2 -> mhEF$^2, SW -> swEF$, CW -> cwEF$, SW2 -> swEF$^2, CW2 -> cwEF$^2},
   (* names as strings: with --massless the symbols ME, ... are 0, and ToString[ME] <> "2" would give the number 2 *)
   Flatten[MapThread[With[{sym = Symbol[#1], sym2 = Symbol[#1 <> "2"]},
       If[NumericQ[sym], {}, {sym -> mfEF @@ #2, sym2 -> (mfEF @@ #2)^2}]] &,
     {{"ME", "MM", "ML", "MU", "MC", "MT", "MD", "MS", "MB"}, {{2, 1}, {2, 2}, {2, 3}, {3, 1}, {3, 2}, {3, 3}, {4, 1}, {4, 2}, {4, 3}}}]]];
genEF$ = {a_. SumOver[g_, n_, ___] :> Sum[a /. g -> i, {i, n}]};
mfRulesEF$ = {Mf2[t_, g_?NumericQ] :> mfEF[Round[t], Round[g]]^2, Mf[t_, g_?NumericQ] :> mfEF[Round[t], Round[g]],
   CKM[i_, j_] :> KroneckerDelta[i, j],
   CKMC[i_, j_] :> KroneckerDelta[i, j], Conjugate[CKM[i_, j_]] :> KroneckerDelta[i, j]};
denRulesEF$ = {IGram[gg_] :> 1/gg, Den[pp_, mm_, dd_] :> 1/(pp - mm)^dd, Den[pp_, mm_] :> 1/(pp - mm)};
loopFnEF$ = _fA0 | _fA0i | _fB0i | _fC0i | _fD0i;
(* LoopTools evaluates a loop function as soon as its arguments are numbers, with the settings of the moment (Delta = 0,
   lambda^2 = 0), which drops the poles: in the massless sets the scaleless B0(0, 0, 0) (photon self-energy) and, once
   the generation sums turn Mf2[2, 1] into ME2 = 0, B1(0, 0, 0) and DB00(0, 0, 0) of the light-fermion loops in the
   renormalization constants, all Delta_UV - Delta_IR type.  So the loop functions get inert heads before LoopTools is
   installed; (d) gives them back their real heads to evaluate them part by part *)
inertEF$ = {A0 -> fA0, A0i -> fA0i, B0i -> fB0i, C0i -> fC0i, D0i -> fD0i};
{bornEF$, wLoopEF$, wCtEF$, rcEF$, subEF$, abbrEF$, dalphaEF$, drEF$} =
  {bornEF$, wLoopEF$, wCtEF$, rcEF$, subEF$, abbrEF$, dalphaEF$, drEF$} /. inertEF$;
Print["(b) loop functions with numerical arguments already: ",
  Select[Union[Cases[{wLoopEF$, wCtEF$, rcEF$, subEF$, abbrEF$, dalphaEF$, drEF$}, loopFnEF$, Infinity]],
    VectorQ[If[Head[#] === fA0, List @@ #, Rest[List @@ #]], NumericQ] &]];

Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
(* (c) and (d) for one set: tag "" (the note's point, alpha(0)), "_heavy" (heavier leptons, alpha(0)), "_ml_aMZ" and
   "_ml_Gmu" (MadGraph's electroweak models: massless fermions but the top, alpha(MZ) or G_mu); shift is added to W *)
runSetEF$[tag_, masses_, al_, shift_, ptsTag_, label_, amps_] := Block[{massEF$ = masses, parEF$, wAllEF$, bAllEF$, subPrepEF$,
    lfListEF$, nLfEF$, lfVEF$, lfREF$, lfIEF$, reImSymEF$, lfRulesEF$, helPrepEF$, ptsEF$, coeffRowsEF$, fnsEF$, fnTableEF$,
    coeffLinesEF$, rcValsEF$},
   parEF$ = parOfEF$[al];
   Print["(c) ", label];
   (* symbolic preparation, once: the generation sums, the fermion masses, and the loop functions -> lf[j]; the numbers are
      then put into the helicity matrix elements, the subexpressions and the abbreviations before they are substituted, so
      that W becomes a linear form in the lf[j] without expanding a symbolic expression (that took longer than 30 minutes) *)
   t1EF$ = AbsoluteTime[];
   prepEF$[x_] := (x //. genEF$) /. mfRulesEF$;
   wAllEF$ = prepEF$[(amps[[2]] + amps[[3]] + shift) //. rcEF$];
   bAllEF$ = prepEF$[amps[[1]]];
   (* the renormalization constants also sit in the subexpressions of the counterterm amplitude *)
   subPrepEF$ = prepEF$[Join[subEF$, abbrEF$] //. rcEF$];
   lfListEF$ = Union[Cases[{wAllEF$, bAllEF$, subPrepEF$[[All, 2]], helEF$[[All, 2]]}, loopFnEF$, Infinity]];
   (* plain symbols lfV1, lfV2, ... (N would turn an index lf[1] into lf[1.]); lfR.., lfI.. stand for their Re and Im *)
   nLfEF$ = Length[lfListEF$];
   lfVEF$ = Table[Symbol["lfV" <> ToString[j]], {j, nLfEF$}];
   lfREF$ = Table[Symbol["lfR" <> ToString[j]], {j, nLfEF$}];
   lfIEF$ = Table[Symbol["lfI" <> ToString[j]], {j, nLfEF$}];
   reImSymEF$ = Dispatch[Join[Thread[(Re /@ lfVEF$) -> lfREF$], Thread[(Im /@ lfVEF$) -> lfIEF$]]];
   lfRulesEF$ = Dispatch[Thread[lfListEF$ -> lfVEF$]];
   wAllEF$ = wAllEF$ /. lfRulesEF$; subPrepEF$ = subPrepEF$ /. lfRulesEF$; helPrepEF$ = helEF$ /. lfRulesEF$;
   Print["(c) loop functions (symbolic arguments): ", Length[lfListEF$], ";  preparation ", Round[AbsoluteTime[] - t1EF$], " s"];
   numRulesEF$[sv_, tv_] := Join[parEF$, {S -> sv, T -> tv, U -> 2 mfEF[2, 1]^2 + 2 mfEF[2, 2]^2 - sv - tv}];
   numPtEF$[x_, nr_] := N[(x //. genEF$) /. mfRulesEF$ /. nr /. denRulesEF$, 30];
   (* the renormalization constants are real parts of self-energies: Re and Im are distributed over sums and numerical
      factors, and Re[lf[j]], Im[lf[j]] become variables of their own (lfr[j], lfi[j]) *)
   reImEF$ = {Re[x_Plus] :> Re /@ x, Im[x_Plus] :> Im /@ x, Re[c_?NumericQ y_] :> Re[c] Re[y] - Im[c] Im[y],
      Im[c_?NumericQ y_] :> Re[c] Im[y] + Im[c] Re[y]};
   ptsEF$ = Import[FileNameJoin[{srcDirEF$, "work", "eemm_points" <> ptsTag <> ".csv"}], "CSV"][[2 ;;]];
   Print["(c) points (sqrt(s), cos(theta)): ", ptsEF$[[All, 1 ;; 2]]];
   coeffRowsEF$ = {}; fnsEF$ = {};
   Do[Module[{sv = Rationalize[p[[3]], 0], tv = Rationalize[p[[4]], 0], nr, repl, wv, bv, arr, keys, cf, t2 = AbsoluteTime[]},
       nr = numRulesEF$[sv, tv];
       repl = Dispatch[Join[Thread[helPrepEF$[[All, 1]] -> numPtEF$[helPrepEF$[[All, 2]], nr]],
          Thread[subPrepEF$[[All, 1]] -> numPtEF$[subPrepEF$[[All, 2]], nr]]]];
       wv = numPtEF$[wAllEF$ //. repl, nr];
       wv = Expand[(wv //. reImEF$) /. reImSymEF$];
       bv = numPtEF$[bAllEF$ //. repl, nr];
       arr = CoefficientArrays[wv, Join[lfVEF$, lfREF$, lfIEF$, {Finite}]];
       If[Length[arr] > 2, Print["   W is not linear in the loop functions at ", p[[1 ;; 2]]]];
       (* the loop functions with the numbers of this point (arguments to 20 digits; equal ones are merged) *)
       (* inert heads (fA0, fB0i, ...): LoopTools is installed only in (d) *)
       keys = (lfListEF$ /. {A0 -> fA0, A0i -> fA0i, B0i -> fB0i, C0i -> fC0i, D0i -> fD0i} /. nr) /.
         (h : fA0 | fA0i | fB0i | fC0i | fD0i)[args__] :> h @@ (If[NumericQ[#], N[Re[#], 20], #] & /@ {args});
       cf = Normal[arr[[2]]];
       cf = Merge[Thread[Join[keys, reKey /@ keys, imKey /@ keys, {Finite}] -> cf], Total];
       fnsEF$ = Union[fnsEF$, keys];
       AppendTo[coeffRowsEF$, {p, bv, arr[[1]], Normal[cf]}];
       Print["(c) sqrt(s) = ", p[[1]], ", cos = ", p[[2]], ": B = ", N[bv, 12], ";  symbols left in W: ",
         Complement[Union[Cases[wv, _Symbol, Infinity]], Join[lfVEF$, lfREF$, lfIEF$, {Finite}]], ";  ",
         Round[AbsoluteTime[] - t2], " s"]], {p, ptsEF$}];


   (* (d) LoopTools values of the functions and the output *)
   SetMudim[N[mzEF$^2]]; SetDelta[0]; SetLambda[0];
   realHeadEF$ = {fA0 -> A0, fA0i -> A0i, fB0i -> B0i, fC0i -> C0i, fD0i -> D0i};
   ltEval$[f_] := Module[{fin, uv, ir, ir2, g = f /. realHeadEF$},
      SetLambda[0]; SetUVDiv[1]; SetDelta[0]; fin = g;
      SetDelta[1]; uv = (f /. realHeadEF$) - fin;
      SetDelta[0]; SetLambda[-1]; SetUVDiv[0]; ir = f /. realHeadEF$;
      SetLambda[-2]; ir2 = f /. realHeadEF$;
      SetLambda[0]; SetUVDiv[1];
      N[{fin, uv, ir, ir2}]];
   keyEF$[f_] := StringReplace[ToString[InputForm[f, NumberMarks -> False]], {"fA0i[" -> "A0i[", "fA0[" -> "A0[", "fB0i[" -> "B0i[",
        "fC0i[" -> "C0i[", "fD0i[" -> "D0i["}];
   headNameEF$ = <|fA0 -> "A0", fA0i -> "A0i", fB0i -> "B0i", fC0i -> "C0i", fD0i -> "D0i"|>;   (* A0 itself is a pure function *)
   fnTableEF$ = Table[Join[{keyEF$[f], headNameEF$[Head[f]], If[MatchQ[f, _fA0], "aa0", ToString[f[[1]]]]},
        ToString[CForm[#]] & /@ If[MatchQ[f, _fA0], {f[[1]]}, List @@ Rest[f]], {ltEval$[f]}], {f, fnsEF$}];
   strEF$[x_] := ToString[CForm[N[x, 17]]];
   keyFullEF$[reKey[f_]] := "Re:" <> keyEF$[f];
   keyFullEF$[imKey[f_]] := "Im:" <> keyEF$[f];
   keyFullEF$[f_] := keyEF$[f];
   Quiet[CreateDirectory[FileNameJoin[{srcDirEF$, "results"}]]];
   Export[FileNameJoin[{srcDirEF$, "results", "eemm_functions" <> tag <> ".csv"}],
     StringRiffle[Prepend[StringRiffle[Join[{"\"" <> #[[1]] <> "\"", #[[2]], #[[3]], "\"" <> StringRiffle[#[[4 ;; -2]], " "] <> "\""},
           strEF$ /@ Flatten[ReIm[Last[#]]]], ","] & /@ fnTableEF$,
       "key,head,id,args,re_fin_lt,im_fin_lt,re_uv_lt,im_uv_lt,re_ir_lt,im_ir_lt,re_ir2_lt,im_ir2_lt"], "\n"] <> "\n", "Text"];
   coeffLinesEF$ = Flatten[Table[Join[
        {StringRiffle[{strEF$[r[[1, 1]]], strEF$[r[[1, 2]]], "\"born\"", strEF$[Re[r[[2]]]], strEF$[Im[r[[2]]]]}, ","],
         StringRiffle[{strEF$[r[[1, 1]]], strEF$[r[[1, 2]]], "\"const\"", strEF$[Re[r[[3]]]], strEF$[Im[r[[3]]]]}, ","]},
        StringRiffle[{strEF$[r[[1, 1]]], strEF$[r[[1, 2]]], "\"" <> keyFullEF$[#[[1]]] <> "\"", strEF$[Re[#[[2]]]], strEF$[Im[#[[2]]]]}, ","] & /@
         r[[4]]], {r, coeffRowsEF$}]];
   Export[FileNameJoin[{srcDirEF$, "results", "eemm_coeffs" <> tag <> ".csv"}],
     StringRiffle[Prepend[coeffLinesEF$, "rs,cos,key,re,im"], "\n"] <> "\n", "Text"];
   Print["(d) wrote ", Length[fnsEF$], " loop functions to results/eemm_functions" <> tag <> ".csv and ", Length[coeffLinesEF$],
     " coefficients to results/eemm_coeffs" <> tag <> ".csv;  ", Round[AbsoluteTime[] - t0EF$], " s"];


   (* the renormalization constants at the point (finite part: Delta = 0, mu = MZ, lambda^2 = 0, i.e. the soft pole of the
      lepton field constants dimensionally regularized), for the comparison with NLOCT in nlo_ufo.wl *)
   rcValsEF$ = Table[Module[{v = Expand[(r[[2]] //. rcEF$) //. genEF$] /. mfRulesEF$ /. parEF$ /. denRulesEF$ /. Finite -> 1},
        v = N[v, 20] /. realHeadEF$ /. (h : A0 | A0i | B0i | C0i | D0i)[args__] :> h @@ (If[NumericQ[#], N[#], #] & /@ {args});
        {ToString[InputForm[r[[1]]]], N[v]}], {r, rcEF$}];
   Print["(d) renormalization constants (Delta = 0, mu = MZ, dimensionally regularized soft poles dropped): ", InputForm[rcValsEF$]];
   Export[FileNameJoin[{srcDirEF$, "results", "eemm_renconst" <> tag <> ".csv"}],
     StringRiffle[Prepend[StringRiffle[{"\"" <> #[[1]] <> "\"", strEF$[Re[#[[2]]]], strEF$[Im[#[[2]]]]}, ","] & /@ rcValsEF$,
       "name,re,im"], "\n"] <> "\n", "Text"];
   ];
ampsEF$ = {bornEF$, wLoopEF$, wCtEF$};
If[masslessEF$,
  runSetEF$["_ml_aMZ", massMlEF$, alMZEF$, -bornEF$ dalphaEF$, "_ml", "massless fermions but the top, alpha(MZ) (aEWM1 = 128.93)",
    ampsEF$];
  runSetEF$["_ml_Gmu", massMlEF$, alGmuEF$, -bornEF$ drEF$, "_ml", "massless fermions but the top, G_mu (G_F = 1.1663788e-5)",
    ampsEF$],
  runSetEF$["", massPhysEF$, alEF$, 0, "", "the note's point, alpha(0)", ampsEF$];
  runSetEF$["_heavy", massHeavyEF$, alEF$, 0, "_heavy", "heavier leptons (m_e = 2, m_mu = 3 GeV), alpha(0)", ampsEF$]];


(* ::Section:: *)
(*Cleanup*)


Uninstall[Links["*LoopTools*"]];
ResetDirectory[];
DeleteDirectory[workDirEF$, DeleteContents -> True];
