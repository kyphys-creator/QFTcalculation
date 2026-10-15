#!/bin/bash
# Research note models/qcd, step (9): aMC@NLO at fixed order, p p -> t tbar at 13 TeV (mu_R = mu_F = m/2, m, 2m) and p pbar at 1.96 TeV
# (mu = m), NNPDF2.3 NLO (pdlabel nn23nlo, alpha_s(M_Z) = 0.119 from the PDF, two-loop running), m_t = 172.5, NLO UFO of step (5)
# with the dummy M_Z, M_W of step (8) (work/QCD_NLO_UFO_amc, made by ee_mg5.py), p including b.  MadGraph5_aMC@NLO refuses NLO with
# fixed parton beams ("Process has incoming j_fks, but fixed shat: not allowed for processes generated at NLO"), hence the hadronic runs.
# -> work/hq/amc_had/Events/run_01..13 (read by hq_hadronic.py).  About 3 hours on 3-6 cores.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work/hq
# runs: 01-04 the cases of the note, 05-06 LO (Tevatron, LHC), 07-08 Tevatron mu = m/2, 2m, 09-10 mu = m with other seeds,
# 11 p p at 1.96 TeV, 12 pbar p at 1.96 TeV (beams exchanged), 13 p pbar at 13 TeV
lo() { # lpp2 ebeam mu seed (fixed-order LO)
  printf 'launch ./work/hq/amc_had\nfixed_order=ON\norder=LO\ndone\nset lpp1 1\nset lpp2 %s\nset ebeam1 %s\nset ebeam2 %s\nset pdlabel nn23nlo\nset fixed_ren_scale True\nset fixed_fac_scale True\nset mur_ref_fixed %s\nset muf_ref_fixed %s\nset req_acc_FO 0.0003\nset ptj 0.0\nset etaj -1.0\nset MT 172.5\nset iseed %s\ndone\n' "$1" "$2" "$2" "$3" "$3" "$4"
}
run2() { # lpp1 lpp2 ebeam mu seed
  printf 'launch ./work/hq/amc_had\nfixed_order=ON\ndone\nset lpp1 %s\nset lpp2 %s\nset ebeam1 %s\nset ebeam2 %s\nset pdlabel nn23nlo\nset fixed_ren_scale True\nset fixed_fac_scale True\nset mur_ref_fixed %s\nset muf_ref_fixed %s\nset req_acc_FO 0.0003\nset ptj 0.0\nset etaj -1.0\nset MT 172.5\nset iseed %s\ndone\n' "$1" "$2" "$3" "$3" "$4" "$4" "$5"
}
run() { # lpp2 ebeam mu seed
  printf 'launch ./work/hq/amc_had\nfixed_order=ON\ndone\nset lpp1 1\nset lpp2 %s\nset ebeam1 %s\nset ebeam2 %s\nset pdlabel nn23nlo\nset fixed_ren_scale True\nset fixed_fac_scale True\nset mur_ref_fixed %s\nset muf_ref_fixed %s\nset req_acc_FO 0.0003\nset ptj 0.0\nset etaj -1.0\nset MT 172.5\nset iseed %s\ndone\n' "$1" "$2" "$2" "$3" "$3" "$4"
}
{
printf 'set automatic_html_opening False\nset nb_core 3\nimport model ./work/QCD_NLO_UFO_amc\ndefine p = g u c d s b u~ c~ d~ s~ b~\ngenerate p p > t t~ [QCD]\noutput ./work/hq/amc_had -f\n'
run 1 6500 172.5 11
run 1 6500 86.25 12
run 1 6500 345.0 13
run -1 980 172.5 14
lo -1 980 172.5 21
lo 1 6500 172.5 22
run -1 980 86.25 41
run -1 980 345.0 42
run -1 980 172.5 43
run 1 6500 172.5 44
run 1 980 172.5 51
run2 -1 1 980 172.5 61
run2 1 -1 6500 172.5 62
} > work/hq/amc_had.mg5
~/hep/bin/mg5_aMC work/hq/amc_had.mg5 > work/hq/amc_had.log 2>&1
grep -E "Total cross section" work/hq/amc_had.log | tail -4
