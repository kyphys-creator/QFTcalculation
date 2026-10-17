(* ::Package:: *)

(* ::Title:: *)
(*Step (9d): the FJ MS-bar parameter counterterms and the tadpole shift for the note's general NLO UFO*)


(* ::Text:: *)
(*The UFO's external parameters p = aEWM1, aS, MZ, MW, MH and the fermion masses get the MS-bar counterterms of the FJ*)
(*scheme, p0 = p + FR$delta[{p}] with FR$delta[{p}] = (1/FR$Eps) (1/2) dp/dln mu (note Eq. (zrule)), the one-loop running*)
(*from Eq. (beta) by the chain rule (g = e/sw, g' = e/cw, v = 2 MW sw/e, lambda = MH^2/(2 v^2), mu^2 = MH^2/2,*)
(*y_f = sqrt(2) m_f/v; FJ: v^2 = mu^2/lambda runs, with its 1/lambda terms).  The tadpole shift of the Higgs field is*)
(*dvT = T/MH^2 with T of step (3) (results/oneloop_sigma.m, K T, Feynman gauge), as poles 1/FR$Eps and finite parts at*)
(*the scale FR$MU (the UFO's MU_R).  Checks: K de/e = 11/6 e^2, and dMZ2 = 2 MZ FR$delta[{MZ}], dMW2 against nlo_fjct.wl*)
(*(massless light fermions).  Writes Src/generated/SM_FJdelta.m.  Batch: wolframscript -file nlo_fjdelta.wl*)


srcDirFD$ = DirectoryName[$InputFileName];
KK = 16 Pi^2;
(* fermions: {mass symbol, type, partner in the doublet (same generation)} *)
upF$ = {MU, MC, MT}; dnF$ = {MD, MS, MB}; lepF$ = {Me, MMU, MTA};
vv$ = 2 MW sw/ee; gg$ = ee/sw; gp$ = ee/cw; la$ = MH^2/(2 vv$^2); mu2$ = MH^2/2;
yf$[m_] := Sqrt[2] m/vv$;
gs$ = Sqrt[4 Pi aS];
Tsum$ = Sum[3 yf$[m]^2, {m, Join[upF$, dnF$]}] + Sum[yf$[m]^2, {m, lepF$}];
(* note Eq. (beta), times K *)
bg$ = -19/6 gg$^3; bgp$ = 41/6 gp$^3; bgs$ = -7 gs$^3;
bla$ = 24 la$^2 + 4 la$ Tsum$ - 2 (Sum[3 yf$[m]^4, {m, Join[upF$, dnF$]}] + Sum[yf$[m]^4, {m, lepF$}]) -
   3 la$ (3 gg$^2 + gp$^2) + 3/8 (2 gg$^4 + (gg$^2 + gp$^2)^2);
gmu2$ = mu2$ (12 la$ + 2 Tsum$ - 9/2 gg$^2 - 3/2 gp$^2);
by$[m_] := Module[{y = yf$[m], i, partner},
   Which[
    MemberQ[upF$, m], i = Position[upF$, m][[1, 1]]; partner = yf$[dnF$[[i]]];
     y (3/2 (y^2 - partner^2) + Tsum$ - 8 gs$^2 - 9/4 gg$^2 - 17/12 gp$^2),
    MemberQ[dnF$, m], i = Position[dnF$, m][[1, 1]]; partner = yf$[upF$[[i]]];
     y (3/2 (y^2 - partner^2) + Tsum$ - 8 gs$^2 - 9/4 gg$^2 - 5/12 gp$^2),
    True, y (3/2 y^2 + Tsum$ - 9/4 gg$^2 - 15/4 gp$^2)]];
(* K d/dln mu of the UFO's parameters *)
dlnv2$ = gmu2$/mu2$ - bla$/la$;
dlne$ = sw^2 bg$/gg$ + cw^2 bgp$/gp$;
run$ = <|
   aEWM1 -> -2 (4 Pi/ee^2) dlne$,
   aS -> 2 gs$ bgs$/(4 Pi),
   MW -> MW (bg$/gg$ + dlnv2$/2),
   MZ -> MZ ((gg$ bg$ + gp$ bgp$)/(gg$^2 + gp$^2) + dlnv2$/2),
   MH -> MH gmu2$/(2 mu2$),
   Splice[Table[m -> m (by$[m]/yf$[m] + dlnv2$/2), {m, Join[upF$, dnF$, lepF$]}]]|>;
(* sw, cw as functions of MW, MZ for the simplification; the expressions keep sw, cw (internal parameters of the UFO) *)
swcw$ = {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]};
simp$[x_] := Simplify[x /. swcw$, Assumptions -> MZ > MW > 0];
deltaRules$ = Normal[KeyValueMap[FR$delta[{#1}, {}] -> 1/FR$Eps (1/2) #2/KK &, run$]];
Print["K de/e = ", simp$[dlne$/2], "  (expect 11/6 ee^2)"];

(* checks against the FeynCalc poles of nlo_fjct.wl (Feynman gauge; massless light fermions) *)
fj$ = Get[FileNameJoin[{srcDirFD$, "results", "nlo_fjct.m"}]];
light0$ = Thread[Join[{MU, MC, MD, MS, MB}, lepF$] -> 0];
chk$[name_, mine_, theirs_] := Print[name, ": (this) - (FeynCalc, nlo_fjct) = ",
   Simplify[(mine - theirs) /. light0$ /. swcw$ /. ee -> Sqrt[4 Pi/aEWM1], Assumptions -> MZ > MW > 0 && aEWM1 > 0]];
chk$["pole of dMZ2", 2 MZ run$[MZ]/(2 KK), fj$["dMZ2"]];
chk$["pole of dMW2", 2 MW run$[MW]/(2 KK), fj$["dMW2"]];
chk$["pole of de/e", dlne$/(2 KK), fj$["de"]];

(* the tadpole shift dvT = T/MH^2, T = (K T)/K of step (3) in Feynman gauge *)
sig$ = Association[Get[FileNameJoin[{srcDirFD$, "results", "oneloop_sigma.m"}]]];
ep = Epsilon;
a0$ = A0[m2_] :> If[m2 === 0, 0, m2 (1/ep + 1 - Log[m2/FR$MU^2])];
tK$ = sig$["T"] /. {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
tLau$ = Module[{y = Simplify[(tK$ /. a0$) /. D -> 4 - 2 ep]}, Simplify /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
dvT$ = (tLau$[[1]]/FR$Eps + tLau$[[2]])/(KK MH^2);
Print["K MH^2 dvT: pole ", Simplify[tLau$[[1]]], ";  finite ", Short[tLau$[[2]], 3]];
(* check: the tadpole part of Sigma_T^ZZ, -(2 MZ^2/v) dvT, against nlo_fjct.wl *)
(* numerically: m^4 ln m^2 of the light fermions -> 0 is a limit (light masses 10^-12 GeV here) *)
ptFD$ = {aEWM1 -> 128, MZ -> 911876/10000, MW -> 80369/1000, MH -> 1252/10, MT -> 17257/100, FR$MU -> 911876/10000};
lightTiny$ = Thread[Join[{MU, MC, MD, MS, MB}, lepF$] -> 10^-12];
Print["Sigma_tad^ZZ = -(2 MZ^2/v) dvT minus nlo_fjct.wl (pole, finite; numbers): ",
  N[({tLau$[[1]], tLau$[[2]]}/(KK MH^2) (-2 MZ^2/vv$) - fj$["tadZZ"]) /. lightTiny$ /. swcw$ /. ee -> Sqrt[4 Pi/aEWM1] /. ptFD$, 20]];
Put[<|"delta" -> deltaRules$, "dvT" -> dvT$|>, FileNameJoin[{srcDirFD$, "generated", "SM_FJdelta.m"}]];
Print["written: generated/SM_FJdelta.m"];
