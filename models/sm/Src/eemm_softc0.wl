(* ::Package:: *)

(* ::Title:: *)
(*Step (6): the soft-photon C0 of e+ e- -> mu+ mu- -- LoopTools, COLLIER and Package-X*)


(* ::Text:: *)
(*Research note models/sm, step (6).  C0(m^2, s, m^2; 0, m, m) (photon exchanged between two on-shell electrons, LoopTools'*)
(*argument order C0(s, m^2, m^2, m^2, m^2, 0) as FormCalc writes it), m = m_e, s = 200^2 and 500^2, mu = 1:*)
(*  (1) LoopTools in dimensional regularization: finite part (lambda^2 = 0) and coefficient of the soft pole (lambda^2 = -1);*)
(*  (2) with a photon mass lambda^2 = 1e-20 GeV^2 from LoopTools (fourth mass argument) and Package-X (ScalarC0, 30 digits);*)
(*  (3) the dimensionally regularized finite part implied by (2): C0(lambda) - a ln(lambda^2/mu^2) (a the pole coefficient),*)
(*      i.e. ln(lambda^2) -> c_eps mu^(2 eps)/eps + ln(mu^2) for a soft singularity;*)
(*  COLLIER's values (both regularizations) come from eemm_collier with the input written here (work/eemm_softc0_in.txt).*)
(*Writes results/eemm_softc0.csv.  How to run:  wolframscript -file eemm_softc0.wl  (plain kernel).*)


srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
m2SC$ = (51099895/10^11)^2; lam2SC$ = 10^-20;
SetMudim[1.]; SetDelta[0];
rowsSC$ = Table[Module[{fin, ir, lam},
    SetLambda[0]; SetUVDiv[1]; fin = C0i[cc0, N[s], N[m2SC$], N[m2SC$], N[m2SC$], N[m2SC$], 0.];
    SetLambda[-1]; SetUVDiv[0]; ir = C0i[cc0, N[s], N[m2SC$], N[m2SC$], N[m2SC$], N[m2SC$], 0.];
    SetLambda[0]; SetUVDiv[1];
    lam = C0i[cc0, N[s], N[m2SC$], N[m2SC$], N[m2SC$], N[m2SC$], N[lam2SC$]];
    {s, fin, ir, lam}], {s, {200^2, 500^2}}];
Uninstall[Links["*LoopTools*"]];
Get["X`"];
pxSC$ = Table[N[X`ScalarC0[m2SC$, s, m2SC$, Sqrt[lam2SC$], Sqrt[m2SC$], Sqrt[m2SC$]], 20], {s, {200^2, 500^2}}];
Do[Module[{r = rowsSC$[[i]], px = pxSC$[[i]], fromLam},
    fromLam = r[[4]] - r[[3]] Log[N[lam2SC$]];
    Print["(a) s = ", r[[1]], ":  photon mass: LoopTools ", r[[4]], ", Package-X ", N[px, 16], ";  dimensional regularization: LoopTools ",
      r[[2]], ",\n      from the photon mass ", fromLam, ";  difference + pi^2/(6 s) = ", Chop[r[[2]] - fromLam + Pi^2/(6 r[[1]]), 10^-15]]],
  {i, 2}];
strSC$[x_] := ToString[CForm[N[x]]];
Export[FileNameJoin[{srcDirSC$, "work", "eemm_softc0_in.txt"}],
  StringRiffle[Flatten[Table[{
      StringRiffle[{ToString[2 i - 1], "C0", "6", strSC$[s], strSC$[m2SC$], strSC$[m2SC$], strSC$[m2SC$], strSC$[m2SC$], "0."}, " "],
      StringRiffle[{ToString[2 i], "C0", "6", strSC$[s], strSC$[m2SC$], strSC$[m2SC$], strSC$[m2SC$], strSC$[m2SC$], strSC$[lam2SC$]}, " "]},
     {i, 2}, {s, {{200^2, 500^2}[[i]]}}]], "\n"] <> "\n", "Text"];
Export[FileNameJoin[{srcDirSC$, "results", "eemm_softc0.csv"}],
  StringRiffle[Prepend[StringRiffle[{strSC$[#[[1, 1]]], strSC$[Re[#[[1, 2]]]], strSC$[Im[#[[1, 2]]]], strSC$[Re[#[[1, 3]]]],
        strSC$[Im[#[[1, 3]]]], strSC$[Re[#[[1, 4]]]], strSC$[Im[#[[1, 4]]]], strSC$[Re[#[[2]]]], strSC$[Im[#[[2]]]]}, ","] & /@
     Transpose[{rowsSC$, pxSC$}], "s,re_fin_lt,im_fin_lt,re_ir_lt,im_ir_lt,re_lam_lt,im_lam_lt,re_lam_px,im_lam_px"], "\n"] <> "\n", "Text"];
Print["(a) wrote results/eemm_softc0.csv and work/eemm_softc0_in.txt (for eemm_collier, mu^2 = 1)"];
