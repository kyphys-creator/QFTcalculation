# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sun 11 Oct 2026 08:24:48


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'UV',
               particles = [ P.phi, P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SSS2 ],
               loop_particles = [ [ [P.phi] ] ],
               couplings = {(0,0,0):C.UVGC_3_1})

V_2 = CTVertex(name = 'V_2',
               type = 'UV',
               particles = [ P.phi, P.phi, P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SSSS2 ],
               loop_particles = [ [ [P.phi] ] ],
               couplings = {(0,0,0):C.UVGC_4_2})

V_3 = CTVertex(name = 'V_3',
               type = 'UV',
               particles = [ P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SS3 ],
               loop_particles = [ [ [P.phi] ] ],
               couplings = {(0,0,0):C.UVGC_5_3})

