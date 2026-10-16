# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Thu 15 Oct 2026 20:55:18


from object_library import all_lorentz, Lorentz

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot
try:
   import form_factors as ForFac 
except ImportError:
   pass


S2 = Lorentz(name = 'S2',
             spins = [ 1 ],
             structure = '1')

SS4 = Lorentz(name = 'SS4',
              spins = [ 1, 1 ],
              structure = '1')

SS5 = Lorentz(name = 'SS5',
              spins = [ 1, 1 ],
              structure = 'P(-1,1)**2')

SS6 = Lorentz(name = 'SS6',
              spins = [ 1, 1 ],
              structure = 'P(-1,2)**2')

FF6 = Lorentz(name = 'FF6',
              spins = [ 2, 2 ],
              structure = 'P(-1,1)*Gamma(-1,2,1)')

FF7 = Lorentz(name = 'FF7',
              spins = [ 2, 2 ],
              structure = 'ProjM(2,1)')

FF8 = Lorentz(name = 'FF8',
              spins = [ 2, 2 ],
              structure = 'P(-1,1)*Gamma(-1,2,-2)*ProjM(-2,1)')

FF9 = Lorentz(name = 'FF9',
              spins = [ 2, 2 ],
              structure = 'ProjP(2,1)')

FF10 = Lorentz(name = 'FF10',
               spins = [ 2, 2 ],
               structure = 'P(-1,1)*Gamma(-1,2,-2)*ProjP(-2,1)')

VV6 = Lorentz(name = 'VV6',
              spins = [ 3, 3 ],
              structure = 'P(1,1)*P(2,1)')

VV7 = Lorentz(name = 'VV7',
              spins = [ 3, 3 ],
              structure = 'P(1,2)*P(2,2)')

VV8 = Lorentz(name = 'VV8',
              spins = [ 3, 3 ],
              structure = 'Metric(1,2)')

VV9 = Lorentz(name = 'VV9',
              spins = [ 3, 3 ],
              structure = 'P(-1,1)**2*Metric(1,2)')

VV10 = Lorentz(name = 'VV10',
               spins = [ 3, 3 ],
               structure = 'P(-1,2)**2*Metric(1,2)')

UUS2 = Lorentz(name = 'UUS2',
               spins = [ -1, -1, 1 ],
               structure = '1')

UUV3 = Lorentz(name = 'UUV3',
               spins = [ -1, -1, 3 ],
               structure = 'P(3,2)')

UUV4 = Lorentz(name = 'UUV4',
               spins = [ -1, -1, 3 ],
               structure = 'P(3,3)')

SSS2 = Lorentz(name = 'SSS2',
               spins = [ 1, 1, 1 ],
               structure = '1')

FFS5 = Lorentz(name = 'FFS5',
               spins = [ 2, 2, 1 ],
               structure = 'Gamma5(2,1)')

FFS6 = Lorentz(name = 'FFS6',
               spins = [ 2, 2, 1 ],
               structure = 'Identity(2,1)')

FFS7 = Lorentz(name = 'FFS7',
               spins = [ 2, 2, 1 ],
               structure = 'ProjM(2,1)')

FFS8 = Lorentz(name = 'FFS8',
               spins = [ 2, 2, 1 ],
               structure = 'ProjP(2,1)')

FFV4 = Lorentz(name = 'FFV4',
               spins = [ 2, 2, 3 ],
               structure = 'Gamma(3,2,1)')

FFV5 = Lorentz(name = 'FFV5',
               spins = [ 2, 2, 3 ],
               structure = 'Gamma(3,2,-1)*ProjM(-1,1)')

FFV6 = Lorentz(name = 'FFV6',
               spins = [ 2, 2, 3 ],
               structure = 'Gamma(3,2,-1)*ProjP(-1,1)')

VSS5 = Lorentz(name = 'VSS5',
               spins = [ 3, 1, 1 ],
               structure = 'P(1,2)')

VSS6 = Lorentz(name = 'VSS6',
               spins = [ 3, 1, 1 ],
               structure = 'P(1,2) - P(1,3)')

VSS7 = Lorentz(name = 'VSS7',
               spins = [ 3, 1, 1 ],
               structure = '1.*P(1,2) - 1.*P(1,3)')

VSS8 = Lorentz(name = 'VSS8',
               spins = [ 3, 1, 1 ],
               structure = 'P(1,3)')

VVS2 = Lorentz(name = 'VVS2',
               spins = [ 3, 3, 1 ],
               structure = 'Metric(1,2)')

VVV16 = Lorentz(name = 'VVV16',
                spins = [ 3, 3, 3 ],
                structure = 'P(3,1)*Metric(1,2)')

VVV17 = Lorentz(name = 'VVV17',
                spins = [ 3, 3, 3 ],
                structure = 'P(3,2)*Metric(1,2)')

