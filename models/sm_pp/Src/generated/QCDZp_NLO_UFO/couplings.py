# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 14:26:05


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



GC_1 = Coupling(name = 'GC_1',
                value = '-G',
                order = {'QCD':1})

GC_2 = Coupling(name = 'GC_2',
                value = 'complex(0,1)*G',
                order = {'QCD':1})

GC_3 = Coupling(name = 'GC_3',
                value = '-(complex(0,1)*G**2)',
                order = {'QCD':2})

GC_4 = Coupling(name = 'GC_4',
                value = 'complex(0,1)*G**2',
                order = {'QCD':2})

GC_5 = Coupling(name = 'GC_5',
                value = '-0.5*(ee*complex(0,1)*gZp)/(cw*sw)',
                order = {'QED':1})

GC_6 = Coupling(name = 'GC_6',
                value = '(ee*complex(0,1)*gZp)/(2.*cw*sw)',
                order = {'QED':1})

GC_7 = Coupling(name = 'GC_7',
                value = '(ee*complex(0,1)*gZp*sw)/(3.*cw)',
                order = {'QED':1})

GC_8 = Coupling(name = 'GC_8',
                value = '(-2*ee*complex(0,1)*gZp*sw)/(3.*cw)',
                order = {'QED':1})

GC_9 = Coupling(name = 'GC_9',
                value = '(ee*complex(0,1)*gZp*sw)/cw',
                order = {'QED':1})
