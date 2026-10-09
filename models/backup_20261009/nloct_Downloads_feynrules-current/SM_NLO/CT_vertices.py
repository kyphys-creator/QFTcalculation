# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.1.0 for Mac OS X ARM (64-bit) (July 16, 2024)
# Date: Mon 25 Nov 2024 13:42:58


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV2 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_212_48,(0,0,1):C.R2GC_212_49})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV10, L.VVVV2, L.VVVV3, L.VVVV5 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(2,1,0):C.R2GC_180_32,(2,1,1):C.R2GC_180_33,(0,1,0):C.R2GC_180_32,(0,1,1):C.R2GC_180_33,(4,1,0):C.R2GC_178_28,(4,1,1):C.R2GC_178_29,(3,1,0):C.R2GC_178_28,(3,1,1):C.R2GC_178_29,(8,1,0):C.R2GC_179_30,(8,1,1):C.R2GC_179_31,(6,1,0):C.R2GC_183_37,(6,1,1):C.R2GC_217_55,(7,1,0):C.R2GC_184_39,(7,1,1):C.R2GC_216_54,(5,1,0):C.R2GC_178_28,(5,1,1):C.R2GC_178_29,(1,1,0):C.R2GC_178_28,(1,1,1):C.R2GC_178_29,(11,0,0):C.R2GC_182_35,(11,0,1):C.R2GC_182_36,(10,0,0):C.R2GC_182_35,(10,0,1):C.R2GC_182_36,(9,0,1):C.R2GC_181_34,(0,2,0):C.R2GC_180_32,(0,2,1):C.R2GC_180_33,(2,2,0):C.R2GC_180_32,(2,2,1):C.R2GC_180_33,(5,2,0):C.R2GC_178_28,(5,2,1):C.R2GC_178_29,(1,2,0):C.R2GC_178_28,(1,2,1):C.R2GC_178_29,(7,2,0):C.R2GC_184_39,(7,2,1):C.R2GC_184_40,(4,2,0):C.R2GC_178_28,(4,2,1):C.R2GC_178_29,(3,2,0):C.R2GC_178_28,(3,2,1):C.R2GC_178_29,(8,2,0):C.R2GC_179_30,(8,2,1):C.R2GC_218_56,(6,2,0):C.R2GC_213_50,(6,2,1):C.R2GC_213_51,(0,3,0):C.R2GC_180_32,(0,3,1):C.R2GC_180_33,(2,3,0):C.R2GC_180_32,(2,3,1):C.R2GC_180_33,(5,3,0):C.R2GC_178_28,(5,3,1):C.R2GC_178_29,(1,3,0):C.R2GC_178_28,(1,3,1):C.R2GC_178_29,(7,3,0):C.R2GC_214_52,(7,3,1):C.R2GC_180_33,(4,3,0):C.R2GC_178_28,(4,3,1):C.R2GC_178_29,(3,3,0):C.R2GC_178_28,(3,3,1):C.R2GC_178_29,(8,3,0):C.R2GC_179_30,(8,3,1):C.R2GC_215_53,(6,3,0):C.R2GC_183_37,(6,3,1):C.R2GC_183_38})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.t__tilde__, P.b, P.G__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               loop_particles = [ [ [P.b, P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_227_59,(0,1,0):C.R2GC_228_60})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS1 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_210_47})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.H ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_209_46})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.b__tilde__, P.t, P.G__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               loop_particles = [ [ [P.b, P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_229_61,(0,1,0):C.R2GC_226_58})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.t__tilde__, P.t, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS1 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_230_62})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.t__tilde__, P.t, P.H ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_231_63})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.u__tilde__, P.u, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,0,0):C.R2GC_187_43})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_187_43})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_187_43})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_185_41})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_185_41})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_185_41})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_186_42})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.b, P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.b, P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_201_44})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_161_24,(0,1,0):C.R2GC_144_3})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_161_24,(0,1,0):C.R2GC_144_3})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_161_24,(0,1,0):C.R2GC_144_3})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_162_25,(0,1,0):C.R2GC_146_4})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_162_25,(0,1,0):C.R2GC_146_4})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_162_25,(0,1,0):C.R2GC_146_4})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_143_2})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_143_2})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_222_57,(0,1,0):C.R2GC_143_2})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_143_2})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_143_2})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_206_45,(0,1,0):C.R2GC_143_2})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV2, L.VV3, L.VV4 ],
                loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ], [ [P.t] ] ],
                couplings = {(0,2,2):C.R2GC_142_1,(0,0,0):C.R2GC_151_5,(0,0,3):C.R2GC_151_6,(0,1,1):C.R2GC_154_11})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.g, P.g, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_152_7,(0,0,1):C.R2GC_152_8})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV10 ],
                loop_particles = [ [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_165_27})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.Z ],
                color = [ 'Identity(2,3)' ],
                lorentz = [ L.VVVV10 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_157_16,(0,0,1):C.R2GC_157_17})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.g, P.g, P.Z, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV10 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_160_22,(0,0,1):C.R2GC_160_23})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.a, P.a, P.g, P.g ],
                color = [ 'Identity(3,4)' ],
                lorentz = [ L.VVVV10 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_155_12,(0,0,1):C.R2GC_155_13})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.Z ],
                color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV10 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(1,0,0):C.R2GC_159_20,(1,0,1):C.R2GC_159_21,(0,1,0):C.R2GC_158_18,(0,1,1):C.R2GC_158_19})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.g ],
                color = [ 'd(2,3,4)' ],
                lorentz = [ L.VVVV10 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_156_14,(0,0,1):C.R2GC_156_15})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.g, P.g, P.H, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_153_9,(0,0,1):C.R2GC_153_10})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.g, P.g, P.G0, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_153_9,(0,0,1):C.R2GC_153_10})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_164_26})

