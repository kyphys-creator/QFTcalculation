# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Fri 16 Oct 2026 20:08:44


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_254_344,(0,0,1):C.R2GC_254_345,(0,0,2):C.R2GC_254_346,(0,0,3):C.R2GC_254_347,(0,0,6):C.R2GC_254_348,(0,0,7):C.R2GC_254_349,(0,0,8):C.R2GC_254_350,(0,0,9):C.R2GC_254_351,(0,0,10):C.R2GC_254_352,(0,0,11):C.R2GC_254_353,(0,0,12):C.R2GC_254_354,(0,0,4):C.R2GC_254_356,(0,0,5):C.R2GC_254_355})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,20):C.R2GC_331_859,(0,0,22):C.R2GC_353_1109,(0,0,0):C.R2GC_353_1110,(0,0,2):C.R2GC_247_274,(0,0,3):C.R2GC_353_1111,(0,0,4):C.R2GC_353_1112,(0,0,5):C.R2GC_353_1113,(0,0,6):C.R2GC_331_853,(0,0,8):C.R2GC_353_1118,(0,0,12):C.R2GC_353_1116,(0,0,14):C.R2GC_353_1117,(0,0,15):C.R2GC_353_1114,(0,0,17):C.R2GC_353_1115,(0,0,18):C.R2GC_331_854,(0,0,19):C.R2GC_331_857,(0,0,21):C.R2GC_353_1119,(0,0,1):C.R2GC_349_1052,(0,0,7):C.R2GC_353_1123,(0,0,9):C.R2GC_353_1120,(0,0,11):C.R2GC_353_1121,(0,0,13):C.R2GC_353_1124,(0,0,16):C.R2GC_353_1122,(0,0,10):C.R2GC_353_1125})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_276_471,(0,0,12):C.R2GC_276_472,(0,0,13):C.R2GC_276_473,(0,0,1):C.R2GC_276_474,(0,0,3):C.R2GC_276_475,(0,0,4):C.R2GC_276_476,(0,0,5):C.R2GC_276_477,(0,0,6):C.R2GC_276_478,(0,0,7):C.R2GC_276_479,(0,0,8):C.R2GC_276_480,(0,0,9):C.R2GC_276_481,(0,0,10):C.R2GC_276_482,(0,0,11):C.R2GC_276_483,(0,0,2):C.R2GC_276_484})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z], [P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_331_850,(0,0,1):C.R2GC_331_851,(0,0,2):C.R2GC_331_852,(0,0,3):C.R2GC_331_853,(0,0,7):C.R2GC_331_854,(0,0,8):C.R2GC_331_855,(0,0,9):C.R2GC_331_856,(0,0,10):C.R2GC_331_857,(0,0,11):C.R2GC_331_858,(0,0,12):C.R2GC_331_859,(0,0,13):C.R2GC_331_860,(0,0,5):C.R2GC_331_861,(0,0,6):C.R2GC_276_480,(0,0,4):C.R2GC_331_862})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__, P.Z] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,20):C.R2GC_331_859,(0,0,22):C.R2GC_353_1109,(0,0,0):C.R2GC_353_1110,(0,0,2):C.R2GC_247_274,(0,0,3):C.R2GC_353_1111,(0,0,4):C.R2GC_353_1112,(0,0,5):C.R2GC_353_1113,(0,0,6):C.R2GC_331_853,(0,0,10):C.R2GC_353_1114,(0,0,12):C.R2GC_353_1115,(0,0,14):C.R2GC_353_1116,(0,0,16):C.R2GC_353_1117,(0,0,17):C.R2GC_353_1118,(0,0,18):C.R2GC_331_854,(0,0,19):C.R2GC_331_857,(0,0,21):C.R2GC_353_1119,(0,0,1):C.R2GC_349_1052,(0,0,7):C.R2GC_353_1120,(0,0,9):C.R2GC_353_1121,(0,0,11):C.R2GC_353_1122,(0,0,13):C.R2GC_353_1123,(0,0,15):C.R2GC_353_1124,(0,0,8):C.R2GC_353_1125})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.H, P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_254_344,(0,0,1):C.R2GC_254_345,(0,0,2):C.R2GC_254_346,(0,0,3):C.R2GC_254_347,(0,0,6):C.R2GC_254_348,(0,0,7):C.R2GC_254_349,(0,0,8):C.R2GC_254_350,(0,0,9):C.R2GC_254_351,(0,0,10):C.R2GC_254_352,(0,0,11):C.R2GC_254_353,(0,0,12):C.R2GC_254_354,(0,0,4):C.R2GC_254_355,(0,0,5):C.R2GC_254_356})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_332_863,(0,0,1):C.R2GC_332_864,(0,0,2):C.R2GC_332_865,(0,0,3):C.R2GC_332_866,(0,0,7):C.R2GC_332_867,(0,0,8):C.R2GC_332_868,(0,0,9):C.R2GC_332_869,(0,0,10):C.R2GC_332_870,(0,0,11):C.R2GC_332_871,(0,0,12):C.R2GC_332_872,(0,0,13):C.R2GC_332_873,(0,0,5):C.R2GC_332_874,(0,0,6):C.R2GC_332_875,(0,0,4):C.R2GC_332_876})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,15):C.R2GC_332_872,(0,0,17):C.R2GC_338_942,(0,0,0):C.R2GC_338_943,(0,0,2):C.R2GC_250_307,(0,0,3):C.R2GC_338_944,(0,0,4):C.R2GC_338_945,(0,0,5):C.R2GC_338_946,(0,0,6):C.R2GC_332_866,(0,0,7):C.R2GC_338_947,(0,0,11):C.R2GC_338_948,(0,0,12):C.R2GC_338_949,(0,0,13):C.R2GC_332_867,(0,0,14):C.R2GC_332_870,(0,0,16):C.R2GC_338_950,(0,0,1):C.R2GC_338_951,(0,0,8):C.R2GC_338_952,(0,0,9):C.R2GC_338_953,(0,0,10):C.R2GC_338_954})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_255_357,(0,0,1):C.R2GC_255_358,(0,0,2):C.R2GC_255_359,(0,0,3):C.R2GC_255_360,(0,0,6):C.R2GC_255_361,(0,0,7):C.R2GC_255_362,(0,0,8):C.R2GC_255_363,(0,0,9):C.R2GC_255_364,(0,0,10):C.R2GC_255_365,(0,0,11):C.R2GC_255_366,(0,0,12):C.R2GC_255_367,(0,0,4):C.R2GC_255_368,(0,0,5):C.R2GC_255_369})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,9):C.R2GC_247_274,(0,0,0):C.R2GC_258_385,(0,0,1):C.R2GC_258_386,(0,0,2):C.R2GC_258_387,(0,0,3):C.R2GC_258_388,(0,0,4):C.R2GC_258_389,(0,0,5):C.R2GC_258_390,(0,0,6):C.R2GC_258_391,(0,0,7):C.R2GC_258_392,(0,0,8):C.R2GC_258_393})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_257_376,(0,0,1):C.R2GC_257_377,(0,0,2):C.R2GC_257_378,(0,0,3):C.R2GC_257_379,(0,0,4):C.R2GC_257_380,(0,0,5):C.R2GC_257_381,(0,0,6):C.R2GC_257_382,(0,0,7):C.R2GC_257_383,(0,0,8):C.R2GC_257_384})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV7 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
                couplings = {(0,0,0):C.R2GC_131_19,(0,0,1):C.R2GC_131_20})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5, L.VVVV8 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
                couplings = {(2,0,0):C.R2GC_138_31,(2,0,1):C.R2GC_138_32,(0,0,0):C.R2GC_138_31,(0,0,1):C.R2GC_138_32,(4,0,0):C.R2GC_133_23,(4,0,1):C.R2GC_133_24,(3,0,0):C.R2GC_133_23,(3,0,1):C.R2GC_133_24,(8,0,0):C.R2GC_135_27,(8,0,1):C.R2GC_135_28,(6,0,0):C.R2GC_141_36,(6,0,1):C.R2GC_141_37,(7,0,0):C.R2GC_139_33,(7,0,1):C.R2GC_139_34,(5,0,0):C.R2GC_133_23,(5,0,1):C.R2GC_133_24,(1,0,0):C.R2GC_133_23,(1,0,1):C.R2GC_133_24,(11,3,0):C.R2GC_134_25,(11,3,1):C.R2GC_134_26,(10,3,0):C.R2GC_134_25,(10,3,1):C.R2GC_134_26,(9,3,1):C.R2GC_111_2,(0,1,0):C.R2GC_138_31,(0,1,1):C.R2GC_138_32,(2,1,0):C.R2GC_138_31,(2,1,1):C.R2GC_138_32,(5,1,0):C.R2GC_133_23,(5,1,1):C.R2GC_133_24,(1,1,0):C.R2GC_133_23,(1,1,1):C.R2GC_133_24,(7,1,0):C.R2GC_139_33,(7,1,1):C.R2GC_140_35,(4,1,0):C.R2GC_133_23,(4,1,1):C.R2GC_133_24,(3,1,0):C.R2GC_133_23,(3,1,1):C.R2GC_133_24,(8,1,0):C.R2GC_135_27,(8,1,1):C.R2GC_136_29,(6,1,0):C.R2GC_143_39,(6,1,1):C.R2GC_143_40,(0,2,0):C.R2GC_138_31,(0,2,1):C.R2GC_138_32,(2,2,0):C.R2GC_138_31,(2,2,1):C.R2GC_138_32,(5,2,0):C.R2GC_133_23,(5,2,1):C.R2GC_133_24,(1,2,0):C.R2GC_133_23,(1,2,1):C.R2GC_133_24,(7,2,0):C.R2GC_144_41,(7,2,1):C.R2GC_138_32,(4,2,0):C.R2GC_133_23,(4,2,1):C.R2GC_133_24,(3,2,0):C.R2GC_133_23,(3,2,1):C.R2GC_133_24,(8,2,0):C.R2GC_135_27,(8,2,1):C.R2GC_137_30,(6,2,0):C.R2GC_141_36,(6,2,1):C.R2GC_142_38})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_346_1012,(0,0,2):C.R2GC_346_1013,(0,0,3):C.R2GC_346_1014,(0,0,4):C.R2GC_346_1015,(0,0,5):C.R2GC_346_1016,(0,0,7):C.R2GC_346_1017,(0,0,10):C.R2GC_346_1018,(0,0,13):C.R2GC_346_1019,(0,0,14):C.R2GC_346_1020,(0,0,15):C.R2GC_346_1021,(0,0,0):C.R2GC_346_1022,(0,0,6):C.R2GC_346_1023,(0,0,8):C.R2GC_346_1024,(0,0,9):C.R2GC_346_1025,(0,0,11):C.R2GC_346_1026,(0,0,12):C.R2GC_346_1027})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_336_916,(0,0,2):C.R2GC_336_917,(0,0,3):C.R2GC_336_918,(0,0,4):C.R2GC_336_919,(0,0,5):C.R2GC_336_920,(0,0,10):C.R2GC_336_921,(0,0,12):C.R2GC_336_922,(0,0,13):C.R2GC_336_923,(0,0,14):C.R2GC_336_924,(0,0,15):C.R2GC_336_925,(0,0,0):C.R2GC_336_926,(0,0,6):C.R2GC_336_927,(0,0,7):C.R2GC_336_928,(0,0,8):C.R2GC_336_929,(0,0,9):C.R2GC_336_930,(0,0,11):C.R2GC_336_931})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_340_966,(0,0,2):C.R2GC_340_967,(0,0,3):C.R2GC_340_968,(0,0,4):C.R2GC_340_969,(0,0,6):C.R2GC_340_970,(0,0,7):C.R2GC_340_971,(0,0,0):C.R2GC_340_972,(0,0,5):C.R2GC_340_973})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_344_990,(0,0,2):C.R2GC_344_991,(0,0,3):C.R2GC_344_992,(0,0,4):C.R2GC_344_993,(0,0,10):C.R2GC_344_994,(0,0,11):C.R2GC_344_995,(0,0,0):C.R2GC_344_996,(0,0,5):C.R2GC_344_997,(0,0,6):C.R2GC_344_998,(0,0,7):C.R2GC_344_999,(0,0,8):C.R2GC_344_1000,(0,0,9):C.R2GC_344_1001})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_334_894,(0,0,2):C.R2GC_334_895,(0,0,3):C.R2GC_334_896,(0,0,4):C.R2GC_334_897,(0,0,10):C.R2GC_334_898,(0,0,11):C.R2GC_334_899,(0,0,0):C.R2GC_334_900,(0,0,5):C.R2GC_334_901,(0,0,6):C.R2GC_334_902,(0,0,7):C.R2GC_334_903,(0,0,8):C.R2GC_334_904,(0,0,9):C.R2GC_334_905})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_270_434,(0,0,1):C.R2GC_270_435,(0,0,2):C.R2GC_270_436,(0,0,3):C.R2GC_270_437,(0,1,0):C.R2GC_271_438,(0,1,1):C.R2GC_232_250,(0,1,2):C.R2GC_183_171,(0,1,3):C.R2GC_271_439,(0,2,0):C.R2GC_271_438,(0,2,1):C.R2GC_232_250,(0,2,2):C.R2GC_183_171,(0,2,3):C.R2GC_271_439,(0,3,0):C.R2GC_270_434,(0,3,1):C.R2GC_270_435,(0,3,2):C.R2GC_270_436,(0,3,3):C.R2GC_270_437,(0,4,0):C.R2GC_270_434,(0,4,1):C.R2GC_270_435,(0,4,2):C.R2GC_270_436,(0,4,3):C.R2GC_270_437,(0,5,0):C.R2GC_271_438,(0,5,1):C.R2GC_232_250,(0,5,2):C.R2GC_183_171,(0,5,3):C.R2GC_271_439})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_346_1012,(0,0,2):C.R2GC_346_1013,(0,0,3):C.R2GC_346_1014,(0,0,4):C.R2GC_346_1015,(0,0,5):C.R2GC_346_1016,(0,0,7):C.R2GC_346_1017,(0,0,10):C.R2GC_346_1018,(0,0,13):C.R2GC_346_1019,(0,0,14):C.R2GC_346_1020,(0,0,15):C.R2GC_346_1021,(0,0,0):C.R2GC_346_1022,(0,0,6):C.R2GC_346_1023,(0,0,8):C.R2GC_346_1024,(0,0,9):C.R2GC_346_1025,(0,0,11):C.R2GC_346_1026,(0,0,12):C.R2GC_346_1027})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_336_925,(0,0,2):C.R2GC_337_932,(0,0,3):C.R2GC_337_933,(0,0,4):C.R2GC_337_934,(0,0,5):C.R2GC_337_935,(0,0,10):C.R2GC_336_922,(0,0,12):C.R2GC_336_921,(0,0,13):C.R2GC_337_936,(0,0,14):C.R2GC_337_937,(0,0,15):C.R2GC_336_916,(0,0,0):C.R2GC_337_938,(0,0,6):C.R2GC_336_930,(0,0,7):C.R2GC_337_939,(0,0,8):C.R2GC_337_940,(0,0,9):C.R2GC_336_927,(0,0,11):C.R2GC_337_941})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_340_971,(0,0,2):C.R2GC_341_974,(0,0,3):C.R2GC_341_975,(0,0,4):C.R2GC_341_976,(0,0,6):C.R2GC_341_977,(0,0,7):C.R2GC_340_966,(0,0,0):C.R2GC_341_978,(0,0,5):C.R2GC_341_979})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_345_1002,(0,0,2):C.R2GC_345_1003,(0,0,3):C.R2GC_345_1004,(0,0,4):C.R2GC_345_1005,(0,0,10):C.R2GC_345_1006,(0,0,11):C.R2GC_345_1007,(0,0,0):C.R2GC_345_1008,(0,0,5):C.R2GC_344_998,(0,0,6):C.R2GC_344_997,(0,0,7):C.R2GC_345_1009,(0,0,8):C.R2GC_345_1010,(0,0,9):C.R2GC_345_1011,(0,1,1):C.R2GC_344_990,(0,1,2):C.R2GC_344_991,(0,1,3):C.R2GC_344_992,(0,1,4):C.R2GC_344_993,(0,1,10):C.R2GC_344_994,(0,1,11):C.R2GC_344_995,(0,1,0):C.R2GC_344_996,(0,1,5):C.R2GC_344_997,(0,1,6):C.R2GC_344_998,(0,1,7):C.R2GC_344_999,(0,1,8):C.R2GC_344_1000,(0,1,9):C.R2GC_344_1001})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_334_894,(0,0,2):C.R2GC_334_895,(0,0,3):C.R2GC_334_896,(0,0,4):C.R2GC_334_897,(0,0,10):C.R2GC_334_898,(0,0,11):C.R2GC_334_899,(0,0,0):C.R2GC_334_900,(0,0,5):C.R2GC_334_901,(0,0,6):C.R2GC_334_902,(0,0,7):C.R2GC_334_903,(0,0,8):C.R2GC_334_904,(0,0,9):C.R2GC_334_905,(0,1,1):C.R2GC_335_906,(0,1,2):C.R2GC_335_907,(0,1,3):C.R2GC_335_908,(0,1,4):C.R2GC_335_909,(0,1,10):C.R2GC_335_910,(0,1,11):C.R2GC_335_911,(0,1,0):C.R2GC_335_912,(0,1,5):C.R2GC_334_904,(0,1,6):C.R2GC_335_913,(0,1,7):C.R2GC_335_914,(0,1,8):C.R2GC_334_901,(0,1,9):C.R2GC_335_915})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_333_877,(0,0,16):C.R2GC_333_878,(0,0,1):C.R2GC_333_879,(0,0,2):C.R2GC_333_880,(0,0,3):C.R2GC_333_881,(0,0,4):C.R2GC_333_882,(0,0,5):C.R2GC_333_883,(0,0,8):C.R2GC_333_885,(0,0,11):C.R2GC_333_884,(0,0,12):C.R2GC_333_886,(0,0,13):C.R2GC_333_887,(0,0,15):C.R2GC_333_888,(0,0,0):C.R2GC_333_889,(0,0,6):C.R2GC_333_890,(0,0,7):C.R2GC_333_891,(0,0,9):C.R2GC_333_893,(0,0,10):C.R2GC_333_892})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.G0, P.G__plus__], [P.a, P.G__plus__, P.H] ], [ [P.a, P.G0, P.W__plus__], [P.a, P.H, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.G__plus__, P.W__plus__, P.Z] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z], [P.G__plus__, P.H, P.Z] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z], [P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_349_1044,(0,0,22):C.R2GC_333_877,(0,0,24):C.R2GC_349_1045,(0,0,3):C.R2GC_349_1046,(0,0,7):C.R2GC_349_1047,(0,0,9):C.R2GC_349_1048,(0,0,10):C.R2GC_333_880,(0,0,11):C.R2GC_333_881,(0,0,12):C.R2GC_333_882,(0,0,13):C.R2GC_333_883,(0,0,16):C.R2GC_349_1049,(0,0,19):C.R2GC_349_1050,(0,0,20):C.R2GC_333_886,(0,0,21):C.R2GC_333_887,(0,0,23):C.R2GC_349_1051,(0,0,1):C.R2GC_349_1052,(0,0,2):C.R2GC_349_1053,(0,0,4):C.R2GC_349_1054,(0,0,6):C.R2GC_349_1055,(0,0,8):C.R2GC_349_1056,(0,0,14):C.R2GC_333_890,(0,0,15):C.R2GC_349_1057,(0,0,17):C.R2GC_349_1058,(0,0,18):C.R2GC_349_1059,(0,0,5):C.R2GC_349_1060})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_333_877,(0,0,16):C.R2GC_333_878,(0,0,1):C.R2GC_333_879,(0,0,2):C.R2GC_333_880,(0,0,3):C.R2GC_333_881,(0,0,4):C.R2GC_333_882,(0,0,5):C.R2GC_333_883,(0,0,9):C.R2GC_333_884,(0,0,10):C.R2GC_333_885,(0,0,12):C.R2GC_333_886,(0,0,13):C.R2GC_333_887,(0,0,15):C.R2GC_333_888,(0,0,0):C.R2GC_333_889,(0,0,6):C.R2GC_333_890,(0,0,7):C.R2GC_333_891,(0,0,8):C.R2GC_333_892,(0,0,11):C.R2GC_333_893})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,9):C.R2GC_339_955,(0,0,11):C.R2GC_339_956,(0,0,1):C.R2GC_339_957,(0,0,2):C.R2GC_339_958,(0,0,3):C.R2GC_339_959,(0,0,4):C.R2GC_339_960,(0,0,5):C.R2GC_339_961,(0,0,7):C.R2GC_339_962,(0,0,8):C.R2GC_339_963,(0,0,10):C.R2GC_339_964,(0,0,0):C.R2GC_339_965,(0,0,6):C.R2GC_338_951})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_272_440,(0,0,0):C.R2GC_272_441,(0,0,1):C.R2GC_272_442,(0,0,2):C.R2GC_272_443,(0,0,4):C.R2GC_263_407,(0,1,3):C.R2GC_272_440,(0,1,0):C.R2GC_272_441,(0,1,1):C.R2GC_272_442,(0,1,2):C.R2GC_272_443,(0,1,4):C.R2GC_263_407,(0,2,3):C.R2GC_273_444,(0,2,0):C.R2GC_273_445,(0,2,1):C.R2GC_273_446,(0,2,2):C.R2GC_273_447,(0,2,4):C.R2GC_264_412})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_265_416,(0,0,1):C.R2GC_265_417,(0,0,2):C.R2GC_265_418,(0,0,3):C.R2GC_265_419,(0,1,0):C.R2GC_266_420,(0,1,1):C.R2GC_266_421,(0,1,2):C.R2GC_266_422,(0,1,3):C.R2GC_266_423,(0,2,0):C.R2GC_266_420,(0,2,1):C.R2GC_266_421,(0,2,2):C.R2GC_266_422,(0,2,3):C.R2GC_266_423,(0,3,0):C.R2GC_265_416,(0,3,1):C.R2GC_265_417,(0,3,2):C.R2GC_265_418,(0,3,3):C.R2GC_265_419,(0,4,0):C.R2GC_265_416,(0,4,1):C.R2GC_265_417,(0,4,2):C.R2GC_265_418,(0,4,3):C.R2GC_265_419,(0,5,0):C.R2GC_266_420,(0,5,1):C.R2GC_266_421,(0,5,2):C.R2GC_266_422,(0,5,3):C.R2GC_266_423})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_277_485,(0,0,6):C.R2GC_277_486,(0,0,8):C.R2GC_277_487,(0,0,1):C.R2GC_277_488,(0,0,3):C.R2GC_277_489,(0,0,4):C.R2GC_277_490,(0,0,5):C.R2GC_277_491,(0,0,7):C.R2GC_277_492,(0,0,2):C.R2GC_277_493,(0,1,0):C.R2GC_277_485,(0,1,6):C.R2GC_277_486,(0,1,8):C.R2GC_277_487,(0,1,1):C.R2GC_277_488,(0,1,3):C.R2GC_277_489,(0,1,4):C.R2GC_277_490,(0,1,5):C.R2GC_277_491,(0,1,7):C.R2GC_277_492,(0,1,2):C.R2GC_277_493,(0,2,6):C.R2GC_278_494,(0,2,1):C.R2GC_278_495,(0,2,4):C.R2GC_278_496,(0,2,5):C.R2GC_278_497,(0,2,7):C.R2GC_278_498,(0,2,2):C.R2GC_278_499})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_303_673,(0,0,1):C.R2GC_303_674,(0,0,2):C.R2GC_303_675,(0,0,6):C.R2GC_303_676,(0,0,3):C.R2GC_303_677,(0,0,4):C.R2GC_303_678,(0,0,5):C.R2GC_303_679,(0,0,7):C.R2GC_303_680,(0,0,9):C.R2GC_303_681,(0,1,0):C.R2GC_306_700,(0,1,1):C.R2GC_306_701,(0,1,2):C.R2GC_306_702,(0,1,6):C.R2GC_306_703,(0,1,3):C.R2GC_306_704,(0,1,5):C.R2GC_306_705,(0,1,7):C.R2GC_306_706,(0,1,8):C.R2GC_306_707,(0,1,9):C.R2GC_306_708})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_285_544,(0,0,1):C.R2GC_285_545,(0,0,2):C.R2GC_285_546,(0,0,6):C.R2GC_285_547,(0,0,3):C.R2GC_285_548,(0,0,5):C.R2GC_285_549,(0,0,7):C.R2GC_285_550,(0,0,8):C.R2GC_285_551,(0,0,9):C.R2GC_285_552,(0,1,0):C.R2GC_283_526,(0,1,1):C.R2GC_283_527,(0,1,2):C.R2GC_283_528,(0,1,6):C.R2GC_283_529,(0,1,3):C.R2GC_283_530,(0,1,4):C.R2GC_283_531,(0,1,5):C.R2GC_283_532,(0,1,7):C.R2GC_283_533,(0,1,9):C.R2GC_283_534})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_293_603,(0,0,1):C.R2GC_293_604,(0,0,2):C.R2GC_293_605,(0,0,6):C.R2GC_293_606,(0,0,3):C.R2GC_293_607,(0,0,4):C.R2GC_293_608,(0,0,5):C.R2GC_293_609,(0,0,7):C.R2GC_293_610,(0,0,9):C.R2GC_293_611,(0,1,0):C.R2GC_296_630,(0,1,1):C.R2GC_296_631,(0,1,2):C.R2GC_296_632,(0,1,6):C.R2GC_296_633,(0,1,3):C.R2GC_296_634,(0,1,5):C.R2GC_296_635,(0,1,7):C.R2GC_296_636,(0,1,8):C.R2GC_296_637,(0,1,9):C.R2GC_296_638})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_300_649,(0,0,1):C.R2GC_300_650,(0,0,2):C.R2GC_300_651,(0,0,3):C.R2GC_300_652,(0,0,5):C.R2GC_300_653,(0,0,6):C.R2GC_300_654,(0,0,4):C.R2GC_300_655,(0,0,7):C.R2GC_300_656})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_287_562,(0,0,1):C.R2GC_287_563,(0,0,4):C.R2GC_287_564,(0,0,3):C.R2GC_287_565,(0,0,5):C.R2GC_287_566,(0,0,7):C.R2GC_287_567,(0,0,2):C.R2GC_287_568,(0,0,6):C.R2GC_287_569})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_290_579,(0,0,1):C.R2GC_290_580,(0,0,2):C.R2GC_290_581,(0,0,3):C.R2GC_290_582,(0,0,5):C.R2GC_290_583,(0,0,6):C.R2GC_290_584,(0,0,4):C.R2GC_290_585,(0,0,7):C.R2GC_290_586})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_301_657,(0,0,1):C.R2GC_301_658,(0,0,2):C.R2GC_301_659,(0,0,4):C.R2GC_301_660,(0,0,5):C.R2GC_301_661,(0,0,6):C.R2GC_301_662,(0,0,3):C.R2GC_301_663,(0,0,7):C.R2GC_301_664})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_282_518,(0,0,1):C.R2GC_282_519,(0,0,5):C.R2GC_282_520,(0,0,3):C.R2GC_282_521,(0,0,6):C.R2GC_282_522,(0,0,7):C.R2GC_282_523,(0,0,2):C.R2GC_282_524,(0,0,4):C.R2GC_282_525})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_291_587,(0,0,1):C.R2GC_291_588,(0,0,2):C.R2GC_291_589,(0,0,4):C.R2GC_291_590,(0,0,5):C.R2GC_291_591,(0,0,6):C.R2GC_291_592,(0,0,3):C.R2GC_291_593,(0,0,7):C.R2GC_291_594})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_305_691,(0,0,1):C.R2GC_305_692,(0,0,2):C.R2GC_305_693,(0,0,6):C.R2GC_305_694,(0,0,3):C.R2GC_305_695,(0,0,5):C.R2GC_305_696,(0,0,7):C.R2GC_305_697,(0,0,8):C.R2GC_305_698,(0,0,9):C.R2GC_305_699,(0,1,0):C.R2GC_304_682,(0,1,1):C.R2GC_304_683,(0,1,2):C.R2GC_304_684,(0,1,6):C.R2GC_304_685,(0,1,3):C.R2GC_304_686,(0,1,4):C.R2GC_304_687,(0,1,5):C.R2GC_304_688,(0,1,7):C.R2GC_304_689,(0,1,9):C.R2GC_304_690})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_284_535,(0,0,1):C.R2GC_284_536,(0,0,2):C.R2GC_284_537,(0,0,6):C.R2GC_284_538,(0,0,3):C.R2GC_284_539,(0,0,4):C.R2GC_284_540,(0,0,5):C.R2GC_284_541,(0,0,7):C.R2GC_284_542,(0,0,9):C.R2GC_284_543,(0,1,0):C.R2GC_286_553,(0,1,1):C.R2GC_286_554,(0,1,2):C.R2GC_286_555,(0,1,6):C.R2GC_286_556,(0,1,3):C.R2GC_286_557,(0,1,5):C.R2GC_286_558,(0,1,7):C.R2GC_286_559,(0,1,8):C.R2GC_286_560,(0,1,9):C.R2GC_286_561})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_295_621,(0,0,1):C.R2GC_295_622,(0,0,2):C.R2GC_295_623,(0,0,6):C.R2GC_295_624,(0,0,3):C.R2GC_295_625,(0,0,5):C.R2GC_295_626,(0,0,7):C.R2GC_295_627,(0,0,8):C.R2GC_295_628,(0,0,9):C.R2GC_295_629,(0,1,0):C.R2GC_294_612,(0,1,1):C.R2GC_294_613,(0,1,2):C.R2GC_294_614,(0,1,6):C.R2GC_294_615,(0,1,3):C.R2GC_294_616,(0,1,4):C.R2GC_294_617,(0,1,5):C.R2GC_294_618,(0,1,7):C.R2GC_294_619,(0,1,9):C.R2GC_294_620})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_312_734,(0,0,1):C.R2GC_312_735,(0,0,2):C.R2GC_312_736,(0,0,3):C.R2GC_312_737,(0,0,4):C.R2GC_312_738})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_317_760,(0,0,1):C.R2GC_317_761,(0,0,2):C.R2GC_317_762,(0,0,3):C.R2GC_317_763,(0,0,4):C.R2GC_317_764})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_322_782,(0,0,1):C.R2GC_322_783,(0,0,2):C.R2GC_322_784,(0,0,3):C.R2GC_322_785,(0,0,4):C.R2GC_322_786})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_309_717,(0,0,1):C.R2GC_309_718,(0,0,2):C.R2GC_309_719,(0,0,4):C.R2GC_309_720,(0,0,3):C.R2GC_309_721,(0,0,5):C.R2GC_309_722})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_314_743,(0,0,1):C.R2GC_314_744,(0,0,3):C.R2GC_314_745,(0,0,5):C.R2GC_314_746,(0,0,2):C.R2GC_314_747,(0,0,4):C.R2GC_314_748})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_319_765,(0,0,1):C.R2GC_319_766,(0,0,3):C.R2GC_319_767,(0,0,5):C.R2GC_319_768,(0,0,2):C.R2GC_319_769,(0,0,4):C.R2GC_319_770})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_310_723,(0,0,1):C.R2GC_310_724,(0,0,3):C.R2GC_310_725,(0,0,4):C.R2GC_310_726,(0,0,2):C.R2GC_310_727,(0,0,5):C.R2GC_310_728})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_315_749,(0,0,1):C.R2GC_315_750,(0,0,4):C.R2GC_315_751,(0,0,5):C.R2GC_315_752,(0,0,2):C.R2GC_315_753,(0,0,3):C.R2GC_315_754})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_320_771,(0,0,1):C.R2GC_320_772,(0,0,4):C.R2GC_320_773,(0,0,5):C.R2GC_320_774,(0,0,2):C.R2GC_320_775,(0,0,3):C.R2GC_320_776})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_311_729,(0,0,1):C.R2GC_311_730,(0,0,2):C.R2GC_311_731,(0,0,3):C.R2GC_311_732,(0,0,4):C.R2GC_311_733})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_316_755,(0,0,1):C.R2GC_316_756,(0,0,2):C.R2GC_316_757,(0,0,3):C.R2GC_316_758,(0,0,4):C.R2GC_316_759})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_321_777,(0,0,1):C.R2GC_321_778,(0,0,2):C.R2GC_321_779,(0,0,3):C.R2GC_321_780,(0,0,4):C.R2GC_321_781})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_307_709,(0,0,1):C.R2GC_307_710,(0,0,4):C.R2GC_307_711,(0,0,3):C.R2GC_307_712,(0,0,5):C.R2GC_307_713,(0,0,7):C.R2GC_307_714,(0,0,2):C.R2GC_307_715,(0,0,6):C.R2GC_307_716})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_281_510,(0,0,1):C.R2GC_281_511,(0,0,2):C.R2GC_281_512,(0,0,3):C.R2GC_281_513,(0,0,5):C.R2GC_281_514,(0,0,6):C.R2GC_281_515,(0,0,4):C.R2GC_281_516,(0,0,7):C.R2GC_281_517})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_297_639,(0,0,1):C.R2GC_297_640,(0,0,4):C.R2GC_297_641,(0,0,3):C.R2GC_297_642,(0,0,5):C.R2GC_297_643,(0,0,7):C.R2GC_297_644,(0,0,2):C.R2GC_297_645,(0,0,6):C.R2GC_297_646})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_302_665,(0,0,1):C.R2GC_302_666,(0,0,5):C.R2GC_302_667,(0,0,3):C.R2GC_302_668,(0,0,6):C.R2GC_302_669,(0,0,7):C.R2GC_302_670,(0,0,2):C.R2GC_302_671,(0,0,4):C.R2GC_302_672})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_280_502,(0,0,1):C.R2GC_280_503,(0,0,2):C.R2GC_280_504,(0,0,4):C.R2GC_280_505,(0,0,5):C.R2GC_280_506,(0,0,6):C.R2GC_280_507,(0,0,3):C.R2GC_280_508,(0,0,7):C.R2GC_280_509})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_292_595,(0,0,1):C.R2GC_292_596,(0,0,5):C.R2GC_292_597,(0,0,3):C.R2GC_292_598,(0,0,6):C.R2GC_292_599,(0,0,7):C.R2GC_292_600,(0,0,2):C.R2GC_292_601,(0,0,4):C.R2GC_292_602})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,9):C.R2GC_248_285,(0,0,0):C.R2GC_259_394,(0,0,1):C.R2GC_259_395,(0,0,2):C.R2GC_259_396,(0,0,3):C.R2GC_259_397,(0,0,4):C.R2GC_259_398,(0,0,5):C.R2GC_259_399,(0,0,6):C.R2GC_259_400,(0,0,7):C.R2GC_259_401,(0,0,8):C.R2GC_259_402})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.Z, P.G0, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_328_828,(0,0,1):C.R2GC_328_829,(0,0,2):C.R2GC_328_830,(0,0,3):C.R2GC_328_831,(0,0,6):C.R2GC_328_832,(0,0,7):C.R2GC_328_833,(0,0,8):C.R2GC_328_834,(0,0,9):C.R2GC_328_835,(0,0,10):C.R2GC_328_836,(0,0,5):C.R2GC_328_837,(0,0,4):C.R2GC_328_838,(0,1,0):C.R2GC_327_817,(0,1,1):C.R2GC_327_818,(0,1,2):C.R2GC_327_819,(0,1,3):C.R2GC_327_820,(0,1,6):C.R2GC_327_821,(0,1,7):C.R2GC_327_822,(0,1,8):C.R2GC_327_823,(0,1,9):C.R2GC_327_824,(0,1,10):C.R2GC_327_825,(0,1,5):C.R2GC_327_826,(0,1,4):C.R2GC_327_827})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_325_797,(0,0,1):C.R2GC_325_798,(0,0,2):C.R2GC_325_799,(0,0,3):C.R2GC_325_800,(0,0,4):C.R2GC_325_801,(0,0,6):C.R2GC_325_802,(0,0,7):C.R2GC_325_803,(0,0,8):C.R2GC_325_804,(0,0,9):C.R2GC_325_805,(0,0,5):C.R2GC_325_806,(0,1,0):C.R2GC_326_807,(0,1,1):C.R2GC_326_808,(0,1,2):C.R2GC_326_809,(0,1,3):C.R2GC_326_810,(0,1,4):C.R2GC_326_811,(0,1,6):C.R2GC_326_812,(0,1,7):C.R2GC_326_813,(0,1,8):C.R2GC_326_814,(0,1,9):C.R2GC_326_815,(0,1,5):C.R2GC_326_816})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_351_1079,(0,0,2):C.R2GC_351_1080,(0,0,3):C.R2GC_351_1081,(0,0,4):C.R2GC_351_1082,(0,0,5):C.R2GC_351_1083,(0,0,8):C.R2GC_351_1084,(0,0,12):C.R2GC_351_1085,(0,0,15):C.R2GC_351_1086,(0,0,16):C.R2GC_351_1087,(0,0,17):C.R2GC_351_1088,(0,0,0):C.R2GC_351_1089,(0,0,7):C.R2GC_351_1090,(0,0,9):C.R2GC_351_1091,(0,0,10):C.R2GC_351_1092,(0,0,11):C.R2GC_351_1093,(0,0,13):C.R2GC_351_1094,(0,0,14):C.R2GC_351_1095,(0,0,6):C.R2GC_351_1096})

