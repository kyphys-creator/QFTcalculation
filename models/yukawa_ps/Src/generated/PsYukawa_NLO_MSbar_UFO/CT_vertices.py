# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Mon 12 Oct 2026 13:29:08


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.phi, P.phi, P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SSSS2 ],
               loop_particles = [ [ [P.psi] ] ],
               couplings = {(0,0,0):C.R2GC_4_2})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.psi__tilde__, P.psi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.phi, P.psi] ] ],
               couplings = {(0,0,0):C.R2GC_8_4})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SS3, L.SS4 ],
               loop_particles = [ [ [P.psi] ] ],
               couplings = {(0,0,0):C.R2GC_5_3,(0,1,0):C.R2GC_3_1})

V_4 = CTVertex(name = 'V_4',
               type = 'UV',
               particles = [ P.phi, P.phi, P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SSSS2 ],
               loop_particles = [ [ [P.phi] ], [ [P.psi] ] ],
               couplings = {(0,0,0):C.UVGC_4_2,(0,0,1):C.UVGC_4_3})

V_5 = CTVertex(name = 'V_5',
               type = 'UV',
               particles = [ P.psi__tilde__, P.psi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.phi, P.psi] ], [ [P.psi] ] ],
               couplings = {(0,0,1):C.UVGC_8_8,(0,0,0):C.UVGC_8_9})

V_6 = CTVertex(name = 'V_6',
               type = 'UV',
               particles = [ P.phi, P.phi ],
               color = [ '1' ],
               lorentz = [ L.SS3, L.SS4 ],
               loop_particles = [ [ [P.phi] ], [ [P.psi] ] ],
               couplings = {(0,0,0):C.UVGC_5_4,(0,0,1):C.UVGC_5_5,(0,1,1):C.UVGC_3_1})

V_7 = CTVertex(name = 'V_7',
               type = 'UV',
               particles = [ P.psi__tilde__, P.psi ],
               color = [ '1' ],
               lorentz = [ L.FF3, L.FF4 ],
               loop_particles = [ [ [P.phi, P.psi] ] ],
               couplings = {(0,0,0):C.UVGC_7_7,(0,1,0):C.UVGC_6_6})