V_50 = CTVertex(name = 'V_50',
                type = 'UV',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,1,0):C.UVGC_212_41,(0,1,1):C.UVGC_212_42,(0,1,4):C.UVGC_212_43,(0,2,2):C.UVGC_167_1,(0,0,3):C.UVGC_168_2})

V_51 = CTVertex(name = 'V_51',
                type = 'UV',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV10, L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(2,1,3):C.UVGC_179_11,(2,1,4):C.UVGC_179_10,(0,1,3):C.UVGC_179_11,(0,1,4):C.UVGC_179_10,(4,1,3):C.UVGC_178_8,(4,1,4):C.UVGC_178_9,(3,1,3):C.UVGC_178_8,(3,1,4):C.UVGC_178_9,(8,1,3):C.UVGC_179_10,(8,1,4):C.UVGC_179_11,(6,1,0):C.UVGC_216_55,(6,1,2):C.UVGC_216_56,(6,1,3):C.UVGC_217_60,(6,1,4):C.UVGC_217_61,(6,1,5):C.UVGC_216_59,(7,1,0):C.UVGC_216_55,(7,1,2):C.UVGC_216_56,(7,1,3):C.UVGC_216_57,(7,1,4):C.UVGC_216_58,(7,1,5):C.UVGC_216_59,(5,1,3):C.UVGC_178_8,(5,1,4):C.UVGC_178_9,(1,1,3):C.UVGC_178_8,(1,1,4):C.UVGC_178_9,(11,0,3):C.UVGC_182_14,(11,0,4):C.UVGC_182_15,(10,0,3):C.UVGC_182_14,(10,0,4):C.UVGC_182_15,(9,0,3):C.UVGC_181_12,(9,0,4):C.UVGC_181_13,(0,2,3):C.UVGC_179_11,(0,2,4):C.UVGC_179_10,(2,2,3):C.UVGC_179_11,(2,2,4):C.UVGC_179_10,(5,2,3):C.UVGC_178_8,(5,2,4):C.UVGC_178_9,(1,2,3):C.UVGC_178_8,(1,2,4):C.UVGC_178_9,(7,2,1):C.UVGC_183_16,(7,2,3):C.UVGC_184_18,(7,2,4):C.UVGC_184_19,(4,2,3):C.UVGC_178_8,(4,2,4):C.UVGC_178_9,(3,2,3):C.UVGC_178_8,(3,2,4):C.UVGC_178_9,(8,2,0):C.UVGC_218_62,(8,2,2):C.UVGC_218_63,(8,2,3):C.UVGC_218_64,(8,2,4):C.UVGC_218_65,(8,2,5):C.UVGC_218_66,(6,2,0):C.UVGC_213_44,(6,2,3):C.UVGC_213_45,(6,2,4):C.UVGC_213_46,(6,2,5):C.UVGC_213_47,(0,3,3):C.UVGC_179_11,(0,3,4):C.UVGC_179_10,(2,3,3):C.UVGC_179_11,(2,3,4):C.UVGC_179_10,(5,3,3):C.UVGC_178_8,(5,3,4):C.UVGC_178_9,(1,3,3):C.UVGC_178_8,(1,3,4):C.UVGC_178_9,(7,3,0):C.UVGC_213_44,(7,3,3):C.UVGC_214_48,(7,3,4):C.UVGC_214_49,(7,3,5):C.UVGC_213_47,(4,3,3):C.UVGC_178_8,(4,3,4):C.UVGC_178_9,(3,3,3):C.UVGC_178_8,(3,3,4):C.UVGC_178_9,(8,3,0):C.UVGC_215_50,(8,3,2):C.UVGC_215_51,(8,3,3):C.UVGC_215_52,(8,3,4):C.UVGC_215_53,(8,3,5):C.UVGC_215_54,(6,3,1):C.UVGC_183_16,(6,3,3):C.UVGC_183_17,(6,3,4):C.UVGC_181_12})

