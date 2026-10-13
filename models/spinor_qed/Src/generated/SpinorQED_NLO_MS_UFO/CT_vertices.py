# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 13 Oct 2026 09:20:53


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.e__plus__, P.e__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.a, P.e__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_5_7})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.mu__plus__, P.mu__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.a, P.mu__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_5_7})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.e__plus__, P.e__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FF1, L.FF2 ],
               loop_particles = [ [ [P.a, P.e__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_8_8,(0,1,0):C.R2GC_11_1})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.mu__plus__, P.mu__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FF1, L.FF2 ],
               loop_particles = [ [ [P.a, P.mu__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_13_2,(0,1,0):C.R2GC_11_1})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.a, P.a ],
               color = [ '1' ],
               lorentz = [ L.VV1, L.VV2 ],
               loop_particles = [ [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__] ], [ [P.mu__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_4_5,(0,0,2):C.R2GC_4_6,(0,1,1):C.R2GC_2_3})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.a, P.a, P.a, P.a ],
               color = [ '1' ],
               lorentz = [ L.VVVV1 ],
               loop_particles = [ [ [P.e__minus__], [P.mu__minus__] ] ],
               couplings = {(0,0,0):C.R2GC_3_4})

V_7 = CTVertex(name = 'V_7',
               type = 'UV',
               particles = [ P.e__plus__, P.e__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1, L.FFV2 ],
               loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__] ], [ [P.mu__minus__] ] ],
               couplings = {(0,0,0):C.UVGC_5_7,(0,1,1):C.UVGC_10_1,(0,1,2):C.UVGC_10_2,(0,1,0):C.UVGC_10_3})

V_8 = CTVertex(name = 'V_8',
               type = 'UV',
               particles = [ P.mu__plus__, P.mu__minus__, P.a ],
               color = [ '1' ],
               lorentz = [ L.FFV1, L.FFV2 ],
               loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.e__minus__] ], [ [P.mu__minus__] ] ],
               couplings = {(0,0,0):C.UVGC_5_7,(0,1,1):C.UVGC_10_1,(0,1,2):C.UVGC_10_2,(0,1,0):C.UVGC_12_5})

V_9 = CTVertex(name = 'V_9',
               type = 'UV',
               particles = [ P.e__plus__, P.e__minus__ ],
               color = [ '1' ],
               lorentz = [ L.FF1, L.FF2 ],
               loop_particles = [ [ [P.a, P.e__minus__] ] ],
               couplings = {(0,0,0):C.UVGC_8_9,(0,1,0):C.UVGC_7_8})

V_10 = CTVertex(name = 'V_10',
                type = 'UV',
                particles = [ P.mu__plus__, P.mu__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FF1, L.FF2 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ] ],
                couplings = {(0,0,0):C.UVGC_13_6,(0,1,0):C.UVGC_11_4})

V_11 = CTVertex(name = 'V_11',
                type = 'UV',
                particles = [ P.a, P.a ],
                color = [ '1' ],
                lorentz = [ L.VV3 ],
                loop_particles = [ [ [P.e__minus__] ], [ [P.mu__minus__] ] ],
                couplings = {(0,0,0):C.UVGC_9_10,(0,0,1):C.UVGC_9_11})