V_66 = CTVertex(name = 'V_66',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_350_1070,(0,0,2):C.R2GC_352_1097,(0,0,3):C.R2GC_352_1098,(0,0,4):C.R2GC_352_1099,(0,0,5):C.R2GC_352_1100,(0,0,11):C.R2GC_350_1067,(0,0,13):C.R2GC_350_1066,(0,0,15):C.R2GC_352_1101,(0,0,16):C.R2GC_352_1102,(0,0,17):C.R2GC_350_1061,(0,0,0):C.R2GC_352_1103,(0,0,7):C.R2GC_350_1075,(0,0,8):C.R2GC_352_1104,(0,0,9):C.R2GC_352_1105,(0,0,10):C.R2GC_350_1072,(0,0,12):C.R2GC_352_1106,(0,0,14):C.R2GC_352_1107,(0,0,6):C.R2GC_352_1108})

V_67 = CTVertex(name = 'V_67',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_347_1028,(0,0,2):C.R2GC_347_1029,(0,0,3):C.R2GC_347_1030,(0,0,4):C.R2GC_347_1031,(0,0,6):C.R2GC_347_1032,(0,0,8):C.R2GC_347_1033,(0,0,0):C.R2GC_347_1034,(0,0,5):C.R2GC_347_1035,(0,0,7):C.R2GC_347_1036})

