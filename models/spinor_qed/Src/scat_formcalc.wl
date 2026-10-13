(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop e+ e- -> mu+ mu- with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (4); independent of FeynCalc.  Run in its own kernel: the patched (FeynCalc) and*)
(*unpatched FeynArts must not be loaded together.  Feynman gauge (the FeynRules model), e = 1, m_e = mu = 1, m_mu = 1.7.*)
(**)
(*CalcFeynAmp with Dimension -> D keeps the loop momentum and the Dirac algebra inside the loop in D dimensions and adds the*)
(*rational terms of the UV poles (FormCalc's symbol Finite, set to 1); HelicityME then forms the spin sums in four*)
(*dimensions.  This is the scheme of FormCalc (four-dimensional external states), not CDR: a pole c Delta times the tree*)
(*gives c Delta B(4) here and c Delta B(D) = c Delta B(4) - 8 c e^4 in CDR (App. H).  The UV poles cancel against the*)
(*counterterms in both schemes, so the MS-bar results differ only through the IR pole:*)
(*  K W(FormCalc) - K W(CDR) = 8 e^4 (IR pole of K W)/B(4)   class by class (Eq. (17)).*)
(*(a) the six one-loop diagrams, computed one by one and classified by their loop functions.*)
(*(b) the tree: 16 x FormCalc's |M0|^2 = B(4) (HelicityME with _Hel = 0 uses (pslash + m)/2 per fermion, i.e. 1/16 of the*)
(*    spin sum, so W = 16 x SquaredME[M0, M1]; SquaredME[a, b] is a^* b).*)
(*(c) LoopTools at the points of scat_feyncalc.wl (f): {UV pole, IR pole, MS-bar finite part} of K W per class*)
(*    VP = W_VPe + W_VPmu - delta3 B(4),  Le = W_Ve + (R_e - 1) B(4),  Lmu likewise,  box,  total,*)
(*    with R_f - 1 = (e^2/K) [2 B1 + 1 + 2 m^2 (2 B1' + 4 B0')] (B1 = B1(m^2; m^2, 0); the rational 1 from (D-4) times the UV*)
(*    pole of B1; the derivatives are UV finite).  UV pole from Delta = 1 minus Delta = 0, IR pole from LoopTools' lambda^2 = -1*)
(*    without the UV part (SetUVDiv[0]), finite part at Delta = lambda^2 = 0, mu = 1.  -> results/scat_formcalc.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_formcalc.wl  (in its own kernel: the patched FeynArts of FeynCalc must not be loaded).  Interactive:  ~/hep/bin/wopen scat_formcalc.wl  (in its own kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirFC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelFC$ = FileNameJoin[{srcDirFC$, "generated", "SpinorQED_FA", "SpinorQED_FA"}];   (* FeynRules output, unpatched *)
workDirFC$ = CreateDirectory[];
SetDirectory[workDirFC$];   (* FormCalc writes its FORM files here *)
(* FormCalc's auxiliary denominators: IGram[x] = 1/x, Den[p, m] = 1/(p - m), Den[p, m, d] = 1/(p - m)^d *)
denRulesFC$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
procFC$ = {F[1], -F[1]} -> {F[2], -F[2]};   (* e-(p1) e+(p2) -> mu-(k1) mu+(k2): FormCalc's k[1], k[2], k[3], k[4] *)
diag0FC$ = InsertFields[CreateTopologies[0, 2 -> 2], procFC$, InsertionLevel -> {Particles}, Model -> modelFC$,
   GenericModel -> modelFC$];
diag1FC$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procFC$,
   InsertionLevel -> {Particles}, Model -> modelFC$, GenericModel -> modelFC$];


(* ::Section:: *)
(*(a) the six one-loop diagrams*)


(* ::Subsubsection:: *)
(*Inspect: the diagrams (unpatched FeynArts)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diag1FC$, ColumnsXRows -> {3, 2}, Numbering -> Simple, DisplayFunction -> Identity]]
]


tree0FC$ = CalcFeynAmp[CreateFeynAmp[diag0FC$] /. M$FACouplings, FermionChains -> VA];
nDiagFC$ = Length[CreateFeynAmp[diag1FC$]];
ampsFC$ = Table[CalcFeynAmp[CreateFeynAmp[DiagramExtract[diag1FC$, i]] /. M$FACouplings, Dimension -> D,
     FermionChains -> VA], {i, nDiagFC$}];
(* classes by the loop functions: a D function -> box; no C function -> vacuum polarization (flavour of the B0(S) loop);
   otherwise the vertex whose C0 starts with m_e^2 or m_mu^2 *)
classOfFC$[a_] := Which[
   ! FreeQ[a, D0i], "box",
   FreeQ[a, C0i], If[! FreeQ[a, B0i[_, S, Me^2, Me^2]], "VPe", "VPmu"],
   ! FreeQ[a, C0i[_, Me^2, S, Me^2, __]], "Ve",
   True, "Vmu"];
classesFC$ = classOfFC$ /@ ampsFC$;
Print["(a) number of one-loop diagrams (expect 6): ", nDiagFC$, ";  classes: ", classesFC$];
Print["(a) loop functions per diagram: ",
  Union[Cases[#, (h : A0 | A0i | B0i | C0i | D0i)[id_, ___] :> {h, id}, Infinity]] & /@ ampsFC$ // Short[#, 8] &];


(* ::Subsubsection:: *)
(*Inspect: the amplitude of a vertex diagram (spinor chains abbreviated F1, F2, ...)*)


If[$Notebooks,
  {ampsFC$[[Position[classesFC$, "Ve"][[1, 1]]]], Select[Abbr[], ! FreeQ[#, DiracChain] &]}
]


(* ::Section:: *)
(*(b) the tree and the spin sums*)


_Hel = 0;
evalSqFC$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];
born4FC$ = Simplify[16 evalSqFC$[SquaredME[tree0FC$, tree0FC$]] /. HelicityME[tree0FC$, tree0FC$] //. Subexpr[] //. Abbr[] /.
     denRulesFC$ /. {Alfa -> 1/(4 Pi), Alfa2 -> 1/(4 Pi)^2, U -> 2 Me^2 + 2 MMU^2 - S - T}];
born4HandFC$ = 8/S^2 ((T - Me^2 - MMU^2)^2 + (U - Me^2 - MMU^2)^2 + 2 S (Me^2 + MMU^2)) /. U -> 2 Me^2 + 2 MMU^2 - S - T;
Print["(b) 16 |M0|^2 (FormCalc) - B(4) (e = 1) = ", Simplify[born4FC$ - born4HandFC$], "  (expect 0)"];
helFC$ = HelicityME[tree0FC$, Join @@ ampsFC$];   (* all Mat[F_1, F_i] of the six diagrams at once *)
interfFC$ = Table[evalSqFC$[SquaredME[tree0FC$, ampsFC$[[i]]]], {i, nDiagFC$}];   (* SquaredME[a, b] = a^* b: M0^* M1 *)
Print["(b) helicity matrix elements: ", Length[helFC$]];


(* ::Subsubsection:: *)
(*Inspect: the interference of a vertex diagram before the numbers*)


If[$Notebooks,
  interfFC$[[Position[classesFC$, "Ve"][[1, 1]]]] // Short[#, 20] &
]


(* ::Section:: *)
(*(c) LoopTools values*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[1];
KK = (4 Pi)^2;
massFC$ = {Me -> 1, MMU -> 17/10};
(* the same rational (s, t) as scat_feyncalc.wl (f) *)
physPtsFC$ = {{16, -6}, {16, -3}, {16, -1}, {36, -20}, {36, -8}, {36, -1}, {100, -70}, {100, -30}, {100, -5}};
(* K W at e = 1 for one kinematic point; fin = 1 keeps FormCalc's rational terms, fin = 0 drops them (for poles) *)
numFC$[x_, {sv_, tv_}, fin_] := Module[{uv = 2 + 2 (17/10)^2 - sv - tv},
   KK 16 N[(x /. helFC$ //. Subexpr[] //. Abbr[]) /. denRulesFC$ /. {Alfa -> 1/(4 Pi), Alfa2 -> 1/(4 Pi)^2, Finite -> fin} /.
       massFC$ /. {S -> N[sv], T -> N[tv], U -> N[uv]}]];
(* R_f - 1 (Feynman gauge, before -delta2) in K/e^2 units, four-dimensional external states *)
rMinus1FC$[m_, fin_] := 2 B0i[bb1, m^2, m^2, 0] + fin + 2 m^2 (2 B0i[dbb1, m^2, m^2, 0] + 4 B0i[dbb0, m^2, m^2, 0]);
classNamesFC$ = {"VP", "Le", "Lmu", "box"};
(* K W per class at one point and one LoopTools setting (VP: the counterterm -delta3 B(4) only has a Delta pole) *)
classValuesFC$[pt_, fin_, delta_] := Module[{w = numFC$[#, pt, fin] & /@ interfFC$, b4 = N[born4HandFC$ /. massFC$ /. {S -> pt[[1]], T -> pt[[2]]}]},
   {Total[Pick[w, classesFC$, "VPe" | "VPmu"]] + 8/3 delta b4,
    Total[Pick[w, classesFC$, "Ve"]] + N[rMinus1FC$[1, fin]] b4,
    Total[Pick[w, classesFC$, "Vmu"]] + N[rMinus1FC$[17/10, fin]] b4,
    Total[Pick[w, classesFC$, "box"]]}];
rowsFC$ = Table[Module[{sv, tv, fin0, fin1, ir, b4, rs, c, e, p, k},
     {sv, tv} = pt; rs = Sqrt[sv]; e = rs/2; p = Sqrt[e^2 - 1]; k = Sqrt[e^2 - (17/10)^2];
     c = (tv - 1 - (17/10)^2 + 2 e^2)/(2 p k);
     b4 = N[born4HandFC$ /. massFC$ /. {S -> sv, T -> tv}];
     SetLambda[0]; SetUVDiv[1];
     SetDelta[0]; fin0 = classValuesFC$[pt, 1, 0];
     SetDelta[1]; fin1 = classValuesFC$[pt, 1, 1];
     SetDelta[0]; SetLambda[-1]; SetUVDiv[0]; ir = classValuesFC$[pt, 0, 0];
     SetLambda[0]; SetUVDiv[1];
     {N[rs], N[c], N[sv], N[tv], b4, Append[#, Total[#]] & /@ Chop[{fin1 - fin0, ir, fin0}, 10^-12]}], {pt, physPtsFC$}];
Print["(c) UV pole of the classes VP, Le, Lmu, box with the counterterms (expect 0): ", Chop[Max[Abs[#[[6, 1]]]] & /@ rowsFC$, 10^-10]];
Do[Print["(c) sqrt(s) = ", r[[1]], ", t = ", r[[4]], ":  IR pole (VP, Le, Lmu, box, total) = ", r[[6, 2]], ";  finite = ", r[[6, 3]]],
  {r, rowsFC$}];


(* ::Subsubsection:: *)
(*Inspect: the values*)


If[$Notebooks,
  TableForm[Flatten[Table[{classNamesFC$ ~Join~ {"total"} // #[[i]] &, r[[1]], r[[4]], r[[6, 2, i]], r[[6, 3, i]]}, {r, rowsFC$}, {i, 5}], 1],
    TableHeadings -> {None, {"class", "sqrt s", "t", "IR pole", "finite"}}]
]


resultsDirFC$ = FileNameJoin[{srcDirFC$, "results"}];
Quiet[CreateDirectory[resultsDirFC$]];
strFC$[x_] := ToString[CForm[N[x]]];
csvLinesFC$ = Flatten[Table[StringRiffle[Join[{Append[classNamesFC$, "total"][[i]]}, strFC$ /@ r[[1 ;; 4]],
       strFC$ /@ Flatten[ReIm[r[[6, All, i]]]]], ","], {r, rowsFC$}, {i, 5}]];
Export[FileNameJoin[{resultsDirFC$, "scat_formcalc.csv"}],
  StringRiffle[Prepend[csvLinesFC$, "class,rs,cos,s,t,re_uv,im_uv,re_ir,im_ir,re_fin,im_fin"], "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[csvLinesFC$], " rows to results/scat_formcalc.csv (K W/e^6 at e = 1, FormCalc scheme)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it closes LoopTools and removes FormCalc's work directory.*)


Uninstall[Links["*LoopTools*"]];
ResetDirectory[];
DeleteDirectory[workDirFC$, DeleteContents -> True];