V_52 = CTVertex(name = 'V_52',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS5 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_227_78,(0,0,2):C.UVGC_227_79,(0,0,1):C.UVGC_227_80,(0,1,0):C.UVGC_228_81,(0,1,2):C.UVGC_228_82,(0,1,1):C.UVGC_228_83})

V_53 = CTVertex(name = 'V_53',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_210_38})

V_54 = CTVertex(name = 'V_54',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_209_37})

V_55 = CTVertex(name = 'V_55',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS5 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_229_84,(0,0,2):C.UVGC_229_85,(0,0,1):C.UVGC_229_86,(0,1,0):C.UVGC_226_75,(0,1,2):C.UVGC_226_76,(0,1,1):C.UVGC_226_77})

V_56 = CTVertex(name = 'V_56',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_230_87})

V_57 = CTVertex(name = 'V_57',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_231_88})

V_58 = CTVertex(name = 'V_58',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_187_22,(0,1,0):C.UVGC_170_4,(0,2,0):C.UVGC_170_4})

V_59 = CTVertex(name = 'V_59',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_187_22,(0,1,0):C.UVGC_170_4,(0,2,0):C.UVGC_170_4})

V_60 = CTVertex(name = 'V_60',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_187_22,(0,1,0):C.UVGC_220_68,(0,2,0):C.UVGC_220_68})

V_61 = CTVertex(name = 'V_61',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_185_20,(0,1,0):C.UVGC_172_5,(0,2,0):C.UVGC_172_5})

V_62 = CTVertex(name = 'V_62',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_185_20,(0,1,0):C.UVGC_172_5,(0,2,0):C.UVGC_172_5})

V_63 = CTVertex(name = 'V_63',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_185_20,(0,1,0):C.UVGC_204_32,(0,2,0):C.UVGC_204_32})

V_64 = CTVertex(name = 'V_64',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ], [ [P.t] ] ],
                couplings = {(0,0,4):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,1):C.UVGC_188_24,(0,1,2):C.UVGC_188_25,(0,1,3):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,4):C.UVGC_188_28,(0,2,0):C.UVGC_188_23,(0,2,1):C.UVGC_188_24,(0,2,2):C.UVGC_188_25,(0,2,3):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,4):C.UVGC_188_28})

V_65 = CTVertex(name = 'V_65',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.c, P.g] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,2):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,1):C.UVGC_188_24,(0,1,3):C.UVGC_188_25,(0,1,4):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,2):C.UVGC_188_28,(0,2,0):C.UVGC_188_23,(0,2,1):C.UVGC_188_24,(0,2,3):C.UVGC_188_25,(0,2,4):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,2):C.UVGC_188_28})