V_68 = CTVertex(name = 'V_68',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_351_1079,(0,0,2):C.R2GC_351_1080,(0,0,3):C.R2GC_351_1081,(0,0,4):C.R2GC_351_1082,(0,0,5):C.R2GC_351_1083,(0,0,8):C.R2GC_351_1084,(0,0,12):C.R2GC_351_1085,(0,0,15):C.R2GC_351_1086,(0,0,16):C.R2GC_351_1087,(0,0,17):C.R2GC_351_1088,(0,0,0):C.R2GC_351_1089,(0,0,7):C.R2GC_351_1090,(0,0,9):C.R2GC_351_1091,(0,0,10):C.R2GC_351_1092,(0,0,11):C.R2GC_351_1093,(0,0,13):C.R2GC_351_1094,(0,0,14):C.R2GC_351_1095,(0,0,6):C.R2GC_351_1096})

V_69 = CTVertex(name = 'V_69',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_350_1061,(0,0,2):C.R2GC_350_1062,(0,0,3):C.R2GC_350_1063,(0,0,4):C.R2GC_350_1064,(0,0,5):C.R2GC_350_1065,(0,0,11):C.R2GC_350_1066,(0,0,13):C.R2GC_350_1067,(0,0,15):C.R2GC_350_1068,(0,0,16):C.R2GC_350_1069,(0,0,17):C.R2GC_350_1070,(0,0,0):C.R2GC_350_1071,(0,0,7):C.R2GC_350_1072,(0,0,8):C.R2GC_350_1073,(0,0,9):C.R2GC_350_1074,(0,0,10):C.R2GC_350_1075,(0,0,12):C.R2GC_350_1076,(0,0,14):C.R2GC_350_1077,(0,0,6):C.R2GC_350_1078})

