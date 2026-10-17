(* ::Package:: *)

(* ::Title:: *)
(*Step (9a): nu_e nubar_e -> nu_mu nubar_mu at one loop with the unpatched FeynArts 3.12 and FormCalc 9.10 (Feynman gauge)*)


(* ::Text:: *)
(*Independent of FeynCalc (run in its own kernel: the patched FeynArts of FeynCalc must not be loaded).  The note's*)
(*FeynArts model (FeynRules output, generated/SM_FA), Feynman gauge (FeynArts' default GaugeRules), all fermions massless*)
(*except the top, the tadpoles attached through the zero-momentum H line included (FJ).  CalcFeynAmp with*)
(*Dimension -> D (rational terms of the UV poles, Finite -> 1), FermionChains -> VA, spin sums with HelicityME (_Hel = 0:*)
(*1/16 of the sum).  The external neutrinos: FormCalc's FieldRC (Denner: dZ^L = -Re Sigma^L(0)), dZ^L/2 per leg.*)
(*MS-bar: LoopTools with Delta = 0 at mu (the poles are the MS-bar counterterms).  Inputs and point as nunu_numeric.wl.*)
(*Writes results/nunu_formcalc.csv: W(MS-bar) = sum_spins M0^* M1 and B4 = sum_spins |M0|^2 at mu = MZ and 500 GeV.*)
(*Batch: wolframscript -file nunu_formcalc.wl*)


Get["FeynArts`"];
Get["FormCalc`"];
t0$ = AbsoluteTime[];
srcDirFC$ = DirectoryName[$InputFileName];
modelFC$ = FileNameJoin[{srcDirFC$, "generated", "SM_FA", "SM_FA"}];
workDirFC$ = CreateDirectory[];
SetDirectory[workDirFC$];
SetOptions[InsertFields, Model -> modelFC$, GenericModel -> modelFC$, InsertionLevel -> {Particles}];
denRulesFC$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
procFC$ = {F[1, {1}], -F[1, {1}]} -> {F[1, {2}], -F[1, {2}]};

(* massless fermions except the top; Yukawa couplings from the masses (note Eq. (masses)) *)
light0FC$ = {MU -> 0, MC -> 0, MD -> 0, MS -> 0, MB -> 0, Me -> 0, MMU -> 0, MTA -> 0};
yukFC$ = {yu[3, 3] -> Sqrt[2] MT/vev, yu[_, _] -> 0, yd[_, _] -> 0, yl[_, _] -> 0};
parFC$ = {lam -> MH^2/(2 vev^2)};

(* the neutrino field constants {dZ^L, dZ^R} first: FieldRC starts a process of its own and clears the abbreviations *)
dzL$ = FieldRC[F[1, {1}]][[1]] /. M$FACouplings /. yukFC$ /. parFC$ /. light0FC$;
dzLm$ = FieldRC[F[1, {2}]][[1]] /. M$FACouplings /. yukFC$ /. parFC$ /. light0FC$;
{dzL$, dzLm$} = {dzL$, dzLm$} //. Subexpr[] //. Abbr[];
ClearProcess[];   (* FormCalc computes one process per session otherwise (DeclareProcess::incomp) *)
diag0FC$ = InsertFields[CreateTopologies[0, 2 -> 2], procFC$];
topsVS$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections, Boxes}];
topsBox$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections, Tadpoles, SelfEnergies, Triangles}];
diagVS$ = InsertFields[topsVS$, procFC$]; diagBox$ = InsertFields[topsBox$, procFC$];
calc$[d_] := CalcFeynAmp[CreateFeynAmp[d] /. M$FACouplings /. yukFC$ /. parFC$ /. light0FC$, Dimension -> D,
   FermionChains -> VA];
tree$ = CalcFeynAmp[CreateFeynAmp[diag0FC$] /. M$FACouplings /. light0FC$, FermionChains -> VA];
vs$ = calc$[diagVS$]; box$ = calc$[diagBox$];
Print["(a) diagrams: tree ", Length[CreateFeynAmp[diag0FC$]], ", self-energy, vertex and tadpole ", Length[CreateFeynAmp[diagVS$]],
  ", boxes ", Length[CreateFeynAmp[diagBox$]], ";  ", Round[AbsoluteTime[] - t0$], " s"];

