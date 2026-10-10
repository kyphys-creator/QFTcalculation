# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sat 10 Oct 2026 06:16:34


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'UV',
               particles = [ P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SS3 ],
               loop_particles = [ [ [P.phi] ] ],
               couplings = {(0,0,0):C.UVGC_2_1})