V_70 = CTVertex(name = 'V_70',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_347_1033,(0,0,2):C.R2GC_348_1037,(0,0,3):C.R2GC_348_1038,(0,0,4):C.R2GC_348_1039,(0,0,6):C.R2GC_348_1040,(0,0,8):C.R2GC_347_1028,(0,0,0):C.R2GC_348_1041,(0,0,5):C.R2GC_348_1042,(0,0,7):C.R2GC_348_1043})

V_71 = CTVertex(name = 'V_71',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV1, L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,1,3):C.R2GC_268_429,(0,1,0):C.R2GC_268_430,(0,1,1):C.R2GC_268_431,(0,1,2):C.R2GC_268_432,(0,1,4):C.R2GC_268_433,(0,2,3):C.R2GC_267_424,(0,2,0):C.R2GC_267_425,(0,2,1):C.R2GC_267_426,(0,2,2):C.R2GC_267_427,(0,2,4):C.R2GC_267_428,(0,3,3):C.R2GC_267_424,(0,3,0):C.R2GC_267_425,(0,3,1):C.R2GC_267_426,(0,3,2):C.R2GC_267_427,(0,3,4):C.R2GC_267_428,(0,0,1):C.R2GC_242_262,(0,0,2):C.R2GC_242_263})

V_72 = CTVertex(name = 'V_72',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_329_839,(0,0,1):C.R2GC_329_840,(0,0,2):C.R2GC_329_841,(0,0,3):C.R2GC_329_842,(0,0,7):C.R2GC_329_843,(0,0,8):C.R2GC_329_844,(0,0,9):C.R2GC_329_845,(0,0,10):C.R2GC_329_846,(0,0,11):C.R2GC_329_847,(0,0,12):C.R2GC_324_787,(0,0,5):C.R2GC_329_849,(0,0,6):C.R2GC_329_848,(0,0,4):C.R2GC_156_92})

