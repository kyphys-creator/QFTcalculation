# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sat 10 Oct 2026 06:16:34


from object_library import all_lorentz, Lorentz

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot
try:
   import form_factors as ForFac 
except ImportError:
   pass


SS1 = Lorentz(name = 'SS1',
              spins = [ 1, 1 ],
              structure = '1')

SS2 = Lorentz(name = 'SS2',
              spins = [ 1, 1 ],
              structure = 'P(-1,2)**2')

SSS1 = Lorentz(name = 'SSS1',
               spins = [ 1, 1, 1 ],
               structure = '1')

