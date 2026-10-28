# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 27 Oct 2026 17:53:40



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
ee = Parameter(name = 'ee',
               nature = 'external',
               type = 'real',
               value = 0.5,
               texname = 'e',
               lhablock = 'AHINPUTS',
               lhacode = [ 1 ])

xiA = Parameter(name = 'xiA',
                nature = 'external',
                type = 'real',
                value = 1.,
                texname = '\\xi _A',
                lhablock = 'GAUGE',
                lhacode = [ 1 ])

MA = Parameter(name = 'MA',
               nature = 'external',
               type = 'real',
               value = 1.,
               texname = '\\text{MA}',
               lhablock = 'MASS',
               lhacode = [ 32 ])

MH = Parameter(name = 'MH',
               nature = 'external',
               type = 'real',
               value = 2.5,
               texname = '\\text{MH}',
               lhablock = 'MASS',
               lhacode = [ 25 ])

WA = Parameter(name = 'WA',
               nature = 'external',
               type = 'real',
               value = 0.,
               texname = '\\text{WA}',
               lhablock = 'DECAY',
               lhacode = [ 32 ])

WH = Parameter(name = 'WH',
               nature = 'external',
               type = 'real',
               value = 0.0155549,
               texname = '\\text{WH}',
               lhablock = 'DECAY',
               lhacode = [ 25 ])

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = 'MA/ee',
                texname = '\\text{vev}')

lam = Parameter(name = 'lam',
                nature = 'internal',
                type = 'real',
                value = 'MH**2/(2.*vev**2)',
                texname = '\\lambda')

muH2 = Parameter(name = 'muH2',
                 nature = 'internal',
                 type = 'real',
                 value = 'lam*vev**2',
                 texname = '\\mu ^2')