V_73 = CTVertex(name = 'V_73',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,10):C.R2GC_324_787,(0,0,0):C.R2GC_258_391,(0,0,1):C.R2GC_324_788,(0,0,2):C.R2GC_324_789,(0,0,3):C.R2GC_324_790,(0,0,4):C.R2GC_324_791,(0,0,6):C.R2GC_324_792,(0,0,7):C.R2GC_324_793,(0,0,8):C.R2GC_324_794,(0,0,9):C.R2GC_324_795,(0,0,5):C.R2GC_324_796})

V_74 = CTVertex(name = 'V_74',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_329_839,(0,0,1):C.R2GC_329_840,(0,0,2):C.R2GC_329_841,(0,0,3):C.R2GC_329_842,(0,0,7):C.R2GC_329_843,(0,0,8):C.R2GC_329_844,(0,0,9):C.R2GC_329_845,(0,0,10):C.R2GC_329_846,(0,0,11):C.R2GC_329_847,(0,0,12):C.R2GC_324_787,(0,0,5):C.R2GC_329_848,(0,0,6):C.R2GC_329_849,(0,0,4):C.R2GC_156_92})

V_75 = CTVertex(name = 'V_75',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_249_287,(0,0,1):C.R2GC_249_288,(0,0,2):C.R2GC_249_289,(0,0,3):C.R2GC_249_290,(0,0,5):C.R2GC_249_291,(0,0,6):C.R2GC_249_292,(0,0,7):C.R2GC_249_293,(0,0,8):C.R2GC_249_294,(0,0,9):C.R2GC_249_295,(0,0,10):C.R2GC_249_296,(0,0,4):C.R2GC_249_297})

V_76 = CTVertex(name = 'V_76',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_263_406,(0,0,0):C.R2GC_263_407,(0,0,1):C.R2GC_263_408,(0,0,2):C.R2GC_263_409,(0,0,4):C.R2GC_263_410,(0,1,3):C.R2GC_263_406,(0,1,0):C.R2GC_263_407,(0,1,1):C.R2GC_263_408,(0,1,2):C.R2GC_263_409,(0,1,4):C.R2GC_263_410,(0,2,3):C.R2GC_264_411,(0,2,0):C.R2GC_264_412,(0,2,1):C.R2GC_264_413,(0,2,2):C.R2GC_264_414,(0,2,4):C.R2GC_264_415})

V_77 = CTVertex(name = 'V_77',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_170_135,(0,0,1):C.R2GC_170_136,(0,0,2):C.R2GC_232_249,(0,0,3):C.R2GC_232_250,(0,1,0):C.R2GC_170_135,(0,1,1):C.R2GC_170_136,(0,1,2):C.R2GC_170_137})

V_78 = CTVertex(name = 'V_78',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_170_135,(0,0,1):C.R2GC_172_140,(0,0,2):C.R2GC_232_249,(0,0,3):C.R2GC_232_250,(0,1,0):C.R2GC_170_135,(0,1,1):C.R2GC_172_140,(0,1,2):C.R2GC_170_137})

V_79 = CTVertex(name = 'V_79',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_170_135,(0,0,1):C.R2GC_208_216,(0,0,2):C.R2GC_232_249,(0,0,3):C.R2GC_232_250,(0,1,0):C.R2GC_170_135,(0,1,1):C.R2GC_208_216,(0,1,2):C.R2GC_170_137})

V_80 = CTVertex(name = 'V_80',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_215_229,(0,1,0):C.R2GC_174_143,(0,1,1):C.R2GC_223_235,(0,1,2):C.R2GC_178_158,(0,1,4):C.R2GC_174_144,(0,1,5):C.R2GC_178_156,(0,2,0):C.R2GC_174_143,(0,2,1):C.R2GC_224_236,(0,2,4):C.R2GC_174_144,(0,2,5):C.R2GC_174_145})

V_81 = CTVertex(name = 'V_81',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,2):C.R2GC_164_123,(0,1,0):C.R2GC_174_143,(0,1,1):C.R2GC_174_144,(0,1,3):C.R2GC_178_156,(0,1,4):C.R2GC_178_157,(0,1,5):C.R2GC_178_158,(0,2,0):C.R2GC_174_143,(0,2,1):C.R2GC_174_144,(0,2,3):C.R2GC_174_145,(0,2,4):C.R2GC_174_146})

V_82 = CTVertex(name = 'V_82',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_193_201,(0,1,0):C.R2GC_174_143,(0,1,1):C.R2GC_201_207,(0,1,2):C.R2GC_178_158,(0,1,4):C.R2GC_174_144,(0,1,5):C.R2GC_178_156,(0,2,0):C.R2GC_174_143,(0,2,1):C.R2GC_202_208,(0,2,4):C.R2GC_174_144,(0,2,5):C.R2GC_174_145})

V_83 = CTVertex(name = 'V_83',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_183_169,(0,0,1):C.R2GC_183_172,(0,0,2):C.R2GC_212_223,(0,0,3):C.R2GC_183_174,(0,0,4):C.R2GC_218_231,(0,0,5):C.R2GC_183_171,(0,1,0):C.R2GC_183_169,(0,1,1):C.R2GC_183_172,(0,1,2):C.R2GC_212_223,(0,1,3):C.R2GC_184_176,(0,1,4):C.R2GC_212_224})

V_84 = CTVertex(name = 'V_84',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_183_169,(0,0,1):C.R2GC_183_170,(0,0,2):C.R2GC_183_171,(0,0,4):C.R2GC_183_172,(0,0,3):C.R2GC_183_173,(0,0,5):C.R2GC_183_174,(0,1,0):C.R2GC_183_169,(0,1,1):C.R2GC_184_175,(0,1,4):C.R2GC_183_172,(0,1,3):C.R2GC_183_173,(0,1,5):C.R2GC_184_176})

V_85 = CTVertex(name = 'V_85',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_183_169,(0,0,1):C.R2GC_183_172,(0,0,2):C.R2GC_190_195,(0,0,3):C.R2GC_183_174,(0,0,4):C.R2GC_196_203,(0,0,5):C.R2GC_183_171,(0,1,0):C.R2GC_183_169,(0,1,1):C.R2GC_183_172,(0,1,2):C.R2GC_190_195,(0,1,3):C.R2GC_184_176,(0,1,4):C.R2GC_190_196})

