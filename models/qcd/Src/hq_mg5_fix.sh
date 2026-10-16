#!/bin/bash
# Research note models/qcd, step (9): the cause of the aMC@NLO p pbar discrepancy and its fix.
# MadGraph5_aMC@NLO 3.8.1, Template/NLO/SubProcesses/genps_fks.f (generate_momenta, l. 1001): use_evpr (the standard FKS mapping
# with event projection) is set to .true. only for (lpp1, lpp2) = (1,1), (2,2), (0,0); for p pbar (1,-1) it keeps its default .false.,
# so the real emission and the collinear counterterms use the mapping without event projection meant for dressed-lepton (e+e- ISR)
# collisions, and the NLO cross section comes out 0.4-0.7% too high (LO is unaffected).  This copies the process directory of
# hq_mg5.sh (work/hq/amc_had, without its events), patches the condition to abs(lpp) = 1 and reruns the p pbar cases.
# -> work/hq/amc_fix/Events/run_01..03 (read by hq_hadronic.py).  About 45 minutes on 6 cores.
cd "$(dirname "$0")"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
rm -rf work/hq/amc_fix
rsync -a --exclude Events work/hq/amc_had/ work/hq/amc_fix/ && mkdir -p work/hq/amc_fix/Events
sed -i '' 's/      if ((lpp(1).eq.1.and.lpp(2).eq.1).or./      if ((abs(lpp(1)).eq.1.and.abs(lpp(2)).eq.1).or./' work/hq/amc_fix/SubProcesses/genps_fks.f
grep -n "abs(lpp(1)).eq.1.and.abs(lpp(2)).eq.1" work/hq/amc_fix/SubProcesses/genps_fks.f || { echo "patch failed"; exit 1; }
run2() { # lpp1 lpp2 ebeam mu seed
  printf 'launch ./work/hq/amc_fix\nfixed_order=ON\ndone\nset lpp1 %s\nset lpp2 %s\nset ebeam1 %s\nset ebeam2 %s\nset pdlabel nn23nlo\nset fixed_ren_scale True\nset fixed_fac_scale True\nset mur_ref_fixed %s\nset muf_ref_fixed %s\nset req_acc_FO 0.0003\nset ptj 0.0\nset etaj -1.0\nset MT 172.5\nset iseed %s\ndone\n' "$1" "$2" "$3" "$3" "$4" "$4" "$5"
}
{
printf 'set automatic_html_opening False\nset nb_core 6\n'
run2 1 -1 980 172.5 71
run2 1 -1 6500 172.5 72
run2 1 -1 980 86.25 73
} > work/hq/amc_fix.mg5
~/hep/bin/mg5_aMC work/hq/amc_fix.mg5 > work/hq/amc_fix.log 2>&1
grep -E "Total cross section" work/hq/amc_fix.log | tail -3
