(* ::Package:: *)

(* ::Title:: *)
(*Step (6): the real emission e+ e- -> mu+ mu- gamma with FeynArts + FeynCalc*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (6).  e-(p1) e+(p2) -> mu-(k1) mu+(k2) gamma(k3), m = m_e, M = m_mu, four dimensions.*)
(*(a) FeynArts: 4 tree diagrams (photon from e-, e+, mu-, mu+).*)
(*(b) Ward identity: with the photon polarization replaced by k3 the spin-summed |M|^2 vanishes, so the polarization sum*)
(*    may be taken as -g (App. H); the -g sum equals the sum over the two transverse polarizations (auxiliary vector p1).*)
(*    Dot products are reduced to the independent p1.p2, p1.k3, p2.k3, k1.k3, p1.k1 by momentum conservation.*)
(*(c) the spin and polarization sum, in the scalar products p_i.p_j; the propagator denominators are written as*)
(*    p1.k3, p2.k3, k1.k3, k2.k3 (the fermion propagators), s and Q^2 = (k1 + k2)^2 (the photon); FeynCalc writes*)
(*    (p1 - k3)^2 - m^2 through k1, k2, p2 by momentum conservation, which is replaced by -2 p1.k3 (no cancellation near the*)
(*    collinear peak).  Written as a Python function to Src/generated/msq_eemumua.py (250 monomials, integer coefficients)*)
(*    for xsec_numeric.py, which checks it against explicit spinors and MadGraph's standalone matrix element.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file real_feyncalc.wl  (run generate_SpinorQED.wl first).  Interactive:  ~/hep/bin/wopen real_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirRE$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirRE$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRE$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirRE$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRE$, "SpinorQED_FA"}], Quiet -> True];
modelRE$ = FileNameJoin[{modelTmpDirRE$, "SpinorQED_FA", "SpinorQED_FA"}];


(* ::Section:: *)
(*(a) diagrams*)


diag3$ = InsertFields[CreateTopologies[0, 2 -> 3], {F[1], -F[1]} -> {F[2], -F[2], V[1]}, InsertionLevel -> {Particles},
   Model -> modelRE$, GenericModel -> modelRE$];


(* ::Subsubsection:: *)
(*Inspect: the four diagrams*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diag3$, ColumnsXRows -> {4, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


Print["(a) number of diagrams (expect 4): ", Length[CreateFeynAmp[diag3$]]];
amp3$ = FCFAConvert[CreateFeynAmp[diag3$] /. M$FACouplings, IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2, k3},
   ChangeDimension -> 4, List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] /. FCGV["EL"] -> EL;
(* no TransversePolarizationVectors: with it FeynCalc drops eps.k3 terms during the Dirac algebra, the amplitude then no
   longer satisfies k3.M = 0 and the -g polarization sum is wrong (15.10 instead of 12.79 at a test point) *)
FCClearScalarProducts[];
SP[p1, p1] = Me^2; SP[p2, p2] = Me^2; SP[k1, k1] = MMU^2; SP[k2, k2] = MMU^2; SP[k3, k3] = 0;


(* ::Section:: *)
(*(b) Ward identity and the polarization sum*)


dotRulesRE$ = {SP[k1, k2] -> k1k2, SP[k1, k3] -> k1k3, SP[k1, p1] -> p1k1, SP[k1, p2] -> p2k1, SP[k2, k3] -> k2k3,
   SP[k2, p1] -> p1k2, SP[k2, p2] -> p2k2, SP[k3, p1] -> p1k3, SP[k3, p2] -> p2k3, SP[p1, p2] -> p1p2};
(* momentum conservation p1 + p2 = k1 + k2 + k3 with k2^2 = M^2, k3^2 = 0: the independent p1p2, p1k3, p2k3, k1k3, p1k1 *)
indepRE$ = Module[{pk1 = (2 p1p2 + 2 Me^2 - 2 (p1k3 + p2k3) + 2 k1k3)/2},   (* (p1 + p2).k1 *)
   {k2k3 -> p1k3 + p2k3 - k1k3, k1k2 -> pk1 - MMU^2 - k1k3, p2k1 -> pk1 - p1k1,
    p1k2 -> Me^2 + p1p2 - p1k1 - p1k3, p2k2 -> p1p2 + Me^2 - (pk1 - p1k1) - p2k3}];
reduceRE$[x_] := Simplify[(FCE[FeynAmpDenominatorExplicit[x] // ExpandScalarProduct] /. dotRulesRE$) /. indepRE$];
(* the photon polarization vector replaced by k3 *)
ward$ = FCI[amp3$] /. Momentum[Polarization[k3, ___], ___] :> Momentum[k3];
wardSq$ = FermionSpinSum[ComplexConjugate[ward$] ward$, ExtraFactor -> 1] // DiracSimplify // Contract;
Print["(b) sum_spins |M(eps -> k3)|^2 (expect 0): ", reduceRE$[wardSq$]];
spinSum$ = FermionSpinSum[ComplexConjugate[amp3$] amp3$, ExtraFactor -> 1] // DiracSimplify;
msqG$ = DoPolarizationSums[spinSum$, k3, 0] // Contract // FeynAmpDenominatorExplicit // ExpandScalarProduct // FCE;
msqT$ = DoPolarizationSums[spinSum$, k3, p1] // Contract // FeynAmpDenominatorExplicit // ExpandScalarProduct // FCE;
Print["(b) -g sum minus transverse sum (expect 0): ", reduceRE$[msqG$ - msqT$]];


(* ::Section:: *)
(*(c) the spin and polarization sum as a Python function*)


(* the propagator denominators by symbols: rk1 = 1/k1.k3, rk2 = 1/k2.k3, rp1 = 1/p1.k3, rp2 = 1/p2.k3, rqq = 1/Q^2, rss = 1/s;
   longer sums first (Plus is Orderless and Flat: a shorter pattern would match inside a longer sum) *)
denRE$[x_] := Which[
   x === 2 k1k2 + 2 k1k3 + 2 k2k3 + 2 MMU^2, 1/rss,
   x === 2 k1k2 + 2 MMU^2 - 2 p2k1 - 2 p2k2, -2/rp1,
   x === 2 k1k2 + 2 MMU^2, 1/rqq,
   x === k1k3, 1/rk1, x === k2k3, 1/rk2, x === p2k3, 1/rp2, x === p1k3, 1/rp1,
   True, x];
msqSym$ = Expand[(msqG$ /. dotRulesRE$) /. Power[x_, n_?Negative] :> Power[denRE$[x], n]];
Print["(c) monomials: ", Length[msqSym$], ";  symbols: ", Union[Cases[msqSym$, _Symbol, Infinity]],
  ";  coefficients integer: ", AllTrue[Cases[msqSym$, n_?NumericQ, {2}], IntegerQ]];


(* ::Subsubsection:: *)
(*Inspect: the terms with the most singular denominators*)


If[$Notebooks,
  Select[List @@ msqSym$, ! FreeQ[#, rp1^2 | rk1^2] &] // TraditionalForm
]


pyStrRE$[t_] := StringReplace[ToString[FortranForm[t]], {"MMU" -> "mm", "Me" -> "me", "EL" -> "el"}];
pyLinesRE$ = Join[
   {"# msq_eemumua.py -- written by real_feyncalc.wl (research note models/spinor_qed, step (6)); do not edit.",
    "# sum over spins and polarizations of |M(e-(p1) e+(p2) -> mu-(k1) mu+(k2) gamma(k3))|^2, four dimensions, e = el.",
    "# Arguments: the dot products (floats or numpy arrays) and me, mm, el; rp1 = 1/p1.k3, rp2 = 1/p2.k3, rk1 = 1/k1.k3,",
    "# rk2 = 1/k2.k3, rqq = 1/(k1 + k2)^2, rss = 1/s.",
    "",
    "def msq(p1p2, p1k1, p1k2, p1k3, p2k1, p2k2, p2k3, k1k2, k1k3, k2k3, me, mm, el):",
    "    rp1, rp2, rk1, rk2 = 1.0 / p1k3, 1.0 / p2k3, 1.0 / k1k3, 1.0 / k2k3",
    "    rqq, rss = 1.0 / (2 * k1k2 + 2 * mm ** 2), 1.0 / (2 * p1p2 + 2 * me ** 2)",
    "    s = 0.0"},
   ("    s = s + " <> pyStrRE$[#]) & /@ (List @@ msqSym$),
   {"    return s", ""}];
Export[FileNameJoin[{srcDirRE$, "generated", "msq_eemumua.py"}], StringRiffle[pyLinesRE$, "\n"], "Text"];
Print["(c) wrote generated/msq_eemumua.py (", Length[msqSym$], " monomials)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it removes the temporary model copy.*)


DeleteDirectory[modelTmpDirRE$, DeleteContents -> True];