V_86 = CTVertex(name = 'V_86',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_165_124,(0,0,4):C.R2GC_165_125,(0,0,3):C.R2GC_216_230,(0,1,1):C.R2GC_213_226,(0,1,2):C.R2GC_179_161,(0,1,5):C.R2GC_179_159,(0,2,1):C.R2GC_219_232,(0,2,5):C.R2GC_175_147})

V_87 = CTVertex(name = 'V_87',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_165_124,(0,0,1):C.R2GC_165_125,(0,0,2):C.R2GC_165_126,(0,1,3):C.R2GC_179_159,(0,1,4):C.R2GC_179_160,(0,1,5):C.R2GC_179_161,(0,2,3):C.R2GC_175_147,(0,2,4):C.R2GC_175_148})

V_88 = CTVertex(name = 'V_88',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_165_124,(0,0,4):C.R2GC_165_125,(0,0,3):C.R2GC_194_202,(0,1,1):C.R2GC_191_198,(0,1,2):C.R2GC_179_161,(0,1,5):C.R2GC_179_159,(0,2,1):C.R2GC_197_204,(0,2,5):C.R2GC_175_147})

V_89 = CTVertex(name = 'V_89',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_185_177,(0,0,1):C.R2GC_165_125,(0,0,2):C.R2GC_213_225,(0,0,3):C.R2GC_185_179,(0,0,4):C.R2GC_219_232,(0,0,5):C.R2GC_179_161,(0,1,0):C.R2GC_185_177,(0,1,1):C.R2GC_165_125,(0,1,2):C.R2GC_213_225,(0,1,3):C.R2GC_186_180,(0,1,4):C.R2GC_213_226})

V_90 = CTVertex(name = 'V_90',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_185_177,(0,0,1):C.R2GC_175_148,(0,0,2):C.R2GC_179_161,(0,0,4):C.R2GC_165_125,(0,0,3):C.R2GC_185_178,(0,0,5):C.R2GC_185_179,(0,1,0):C.R2GC_185_177,(0,1,1):C.R2GC_179_160,(0,1,4):C.R2GC_165_125,(0,1,3):C.R2GC_185_178,(0,1,5):C.R2GC_186_180})

V_91 = CTVertex(name = 'V_91',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_185_177,(0,0,1):C.R2GC_165_125,(0,0,2):C.R2GC_191_197,(0,0,3):C.R2GC_185_179,(0,0,4):C.R2GC_197_204,(0,0,5):C.R2GC_179_161,(0,1,0):C.R2GC_185_177,(0,1,1):C.R2GC_165_125,(0,1,2):C.R2GC_191_197,(0,1,3):C.R2GC_186_180,(0,1,4):C.R2GC_191_198})

V_92 = CTVertex(name = 'V_92',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_572,(0,0,2):C.R2GC_288_571,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_576,(0,0,8):C.R2GC_288_575,(0,1,3):C.R2GC_299_647,(0,1,5):C.R2GC_299_648})

V_93 = CTVertex(name = 'V_93',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_571,(0,0,2):C.R2GC_288_572,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_575,(0,0,8):C.R2GC_288_576,(0,1,3):C.R2GC_279_500,(0,1,5):C.R2GC_279_501})

V_94 = CTVertex(name = 'V_94',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_572,(0,0,2):C.R2GC_288_571,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_576,(0,0,8):C.R2GC_288_575,(0,1,3):C.R2GC_289_577,(0,1,5):C.R2GC_289_578})

V_95 = CTVertex(name = 'V_95',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_572,(0,0,2):C.R2GC_288_571,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_576,(0,0,8):C.R2GC_288_575,(0,1,3):C.R2GC_299_647,(0,1,5):C.R2GC_299_648})

V_96 = CTVertex(name = 'V_96',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_571,(0,0,2):C.R2GC_288_572,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_575,(0,0,8):C.R2GC_288_576,(0,1,3):C.R2GC_279_500,(0,1,5):C.R2GC_279_501})

V_97 = CTVertex(name = 'V_97',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_288_570,(0,0,1):C.R2GC_288_572,(0,0,2):C.R2GC_288_571,(0,0,4):C.R2GC_288_573,(0,0,6):C.R2GC_288_574,(0,0,7):C.R2GC_288_576,(0,0,8):C.R2GC_288_575,(0,1,3):C.R2GC_289_577,(0,1,5):C.R2GC_289_578})

V_98 = CTVertex(name = 'V_98',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_99 = CTVertex(name = 'V_99',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_100 = CTVertex(name = 'V_100',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_101 = CTVertex(name = 'V_101',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_102 = CTVertex(name = 'V_102',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_103 = CTVertex(name = 'V_103',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_313_739,(0,0,1):C.R2GC_313_740,(0,0,2):C.R2GC_313_741,(0,0,3):C.R2GC_313_742})

V_104 = CTVertex(name = 'V_104',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_180_162,(0,0,1):C.R2GC_228_240,(0,0,2):C.R2GC_180_167,(0,0,4):C.R2GC_180_163,(0,0,3):C.R2GC_228_241,(0,0,5):C.R2GC_180_165,(0,1,0):C.R2GC_176_149,(0,1,1):C.R2GC_229_242,(0,1,4):C.R2GC_176_150,(0,1,3):C.R2GC_229_243,(0,1,5):C.R2GC_176_152})

V_105 = CTVertex(name = 'V_105',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_180_162,(0,0,1):C.R2GC_180_163,(0,0,2):C.R2GC_180_164,(0,0,3):C.R2GC_180_165,(0,0,4):C.R2GC_180_166,(0,0,5):C.R2GC_180_167,(0,1,0):C.R2GC_176_149,(0,1,1):C.R2GC_176_150,(0,1,2):C.R2GC_176_151,(0,1,3):C.R2GC_176_152,(0,1,4):C.R2GC_176_153})

V_106 = CTVertex(name = 'V_106',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_180_162,(0,0,1):C.R2GC_206_212,(0,0,2):C.R2GC_180_167,(0,0,4):C.R2GC_180_163,(0,0,3):C.R2GC_206_213,(0,0,5):C.R2GC_180_165,(0,1,0):C.R2GC_176_149,(0,1,1):C.R2GC_207_214,(0,1,4):C.R2GC_176_150,(0,1,3):C.R2GC_207_215,(0,1,5):C.R2GC_176_152})

V_107 = CTVertex(name = 'V_107',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_188_184,(0,0,1):C.R2GC_188_187,(0,0,2):C.R2GC_220_233,(0,0,3):C.R2GC_188_189,(0,0,4):C.R2GC_220_234,(0,0,5):C.R2GC_188_186,(0,1,0):C.R2GC_189_190,(0,1,1):C.R2GC_189_192,(0,1,2):C.R2GC_214_227,(0,1,3):C.R2GC_189_194,(0,1,4):C.R2GC_214_228})

V_108 = CTVertex(name = 'V_108',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_188_184,(0,0,1):C.R2GC_188_185,(0,0,2):C.R2GC_188_186,(0,0,4):C.R2GC_188_187,(0,0,3):C.R2GC_188_188,(0,0,5):C.R2GC_188_189,(0,1,0):C.R2GC_189_190,(0,1,1):C.R2GC_189_191,(0,1,4):C.R2GC_189_192,(0,1,3):C.R2GC_189_193,(0,1,5):C.R2GC_189_194})

V_109 = CTVertex(name = 'V_109',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_188_184,(0,0,1):C.R2GC_188_187,(0,0,2):C.R2GC_198_205,(0,0,3):C.R2GC_188_189,(0,0,4):C.R2GC_198_206,(0,0,5):C.R2GC_188_186,(0,1,0):C.R2GC_189_190,(0,1,1):C.R2GC_189_192,(0,1,2):C.R2GC_192_199,(0,1,3):C.R2GC_189_194,(0,1,4):C.R2GC_192_200})

V_110 = CTVertex(name = 'V_110',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_356_1136,(0,0,1):C.R2GC_356_1137,(0,0,2):C.R2GC_356_1138})

V_111 = CTVertex(name = 'V_111',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_357_1139,(0,0,1):C.R2GC_356_1137,(0,0,2):C.R2GC_356_1138})

V_112 = CTVertex(name = 'V_112',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_358_1140,(0,0,1):C.R2GC_356_1137,(0,0,2):C.R2GC_356_1138})

V_113 = CTVertex(name = 'V_113',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_233_251,(0,0,1):C.R2GC_233_252,(0,0,2):C.R2GC_233_253,(0,0,4):C.R2GC_233_254,(0,1,0):C.R2GC_230_244,(0,1,1):C.R2GC_230_245,(0,1,2):C.R2GC_230_246,(0,1,3):C.R2GC_230_247})

V_114 = CTVertex(name = 'V_114',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_233_251,(0,0,1):C.R2GC_238_258,(0,0,3):C.R2GC_233_253,(0,0,4):C.R2GC_233_254,(0,1,0):C.R2GC_230_244,(0,1,1):C.R2GC_235_256,(0,1,2):C.R2GC_235_257,(0,1,3):C.R2GC_230_246})

V_115 = CTVertex(name = 'V_115',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_233_251,(0,0,1):C.R2GC_245_264,(0,0,3):C.R2GC_233_253,(0,0,4):C.R2GC_233_254,(0,1,0):C.R2GC_230_244,(0,1,1):C.R2GC_240_259,(0,1,2):C.R2GC_240_260,(0,1,3):C.R2GC_230_246})

V_116 = CTVertex(name = 'V_116',
                 type = 'R2',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S1 ],
                 loop_particles = [ [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_161_116,(0,0,1):C.R2GC_161_117})

V_117 = CTVertex(name = 'V_117',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_171_138,(0,1,1):C.R2GC_171_139,(0,3,0):C.R2GC_171_138,(0,3,1):C.R2GC_171_139,(0,2,1):C.R2GC_231_248,(0,2,2):C.R2GC_177_155,(0,4,1):C.R2GC_119_9,(0,0,0):C.R2GC_117_7})

