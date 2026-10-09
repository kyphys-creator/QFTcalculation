# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Fri 9 Oct 2026 14:45:58


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.phi, P.phi, P.phi ],
             color = [ '1' ],
             lorentz = [ L.SSS1 ],
             couplings = {(0,0):C.GC_1})

