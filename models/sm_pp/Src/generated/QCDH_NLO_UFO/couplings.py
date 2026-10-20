# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 12:21:32


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



GC_1 = Coupling(name = 'GC_1',
                value = '-G',
                order = {'QCD':1})

GC_2 = Coupling(name = 'GC_2',
                value = 'complex(0,1)*G',
                order = {'QCD':1})

GC_3 = Coupling(name = 'GC_3',
                value = 'complex(0,1)*G**2',
                order = {'QCD':2})

GC_4 = Coupling(name = 'GC_4',
                value = '(aS*complex(0,1)*kHgg)/(3.*cmath.pi*vev)',
                order = {'HIG':1,'QCD':2})

GC_5 = Coupling(name = 'GC_5',
                value = '(aS*G*kHgg)/(3.*cmath.pi*vev)',
                order = {'HIG':1,'QCD':3})

GC_6 = Coupling(name = 'GC_6',
                value = '-(1./3.)*(aS*complex(0,1)*G**2*kHgg)/(cmath.pi*vev)',
                order = {'HIG':1,'QCD':4})