V_118 = CTVertex(name = 'V_118',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF3 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_177_155,(0,0,1):C.R2GC_234_255})

V_119 = CTVertex(name = 'V_119',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_173_141,(0,1,1):C.R2GC_173_142,(0,3,0):C.R2GC_173_141,(0,3,1):C.R2GC_173_142,(0,2,1):C.R2GC_231_248,(0,2,2):C.R2GC_177_155,(0,4,1):C.R2GC_119_9,(0,0,0):C.R2GC_117_7})

V_120 = CTVertex(name = 'V_120',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF3 ],
                 loop_particles = [ [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_177_155,(0,0,1):C.R2GC_234_255})

V_121 = CTVertex(name = 'V_121',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_209_217,(0,1,1):C.R2GC_209_218,(0,3,0):C.R2GC_209_217,(0,3,1):C.R2GC_209_218,(0,2,1):C.R2GC_231_248,(0,2,2):C.R2GC_177_155,(0,4,1):C.R2GC_119_9,(0,0,0):C.R2GC_117_7})

V_122 = CTVertex(name = 'V_122',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF3 ],
                 loop_particles = [ [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_177_155,(0,0,1):C.R2GC_234_255})

V_123 = CTVertex(name = 'V_123',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.W__plus__] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_227_237,(0,0,2):C.R2GC_227_238,(0,0,3):C.R2GC_227_239,(0,2,0):C.R2GC_227_237,(0,2,2):C.R2GC_227_238,(0,2,3):C.R2GC_227_239,(0,1,0):C.R2GC_166_127,(0,1,1):C.R2GC_177_155,(0,1,2):C.R2GC_162_118,(0,1,3):C.R2GC_177_154,(0,3,0):C.R2GC_166_127,(0,3,2):C.R2GC_162_118,(0,3,3):C.R2GC_166_128})

V_124 = CTVertex(name = 'V_124',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.Z] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_169_132,(0,1,1):C.R2GC_169_133,(0,1,2):C.R2GC_169_134,(0,3,0):C.R2GC_169_132,(0,3,1):C.R2GC_169_133,(0,3,2):C.R2GC_169_134,(0,2,1):C.R2GC_162_118,(0,2,2):C.R2GC_181_168,(0,2,3):C.R2GC_177_155,(0,4,1):C.R2GC_162_118,(0,4,2):C.R2GC_162_119,(0,0,0):C.R2GC_115_6})

V_125 = CTVertex(name = 'V_125',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.Z] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_167_129,(0,0,1):C.R2GC_167_130,(0,0,2):C.R2GC_167_131,(0,2,0):C.R2GC_167_129,(0,2,1):C.R2GC_167_130,(0,2,2):C.R2GC_167_131,(0,1,0):C.R2GC_166_127,(0,1,1):C.R2GC_162_118,(0,1,2):C.R2GC_177_154,(0,1,3):C.R2GC_177_155,(0,3,0):C.R2GC_166_127,(0,3,1):C.R2GC_162_118,(0,3,2):C.R2GC_166_128})

V_126 = CTVertex(name = 'V_126',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.W__plus__] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,1,0):C.R2GC_187_181,(0,1,2):C.R2GC_187_182,(0,1,3):C.R2GC_187_183,(0,3,0):C.R2GC_187_181,(0,3,2):C.R2GC_187_182,(0,3,3):C.R2GC_187_183,(0,2,1):C.R2GC_177_155,(0,2,2):C.R2GC_162_118,(0,2,3):C.R2GC_181_168,(0,4,2):C.R2GC_162_118,(0,4,3):C.R2GC_162_119,(0,0,0):C.R2GC_115_6})

V_127 = CTVertex(name = 'V_127',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.W__plus__] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_205_209,(0,0,2):C.R2GC_205_210,(0,0,3):C.R2GC_205_211,(0,2,0):C.R2GC_205_209,(0,2,2):C.R2GC_205_210,(0,2,3):C.R2GC_205_211,(0,1,0):C.R2GC_166_127,(0,1,1):C.R2GC_177_155,(0,1,2):C.R2GC_162_118,(0,1,3):C.R2GC_177_154,(0,3,0):C.R2GC_166_127,(0,3,2):C.R2GC_162_118,(0,3,3):C.R2GC_166_128})

V_128 = CTVertex(name = 'V_128',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF2, L.FF3, L.FF4, L.FF5 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.Z] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_163_120,(0,1,1):C.R2GC_163_121,(0,1,2):C.R2GC_163_122,(0,3,0):C.R2GC_163_120,(0,3,1):C.R2GC_163_121,(0,3,2):C.R2GC_163_122,(0,2,1):C.R2GC_162_118,(0,2,2):C.R2GC_181_168,(0,2,3):C.R2GC_177_155,(0,4,1):C.R2GC_162_118,(0,4,2):C.R2GC_162_119,(0,0,0):C.R2GC_115_6})

V_129 = CTVertex(name = 'V_129',
                 type = 'R2',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_253_331,(0,0,1):C.R2GC_253_332,(0,0,2):C.R2GC_253_333,(0,0,3):C.R2GC_253_334,(0,0,6):C.R2GC_253_335,(0,0,7):C.R2GC_253_336,(0,0,8):C.R2GC_253_337,(0,0,9):C.R2GC_253_338,(0,0,10):C.R2GC_253_339,(0,0,11):C.R2GC_253_340,(0,0,12):C.R2GC_253_341,(0,0,4):C.R2GC_253_342,(0,0,5):C.R2GC_253_343,(0,1,0):C.R2GC_252_320,(0,1,1):C.R2GC_252_321,(0,1,2):C.R2GC_252_322,(0,1,3):C.R2GC_252_323,(0,1,6):C.R2GC_252_324,(0,1,7):C.R2GC_252_325,(0,1,8):C.R2GC_252_326,(0,1,9):C.R2GC_252_327,(0,1,10):C.R2GC_252_328,(0,1,4):C.R2GC_252_329,(0,1,5):C.R2GC_252_330})

V_130 = CTVertex(name = 'V_130',
                 type = 'R2',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_253_331,(0,0,1):C.R2GC_253_332,(0,0,2):C.R2GC_253_333,(0,0,3):C.R2GC_253_334,(0,0,6):C.R2GC_253_335,(0,0,7):C.R2GC_253_336,(0,0,8):C.R2GC_253_337,(0,0,9):C.R2GC_253_338,(0,0,10):C.R2GC_253_339,(0,0,11):C.R2GC_261_403,(0,0,12):C.R2GC_261_404,(0,0,4):C.R2GC_253_343,(0,0,5):C.R2GC_261_405,(0,1,0):C.R2GC_252_320,(0,1,1):C.R2GC_252_321,(0,1,2):C.R2GC_252_322,(0,1,3):C.R2GC_252_323,(0,1,6):C.R2GC_252_324,(0,1,7):C.R2GC_252_325,(0,1,8):C.R2GC_252_326,(0,1,9):C.R2GC_252_327,(0,1,10):C.R2GC_252_328,(0,1,4):C.R2GC_252_330,(0,1,5):C.R2GC_252_329})

V_131 = CTVertex(name = 'V_131',
                 type = 'R2',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,12):C.R2GC_261_403,(0,0,14):C.R2GC_275_458,(0,0,0):C.R2GC_275_459,(0,0,1):C.R2GC_275_460,(0,0,2):C.R2GC_275_461,(0,0,3):C.R2GC_275_462,(0,0,4):C.R2GC_275_463,(0,0,5):C.R2GC_275_464,(0,0,6):C.R2GC_275_465,(0,0,8):C.R2GC_275_466,(0,0,9):C.R2GC_275_467,(0,0,10):C.R2GC_275_468,(0,0,11):C.R2GC_275_469,(0,0,13):C.R2GC_275_470,(0,1,0):C.R2GC_256_370,(0,1,2):C.R2GC_256_371,(0,1,3):C.R2GC_256_372,(0,1,4):C.R2GC_256_373,(0,1,5):C.R2GC_252_323,(0,1,7):C.R2GC_256_374,(0,1,8):C.R2GC_256_375,(0,1,10):C.R2GC_252_324,(0,1,11):C.R2GC_252_327})

V_132 = CTVertex(name = 'V_132',
                 type = 'R2',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,12):C.R2GC_112_3,(0,0,0):C.R2GC_155_79,(0,0,2):C.R2GC_155_80,(0,0,4):C.R2GC_155_81,(0,0,5):C.R2GC_155_82,(0,0,7):C.R2GC_155_83,(0,0,8):C.R2GC_155_84,(0,0,9):C.R2GC_155_85,(0,0,10):C.R2GC_155_86,(0,0,11):C.R2GC_155_87,(0,0,12):C.R2GC_155_88,(0,1,1):C.R2GC_128_13,(0,1,3):C.R2GC_128_14,(0,1,6):C.R2GC_128_15})

V_133 = CTVertex(name = 'V_133',
                 type = 'R2',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,12):C.R2GC_114_5,(0,0,0):C.R2GC_160_106,(0,0,2):C.R2GC_160_107,(0,0,4):C.R2GC_160_108,(0,0,5):C.R2GC_160_109,(0,0,7):C.R2GC_160_110,(0,0,8):C.R2GC_160_111,(0,0,9):C.R2GC_160_112,(0,0,10):C.R2GC_160_113,(0,0,11):C.R2GC_160_114,(0,0,12):C.R2GC_160_115,(0,1,1):C.R2GC_146_48,(0,1,3):C.R2GC_146_49,(0,1,6):C.R2GC_146_50})

