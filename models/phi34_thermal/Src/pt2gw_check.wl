(* ::Package:: *)

(* ::Title:: *)
(*Step (8c): the Dine-form transitions against PT2GWFinder 1.1.0 and FindBounce 1.1.0*)


(* ::Text:: *)
(*Research note models/phi34_thermal, step (8).  For the SM-like coefficients and BP1-BP4 (steps (1), (2)):*)
(*(a) FindBounce: S_3 of the zero-temperature tree potential (alpha = 0.5, 0.9) and, through PT2GW's Action, S_3/T at the T_n*)
(*of steps (1), (2), against tptlib.bounce.  (b) TracePhases (PT2GW's own phase tracing) and FindCritical: T_c against the*)
(*closed form.  (c) FindNucleation with the criterion Gamma = H^4 of this note (PT2GW's H includes the vacuum energy |Delta V|;*)
(*the bisection tolerance is 10^-3 of the search range, so the range is narrowed to T_n +- 0.2%).  (d) Alpha (trace definition,*)
(*numerical T-derivative) and beta/H = T d(S_3/T)/dT at our T_n (quadratic fit of S_3/T at seven temperatures).  (e) ComputeGW (LISA CosWG 2024 template) with our T_n, alpha_theta,*)
(*beta/H, v_w = 0.95: peak and total (integral over ln f) of the sound-wave spectrum against ours (step (3)).  (f) PT2GW's own*)
(*pipeline (SearchPhases: nucleation by the integral of Gamma/H^4, transition at percolation T_p).*)
(*Reads Src/results/{dine_form,strong_pt,gw_spectrum,cosmotransitions_check}.csv; writes Src/results/pt2gw_check.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file pt2gw_check.wl  (about 30 minutes); only the lines starting with (a)-(f) are printed.  Interactive:  ~/hep/bin/wopen pt2gw_check.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


Quiet[Get["PT2GW`"]];
$PT2GWPrint = False;
srcDirPT$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
res$ = FileNameJoin[{srcDirPT$, "results", #}] &;
step1$ = Association[Rule @@@ Rest[Import[res$["dine_form.csv"]]]];
sp$ = Import[res$["strong_pt.csv"]];
ib$ = First@FirstPosition[sp$, {"benchmark", ___}];
keys$ = Rest[sp$[[ib$]]];
bench$ = AssociationThread[keys$ -> #] & /@ (Rest /@ sp$[[ib$ + 1 ;; ib$ + 4]]);
names$ = {"SM-like", "BP1", "BP2", "BP3", "BP4"};
pts$ = Prepend[bench$, <|"lam" -> step1$["lambda_T_Tc"], "E" -> step1$["E"], "Tn" -> step1$["Tn"], "betaH" -> step1$["beta_over_H"],
     "alpha_theta" -> 0.|>];
gw$ = Import[res$["gw_spectrum.csv"]];
gwRows$ = Select[gw$, Length[#] > 10 && MemberQ[{"BP1", "BP2", "BP3", "BP4"}, #[[1]]] && #[[2]] == 0.95 &];
gwKeys$ = gw$[[1]];
ct$ = Association[Rule @@@ (#[[{1, 3}]] & /@ Select[Import[res$["cosmotransitions_check.csv"]], Length[#] == 3 && StringQ[#[[1]]] &])];
Dd$ = step1$["D"]; T0$ = step1$["T0"];
model$[p_] := Module[{e = p["E"], lt = p["lam"], R},
   R = lt Dd$/e^2;
   {Function[{x, T}, Dd$ (T^2 - T0$^2) x^2 - e T x^3 + lt/4 x^4],
    {Function[T, 0.], Function[T, Module[{a = R (1 - T0$^2/T^2)}, -(a e T/(3 lt)) (-9/(2 a) (1 + Sqrt[1 - 8 a/9]))]]},
    T0$/Sqrt[1 - 1/R]}];                                                                   (* V, phases, T_c *)
alphaTheta$[p_, T_] := 15 Dd$/(Pi^2 106.75) (T0$/T)^2 (#/T)^2 &[(model$[p][[2, 2]])[T]];   (* Eq. (7) of the note *)
out$ = {{"quantity", "point", "PT2GW", "this_note"}};
add$[q_, n_, a_, b_] := AppendTo[out$, {q, n, a, b}];


(* ::Section:: *)
(*(a) FindBounce*)


(* FindBounce on the line from the false vacuum to an end point: the true minimum f_-, or the point f(0) + 0.3 (f_- - f(0)) just
   past the centre of the bounce (zero-temperature note); PT2GW's Action moves the end point to the exit point (ShiftToExitPoint) *)
zt$ = Select[Import[FileNameJoin[{srcDirPT$, "..", "..", "phi34", "Src", "results", "bounce.csv"}]], Length[#] > 3 && #[[1]] == 3 &];
Do[Module[{row = SelectFirst[zt$, #[[2]] == a &], v = f^2/2 + f^3/6 + a f^4/72, fm = -9/(2 a) (1 + Sqrt[1 - 8 a/9]), s},
   Do[s = Quiet[FindBounce[v, f, {0., end}, "Dimension" -> 3, "FieldPoints" -> n]]["Action"];
     Print["(a) FindBounce S_3 of the tree potential, alpha = ", a, ", end point ", end, ", ", n, " field points: ", s,
       " vs zero-temperature note ", row[[4]], " (rel. ", s/row[[4]] - 1, ")"];
     add$["S3_tree_alpha" <> ToString[a] <> "_end" <> ToString[Round[end, 0.01]] <> "_n" <> ToString[n], "", s, row[[4]]],
     {end, {fm, row[[3]] + 0.3 (fm - row[[3]])}}, {n, {31, 1001}}]], {a, {0.5, 0.9}}];
Do[Module[{p = pts$[[i]], v, ph, s},
   {v, ph} = model$[p][[;; 2]];
   s = Quiet[Action[p["Tn"], v, ph, "FieldPoints" -> #]] & /@ {51, 801};
   Print["(a) ", names$[[i]], ": S_3/T at T_n of steps (1), (2) by PT2GW's Action (FindBounce, 51 and 801 field points) ", s,
     " vs tptlib.bounce ", ct$["S3T_dine_" <> names$[[i]]], " (rel. ", s/ct$["S3T_dine_" <> names$[[i]]] - 1, ")"];
   add$["S3T_at_Tn_n51", names$[[i]], s[[1]], ct$["S3T_dine_" <> names$[[i]]]];
   add$["S3T_at_Tn_n801", names$[[i]], s[[2]], ct$["S3T_dine_" <> names$[[i]]]]], {i, 5}];


(* ::Section:: *)
(*(b) critical temperature, (c) nucleation with Gamma = H^4, (d) alpha and beta/H at our T_n*)


traced$ = <||>;
Do[Module[{p = pts$[[i]], v, ph, tc, tcPT, tnPT, tnOurs, aPT, aOurs, sF, bPT, dT, dv, rho, phT, t1, ts, ss, fit, resid},
   {v, ph, tc} = model$[p];
   t1 = T0$/Sqrt[1 - 9/(8 p["lam"] Dd$/p["E"]^2)];
   phT = Quiet[TracePhases[v, "TRange" -> {T0$ + 0.01, 1.05 t1}]];          (* PT2GW's own phase tracing *)
   traced$[names$[[i]]] = phT;
   tcPT = Quiet[FindCritical[v, phT]];
   tcPT = If[ListQ[tcPT], First[Flatten[tcPT /. Rule[_, x_] :> x]], tcPT /. Rule[_, x_] :> x];
   tnOurs = If[KeyExistsQ[ct$, "Tn_" <> names$[[i]]], ct$["Tn_" <> names$[[i]]], p["Tn"]];
   tnPT = Quiet[FindNucleation[v, {0.998 tnOurs, Min[1.002 tnOurs, tc]}, ph, "NucleationCriterion" -> "DecayOverHubble",
       ProgressIndicator -> False, "FieldPoints" -> 201]];
   tnPT = If[ListQ[tnPT], First[Flatten[tnPT /. Rule[_, x_] :> x]], tnPT /. Rule[_, x_] :> x];
   dv = v[(ph[[1]])[tnOurs], tnOurs] - v[(ph[[2]])[tnOurs], tnOurs]; rho = Pi^2/30 106.75 tnOurs^4;
   aPT = Alpha[tnOurs, v, ph]; aOurs = alphaTheta$[p, tnOurs];
   dT = Min[2*^-3 (tc - tnOurs), 0.5];
   ts = tnOurs + dT Range[-3, 3];
   ss = Quiet[Action[#, v, ph, "FieldPoints" -> 401]] & /@ ts;
   fit = Fit[Transpose[{ts - tnOurs, ss}], {1, x, x^2}, x];
   resid = Sqrt[Mean[(ss - (fit /. x -> (ts - tnOurs)))^2]];
   bPT = tnOurs Coefficient[fit, x];
   Print["(b) ", names$[[i]], ": T_c FindCritical ", tcPT, " vs closed form ", tc, " (rel. ", tcPT/tc - 1, ")"];
   Print["(c) ", names$[[i]], ": T_n (Gamma = H^4) FindNucleation ", tnPT, " vs this note ", tnOurs, " (rel. ", tnPT/tnOurs - 1,
     "; Delta V/rho_rad = ", dv/rho, ", expected shift from |Delta V| in H about ", -2 Log[1 + dv/rho]/p["betaH"], ")"];
   Print["(d) ", names$[[i]], ": at T_n alpha (Alpha) ", aPT, " vs Eq. (7) ", aOurs, " (rel. ", aPT/aOurs - 1, ");  beta/H from FindBounce ",
     bPT, " vs this note ", p["betaH"], " (rel. ", bPT/p["betaH"] - 1, "; rms residual of the fit ", resid, ")"];
   add$["Tc", names$[[i]], tcPT, tc]; add$["Tn_DecayOverHubble", names$[[i]], tnPT, tnOurs];
   add$["alpha_at_Tn", names$[[i]], aPT, aOurs]; add$["betaH_at_Tn", names$[[i]], bPT, p["betaH"]];
   add$["betaH_fit_rms_residual", names$[[i]], resid, ""]], {i, 5}];


(* ::Section:: *)
(*(e) gravitational waves with our parameters (LISA CosWG 2024 template of PT2GW)*)


Do[Module[{r = AssociationThread[gwKeys$ -> gwRows$[[i]]], g, sw, tot, h2, u0, totOurs},
   g = ComputeGW[r["Tn"], r["alpha"], r["betaH"], 0.95, 106.75, "GeV"];
   sw = g["h2Omega"]["Soundwaves"];
   tot = NIntegrate[sw[Exp[u]], {u, Log[1*^-6], Log[10.]}, PrecisionGoal -> 8];
   {h2, u0} = {#[[1]], u /. #[[2]]} &[FindMaximum[Log[sw[Exp[u]]], {u, Log[r["fp"]]}]];
   g = Join[g, <|"h2OmegaPeak" -> Exp[h2], "fPeak" -> Exp[u0]|>];
   (* ours: total = h^2 x 3 x F_gw0 K^2 (H R) Omega~ min(1, H tau_sh), the peak of C(s) normalised by 0.687 *)
   totOurs = r["sw_peak"]/0.687;
   Print["(e) ", r["name"], ": sound-wave peak PT2GW ", g["h2OmegaPeak"], " at ", 1000 g["fPeak"], " mHz vs this note ", r["sw_peak"],
     " at ", 1000 r["fp"], " mHz (ratio ", g["h2OmegaPeak"]/r["sw_peak"], ");  integral over ln f ", tot, " vs ", totOurs,
     " (ratio ", tot/totOurs, ");  K: ", g["Ksw"], " vs ", r["K"]];
   add$["GW_peak", r["name"], g["h2OmegaPeak"], r["sw_peak"]]; add$["GW_fpeak_Hz", r["name"], g["fPeak"], r["fp"]];
   add$["GW_total", r["name"], tot, totOurs]], {i, 4}];


(* ::Section:: *)
(*(f) PT2GW's own pipeline (SearchPhases, v_w = 0.95)*)


transitions$ = <||>;
Do[Module[{p = pts$[[i]], v, tr},
   v = model$[p][[1]];
   transitions$[names$[[i]]] = Quiet[SearchPhases[v, traced$[names$[[i]]], 0.95, ProgressIndicator -> False]];
   tr = transitions$[names$[[i]]][[1]];
   Print["(f) ", names$[[i]], ": T_c ", tr["Tc"], ", T_n (integral of Gamma/H^4 = 1) ", tr["Tn"], " (S_3/T ", tr["NucleationAction"],
     "), T_p ", tr["Tp"], ", alpha(T_p) ", tr["\[Alpha]"], ", beta/H(T_p) ", tr["\[Beta]/H"], ", peak h^2 Omega ", tr["h2OmegaPeak"], " at ",
     1000 tr["fPeak"], " mHz"];
   add$["SearchPhases_Tn_integral", names$[[i]], tr["Tn"], p["Tn"]]; add$["SearchPhases_Tp", names$[[i]], tr["Tp"], ""];
   add$["SearchPhases_alpha_Tp", names$[[i]], tr["\[Alpha]"], ""]; add$["SearchPhases_betaH_Tp", names$[[i]], tr["\[Beta]/H"], ""];
   add$["SearchPhases_peak", names$[[i]], tr["h2OmegaPeak"], ""]], {i, 5}];


(* ::Subsubsection:: *)
(*Inspect: the BP4 transition of PT2GW*)


If[$Notebooks, PlotGW[transitions$["BP4"]]]


(* ::Section:: *)
(*Output*)


(* CSV writer: a field is quoted only when it contains a comma or a quote *)
csvField$[x_] := Module[{s = Which[StringQ[x], x, NumberQ[x], ToString[N[x], CForm], True, ToString[x, InputForm]]},
   If[StringContainsQ[s, "," | "\""], "\"" <> StringReplace[s, "\"" -> "\"\""] <> "\"", s]];
writeCSV$[file_, rows_] := Export[file, StringRiffle[StringRiffle[csvField$ /@ #, ","] & /@ rows, "\n"] <> "\n", "Text"];
writeCSV$[res$["pt2gw_check.csv"], out$];
Print["(f) wrote results/pt2gw_check.csv"];