VVV18 = Lorentz(name = 'VVV18',
                spins = [ 3, 3, 3 ],
                structure = 'P(3,3)*Metric(1,2)')

VVV19 = Lorentz(name = 'VVV19',
                spins = [ 3, 3, 3 ],
                structure = 'P(2,1)*Metric(1,3)')

VVV20 = Lorentz(name = 'VVV20',
                spins = [ 3, 3, 3 ],
                structure = 'P(2,2)*Metric(1,3)')

VVV21 = Lorentz(name = 'VVV21',
                spins = [ 3, 3, 3 ],
                structure = 'P(2,3)*Metric(1,3)')

VVV22 = Lorentz(name = 'VVV22',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,1)*Metric(1,2) + 1.*P(3,2)*Metric(1,2) + 1.*P(3,3)*Metric(1,2) + 1.*P(2,1)*Metric(1,3) + 1.*P(2,2)*Metric(1,3) + 1.*P(2,3)*Metric(1,3)')

VVV23 = Lorentz(name = 'VVV23',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,1)*Metric(1,2) + 1.*P(3,2)*Metric(1,2) + 1.*P(3,3)*Metric(1,2) + 1.*P(2,1)*Metric(1,3) + 1.*P(2,2)*Metric(1,3) + 1.*P(2,3)*Metric(1,3)')

VVV24 = Lorentz(name = 'VVV24',
                spins = [ 3, 3, 3 ],
                structure = 'P(1,1)*Metric(2,3)')

VVV25 = Lorentz(name = 'VVV25',
                spins = [ 3, 3, 3 ],
                structure = 'P(1,2)*Metric(2,3)')

VVV26 = Lorentz(name = 'VVV26',
                spins = [ 3, 3, 3 ],
                structure = 'P(1,3)*Metric(2,3)')

VVV27 = Lorentz(name = 'VVV27',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,3)*Metric(1,2) - 0.333333333333333333333333333333333333333*P(2,1)*Metric(1,3) + 0.666666666666666666666666666666666666667*P(2,2)*Metric(1,3) - 0.333333333333333333333333333333333333333*P(2,3)*Metric(1,3) - 1.*P(1,2)*Metric(2,3) - 1.*P(1,3)*Metric(2,3)')

VVV28 = Lorentz(name = 'VVV28',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,3)*Metric(1,2) - 1.*P(2,1)*Metric(1,3) - 1.*P(2,3)*Metric(1,3) - 1.*P(1,2)*Metric(2,3) - 1.*P(1,3)*Metric(2,3)')

VVV29 = Lorentz(name = 'VVV29',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,1)*Metric(1,2) + 1.*P(3,2)*Metric(1,2) + 1.*P(2,1)*Metric(1,3) + 1.*P(2,3)*Metric(1,3) + 1.*P(1,2)*Metric(2,3) + 1.*P(1,3)*Metric(2,3)')

VVV30 = Lorentz(name = 'VVV30',
                spins = [ 3, 3, 3 ],
                structure = '1.*P(3,1)*Metric(1,2) + 1.*P(3,2)*Metric(1,2) + 1.*P(2,1)*Metric(1,3) + 1.*P(2,3)*Metric(1,3) + 1.*P(1,2)*Metric(2,3) + 1.*P(1,3)*Metric(2,3)')

SSSS2 = Lorentz(name = 'SSSS2',
                spins = [ 1, 1, 1, 1 ],
                structure = '1')

VVSS2 = Lorentz(name = 'VVSS2',
                spins = [ 3, 3, 1, 1 ],
                structure = 'Metric(1,2)')

VVVV7 = Lorentz(name = 'VVVV7',
                spins = [ 3, 3, 3, 3 ],
                structure = 'Epsilon(1,2,3,4)')

VVVV8 = Lorentz(name = 'VVVV8',
                spins = [ 3, 3, 3, 3 ],
                structure = 'Metric(1,4)*Metric(2,3)')

VVVV9 = Lorentz(name = 'VVVV9',
                spins = [ 3, 3, 3, 3 ],
                structure = 'Metric(1,3)*Metric(2,4)')

VVVV10 = Lorentz(name = 'VVVV10',
                 spins = [ 3, 3, 3, 3 ],
                 structure = 'Metric(1,2)*Metric(3,4)')

VVVV11 = Lorentz(name = 'VVVV11',
                 spins = [ 3, 3, 3, 3 ],
                 structure = 'Metric(1,4)*Metric(2,3) + Metric(1,3)*Metric(2,4) + Metric(1,2)*Metric(3,4)')

VVVV12 = Lorentz(name = 'VVVV12',
                 spins = [ 3, 3, 3, 3 ],
                 structure = '1.*Metric(1,4)*Metric(2,3) + 1.*Metric(1,3)*Metric(2,4) + 1.*Metric(1,2)*Metric(3,4)')