V_66 = CTVertex(name = 'V_66',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.t] ], [ [P.t] ] ],
                couplings = {(0,0,4):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,1):C.UVGC_188_24,(0,1,2):C.UVGC_188_25,(0,1,3):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,4):C.UVGC_221_69,(0,2,0):C.UVGC_188_23,(0,2,1):C.UVGC_188_24,(0,2,2):C.UVGC_188_25,(0,2,3):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,4):C.UVGC_221_69})

V_67 = CTVertex(name = 'V_67',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.d, P.g] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,2):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,1):C.UVGC_188_24,(0,1,3):C.UVGC_188_25,(0,1,4):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,2):C.UVGC_188_28,(0,2,0):C.UVGC_188_23,(0,2,1):C.UVGC_188_24,(0,2,3):C.UVGC_188_25,(0,2,4):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,2):C.UVGC_188_28})

V_68 = CTVertex(name = 'V_68',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ], [ [P.t] ] ],
                couplings = {(0,0,4):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,1):C.UVGC_188_24,(0,1,2):C.UVGC_188_25,(0,1,3):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,4):C.UVGC_188_28,(0,2,0):C.UVGC_188_23,(0,2,1):C.UVGC_188_24,(0,2,2):C.UVGC_188_25,(0,2,3):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,4):C.UVGC_188_28})

V_69 = CTVertex(name = 'V_69',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b] ], [ [P.b, P.g] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,1):C.UVGC_186_21,(0,1,0):C.UVGC_188_23,(0,1,2):C.UVGC_188_24,(0,1,3):C.UVGC_188_25,(0,1,4):C.UVGC_188_26,(0,1,5):C.UVGC_188_27,(0,1,1):C.UVGC_205_33,(0,2,0):C.UVGC_188_23,(0,2,2):C.UVGC_188_24,(0,2,3):C.UVGC_188_25,(0,2,4):C.UVGC_188_26,(0,2,5):C.UVGC_188_27,(0,2,1):C.UVGC_205_33})

V_70 = CTVertex(name = 'V_70',
                type = 'UV',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_201_29,(0,0,1):C.UVGC_201_30})

V_71 = CTVertex(name = 'V_71',
                type = 'UV',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.c, P.g], [P.g, P.s] ], [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_201_29,(0,0,1):C.UVGC_201_30})

V_72 = CTVertex(name = 'V_72',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_223_71,(0,0,2):C.UVGC_223_72,(0,0,1):C.UVGC_201_30})

V_73 = CTVertex(name = 'V_73',
                type = 'UV',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_201_29,(0,0,1):C.UVGC_201_30})

V_74 = CTVertex(name = 'V_74',
                type = 'UV',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.c, P.g], [P.g, P.s] ], [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_201_29,(0,0,1):C.UVGC_201_30})

V_75 = CTVertex(name = 'V_75',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_223_71,(0,0,2):C.UVGC_223_72,(0,0,1):C.UVGC_201_30})

V_76 = CTVertex(name = 'V_76',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_224_73,(0,1,0):C.UVGC_225_74})

V_77 = CTVertex(name = 'V_77',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_207_35,(0,1,0):C.UVGC_208_36})

V_78 = CTVertex(name = 'V_78',
                type = 'UV',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_169_3})

V_79 = CTVertex(name = 'V_79',
                type = 'UV',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_169_3})

V_80 = CTVertex(name = 'V_80',
                type = 'UV',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_222_70,(0,1,0):C.UVGC_219_67})

V_81 = CTVertex(name = 'V_81',
                type = 'UV',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_169_3})

V_82 = CTVertex(name = 'V_82',
                type = 'UV',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_169_3})

V_83 = CTVertex(name = 'V_83',
                type = 'UV',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_206_34,(0,1,0):C.UVGC_203_31})

V_84 = CTVertex(name = 'V_84',
                type = 'UV',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1, L.VV5 ],
                loop_particles = [ [ [P.b] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,1,0):C.UVGC_211_39,(0,1,3):C.UVGC_211_40,(0,0,1):C.UVGC_177_6,(0,0,2):C.UVGC_177_7})