V_134 = CTVertex(name = 'V_134',
                 type = 'R2',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,13):C.R2GC_113_4,(0,0,0):C.R2GC_355_1126,(0,0,2):C.R2GC_355_1127,(0,0,4):C.R2GC_355_1128,(0,0,5):C.R2GC_355_1129,(0,0,7):C.R2GC_355_1130,(0,0,8):C.R2GC_355_1131,(0,0,9):C.R2GC_355_1132,(0,0,10):C.R2GC_355_1133,(0,0,11):C.R2GC_355_1134,(0,0,13):C.R2GC_355_1135,(0,1,1):C.R2GC_153_71,(0,1,3):C.R2GC_153_72,(0,1,6):C.R2GC_153_73,(0,1,12):C.R2GC_153_74})

V_135 = CTVertex(name = 'V_135',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,2,0):C.R2GC_112_3,(0,2,10):C.R2GC_113_4,(0,0,9):C.R2GC_274_448,(0,0,11):C.R2GC_274_449,(0,0,0):C.R2GC_274_450,(0,0,1):C.R2GC_274_451,(0,0,3):C.R2GC_274_452,(0,0,4):C.R2GC_274_453,(0,0,5):C.R2GC_274_454,(0,0,7):C.R2GC_274_455,(0,0,8):C.R2GC_274_456,(0,0,10):C.R2GC_274_457,(0,1,2):C.R2GC_177_155,(0,1,6):C.R2GC_241_261})

V_136 = CTVertex(name = 'V_136',
                 type = 'R2',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV3, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,2,4):C.R2GC_110_1,(0,0,0):C.R2GC_145_42,(0,0,2):C.R2GC_145_43,(0,0,3):C.R2GC_145_44,(0,0,5):C.R2GC_145_45,(0,0,6):C.R2GC_145_46,(0,0,7):C.R2GC_145_47,(0,1,1):C.R2GC_129_16})

V_137 = CTVertex(name = 'V_137',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_118_8})

V_138 = CTVertex(name = 'V_138',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_121_10})

V_139 = CTVertex(name = 'V_139',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_125_11})

V_140 = CTVertex(name = 'V_140',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_250_298,(0,0,1):C.R2GC_250_299,(0,0,2):C.R2GC_250_300,(0,0,3):C.R2GC_250_301,(0,0,5):C.R2GC_250_302,(0,0,6):C.R2GC_250_303,(0,0,7):C.R2GC_250_304,(0,0,8):C.R2GC_250_305,(0,0,9):C.R2GC_250_306,(0,0,10):C.R2GC_250_307,(0,0,4):C.R2GC_250_308})

V_141 = CTVertex(name = 'V_141',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_251_309,(0,0,1):C.R2GC_251_310,(0,0,2):C.R2GC_251_311,(0,0,3):C.R2GC_251_312,(0,0,5):C.R2GC_251_313,(0,0,6):C.R2GC_251_314,(0,0,7):C.R2GC_251_315,(0,0,8):C.R2GC_251_316,(0,0,9):C.R2GC_251_317,(0,0,10):C.R2GC_251_318,(0,0,4):C.R2GC_251_319})

V_142 = CTVertex(name = 'V_142',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_151_59,(0,0,1):C.R2GC_151_60,(0,0,2):C.R2GC_151_61,(0,0,3):C.R2GC_151_62,(0,0,4):C.R2GC_151_63,(0,0,5):C.R2GC_151_64})

V_143 = CTVertex(name = 'V_143',
                 type = 'R2',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_127_12})

V_144 = CTVertex(name = 'V_144',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_154_75,(0,0,1):C.R2GC_154_76,(0,0,2):C.R2GC_154_77,(0,0,3):C.R2GC_154_78})

V_145 = CTVertex(name = 'V_145',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_159_102,(0,0,1):C.R2GC_159_103,(0,0,2):C.R2GC_159_104,(0,0,3):C.R2GC_159_105})

V_146 = CTVertex(name = 'V_146',
                 type = 'R2',
                 particles = [ P.a, P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_158_98,(0,0,1):C.R2GC_158_99,(0,0,2):C.R2GC_158_100,(0,0,3):C.R2GC_158_101})

V_147 = CTVertex(name = 'V_147',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_157_94,(0,0,1):C.R2GC_157_95,(0,0,2):C.R2GC_157_96,(0,0,3):C.R2GC_157_97})

V_148 = CTVertex(name = 'V_148',
                 type = 'R2',
                 particles = [ P.Z, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_156_89,(0,0,1):C.R2GC_156_90,(0,0,2):C.R2GC_156_91,(0,0,3):C.R2GC_156_92,(0,0,4):C.R2GC_156_93})

V_149 = CTVertex(name = 'V_149',
                 type = 'R2',
                 particles = [ P.a, P.a, P.g, P.g ],
                 color = [ 'Identity(3,4)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_130_17,(0,0,1):C.R2GC_130_18})

V_150 = CTVertex(name = 'V_150',
                 type = 'R2',
                 particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_210_219})

V_151 = CTVertex(name = 'V_151',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.Z ],
                 color = [ 'Identity(2,3)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_147_51,(0,0,1):C.R2GC_147_52})

V_152 = CTVertex(name = 'V_152',
                 type = 'R2',
                 particles = [ P.g, P.g, P.Z, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_150_57,(0,0,1):C.R2GC_150_58})

V_153 = CTVertex(name = 'V_153',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.g ],
                 color = [ 'd(2,3,4)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_132_21,(0,0,1):C.R2GC_132_22})

V_154 = CTVertex(name = 'V_154',
                 type = 'R2',
                 particles = [ P.g, P.g, P.g, P.Z ],
                 color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                 lorentz = [ L.VVVV1, L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(1,0,0):C.R2GC_149_55,(1,0,1):C.R2GC_149_56,(0,1,0):C.R2GC_148_53,(0,1,1):C.R2GC_148_54})

V_155 = CTVertex(name = 'V_155',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_247_265,(0,0,1):C.R2GC_247_266,(0,0,2):C.R2GC_247_267,(0,0,3):C.R2GC_247_268,(0,0,5):C.R2GC_247_269,(0,0,6):C.R2GC_247_270,(0,0,7):C.R2GC_247_271,(0,0,8):C.R2GC_247_272,(0,0,9):C.R2GC_247_273,(0,0,10):C.R2GC_247_274,(0,0,4):C.R2GC_247_275})

V_156 = CTVertex(name = 'V_156',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_248_276,(0,0,1):C.R2GC_248_277,(0,0,2):C.R2GC_248_278,(0,0,3):C.R2GC_248_279,(0,0,5):C.R2GC_248_280,(0,0,6):C.R2GC_248_281,(0,0,7):C.R2GC_248_282,(0,0,8):C.R2GC_248_283,(0,0,9):C.R2GC_248_284,(0,0,10):C.R2GC_248_285,(0,0,4):C.R2GC_248_286})

V_157 = CTVertex(name = 'V_157',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_152_65,(0,0,1):C.R2GC_152_66,(0,0,2):C.R2GC_152_67,(0,0,3):C.R2GC_152_68,(0,0,4):C.R2GC_152_69,(0,0,5):C.R2GC_152_70})

V_158 = CTVertex(name = 'V_158',
                 type = 'R2',
                 particles = [ P.a, P.a, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_247_265,(0,0,1):C.R2GC_247_266,(0,0,2):C.R2GC_247_267,(0,0,3):C.R2GC_247_268,(0,0,5):C.R2GC_247_269,(0,0,6):C.R2GC_247_270,(0,0,7):C.R2GC_247_271,(0,0,8):C.R2GC_247_272,(0,0,9):C.R2GC_247_273,(0,0,10):C.R2GC_247_274,(0,0,4):C.R2GC_247_275})

V_159 = CTVertex(name = 'V_159',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_248_276,(0,0,1):C.R2GC_248_277,(0,0,2):C.R2GC_248_278,(0,0,3):C.R2GC_248_279,(0,0,5):C.R2GC_248_280,(0,0,6):C.R2GC_248_281,(0,0,7):C.R2GC_248_282,(0,0,8):C.R2GC_248_283,(0,0,9):C.R2GC_248_284,(0,0,10):C.R2GC_248_285,(0,0,4):C.R2GC_248_286})

V_160 = CTVertex(name = 'V_160',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G0, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_152_65,(0,0,1):C.R2GC_152_66,(0,0,2):C.R2GC_152_67,(0,0,3):C.R2GC_152_68,(0,0,4):C.R2GC_152_69,(0,0,5):C.R2GC_152_70})

V_161 = CTVertex(name = 'V_161',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_342_980,(0,0,8):C.R2GC_342_981,(0,0,0):C.R2GC_342_982,(0,0,1):C.R2GC_342_983,(0,0,2):C.R2GC_342_984,(0,0,3):C.R2GC_342_985,(0,0,4):C.R2GC_342_986,(0,0,6):C.R2GC_342_987,(0,0,7):C.R2GC_342_988,(0,0,9):C.R2GC_342_989})

V_162 = CTVertex(name = 'V_162',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_211_220,(0,0,1):C.R2GC_211_221,(0,0,2):C.R2GC_211_222})

V_163 = CTVertex(name = 'V_163',
                 type = 'R2',
                 particles = [ P.W__plus__, P.W__plus__, P.G__minus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_342_980,(0,0,8):C.R2GC_342_981,(0,0,0):C.R2GC_342_982,(0,0,1):C.R2GC_342_983,(0,0,2):C.R2GC_342_984,(0,0,3):C.R2GC_342_985,(0,0,4):C.R2GC_342_986,(0,0,6):C.R2GC_342_987,(0,0,7):C.R2GC_342_988,(0,0,9):C.R2GC_342_989})

V_164 = CTVertex(name = 'V_164',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_356_2})

V_165 = CTVertex(name = 'V_165',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_356_2})

V_166 = CTVertex(name = 'V_166',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_356_2})

V_167 = CTVertex(name = 'V_167',
                 type = 'UV',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1 ],
                 loop_particles = [ [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_355_1})

