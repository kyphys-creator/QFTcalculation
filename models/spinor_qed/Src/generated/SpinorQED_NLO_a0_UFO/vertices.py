# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 13 Oct 2026 09:20:53


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.e__plus__, P.e__minus__, P.a ],
             color = [ '1' ],
             lorentz = [ L.FFV3 ],
             couplings = {(0,0):C.GC_1})

V_2 = Vertex(name = 'V_2',
             particles = [ P.mu__plus__, P.mu__minus__, P.a ],
             color = [ '1' ],
             lorentz = [ L.FFV3 ],
             couplings = {(0,0):C.GC_1})

