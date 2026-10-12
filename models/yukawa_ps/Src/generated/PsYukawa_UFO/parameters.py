# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Mon 12 Oct 2026 11:13:47



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
yps = Parameter(name = 'yps',
                nature = 'external',
                type = 'real',
                value = 1.,
                texname = '\\text{y}',
                lhablock = 'PSYBLOCK',
                lhacode = [ 1 ])

lamphi = Parameter(name = 'lamphi',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{$\\backslash \\backslash $lambda}',
                   lhablock = 'PSYBLOCK',
                   lhacode = [ 2 ])

mphi = Parameter(name = 'mphi',
                 nature = 'external',
                 type = 'real',
                 value = 1.,
                 texname = '\\text{mphi}',
                 lhablock = 'MASS',
                 lhacode = [ 9000001 ])

Mpsi = Parameter(name = 'Mpsi',
                 nature = 'external',
                 type = 'real',
                 value = 0.7,
                 texname = '\\text{Mpsi}',
                 lhablock = 'MASS',
                 lhacode = [ 9000002 ])

