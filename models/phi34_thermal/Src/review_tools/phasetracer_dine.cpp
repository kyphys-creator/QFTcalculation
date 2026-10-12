// Step (11): the general form of Dine et al., V = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4, in PhaseTracer 2.2.2.
// Research note models/phi34_thermal.  Reads lines "name D E T0 lambda_T T1 t_low tight T_a T_b ..." from stdin (written by
// review_tools_check.py; t_low between T0 and T_n, where the symmetric phase still exists) and prints, for each point, one CSV line:
//   name,tight,TC,TN,S3T_TN,alpha,betaH,peak_amplitude,peak_frequency,S3T(T_a),S3T(T_b),...
// PhaseTracer's own conventions: T_n from S3/T = 140; alpha = Delta(V - T/4 dV/dT)/rho_rad; beta/H = T d(S3/T)/dT from a
// linear fit of 6 actions in [T - 0.1, T + 0.1] GeV; the GW spectra at T_n.  tight = 1 sets the shooting tolerances to 1e-10.
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "phasetracer.hpp"
#include "potential.hpp"

class DineForm : public EffectivePotential::Potential {
public:
  DineForm(double D, double E, double T0, double lam) : D(D), E(E), T0(T0), lam(lam) {}
  double V(Eigen::VectorXd x, double T) const override {
    const double p = x[0];
    return D * (T * T - T0 * T0) * p * p - E * T * p * p * p + 0.25 * lam * p * p * p * p;
  }
  size_t get_n_scalars() const override { return 1; }
  bool forbidden(Eigen::VectorXd x) const override { return x[0] < -0.1; }
  Eigen::VectorXd dV_dx(Eigen::VectorXd x, double T) const override {
    const double p = x[0];
    Eigen::VectorXd d(1);
    d(0) = 2. * D * (T * T - T0 * T0) * p - 3. * E * T * p * p + lam * p * p * p;
    return d;
  }
  Eigen::VectorXd d2V_dxdt(Eigen::VectorXd x, double T) const override {
    const double p = x[0];
    Eigen::VectorXd d(1);
    d(0) = 4. * D * T * p - 3. * E * p * p;
    return d;
  }
  Eigen::MatrixXd d2V_dx2(Eigen::VectorXd x, double T) const override {
    const double p = x[0];
    Eigen::MatrixXd d(1, 1);
    d(0, 0) = 2. * D * (T * T - T0 * T0) - 6. * E * T * p + 3. * lam * p * p;
    return d;
  }

private:
  double D, E, T0, lam;
};

int main() {
  LOGGER(fatal);
  std::string line;
  std::cout << std::setprecision(15);
  while (std::getline(std::cin, line)) {
    if (line.empty()) continue;
    std::istringstream in(line);
    std::string name;
    double D, E, T0, lam, T1, tlow;
    int tight;
    in >> name >> D >> E >> T0 >> lam >> T1 >> tlow >> tight;
    std::vector<double> Ts;
    for (double t; in >> t;) Ts.push_back(t);

    DineForm model(D, E, T0, lam);
    PhaseTracer::PhaseFinder pf(model);
    pf.set_seed(1);
    pf.set_t_low(tlow);                     // V''(0) -> 0 at T0: stay above it
    pf.set_check_hessian_singular(false);
    pf.set_lower_bounds({-100.});
    pf.set_upper_bounds({1.e5});           // the default bound (1600 GeV) cuts the broken phase of BP4
    pf.set_t_high(1.05 * T1);
    pf.set_find_min_x_tol_rel(1e-10);
    pf.set_find_min_x_tol_abs(1e-10);
    pf.set_dt_start_rel(1e-5);
    pf.set_t_jump_rel(1e-6);
    pf.find_phases();

    PhaseTracer::ActionCalculator ac(model);
    if (tight) {
      ac.set_PD_xtol(1e-10);
      ac.set_PD_phitol(1e-10);
    }
    PhaseTracer::TransitionFinder tf(pf, ac);
    tf.set_TC_tol_rel(1e-14);
    tf.set_Tnuc_tol_rel(1e-10);
    tf.set_fit_action_curve(false);
    tf.set_vw(0.95);
    tf.find_transitions();
    const auto trans = tf.get_transitions();
    if (trans.empty()) {
      std::cout << name << "," << tight << ",no transition" << std::endl;
      continue;
    }
    const auto &t0 = trans[0];

    PhaseTracer::GravWaveCalculator gc(tf);
    gc.set_vw(0.95);
    gc.set_epsilon(0.05);                   // kappa_turb = 0.05 kappa_v, as in the note
    gc.set_T_threshold_bubble_collision(0.);  // no bubble collisions (the note neglects them)
    gc.set_min_frequency(1e-6);
    gc.set_max_frequency(10.);
    gc.set_num_frequency(8001);
    const auto sps = gc.calc_spectrums();

    std::cout << name << "," << tight << "," << t0.TC << "," << t0.TN << ","
              << tf.get_action(t0.true_phase, t0.false_phase, t0.TN) / t0.TN;
    if (!sps.empty())
      std::cout << "," << sps[0].alpha << "," << sps[0].beta_H << "," << sps[0].peak_amplitude << "," << sps[0].peak_frequency;
    else
      std::cout << ",nan,nan,nan,nan";
    for (double T : Ts) std::cout << "," << tf.get_action(t0.true_phase, t0.false_phase, T) / T;
    std::cout << std::endl;
  }
  return 0;
}
