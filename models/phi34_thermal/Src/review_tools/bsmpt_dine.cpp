// Step (11): the general form of Dine et al., V = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4, in BSMPT 3.2.0.
// Research note models/phi34_thermal.  A user potential in the way of BSMPT's standalone/GenericModel.cpp: VEff returns
// the general form (diff = 0), its field derivative (diff = 1) and its temperature derivative (diff = -1, used for alpha).
// Four "Higgs" fields as in GenericModel (only the first is used), so that BSMPT's radiation count gives g* = 106.75.
// Reads lines "name D E T0 lambda_T T_low T_high" from stdin and prints one CSV line per point:
//   name,Tc,Tn_approx(S3/T=140),Tn(Gamma=H^4),Tp,alpha(Tn),betaH(Tn),kappa_sw,cs_f,cs_t,f1_sw,f2_sw,omega2_sw,SNR_sw
// BSMPT's conventions: Gamma = T^4 (S3/2 pi T)^(3/2) e^(-S3/T); H^2 = (rho_rad + Delta V)/(3 M_Pl^2), M_Pl = 2.4e18 GeV;
// alpha = [Delta V - (T/4) Delta dV/dT]/rho_rad.  Its GW stage needs SM-like particle masses (wall pressure), which
// the general form does not have: the GW columns are printed but not used.
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include <BSMPT/models/ClassPotentialOrigin.h>
#include <BSMPT/models/IncludeAllModels.h>
#include <BSMPT/transition_tracer/transition_tracer.h>
#include <BSMPT/utility/Logger.h>

using namespace BSMPT;

class DineForm : public Class_Potential_Origin {
public:
  DineForm(double D_, double E_, double T0_, double lam_, double Tlow)
      : Class_Potential_Origin(GetSMConstants()), D(D_), E(E_), T0(T0_), lam(lam_) {
    NNeutralHiggs = 4;
    NChargedHiggs = 0;
    NHiggs = NNeutralHiggs + NChargedHiggs;
    nVEV = 1;
    // BSMPT tracks the "EW" phase from vevTreeMin at T_low: use the broken minimum there (closed form), not the T = 0 one,
    // which lies too far away for BP4 and is not found
    vevTreeMin = {(3 * E * Tlow + std::sqrt(9 * E * E * Tlow * Tlow - 8 * lam * D * (Tlow * Tlow - T0 * T0))) / (2 * lam)};
    VevOrder.resize(nVEV);
    VevOrder[0] = 0;
    // The GW stage asks for the particle masses (wall pressure, kappa_col).  The general form has no particle content:
    // zero tensors, so that alpha, beta/H and the temperatures are computed; the GW numbers are not used.
    initVectors();
    SetCurvatureDone = true;
  }
  void ReadAndSet(const std::string &, std::vector<double> &) override {}
  std::vector<std::string> addLegendCT() const override { return {}; }
  std::vector<std::string> addLegendTemp() const override { return {}; }
  std::vector<std::string> addLegendTripleCouplings() const override { return {}; }
  std::vector<std::string> addLegendVEV() const override { return {"phi"}; }
  void set_gen(const std::vector<double> &) override {}
  void set_CT_Pot_Par(const std::vector<double> &) override {}
  void write() const override {}
  void SetCurvatureArrays() override {}
  bool CalculateDebyeSimplified() override { return true; }
  bool CalculateDebyeGaugeSimplified() override { return true; }
  double VTreeSimplified(const std::vector<double> &) const override { return 0; }
  double VCounterSimplified(const std::vector<double> &) const override { return 0; }
  void AdjustRotationMatrix() override {}
  void TripleHiggsCouplings() override {}
  std::vector<double> calc_CT() const override { return {0}; }
  void Debugging(const std::vector<double> &, std::vector<double> &) const override {}
  double EWSBVEV(const std::vector<double> &) const override { return 0; }
  void SetEWVEVZero(std::vector<double> &sol) const override { sol = std::vector<double>(nVEV, 0); }
  double VEff(const std::vector<double> &v, double T = 0, int diff = 0, const Order &order = Order::OneLoop) const override {
    (void)order;
    const double p = v[0];
    if (diff == 0) return D * (T * T - T0 * T0) * p * p - E * T * p * p * p + 0.25 * lam * p * p * p * p;
    if (diff == -1) return 2 * D * T * p * p - E * p * p * p;
    if (diff == 1) return 2 * D * (T * T - T0 * T0) * p - 3 * E * T * p * p + lam * p * p * p;
    return 0;
  }

private:
  double D, E, T0, lam;
};

int main() {
  SetLogger({"--logginglevel::default=false"});
  std::string line;
  std::cout << std::setprecision(15);
  while (std::getline(std::cin, line)) {
    if (line.empty()) continue;
    std::istringstream in(line);
    std::string name;
    double D, E, T0, lam, Tlow, Thigh;
    in >> name >> D >> E >> T0 >> lam >> Tlow >> Thigh;
    auto model = std::make_shared<DineForm>(D, E, T0, lam, Tlow);
    user_input input;
    input.modelPointer = model;
    input.T_low = Tlow;
    input.T_high = Thigh;
    input.vwall = 0.95;
    input.epsturb = 0.05;
    input.ewsr_check = 0;
    input.nlo_check = 0;
    input.gw_calculation = true;
    input.which_transition_temp = TransitionTemperature::Nucleation;
    TransitionTracer trans(input);
    const auto &out = trans.output_store;
    if (out.vec_trans_data.empty()) {
      std::cout << name << ",no transition" << std::endl;
      continue;
    }
    const auto &td = out.vec_trans_data[0];
    auto o = [](const std::optional<double> &x) { return x ? *x : std::nan(""); };
    std::cout << name << "," << o(td.crit_temp) << "," << o(td.nucl_approx_temp) << "," << o(td.nucl_temp) << ","
              << o(td.perc_temp);
    if (!out.vec_gw_data.empty()) {
      const auto &g = out.vec_gw_data[0];
      std::cout << "," << o(g.alpha) << "," << o(g.beta_over_H) << "," << o(g.kappa_sw) << "," << o(g.cs_f) << ","
                << o(g.cs_t) << "," << o(g.f1_sw) << "," << o(g.f2_sw) << "," << o(g.omega_2_sw) << "," << o(g.SNR_sw);
    }
    std::cout << std::endl;
  }
  return 0;
}
