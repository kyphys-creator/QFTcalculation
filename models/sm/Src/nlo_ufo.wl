(* ::Package:: *)

(* ::Title:: *)
(*Step (6), 3 of 3: the NLO UFO of the Standard Model (on-shell, alpha(0)) with NLOCT's counterterm and R2 vertices*)


(* ::Text:: *)
(*FeynRules: read Src/generated/SM_CT.nlo (nlo_nloct.wl), compare NLOCT's two-point counterterms with the note's*)
(*(results/ct_note.m, Eqs. (ct), the delta t = -T scheme of step (4)), set the charge to alpha(0) and write the UFO*)
(*Src/generated/SM_NLO_a0_UFO for MadLoop (overwritten).*)
(*(a) Two-point counterterms at the point of step (3) (Delta = 0, mu = MZ; NLOCT's 1/FR$Eps -> 0, FR$MU -> MZ).  With the*)
(*    vertex forms  V V': I [a (k^mu k^nu - k^2 g^mu nu) + b g^mu nu],  H H: I [c1 k^2 + c0]  (FeynRules' fields = the note's):*)
(*      A A: a = dZAA;   A Z: a = (dZAZ + dZZA)/2, b = MZ^2 dZZA/2;   Z Z: a = dZZZ, b = dMZsq + MZ^2 dZZZ;*)
(*      W W: a = dZW, b = dMWsq + MW^2 dZW;   H H: c1 = dZH, c0 = -(dMHsq + MH^2 dZH).*)
(*    NLOCT cancels the tadpoles with a shift of the Higgs field, H -> H - deltat/MH^2 (its tadpole counterterm vertex is*)
(*    the one-point C[S[1]]); the shift adds -Sigma_tad to the mass terms, so the total b - M^2 a is the note's delta M^2 of*)
(*    the delta t = -T scheme when NLOCT's on-shell conditions use the one-particle-irreducible self-energies.*)
(*    dZW has a soft pole (photon); NLOCT's 1/FR$Eps includes it (FR$IR -> 1), the note's value is taken with LoopTools'*)
(*    lambda^2 = 0, i.e. the same dimensionally regularized finite part.*)
(*(b) alpha(0): NLOCT renormalizes aEWM1 in MS-bar (delta aEWM1 a pure pole).  The on-shell charge constant of the note,*)
(*      delta Z_e = (1/2) Pi^AA(0) + (s/c) Sigma^AZ_T(0)/MZ^2      (Eq. (dZe), Eq. (Pi0)),*)
(*    has the finite part (B0(0, m, m) = Delta - ln(m^2/mu^2))*)
(*      delta Z_e,fin = -(ee^2/(16 Pi^2)) [ (2/3) sum_f Nc Q_f^2 ln(m_f^2/mu^2) - (7/2) ln(MW^2/mu^2) + 1/3 ],*)
(*    and a change delta ee/ee -> delta ee/ee + delta Z_e,fin changes every counterterm vertex by delta Z_e,fin ee dV/dee*)
(*    (V the tree vertex as a function of ee, MW, MZ, MH and the masses: vev = 2 MW sw/ee, y_f = sqrt2 m_f/vev,*)
(*    lam = MH^2/(2 vev^2), gw = ee/sw, g1 = ee/cw; sw and cw depend on MW and MZ only).  The fermion terms carry the loop*)
(*    label IPL[{f}], the bosonic ones IPL[{W}] (WriteUFO turns the labels into the loop_particles of the CT vertices).*)
(*(c) Two UFOs, the note's point (SM_NLO_a0_UFO) and heavier leptons (SM_NLO_a0_heavy_UFO, m_e = 2, m_mu = 3 GeV), with*)
(*    the R2 vertices and the UV vertices as 40-digit numbers at the point (mu_R = MZ); see the comment in (c).*)
(**)
(*Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_ufo.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_ufo.wl  (in a fresh kernel), then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*FeynRules, the model and the NLOCT counterterms*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["SM.fr"];
LoadRestriction[FileNameJoin[{srcDirNU$, "DiagonalCKM.rst"}]];
t0NU$ = AbsoluteTime[];
Get[FileNameJoin[{srcDirNU$, "generated", "SM_CT.nlo"}]];
R2$vertlist = DeleteCases[R2$vertlist, {}];
UV$vertlist = DeleteCases[UV$vertlist, {}];
ctParNU$ = Dispatch[FR$CTparam];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist],
  ";  UV vertices: ", Length[UV$vertlist], ";  CT parameters: ", Length[FR$CTparam], ";  read in ", Round[AbsoluteTime[] - t0NU$], " s"];


(* ::Section:: *)
(*(a) two-point counterterms against the note*)


alNU$ = 1000000000/137035999177; mzNU$ = 911880/10000; mwNU$ = 803692/10000; mhNU$ = 12520/100;
massNU$ = {Me -> 51099895/10^11, MMU -> 1056583755/10^10, MTA -> 177686/10^5, MU -> 216/10^5, MC -> 12730/10^4,
   MT -> 17257/100, MD -> 470/10^5, MS -> 935/10^4, MB -> 4183/10^3};
(* the internal parameters in terms of ee, MW, MZ, MH and the masses (FR$LoopSwitches: MW external) *)
yukNU$ = {ye -> Sqrt[2] Me/vev, ym -> Sqrt[2] MMU/vev, ytau -> Sqrt[2] MTA/vev, yup -> Sqrt[2] MU/vev, yc -> Sqrt[2] MC/vev,
   yt -> Sqrt[2] MT/vev, ydo -> Sqrt[2] MD/vev, ys -> Sqrt[2] MS/vev, yb -> Sqrt[2] MB/vev};
intNU$ = Join[yukNU$, {lam -> MH^2/(2 vev^2), muH -> MH/Sqrt[2], gw -> ee/sw, g1 -> ee/cw}];
vevNU$ = {vev -> 2 MW sw/ee};
pointNU$ = Join[{ee -> Sqrt[4 Pi alNU$], aEWM1 -> 1/alNU$, MW -> mwNU$, MZ -> mzNU$, MH -> mhNU$, cw -> mwNU$/mzNU$,
    sw -> Sqrt[1 - mwNU$^2/mzNU$^2], aS -> 118/1000, gs -> Sqrt[4 Pi 118/1000], FR$MU -> mzNU$}, massNU$];
(* finite part: 1/FR$Eps -> 0 (expressions are at most linear in 1/FR$Eps) *)
(* the Lorentz and spin structures are replaced by symbols first: N would turn Ext[1] into Ext[1.] *)
fvNU$ = {FV[2, Index[Lorentz, Ext[_]]] -> fv, SP[2, 2] -> kk, ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]] -> gg,
   SlashedP[2, Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> pslash, ProjM[Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> pm,
   ProjP[Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> pp,
   TensDot[SlashedP[2], ProjM][Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> pslashm,
   TensDot[SlashedP[2], ProjP][Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> pslashp};
numNU$[v_] := Module[{y = (v //. ctParNU$) /. fvNU$ /. IPL[_] -> 1 //. intNU$ /. vevNU$ /. pointNU$},
   y = Expand[N[y /. FR$Eps -> 1/xeps, 30]];
   Coefficient[y, xeps, 0] /. xeps -> 0];
vertNU$[legs_] := First[Cases[UV$vertlist, {legs, v_} :> v]];
abNU$[legs_] := Module[{v = Expand[numNU$[vertNU$[legs]]]},
   {Coefficient[v, fv, 2]/I, Coefficient[v /. fv -> 0 /. kk -> 0, gg]/I, Coefficient[v, kk gg]/I + Coefficient[v, fv, 2]/I}];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[N[mzNU$^2]]; SetDelta[0]; SetLambda[0];
ctNoteNU$ = Association[Rule @@@ Get[FileNameJoin[{srcDirNU$, "results", "ct_note.m"}]]];
noteNU$ = Re[N[# /. {B0OL[p_, a_, b_] :> B0[N[p], N[a], N[b]], DB0OL[p_, a_, b_] :> DB0[N[p], N[a], N[b]]}]] & /@ ctNoteNU$;
{aAA, bAA, chkAA} = abNU$[{{A, 1}, {A, 2}}];
{aAZ, bAZ, chkAZ} = abNU$[{{A, 1}, {Z, 2}}];
{aZZ, bZZ, chkZZ} = abNU$[{{Z, 1}, {Z, 2}}];
{aWW, bWW, chkWW} = abNU$[{{Wbar, 1}, {W, 2}}];
hhNU$ = Expand[numNU$[vertNU$[{{H, 1}, {H, 2}}]]];
{c1HH, c0HH} = {Coefficient[hhNU$, kk]/I, (hhNU$ /. kk -> 0)/I};
mz2N = N[mzNU$^2]; mw2N = N[mwNU$^2]; mh2N = N[mhNU$^2];
cmpNU$ = {
   {"dZAA", aAA, noteNU$["dZAA"]}, {"b(AA) = 0", bAA, 0.},
   {"(dZAZ + dZZA)/2", aAZ, (noteNU$["dZAZ"] + noteNU$["dZZA"])/2}, {"MZ^2 dZZA/2", bAZ, mz2N noteNU$["dZZA"]/2},
   {"dZZZ", aZZ, noteNU$["dZZZ"]}, {"dMZsq", bZZ - mz2N aZZ, noteNU$["dMZsq"]},
   {"dZW", aWW, noteNU$["dZW"]}, {"dMWsq", bWW - mw2N aWW, noteNU$["dMWsq"]},
   {"dZH", c1HH, noteNU$["dZH"]}, {"dMHsq", -c0HH - mh2N c1HH, noteNU$["dMHsq"]}};
fmtNU$[x_, n_] := ToString[NumberForm[Chop[N[x], 10^-14], n, NumberFormat -> (If[#3 == "", #1, Row[{#1, "e", #3}]] &)], OutputForm];
Do[Print["(a) ", StringPadRight[c[[1]], 16], " NLOCT ", fmtNU$[c[[2]], 15], "   note ", fmtNU$[c[[3]], 15], "   rel. diff. ",
    fmtNU$[If[c[[3]] == 0, Abs[c[[2]]], Abs[c[[2]]/c[[3]] - 1]], 2]], {c, cmpNU$}];
Print["(a) transversality (the k^2 g^mu nu coefficient is -a): ", Chop[{chkAA, chkAZ, chkZZ, chkWW}, 10^-12], "  (expect 0)"];
Print["(a) the electron two-point counterterm / I (pslashm = pslash PL, pm = PL, ...): ",
  InputForm[Chop[N[Expand[numNU$[vertNU$[{{ebar, 1}, {e, 2}}]]/I]], 10^-16]]];


(* ::Section:: *)
(*(b) alpha(0): the charge counterterm*)


fermNU$ = {{e, Me, -1, 1}, {mu, MMU, -1, 1}, {ta, MTA, -1, 1}, {u, MU, 2/3, 3}, {c, MC, 2/3, 3}, {t, MT, 2/3, 3},
   {d, MD, -1/3, 3}, {s, MS, -1/3, 3}, {b, MB, -1/3, 3}};
dZeFinNU$ = -ee^2/(16 Pi^2) (Sum[2/3 f[[4]] f[[3]]^2 2 Log[f[[2]]/FR$MU] IPL[{f[[1]]}], {f, fermNU$}] -
     7/2 2 Log[MW/FR$MU] IPL[{W}] + 1/3 IPL[{W}]);
(* check against the note's delta Z_e (step (4)): its finite part at the point *)
Print["(b) delta Z_e,fin at the point: ", fmtNU$[dZeFinNU$ /. IPL[_] -> 1 /. pointNU$, 16],
  "   (note, Delta = 0, mu = MZ: 0.03680569473 of Table ct)"];
treeNU$ = FeynmanRules[LSM, FlavorExpand -> True];
(* ee dV/dee at fixed MW, MZ, MH, masses (sw, cw fixed) *)
eeDerNU$[v_] := Module[{w = v //. intNU$ /. vevNU$}, Simplify[ee D[w, ee]]];
shiftNU$ = DeleteCases[{#[[1]], eeDerNU$[#[[2]]]} & /@ treeNU$, {_, 0}];
Print["(b) tree vertices ", Length[treeNU$], ", of which depend on ee: ", Length[shiftNU$]];
Print["(b) e e A: ee dV/dee = ", InputForm[Cases[shiftNU$, {{{ebar, 1}, {e, 2}, {A, 3}}, v_} :> v]], ";  e e Z: ",
  InputForm[Cases[shiftNU$, {{{ebar, 1}, {e, 2}, {Z, 3}}, v_} :> v]]];
(* add delta Z_e,fin ee dV/dee to the UV vertices (a new entry where NLOCT has none) *)
uvA0NU$ = UV$vertlist;
Do[Module[{pos = Position[uvA0NU$[[All, 1]], sh[[1]], {1}, Heads -> False]},
    If[pos === {},
      AppendTo[uvA0NU$, {sh[[1]], Expand[dZeFinNU$ sh[[2]]]}],
      uvA0NU$[[pos[[1, 1]], 2]] = uvA0NU$[[pos[[1, 1]], 2]] + Expand[dZeFinNU$ sh[[2]]]]], {sh, shiftNU$}];
Print["(b) UV vertices after the alpha(0) shift: ", Length[uvA0NU$], " (NLOCT: ", Length[UV$vertlist], ")"];


(* ::Section:: *)
(*(c) the UFO*)


FeynmanGauge = True;
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
(* Why numbers.  FeynRules 2.3.49 does not write CT_parameters.py (WritePYCTParamters is never called and calls the
   misspelled CreateCTParamterObjectEntry), and the couplings containing CT parameters get the order {'1': 1}; so the CT
   parameters are substituted back.  The UV vertices are then 44 million leaves long, mostly from NLOCT's branches
   If[m == 0, ...], If[m1 == m2, ...]; resolved for non-zero, mutually different masses they still have 7 million
   leaves, WriteUFO needs 44 minutes, and the closed forms cancel to 24 digits for m_e << MW: MadLoop evaluates them in
   double precision and gets the virtual wrong by orders of magnitude (c0).  So each UFO carries the counterterm
   couplings as numbers at one parameter point (40 digits, mu_R = MZ), each term written as
   number x (ee/ee0)^a (gs/gs0)^b so that MadGraph sees the coupling orders.  The tree couplings stay symbolic, so the
   param_card must hold the same point. *)
ifResNU$[x_, pt_] := x /. If[c_, a_, b_] :> If[TrueQ[c /. pt], a, b];
uvFullNU$ = uvA0NU$ //. ctParNU$;
ordNU$ = {aEWM1 -> 4 Pi/ee^2, aS -> gs^2/(4 Pi)};
(* the point: masses (exact), FR$MU -> MZ *)
ptRulesNU$[masses_] := Join[{MW -> mwNU$, MZ -> mzNU$, MH -> mhNU$, FR$MU -> mzNU$}, masses];
ee0NU$ = Sqrt[4 Pi alNU$]; gs0NU$ = Sqrt[4 Pi 118/1000];
(* N must not turn the integers inside the structures into reals (Ext[1] -> Ext[1.], FV[2, ...] -> FV[2., ...], Ga[5, ...]):
   the colour structures would become Identity(1.,2.) and MadGraph cannot read them *)
Unprotect[Index, Ext, FV, SP, SlashedP, Ga];
SetAttributes[{Index, Ext, FV, SP, SlashedP, Ga}, NHoldAll];
numVertNU$[v_, masses_] := Module[{pt = ptRulesNU$[masses], w},
   w = ifResNU$[v, pt] //. intNU$ /. vevNU$ /. ordNU$;
   w = w /. {ee -> ee0NU$ xe, gs -> gs0NU$ xg} /. {cw -> mwNU$/mzNU$, sw -> Sqrt[1 - mwNU$^2/mzNU$^2]} /. pt;
   w = Expand[N[w, 40]];
   Chop[w, 10^-40] /. {xe -> ee/ee0NU$, xg -> gs/gs0NU$}];
(* (c0) the precision of the closed forms in double precision: the e e Z and mu mu Z vertices at the note's point *)
Do[Module[{v = ifResNU$[First[Cases[uvFullNU$, {legs, x_} :> x]], ptRulesNU$[massNU$]] //. intNU$ /. vevNU$ /. ordNU$ /. fvNU$ /.
      IPL[_] -> 1 /. FR$Eps -> Infinity, ex, mach},
    v = v /. {TensDot[Ga[Index[Lorentz, Ext[3]]], ProjM][Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> gl,
       TensDot[Ga[Index[Lorentz, Ext[3]]], ProjP][Index[Spin, Ext[1]], Index[Spin, Ext[2]]] -> gr};
    ex = N[Coefficient[v /. ee -> ee0NU$ /. {cw -> mwNU$/mzNU$, sw -> Sqrt[1 - mwNU$^2/mzNU$^2]} /. ptRulesNU$[massNU$], #] & /@ {gl, gr}, 30];
    mach = Coefficient[v /. ee -> N[ee0NU$] /. {cw -> N[mwNU$/mzNU$], sw -> N[Sqrt[1 - mwNU$^2/mzNU$^2]]} /. (N /@ ptRulesNU$[massNU$]), #] & /@ {gl, gr};
    Print["(c0) ", legs[[All, 1]], " UV counterterm, coefficients of gamma PL, gamma PR: 30 digits ", N[ex, 12],
      ";  machine precision ", mach]],
  {legs, {{{ebar, 1}, {e, 2}, {Z, 3}}, {{mubar, 1}, {mu, 2}, {Z, 3}}}}];
massHeavyNU$ = massNU$ /. {(Me -> _) -> (Me -> 2), (MMU -> _) -> (MMU -> 3)};
writeNumUFO$[name_, masses_] := Module[{t = AbsoluteTime[], uv},
   uv = {#[[1]], numVertNU$[#[[2]], masses]} & /@ uvFullNU$;
   uv = DeleteCases[uv, {_, 0 | 0.}];
   Print["(c) ", name, ": UV vertices ", Length[uv], ", ", LeafCount[uv], " leaves (numbers) in ", Round[AbsoluteTime[] - t], " s"];
   If[DirectoryQ[name], DeleteDirectory[name, DeleteContents -> True]];
   t = AbsoluteTime[];
   WriteUFO[LSM, UVCounterterms -> uv, R2Vertices -> R2$vertlist, Output -> name];
   Print["(c) ", name, ": WriteUFO in ", Round[AbsoluteTime[] - t], " s"]];
writeNumUFO$["SM_NLO_a0_UFO", massNU$];
writeNumUFO$["SM_NLO_a0_heavy_UFO", massHeavyNU$];
(* MadGraph's UFO-to-Fortran converter writes numbers with '%e', i.e. 7 significant digits.  In couplings.py the rational
   coefficients written as decimals are turned back into ratios (MadGraph keeps small integers exact); the numbers in
   CT_couplings.py are split into three 7-digit integers times powers of ten by ufo_digits.py. *)
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Do[Print["(c) ", u, ": decimal coefficients made exact in couplings.py: ", exactUFO$[FileNameJoin[{Directory[], u, "couplings.py"}]]],
  {u, {"SM_NLO_a0_UFO", "SM_NLO_a0_heavy_UFO"}}];
Print["written: ", FileNames["SM_NLO_a0*_UFO"]];
