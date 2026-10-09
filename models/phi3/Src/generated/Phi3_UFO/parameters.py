# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Fri 9 Oct 2026 14:45:58



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
gphi = Parameter(name = 'gphi',
                 nature = 'external',
                 type = 'real',
                 value = 1.,
                 texname = '\\text{g}',
                 lhablock = 'PHI3BLOCK',
                 lhacode = [ 1 ])

m = Parameter(name = 'm',
              nature = 'external',
              type = 'real',
              value = 1.,
              texname = 'm',
              lhablock = 'MASS',
              lhacode = [ 9000001 ])