_Hel = 0;
evalSqFC$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];
hel$ = HelicityME[tree$, Join[tree$, vs$, box$]];
sq$[a_, b_] := 16 evalSqFC$[SquaredME[a, b]];
b4$ = sq$[tree$, tree$]; wVS$ = sq$[tree$, vs$]; wBox$ = sq$[tree$, box$];
Print["(b) spin sums and FieldRC;  ", Round[AbsoluteTime[] - t0$], " s;  B4 = ",
  InputForm[Simplify[b4$ /. hel$ /. denRulesFC$]]];

Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
sqs$ = 500; th$ = Pi/3;
valFC$ = Module[{e = Sqrt[4 Pi/128], mz = 911876/10000, mw = 80369/1000, mh = 1252/10, mt = 17257/100, sw, v},
   sw = Sqrt[1 - mw^2/mz^2]; v = 2 mw sw/e;
   <|"EL" -> e, "MZ" -> mz, "MW" -> mw, "MH" -> mh, "MT" -> mt, "MZ2" -> mz^2, "MW2" -> mw^2, "MH2" -> mh^2, "MT2" -> mt^2,
    "Alfa" -> e^2/(4 Pi), "Alfa2" -> e^4/(4 Pi)^2, "sw" -> sw, "cw" -> mw/mz, "vev" -> v, "lam" -> mh^2/(2 v^2),
    "Finite" -> 1, "S" -> sqs$^2, "T" -> -sqs$^2 (1 - Cos[th$])/2, "U" -> -sqs$^2 (1 + Cos[th$])/2,
    "MB" -> 0, "MC" -> 0, "MS" -> 0, "MD" -> 0, "MU" -> 0, "MTA" -> 0, "MMU" -> 0, "Me" -> 0,
    "MB2" -> 0, "MC2" -> 0, "MS2" -> 0, "MD2" -> 0, "MU2" -> 0, "MTA2" -> 0, "MMU2" -> 0, "Me2" -> 0|>];
byName$ = s_Symbol /; KeyExistsQ[valFC$, SymbolName[s]] :> valFC$[SymbolName[s]];
numFC$[x_] := Module[{y = (x /. hel$ //. Subexpr[] //. Abbr[]) /. denRulesFC$ /. yukFC$ /. parFC$, left},
   y = y //. byName$;
   left = Union[Cases[y, s_Symbol /; !MemberQ[{"System`"}, Context[s]] && !NumericQ[s], Infinity]];
   If[left =!= {}, Print["   symbols left before N: ", left]];
   N[y]];
rows$ = Table[Module[{b4, wvs, wbox, dz, dzm, w},
    SetMudim[N[mu0]^2]; SetDelta[0];
    b4 = numFC$[b4$]; wvs = numFC$[wVS$]; wbox = numFC$[wBox$];
    dz = numFC$[dzL$]; dzm = numFC$[dzLm$];
    w = wvs + wbox + (dz + dzm) b4;   (* dZ^L/2 for each of the four legs *)
    Print["(c) mu = ", mu0, ":  B4/4 = ", NumberForm[b4/4, 16], ";  W = ", w, " (self-energy+vertex+tadpole ", wvs,
      ", boxes ", wbox, ", legs ", (dz + dzm) b4, ")"];
    {mu0, b4, Re[w], Im[w], Re[wvs], Re[wbox], Re[(dz + dzm) b4]}], {mu0, {911876/10000, 500}}];
Export[FileNameJoin[{srcDirFC$, "results", "nunu_formcalc.csv"}],
  Prepend[N[rows$], {"mu", "B4", "re_W_MSbar", "im_W_MSbar", "re_W_vs_tad", "re_W_box", "re_W_legs"}], "CSV"];
ResetDirectory[];
Quiet[DeleteDirectory[workDirFC$, DeleteContents -> True]];
Print["total ", Round[AbsoluteTime[] - t0$], " s"];
