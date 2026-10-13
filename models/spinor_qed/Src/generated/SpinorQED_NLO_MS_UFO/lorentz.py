# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 13 Oct 2026 09:20:53


from object_library import all_lorentz, Lorentz

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot
try:
   import form_factors as ForFac 
except ImportError:
   pass


FF1 = Lorentz(name = 'FF1',
              spins = [ 2, 2 ],
              structure = 'ProjM(2,1) + ProjP(2,1)')

FF2 = Lorentz(name = 'FF2',
              spins = [ 2, 2 ],
              structure = 'P(-1,1)*Gamma(-1,2,-2)*ProjM(-2,1) + P(-1,1)*Gamma(-1,2,-2)*ProjP(-2,1)')

VV1 = Lorentz(name = 'VV1',
              spins = [ 3, 3 ],
              structure = 'Metric(1,2)')

VV2 = Lorentz(name = 'VV2',
              spins = [ 3, 3 ],
              structure = 'P(-1,2)**2*Metric(1,2)')

VV3 = Lorentz(name = 'VV3',
              spins = [ 3, 3 ],
              structure = 'P(1,2)*P(2,2) - P(-1,2)**2*Metric(1,2)')

FFV1 = Lorentz(name = 'FFV1',
               spins = [ 2, 2, 3 ],
               structure = 'Gamma(3,2,1)')

FFV2 = Lorentz(name = 'FFV2',
               spins = [ 2, 2, 3 ],
               structure = 'Gamma(3,2,-1)*ProjM(-1,1) + Gamma(3,2,-1)*ProjP(-1,1)')

VVVV1 = Lorentz(name = 'VVVV1',
                spins = [ 3, 3, 3, 3 ],
                structure = 'Metric(1,4)*Metric(2,3) + Metric(1,3)*Metric(2,4) + Metric(1,2)*Metric(3,4)')

