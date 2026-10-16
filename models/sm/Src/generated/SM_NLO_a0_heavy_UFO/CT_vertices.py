# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Thu 15 Oct 2026 20:55:19


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS2 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_407_815,(0,0,1):C.R2GC_407_816,(0,0,2):C.R2GC_407_817,(0,0,3):C.R2GC_407_818,(0,0,7):C.R2GC_407_819,(0,0,8):C.R2GC_407_820,(0,0,9):C.R2GC_407_821,(0,0,10):C.R2GC_407_822,(0,0,11):C.R2GC_407_823,(0,0,12):C.R2GC_407_824,(0,0,13):C.R2GC_407_825,(0,0,5):C.R2GC_407_826,(0,0,6):C.R2GC_407_827,(0,0,4):C.R2GC_407_828})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS2 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,15):C.R2GC_407_824,(0,0,17):C.R2GC_414_871,(0,0,0):C.R2GC_414_872,(0,0,2):C.R2GC_293_231,(0,0,3):C.R2GC_414_873,(0,0,4):C.R2GC_414_874,(0,0,5):C.R2GC_414_875,(0,0,6):C.R2GC_407_818,(0,0,7):C.R2GC_414_876,(0,0,11):C.R2GC_414_877,(0,0,12):C.R2GC_414_878,(0,0,13):C.R2GC_407_819,(0,0,14):C.R2GC_407_822,(0,0,16):C.R2GC_414_879,(0,0,1):C.R2GC_414_880,(0,0,8):C.R2GC_414_881,(0,0,9):C.R2GC_414_882,(0,0,10):C.R2GC_414_883})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS2 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_310_327,(0,0,1):C.R2GC_310_328,(0,0,2):C.R2GC_310_329,(0,0,3):C.R2GC_310_330,(0,0,6):C.R2GC_310_331,(0,0,7):C.R2GC_310_332,(0,0,8):C.R2GC_310_333,(0,0,9):C.R2GC_310_334,(0,0,10):C.R2GC_310_335,(0,0,11):C.R2GC_310_336,(0,0,12):C.R2GC_310_337,(0,0,4):C.R2GC_310_338,(0,0,5):C.R2GC_310_339})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVSS2 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
               couplings = {(0,0,9):C.R2GC_296_253,(0,0,0):C.R2GC_311_340,(0,0,1):C.R2GC_311_341,(0,0,2):C.R2GC_311_342,(0,0,3):C.R2GC_311_343,(0,0,4):C.R2GC_311_344,(0,0,5):C.R2GC_311_345,(0,0,6):C.R2GC_311_346,(0,0,7):C.R2GC_311_347,(0,0,8):C.R2GC_311_348})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.a, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS5, L.VSS8 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
               couplings = {(0,0,0):C.R2GC_305_304,(0,0,1):C.R2GC_305_305,(0,0,2):C.R2GC_305_306,(0,0,3):C.R2GC_305_307,(0,0,4):C.R2GC_305_308,(0,0,5):C.R2GC_305_309,(0,0,6):C.R2GC_305_310,(0,0,7):C.R2GC_305_311,(0,0,8):C.R2GC_305_312,(0,1,0):C.R2GC_306_313,(0,1,1):C.R2GC_306_314,(0,1,2):C.R2GC_306_315,(0,1,3):C.R2GC_306_316,(0,1,4):C.R2GC_306_317,(0,1,5):C.R2GC_306_318,(0,1,6):C.R2GC_306_319,(0,1,7):C.R2GC_306_320,(0,1,8):C.R2GC_306_321})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV16, L.VVV17, L.VVV19, L.VVV21, L.VVV25, L.VVV26 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_172_73,(0,0,1):C.R2GC_172_74,(0,1,0):C.R2GC_169_71,(0,1,1):C.R2GC_169_72,(0,2,0):C.R2GC_169_71,(0,2,1):C.R2GC_169_72,(0,3,0):C.R2GC_172_73,(0,3,1):C.R2GC_172_74,(0,4,0):C.R2GC_172_73,(0,4,1):C.R2GC_172_74,(0,5,0):C.R2GC_169_71,(0,5,1):C.R2GC_169_72})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,1,0):C.R2GC_147_63,(0,1,1):C.R2GC_147_64,(2,1,0):C.R2GC_147_63,(2,1,1):C.R2GC_147_64,(6,1,0):C.R2GC_177_77,(6,1,1):C.R2GC_180_82,(7,1,0):C.R2GC_178_79,(7,1,1):C.R2GC_179_81,(5,1,0):C.R2GC_145_59,(5,1,1):C.R2GC_145_60,(1,1,0):C.R2GC_145_59,(1,1,1):C.R2GC_145_60,(4,1,0):C.R2GC_145_59,(4,1,1):C.R2GC_145_60,(3,1,0):C.R2GC_145_59,(3,1,1):C.R2GC_145_60,(8,1,0):C.R2GC_146_61,(8,1,1):C.R2GC_146_62,(11,1,0):C.R2GC_149_66,(11,1,1):C.R2GC_149_67,(10,1,0):C.R2GC_149_66,(10,1,1):C.R2GC_149_67,(9,1,1):C.R2GC_148_65,(0,2,0):C.R2GC_147_63,(0,2,1):C.R2GC_147_64,(2,2,0):C.R2GC_147_63,(2,2,1):C.R2GC_147_64,(6,2,0):C.R2GC_181_83,(6,2,1):C.R2GC_181_84,(7,2,0):C.R2GC_178_79,(7,2,1):C.R2GC_178_80,(5,2,0):C.R2GC_145_59,(5,2,1):C.R2GC_145_60,(1,2,0):C.R2GC_145_59,(1,2,1):C.R2GC_145_60,(4,2,0):C.R2GC_145_59,(4,2,1):C.R2GC_145_60,(3,2,0):C.R2GC_145_59,(3,2,1):C.R2GC_145_60,(8,2,0):C.R2GC_146_61,(8,2,1):C.R2GC_176_76,(11,2,0):C.R2GC_149_66,(11,2,1):C.R2GC_149_67,(10,2,0):C.R2GC_149_66,(10,2,1):C.R2GC_149_67,(9,2,1):C.R2GC_148_65,(0,0,0):C.R2GC_147_63,(0,0,1):C.R2GC_147_64,(2,0,0):C.R2GC_147_63,(2,0,1):C.R2GC_147_64,(6,0,0):C.R2GC_177_77,(6,0,1):C.R2GC_177_78,(7,0,0):C.R2GC_182_85,(7,0,1):C.R2GC_147_64,(5,0,0):C.R2GC_145_59,(5,0,1):C.R2GC_145_60,(1,0,0):C.R2GC_145_59,(1,0,1):C.R2GC_145_60,(4,0,0):C.R2GC_145_59,(4,0,1):C.R2GC_145_60,(3,0,0):C.R2GC_145_59,(3,0,1):C.R2GC_145_60,(8,0,0):C.R2GC_146_61,(8,0,1):C.R2GC_175_75,(11,0,0):C.R2GC_149_66,(11,0,1):C.R2GC_149_67,(10,0,0):C.R2GC_149_66,(10,0,1):C.R2GC_149_67,(9,0,1):C.R2GC_148_65})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.u__tilde__, P.d, P.G__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS7, L.FFS8 ],
               loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_380_640,(0,0,1):C.R2GC_380_641,(0,0,2):C.R2GC_380_642,(0,0,6):C.R2GC_380_643,(0,0,3):C.R2GC_380_644,(0,0,4):C.R2GC_380_645,(0,0,5):C.R2GC_380_646,(0,0,7):C.R2GC_380_647,(0,0,9):C.R2GC_380_648,(0,1,0):C.R2GC_381_649,(0,1,1):C.R2GC_381_650,(0,1,2):C.R2GC_381_651,(0,1,6):C.R2GC_381_652,(0,1,3):C.R2GC_381_653,(0,1,5):C.R2GC_381_654,(0,1,7):C.R2GC_381_655,(0,1,8):C.R2GC_381_656,(0,1,9):C.R2GC_381_657})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.c__tilde__, P.s, P.G__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS7, L.FFS8 ],
               loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_356_500,(0,0,1):C.R2GC_356_501,(0,0,2):C.R2GC_356_502,(0,0,6):C.R2GC_356_503,(0,0,3):C.R2GC_356_504,(0,0,5):C.R2GC_356_505,(0,0,7):C.R2GC_356_506,(0,0,8):C.R2GC_356_507,(0,0,9):C.R2GC_356_508,(0,1,0):C.R2GC_357_509,(0,1,1):C.R2GC_357_510,(0,1,2):C.R2GC_357_511,(0,1,6):C.R2GC_357_512,(0,1,3):C.R2GC_357_513,(0,1,4):C.R2GC_357_514,(0,1,5):C.R2GC_357_515,(0,1,7):C.R2GC_357_516,(0,1,9):C.R2GC_357_517})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS7, L.FFS8 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_367_572,(0,0,1):C.R2GC_367_573,(0,0,2):C.R2GC_367_574,(0,0,6):C.R2GC_367_575,(0,0,3):C.R2GC_367_576,(0,0,4):C.R2GC_367_577,(0,0,5):C.R2GC_367_578,(0,0,7):C.R2GC_367_579,(0,0,9):C.R2GC_367_580,(0,1,0):C.R2GC_366_563,(0,1,1):C.R2GC_366_564,(0,1,2):C.R2GC_366_565,(0,1,6):C.R2GC_366_566,(0,1,3):C.R2GC_366_567,(0,1,5):C.R2GC_366_568,(0,1,7):C.R2GC_366_569,(0,1,8):C.R2GC_366_570,(0,1,9):C.R2GC_366_571})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_377_616,(0,0,1):C.R2GC_377_617,(0,0,2):C.R2GC_377_618,(0,0,3):C.R2GC_377_619,(0,0,5):C.R2GC_377_620,(0,0,6):C.R2GC_377_621,(0,0,4):C.R2GC_377_622,(0,0,7):C.R2GC_377_623})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_358_518,(0,0,1):C.R2GC_358_519,(0,0,4):C.R2GC_358_520,(0,0,3):C.R2GC_358_521,(0,0,5):C.R2GC_358_522,(0,0,7):C.R2GC_358_523,(0,0,2):C.R2GC_358_524,(0,0,6):C.R2GC_358_525})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_363_539,(0,0,1):C.R2GC_363_540,(0,0,2):C.R2GC_363_541,(0,0,3):C.R2GC_363_542,(0,0,5):C.R2GC_363_543,(0,0,6):C.R2GC_363_544,(0,0,4):C.R2GC_363_545,(0,0,7):C.R2GC_363_546})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_378_624,(0,0,1):C.R2GC_378_625,(0,0,2):C.R2GC_378_626,(0,0,4):C.R2GC_378_627,(0,0,5):C.R2GC_378_628,(0,0,6):C.R2GC_378_629,(0,0,3):C.R2GC_378_630,(0,0,7):C.R2GC_378_631})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_353_474,(0,0,1):C.R2GC_353_475,(0,0,5):C.R2GC_353_476,(0,0,3):C.R2GC_353_477,(0,0,6):C.R2GC_353_478,(0,0,7):C.R2GC_353_479,(0,0,2):C.R2GC_353_480,(0,0,4):C.R2GC_353_481})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_364_547,(0,0,1):C.R2GC_364_548,(0,0,2):C.R2GC_364_549,(0,0,4):C.R2GC_364_550,(0,0,5):C.R2GC_364_551,(0,0,6):C.R2GC_364_552,(0,0,3):C.R2GC_364_553,(0,0,7):C.R2GC_364_554})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS7 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_388_696,(0,0,1):C.R2GC_388_697,(0,0,2):C.R2GC_388_698,(0,0,3):C.R2GC_388_699,(0,0,4):C.R2GC_388_700})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS7 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_393_722,(0,0,1):C.R2GC_393_723,(0,0,2):C.R2GC_393_724,(0,0,3):C.R2GC_393_725,(0,0,4):C.R2GC_393_726})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS7 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_398_744,(0,0,1):C.R2GC_398_745,(0,0,2):C.R2GC_398_746,(0,0,3):C.R2GC_398_747,(0,0,4):C.R2GC_398_748})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_386_684,(0,0,1):C.R2GC_386_685,(0,0,2):C.R2GC_386_686,(0,0,4):C.R2GC_386_687,(0,0,3):C.R2GC_386_688,(0,0,5):C.R2GC_386_689})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_391_710,(0,0,1):C.R2GC_391_711,(0,0,3):C.R2GC_391_712,(0,0,5):C.R2GC_391_713,(0,0,2):C.R2GC_391_714,(0,0,4):C.R2GC_391_715})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_396_732,(0,0,1):C.R2GC_396_733,(0,0,3):C.R2GC_396_734,(0,0,5):C.R2GC_396_735,(0,0,2):C.R2GC_396_736,(0,0,4):C.R2GC_396_737})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_387_690,(0,0,1):C.R2GC_387_691,(0,0,3):C.R2GC_387_692,(0,0,4):C.R2GC_387_693,(0,0,2):C.R2GC_387_694,(0,0,5):C.R2GC_387_695})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_392_716,(0,0,1):C.R2GC_392_717,(0,0,4):C.R2GC_392_718,(0,0,5):C.R2GC_392_719,(0,0,2):C.R2GC_392_720,(0,0,3):C.R2GC_392_721})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_397_738,(0,0,1):C.R2GC_397_739,(0,0,4):C.R2GC_397_740,(0,0,5):C.R2GC_397_741,(0,0,2):C.R2GC_397_742,(0,0,3):C.R2GC_397_743})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS7, L.FFS8 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_382_658,(0,0,1):C.R2GC_382_659,(0,0,2):C.R2GC_382_660,(0,0,6):C.R2GC_382_661,(0,0,3):C.R2GC_382_662,(0,0,5):C.R2GC_382_663,(0,0,7):C.R2GC_382_664,(0,0,8):C.R2GC_382_665,(0,0,9):C.R2GC_382_666,(0,1,0):C.R2GC_383_667,(0,1,1):C.R2GC_383_668,(0,1,2):C.R2GC_383_669,(0,1,6):C.R2GC_383_670,(0,1,3):C.R2GC_383_671,(0,1,4):C.R2GC_383_672,(0,1,5):C.R2GC_383_673,(0,1,7):C.R2GC_383_674,(0,1,9):C.R2GC_383_675})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS7, L.FFS8 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_354_482,(0,0,1):C.R2GC_354_483,(0,0,2):C.R2GC_354_484,(0,0,6):C.R2GC_354_485,(0,0,3):C.R2GC_354_486,(0,0,4):C.R2GC_354_487,(0,0,5):C.R2GC_354_488,(0,0,7):C.R2GC_354_489,(0,0,9):C.R2GC_354_490,(0,1,0):C.R2GC_355_491,(0,1,1):C.R2GC_355_492,(0,1,2):C.R2GC_355_493,(0,1,6):C.R2GC_355_494,(0,1,3):C.R2GC_355_495,(0,1,5):C.R2GC_355_496,(0,1,7):C.R2GC_355_497,(0,1,8):C.R2GC_355_498,(0,1,9):C.R2GC_355_499})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS7, L.FFS8 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_369_590,(0,0,1):C.R2GC_369_591,(0,0,2):C.R2GC_369_592,(0,0,6):C.R2GC_369_593,(0,0,3):C.R2GC_369_594,(0,0,5):C.R2GC_369_595,(0,0,7):C.R2GC_369_596,(0,0,8):C.R2GC_369_597,(0,0,9):C.R2GC_369_598,(0,1,0):C.R2GC_368_581,(0,1,1):C.R2GC_368_582,(0,1,2):C.R2GC_368_583,(0,1,6):C.R2GC_368_584,(0,1,3):C.R2GC_368_585,(0,1,4):C.R2GC_368_586,(0,1,5):C.R2GC_368_587,(0,1,7):C.R2GC_368_588,(0,1,9):C.R2GC_368_589})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_384_676,(0,0,1):C.R2GC_384_677,(0,0,4):C.R2GC_384_678,(0,0,3):C.R2GC_384_679,(0,0,5):C.R2GC_384_680,(0,0,7):C.R2GC_384_681,(0,0,2):C.R2GC_384_682,(0,0,6):C.R2GC_384_683})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_352_466,(0,0,1):C.R2GC_352_467,(0,0,2):C.R2GC_352_468,(0,0,3):C.R2GC_352_469,(0,0,5):C.R2GC_352_470,(0,0,6):C.R2GC_352_471,(0,0,4):C.R2GC_352_472,(0,0,7):C.R2GC_352_473})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS5 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_370_599,(0,0,1):C.R2GC_370_600,(0,0,4):C.R2GC_370_601,(0,0,3):C.R2GC_370_602,(0,0,5):C.R2GC_370_603,(0,0,7):C.R2GC_370_604,(0,0,2):C.R2GC_370_605,(0,0,6):C.R2GC_370_606})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_379_632,(0,0,1):C.R2GC_379_633,(0,0,5):C.R2GC_379_634,(0,0,3):C.R2GC_379_635,(0,0,6):C.R2GC_379_636,(0,0,7):C.R2GC_379_637,(0,0,2):C.R2GC_379_638,(0,0,4):C.R2GC_379_639})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_351_458,(0,0,1):C.R2GC_351_459,(0,0,2):C.R2GC_351_460,(0,0,4):C.R2GC_351_461,(0,0,5):C.R2GC_351_462,(0,0,6):C.R2GC_351_463,(0,0,3):C.R2GC_351_464,(0,0,7):C.R2GC_351_465})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS6 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_365_555,(0,0,1):C.R2GC_365_556,(0,0,5):C.R2GC_365_557,(0,0,3):C.R2GC_365_558,(0,0,6):C.R2GC_365_559,(0,0,7):C.R2GC_365_560,(0,0,2):C.R2GC_365_561,(0,0,4):C.R2GC_365_562})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_428_992,(0,0,2):C.R2GC_428_993,(0,0,3):C.R2GC_428_994,(0,0,4):C.R2GC_428_995,(0,0,5):C.R2GC_428_996,(0,0,7):C.R2GC_428_997,(0,0,10):C.R2GC_428_998,(0,0,13):C.R2GC_428_999,(0,0,14):C.R2GC_428_1000,(0,0,15):C.R2GC_428_1001,(0,0,0):C.R2GC_428_1002,(0,0,6):C.R2GC_428_1003,(0,0,8):C.R2GC_428_1004,(0,0,9):C.R2GC_428_1005,(0,0,11):C.R2GC_428_1006,(0,0,12):C.R2GC_428_1007})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_419_920,(0,0,2):C.R2GC_421_944,(0,0,3):C.R2GC_421_945,(0,0,4):C.R2GC_421_946,(0,0,5):C.R2GC_421_947,(0,0,10):C.R2GC_419_917,(0,0,12):C.R2GC_419_916,(0,0,13):C.R2GC_421_948,(0,0,14):C.R2GC_421_949,(0,0,15):C.R2GC_419_911,(0,0,0):C.R2GC_421_950,(0,0,6):C.R2GC_419_925,(0,0,7):C.R2GC_421_951,(0,0,8):C.R2GC_421_952,(0,0,9):C.R2GC_419_922,(0,0,11):C.R2GC_421_953})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_411_856,(0,0,2):C.R2GC_418_905,(0,0,3):C.R2GC_418_906,(0,0,4):C.R2GC_418_907,(0,0,6):C.R2GC_418_908,(0,0,7):C.R2GC_411_851,(0,0,0):C.R2GC_418_909,(0,0,5):C.R2GC_418_910})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_423_963,(0,0,2):C.R2GC_423_964,(0,0,3):C.R2GC_423_965,(0,0,4):C.R2GC_423_966,(0,0,10):C.R2GC_423_967,(0,0,11):C.R2GC_423_968,(0,0,0):C.R2GC_423_969,(0,0,5):C.R2GC_423_970,(0,0,6):C.R2GC_423_971,(0,0,7):C.R2GC_423_972,(0,0,8):C.R2GC_423_973,(0,0,9):C.R2GC_423_974,(0,1,1):C.R2GC_425_975,(0,1,2):C.R2GC_425_976,(0,1,3):C.R2GC_425_977,(0,1,4):C.R2GC_425_978,(0,1,10):C.R2GC_425_979,(0,1,11):C.R2GC_425_980,(0,1,0):C.R2GC_425_981,(0,1,5):C.R2GC_423_971,(0,1,6):C.R2GC_423_970,(0,1,7):C.R2GC_425_982,(0,1,8):C.R2GC_425_983,(0,1,9):C.R2GC_425_984})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_416_895,(0,0,2):C.R2GC_416_896,(0,0,3):C.R2GC_416_897,(0,0,4):C.R2GC_416_898,(0,0,10):C.R2GC_416_899,(0,0,11):C.R2GC_416_900,(0,0,0):C.R2GC_416_901,(0,0,5):C.R2GC_412_869,(0,0,6):C.R2GC_416_902,(0,0,7):C.R2GC_416_903,(0,0,8):C.R2GC_412_866,(0,0,9):C.R2GC_416_904,(0,1,1):C.R2GC_412_859,(0,1,2):C.R2GC_412_860,(0,1,3):C.R2GC_412_861,(0,1,4):C.R2GC_412_862,(0,1,10):C.R2GC_412_863,(0,1,11):C.R2GC_412_864,(0,1,0):C.R2GC_412_865,(0,1,5):C.R2GC_412_866,(0,1,6):C.R2GC_412_867,(0,1,7):C.R2GC_412_868,(0,1,8):C.R2GC_412_869,(0,1,9):C.R2GC_412_870})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVV16, L.VVV17, L.VVV19, L.VVV21, L.VVV25, L.VVV26 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_319_379,(0,0,1):C.R2GC_319_380,(0,0,2):C.R2GC_319_381,(0,0,3):C.R2GC_319_382,(0,1,0):C.R2GC_316_373,(0,1,1):C.R2GC_286_190,(0,1,2):C.R2GC_279_180,(0,1,3):C.R2GC_316_374,(0,2,0):C.R2GC_316_373,(0,2,1):C.R2GC_286_190,(0,2,2):C.R2GC_279_180,(0,2,3):C.R2GC_316_374,(0,3,0):C.R2GC_319_379,(0,3,1):C.R2GC_319_380,(0,3,2):C.R2GC_319_381,(0,3,3):C.R2GC_319_382,(0,4,0):C.R2GC_319_379,(0,4,1):C.R2GC_319_380,(0,4,2):C.R2GC_319_381,(0,4,3):C.R2GC_319_382,(0,5,0):C.R2GC_316_373,(0,5,1):C.R2GC_286_190,(0,5,2):C.R2GC_279_180,(0,5,3):C.R2GC_316_374})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_428_992,(0,0,2):C.R2GC_428_993,(0,0,3):C.R2GC_428_994,(0,0,4):C.R2GC_428_995,(0,0,5):C.R2GC_428_996,(0,0,7):C.R2GC_428_997,(0,0,10):C.R2GC_428_998,(0,0,13):C.R2GC_428_999,(0,0,14):C.R2GC_428_1000,(0,0,15):C.R2GC_428_1001,(0,0,0):C.R2GC_428_1002,(0,0,6):C.R2GC_428_1003,(0,0,8):C.R2GC_428_1004,(0,0,9):C.R2GC_428_1005,(0,0,11):C.R2GC_428_1006,(0,0,12):C.R2GC_428_1007})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_419_911,(0,0,2):C.R2GC_419_912,(0,0,3):C.R2GC_419_913,(0,0,4):C.R2GC_419_914,(0,0,5):C.R2GC_419_915,(0,0,10):C.R2GC_419_916,(0,0,12):C.R2GC_419_917,(0,0,13):C.R2GC_419_918,(0,0,14):C.R2GC_419_919,(0,0,15):C.R2GC_419_920,(0,0,0):C.R2GC_419_921,(0,0,6):C.R2GC_419_922,(0,0,7):C.R2GC_419_923,(0,0,8):C.R2GC_419_924,(0,0,9):C.R2GC_419_925,(0,0,11):C.R2GC_419_926})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_411_851,(0,0,2):C.R2GC_411_852,(0,0,3):C.R2GC_411_853,(0,0,4):C.R2GC_411_854,(0,0,6):C.R2GC_411_855,(0,0,7):C.R2GC_411_856,(0,0,0):C.R2GC_411_857,(0,0,5):C.R2GC_411_858})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_425_975,(0,0,2):C.R2GC_425_976,(0,0,3):C.R2GC_425_977,(0,0,4):C.R2GC_425_978,(0,0,10):C.R2GC_425_979,(0,0,11):C.R2GC_425_980,(0,0,0):C.R2GC_425_981,(0,0,5):C.R2GC_423_971,(0,0,6):C.R2GC_423_970,(0,0,7):C.R2GC_425_982,(0,0,8):C.R2GC_425_983,(0,0,9):C.R2GC_425_984,(0,1,1):C.R2GC_423_963,(0,1,2):C.R2GC_423_964,(0,1,3):C.R2GC_423_965,(0,1,4):C.R2GC_423_966,(0,1,10):C.R2GC_423_967,(0,1,11):C.R2GC_423_968,(0,1,0):C.R2GC_423_969,(0,1,5):C.R2GC_423_970,(0,1,6):C.R2GC_423_971,(0,1,7):C.R2GC_423_972,(0,1,8):C.R2GC_423_973,(0,1,9):C.R2GC_423_974})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_416_895,(0,0,2):C.R2GC_416_896,(0,0,3):C.R2GC_416_897,(0,0,4):C.R2GC_416_898,(0,0,10):C.R2GC_416_899,(0,0,11):C.R2GC_416_900,(0,0,0):C.R2GC_416_901,(0,0,5):C.R2GC_412_869,(0,0,6):C.R2GC_416_902,(0,0,7):C.R2GC_416_903,(0,0,8):C.R2GC_412_866,(0,0,9):C.R2GC_416_904,(0,1,1):C.R2GC_412_859,(0,1,2):C.R2GC_412_860,(0,1,3):C.R2GC_412_861,(0,1,4):C.R2GC_412_862,(0,1,10):C.R2GC_412_863,(0,1,11):C.R2GC_412_864,(0,1,0):C.R2GC_412_865,(0,1,5):C.R2GC_412_866,(0,1,6):C.R2GC_412_867,(0,1,7):C.R2GC_412_868,(0,1,8):C.R2GC_412_869,(0,1,9):C.R2GC_412_870})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_420_927,(0,0,16):C.R2GC_420_928,(0,0,1):C.R2GC_420_929,(0,0,2):C.R2GC_420_930,(0,0,3):C.R2GC_420_931,(0,0,4):C.R2GC_420_932,(0,0,5):C.R2GC_420_933,(0,0,8):C.R2GC_420_935,(0,0,11):C.R2GC_420_934,(0,0,12):C.R2GC_420_936,(0,0,13):C.R2GC_420_937,(0,0,15):C.R2GC_420_938,(0,0,0):C.R2GC_420_939,(0,0,6):C.R2GC_420_940,(0,0,7):C.R2GC_420_941,(0,0,9):C.R2GC_420_943,(0,0,10):C.R2GC_420_942})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.G0, P.G__plus__], [P.a, P.G__plus__, P.H] ], [ [P.a, P.G0, P.W__plus__], [P.a, P.H, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.G__plus__, P.W__plus__, P.Z] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z], [P.G__plus__, P.H, P.Z] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z], [P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_431_1018,(0,0,22):C.R2GC_420_927,(0,0,24):C.R2GC_431_1019,(0,0,3):C.R2GC_431_1020,(0,0,7):C.R2GC_431_1021,(0,0,9):C.R2GC_431_1022,(0,0,10):C.R2GC_420_930,(0,0,11):C.R2GC_420_931,(0,0,12):C.R2GC_420_932,(0,0,13):C.R2GC_420_933,(0,0,16):C.R2GC_431_1023,(0,0,19):C.R2GC_431_1024,(0,0,20):C.R2GC_420_936,(0,0,21):C.R2GC_420_937,(0,0,23):C.R2GC_431_1025,(0,0,1):C.R2GC_431_1026,(0,0,2):C.R2GC_431_1027,(0,0,4):C.R2GC_431_1028,(0,0,6):C.R2GC_431_1029,(0,0,8):C.R2GC_431_1030,(0,0,14):C.R2GC_420_940,(0,0,15):C.R2GC_431_1031,(0,0,17):C.R2GC_431_1032,(0,0,18):C.R2GC_431_1033,(0,0,5):C.R2GC_431_1034})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_420_927,(0,0,16):C.R2GC_420_928,(0,0,1):C.R2GC_420_929,(0,0,2):C.R2GC_420_930,(0,0,3):C.R2GC_420_931,(0,0,4):C.R2GC_420_932,(0,0,5):C.R2GC_420_933,(0,0,9):C.R2GC_420_934,(0,0,10):C.R2GC_420_935,(0,0,12):C.R2GC_420_936,(0,0,13):C.R2GC_420_937,(0,0,15):C.R2GC_420_938,(0,0,0):C.R2GC_420_939,(0,0,6):C.R2GC_420_940,(0,0,7):C.R2GC_420_941,(0,0,8):C.R2GC_420_942,(0,0,11):C.R2GC_420_943})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,9):C.R2GC_415_884,(0,0,11):C.R2GC_415_885,(0,0,1):C.R2GC_415_886,(0,0,2):C.R2GC_415_887,(0,0,3):C.R2GC_415_888,(0,0,4):C.R2GC_415_889,(0,0,5):C.R2GC_415_890,(0,0,7):C.R2GC_415_891,(0,0,8):C.R2GC_415_892,(0,0,10):C.R2GC_415_893,(0,0,0):C.R2GC_415_894,(0,0,6):C.R2GC_414_880})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,1,3):C.R2GC_326_383,(0,1,0):C.R2GC_326_384,(0,1,1):C.R2GC_326_385,(0,1,2):C.R2GC_326_386,(0,1,4):C.R2GC_326_387,(0,2,3):C.R2GC_326_383,(0,2,0):C.R2GC_326_384,(0,2,1):C.R2GC_326_385,(0,2,2):C.R2GC_326_386,(0,2,4):C.R2GC_326_387,(0,0,3):C.R2GC_327_388,(0,0,0):C.R2GC_327_389,(0,0,1):C.R2GC_327_390,(0,0,2):C.R2GC_327_391,(0,0,4):C.R2GC_327_392})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVV16, L.VVV17, L.VVV19, L.VVV21, L.VVV25, L.VVV26 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_336_427,(0,0,1):C.R2GC_336_428,(0,0,2):C.R2GC_336_429,(0,0,3):C.R2GC_336_430,(0,1,0):C.R2GC_317_375,(0,1,1):C.R2GC_317_376,(0,1,2):C.R2GC_317_377,(0,1,3):C.R2GC_317_378,(0,2,0):C.R2GC_317_375,(0,2,1):C.R2GC_317_376,(0,2,2):C.R2GC_317_377,(0,2,3):C.R2GC_317_378,(0,3,0):C.R2GC_336_427,(0,3,1):C.R2GC_336_428,(0,3,2):C.R2GC_336_429,(0,3,3):C.R2GC_336_430,(0,4,0):C.R2GC_336_427,(0,4,1):C.R2GC_336_428,(0,4,2):C.R2GC_336_429,(0,4,3):C.R2GC_336_430,(0,5,0):C.R2GC_317_375,(0,5,1):C.R2GC_317_376,(0,5,2):C.R2GC_317_377,(0,5,3):C.R2GC_317_378})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,1,0):C.R2GC_432_1035,(0,1,6):C.R2GC_432_1036,(0,1,8):C.R2GC_432_1037,(0,1,1):C.R2GC_432_1038,(0,1,3):C.R2GC_432_1039,(0,1,4):C.R2GC_432_1040,(0,1,5):C.R2GC_432_1041,(0,1,7):C.R2GC_432_1042,(0,1,2):C.R2GC_432_1043,(0,2,0):C.R2GC_432_1035,(0,2,6):C.R2GC_432_1036,(0,2,8):C.R2GC_432_1037,(0,2,1):C.R2GC_432_1038,(0,2,3):C.R2GC_432_1039,(0,2,4):C.R2GC_432_1040,(0,2,5):C.R2GC_432_1041,(0,2,7):C.R2GC_432_1042,(0,2,2):C.R2GC_432_1043,(0,0,6):C.R2GC_433_1044,(0,0,1):C.R2GC_433_1045,(0,0,4):C.R2GC_433_1046,(0,0,5):C.R2GC_433_1047,(0,0,7):C.R2GC_433_1048,(0,0,2):C.R2GC_433_1049})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS8 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_389_701,(0,0,1):C.R2GC_389_702,(0,0,2):C.R2GC_389_703,(0,0,3):C.R2GC_389_704,(0,0,4):C.R2GC_389_705})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_394_727,(0,0,1):C.R2GC_394_728,(0,0,2):C.R2GC_394_729,(0,0,3):C.R2GC_394_730,(0,0,4):C.R2GC_394_731})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS8 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_399_749,(0,0,1):C.R2GC_399_750,(0,0,2):C.R2GC_399_751,(0,0,3):C.R2GC_399_752,(0,0,4):C.R2GC_399_753})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,9):C.R2GC_295_242,(0,0,0):C.R2GC_403_774,(0,0,1):C.R2GC_403_775,(0,0,2):C.R2GC_403_776,(0,0,3):C.R2GC_403_777,(0,0,4):C.R2GC_403_778,(0,0,5):C.R2GC_403_779,(0,0,6):C.R2GC_403_780,(0,0,7):C.R2GC_403_781,(0,0,8):C.R2GC_403_782})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.Z, P.G0, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_408_829,(0,0,1):C.R2GC_408_830,(0,0,2):C.R2GC_408_831,(0,0,3):C.R2GC_408_832,(0,0,6):C.R2GC_408_833,(0,0,7):C.R2GC_408_834,(0,0,8):C.R2GC_408_835,(0,0,9):C.R2GC_408_836,(0,0,10):C.R2GC_408_837,(0,0,5):C.R2GC_408_838,(0,0,4):C.R2GC_408_839,(0,1,0):C.R2GC_405_793,(0,1,1):C.R2GC_405_794,(0,1,2):C.R2GC_405_795,(0,1,3):C.R2GC_405_796,(0,1,6):C.R2GC_405_797,(0,1,7):C.R2GC_405_798,(0,1,8):C.R2GC_405_799,(0,1,9):C.R2GC_405_800,(0,1,10):C.R2GC_405_801,(0,1,5):C.R2GC_405_802,(0,1,4):C.R2GC_405_803})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS5, L.VSS8 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_401_754,(0,0,1):C.R2GC_401_755,(0,0,2):C.R2GC_401_756,(0,0,3):C.R2GC_401_757,(0,0,4):C.R2GC_401_758,(0,0,6):C.R2GC_401_759,(0,0,7):C.R2GC_401_760,(0,0,8):C.R2GC_401_761,(0,0,9):C.R2GC_401_762,(0,0,5):C.R2GC_401_763,(0,1,0):C.R2GC_402_764,(0,1,1):C.R2GC_402_765,(0,1,2):C.R2GC_402_766,(0,1,3):C.R2GC_402_767,(0,1,4):C.R2GC_402_768,(0,1,6):C.R2GC_402_769,(0,1,7):C.R2GC_402_770,(0,1,8):C.R2GC_402_771,(0,1,9):C.R2GC_402_772,(0,1,5):C.R2GC_402_773})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_435_1068,(0,0,2):C.R2GC_435_1069,(0,0,3):C.R2GC_435_1070,(0,0,4):C.R2GC_435_1071,(0,0,5):C.R2GC_435_1072,(0,0,8):C.R2GC_435_1073,(0,0,12):C.R2GC_435_1074,(0,0,15):C.R2GC_435_1075,(0,0,16):C.R2GC_435_1076,(0,0,17):C.R2GC_435_1077,(0,0,0):C.R2GC_435_1078,(0,0,7):C.R2GC_435_1079,(0,0,9):C.R2GC_435_1080,(0,0,10):C.R2GC_435_1081,(0,0,11):C.R2GC_435_1082,(0,0,13):C.R2GC_435_1083,(0,0,14):C.R2GC_435_1084,(0,0,6):C.R2GC_435_1085})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_434_1050,(0,0,2):C.R2GC_434_1051,(0,0,3):C.R2GC_434_1052,(0,0,4):C.R2GC_434_1053,(0,0,5):C.R2GC_434_1054,(0,0,11):C.R2GC_434_1055,(0,0,13):C.R2GC_434_1056,(0,0,15):C.R2GC_434_1057,(0,0,16):C.R2GC_434_1058,(0,0,17):C.R2GC_434_1059,(0,0,0):C.R2GC_434_1060,(0,0,7):C.R2GC_434_1061,(0,0,8):C.R2GC_434_1062,(0,0,9):C.R2GC_434_1063,(0,0,10):C.R2GC_434_1064,(0,0,12):C.R2GC_434_1065,(0,0,14):C.R2GC_434_1066,(0,0,6):C.R2GC_434_1067})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_422_954,(0,0,2):C.R2GC_422_955,(0,0,3):C.R2GC_422_956,(0,0,4):C.R2GC_422_957,(0,0,6):C.R2GC_422_958,(0,0,8):C.R2GC_422_959,(0,0,0):C.R2GC_422_960,(0,0,5):C.R2GC_422_961,(0,0,7):C.R2GC_422_962})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_435_1068,(0,0,2):C.R2GC_435_1069,(0,0,3):C.R2GC_435_1070,(0,0,4):C.R2GC_435_1071,(0,0,5):C.R2GC_435_1072,(0,0,8):C.R2GC_435_1073,(0,0,12):C.R2GC_435_1074,(0,0,15):C.R2GC_435_1075,(0,0,16):C.R2GC_435_1076,(0,0,17):C.R2GC_435_1077,(0,0,0):C.R2GC_435_1078,(0,0,7):C.R2GC_435_1079,(0,0,9):C.R2GC_435_1080,(0,0,10):C.R2GC_435_1081,(0,0,11):C.R2GC_435_1082,(0,0,13):C.R2GC_435_1083,(0,0,14):C.R2GC_435_1084,(0,0,6):C.R2GC_435_1085})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_434_1059,(0,0,2):C.R2GC_436_1086,(0,0,3):C.R2GC_436_1087,(0,0,4):C.R2GC_436_1088,(0,0,5):C.R2GC_436_1089,(0,0,11):C.R2GC_434_1056,(0,0,13):C.R2GC_434_1055,(0,0,15):C.R2GC_436_1090,(0,0,16):C.R2GC_436_1091,(0,0,17):C.R2GC_434_1050,(0,0,0):C.R2GC_436_1092,(0,0,7):C.R2GC_434_1064,(0,0,8):C.R2GC_436_1093,(0,0,9):C.R2GC_436_1094,(0,0,10):C.R2GC_434_1061,(0,0,12):C.R2GC_436_1095,(0,0,14):C.R2GC_436_1096,(0,0,6):C.R2GC_436_1097})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_422_959,(0,0,2):C.R2GC_427_985,(0,0,3):C.R2GC_427_986,(0,0,4):C.R2GC_427_987,(0,0,6):C.R2GC_427_988,(0,0,8):C.R2GC_422_954,(0,0,0):C.R2GC_427_989,(0,0,5):C.R2GC_427_990,(0,0,7):C.R2GC_427_991})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV10, L.VVVV7, L.VVVV8, L.VVVV9 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,2,3):C.R2GC_344_440,(0,2,0):C.R2GC_344_441,(0,2,1):C.R2GC_344_442,(0,2,2):C.R2GC_344_443,(0,2,4):C.R2GC_344_444,(0,3,3):C.R2GC_342_431,(0,3,0):C.R2GC_342_432,(0,3,1):C.R2GC_342_433,(0,3,2):C.R2GC_342_434,(0,3,4):C.R2GC_342_435,(0,0,3):C.R2GC_342_431,(0,0,0):C.R2GC_342_432,(0,0,1):C.R2GC_342_433,(0,0,2):C.R2GC_342_434,(0,0,4):C.R2GC_342_435,(0,1,1):C.R2GC_127_57,(0,1,2):C.R2GC_127_58})

V_66 = CTVertex(name = 'V_66',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_409_840,(0,0,1):C.R2GC_409_841,(0,0,2):C.R2GC_409_842,(0,0,3):C.R2GC_409_843,(0,0,7):C.R2GC_409_844,(0,0,8):C.R2GC_409_845,(0,0,9):C.R2GC_409_846,(0,0,10):C.R2GC_409_847,(0,0,11):C.R2GC_409_848,(0,0,12):C.R2GC_404_783,(0,0,5):C.R2GC_409_849,(0,0,6):C.R2GC_409_850,(0,0,4):C.R2GC_121_39})

V_67 = CTVertex(name = 'V_67',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,10):C.R2GC_404_783,(0,0,0):C.R2GC_311_346,(0,0,1):C.R2GC_404_784,(0,0,2):C.R2GC_404_785,(0,0,3):C.R2GC_404_786,(0,0,4):C.R2GC_404_787,(0,0,6):C.R2GC_404_788,(0,0,7):C.R2GC_404_789,(0,0,8):C.R2GC_404_790,(0,0,9):C.R2GC_404_791,(0,0,5):C.R2GC_404_792})

V_68 = CTVertex(name = 'V_68',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS2 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_409_840,(0,0,1):C.R2GC_409_841,(0,0,2):C.R2GC_409_842,(0,0,3):C.R2GC_409_843,(0,0,7):C.R2GC_409_844,(0,0,8):C.R2GC_409_845,(0,0,9):C.R2GC_409_846,(0,0,10):C.R2GC_409_847,(0,0,11):C.R2GC_409_848,(0,0,12):C.R2GC_404_783,(0,0,5):C.R2GC_409_850,(0,0,6):C.R2GC_409_849,(0,0,4):C.R2GC_121_39})

V_69 = CTVertex(name = 'V_69',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS2 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_406_804,(0,0,1):C.R2GC_406_805,(0,0,2):C.R2GC_406_806,(0,0,3):C.R2GC_406_807,(0,0,5):C.R2GC_406_808,(0,0,6):C.R2GC_406_809,(0,0,7):C.R2GC_406_810,(0,0,8):C.R2GC_406_811,(0,0,9):C.R2GC_406_812,(0,0,10):C.R2GC_406_813,(0,0,4):C.R2GC_406_814})

V_70 = CTVertex(name = 'V_70',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,1,3):C.R2GC_343_436,(0,1,0):C.R2GC_326_387,(0,1,1):C.R2GC_343_437,(0,1,2):C.R2GC_343_438,(0,1,4):C.R2GC_343_439,(0,2,3):C.R2GC_343_436,(0,2,0):C.R2GC_326_387,(0,2,1):C.R2GC_343_437,(0,2,2):C.R2GC_343_438,(0,2,4):C.R2GC_343_439,(0,0,3):C.R2GC_345_445,(0,0,0):C.R2GC_327_392,(0,0,1):C.R2GC_345_446,(0,0,2):C.R2GC_345_447,(0,0,4):C.R2GC_345_448})

V_71 = CTVertex(name = 'V_71',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_272_171,(0,0,1):C.R2GC_272_172,(0,0,2):C.R2GC_286_189,(0,0,3):C.R2GC_286_190,(0,1,0):C.R2GC_272_171,(0,1,1):C.R2GC_272_172,(0,1,2):C.R2GC_272_173})

V_72 = CTVertex(name = 'V_72',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_272_171,(0,0,1):C.R2GC_273_174,(0,0,2):C.R2GC_286_189,(0,0,3):C.R2GC_286_190,(0,1,0):C.R2GC_272_171,(0,1,1):C.R2GC_273_174,(0,1,2):C.R2GC_272_173})

V_73 = CTVertex(name = 'V_73',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_272_171,(0,0,1):C.R2GC_274_175,(0,0,2):C.R2GC_286_189,(0,0,3):C.R2GC_286_190,(0,1,0):C.R2GC_272_171,(0,1,1):C.R2GC_274_175,(0,1,2):C.R2GC_272_173})

V_74 = CTVertex(name = 'V_74',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_238_127,(0,1,0):C.R2GC_269_165,(0,1,1):C.R2GC_285_188,(0,1,2):C.R2GC_283_186,(0,1,4):C.R2GC_269_166,(0,1,5):C.R2GC_283_184,(0,2,0):C.R2GC_269_165,(0,2,1):C.R2GC_271_170,(0,2,4):C.R2GC_269_166,(0,2,5):C.R2GC_269_167})

V_75 = CTVertex(name = 'V_75',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,2):C.R2GC_207_89,(0,1,0):C.R2GC_269_165,(0,1,1):C.R2GC_269_166,(0,1,3):C.R2GC_283_184,(0,1,4):C.R2GC_283_185,(0,1,5):C.R2GC_283_186,(0,2,0):C.R2GC_269_165,(0,2,1):C.R2GC_269_166,(0,2,3):C.R2GC_269_167,(0,2,4):C.R2GC_269_168})

V_76 = CTVertex(name = 'V_76',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_225_116,(0,1,0):C.R2GC_269_165,(0,1,1):C.R2GC_284_187,(0,1,2):C.R2GC_283_186,(0,1,4):C.R2GC_269_166,(0,1,5):C.R2GC_283_184,(0,2,0):C.R2GC_269_165,(0,2,1):C.R2GC_270_169,(0,2,4):C.R2GC_269_166,(0,2,5):C.R2GC_269_167})

V_77 = CTVertex(name = 'V_77',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_266_156,(0,0,1):C.R2GC_266_158,(0,0,2):C.R2GC_268_163,(0,0,3):C.R2GC_279_181,(0,0,4):C.R2GC_281_183,(0,0,5):C.R2GC_279_180,(0,1,0):C.R2GC_266_156,(0,1,1):C.R2GC_266_158,(0,1,2):C.R2GC_268_163,(0,1,3):C.R2GC_266_160,(0,1,4):C.R2GC_268_164})

V_78 = CTVertex(name = 'V_78',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_266_156,(0,0,1):C.R2GC_279_179,(0,0,2):C.R2GC_279_180,(0,0,4):C.R2GC_266_158,(0,0,3):C.R2GC_266_159,(0,0,5):C.R2GC_279_181,(0,1,0):C.R2GC_266_156,(0,1,1):C.R2GC_266_157,(0,1,4):C.R2GC_266_158,(0,1,3):C.R2GC_266_159,(0,1,5):C.R2GC_266_160})

V_79 = CTVertex(name = 'V_79',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_266_156,(0,0,1):C.R2GC_266_158,(0,0,2):C.R2GC_267_161,(0,0,3):C.R2GC_279_181,(0,0,4):C.R2GC_280_182,(0,0,5):C.R2GC_279_180,(0,1,0):C.R2GC_266_156,(0,1,1):C.R2GC_266_158,(0,1,2):C.R2GC_267_161,(0,1,3):C.R2GC_266_160,(0,1,4):C.R2GC_267_162})

V_80 = CTVertex(name = 'V_80',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_208_90,(0,0,4):C.R2GC_208_91,(0,0,3):C.R2GC_239_128,(0,1,1):C.R2GC_243_133,(0,1,2):C.R2GC_219_106,(0,1,5):C.R2GC_219_104,(0,2,1):C.R2GC_244_134,(0,2,5):C.R2GC_218_102})

V_81 = CTVertex(name = 'V_81',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_208_90,(0,0,1):C.R2GC_208_91,(0,0,2):C.R2GC_208_92,(0,1,3):C.R2GC_219_104,(0,1,4):C.R2GC_219_105,(0,1,5):C.R2GC_219_106,(0,2,3):C.R2GC_218_102,(0,2,4):C.R2GC_218_103})

V_82 = CTVertex(name = 'V_82',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_208_90,(0,0,4):C.R2GC_208_91,(0,0,3):C.R2GC_226_117,(0,1,1):C.R2GC_230_122,(0,1,2):C.R2GC_219_106,(0,1,5):C.R2GC_219_104,(0,2,1):C.R2GC_231_123,(0,2,5):C.R2GC_218_102})

V_83 = CTVertex(name = 'V_83',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_223_112,(0,0,1):C.R2GC_208_91,(0,0,2):C.R2GC_243_132,(0,0,3):C.R2GC_224_115,(0,0,4):C.R2GC_244_134,(0,0,5):C.R2GC_219_106,(0,1,0):C.R2GC_223_112,(0,1,1):C.R2GC_208_91,(0,1,2):C.R2GC_243_132,(0,1,3):C.R2GC_223_114,(0,1,4):C.R2GC_243_133})

V_84 = CTVertex(name = 'V_84',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_223_112,(0,0,1):C.R2GC_218_103,(0,0,2):C.R2GC_219_106,(0,0,4):C.R2GC_208_91,(0,0,3):C.R2GC_223_113,(0,0,5):C.R2GC_224_115,(0,1,0):C.R2GC_223_112,(0,1,1):C.R2GC_219_105,(0,1,4):C.R2GC_208_91,(0,1,3):C.R2GC_223_113,(0,1,5):C.R2GC_223_114})

V_85 = CTVertex(name = 'V_85',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_223_112,(0,0,1):C.R2GC_208_91,(0,0,2):C.R2GC_230_121,(0,0,3):C.R2GC_224_115,(0,0,4):C.R2GC_231_123,(0,0,5):C.R2GC_219_106,(0,1,0):C.R2GC_223_112,(0,1,1):C.R2GC_208_91,(0,1,2):C.R2GC_230_121,(0,1,3):C.R2GC_223_114,(0,1,4):C.R2GC_230_122})

V_86 = CTVertex(name = 'V_86',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_528,(0,0,2):C.R2GC_359_527,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_532,(0,0,8):C.R2GC_359_531,(0,1,3):C.R2GC_376_614,(0,1,5):C.R2GC_376_615})

V_87 = CTVertex(name = 'V_87',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_527,(0,0,2):C.R2GC_359_528,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_531,(0,0,8):C.R2GC_359_532,(0,1,3):C.R2GC_350_456,(0,1,5):C.R2GC_350_457})

V_88 = CTVertex(name = 'V_88',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_528,(0,0,2):C.R2GC_359_527,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_532,(0,0,8):C.R2GC_359_531,(0,1,3):C.R2GC_362_537,(0,1,5):C.R2GC_362_538})

V_89 = CTVertex(name = 'V_89',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_528,(0,0,2):C.R2GC_359_527,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_532,(0,0,8):C.R2GC_359_531,(0,1,3):C.R2GC_376_614,(0,1,5):C.R2GC_376_615})

V_90 = CTVertex(name = 'V_90',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_527,(0,0,2):C.R2GC_359_528,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_531,(0,0,8):C.R2GC_359_532,(0,1,3):C.R2GC_350_456,(0,1,5):C.R2GC_350_457})

V_91 = CTVertex(name = 'V_91',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_359_526,(0,0,1):C.R2GC_359_528,(0,0,2):C.R2GC_359_527,(0,0,4):C.R2GC_359_529,(0,0,6):C.R2GC_359_530,(0,0,7):C.R2GC_359_532,(0,0,8):C.R2GC_359_531,(0,1,3):C.R2GC_362_537,(0,1,5):C.R2GC_362_538})

V_92 = CTVertex(name = 'V_92',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_93 = CTVertex(name = 'V_93',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_94 = CTVertex(name = 'V_94',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_95 = CTVertex(name = 'V_95',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_96 = CTVertex(name = 'V_96',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_97 = CTVertex(name = 'V_97',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV5 ],
                loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_390_706,(0,0,1):C.R2GC_390_707,(0,0,2):C.R2GC_390_708,(0,0,3):C.R2GC_390_709})

V_98 = CTVertex(name = 'V_98',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_330_404,(0,0,1):C.R2GC_374_610,(0,0,2):C.R2GC_330_409,(0,0,4):C.R2GC_330_405,(0,0,3):C.R2GC_374_611,(0,0,5):C.R2GC_330_407,(0,1,0):C.R2GC_331_410,(0,1,1):C.R2GC_375_612,(0,1,4):C.R2GC_331_411,(0,1,3):C.R2GC_375_613,(0,1,5):C.R2GC_331_413})

V_99 = CTVertex(name = 'V_99',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_330_404,(0,0,1):C.R2GC_330_405,(0,0,2):C.R2GC_330_406,(0,0,3):C.R2GC_330_407,(0,0,4):C.R2GC_330_408,(0,0,5):C.R2GC_330_409,(0,1,0):C.R2GC_331_410,(0,1,1):C.R2GC_331_411,(0,1,2):C.R2GC_331_412,(0,1,3):C.R2GC_331_413,(0,1,4):C.R2GC_331_414})

V_100 = CTVertex(name = 'V_100',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_330_404,(0,0,1):C.R2GC_360_533,(0,0,2):C.R2GC_330_409,(0,0,4):C.R2GC_330_405,(0,0,3):C.R2GC_360_534,(0,0,5):C.R2GC_330_407,(0,1,0):C.R2GC_331_410,(0,1,1):C.R2GC_361_535,(0,1,4):C.R2GC_331_411,(0,1,3):C.R2GC_361_536,(0,1,5):C.R2GC_331_413})

V_101 = CTVertex(name = 'V_101',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_329_398,(0,0,1):C.R2GC_329_399,(0,0,2):C.R2GC_333_417,(0,0,3):C.R2GC_329_401,(0,0,4):C.R2GC_333_418,(0,0,5):C.R2GC_329_403,(0,1,0):C.R2GC_328_393,(0,1,1):C.R2GC_328_394,(0,1,2):C.R2GC_332_415,(0,1,3):C.R2GC_328_396,(0,1,4):C.R2GC_332_416})

V_102 = CTVertex(name = 'V_102',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_329_398,(0,0,1):C.R2GC_349_454,(0,0,2):C.R2GC_329_403,(0,0,4):C.R2GC_329_399,(0,0,3):C.R2GC_349_455,(0,0,5):C.R2GC_329_401,(0,1,0):C.R2GC_328_393,(0,1,1):C.R2GC_348_452,(0,1,4):C.R2GC_328_394,(0,1,3):C.R2GC_348_453,(0,1,5):C.R2GC_328_396})

V_103 = CTVertex(name = 'V_103',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_329_398,(0,0,1):C.R2GC_329_399,(0,0,2):C.R2GC_329_400,(0,0,3):C.R2GC_329_401,(0,0,4):C.R2GC_329_402,(0,0,5):C.R2GC_329_403,(0,1,0):C.R2GC_328_393,(0,1,1):C.R2GC_328_394,(0,1,2):C.R2GC_328_395,(0,1,3):C.R2GC_328_396,(0,1,4):C.R2GC_328_397})

V_104 = CTVertex(name = 'V_104',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_307_322,(0,0,1):C.R2GC_307_323,(0,0,2):C.R2GC_307_324})

V_105 = CTVertex(name = 'V_105',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_308_325,(0,0,1):C.R2GC_307_323,(0,0,2):C.R2GC_307_324})

V_106 = CTVertex(name = 'V_106',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_309_326,(0,0,1):C.R2GC_307_323,(0,0,2):C.R2GC_307_324})

V_107 = CTVertex(name = 'V_107',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_335_423,(0,0,1):C.R2GC_335_424,(0,0,2):C.R2GC_335_425,(0,0,4):C.R2GC_335_426,(0,1,0):C.R2GC_334_419,(0,1,1):C.R2GC_334_420,(0,1,2):C.R2GC_334_421,(0,1,3):C.R2GC_334_422})

V_108 = CTVertex(name = 'V_108',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_335_423,(0,0,1):C.R2GC_347_451,(0,0,3):C.R2GC_335_425,(0,0,4):C.R2GC_335_426,(0,1,0):C.R2GC_334_419,(0,1,1):C.R2GC_346_449,(0,1,2):C.R2GC_346_450,(0,1,3):C.R2GC_334_421})

V_109 = CTVertex(name = 'V_109',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_335_423,(0,0,1):C.R2GC_373_609,(0,0,3):C.R2GC_335_425,(0,0,4):C.R2GC_335_426,(0,1,0):C.R2GC_334_419,(0,1,1):C.R2GC_372_607,(0,1,2):C.R2GC_372_608,(0,1,3):C.R2GC_334_421})

V_110 = CTVertex(name = 'V_110',
                 type = 'R2',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S2 ],
                 loop_particles = [ [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_205_86,(0,0,1):C.R2GC_205_87})

V_111 = CTVertex(name = 'V_111',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.R2GC_251_139,(0,2,1):C.R2GC_251_140,(0,4,0):C.R2GC_251_139,(0,4,1):C.R2GC_251_140,(0,3,1):C.R2GC_252_141,(0,3,2):C.R2GC_217_101,(0,0,1):C.R2GC_250_138,(0,1,0):C.R2GC_210_93})

V_112 = CTVertex(name = 'V_112',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_217_101,(0,0,1):C.R2GC_253_142})

V_113 = CTVertex(name = 'V_113',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.R2GC_255_143,(0,2,1):C.R2GC_255_144,(0,4,0):C.R2GC_255_143,(0,4,1):C.R2GC_255_144,(0,3,1):C.R2GC_252_141,(0,3,2):C.R2GC_217_101,(0,0,1):C.R2GC_250_138,(0,1,0):C.R2GC_210_93})

V_114 = CTVertex(name = 'V_114',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_217_101,(0,0,1):C.R2GC_253_142})

V_115 = CTVertex(name = 'V_115',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.R2GC_259_145,(0,2,1):C.R2GC_259_146,(0,4,0):C.R2GC_259_145,(0,4,1):C.R2GC_259_146,(0,3,1):C.R2GC_252_141,(0,3,2):C.R2GC_217_101,(0,0,1):C.R2GC_250_138,(0,1,0):C.R2GC_210_93})

V_116 = CTVertex(name = 'V_116',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_217_101,(0,0,1):C.R2GC_253_142})

V_117 = CTVertex(name = 'V_117',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.W__plus__] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,1,0):C.R2GC_245_135,(0,1,2):C.R2GC_245_136,(0,1,3):C.R2GC_245_137,(0,3,0):C.R2GC_245_135,(0,3,2):C.R2GC_245_136,(0,3,3):C.R2GC_245_137,(0,2,0):C.R2GC_215_94,(0,2,1):C.R2GC_217_101,(0,2,2):C.R2GC_215_95,(0,2,3):C.R2GC_217_100,(0,0,0):C.R2GC_215_94,(0,0,2):C.R2GC_215_95,(0,0,3):C.R2GC_215_96})

V_118 = CTVertex(name = 'V_118',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.Z] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.R2GC_240_129,(0,2,1):C.R2GC_240_130,(0,2,2):C.R2GC_240_131,(0,4,0):C.R2GC_240_129,(0,4,1):C.R2GC_240_130,(0,4,2):C.R2GC_240_131,(0,3,1):C.R2GC_215_95,(0,3,2):C.R2GC_222_111,(0,3,3):C.R2GC_217_101,(0,0,1):C.R2GC_215_95,(0,0,2):C.R2GC_220_107,(0,1,0):C.R2GC_206_88})

V_119 = CTVertex(name = 'V_119',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.Z] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_216_97,(0,1,1):C.R2GC_216_98,(0,1,2):C.R2GC_216_99,(0,3,0):C.R2GC_216_97,(0,3,1):C.R2GC_216_98,(0,3,2):C.R2GC_216_99,(0,2,0):C.R2GC_215_94,(0,2,1):C.R2GC_215_95,(0,2,2):C.R2GC_217_100,(0,2,3):C.R2GC_217_101,(0,0,0):C.R2GC_215_94,(0,0,1):C.R2GC_215_95,(0,0,2):C.R2GC_215_96})

V_120 = CTVertex(name = 'V_120',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.W__plus__] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,2,0):C.R2GC_221_108,(0,2,2):C.R2GC_221_109,(0,2,3):C.R2GC_221_110,(0,4,0):C.R2GC_221_108,(0,4,2):C.R2GC_221_109,(0,4,3):C.R2GC_221_110,(0,3,1):C.R2GC_217_101,(0,3,2):C.R2GC_215_95,(0,3,3):C.R2GC_222_111,(0,0,2):C.R2GC_215_95,(0,0,3):C.R2GC_220_107,(0,1,0):C.R2GC_206_88})

V_121 = CTVertex(name = 'V_121',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.W__plus__] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,1,0):C.R2GC_234_124,(0,1,2):C.R2GC_234_125,(0,1,3):C.R2GC_234_126,(0,3,0):C.R2GC_234_124,(0,3,2):C.R2GC_234_125,(0,3,3):C.R2GC_234_126,(0,2,0):C.R2GC_215_94,(0,2,1):C.R2GC_217_101,(0,2,2):C.R2GC_215_95,(0,2,3):C.R2GC_217_100,(0,0,0):C.R2GC_215_94,(0,0,2):C.R2GC_215_95,(0,0,3):C.R2GC_215_96})

V_122 = CTVertex(name = 'V_122',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.Z] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.R2GC_228_118,(0,2,1):C.R2GC_228_119,(0,2,2):C.R2GC_228_120,(0,4,0):C.R2GC_228_118,(0,4,1):C.R2GC_228_119,(0,4,2):C.R2GC_228_120,(0,3,1):C.R2GC_215_95,(0,3,2):C.R2GC_222_111,(0,3,3):C.R2GC_217_101,(0,0,1):C.R2GC_215_95,(0,0,2):C.R2GC_220_107,(0,1,0):C.R2GC_206_88})

V_123 = CTVertex(name = 'V_123',
                 type = 'R2',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS6 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_298_266,(0,0,1):C.R2GC_298_267,(0,0,2):C.R2GC_298_268,(0,0,3):C.R2GC_298_269,(0,0,6):C.R2GC_298_270,(0,0,7):C.R2GC_298_271,(0,0,8):C.R2GC_298_272,(0,0,9):C.R2GC_298_273,(0,0,10):C.R2GC_298_274,(0,0,11):C.R2GC_298_275,(0,0,12):C.R2GC_298_276,(0,0,4):C.R2GC_298_277,(0,0,5):C.R2GC_298_278,(0,1,0):C.R2GC_297_255,(0,1,1):C.R2GC_297_256,(0,1,2):C.R2GC_297_257,(0,1,3):C.R2GC_297_258,(0,1,6):C.R2GC_297_259,(0,1,7):C.R2GC_297_260,(0,1,8):C.R2GC_297_261,(0,1,9):C.R2GC_297_262,(0,1,10):C.R2GC_297_263,(0,1,4):C.R2GC_297_264,(0,1,5):C.R2GC_297_265})

V_124 = CTVertex(name = 'V_124',
                 type = 'R2',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS6 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_298_266,(0,0,1):C.R2GC_298_267,(0,0,2):C.R2GC_298_268,(0,0,3):C.R2GC_298_269,(0,0,6):C.R2GC_298_270,(0,0,7):C.R2GC_298_271,(0,0,8):C.R2GC_298_272,(0,0,9):C.R2GC_298_273,(0,0,10):C.R2GC_298_274,(0,0,11):C.R2GC_302_285,(0,0,12):C.R2GC_302_286,(0,0,4):C.R2GC_298_278,(0,0,5):C.R2GC_302_287,(0,1,0):C.R2GC_297_255,(0,1,1):C.R2GC_297_256,(0,1,2):C.R2GC_297_257,(0,1,3):C.R2GC_297_258,(0,1,6):C.R2GC_297_259,(0,1,7):C.R2GC_297_260,(0,1,8):C.R2GC_297_261,(0,1,9):C.R2GC_297_262,(0,1,10):C.R2GC_297_263,(0,1,4):C.R2GC_297_265,(0,1,5):C.R2GC_297_264})

V_125 = CTVertex(name = 'V_125',
                 type = 'R2',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,12):C.R2GC_302_285,(0,0,14):C.R2GC_314_350,(0,0,0):C.R2GC_314_351,(0,0,1):C.R2GC_314_352,(0,0,2):C.R2GC_314_353,(0,0,3):C.R2GC_314_354,(0,0,4):C.R2GC_314_355,(0,0,5):C.R2GC_314_356,(0,0,6):C.R2GC_314_357,(0,0,8):C.R2GC_314_358,(0,0,9):C.R2GC_314_359,(0,0,10):C.R2GC_314_360,(0,0,11):C.R2GC_314_361,(0,0,13):C.R2GC_314_362,(0,1,0):C.R2GC_304_298,(0,1,2):C.R2GC_304_299,(0,1,3):C.R2GC_304_300,(0,1,4):C.R2GC_304_301,(0,1,5):C.R2GC_297_258,(0,1,7):C.R2GC_304_302,(0,1,8):C.R2GC_304_303,(0,1,10):C.R2GC_297_259,(0,1,11):C.R2GC_297_262})

V_126 = CTVertex(name = 'V_126',
                 type = 'R2',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,12):C.R2GC_265_155,(0,2,0):C.R2GC_291_201,(0,2,2):C.R2GC_291_202,(0,2,4):C.R2GC_291_203,(0,2,5):C.R2GC_291_204,(0,2,7):C.R2GC_291_205,(0,2,8):C.R2GC_291_206,(0,2,9):C.R2GC_291_207,(0,2,10):C.R2GC_291_208,(0,2,11):C.R2GC_291_209,(0,2,12):C.R2GC_291_210,(0,0,1):C.R2GC_264_152,(0,0,3):C.R2GC_264_153,(0,0,6):C.R2GC_264_154,(0,0,12):C.R2GC_210_93})

V_127 = CTVertex(name = 'V_127',
                 type = 'R2',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,12):C.R2GC_263_151,(0,2,0):C.R2GC_290_191,(0,2,2):C.R2GC_290_192,(0,2,4):C.R2GC_290_193,(0,2,5):C.R2GC_290_194,(0,2,7):C.R2GC_290_195,(0,2,8):C.R2GC_290_196,(0,2,9):C.R2GC_290_197,(0,2,10):C.R2GC_290_198,(0,2,11):C.R2GC_290_199,(0,2,12):C.R2GC_290_200,(0,0,1):C.R2GC_262_147,(0,0,3):C.R2GC_262_148,(0,0,6):C.R2GC_262_149,(0,0,12):C.R2GC_262_150})

V_128 = CTVertex(name = 'V_128',
                 type = 'R2',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,13):C.R2GC_300_284,(0,2,0):C.R2GC_303_288,(0,2,2):C.R2GC_303_289,(0,2,4):C.R2GC_303_290,(0,2,5):C.R2GC_303_291,(0,2,7):C.R2GC_303_292,(0,2,8):C.R2GC_303_293,(0,2,9):C.R2GC_303_294,(0,2,10):C.R2GC_303_295,(0,2,11):C.R2GC_303_296,(0,2,13):C.R2GC_303_297,(0,0,1):C.R2GC_299_279,(0,0,3):C.R2GC_299_280,(0,0,6):C.R2GC_299_281,(0,0,12):C.R2GC_299_282,(0,0,13):C.R2GC_299_283})

V_129 = CTVertex(name = 'V_129',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV6, L.VV8, L.VV9 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_265_155,(0,0,10):C.R2GC_300_284,(0,1,9):C.R2GC_315_363,(0,1,11):C.R2GC_315_364,(0,1,0):C.R2GC_315_365,(0,1,1):C.R2GC_315_366,(0,1,3):C.R2GC_315_367,(0,1,4):C.R2GC_315_368,(0,1,5):C.R2GC_315_369,(0,1,7):C.R2GC_315_370,(0,1,8):C.R2GC_315_371,(0,1,10):C.R2GC_315_372,(0,2,0):C.R2GC_210_93,(0,2,2):C.R2GC_217_101,(0,2,6):C.R2GC_312_349,(0,2,10):C.R2GC_299_283})

V_130 = CTVertex(name = 'V_130',
                 type = 'R2',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,1,4):C.R2GC_167_68,(0,2,0):C.R2GC_113_6,(0,2,2):C.R2GC_113_7,(0,2,3):C.R2GC_113_8,(0,2,5):C.R2GC_113_9,(0,2,6):C.R2GC_113_10,(0,2,7):C.R2GC_113_11,(0,0,1):C.R2GC_168_69,(0,0,4):C.R2GC_168_70})

V_131 = CTVertex(name = 'V_131',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_276_176})

V_132 = CTVertex(name = 'V_132',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_277_177})

V_133 = CTVertex(name = 'V_133',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_278_178})

V_134 = CTVertex(name = 'V_134',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_293_222,(0,0,1):C.R2GC_293_223,(0,0,2):C.R2GC_293_224,(0,0,3):C.R2GC_293_225,(0,0,5):C.R2GC_293_226,(0,0,6):C.R2GC_293_227,(0,0,7):C.R2GC_293_228,(0,0,8):C.R2GC_293_229,(0,0,9):C.R2GC_293_230,(0,0,10):C.R2GC_293_231,(0,0,4):C.R2GC_293_232})

V_135 = CTVertex(name = 'V_135',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_292_211,(0,0,1):C.R2GC_292_212,(0,0,2):C.R2GC_292_213,(0,0,3):C.R2GC_292_214,(0,0,5):C.R2GC_292_215,(0,0,6):C.R2GC_292_216,(0,0,7):C.R2GC_292_217,(0,0,8):C.R2GC_292_218,(0,0,9):C.R2GC_292_219,(0,0,10):C.R2GC_292_220,(0,0,4):C.R2GC_292_221})

V_136 = CTVertex(name = 'V_136',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_118_20,(0,0,1):C.R2GC_118_21,(0,0,2):C.R2GC_118_22,(0,0,3):C.R2GC_118_23,(0,0,4):C.R2GC_118_24,(0,0,5):C.R2GC_118_25})

V_137 = CTVertex(name = 'V_137',
                 type = 'R2',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS6 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_110_1})

V_138 = CTVertex(name = 'V_138',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_120_32,(0,0,1):C.R2GC_120_33,(0,0,2):C.R2GC_120_34,(0,0,3):C.R2GC_120_35})

V_139 = CTVertex(name = 'V_139',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_124_49,(0,0,1):C.R2GC_124_50,(0,0,2):C.R2GC_124_51,(0,0,3):C.R2GC_124_52})

V_140 = CTVertex(name = 'V_140',
                 type = 'R2',
                 particles = [ P.a, P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_123_45,(0,0,1):C.R2GC_123_46,(0,0,2):C.R2GC_123_47,(0,0,3):C.R2GC_123_48})

V_141 = CTVertex(name = 'V_141',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_122_41,(0,0,1):C.R2GC_122_42,(0,0,2):C.R2GC_122_43,(0,0,3):C.R2GC_122_44})

V_142 = CTVertex(name = 'V_142',
                 type = 'R2',
                 particles = [ P.Z, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_121_36,(0,0,1):C.R2GC_121_37,(0,0,2):C.R2GC_121_38,(0,0,3):C.R2GC_121_39,(0,0,4):C.R2GC_121_40})

V_143 = CTVertex(name = 'V_143',
                 type = 'R2',
                 particles = [ P.a, P.a, P.g, P.g ],
                 color = [ 'Identity(3,4)' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_111_2,(0,0,1):C.R2GC_111_3})

V_144 = CTVertex(name = 'V_144',
                 type = 'R2',
                 particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_125_53})

V_145 = CTVertex(name = 'V_145',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.Z ],
                 color = [ 'Identity(2,3)' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_114_12,(0,0,1):C.R2GC_114_13})

V_146 = CTVertex(name = 'V_146',
                 type = 'R2',
                 particles = [ P.g, P.g, P.Z, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_117_18,(0,0,1):C.R2GC_117_19})

V_147 = CTVertex(name = 'V_147',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.g ],
                 color = [ 'd(2,3,4)' ],
                 lorentz = [ L.VVVV11 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_112_4,(0,0,1):C.R2GC_112_5})

V_148 = CTVertex(name = 'V_148',
                 type = 'R2',
                 particles = [ P.g, P.g, P.g, P.Z ],
                 color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                 lorentz = [ L.VVVV11, L.VVVV7 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(1,1,0):C.R2GC_116_16,(1,1,1):C.R2GC_116_17,(0,0,0):C.R2GC_115_14,(0,0,1):C.R2GC_115_15})

V_149 = CTVertex(name = 'V_149',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_296_244,(0,0,1):C.R2GC_296_245,(0,0,2):C.R2GC_296_246,(0,0,3):C.R2GC_296_247,(0,0,5):C.R2GC_296_248,(0,0,6):C.R2GC_296_249,(0,0,7):C.R2GC_296_250,(0,0,8):C.R2GC_296_251,(0,0,9):C.R2GC_296_252,(0,0,10):C.R2GC_296_253,(0,0,4):C.R2GC_296_254})

V_150 = CTVertex(name = 'V_150',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_295_233,(0,0,1):C.R2GC_295_234,(0,0,2):C.R2GC_295_235,(0,0,3):C.R2GC_295_236,(0,0,5):C.R2GC_295_237,(0,0,6):C.R2GC_295_238,(0,0,7):C.R2GC_295_239,(0,0,8):C.R2GC_295_240,(0,0,9):C.R2GC_295_241,(0,0,10):C.R2GC_295_242,(0,0,4):C.R2GC_295_243})

V_151 = CTVertex(name = 'V_151',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_119_26,(0,0,1):C.R2GC_119_27,(0,0,2):C.R2GC_119_28,(0,0,3):C.R2GC_119_29,(0,0,4):C.R2GC_119_30,(0,0,5):C.R2GC_119_31})

V_152 = CTVertex(name = 'V_152',
                 type = 'R2',
                 particles = [ P.a, P.a, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_296_244,(0,0,1):C.R2GC_296_245,(0,0,2):C.R2GC_296_246,(0,0,3):C.R2GC_296_247,(0,0,5):C.R2GC_296_248,(0,0,6):C.R2GC_296_249,(0,0,7):C.R2GC_296_250,(0,0,8):C.R2GC_296_251,(0,0,9):C.R2GC_296_252,(0,0,10):C.R2GC_296_253,(0,0,4):C.R2GC_296_254})

V_153 = CTVertex(name = 'V_153',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_295_233,(0,0,1):C.R2GC_295_234,(0,0,2):C.R2GC_295_235,(0,0,3):C.R2GC_295_236,(0,0,5):C.R2GC_295_237,(0,0,6):C.R2GC_295_238,(0,0,7):C.R2GC_295_239,(0,0,8):C.R2GC_295_240,(0,0,9):C.R2GC_295_241,(0,0,10):C.R2GC_295_242,(0,0,4):C.R2GC_295_243})

V_154 = CTVertex(name = 'V_154',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G0, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_119_26,(0,0,1):C.R2GC_119_27,(0,0,2):C.R2GC_119_28,(0,0,3):C.R2GC_119_29,(0,0,4):C.R2GC_119_30,(0,0,5):C.R2GC_119_31})

V_155 = CTVertex(name = 'V_155',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_429_1008,(0,0,8):C.R2GC_429_1009,(0,0,0):C.R2GC_429_1010,(0,0,1):C.R2GC_429_1011,(0,0,2):C.R2GC_429_1012,(0,0,3):C.R2GC_429_1013,(0,0,4):C.R2GC_429_1014,(0,0,6):C.R2GC_429_1015,(0,0,7):C.R2GC_429_1016,(0,0,9):C.R2GC_429_1017})

V_156 = CTVertex(name = 'V_156',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_126_54,(0,0,1):C.R2GC_126_55,(0,0,2):C.R2GC_126_56})

V_157 = CTVertex(name = 'V_157',
                 type = 'R2',
                 particles = [ P.W__plus__, P.W__plus__, P.G__minus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_429_1008,(0,0,8):C.R2GC_429_1009,(0,0,0):C.R2GC_429_1010,(0,0,1):C.R2GC_429_1011,(0,0,2):C.R2GC_429_1012,(0,0,3):C.R2GC_429_1013,(0,0,4):C.R2GC_429_1014,(0,0,6):C.R2GC_429_1015,(0,0,7):C.R2GC_429_1016,(0,0,9):C.R2GC_429_1017})

V_158 = CTVertex(name = 'V_158',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_200_306,(0,0,1):C.UVGC_200_307,(0,0,2):C.UVGC_200_308,(0,0,3):C.UVGC_200_309,(0,0,4):C.UVGC_200_310,(0,0,5):C.UVGC_200_311,(0,0,6):C.UVGC_200_312,(0,0,7):C.UVGC_200_313,(0,0,8):C.UVGC_200_314,(0,0,9):C.UVGC_200_315})

V_159 = CTVertex(name = 'V_159',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_198_286,(0,0,1):C.UVGC_198_287,(0,0,2):C.UVGC_198_288,(0,0,3):C.UVGC_198_289,(0,0,4):C.UVGC_198_290,(0,0,5):C.UVGC_198_291,(0,0,6):C.UVGC_198_292,(0,0,7):C.UVGC_198_293,(0,0,8):C.UVGC_198_294,(0,0,9):C.UVGC_198_295})

V_160 = CTVertex(name = 'V_160',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_199_296,(0,0,1):C.UVGC_199_297,(0,0,2):C.UVGC_199_298,(0,0,3):C.UVGC_199_299,(0,0,4):C.UVGC_199_300,(0,0,5):C.UVGC_199_301,(0,0,6):C.UVGC_199_302,(0,0,7):C.UVGC_199_303,(0,0,8):C.UVGC_199_304,(0,0,9):C.UVGC_199_305})

V_161 = CTVertex(name = 'V_161',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_198_286,(0,0,1):C.UVGC_198_287,(0,0,2):C.UVGC_198_288,(0,0,3):C.UVGC_198_289,(0,0,4):C.UVGC_198_290,(0,0,5):C.UVGC_198_291,(0,0,6):C.UVGC_198_292,(0,0,7):C.UVGC_198_293,(0,0,8):C.UVGC_198_294,(0,0,9):C.UVGC_198_295})

V_162 = CTVertex(name = 'V_162',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_198_286,(0,0,1):C.UVGC_198_287,(0,0,2):C.UVGC_198_288,(0,0,3):C.UVGC_198_289,(0,0,4):C.UVGC_198_290,(0,0,5):C.UVGC_198_291,(0,0,6):C.UVGC_198_292,(0,0,7):C.UVGC_198_293,(0,0,8):C.UVGC_198_294,(0,0,9):C.UVGC_198_295})

V_163 = CTVertex(name = 'V_163',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_200_306,(0,0,1):C.UVGC_200_307,(0,0,2):C.UVGC_200_308,(0,0,3):C.UVGC_200_309,(0,0,4):C.UVGC_200_310,(0,0,5):C.UVGC_200_311,(0,0,6):C.UVGC_200_312,(0,0,7):C.UVGC_200_313,(0,0,8):C.UVGC_200_314,(0,0,9):C.UVGC_200_315})

V_164 = CTVertex(name = 'V_164',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_407_3958,(0,0,4):C.UVGC_407_3959,(0,0,6):C.UVGC_407_3960,(0,0,8):C.UVGC_407_3961,(0,0,10):C.UVGC_407_3962,(0,0,16):C.UVGC_407_3963,(0,0,18):C.UVGC_407_3964,(0,0,19):C.UVGC_407_3965,(0,0,23):C.UVGC_407_3966,(0,0,26):C.UVGC_407_3967,(0,0,28):C.UVGC_407_3968,(0,0,29):C.UVGC_407_3969,(0,0,30):C.UVGC_407_3970,(0,0,32):C.UVGC_407_3971,(0,0,33):C.UVGC_407_3972,(0,0,34):C.UVGC_407_3973,(0,0,36):C.UVGC_407_3974,(0,0,0):C.UVGC_407_3975,(0,0,1):C.UVGC_407_3976,(0,0,3):C.UVGC_407_3977,(0,0,5):C.UVGC_407_3978,(0,0,7):C.UVGC_407_3979,(0,0,9):C.UVGC_407_3980,(0,0,11):C.UVGC_407_3981,(0,0,12):C.UVGC_407_3982,(0,0,14):C.UVGC_407_3983,(0,0,15):C.UVGC_407_3984,(0,0,17):C.UVGC_407_3985,(0,0,20):C.UVGC_407_3986,(0,0,21):C.UVGC_407_3987,(0,0,22):C.UVGC_407_3988,(0,0,24):C.UVGC_407_3989,(0,0,25):C.UVGC_407_3990,(0,0,27):C.UVGC_407_3991,(0,0,31):C.UVGC_407_3992,(0,0,35):C.UVGC_407_3993,(0,0,13):C.UVGC_407_3994})

V_165 = CTVertex(name = 'V_165',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_414_4174,(0,0,5):C.UVGC_414_4175,(0,0,7):C.UVGC_414_4176,(0,0,9):C.UVGC_414_4177,(0,0,11):C.UVGC_414_4178,(0,0,18):C.UVGC_414_4179,(0,0,20):C.UVGC_407_3964,(0,0,21):C.UVGC_414_4180,(0,0,27):C.UVGC_407_3966,(0,0,30):C.UVGC_414_4181,(0,0,32):C.UVGC_414_4182,(0,0,33):C.UVGC_414_4183,(0,0,34):C.UVGC_414_4184,(0,0,36):C.UVGC_414_4185,(0,0,37):C.UVGC_407_3972,(0,0,38):C.UVGC_407_3973,(0,0,40):C.UVGC_414_4186,(0,0,0):C.UVGC_414_4187,(0,0,2):C.UVGC_414_4188,(0,0,4):C.UVGC_414_4189,(0,0,6):C.UVGC_414_4190,(0,0,8):C.UVGC_414_4191,(0,0,10):C.UVGC_414_4192,(0,0,12):C.UVGC_407_3981,(0,0,13):C.UVGC_414_4193,(0,0,14):C.UVGC_414_4194,(0,0,16):C.UVGC_407_3983,(0,0,17):C.UVGC_407_3984,(0,0,19):C.UVGC_414_4195,(0,0,22):C.UVGC_414_4196,(0,0,24):C.UVGC_414_4197,(0,0,26):C.UVGC_414_4198,(0,0,28):C.UVGC_414_4199,(0,0,29):C.UVGC_414_4200,(0,0,31):C.UVGC_414_4201,(0,0,35):C.UVGC_414_4202,(0,0,39):C.UVGC_414_4203,(0,0,1):C.UVGC_414_4204,(0,0,15):C.UVGC_414_4205,(0,0,23):C.UVGC_414_4206,(0,0,25):C.UVGC_414_4207})

V_166 = CTVertex(name = 'V_166',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_310_1044,(0,0,4):C.UVGC_310_1045,(0,0,6):C.UVGC_310_1046,(0,0,8):C.UVGC_310_1047,(0,0,10):C.UVGC_310_1048,(0,0,15):C.UVGC_310_1049,(0,0,17):C.UVGC_310_1050,(0,0,18):C.UVGC_310_1051,(0,0,22):C.UVGC_310_1052,(0,0,25):C.UVGC_310_1053,(0,0,27):C.UVGC_310_1054,(0,0,28):C.UVGC_310_1055,(0,0,29):C.UVGC_310_1056,(0,0,31):C.UVGC_310_1057,(0,0,32):C.UVGC_310_1058,(0,0,33):C.UVGC_310_1059,(0,0,35):C.UVGC_310_1060,(0,0,0):C.UVGC_310_1061,(0,0,1):C.UVGC_310_1062,(0,0,3):C.UVGC_310_1063,(0,0,5):C.UVGC_310_1064,(0,0,7):C.UVGC_310_1065,(0,0,9):C.UVGC_310_1066,(0,0,11):C.UVGC_310_1067,(0,0,12):C.UVGC_310_1068,(0,0,13):C.UVGC_310_1069,(0,0,14):C.UVGC_310_1070,(0,0,16):C.UVGC_310_1071,(0,0,19):C.UVGC_310_1072,(0,0,20):C.UVGC_310_1073,(0,0,21):C.UVGC_310_1074,(0,0,23):C.UVGC_310_1075,(0,0,24):C.UVGC_310_1076,(0,0,26):C.UVGC_310_1077,(0,0,30):C.UVGC_310_1078,(0,0,34):C.UVGC_310_1079})

V_167 = CTVertex(name = 'V_167',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__], [P.u] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,1):C.UVGC_311_1080,(0,0,7):C.UVGC_311_1081,(0,0,9):C.UVGC_311_1082,(0,0,16):C.UVGC_311_1083,(0,0,0):C.UVGC_311_1084,(0,0,2):C.UVGC_311_1085,(0,0,3):C.UVGC_311_1086,(0,0,4):C.UVGC_311_1087,(0,0,5):C.UVGC_311_1088,(0,0,6):C.UVGC_311_1089,(0,0,8):C.UVGC_311_1090,(0,0,10):C.UVGC_311_1091,(0,0,11):C.UVGC_311_1092,(0,0,12):C.UVGC_311_1093,(0,0,13):C.UVGC_311_1094,(0,0,14):C.UVGC_311_1095,(0,0,15):C.UVGC_311_1096,(0,0,17):C.UVGC_311_1097})

V_168 = CTVertex(name = 'V_168',
                 type = 'UV',
                 particles = [ P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__], [P.u] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,1):C.UVGC_305_973,(0,0,7):C.UVGC_286_797,(0,0,9):C.UVGC_272_717,(0,0,16):C.UVGC_305_974,(0,0,0):C.UVGC_305_975,(0,0,2):C.UVGC_305_976,(0,0,3):C.UVGC_305_977,(0,0,4):C.UVGC_305_978,(0,0,5):C.UVGC_305_979,(0,0,6):C.UVGC_305_980,(0,0,8):C.UVGC_305_981,(0,0,10):C.UVGC_305_982,(0,0,11):C.UVGC_286_801,(0,0,12):C.UVGC_305_983,(0,0,13):C.UVGC_305_984,(0,0,14):C.UVGC_305_985,(0,0,15):C.UVGC_305_986,(0,0,17):C.UVGC_305_987,(0,1,1):C.UVGC_305_973,(0,1,7):C.UVGC_306_988,(0,1,9):C.UVGC_306_989,(0,1,16):C.UVGC_306_990,(0,1,0):C.UVGC_306_991,(0,1,2):C.UVGC_306_992,(0,1,3):C.UVGC_306_993,(0,1,4):C.UVGC_306_994,(0,1,5):C.UVGC_306_995,(0,1,6):C.UVGC_306_996,(0,1,8):C.UVGC_306_997,(0,1,10):C.UVGC_306_998,(0,1,11):C.UVGC_306_999,(0,1,12):C.UVGC_306_1000,(0,1,13):C.UVGC_306_1001,(0,1,14):C.UVGC_306_1002,(0,1,15):C.UVGC_306_1003,(0,1,17):C.UVGC_306_1004})

V_169 = CTVertex(name = 'V_169',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_189_196,(0,0,1):C.UVGC_189_197,(0,0,2):C.UVGC_189_198,(0,0,3):C.UVGC_189_199,(0,0,4):C.UVGC_189_200,(0,0,5):C.UVGC_189_201,(0,0,6):C.UVGC_189_202,(0,0,7):C.UVGC_189_203,(0,0,8):C.UVGC_189_204,(0,0,9):C.UVGC_189_205,(0,1,0):C.UVGC_189_196,(0,1,1):C.UVGC_189_197,(0,1,2):C.UVGC_189_198,(0,1,3):C.UVGC_189_199,(0,1,4):C.UVGC_189_200,(0,1,5):C.UVGC_189_201,(0,1,6):C.UVGC_189_202,(0,1,7):C.UVGC_189_203,(0,1,8):C.UVGC_189_204,(0,1,9):C.UVGC_189_205})

V_170 = CTVertex(name = 'V_170',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_188_186,(0,0,1):C.UVGC_188_187,(0,0,2):C.UVGC_188_188,(0,0,3):C.UVGC_188_189,(0,0,4):C.UVGC_188_190,(0,0,5):C.UVGC_188_191,(0,0,6):C.UVGC_188_192,(0,0,7):C.UVGC_188_193,(0,0,8):C.UVGC_188_194,(0,0,9):C.UVGC_188_195,(0,1,0):C.UVGC_188_186,(0,1,1):C.UVGC_188_187,(0,1,2):C.UVGC_188_188,(0,1,3):C.UVGC_188_189,(0,1,4):C.UVGC_188_190,(0,1,5):C.UVGC_188_191,(0,1,6):C.UVGC_188_192,(0,1,7):C.UVGC_188_193,(0,1,8):C.UVGC_188_194,(0,1,9):C.UVGC_188_195})

V_171 = CTVertex(name = 'V_171',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_185_156,(0,0,1):C.UVGC_185_157,(0,0,2):C.UVGC_185_158,(0,0,3):C.UVGC_185_159,(0,0,4):C.UVGC_185_160,(0,0,5):C.UVGC_185_161,(0,0,6):C.UVGC_185_162,(0,0,7):C.UVGC_185_163,(0,0,8):C.UVGC_185_164,(0,0,9):C.UVGC_185_165})

V_172 = CTVertex(name = 'V_172',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_189_196,(0,0,1):C.UVGC_189_197,(0,0,2):C.UVGC_189_198,(0,0,3):C.UVGC_189_199,(0,0,4):C.UVGC_189_200,(0,0,5):C.UVGC_189_201,(0,0,6):C.UVGC_189_202,(0,0,7):C.UVGC_189_203,(0,0,8):C.UVGC_189_204,(0,0,9):C.UVGC_189_205,(0,1,0):C.UVGC_189_196,(0,1,1):C.UVGC_189_197,(0,1,2):C.UVGC_189_198,(0,1,3):C.UVGC_189_199,(0,1,4):C.UVGC_189_200,(0,1,5):C.UVGC_189_201,(0,1,6):C.UVGC_189_202,(0,1,7):C.UVGC_189_203,(0,1,8):C.UVGC_189_204,(0,1,9):C.UVGC_189_205})

V_173 = CTVertex(name = 'V_173',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_196_266,(0,0,1):C.UVGC_196_267,(0,0,2):C.UVGC_196_268,(0,0,3):C.UVGC_196_269,(0,0,4):C.UVGC_196_270,(0,0,5):C.UVGC_196_271,(0,0,6):C.UVGC_196_272,(0,0,7):C.UVGC_196_273,(0,0,8):C.UVGC_196_274,(0,0,9):C.UVGC_196_275})

V_174 = CTVertex(name = 'V_174',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_192_226,(0,0,1):C.UVGC_192_227,(0,0,2):C.UVGC_192_228,(0,0,3):C.UVGC_192_229,(0,0,4):C.UVGC_192_230,(0,0,5):C.UVGC_192_231,(0,0,6):C.UVGC_192_232,(0,0,7):C.UVGC_192_233,(0,0,8):C.UVGC_192_234,(0,0,9):C.UVGC_192_235})

V_175 = CTVertex(name = 'V_175',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_188_186,(0,0,1):C.UVGC_188_187,(0,0,2):C.UVGC_188_188,(0,0,3):C.UVGC_188_189,(0,0,4):C.UVGC_188_190,(0,0,5):C.UVGC_188_191,(0,0,6):C.UVGC_188_192,(0,0,7):C.UVGC_188_193,(0,0,8):C.UVGC_188_194,(0,0,9):C.UVGC_188_195,(0,1,0):C.UVGC_188_186,(0,1,1):C.UVGC_188_187,(0,1,2):C.UVGC_188_188,(0,1,3):C.UVGC_188_189,(0,1,4):C.UVGC_188_190,(0,1,5):C.UVGC_188_191,(0,1,6):C.UVGC_188_192,(0,1,7):C.UVGC_188_193,(0,1,8):C.UVGC_188_194,(0,1,9):C.UVGC_188_195})

V_176 = CTVertex(name = 'V_176',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_190_206,(0,0,1):C.UVGC_190_207,(0,0,2):C.UVGC_190_208,(0,0,3):C.UVGC_190_209,(0,0,4):C.UVGC_190_210,(0,0,5):C.UVGC_190_211,(0,0,6):C.UVGC_190_212,(0,0,7):C.UVGC_190_213,(0,0,8):C.UVGC_190_214,(0,0,9):C.UVGC_190_215,(0,1,0):C.UVGC_190_206,(0,1,1):C.UVGC_190_207,(0,1,2):C.UVGC_190_208,(0,1,3):C.UVGC_190_209,(0,1,4):C.UVGC_190_210,(0,1,5):C.UVGC_190_211,(0,1,6):C.UVGC_190_212,(0,1,7):C.UVGC_190_213,(0,1,8):C.UVGC_190_214,(0,1,9):C.UVGC_190_215})

V_177 = CTVertex(name = 'V_177',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_186_166,(0,0,1):C.UVGC_186_167,(0,0,2):C.UVGC_186_168,(0,0,3):C.UVGC_186_169,(0,0,4):C.UVGC_186_170,(0,0,5):C.UVGC_186_171,(0,0,6):C.UVGC_186_172,(0,0,7):C.UVGC_186_173,(0,0,8):C.UVGC_186_174,(0,0,9):C.UVGC_186_175})

V_178 = CTVertex(name = 'V_178',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_191_216,(0,0,1):C.UVGC_191_217,(0,0,2):C.UVGC_191_218,(0,0,3):C.UVGC_191_219,(0,0,4):C.UVGC_191_220,(0,0,5):C.UVGC_191_221,(0,0,6):C.UVGC_191_222,(0,0,7):C.UVGC_191_223,(0,0,8):C.UVGC_191_224,(0,0,9):C.UVGC_191_225,(0,1,0):C.UVGC_191_216,(0,1,1):C.UVGC_191_217,(0,1,2):C.UVGC_191_218,(0,1,3):C.UVGC_191_219,(0,1,4):C.UVGC_191_220,(0,1,5):C.UVGC_191_221,(0,1,6):C.UVGC_191_222,(0,1,7):C.UVGC_191_223,(0,1,8):C.UVGC_191_224,(0,1,9):C.UVGC_191_225})

V_179 = CTVertex(name = 'V_179',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_195_256,(0,0,1):C.UVGC_195_257,(0,0,2):C.UVGC_195_258,(0,0,3):C.UVGC_195_259,(0,0,4):C.UVGC_195_260,(0,0,5):C.UVGC_195_261,(0,0,6):C.UVGC_195_262,(0,0,7):C.UVGC_195_263,(0,0,8):C.UVGC_195_264,(0,0,9):C.UVGC_195_265})

V_180 = CTVertex(name = 'V_180',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_188_186,(0,0,1):C.UVGC_188_187,(0,0,2):C.UVGC_188_188,(0,0,3):C.UVGC_188_189,(0,0,4):C.UVGC_188_190,(0,0,5):C.UVGC_188_191,(0,0,6):C.UVGC_188_192,(0,0,7):C.UVGC_188_193,(0,0,8):C.UVGC_188_194,(0,0,9):C.UVGC_188_195,(0,1,0):C.UVGC_188_186,(0,1,1):C.UVGC_188_187,(0,1,2):C.UVGC_188_188,(0,1,3):C.UVGC_188_189,(0,1,4):C.UVGC_188_190,(0,1,5):C.UVGC_188_191,(0,1,6):C.UVGC_188_192,(0,1,7):C.UVGC_188_193,(0,1,8):C.UVGC_188_194,(0,1,9):C.UVGC_188_195})

V_181 = CTVertex(name = 'V_181',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_184_146,(0,0,1):C.UVGC_184_147,(0,0,2):C.UVGC_184_148,(0,0,3):C.UVGC_184_149,(0,0,4):C.UVGC_184_150,(0,0,5):C.UVGC_184_151,(0,0,6):C.UVGC_184_152,(0,0,7):C.UVGC_184_153,(0,0,8):C.UVGC_184_154,(0,0,9):C.UVGC_184_155})

V_182 = CTVertex(name = 'V_182',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_192_226,(0,0,1):C.UVGC_192_227,(0,0,2):C.UVGC_192_228,(0,0,3):C.UVGC_192_229,(0,0,4):C.UVGC_192_230,(0,0,5):C.UVGC_192_231,(0,0,6):C.UVGC_192_232,(0,0,7):C.UVGC_192_233,(0,0,8):C.UVGC_192_234,(0,0,9):C.UVGC_192_235})

V_183 = CTVertex(name = 'V_183',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_189_196,(0,0,1):C.UVGC_189_197,(0,0,2):C.UVGC_189_198,(0,0,3):C.UVGC_189_199,(0,0,4):C.UVGC_189_200,(0,0,5):C.UVGC_189_201,(0,0,6):C.UVGC_189_202,(0,0,7):C.UVGC_189_203,(0,0,8):C.UVGC_189_204,(0,0,9):C.UVGC_189_205,(0,1,0):C.UVGC_189_196,(0,1,1):C.UVGC_189_197,(0,1,2):C.UVGC_189_198,(0,1,3):C.UVGC_189_199,(0,1,4):C.UVGC_189_200,(0,1,5):C.UVGC_189_201,(0,1,6):C.UVGC_189_202,(0,1,7):C.UVGC_189_203,(0,1,8):C.UVGC_189_204,(0,1,9):C.UVGC_189_205})

V_184 = CTVertex(name = 'V_184',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_191_216,(0,0,1):C.UVGC_191_217,(0,0,2):C.UVGC_191_218,(0,0,3):C.UVGC_191_219,(0,0,4):C.UVGC_191_220,(0,0,5):C.UVGC_191_221,(0,0,6):C.UVGC_191_222,(0,0,7):C.UVGC_191_223,(0,0,8):C.UVGC_191_224,(0,0,9):C.UVGC_191_225,(0,1,0):C.UVGC_191_216,(0,1,1):C.UVGC_191_217,(0,1,2):C.UVGC_191_218,(0,1,3):C.UVGC_191_219,(0,1,4):C.UVGC_191_220,(0,1,5):C.UVGC_191_221,(0,1,6):C.UVGC_191_222,(0,1,7):C.UVGC_191_223,(0,1,8):C.UVGC_191_224,(0,1,9):C.UVGC_191_225})

V_185 = CTVertex(name = 'V_185',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_194_246,(0,0,1):C.UVGC_194_247,(0,0,2):C.UVGC_194_248,(0,0,3):C.UVGC_194_249,(0,0,4):C.UVGC_194_250,(0,0,5):C.UVGC_194_251,(0,0,6):C.UVGC_194_252,(0,0,7):C.UVGC_194_253,(0,0,8):C.UVGC_194_254,(0,0,9):C.UVGC_194_255})

V_186 = CTVertex(name = 'V_186',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_190_206,(0,0,1):C.UVGC_190_207,(0,0,2):C.UVGC_190_208,(0,0,3):C.UVGC_190_209,(0,0,4):C.UVGC_190_210,(0,0,5):C.UVGC_190_211,(0,0,6):C.UVGC_190_212,(0,0,7):C.UVGC_190_213,(0,0,8):C.UVGC_190_214,(0,0,9):C.UVGC_190_215,(0,1,0):C.UVGC_190_206,(0,1,1):C.UVGC_190_207,(0,1,2):C.UVGC_190_208,(0,1,3):C.UVGC_190_209,(0,1,4):C.UVGC_190_210,(0,1,5):C.UVGC_190_211,(0,1,6):C.UVGC_190_212,(0,1,7):C.UVGC_190_213,(0,1,8):C.UVGC_190_214,(0,1,9):C.UVGC_190_215})

V_187 = CTVertex(name = 'V_187',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_183_136,(0,0,1):C.UVGC_183_137,(0,0,2):C.UVGC_183_138,(0,0,3):C.UVGC_183_139,(0,0,4):C.UVGC_183_140,(0,0,5):C.UVGC_183_141,(0,0,6):C.UVGC_183_142,(0,0,7):C.UVGC_183_143,(0,0,8):C.UVGC_183_144,(0,0,9):C.UVGC_183_145})

V_188 = CTVertex(name = 'V_188',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_191_216,(0,0,1):C.UVGC_191_217,(0,0,2):C.UVGC_191_218,(0,0,3):C.UVGC_191_219,(0,0,4):C.UVGC_191_220,(0,0,5):C.UVGC_191_221,(0,0,6):C.UVGC_191_222,(0,0,7):C.UVGC_191_223,(0,0,8):C.UVGC_191_224,(0,0,9):C.UVGC_191_225,(0,1,0):C.UVGC_191_216,(0,1,1):C.UVGC_191_217,(0,1,2):C.UVGC_191_218,(0,1,3):C.UVGC_191_219,(0,1,4):C.UVGC_191_220,(0,1,5):C.UVGC_191_221,(0,1,6):C.UVGC_191_222,(0,1,7):C.UVGC_191_223,(0,1,8):C.UVGC_191_224,(0,1,9):C.UVGC_191_225})

V_189 = CTVertex(name = 'V_189',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_197_276,(0,0,1):C.UVGC_197_277,(0,0,2):C.UVGC_197_278,(0,0,3):C.UVGC_197_279,(0,0,4):C.UVGC_197_280,(0,0,5):C.UVGC_197_281,(0,0,6):C.UVGC_197_282,(0,0,7):C.UVGC_197_283,(0,0,8):C.UVGC_197_284,(0,0,9):C.UVGC_197_285})

V_190 = CTVertex(name = 'V_190',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV3, L.UUV4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_190_206,(0,0,1):C.UVGC_190_207,(0,0,2):C.UVGC_190_208,(0,0,3):C.UVGC_190_209,(0,0,4):C.UVGC_190_210,(0,0,5):C.UVGC_190_211,(0,0,6):C.UVGC_190_212,(0,0,7):C.UVGC_190_213,(0,0,8):C.UVGC_190_214,(0,0,9):C.UVGC_190_215,(0,1,0):C.UVGC_190_206,(0,1,1):C.UVGC_190_207,(0,1,2):C.UVGC_190_208,(0,1,3):C.UVGC_190_209,(0,1,4):C.UVGC_190_210,(0,1,5):C.UVGC_190_211,(0,1,6):C.UVGC_190_212,(0,1,7):C.UVGC_190_213,(0,1,8):C.UVGC_190_214,(0,1,9):C.UVGC_190_215})

V_191 = CTVertex(name = 'V_191',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_193_236,(0,0,1):C.UVGC_193_237,(0,0,2):C.UVGC_193_238,(0,0,3):C.UVGC_193_239,(0,0,4):C.UVGC_193_240,(0,0,5):C.UVGC_193_241,(0,0,6):C.UVGC_193_242,(0,0,7):C.UVGC_193_243,(0,0,8):C.UVGC_193_244,(0,0,9):C.UVGC_193_245})

V_192 = CTVertex(name = 'V_192',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.VVV16, L.VVV17, L.VVV18, L.VVV19, L.VVV20, L.VVV21, L.VVV25, L.VVV26 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.ghG] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.UVGC_172_84,(0,0,1):C.UVGC_172_85,(0,0,2):C.UVGC_172_86,(0,0,3):C.UVGC_172_87,(0,0,4):C.UVGC_172_88,(0,0,5):C.UVGC_172_89,(0,0,6):C.UVGC_172_90,(0,0,7):C.UVGC_172_91,(0,1,0):C.UVGC_169_72,(0,1,1):C.UVGC_169_73,(0,1,2):C.UVGC_169_74,(0,1,3):C.UVGC_169_75,(0,1,4):C.UVGC_169_76,(0,1,5):C.UVGC_169_77,(0,1,6):C.UVGC_169_78,(0,1,7):C.UVGC_169_79,(0,3,0):C.UVGC_169_72,(0,3,1):C.UVGC_169_73,(0,3,2):C.UVGC_169_74,(0,3,3):C.UVGC_171_82,(0,3,4):C.UVGC_171_83,(0,3,5):C.UVGC_169_77,(0,3,6):C.UVGC_169_78,(0,3,7):C.UVGC_169_79,(0,5,0):C.UVGC_172_84,(0,5,1):C.UVGC_172_85,(0,5,2):C.UVGC_172_86,(0,5,3):C.UVGC_174_94,(0,5,4):C.UVGC_174_95,(0,5,5):C.UVGC_172_89,(0,5,6):C.UVGC_172_90,(0,5,7):C.UVGC_172_91,(0,6,0):C.UVGC_172_84,(0,6,1):C.UVGC_172_85,(0,6,2):C.UVGC_172_86,(0,6,3):C.UVGC_173_92,(0,6,4):C.UVGC_173_93,(0,6,5):C.UVGC_172_89,(0,6,6):C.UVGC_172_90,(0,6,7):C.UVGC_172_91,(0,7,0):C.UVGC_169_72,(0,7,1):C.UVGC_169_73,(0,7,2):C.UVGC_169_74,(0,7,3):C.UVGC_170_80,(0,7,4):C.UVGC_170_81,(0,7,5):C.UVGC_169_77,(0,7,6):C.UVGC_169_78,(0,7,7):C.UVGC_169_79,(0,2,3):C.UVGC_143_12,(0,2,4):C.UVGC_143_13,(0,4,3):C.UVGC_144_14,(0,4,4):C.UVGC_144_15})

V_193 = CTVertex(name = 'V_193',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g, P.g ],
                 color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                 lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.ghG] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,1,4):C.UVGC_146_19,(0,1,5):C.UVGC_146_18,(2,1,4):C.UVGC_146_19,(2,1,5):C.UVGC_146_18,(6,1,0):C.UVGC_179_116,(6,1,2):C.UVGC_179_117,(6,1,3):C.UVGC_179_118,(6,1,4):C.UVGC_180_124,(6,1,5):C.UVGC_180_125,(6,1,6):C.UVGC_179_121,(6,1,7):C.UVGC_179_122,(6,1,8):C.UVGC_179_123,(7,1,0):C.UVGC_179_116,(7,1,2):C.UVGC_179_117,(7,1,3):C.UVGC_179_118,(7,1,4):C.UVGC_179_119,(7,1,5):C.UVGC_179_120,(7,1,6):C.UVGC_179_121,(7,1,7):C.UVGC_179_122,(7,1,8):C.UVGC_179_123,(5,1,4):C.UVGC_145_16,(5,1,5):C.UVGC_145_17,(1,1,4):C.UVGC_145_16,(1,1,5):C.UVGC_145_17,(4,1,4):C.UVGC_145_16,(4,1,5):C.UVGC_145_17,(3,1,4):C.UVGC_145_16,(3,1,5):C.UVGC_145_17,(8,1,4):C.UVGC_146_18,(8,1,5):C.UVGC_146_19,(11,1,4):C.UVGC_149_22,(11,1,5):C.UVGC_149_23,(10,1,4):C.UVGC_149_22,(10,1,5):C.UVGC_149_23,(9,1,4):C.UVGC_148_20,(9,1,5):C.UVGC_148_21,(0,2,4):C.UVGC_146_19,(0,2,5):C.UVGC_146_18,(2,2,4):C.UVGC_146_19,(2,2,5):C.UVGC_146_18,(6,2,0):C.UVGC_181_126,(6,2,2):C.UVGC_181_127,(6,2,3):C.UVGC_181_128,(6,2,4):C.UVGC_181_129,(6,2,5):C.UVGC_181_130,(6,2,6):C.UVGC_181_131,(6,2,7):C.UVGC_181_132,(6,2,8):C.UVGC_181_133,(7,2,1):C.UVGC_177_112,(7,2,4):C.UVGC_178_114,(7,2,5):C.UVGC_178_115,(5,2,4):C.UVGC_145_16,(5,2,5):C.UVGC_145_17,(1,2,4):C.UVGC_145_16,(1,2,5):C.UVGC_145_17,(4,2,4):C.UVGC_145_16,(4,2,5):C.UVGC_145_17,(3,2,4):C.UVGC_145_16,(3,2,5):C.UVGC_145_17,(8,2,0):C.UVGC_176_104,(8,2,2):C.UVGC_176_105,(8,2,3):C.UVGC_176_106,(8,2,4):C.UVGC_176_107,(8,2,5):C.UVGC_176_108,(8,2,6):C.UVGC_176_109,(8,2,7):C.UVGC_176_110,(8,2,8):C.UVGC_176_111,(11,2,4):C.UVGC_149_22,(11,2,5):C.UVGC_149_23,(10,2,4):C.UVGC_149_22,(10,2,5):C.UVGC_149_23,(9,2,4):C.UVGC_148_20,(9,2,5):C.UVGC_148_21,(0,0,4):C.UVGC_146_19,(0,0,5):C.UVGC_146_18,(2,0,4):C.UVGC_146_19,(2,0,5):C.UVGC_146_18,(6,0,1):C.UVGC_177_112,(6,0,4):C.UVGC_177_113,(6,0,5):C.UVGC_148_20,(7,0,0):C.UVGC_181_126,(7,0,2):C.UVGC_181_127,(7,0,3):C.UVGC_181_128,(7,0,4):C.UVGC_182_134,(7,0,5):C.UVGC_182_135,(7,0,6):C.UVGC_181_131,(7,0,7):C.UVGC_181_132,(7,0,8):C.UVGC_181_133,(5,0,4):C.UVGC_145_16,(5,0,5):C.UVGC_145_17,(1,0,4):C.UVGC_145_16,(1,0,5):C.UVGC_145_17,(4,0,4):C.UVGC_145_16,(4,0,5):C.UVGC_145_17,(3,0,4):C.UVGC_145_16,(3,0,5):C.UVGC_145_17,(8,0,0):C.UVGC_175_96,(8,0,2):C.UVGC_175_97,(8,0,3):C.UVGC_175_98,(8,0,4):C.UVGC_175_99,(8,0,5):C.UVGC_175_100,(8,0,6):C.UVGC_175_101,(8,0,7):C.UVGC_175_102,(8,0,8):C.UVGC_175_103,(11,0,4):C.UVGC_149_22,(11,0,5):C.UVGC_149_23,(10,0,4):C.UVGC_149_22,(10,0,5):C.UVGC_149_23,(9,0,4):C.UVGC_148_20,(9,0,5):C.UVGC_148_21})

V_194 = CTVertex(name = 'V_194',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.u] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_380_2878,(0,0,9):C.UVGC_380_2879,(0,0,11):C.UVGC_380_2880,(0,0,24):C.UVGC_380_2881,(0,0,26):C.UVGC_380_2882,(0,0,33):C.UVGC_380_2883,(0,0,35):C.UVGC_380_2884,(0,0,42):C.UVGC_380_2885,(0,0,46):C.UVGC_380_2886,(0,0,48):C.UVGC_380_2887,(0,0,49):C.UVGC_380_2888,(0,0,50):C.UVGC_380_2889,(0,0,52):C.UVGC_380_2890,(0,0,55):C.UVGC_380_2891,(0,0,56):C.UVGC_380_2892,(0,0,58):C.UVGC_380_2893,(0,0,0):C.UVGC_380_2894,(0,0,3):C.UVGC_380_2895,(0,0,5):C.UVGC_380_2896,(0,0,6):C.UVGC_380_2897,(0,0,8):C.UVGC_380_2898,(0,0,10):C.UVGC_380_2899,(0,0,12):C.UVGC_380_2900,(0,0,13):C.UVGC_380_2901,(0,0,16):C.UVGC_380_2902,(0,0,19):C.UVGC_380_2903,(0,0,20):C.UVGC_380_2904,(0,0,22):C.UVGC_380_2905,(0,0,23):C.UVGC_380_2906,(0,0,25):C.UVGC_380_2907,(0,0,41):C.UVGC_380_2908,(0,0,27):C.UVGC_380_2909,(0,0,28):C.UVGC_380_2910,(0,0,29):C.UVGC_380_2911,(0,0,31):C.UVGC_380_2912,(0,0,32):C.UVGC_380_2913,(0,0,34):C.UVGC_380_2914,(0,0,36):C.UVGC_380_2915,(0,0,37):C.UVGC_380_2916,(0,0,39):C.UVGC_380_2917,(0,0,40):C.UVGC_380_2918,(0,0,43):C.UVGC_380_2919,(0,0,44):C.UVGC_380_2920,(0,0,45):C.UVGC_380_2921,(0,0,47):C.UVGC_380_2922,(0,0,51):C.UVGC_380_2923,(0,0,53):C.UVGC_380_2924,(0,0,54):C.UVGC_380_2925,(0,0,57):C.UVGC_380_2926,(0,0,1):C.UVGC_380_2927,(0,0,2):C.UVGC_380_2928,(0,0,4):C.UVGC_380_2929,(0,0,18):C.UVGC_380_2930,(0,0,14):C.UVGC_380_2931,(0,0,15):C.UVGC_380_2932,(0,0,17):C.UVGC_380_2933,(0,0,21):C.UVGC_380_2934,(0,0,38):C.UVGC_380_2935,(0,1,7):C.UVGC_381_2936,(0,1,9):C.UVGC_381_2937,(0,1,11):C.UVGC_381_2938,(0,1,24):C.UVGC_381_2939,(0,1,26):C.UVGC_381_2940,(0,1,33):C.UVGC_381_2941,(0,1,35):C.UVGC_381_2942,(0,1,42):C.UVGC_381_2943,(0,1,46):C.UVGC_381_2944,(0,1,48):C.UVGC_381_2945,(0,1,49):C.UVGC_381_2946,(0,1,50):C.UVGC_381_2947,(0,1,52):C.UVGC_381_2948,(0,1,55):C.UVGC_381_2949,(0,1,56):C.UVGC_381_2950,(0,1,58):C.UVGC_381_2951,(0,1,0):C.UVGC_381_2952,(0,1,3):C.UVGC_381_2953,(0,1,5):C.UVGC_381_2954,(0,1,6):C.UVGC_381_2955,(0,1,8):C.UVGC_381_2956,(0,1,10):C.UVGC_381_2957,(0,1,12):C.UVGC_381_2958,(0,1,13):C.UVGC_381_2959,(0,1,16):C.UVGC_381_2960,(0,1,19):C.UVGC_381_2961,(0,1,20):C.UVGC_381_2962,(0,1,22):C.UVGC_381_2963,(0,1,23):C.UVGC_381_2964,(0,1,25):C.UVGC_381_2965,(0,1,41):C.UVGC_381_2966,(0,1,27):C.UVGC_381_2967,(0,1,28):C.UVGC_381_2968,(0,1,29):C.UVGC_381_2969,(0,1,31):C.UVGC_381_2970,(0,1,32):C.UVGC_381_2971,(0,1,34):C.UVGC_381_2972,(0,1,36):C.UVGC_381_2973,(0,1,37):C.UVGC_381_2974,(0,1,39):C.UVGC_381_2975,(0,1,40):C.UVGC_381_2976,(0,1,43):C.UVGC_381_2977,(0,1,44):C.UVGC_381_2978,(0,1,45):C.UVGC_381_2979,(0,1,47):C.UVGC_381_2980,(0,1,51):C.UVGC_381_2981,(0,1,53):C.UVGC_381_2982,(0,1,54):C.UVGC_381_2983,(0,1,57):C.UVGC_381_2984,(0,1,1):C.UVGC_381_2985,(0,1,2):C.UVGC_381_2986,(0,1,4):C.UVGC_381_2987,(0,1,18):C.UVGC_381_2988,(0,1,14):C.UVGC_381_2989,(0,1,17):C.UVGC_381_2990,(0,1,21):C.UVGC_381_2991,(0,1,30):C.UVGC_381_2992,(0,1,38):C.UVGC_381_2993})

V_195 = CTVertex(name = 'V_195',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.s] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_356_2057,(0,0,9):C.UVGC_356_2058,(0,0,22):C.UVGC_356_2059,(0,0,24):C.UVGC_356_2060,(0,0,26):C.UVGC_356_2061,(0,0,33):C.UVGC_356_2062,(0,0,35):C.UVGC_356_2063,(0,0,42):C.UVGC_356_2064,(0,0,46):C.UVGC_356_2065,(0,0,48):C.UVGC_356_2066,(0,0,51):C.UVGC_356_2067,(0,0,52):C.UVGC_356_2068,(0,0,54):C.UVGC_356_2069,(0,0,55):C.UVGC_356_2070,(0,0,56):C.UVGC_356_2071,(0,0,58):C.UVGC_356_2072,(0,0,0):C.UVGC_356_2073,(0,0,3):C.UVGC_356_2074,(0,0,5):C.UVGC_356_2075,(0,0,6):C.UVGC_356_2076,(0,0,8):C.UVGC_356_2077,(0,0,10):C.UVGC_356_2078,(0,0,11):C.UVGC_356_2079,(0,0,14):C.UVGC_356_2080,(0,0,17):C.UVGC_356_2081,(0,0,18):C.UVGC_356_2082,(0,0,20):C.UVGC_356_2083,(0,0,21):C.UVGC_356_2084,(0,0,23):C.UVGC_356_2085,(0,0,25):C.UVGC_356_2086,(0,0,41):C.UVGC_356_2087,(0,0,27):C.UVGC_356_2088,(0,0,28):C.UVGC_356_2089,(0,0,29):C.UVGC_356_2090,(0,0,31):C.UVGC_356_2091,(0,0,32):C.UVGC_356_2092,(0,0,34):C.UVGC_356_2093,(0,0,36):C.UVGC_356_2094,(0,0,37):C.UVGC_356_2095,(0,0,39):C.UVGC_356_2096,(0,0,40):C.UVGC_356_2097,(0,0,43):C.UVGC_356_2098,(0,0,44):C.UVGC_356_2099,(0,0,45):C.UVGC_356_2100,(0,0,47):C.UVGC_356_2101,(0,0,49):C.UVGC_356_2102,(0,0,50):C.UVGC_356_2103,(0,0,53):C.UVGC_356_2104,(0,0,57):C.UVGC_356_2105,(0,0,1):C.UVGC_356_2106,(0,0,2):C.UVGC_356_2107,(0,0,4):C.UVGC_356_2108,(0,0,16):C.UVGC_356_2109,(0,0,12):C.UVGC_356_2110,(0,0,15):C.UVGC_356_2111,(0,0,19):C.UVGC_356_2112,(0,0,30):C.UVGC_356_2113,(0,0,38):C.UVGC_356_2114,(0,1,7):C.UVGC_357_2115,(0,1,9):C.UVGC_357_2116,(0,1,22):C.UVGC_357_2117,(0,1,24):C.UVGC_357_2118,(0,1,26):C.UVGC_357_2119,(0,1,33):C.UVGC_357_2120,(0,1,35):C.UVGC_357_2121,(0,1,42):C.UVGC_357_2122,(0,1,46):C.UVGC_357_2123,(0,1,48):C.UVGC_357_2124,(0,1,51):C.UVGC_357_2125,(0,1,52):C.UVGC_357_2126,(0,1,54):C.UVGC_357_2127,(0,1,55):C.UVGC_357_2128,(0,1,56):C.UVGC_357_2129,(0,1,58):C.UVGC_357_2130,(0,1,0):C.UVGC_357_2131,(0,1,3):C.UVGC_357_2132,(0,1,5):C.UVGC_357_2133,(0,1,6):C.UVGC_357_2134,(0,1,8):C.UVGC_357_2135,(0,1,10):C.UVGC_357_2136,(0,1,11):C.UVGC_357_2137,(0,1,14):C.UVGC_357_2138,(0,1,17):C.UVGC_357_2139,(0,1,18):C.UVGC_357_2140,(0,1,20):C.UVGC_357_2141,(0,1,21):C.UVGC_357_2142,(0,1,23):C.UVGC_357_2143,(0,1,25):C.UVGC_357_2144,(0,1,41):C.UVGC_357_2145,(0,1,27):C.UVGC_357_2146,(0,1,28):C.UVGC_357_2147,(0,1,29):C.UVGC_357_2148,(0,1,31):C.UVGC_357_2149,(0,1,32):C.UVGC_357_2150,(0,1,34):C.UVGC_357_2151,(0,1,36):C.UVGC_357_2152,(0,1,37):C.UVGC_357_2153,(0,1,39):C.UVGC_357_2154,(0,1,40):C.UVGC_357_2155,(0,1,43):C.UVGC_357_2156,(0,1,44):C.UVGC_357_2157,(0,1,45):C.UVGC_357_2158,(0,1,47):C.UVGC_357_2159,(0,1,49):C.UVGC_357_2160,(0,1,50):C.UVGC_357_2161,(0,1,53):C.UVGC_357_2162,(0,1,57):C.UVGC_357_2163,(0,1,1):C.UVGC_357_2164,(0,1,2):C.UVGC_357_2165,(0,1,4):C.UVGC_357_2166,(0,1,16):C.UVGC_357_2167,(0,1,12):C.UVGC_357_2168,(0,1,13):C.UVGC_357_2169,(0,1,15):C.UVGC_357_2170,(0,1,19):C.UVGC_357_2171,(0,1,38):C.UVGC_357_2172})

V_196 = CTVertex(name = 'V_196',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.t] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_367_2480,(0,0,20):C.UVGC_367_2481,(0,0,22):C.UVGC_367_2482,(0,0,24):C.UVGC_367_2483,(0,0,26):C.UVGC_367_2484,(0,0,33):C.UVGC_367_2485,(0,0,35):C.UVGC_367_2486,(0,0,42):C.UVGC_367_2487,(0,0,46):C.UVGC_367_2488,(0,0,48):C.UVGC_367_2489,(0,0,49):C.UVGC_367_2490,(0,0,50):C.UVGC_367_2491,(0,0,54):C.UVGC_367_2492,(0,0,55):C.UVGC_367_2493,(0,0,56):C.UVGC_367_2494,(0,0,58):C.UVGC_367_2495,(0,0,0):C.UVGC_367_2496,(0,0,3):C.UVGC_367_2497,(0,0,5):C.UVGC_367_2498,(0,0,6):C.UVGC_367_2499,(0,0,8):C.UVGC_367_2500,(0,0,9):C.UVGC_367_2501,(0,0,12):C.UVGC_367_2502,(0,0,15):C.UVGC_367_2503,(0,0,16):C.UVGC_367_2504,(0,0,18):C.UVGC_367_2505,(0,0,19):C.UVGC_367_2506,(0,0,21):C.UVGC_367_2507,(0,0,23):C.UVGC_367_2508,(0,0,25):C.UVGC_367_2509,(0,0,41):C.UVGC_367_2510,(0,0,27):C.UVGC_367_2511,(0,0,28):C.UVGC_367_2512,(0,0,29):C.UVGC_367_2513,(0,0,31):C.UVGC_367_2514,(0,0,32):C.UVGC_367_2515,(0,0,34):C.UVGC_367_2516,(0,0,36):C.UVGC_367_2517,(0,0,37):C.UVGC_367_2518,(0,0,39):C.UVGC_367_2519,(0,0,40):C.UVGC_367_2520,(0,0,43):C.UVGC_367_2521,(0,0,44):C.UVGC_367_2522,(0,0,45):C.UVGC_367_2523,(0,0,47):C.UVGC_367_2524,(0,0,52):C.UVGC_367_2525,(0,0,53):C.UVGC_367_2526,(0,0,51):C.UVGC_367_2527,(0,0,57):C.UVGC_367_2528,(0,0,1):C.UVGC_367_2529,(0,0,2):C.UVGC_367_2530,(0,0,4):C.UVGC_367_2531,(0,0,14):C.UVGC_367_2532,(0,0,10):C.UVGC_367_2533,(0,0,11):C.UVGC_367_2534,(0,0,13):C.UVGC_367_2535,(0,0,17):C.UVGC_367_2536,(0,0,38):C.UVGC_367_2537,(0,1,7):C.UVGC_366_2422,(0,1,20):C.UVGC_366_2423,(0,1,22):C.UVGC_366_2424,(0,1,24):C.UVGC_366_2425,(0,1,26):C.UVGC_366_2426,(0,1,33):C.UVGC_366_2427,(0,1,35):C.UVGC_366_2428,(0,1,42):C.UVGC_366_2429,(0,1,46):C.UVGC_366_2430,(0,1,48):C.UVGC_366_2431,(0,1,49):C.UVGC_366_2432,(0,1,50):C.UVGC_366_2433,(0,1,54):C.UVGC_366_2434,(0,1,55):C.UVGC_366_2435,(0,1,56):C.UVGC_366_2436,(0,1,58):C.UVGC_366_2437,(0,1,0):C.UVGC_366_2438,(0,1,3):C.UVGC_366_2439,(0,1,5):C.UVGC_366_2440,(0,1,6):C.UVGC_366_2441,(0,1,8):C.UVGC_366_2442,(0,1,9):C.UVGC_366_2443,(0,1,12):C.UVGC_366_2444,(0,1,15):C.UVGC_366_2445,(0,1,16):C.UVGC_366_2446,(0,1,18):C.UVGC_366_2447,(0,1,19):C.UVGC_366_2448,(0,1,21):C.UVGC_366_2449,(0,1,23):C.UVGC_366_2450,(0,1,25):C.UVGC_366_2451,(0,1,41):C.UVGC_366_2452,(0,1,27):C.UVGC_366_2453,(0,1,28):C.UVGC_366_2454,(0,1,29):C.UVGC_366_2455,(0,1,31):C.UVGC_366_2456,(0,1,32):C.UVGC_366_2457,(0,1,34):C.UVGC_366_2458,(0,1,36):C.UVGC_366_2459,(0,1,37):C.UVGC_366_2460,(0,1,39):C.UVGC_366_2461,(0,1,40):C.UVGC_366_2462,(0,1,43):C.UVGC_366_2463,(0,1,44):C.UVGC_366_2464,(0,1,45):C.UVGC_366_2465,(0,1,47):C.UVGC_366_2466,(0,1,52):C.UVGC_366_2467,(0,1,53):C.UVGC_366_2468,(0,1,51):C.UVGC_366_2469,(0,1,57):C.UVGC_366_2470,(0,1,1):C.UVGC_366_2471,(0,1,2):C.UVGC_366_2472,(0,1,4):C.UVGC_366_2473,(0,1,14):C.UVGC_366_2474,(0,1,10):C.UVGC_366_2475,(0,1,13):C.UVGC_366_2476,(0,1,17):C.UVGC_366_2477,(0,1,30):C.UVGC_366_2478,(0,1,38):C.UVGC_366_2479})

V_197 = CTVertex(name = 'V_197',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.u] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_377_2745,(0,0,5):C.UVGC_377_2746,(0,0,7):C.UVGC_377_2747,(0,0,14):C.UVGC_377_2748,(0,0,16):C.UVGC_377_2749,(0,0,20):C.UVGC_377_2750,(0,0,22):C.UVGC_377_2751,(0,0,28):C.UVGC_377_2752,(0,0,31):C.UVGC_377_2753,(0,0,33):C.UVGC_377_2754,(0,0,34):C.UVGC_377_2755,(0,0,35):C.UVGC_377_2756,(0,0,37):C.UVGC_377_2757,(0,0,39):C.UVGC_377_2758,(0,0,40):C.UVGC_377_2759,(0,0,42):C.UVGC_377_2760,(0,0,0):C.UVGC_377_2761,(0,0,1):C.UVGC_377_2762,(0,0,2):C.UVGC_377_2763,(0,0,4):C.UVGC_377_2764,(0,0,6):C.UVGC_377_2765,(0,0,8):C.UVGC_377_2766,(0,0,9):C.UVGC_377_2767,(0,0,10):C.UVGC_377_2768,(0,0,12):C.UVGC_377_2769,(0,0,13):C.UVGC_377_2770,(0,0,15):C.UVGC_377_2771,(0,0,17):C.UVGC_377_2772,(0,0,18):C.UVGC_377_2773,(0,0,19):C.UVGC_377_2774,(0,0,21):C.UVGC_377_2775,(0,0,23):C.UVGC_377_2776,(0,0,24):C.UVGC_377_2777,(0,0,26):C.UVGC_377_2778,(0,0,27):C.UVGC_377_2779,(0,0,29):C.UVGC_377_2780,(0,0,30):C.UVGC_377_2781,(0,0,32):C.UVGC_377_2782,(0,0,36):C.UVGC_377_2783,(0,0,38):C.UVGC_377_2784,(0,0,41):C.UVGC_377_2785,(0,0,11):C.UVGC_377_2786,(0,0,25):C.UVGC_377_2787})

V_198 = CTVertex(name = 'V_198',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.s] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.c, P.s] ], [ [P.c, P.W__plus__] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_358_2173,(0,0,5):C.UVGC_358_2174,(0,0,10):C.UVGC_358_2175,(0,0,12):C.UVGC_358_2176,(0,0,14):C.UVGC_358_2177,(0,0,19):C.UVGC_358_2178,(0,0,21):C.UVGC_358_2179,(0,0,26):C.UVGC_358_2180,(0,0,31):C.UVGC_358_2181,(0,0,33):C.UVGC_358_2182,(0,0,35):C.UVGC_358_2183,(0,0,36):C.UVGC_358_2184,(0,0,38):C.UVGC_358_2185,(0,0,39):C.UVGC_358_2186,(0,0,40):C.UVGC_358_2187,(0,0,42):C.UVGC_358_2188,(0,0,0):C.UVGC_358_2189,(0,0,1):C.UVGC_358_2190,(0,0,2):C.UVGC_358_2191,(0,0,4):C.UVGC_358_2192,(0,0,6):C.UVGC_358_2193,(0,0,8):C.UVGC_358_2194,(0,0,9):C.UVGC_358_2195,(0,0,11):C.UVGC_358_2196,(0,0,13):C.UVGC_358_2197,(0,0,25):C.UVGC_358_2198,(0,0,15):C.UVGC_358_2199,(0,0,16):C.UVGC_358_2200,(0,0,17):C.UVGC_358_2201,(0,0,18):C.UVGC_358_2202,(0,0,20):C.UVGC_358_2203,(0,0,22):C.UVGC_358_2204,(0,0,23):C.UVGC_358_2205,(0,0,24):C.UVGC_358_2206,(0,0,27):C.UVGC_358_2207,(0,0,29):C.UVGC_358_2208,(0,0,30):C.UVGC_358_2209,(0,0,32):C.UVGC_358_2210,(0,0,34):C.UVGC_358_2211,(0,0,37):C.UVGC_358_2212,(0,0,41):C.UVGC_358_2213,(0,0,7):C.UVGC_358_2214,(0,0,28):C.UVGC_358_2215})

V_199 = CTVertex(name = 'V_199',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.t] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_363_2289,(0,0,10):C.UVGC_363_2290,(0,0,12):C.UVGC_363_2291,(0,0,14):C.UVGC_363_2292,(0,0,16):C.UVGC_363_2293,(0,0,20):C.UVGC_363_2294,(0,0,22):C.UVGC_363_2295,(0,0,28):C.UVGC_363_2296,(0,0,31):C.UVGC_363_2297,(0,0,33):C.UVGC_363_2298,(0,0,34):C.UVGC_363_2299,(0,0,35):C.UVGC_363_2300,(0,0,38):C.UVGC_363_2301,(0,0,39):C.UVGC_363_2302,(0,0,40):C.UVGC_363_2303,(0,0,42):C.UVGC_363_2304,(0,0,0):C.UVGC_363_2305,(0,0,1):C.UVGC_363_2306,(0,0,2):C.UVGC_363_2307,(0,0,4):C.UVGC_363_2308,(0,0,5):C.UVGC_363_2309,(0,0,6):C.UVGC_363_2310,(0,0,8):C.UVGC_363_2311,(0,0,9):C.UVGC_363_2312,(0,0,11):C.UVGC_363_2313,(0,0,13):C.UVGC_363_2314,(0,0,15):C.UVGC_363_2315,(0,0,17):C.UVGC_363_2316,(0,0,18):C.UVGC_363_2317,(0,0,19):C.UVGC_363_2318,(0,0,21):C.UVGC_363_2319,(0,0,23):C.UVGC_363_2320,(0,0,24):C.UVGC_363_2321,(0,0,26):C.UVGC_363_2322,(0,0,27):C.UVGC_363_2323,(0,0,29):C.UVGC_363_2324,(0,0,30):C.UVGC_363_2325,(0,0,32):C.UVGC_363_2326,(0,0,37):C.UVGC_363_2327,(0,0,36):C.UVGC_363_2328,(0,0,41):C.UVGC_363_2329,(0,0,7):C.UVGC_363_2330,(0,0,25):C.UVGC_363_2331})

V_200 = CTVertex(name = 'V_200',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_152_28,(0,0,24):C.UVGC_152_29,(0,1,3):C.UVGC_378_2788,(0,1,5):C.UVGC_378_2789,(0,1,7):C.UVGC_378_2790,(0,1,14):C.UVGC_378_2791,(0,1,16):C.UVGC_378_2792,(0,1,22):C.UVGC_378_2793,(0,1,25):C.UVGC_378_2794,(0,1,26):C.UVGC_378_2795,(0,1,32):C.UVGC_378_2796,(0,1,35):C.UVGC_378_2797,(0,1,37):C.UVGC_378_2798,(0,1,38):C.UVGC_378_2799,(0,1,39):C.UVGC_378_2800,(0,1,41):C.UVGC_378_2801,(0,1,43):C.UVGC_378_2802,(0,1,44):C.UVGC_378_2803,(0,1,46):C.UVGC_378_2804,(0,1,0):C.UVGC_378_2805,(0,1,1):C.UVGC_378_2806,(0,1,2):C.UVGC_378_2807,(0,1,4):C.UVGC_378_2808,(0,1,6):C.UVGC_378_2809,(0,1,8):C.UVGC_378_2810,(0,1,9):C.UVGC_378_2811,(0,1,11):C.UVGC_378_2812,(0,1,12):C.UVGC_378_2813,(0,1,13):C.UVGC_378_2814,(0,1,15):C.UVGC_378_2815,(0,1,17):C.UVGC_378_2816,(0,1,18):C.UVGC_378_2817,(0,1,19):C.UVGC_378_2818,(0,1,20):C.UVGC_378_2819,(0,1,23):C.UVGC_378_2820,(0,1,27):C.UVGC_378_2821,(0,1,28):C.UVGC_378_2822,(0,1,30):C.UVGC_378_2823,(0,1,31):C.UVGC_378_2824,(0,1,33):C.UVGC_378_2825,(0,1,34):C.UVGC_378_2826,(0,1,36):C.UVGC_378_2827,(0,1,40):C.UVGC_378_2828,(0,1,42):C.UVGC_378_2829,(0,1,45):C.UVGC_378_2830,(0,1,10):C.UVGC_378_2831,(0,1,29):C.UVGC_378_2832})

V_201 = CTVertex(name = 'V_201',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.s] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.c, P.s] ], [ [P.c, P.W__plus__] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_153_30,(0,0,24):C.UVGC_153_31,(0,1,3):C.UVGC_353_1896,(0,1,5):C.UVGC_353_1897,(0,1,10):C.UVGC_353_1898,(0,1,12):C.UVGC_353_1899,(0,1,14):C.UVGC_353_1900,(0,1,22):C.UVGC_353_1901,(0,1,25):C.UVGC_353_1902,(0,1,26):C.UVGC_353_1903,(0,1,31):C.UVGC_353_1904,(0,1,35):C.UVGC_353_1905,(0,1,37):C.UVGC_353_1906,(0,1,39):C.UVGC_353_1907,(0,1,40):C.UVGC_353_1908,(0,1,42):C.UVGC_353_1909,(0,1,43):C.UVGC_353_1910,(0,1,44):C.UVGC_353_1911,(0,1,46):C.UVGC_353_1912,(0,1,0):C.UVGC_353_1913,(0,1,1):C.UVGC_353_1914,(0,1,2):C.UVGC_353_1915,(0,1,4):C.UVGC_353_1916,(0,1,6):C.UVGC_353_1917,(0,1,8):C.UVGC_353_1918,(0,1,9):C.UVGC_353_1919,(0,1,11):C.UVGC_353_1920,(0,1,13):C.UVGC_353_1921,(0,1,30):C.UVGC_353_1922,(0,1,15):C.UVGC_353_1923,(0,1,16):C.UVGC_353_1924,(0,1,17):C.UVGC_353_1925,(0,1,19):C.UVGC_353_1926,(0,1,20):C.UVGC_353_1927,(0,1,23):C.UVGC_353_1928,(0,1,27):C.UVGC_353_1929,(0,1,28):C.UVGC_353_1930,(0,1,29):C.UVGC_353_1931,(0,1,32):C.UVGC_353_1932,(0,1,33):C.UVGC_353_1933,(0,1,34):C.UVGC_353_1934,(0,1,36):C.UVGC_353_1935,(0,1,38):C.UVGC_353_1936,(0,1,41):C.UVGC_353_1937,(0,1,45):C.UVGC_353_1938,(0,1,7):C.UVGC_353_1939,(0,1,18):C.UVGC_353_1940})

V_202 = CTVertex(name = 'V_202',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_158_40,(0,0,24):C.UVGC_158_41,(0,1,3):C.UVGC_364_2332,(0,1,10):C.UVGC_364_2333,(0,1,12):C.UVGC_364_2334,(0,1,14):C.UVGC_364_2335,(0,1,16):C.UVGC_364_2336,(0,1,22):C.UVGC_364_2337,(0,1,25):C.UVGC_364_2338,(0,1,26):C.UVGC_364_2339,(0,1,32):C.UVGC_364_2340,(0,1,35):C.UVGC_364_2341,(0,1,37):C.UVGC_364_2342,(0,1,38):C.UVGC_364_2343,(0,1,39):C.UVGC_364_2344,(0,1,42):C.UVGC_364_2345,(0,1,43):C.UVGC_364_2346,(0,1,44):C.UVGC_364_2347,(0,1,46):C.UVGC_364_2348,(0,1,0):C.UVGC_364_2349,(0,1,1):C.UVGC_364_2350,(0,1,2):C.UVGC_364_2351,(0,1,4):C.UVGC_364_2352,(0,1,5):C.UVGC_364_2353,(0,1,7):C.UVGC_364_2354,(0,1,8):C.UVGC_364_2355,(0,1,9):C.UVGC_364_2356,(0,1,11):C.UVGC_364_2357,(0,1,13):C.UVGC_364_2358,(0,1,15):C.UVGC_364_2359,(0,1,17):C.UVGC_364_2360,(0,1,18):C.UVGC_364_2361,(0,1,19):C.UVGC_364_2362,(0,1,20):C.UVGC_364_2363,(0,1,23):C.UVGC_364_2364,(0,1,27):C.UVGC_364_2365,(0,1,28):C.UVGC_364_2366,(0,1,30):C.UVGC_364_2367,(0,1,31):C.UVGC_364_2368,(0,1,33):C.UVGC_364_2369,(0,1,34):C.UVGC_364_2370,(0,1,36):C.UVGC_364_2371,(0,1,41):C.UVGC_364_2372,(0,1,40):C.UVGC_364_2373,(0,1,45):C.UVGC_364_2374,(0,1,6):C.UVGC_364_2375,(0,1,29):C.UVGC_364_2376})

V_203 = CTVertex(name = 'V_203',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS7 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.Z] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.ve, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.ve, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_388_3255,(0,0,6):C.UVGC_388_3256,(0,0,8):C.UVGC_388_3257,(0,0,10):C.UVGC_388_3258,(0,0,20):C.UVGC_388_3259,(0,0,25):C.UVGC_388_3260,(0,0,27):C.UVGC_388_3261,(0,0,33):C.UVGC_388_3262,(0,0,36):C.UVGC_388_3263,(0,0,38):C.UVGC_388_3264,(0,0,39):C.UVGC_388_3265,(0,0,40):C.UVGC_388_3266,(0,0,42):C.UVGC_388_3267,(0,0,43):C.UVGC_388_3268,(0,0,46):C.UVGC_388_3269,(0,0,48):C.UVGC_388_3270,(0,0,0):C.UVGC_388_3271,(0,0,2):C.UVGC_388_3272,(0,0,3):C.UVGC_388_3273,(0,0,5):C.UVGC_388_3274,(0,0,7):C.UVGC_388_3275,(0,0,9):C.UVGC_388_3276,(0,0,11):C.UVGC_388_3277,(0,0,13):C.UVGC_388_3278,(0,0,15):C.UVGC_388_3279,(0,0,16):C.UVGC_388_3280,(0,0,18):C.UVGC_388_3281,(0,0,19):C.UVGC_388_3282,(0,0,21):C.UVGC_388_3283,(0,0,22):C.UVGC_388_3284,(0,0,23):C.UVGC_388_3285,(0,0,24):C.UVGC_388_3286,(0,0,26):C.UVGC_388_3287,(0,0,28):C.UVGC_388_3288,(0,0,29):C.UVGC_388_3289,(0,0,31):C.UVGC_388_3290,(0,0,32):C.UVGC_388_3291,(0,0,34):C.UVGC_388_3292,(0,0,35):C.UVGC_388_3293,(0,0,37):C.UVGC_388_3294,(0,0,41):C.UVGC_388_3295,(0,0,44):C.UVGC_388_3296,(0,0,45):C.UVGC_388_3297,(0,0,47):C.UVGC_388_3298,(0,0,1):C.UVGC_388_3299,(0,0,12):C.UVGC_388_3300,(0,0,14):C.UVGC_388_3301,(0,0,17):C.UVGC_388_3302,(0,0,30):C.UVGC_388_3303})

V_204 = CTVertex(name = 'V_204',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS7 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.mu__minus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.vm, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_393_3453,(0,0,6):C.UVGC_393_3454,(0,0,8):C.UVGC_393_3455,(0,0,10):C.UVGC_393_3456,(0,0,12):C.UVGC_393_3457,(0,0,19):C.UVGC_393_3458,(0,0,21):C.UVGC_393_3459,(0,0,29):C.UVGC_393_3460,(0,0,33):C.UVGC_393_3461,(0,0,38):C.UVGC_393_3462,(0,0,39):C.UVGC_393_3463,(0,0,40):C.UVGC_393_3464,(0,0,42):C.UVGC_393_3465,(0,0,43):C.UVGC_393_3466,(0,0,46):C.UVGC_393_3467,(0,0,48):C.UVGC_393_3468,(0,0,0):C.UVGC_393_3469,(0,0,2):C.UVGC_393_3470,(0,0,3):C.UVGC_393_3471,(0,0,5):C.UVGC_393_3472,(0,0,7):C.UVGC_393_3473,(0,0,9):C.UVGC_393_3474,(0,0,11):C.UVGC_393_3475,(0,0,13):C.UVGC_393_3476,(0,0,14):C.UVGC_393_3477,(0,0,15):C.UVGC_393_3478,(0,0,17):C.UVGC_393_3479,(0,0,18):C.UVGC_393_3480,(0,0,20):C.UVGC_393_3481,(0,0,22):C.UVGC_393_3482,(0,0,23):C.UVGC_393_3483,(0,0,25):C.UVGC_393_3484,(0,0,27):C.UVGC_393_3485,(0,0,28):C.UVGC_393_3486,(0,0,30):C.UVGC_393_3487,(0,0,31):C.UVGC_393_3488,(0,0,32):C.UVGC_393_3489,(0,0,34):C.UVGC_393_3490,(0,0,36):C.UVGC_393_3491,(0,0,37):C.UVGC_393_3492,(0,0,41):C.UVGC_393_3493,(0,0,44):C.UVGC_393_3494,(0,0,45):C.UVGC_393_3495,(0,0,47):C.UVGC_393_3496,(0,0,1):C.UVGC_393_3497,(0,0,16):C.UVGC_393_3498,(0,0,24):C.UVGC_393_3499,(0,0,26):C.UVGC_393_3500,(0,0,35):C.UVGC_393_3501})

V_205 = CTVertex(name = 'V_205',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS7 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ta__minus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.vt, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_398_3646,(0,0,6):C.UVGC_398_3647,(0,0,8):C.UVGC_398_3648,(0,0,10):C.UVGC_398_3649,(0,0,12):C.UVGC_398_3650,(0,0,19):C.UVGC_398_3651,(0,0,21):C.UVGC_398_3652,(0,0,29):C.UVGC_398_3653,(0,0,33):C.UVGC_398_3654,(0,0,35):C.UVGC_398_3655,(0,0,36):C.UVGC_398_3656,(0,0,37):C.UVGC_398_3657,(0,0,42):C.UVGC_398_3658,(0,0,43):C.UVGC_398_3659,(0,0,46):C.UVGC_398_3660,(0,0,48):C.UVGC_398_3661,(0,0,0):C.UVGC_398_3662,(0,0,2):C.UVGC_398_3663,(0,0,3):C.UVGC_398_3664,(0,0,5):C.UVGC_398_3665,(0,0,7):C.UVGC_398_3666,(0,0,9):C.UVGC_398_3667,(0,0,11):C.UVGC_398_3668,(0,0,13):C.UVGC_398_3669,(0,0,14):C.UVGC_398_3670,(0,0,15):C.UVGC_398_3671,(0,0,17):C.UVGC_398_3672,(0,0,18):C.UVGC_398_3673,(0,0,20):C.UVGC_398_3674,(0,0,22):C.UVGC_398_3675,(0,0,23):C.UVGC_398_3676,(0,0,25):C.UVGC_398_3677,(0,0,27):C.UVGC_398_3678,(0,0,28):C.UVGC_398_3679,(0,0,30):C.UVGC_398_3680,(0,0,31):C.UVGC_398_3681,(0,0,32):C.UVGC_398_3682,(0,0,34):C.UVGC_398_3683,(0,0,38):C.UVGC_398_3684,(0,0,40):C.UVGC_398_3685,(0,0,41):C.UVGC_398_3686,(0,0,44):C.UVGC_398_3687,(0,0,45):C.UVGC_398_3688,(0,0,47):C.UVGC_398_3689,(0,0,1):C.UVGC_398_3690,(0,0,16):C.UVGC_398_3691,(0,0,24):C.UVGC_398_3692,(0,0,26):C.UVGC_398_3693,(0,0,39):C.UVGC_398_3694})

V_206 = CTVertex(name = 'V_206',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.Z] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.ve, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_386_3169,(0,0,5):C.UVGC_386_3170,(0,0,7):C.UVGC_386_3171,(0,0,9):C.UVGC_386_3172,(0,0,15):C.UVGC_386_3173,(0,0,19):C.UVGC_386_3174,(0,0,21):C.UVGC_386_3175,(0,0,27):C.UVGC_386_3176,(0,0,30):C.UVGC_386_3177,(0,0,32):C.UVGC_386_3178,(0,0,33):C.UVGC_386_3179,(0,0,34):C.UVGC_386_3180,(0,0,36):C.UVGC_386_3181,(0,0,37):C.UVGC_386_3182,(0,0,39):C.UVGC_386_3183,(0,0,41):C.UVGC_386_3184,(0,0,0):C.UVGC_386_3185,(0,0,1):C.UVGC_386_3186,(0,0,2):C.UVGC_386_3187,(0,0,4):C.UVGC_386_3188,(0,0,6):C.UVGC_386_3189,(0,0,8):C.UVGC_386_3190,(0,0,10):C.UVGC_386_3191,(0,0,11):C.UVGC_386_3192,(0,0,13):C.UVGC_386_3193,(0,0,14):C.UVGC_386_3194,(0,0,16):C.UVGC_386_3195,(0,0,17):C.UVGC_386_3196,(0,0,18):C.UVGC_386_3197,(0,0,20):C.UVGC_386_3198,(0,0,22):C.UVGC_386_3199,(0,0,23):C.UVGC_386_3200,(0,0,25):C.UVGC_386_3201,(0,0,26):C.UVGC_386_3202,(0,0,28):C.UVGC_386_3203,(0,0,29):C.UVGC_386_3204,(0,0,31):C.UVGC_386_3205,(0,0,35):C.UVGC_386_3206,(0,0,38):C.UVGC_386_3207,(0,0,40):C.UVGC_386_3208,(0,0,12):C.UVGC_386_3209,(0,0,24):C.UVGC_386_3210})

V_207 = CTVertex(name = 'V_207',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_391_3367,(0,0,5):C.UVGC_391_3368,(0,0,7):C.UVGC_391_3369,(0,0,9):C.UVGC_391_3370,(0,0,11):C.UVGC_391_3371,(0,0,16):C.UVGC_391_3372,(0,0,18):C.UVGC_391_3373,(0,0,24):C.UVGC_391_3374,(0,0,29):C.UVGC_391_3375,(0,0,32):C.UVGC_391_3376,(0,0,33):C.UVGC_391_3377,(0,0,34):C.UVGC_391_3378,(0,0,36):C.UVGC_391_3379,(0,0,37):C.UVGC_391_3380,(0,0,39):C.UVGC_391_3381,(0,0,41):C.UVGC_391_3382,(0,0,0):C.UVGC_391_3383,(0,0,1):C.UVGC_391_3384,(0,0,2):C.UVGC_391_3385,(0,0,4):C.UVGC_391_3386,(0,0,6):C.UVGC_391_3387,(0,0,8):C.UVGC_391_3388,(0,0,10):C.UVGC_391_3389,(0,0,12):C.UVGC_391_3390,(0,0,13):C.UVGC_391_3391,(0,0,14):C.UVGC_391_3392,(0,0,15):C.UVGC_391_3393,(0,0,17):C.UVGC_391_3394,(0,0,19):C.UVGC_391_3395,(0,0,20):C.UVGC_391_3396,(0,0,22):C.UVGC_391_3397,(0,0,23):C.UVGC_391_3398,(0,0,25):C.UVGC_391_3399,(0,0,27):C.UVGC_391_3400,(0,0,28):C.UVGC_391_3401,(0,0,30):C.UVGC_391_3402,(0,0,31):C.UVGC_391_3403,(0,0,35):C.UVGC_391_3404,(0,0,38):C.UVGC_391_3405,(0,0,40):C.UVGC_391_3406,(0,0,21):C.UVGC_391_3407,(0,0,26):C.UVGC_391_3408})

V_208 = CTVertex(name = 'V_208',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_396_3560,(0,0,5):C.UVGC_396_3561,(0,0,7):C.UVGC_396_3562,(0,0,9):C.UVGC_396_3563,(0,0,11):C.UVGC_396_3564,(0,0,16):C.UVGC_396_3565,(0,0,18):C.UVGC_396_3566,(0,0,24):C.UVGC_396_3567,(0,0,29):C.UVGC_396_3568,(0,0,31):C.UVGC_396_3569,(0,0,32):C.UVGC_396_3570,(0,0,33):C.UVGC_396_3571,(0,0,36):C.UVGC_396_3572,(0,0,37):C.UVGC_396_3573,(0,0,39):C.UVGC_396_3574,(0,0,41):C.UVGC_396_3575,(0,0,0):C.UVGC_396_3576,(0,0,1):C.UVGC_396_3577,(0,0,2):C.UVGC_396_3578,(0,0,4):C.UVGC_396_3579,(0,0,6):C.UVGC_396_3580,(0,0,8):C.UVGC_396_3581,(0,0,10):C.UVGC_396_3582,(0,0,12):C.UVGC_396_3583,(0,0,13):C.UVGC_396_3584,(0,0,14):C.UVGC_396_3585,(0,0,15):C.UVGC_396_3586,(0,0,17):C.UVGC_396_3587,(0,0,19):C.UVGC_396_3588,(0,0,20):C.UVGC_396_3589,(0,0,22):C.UVGC_396_3590,(0,0,23):C.UVGC_396_3591,(0,0,25):C.UVGC_396_3592,(0,0,27):C.UVGC_396_3593,(0,0,28):C.UVGC_396_3594,(0,0,30):C.UVGC_396_3595,(0,0,34):C.UVGC_396_3596,(0,0,35):C.UVGC_396_3597,(0,0,38):C.UVGC_396_3598,(0,0,40):C.UVGC_396_3599,(0,0,21):C.UVGC_396_3600,(0,0,26):C.UVGC_396_3601})

V_209 = CTVertex(name = 'V_209',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.Z] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.ve, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,20):C.UVGC_156_36,(0,0,23):C.UVGC_156_37,(0,1,3):C.UVGC_387_3211,(0,1,5):C.UVGC_387_3212,(0,1,7):C.UVGC_387_3213,(0,1,9):C.UVGC_387_3214,(0,1,15):C.UVGC_387_3215,(0,1,21):C.UVGC_387_3216,(0,1,24):C.UVGC_387_3217,(0,1,25):C.UVGC_387_3218,(0,1,31):C.UVGC_387_3219,(0,1,34):C.UVGC_387_3220,(0,1,36):C.UVGC_387_3221,(0,1,37):C.UVGC_387_3222,(0,1,38):C.UVGC_387_3223,(0,1,40):C.UVGC_387_3224,(0,1,41):C.UVGC_387_3225,(0,1,43):C.UVGC_387_3226,(0,1,45):C.UVGC_387_3227,(0,1,0):C.UVGC_387_3228,(0,1,1):C.UVGC_387_3229,(0,1,2):C.UVGC_387_3230,(0,1,4):C.UVGC_387_3231,(0,1,6):C.UVGC_387_3232,(0,1,8):C.UVGC_387_3233,(0,1,10):C.UVGC_387_3234,(0,1,12):C.UVGC_387_3235,(0,1,13):C.UVGC_387_3236,(0,1,14):C.UVGC_387_3237,(0,1,16):C.UVGC_387_3238,(0,1,17):C.UVGC_387_3239,(0,1,18):C.UVGC_387_3240,(0,1,19):C.UVGC_387_3241,(0,1,22):C.UVGC_387_3242,(0,1,26):C.UVGC_387_3243,(0,1,27):C.UVGC_387_3244,(0,1,29):C.UVGC_387_3245,(0,1,30):C.UVGC_387_3246,(0,1,32):C.UVGC_387_3247,(0,1,33):C.UVGC_387_3248,(0,1,35):C.UVGC_387_3249,(0,1,39):C.UVGC_387_3250,(0,1,42):C.UVGC_387_3251,(0,1,44):C.UVGC_387_3252,(0,1,11):C.UVGC_387_3253,(0,1,28):C.UVGC_387_3254})

V_210 = CTVertex(name = 'V_210',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,18):C.UVGC_157_38,(0,0,21):C.UVGC_157_39,(0,1,3):C.UVGC_392_3409,(0,1,5):C.UVGC_392_3410,(0,1,7):C.UVGC_392_3411,(0,1,9):C.UVGC_392_3412,(0,1,11):C.UVGC_392_3413,(0,1,19):C.UVGC_392_3414,(0,1,22):C.UVGC_392_3415,(0,1,23):C.UVGC_392_3416,(0,1,29):C.UVGC_392_3417,(0,1,33):C.UVGC_392_3418,(0,1,36):C.UVGC_392_3419,(0,1,37):C.UVGC_392_3420,(0,1,38):C.UVGC_392_3421,(0,1,40):C.UVGC_392_3422,(0,1,41):C.UVGC_392_3423,(0,1,43):C.UVGC_392_3424,(0,1,45):C.UVGC_392_3425,(0,1,0):C.UVGC_392_3426,(0,1,1):C.UVGC_392_3427,(0,1,2):C.UVGC_392_3428,(0,1,4):C.UVGC_392_3429,(0,1,6):C.UVGC_392_3430,(0,1,8):C.UVGC_392_3431,(0,1,10):C.UVGC_392_3432,(0,1,12):C.UVGC_392_3433,(0,1,13):C.UVGC_392_3434,(0,1,14):C.UVGC_392_3435,(0,1,16):C.UVGC_392_3436,(0,1,17):C.UVGC_392_3437,(0,1,20):C.UVGC_392_3438,(0,1,24):C.UVGC_392_3439,(0,1,25):C.UVGC_392_3440,(0,1,27):C.UVGC_392_3441,(0,1,28):C.UVGC_392_3442,(0,1,30):C.UVGC_392_3443,(0,1,31):C.UVGC_392_3444,(0,1,32):C.UVGC_392_3445,(0,1,34):C.UVGC_392_3446,(0,1,35):C.UVGC_392_3447,(0,1,39):C.UVGC_392_3448,(0,1,42):C.UVGC_392_3449,(0,1,44):C.UVGC_392_3450,(0,1,15):C.UVGC_392_3451,(0,1,26):C.UVGC_392_3452})

V_211 = CTVertex(name = 'V_211',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,18):C.UVGC_155_34,(0,0,21):C.UVGC_155_35,(0,1,3):C.UVGC_397_3602,(0,1,5):C.UVGC_397_3603,(0,1,7):C.UVGC_397_3604,(0,1,9):C.UVGC_397_3605,(0,1,11):C.UVGC_397_3606,(0,1,19):C.UVGC_397_3607,(0,1,22):C.UVGC_397_3608,(0,1,23):C.UVGC_397_3609,(0,1,29):C.UVGC_397_3610,(0,1,33):C.UVGC_397_3611,(0,1,35):C.UVGC_397_3612,(0,1,36):C.UVGC_397_3613,(0,1,37):C.UVGC_397_3614,(0,1,40):C.UVGC_397_3615,(0,1,41):C.UVGC_397_3616,(0,1,43):C.UVGC_397_3617,(0,1,45):C.UVGC_397_3618,(0,1,0):C.UVGC_397_3619,(0,1,1):C.UVGC_397_3620,(0,1,2):C.UVGC_397_3621,(0,1,4):C.UVGC_397_3622,(0,1,6):C.UVGC_397_3623,(0,1,8):C.UVGC_397_3624,(0,1,10):C.UVGC_397_3625,(0,1,12):C.UVGC_397_3626,(0,1,13):C.UVGC_397_3627,(0,1,14):C.UVGC_397_3628,(0,1,16):C.UVGC_397_3629,(0,1,17):C.UVGC_397_3630,(0,1,20):C.UVGC_397_3631,(0,1,24):C.UVGC_397_3632,(0,1,25):C.UVGC_397_3633,(0,1,27):C.UVGC_397_3634,(0,1,28):C.UVGC_397_3635,(0,1,30):C.UVGC_397_3636,(0,1,31):C.UVGC_397_3637,(0,1,32):C.UVGC_397_3638,(0,1,34):C.UVGC_397_3639,(0,1,38):C.UVGC_397_3640,(0,1,39):C.UVGC_397_3641,(0,1,42):C.UVGC_397_3642,(0,1,44):C.UVGC_397_3643,(0,1,15):C.UVGC_397_3644,(0,1,26):C.UVGC_397_3645})

V_212 = CTVertex(name = 'V_212',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.u] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_382_2994,(0,0,9):C.UVGC_382_2995,(0,0,11):C.UVGC_382_2996,(0,0,24):C.UVGC_382_2997,(0,0,26):C.UVGC_382_2998,(0,0,33):C.UVGC_382_2999,(0,0,35):C.UVGC_382_3000,(0,0,42):C.UVGC_382_3001,(0,0,46):C.UVGC_382_3002,(0,0,48):C.UVGC_382_3003,(0,0,49):C.UVGC_382_3004,(0,0,50):C.UVGC_382_3005,(0,0,52):C.UVGC_382_3006,(0,0,55):C.UVGC_382_3007,(0,0,56):C.UVGC_382_3008,(0,0,58):C.UVGC_382_3009,(0,0,0):C.UVGC_382_3010,(0,0,3):C.UVGC_382_3011,(0,0,5):C.UVGC_382_3012,(0,0,6):C.UVGC_382_3013,(0,0,8):C.UVGC_382_3014,(0,0,10):C.UVGC_382_3015,(0,0,12):C.UVGC_382_3016,(0,0,13):C.UVGC_382_3017,(0,0,16):C.UVGC_382_3018,(0,0,19):C.UVGC_382_3019,(0,0,20):C.UVGC_382_3020,(0,0,22):C.UVGC_382_3021,(0,0,23):C.UVGC_382_3022,(0,0,25):C.UVGC_382_3023,(0,0,41):C.UVGC_382_3024,(0,0,27):C.UVGC_382_3025,(0,0,28):C.UVGC_382_3026,(0,0,29):C.UVGC_382_3027,(0,0,31):C.UVGC_382_3028,(0,0,32):C.UVGC_382_3029,(0,0,34):C.UVGC_382_3030,(0,0,36):C.UVGC_382_3031,(0,0,37):C.UVGC_382_3032,(0,0,39):C.UVGC_382_3033,(0,0,40):C.UVGC_382_3034,(0,0,43):C.UVGC_382_3035,(0,0,44):C.UVGC_382_3036,(0,0,45):C.UVGC_382_3037,(0,0,47):C.UVGC_382_3038,(0,0,51):C.UVGC_382_3039,(0,0,53):C.UVGC_382_3040,(0,0,54):C.UVGC_382_3041,(0,0,57):C.UVGC_382_3042,(0,0,1):C.UVGC_382_3043,(0,0,2):C.UVGC_382_3044,(0,0,4):C.UVGC_382_3045,(0,0,18):C.UVGC_382_3046,(0,0,14):C.UVGC_382_3047,(0,0,17):C.UVGC_382_3048,(0,0,21):C.UVGC_382_3049,(0,0,30):C.UVGC_382_3050,(0,0,38):C.UVGC_382_3051,(0,1,7):C.UVGC_383_3052,(0,1,9):C.UVGC_383_3053,(0,1,11):C.UVGC_383_3054,(0,1,24):C.UVGC_383_3055,(0,1,26):C.UVGC_383_3056,(0,1,33):C.UVGC_383_3057,(0,1,35):C.UVGC_383_3058,(0,1,42):C.UVGC_383_3059,(0,1,46):C.UVGC_383_3060,(0,1,48):C.UVGC_383_3061,(0,1,49):C.UVGC_383_3062,(0,1,50):C.UVGC_383_3063,(0,1,52):C.UVGC_383_3064,(0,1,55):C.UVGC_383_3065,(0,1,56):C.UVGC_383_3066,(0,1,58):C.UVGC_383_3067,(0,1,0):C.UVGC_383_3068,(0,1,3):C.UVGC_383_3069,(0,1,5):C.UVGC_383_3070,(0,1,6):C.UVGC_383_3071,(0,1,8):C.UVGC_383_3072,(0,1,10):C.UVGC_383_3073,(0,1,12):C.UVGC_383_3074,(0,1,13):C.UVGC_383_3075,(0,1,16):C.UVGC_383_3076,(0,1,19):C.UVGC_383_3077,(0,1,20):C.UVGC_383_3078,(0,1,22):C.UVGC_383_3079,(0,1,23):C.UVGC_383_3080,(0,1,25):C.UVGC_383_3081,(0,1,41):C.UVGC_383_3082,(0,1,27):C.UVGC_383_3083,(0,1,28):C.UVGC_383_3084,(0,1,29):C.UVGC_383_3085,(0,1,31):C.UVGC_383_3086,(0,1,32):C.UVGC_383_3087,(0,1,34):C.UVGC_383_3088,(0,1,36):C.UVGC_383_3089,(0,1,37):C.UVGC_383_3090,(0,1,39):C.UVGC_383_3091,(0,1,40):C.UVGC_383_3092,(0,1,43):C.UVGC_383_3093,(0,1,44):C.UVGC_383_3094,(0,1,45):C.UVGC_383_3095,(0,1,47):C.UVGC_383_3096,(0,1,51):C.UVGC_383_3097,(0,1,53):C.UVGC_383_3098,(0,1,54):C.UVGC_383_3099,(0,1,57):C.UVGC_383_3100,(0,1,1):C.UVGC_383_3101,(0,1,2):C.UVGC_383_3102,(0,1,4):C.UVGC_383_3103,(0,1,18):C.UVGC_383_3104,(0,1,14):C.UVGC_383_3105,(0,1,15):C.UVGC_383_3106,(0,1,17):C.UVGC_383_3107,(0,1,21):C.UVGC_383_3108,(0,1,38):C.UVGC_383_3109})

V_213 = CTVertex(name = 'V_213',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.s] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_354_1941,(0,0,9):C.UVGC_354_1942,(0,0,22):C.UVGC_354_1943,(0,0,24):C.UVGC_354_1944,(0,0,26):C.UVGC_354_1945,(0,0,33):C.UVGC_354_1946,(0,0,35):C.UVGC_354_1947,(0,0,42):C.UVGC_354_1948,(0,0,46):C.UVGC_354_1949,(0,0,48):C.UVGC_354_1950,(0,0,51):C.UVGC_354_1951,(0,0,52):C.UVGC_354_1952,(0,0,54):C.UVGC_354_1953,(0,0,55):C.UVGC_354_1954,(0,0,56):C.UVGC_354_1955,(0,0,58):C.UVGC_354_1956,(0,0,0):C.UVGC_354_1957,(0,0,3):C.UVGC_354_1958,(0,0,5):C.UVGC_354_1959,(0,0,6):C.UVGC_354_1960,(0,0,8):C.UVGC_354_1961,(0,0,10):C.UVGC_354_1962,(0,0,11):C.UVGC_354_1963,(0,0,14):C.UVGC_354_1964,(0,0,17):C.UVGC_354_1965,(0,0,18):C.UVGC_354_1966,(0,0,20):C.UVGC_354_1967,(0,0,21):C.UVGC_354_1968,(0,0,23):C.UVGC_354_1969,(0,0,25):C.UVGC_354_1970,(0,0,41):C.UVGC_354_1971,(0,0,27):C.UVGC_354_1972,(0,0,28):C.UVGC_354_1973,(0,0,29):C.UVGC_354_1974,(0,0,31):C.UVGC_354_1975,(0,0,32):C.UVGC_354_1976,(0,0,34):C.UVGC_354_1977,(0,0,36):C.UVGC_354_1978,(0,0,37):C.UVGC_354_1979,(0,0,39):C.UVGC_354_1980,(0,0,40):C.UVGC_354_1981,(0,0,43):C.UVGC_354_1982,(0,0,44):C.UVGC_354_1983,(0,0,45):C.UVGC_354_1984,(0,0,47):C.UVGC_354_1985,(0,0,49):C.UVGC_354_1986,(0,0,50):C.UVGC_354_1987,(0,0,53):C.UVGC_354_1988,(0,0,57):C.UVGC_354_1989,(0,0,1):C.UVGC_354_1990,(0,0,2):C.UVGC_354_1991,(0,0,4):C.UVGC_354_1992,(0,0,16):C.UVGC_354_1993,(0,0,12):C.UVGC_354_1994,(0,0,13):C.UVGC_354_1995,(0,0,15):C.UVGC_354_1996,(0,0,19):C.UVGC_354_1997,(0,0,38):C.UVGC_354_1998,(0,1,7):C.UVGC_355_1999,(0,1,9):C.UVGC_355_2000,(0,1,22):C.UVGC_355_2001,(0,1,24):C.UVGC_355_2002,(0,1,26):C.UVGC_355_2003,(0,1,33):C.UVGC_355_2004,(0,1,35):C.UVGC_355_2005,(0,1,42):C.UVGC_355_2006,(0,1,46):C.UVGC_355_2007,(0,1,48):C.UVGC_355_2008,(0,1,51):C.UVGC_355_2009,(0,1,52):C.UVGC_355_2010,(0,1,54):C.UVGC_355_2011,(0,1,55):C.UVGC_355_2012,(0,1,56):C.UVGC_355_2013,(0,1,58):C.UVGC_355_2014,(0,1,0):C.UVGC_355_2015,(0,1,3):C.UVGC_355_2016,(0,1,5):C.UVGC_355_2017,(0,1,6):C.UVGC_355_2018,(0,1,8):C.UVGC_355_2019,(0,1,10):C.UVGC_355_2020,(0,1,11):C.UVGC_355_2021,(0,1,14):C.UVGC_355_2022,(0,1,17):C.UVGC_355_2023,(0,1,18):C.UVGC_355_2024,(0,1,20):C.UVGC_355_2025,(0,1,21):C.UVGC_355_2026,(0,1,23):C.UVGC_355_2027,(0,1,25):C.UVGC_355_2028,(0,1,41):C.UVGC_355_2029,(0,1,27):C.UVGC_355_2030,(0,1,28):C.UVGC_355_2031,(0,1,29):C.UVGC_355_2032,(0,1,31):C.UVGC_355_2033,(0,1,32):C.UVGC_355_2034,(0,1,34):C.UVGC_355_2035,(0,1,36):C.UVGC_355_2036,(0,1,37):C.UVGC_355_2037,(0,1,39):C.UVGC_355_2038,(0,1,40):C.UVGC_355_2039,(0,1,43):C.UVGC_355_2040,(0,1,44):C.UVGC_355_2041,(0,1,45):C.UVGC_355_2042,(0,1,47):C.UVGC_355_2043,(0,1,49):C.UVGC_355_2044,(0,1,50):C.UVGC_355_2045,(0,1,53):C.UVGC_355_2046,(0,1,57):C.UVGC_355_2047,(0,1,1):C.UVGC_355_2048,(0,1,2):C.UVGC_355_2049,(0,1,4):C.UVGC_355_2050,(0,1,16):C.UVGC_355_2051,(0,1,12):C.UVGC_355_2052,(0,1,15):C.UVGC_355_2053,(0,1,19):C.UVGC_355_2054,(0,1,30):C.UVGC_355_2055,(0,1,38):C.UVGC_355_2056})

V_214 = CTVertex(name = 'V_214',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS7, L.FFS8 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.t] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_369_2596,(0,0,20):C.UVGC_369_2597,(0,0,22):C.UVGC_369_2598,(0,0,24):C.UVGC_369_2599,(0,0,26):C.UVGC_369_2600,(0,0,33):C.UVGC_369_2601,(0,0,35):C.UVGC_369_2602,(0,0,42):C.UVGC_369_2603,(0,0,46):C.UVGC_369_2604,(0,0,48):C.UVGC_369_2605,(0,0,49):C.UVGC_369_2606,(0,0,50):C.UVGC_369_2607,(0,0,54):C.UVGC_369_2608,(0,0,55):C.UVGC_369_2609,(0,0,56):C.UVGC_369_2610,(0,0,58):C.UVGC_369_2611,(0,0,0):C.UVGC_369_2612,(0,0,3):C.UVGC_369_2613,(0,0,5):C.UVGC_369_2614,(0,0,6):C.UVGC_369_2615,(0,0,8):C.UVGC_369_2616,(0,0,9):C.UVGC_369_2617,(0,0,12):C.UVGC_369_2618,(0,0,15):C.UVGC_369_2619,(0,0,16):C.UVGC_369_2620,(0,0,18):C.UVGC_369_2621,(0,0,19):C.UVGC_369_2622,(0,0,21):C.UVGC_369_2623,(0,0,23):C.UVGC_369_2624,(0,0,25):C.UVGC_369_2625,(0,0,41):C.UVGC_369_2626,(0,0,27):C.UVGC_369_2627,(0,0,28):C.UVGC_369_2628,(0,0,29):C.UVGC_369_2629,(0,0,31):C.UVGC_369_2630,(0,0,32):C.UVGC_369_2631,(0,0,34):C.UVGC_369_2632,(0,0,36):C.UVGC_369_2633,(0,0,37):C.UVGC_369_2634,(0,0,39):C.UVGC_369_2635,(0,0,40):C.UVGC_369_2636,(0,0,43):C.UVGC_369_2637,(0,0,44):C.UVGC_369_2638,(0,0,45):C.UVGC_369_2639,(0,0,47):C.UVGC_369_2640,(0,0,52):C.UVGC_369_2641,(0,0,53):C.UVGC_369_2642,(0,0,51):C.UVGC_369_2643,(0,0,57):C.UVGC_369_2644,(0,0,1):C.UVGC_369_2645,(0,0,2):C.UVGC_369_2646,(0,0,4):C.UVGC_369_2647,(0,0,14):C.UVGC_369_2648,(0,0,10):C.UVGC_369_2649,(0,0,13):C.UVGC_369_2650,(0,0,17):C.UVGC_369_2651,(0,0,30):C.UVGC_369_2652,(0,0,38):C.UVGC_369_2653,(0,1,7):C.UVGC_368_2538,(0,1,20):C.UVGC_368_2539,(0,1,22):C.UVGC_368_2540,(0,1,24):C.UVGC_368_2541,(0,1,26):C.UVGC_368_2542,(0,1,33):C.UVGC_368_2543,(0,1,35):C.UVGC_368_2544,(0,1,42):C.UVGC_368_2545,(0,1,46):C.UVGC_368_2546,(0,1,48):C.UVGC_368_2547,(0,1,49):C.UVGC_368_2548,(0,1,50):C.UVGC_368_2549,(0,1,54):C.UVGC_368_2550,(0,1,55):C.UVGC_368_2551,(0,1,56):C.UVGC_368_2552,(0,1,58):C.UVGC_368_2553,(0,1,0):C.UVGC_368_2554,(0,1,3):C.UVGC_368_2555,(0,1,5):C.UVGC_368_2556,(0,1,6):C.UVGC_368_2557,(0,1,8):C.UVGC_368_2558,(0,1,9):C.UVGC_368_2559,(0,1,12):C.UVGC_368_2560,(0,1,15):C.UVGC_368_2561,(0,1,16):C.UVGC_368_2562,(0,1,18):C.UVGC_368_2563,(0,1,19):C.UVGC_368_2564,(0,1,21):C.UVGC_368_2565,(0,1,23):C.UVGC_368_2566,(0,1,25):C.UVGC_368_2567,(0,1,41):C.UVGC_368_2568,(0,1,27):C.UVGC_368_2569,(0,1,28):C.UVGC_368_2570,(0,1,29):C.UVGC_368_2571,(0,1,31):C.UVGC_368_2572,(0,1,32):C.UVGC_368_2573,(0,1,34):C.UVGC_368_2574,(0,1,36):C.UVGC_368_2575,(0,1,37):C.UVGC_368_2576,(0,1,39):C.UVGC_368_2577,(0,1,40):C.UVGC_368_2578,(0,1,43):C.UVGC_368_2579,(0,1,44):C.UVGC_368_2580,(0,1,45):C.UVGC_368_2581,(0,1,47):C.UVGC_368_2582,(0,1,52):C.UVGC_368_2583,(0,1,53):C.UVGC_368_2584,(0,1,51):C.UVGC_368_2585,(0,1,57):C.UVGC_368_2586,(0,1,1):C.UVGC_368_2587,(0,1,2):C.UVGC_368_2588,(0,1,4):C.UVGC_368_2589,(0,1,14):C.UVGC_368_2590,(0,1,10):C.UVGC_368_2591,(0,1,11):C.UVGC_368_2592,(0,1,13):C.UVGC_368_2593,(0,1,17):C.UVGC_368_2594,(0,1,38):C.UVGC_368_2595})

V_215 = CTVertex(name = 'V_215',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.u] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.d, P.u] ], [ [P.d, P.W__plus__] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_384_3110,(0,0,5):C.UVGC_384_3111,(0,0,7):C.UVGC_384_3112,(0,0,12):C.UVGC_384_3113,(0,0,14):C.UVGC_384_3114,(0,0,19):C.UVGC_384_3115,(0,0,21):C.UVGC_384_3116,(0,0,26):C.UVGC_384_3117,(0,0,31):C.UVGC_384_3118,(0,0,33):C.UVGC_384_3119,(0,0,34):C.UVGC_384_3120,(0,0,35):C.UVGC_384_3121,(0,0,37):C.UVGC_384_3122,(0,0,39):C.UVGC_384_3123,(0,0,40):C.UVGC_384_3124,(0,0,42):C.UVGC_384_3125,(0,0,0):C.UVGC_384_3126,(0,0,1):C.UVGC_384_3127,(0,0,2):C.UVGC_384_3128,(0,0,4):C.UVGC_384_3129,(0,0,6):C.UVGC_384_3130,(0,0,8):C.UVGC_384_3131,(0,0,10):C.UVGC_384_3132,(0,0,11):C.UVGC_384_3133,(0,0,13):C.UVGC_384_3134,(0,0,25):C.UVGC_384_3135,(0,0,15):C.UVGC_384_3136,(0,0,16):C.UVGC_384_3137,(0,0,17):C.UVGC_384_3138,(0,0,18):C.UVGC_384_3139,(0,0,20):C.UVGC_384_3140,(0,0,22):C.UVGC_384_3141,(0,0,23):C.UVGC_384_3142,(0,0,24):C.UVGC_384_3143,(0,0,27):C.UVGC_384_3144,(0,0,29):C.UVGC_384_3145,(0,0,30):C.UVGC_384_3146,(0,0,32):C.UVGC_384_3147,(0,0,36):C.UVGC_384_3148,(0,0,38):C.UVGC_384_3149,(0,0,41):C.UVGC_384_3150,(0,0,9):C.UVGC_384_3151,(0,0,28):C.UVGC_384_3152})

V_216 = CTVertex(name = 'V_216',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.s] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_352_1853,(0,0,5):C.UVGC_352_1854,(0,0,12):C.UVGC_352_1855,(0,0,14):C.UVGC_352_1856,(0,0,16):C.UVGC_352_1857,(0,0,20):C.UVGC_352_1858,(0,0,22):C.UVGC_352_1859,(0,0,28):C.UVGC_352_1860,(0,0,31):C.UVGC_352_1861,(0,0,33):C.UVGC_352_1862,(0,0,35):C.UVGC_352_1863,(0,0,36):C.UVGC_352_1864,(0,0,38):C.UVGC_352_1865,(0,0,39):C.UVGC_352_1866,(0,0,40):C.UVGC_352_1867,(0,0,42):C.UVGC_352_1868,(0,0,0):C.UVGC_352_1869,(0,0,1):C.UVGC_352_1870,(0,0,2):C.UVGC_352_1871,(0,0,4):C.UVGC_352_1872,(0,0,6):C.UVGC_352_1873,(0,0,7):C.UVGC_352_1874,(0,0,8):C.UVGC_352_1875,(0,0,10):C.UVGC_352_1876,(0,0,11):C.UVGC_352_1877,(0,0,13):C.UVGC_352_1878,(0,0,15):C.UVGC_352_1879,(0,0,17):C.UVGC_352_1880,(0,0,18):C.UVGC_352_1881,(0,0,19):C.UVGC_352_1882,(0,0,21):C.UVGC_352_1883,(0,0,23):C.UVGC_352_1884,(0,0,24):C.UVGC_352_1885,(0,0,26):C.UVGC_352_1886,(0,0,27):C.UVGC_352_1887,(0,0,29):C.UVGC_352_1888,(0,0,30):C.UVGC_352_1889,(0,0,32):C.UVGC_352_1890,(0,0,34):C.UVGC_352_1891,(0,0,37):C.UVGC_352_1892,(0,0,41):C.UVGC_352_1893,(0,0,9):C.UVGC_352_1894,(0,0,25):C.UVGC_352_1895})

V_217 = CTVertex(name = 'V_217',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.t] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.b, P.W__plus__] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_370_2654,(0,0,8):C.UVGC_370_2655,(0,0,10):C.UVGC_370_2656,(0,0,12):C.UVGC_370_2657,(0,0,14):C.UVGC_370_2658,(0,0,19):C.UVGC_370_2659,(0,0,21):C.UVGC_370_2660,(0,0,26):C.UVGC_370_2661,(0,0,31):C.UVGC_370_2662,(0,0,33):C.UVGC_370_2663,(0,0,34):C.UVGC_370_2664,(0,0,35):C.UVGC_370_2665,(0,0,38):C.UVGC_370_2666,(0,0,39):C.UVGC_370_2667,(0,0,40):C.UVGC_370_2668,(0,0,42):C.UVGC_370_2669,(0,0,0):C.UVGC_370_2670,(0,0,1):C.UVGC_370_2671,(0,0,2):C.UVGC_370_2672,(0,0,4):C.UVGC_370_2673,(0,0,6):C.UVGC_370_2674,(0,0,7):C.UVGC_370_2675,(0,0,9):C.UVGC_370_2676,(0,0,11):C.UVGC_370_2677,(0,0,13):C.UVGC_370_2678,(0,0,25):C.UVGC_370_2679,(0,0,15):C.UVGC_370_2680,(0,0,16):C.UVGC_370_2681,(0,0,17):C.UVGC_370_2682,(0,0,18):C.UVGC_370_2683,(0,0,20):C.UVGC_370_2684,(0,0,22):C.UVGC_370_2685,(0,0,23):C.UVGC_370_2686,(0,0,24):C.UVGC_370_2687,(0,0,27):C.UVGC_370_2688,(0,0,29):C.UVGC_370_2689,(0,0,30):C.UVGC_370_2690,(0,0,32):C.UVGC_370_2691,(0,0,37):C.UVGC_370_2692,(0,0,36):C.UVGC_370_2693,(0,0,41):C.UVGC_370_2694,(0,0,5):C.UVGC_370_2695,(0,0,28):C.UVGC_370_2696})

V_218 = CTVertex(name = 'V_218',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.u] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.d, P.u] ], [ [P.d, P.W__plus__] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_151_26,(0,0,24):C.UVGC_151_27,(0,1,3):C.UVGC_379_2833,(0,1,5):C.UVGC_379_2834,(0,1,7):C.UVGC_379_2835,(0,1,12):C.UVGC_379_2836,(0,1,14):C.UVGC_379_2837,(0,1,22):C.UVGC_379_2838,(0,1,25):C.UVGC_379_2839,(0,1,26):C.UVGC_379_2840,(0,1,31):C.UVGC_379_2841,(0,1,35):C.UVGC_379_2842,(0,1,37):C.UVGC_379_2843,(0,1,38):C.UVGC_379_2844,(0,1,39):C.UVGC_379_2845,(0,1,41):C.UVGC_379_2846,(0,1,43):C.UVGC_379_2847,(0,1,44):C.UVGC_379_2848,(0,1,46):C.UVGC_379_2849,(0,1,0):C.UVGC_379_2850,(0,1,1):C.UVGC_379_2851,(0,1,2):C.UVGC_379_2852,(0,1,4):C.UVGC_379_2853,(0,1,6):C.UVGC_379_2854,(0,1,8):C.UVGC_379_2855,(0,1,10):C.UVGC_379_2856,(0,1,11):C.UVGC_379_2857,(0,1,13):C.UVGC_379_2858,(0,1,30):C.UVGC_379_2859,(0,1,15):C.UVGC_379_2860,(0,1,16):C.UVGC_379_2861,(0,1,17):C.UVGC_379_2862,(0,1,19):C.UVGC_379_2863,(0,1,20):C.UVGC_379_2864,(0,1,23):C.UVGC_379_2865,(0,1,27):C.UVGC_379_2866,(0,1,28):C.UVGC_379_2867,(0,1,29):C.UVGC_379_2868,(0,1,32):C.UVGC_379_2869,(0,1,33):C.UVGC_379_2870,(0,1,34):C.UVGC_379_2871,(0,1,36):C.UVGC_379_2872,(0,1,40):C.UVGC_379_2873,(0,1,42):C.UVGC_379_2874,(0,1,45):C.UVGC_379_2875,(0,1,9):C.UVGC_379_2876,(0,1,18):C.UVGC_379_2877})

V_219 = CTVertex(name = 'V_219',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_154_32,(0,0,24):C.UVGC_154_33,(0,1,3):C.UVGC_351_1808,(0,1,5):C.UVGC_351_1809,(0,1,12):C.UVGC_351_1810,(0,1,14):C.UVGC_351_1811,(0,1,16):C.UVGC_351_1812,(0,1,22):C.UVGC_351_1813,(0,1,25):C.UVGC_351_1814,(0,1,26):C.UVGC_351_1815,(0,1,32):C.UVGC_351_1816,(0,1,35):C.UVGC_351_1817,(0,1,37):C.UVGC_351_1818,(0,1,39):C.UVGC_351_1819,(0,1,40):C.UVGC_351_1820,(0,1,42):C.UVGC_351_1821,(0,1,43):C.UVGC_351_1822,(0,1,44):C.UVGC_351_1823,(0,1,46):C.UVGC_351_1824,(0,1,0):C.UVGC_351_1825,(0,1,1):C.UVGC_351_1826,(0,1,2):C.UVGC_351_1827,(0,1,4):C.UVGC_351_1828,(0,1,6):C.UVGC_351_1829,(0,1,7):C.UVGC_351_1830,(0,1,9):C.UVGC_351_1831,(0,1,10):C.UVGC_351_1832,(0,1,11):C.UVGC_351_1833,(0,1,13):C.UVGC_351_1834,(0,1,15):C.UVGC_351_1835,(0,1,17):C.UVGC_351_1836,(0,1,18):C.UVGC_351_1837,(0,1,19):C.UVGC_351_1838,(0,1,20):C.UVGC_351_1839,(0,1,23):C.UVGC_351_1840,(0,1,27):C.UVGC_351_1841,(0,1,28):C.UVGC_351_1842,(0,1,30):C.UVGC_351_1843,(0,1,31):C.UVGC_351_1844,(0,1,33):C.UVGC_351_1845,(0,1,34):C.UVGC_351_1846,(0,1,36):C.UVGC_351_1847,(0,1,38):C.UVGC_351_1848,(0,1,41):C.UVGC_351_1849,(0,1,45):C.UVGC_351_1850,(0,1,8):C.UVGC_351_1851,(0,1,29):C.UVGC_351_1852})

V_220 = CTVertex(name = 'V_220',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS5, L.FFS6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.t] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.b, P.W__plus__] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,21):C.UVGC_159_42,(0,0,24):C.UVGC_159_43,(0,1,3):C.UVGC_365_2377,(0,1,8):C.UVGC_365_2378,(0,1,10):C.UVGC_365_2379,(0,1,12):C.UVGC_365_2380,(0,1,14):C.UVGC_365_2381,(0,1,22):C.UVGC_365_2382,(0,1,25):C.UVGC_365_2383,(0,1,26):C.UVGC_365_2384,(0,1,31):C.UVGC_365_2385,(0,1,35):C.UVGC_365_2386,(0,1,37):C.UVGC_365_2387,(0,1,38):C.UVGC_365_2388,(0,1,39):C.UVGC_365_2389,(0,1,42):C.UVGC_365_2390,(0,1,43):C.UVGC_365_2391,(0,1,44):C.UVGC_365_2392,(0,1,46):C.UVGC_365_2393,(0,1,0):C.UVGC_365_2394,(0,1,1):C.UVGC_365_2395,(0,1,2):C.UVGC_365_2396,(0,1,4):C.UVGC_365_2397,(0,1,6):C.UVGC_365_2398,(0,1,7):C.UVGC_365_2399,(0,1,9):C.UVGC_365_2400,(0,1,11):C.UVGC_365_2401,(0,1,13):C.UVGC_365_2402,(0,1,30):C.UVGC_365_2403,(0,1,15):C.UVGC_365_2404,(0,1,16):C.UVGC_365_2405,(0,1,17):C.UVGC_365_2406,(0,1,19):C.UVGC_365_2407,(0,1,20):C.UVGC_365_2408,(0,1,23):C.UVGC_365_2409,(0,1,27):C.UVGC_365_2410,(0,1,28):C.UVGC_365_2411,(0,1,29):C.UVGC_365_2412,(0,1,32):C.UVGC_365_2413,(0,1,33):C.UVGC_365_2414,(0,1,34):C.UVGC_365_2415,(0,1,36):C.UVGC_365_2416,(0,1,41):C.UVGC_365_2417,(0,1,40):C.UVGC_365_2418,(0,1,45):C.UVGC_365_2419,(0,1,5):C.UVGC_365_2420,(0,1,18):C.UVGC_365_2421})

V_221 = CTVertex(name = 'V_221',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_428_4635,(0,0,5):C.UVGC_428_4636,(0,0,7):C.UVGC_428_4637,(0,0,9):C.UVGC_428_4638,(0,0,15):C.UVGC_428_4639,(0,0,17):C.UVGC_428_4640,(0,0,26):C.UVGC_428_4641,(0,0,28):C.UVGC_428_4642,(0,0,29):C.UVGC_428_4643,(0,0,30):C.UVGC_428_4644,(0,0,32):C.UVGC_428_4645,(0,0,33):C.UVGC_428_4646,(0,0,34):C.UVGC_428_4647,(0,0,36):C.UVGC_428_4648,(0,0,0):C.UVGC_428_4649,(0,0,2):C.UVGC_428_4650,(0,0,4):C.UVGC_428_4651,(0,0,6):C.UVGC_428_4652,(0,0,8):C.UVGC_428_4653,(0,0,10):C.UVGC_428_4654,(0,0,11):C.UVGC_428_4655,(0,0,12):C.UVGC_428_4656,(0,0,13):C.UVGC_428_4657,(0,0,14):C.UVGC_428_4658,(0,0,16):C.UVGC_428_4659,(0,0,18):C.UVGC_428_4660,(0,0,20):C.UVGC_428_4661,(0,0,22):C.UVGC_428_4662,(0,0,23):C.UVGC_428_4663,(0,0,25):C.UVGC_428_4664,(0,0,27):C.UVGC_428_4665,(0,0,31):C.UVGC_428_4666,(0,0,35):C.UVGC_428_4667,(0,0,1):C.UVGC_428_4668,(0,0,19):C.UVGC_428_4669,(0,0,21):C.UVGC_428_4670,(0,0,24):C.UVGC_428_4671})

V_222 = CTVertex(name = 'V_222',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_421_4419,(0,0,5):C.UVGC_421_4420,(0,0,7):C.UVGC_421_4421,(0,0,9):C.UVGC_421_4422,(0,0,11):C.UVGC_421_4423,(0,0,19):C.UVGC_421_4424,(0,0,21):C.UVGC_421_4425,(0,0,22):C.UVGC_421_4426,(0,0,23):C.UVGC_421_4427,(0,0,28):C.UVGC_421_4428,(0,0,31):C.UVGC_421_4429,(0,0,33):C.UVGC_421_4430,(0,0,34):C.UVGC_421_4431,(0,0,35):C.UVGC_421_4432,(0,0,37):C.UVGC_421_4433,(0,0,38):C.UVGC_421_4434,(0,0,39):C.UVGC_421_4435,(0,0,41):C.UVGC_421_4436,(0,0,0):C.UVGC_421_4437,(0,0,2):C.UVGC_421_4438,(0,0,4):C.UVGC_421_4439,(0,0,6):C.UVGC_421_4440,(0,0,8):C.UVGC_421_4441,(0,0,10):C.UVGC_421_4442,(0,0,12):C.UVGC_421_4443,(0,0,14):C.UVGC_421_4444,(0,0,15):C.UVGC_421_4445,(0,0,17):C.UVGC_421_4446,(0,0,18):C.UVGC_421_4447,(0,0,20):C.UVGC_421_4448,(0,0,24):C.UVGC_421_4449,(0,0,25):C.UVGC_421_4450,(0,0,27):C.UVGC_421_4451,(0,0,29):C.UVGC_421_4452,(0,0,30):C.UVGC_421_4453,(0,0,32):C.UVGC_421_4454,(0,0,36):C.UVGC_421_4455,(0,0,40):C.UVGC_421_4456,(0,0,1):C.UVGC_421_4457,(0,0,13):C.UVGC_421_4458,(0,0,16):C.UVGC_421_4459,(0,0,26):C.UVGC_421_4460})

V_223 = CTVertex(name = 'V_223',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_411_4082,(0,0,8):C.UVGC_418_4308,(0,0,14):C.UVGC_418_4309,(0,0,17):C.UVGC_418_4310,(0,0,23):C.UVGC_418_4311,(0,0,27):C.UVGC_411_4087,(0,0,28):C.UVGC_418_4312,(0,0,30):C.UVGC_418_4313,(0,0,0):C.UVGC_418_4314,(0,0,2):C.UVGC_418_4315,(0,0,4):C.UVGC_418_4316,(0,0,5):C.UVGC_418_4317,(0,0,6):C.UVGC_418_4318,(0,0,7):C.UVGC_418_4319,(0,0,9):C.UVGC_418_4320,(0,0,11):C.UVGC_418_4321,(0,0,12):C.UVGC_418_4322,(0,0,13):C.UVGC_418_4323,(0,0,15):C.UVGC_418_4324,(0,0,16):C.UVGC_418_4325,(0,0,18):C.UVGC_418_4326,(0,0,20):C.UVGC_418_4327,(0,0,22):C.UVGC_418_4328,(0,0,24):C.UVGC_418_4329,(0,0,25):C.UVGC_418_4330,(0,0,26):C.UVGC_418_4331,(0,0,29):C.UVGC_418_4332,(0,0,1):C.UVGC_418_4333,(0,0,10):C.UVGC_411_4111,(0,0,19):C.UVGC_411_4110,(0,0,21):C.UVGC_418_4334})

V_224 = CTVertex(name = 'V_224',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_423_4506,(0,0,5):C.UVGC_423_4507,(0,0,7):C.UVGC_423_4508,(0,0,9):C.UVGC_423_4509,(0,0,16):C.UVGC_423_4510,(0,0,18):C.UVGC_423_4511,(0,0,28):C.UVGC_423_4512,(0,0,30):C.UVGC_423_4513,(0,0,31):C.UVGC_423_4514,(0,0,32):C.UVGC_423_4515,(0,0,34):C.UVGC_423_4516,(0,0,35):C.UVGC_423_4517,(0,0,36):C.UVGC_423_4518,(0,0,38):C.UVGC_423_4519,(0,0,0):C.UVGC_424_4545,(0,0,2):C.UVGC_423_4521,(0,0,4):C.UVGC_423_4522,(0,0,6):C.UVGC_423_4523,(0,0,8):C.UVGC_423_4524,(0,0,10):C.UVGC_423_4525,(0,0,11):C.UVGC_423_4526,(0,0,13):C.UVGC_423_4527,(0,0,14):C.UVGC_424_4546,(0,0,15):C.UVGC_423_4529,(0,0,17):C.UVGC_423_4530,(0,0,19):C.UVGC_423_4531,(0,0,22):C.UVGC_424_4547,(0,0,24):C.UVGC_424_4548,(0,0,25):C.UVGC_423_4534,(0,0,27):C.UVGC_424_4549,(0,0,29):C.UVGC_423_4536,(0,0,33):C.UVGC_423_4537,(0,0,37):C.UVGC_423_4538,(0,0,1):C.UVGC_423_4539,(0,0,12):C.UVGC_423_4540,(0,0,20):C.UVGC_423_4541,(0,0,21):C.UVGC_423_4542,(0,0,23):C.UVGC_423_4543,(0,0,26):C.UVGC_423_4544,(0,1,3):C.UVGC_425_4550,(0,1,5):C.UVGC_425_4551,(0,1,7):C.UVGC_425_4552,(0,1,9):C.UVGC_425_4553,(0,1,16):C.UVGC_425_4554,(0,1,18):C.UVGC_425_4555,(0,1,28):C.UVGC_425_4556,(0,1,30):C.UVGC_425_4557,(0,1,31):C.UVGC_425_4558,(0,1,32):C.UVGC_425_4559,(0,1,34):C.UVGC_425_4560,(0,1,35):C.UVGC_425_4561,(0,1,36):C.UVGC_425_4562,(0,1,38):C.UVGC_425_4563,(0,1,0):C.UVGC_425_4564,(0,1,2):C.UVGC_425_4565,(0,1,4):C.UVGC_425_4566,(0,1,6):C.UVGC_425_4567,(0,1,8):C.UVGC_425_4568,(0,1,10):C.UVGC_425_4569,(0,1,11):C.UVGC_425_4570,(0,1,13):C.UVGC_425_4571,(0,1,14):C.UVGC_425_4572,(0,1,15):C.UVGC_425_4573,(0,1,17):C.UVGC_425_4574,(0,1,19):C.UVGC_425_4575,(0,1,22):C.UVGC_425_4576,(0,1,24):C.UVGC_425_4577,(0,1,25):C.UVGC_425_4578,(0,1,27):C.UVGC_425_4579,(0,1,29):C.UVGC_425_4580,(0,1,33):C.UVGC_425_4581,(0,1,37):C.UVGC_425_4582,(0,1,1):C.UVGC_425_4583,(0,1,12):C.UVGC_423_4541,(0,1,20):C.UVGC_423_4540,(0,1,21):C.UVGC_425_4584,(0,1,23):C.UVGC_425_4585,(0,1,26):C.UVGC_425_4586})

V_225 = CTVertex(name = 'V_225',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_416_4248,(0,0,5):C.UVGC_416_4249,(0,0,7):C.UVGC_417_4290,(0,0,9):C.UVGC_416_4251,(0,0,11):C.UVGC_416_4252,(0,0,20):C.UVGC_416_4254,(0,0,22):C.UVGC_417_4291,(0,0,23):C.UVGC_416_4255,(0,0,24):C.UVGC_416_4256,(0,0,30):C.UVGC_416_4257,(0,0,33):C.UVGC_416_4258,(0,0,35):C.UVGC_416_4259,(0,0,36):C.UVGC_416_4260,(0,0,37):C.UVGC_416_4261,(0,0,39):C.UVGC_416_4262,(0,0,40):C.UVGC_417_4292,(0,0,41):C.UVGC_417_4293,(0,0,43):C.UVGC_416_4265,(0,0,0):C.UVGC_417_4294,(0,0,2):C.UVGC_417_4295,(0,0,4):C.UVGC_417_4296,(0,0,6):C.UVGC_416_4269,(0,0,8):C.UVGC_417_4297,(0,0,10):C.UVGC_416_4271,(0,0,12):C.UVGC_416_4272,(0,0,15):C.UVGC_417_4298,(0,0,16):C.UVGC_417_4299,(0,0,18):C.UVGC_417_4300,(0,0,19):C.UVGC_416_4276,(0,0,21):C.UVGC_417_4301,(0,0,25):C.UVGC_416_4278,(0,0,27):C.UVGC_417_4302,(0,0,29):C.UVGC_417_4303,(0,0,31):C.UVGC_417_4304,(0,0,32):C.UVGC_417_4305,(0,0,34):C.UVGC_417_4306,(0,0,38):C.UVGC_417_4307,(0,0,42):C.UVGC_416_4285,(0,0,1):C.UVGC_416_4286,(0,0,13):C.UVGC_412_4155,(0,0,14):C.UVGC_416_4287,(0,0,17):C.UVGC_416_4288,(0,0,26):C.UVGC_412_4152,(0,0,28):C.UVGC_416_4289,(0,1,3):C.UVGC_412_4113,(0,1,5):C.UVGC_412_4114,(0,1,7):C.UVGC_412_4115,(0,1,9):C.UVGC_412_4116,(0,1,11):C.UVGC_412_4117,(0,1,20):C.UVGC_412_4118,(0,1,22):C.UVGC_412_4119,(0,1,23):C.UVGC_412_4120,(0,1,24):C.UVGC_412_4121,(0,1,30):C.UVGC_412_4122,(0,1,33):C.UVGC_412_4123,(0,1,35):C.UVGC_412_4124,(0,1,36):C.UVGC_412_4125,(0,1,37):C.UVGC_412_4126,(0,1,39):C.UVGC_412_4127,(0,1,40):C.UVGC_412_4128,(0,1,41):C.UVGC_412_4129,(0,1,43):C.UVGC_412_4130,(0,1,0):C.UVGC_412_4131,(0,1,2):C.UVGC_412_4132,(0,1,4):C.UVGC_412_4133,(0,1,6):C.UVGC_412_4134,(0,1,8):C.UVGC_412_4135,(0,1,10):C.UVGC_412_4136,(0,1,12):C.UVGC_412_4137,(0,1,15):C.UVGC_412_4138,(0,1,16):C.UVGC_412_4139,(0,1,18):C.UVGC_412_4140,(0,1,19):C.UVGC_412_4141,(0,1,21):C.UVGC_412_4142,(0,1,25):C.UVGC_412_4143,(0,1,27):C.UVGC_412_4144,(0,1,29):C.UVGC_412_4145,(0,1,31):C.UVGC_412_4146,(0,1,32):C.UVGC_412_4147,(0,1,34):C.UVGC_412_4148,(0,1,38):C.UVGC_412_4149,(0,1,42):C.UVGC_412_4150,(0,1,1):C.UVGC_412_4151,(0,1,13):C.UVGC_412_4152,(0,1,14):C.UVGC_412_4153,(0,1,17):C.UVGC_412_4154,(0,1,26):C.UVGC_412_4155,(0,1,28):C.UVGC_412_4156})

V_226 = CTVertex(name = 'V_226',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVV16, L.VVV17, L.VVV19, L.VVV20, L.VVV21, L.VVV24, L.VVV25, L.VVV26 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__], [P.u] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__], [P.G__plus__, P.H] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_305_973,(0,0,12):C.UVGC_319_1228,(0,0,16):C.UVGC_306_989,(0,0,23):C.UVGC_325_1276,(0,0,0):C.UVGC_319_1230,(0,0,1):C.UVGC_325_1277,(0,0,3):C.UVGC_319_1232,(0,0,4):C.UVGC_319_1233,(0,0,5):C.UVGC_319_1234,(0,0,6):C.UVGC_319_1235,(0,0,7):C.UVGC_319_1236,(0,0,9):C.UVGC_325_1278,(0,0,11):C.UVGC_325_1279,(0,0,13):C.UVGC_325_1280,(0,0,15):C.UVGC_325_1281,(0,0,17):C.UVGC_319_1239,(0,0,18):C.UVGC_319_1240,(0,0,19):C.UVGC_319_1241,(0,0,20):C.UVGC_319_1242,(0,0,21):C.UVGC_319_1243,(0,0,22):C.UVGC_319_1244,(0,0,24):C.UVGC_325_1282,(0,1,2):C.UVGC_305_973,(0,1,12):C.UVGC_316_1174,(0,1,16):C.UVGC_272_717,(0,1,23):C.UVGC_316_1175,(0,1,0):C.UVGC_316_1176,(0,1,1):C.UVGC_322_1257,(0,1,3):C.UVGC_316_1178,(0,1,4):C.UVGC_316_1179,(0,1,5):C.UVGC_316_1180,(0,1,6):C.UVGC_316_1181,(0,1,7):C.UVGC_322_1258,(0,1,9):C.UVGC_322_1259,(0,1,11):C.UVGC_322_1260,(0,1,13):C.UVGC_322_1261,(0,1,15):C.UVGC_322_1262,(0,1,17):C.UVGC_322_1263,(0,1,18):C.UVGC_316_1186,(0,1,19):C.UVGC_316_1187,(0,1,20):C.UVGC_316_1188,(0,1,21):C.UVGC_316_1189,(0,1,22):C.UVGC_316_1190,(0,1,24):C.UVGC_322_1264,(0,2,2):C.UVGC_305_973,(0,2,12):C.UVGC_316_1174,(0,2,16):C.UVGC_272_717,(0,2,23):C.UVGC_324_1271,(0,2,0):C.UVGC_316_1176,(0,2,1):C.UVGC_324_1272,(0,2,3):C.UVGC_316_1178,(0,2,4):C.UVGC_316_1179,(0,2,5):C.UVGC_316_1180,(0,2,6):C.UVGC_316_1181,(0,2,7):C.UVGC_322_1258,(0,2,10):C.UVGC_324_1273,(0,2,14):C.UVGC_324_1274,(0,2,17):C.UVGC_322_1263,(0,2,18):C.UVGC_316_1186,(0,2,19):C.UVGC_316_1187,(0,2,20):C.UVGC_316_1188,(0,2,21):C.UVGC_316_1189,(0,2,22):C.UVGC_316_1190,(0,2,24):C.UVGC_324_1275,(0,4,2):C.UVGC_305_973,(0,4,12):C.UVGC_319_1228,(0,4,16):C.UVGC_306_989,(0,4,23):C.UVGC_319_1229,(0,4,0):C.UVGC_319_1230,(0,4,1):C.UVGC_319_1231,(0,4,3):C.UVGC_319_1232,(0,4,4):C.UVGC_319_1233,(0,4,5):C.UVGC_319_1234,(0,4,6):C.UVGC_319_1235,(0,4,7):C.UVGC_319_1236,(0,4,10):C.UVGC_319_1237,(0,4,14):C.UVGC_319_1238,(0,4,17):C.UVGC_319_1239,(0,4,18):C.UVGC_319_1240,(0,4,19):C.UVGC_319_1241,(0,4,20):C.UVGC_319_1242,(0,4,21):C.UVGC_319_1243,(0,4,22):C.UVGC_319_1244,(0,4,24):C.UVGC_319_1245,(0,6,2):C.UVGC_305_973,(0,6,12):C.UVGC_319_1228,(0,6,16):C.UVGC_306_989,(0,6,23):C.UVGC_319_1229,(0,6,0):C.UVGC_319_1230,(0,6,1):C.UVGC_323_1265,(0,6,3):C.UVGC_319_1232,(0,6,4):C.UVGC_319_1233,(0,6,5):C.UVGC_319_1234,(0,6,6):C.UVGC_319_1235,(0,6,7):C.UVGC_323_1266,(0,6,10):C.UVGC_323_1267,(0,6,14):C.UVGC_323_1268,(0,6,17):C.UVGC_323_1269,(0,6,18):C.UVGC_319_1240,(0,6,19):C.UVGC_319_1241,(0,6,20):C.UVGC_319_1242,(0,6,21):C.UVGC_319_1243,(0,6,22):C.UVGC_319_1244,(0,6,24):C.UVGC_323_1270,(0,7,2):C.UVGC_305_973,(0,7,12):C.UVGC_316_1174,(0,7,16):C.UVGC_272_717,(0,7,23):C.UVGC_316_1175,(0,7,0):C.UVGC_316_1176,(0,7,1):C.UVGC_316_1177,(0,7,3):C.UVGC_316_1178,(0,7,4):C.UVGC_316_1179,(0,7,5):C.UVGC_316_1180,(0,7,6):C.UVGC_316_1181,(0,7,7):C.UVGC_316_1182,(0,7,10):C.UVGC_316_1183,(0,7,14):C.UVGC_316_1184,(0,7,17):C.UVGC_316_1185,(0,7,18):C.UVGC_316_1186,(0,7,19):C.UVGC_316_1187,(0,7,20):C.UVGC_316_1188,(0,7,21):C.UVGC_316_1189,(0,7,22):C.UVGC_316_1190,(0,7,24):C.UVGC_316_1191,(0,3,1):C.UVGC_136_5,(0,3,9):C.UVGC_318_1224,(0,3,11):C.UVGC_318_1225,(0,3,13):C.UVGC_318_1226,(0,3,15):C.UVGC_318_1227,(0,3,24):C.UVGC_138_7,(0,5,1):C.UVGC_321_1250,(0,5,8):C.UVGC_321_1251,(0,5,9):C.UVGC_321_1252,(0,5,11):C.UVGC_321_1253,(0,5,13):C.UVGC_321_1254,(0,5,15):C.UVGC_321_1255,(0,5,24):C.UVGC_321_1256})

V_227 = CTVertex(name = 'V_227',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_428_4635,(0,0,5):C.UVGC_428_4636,(0,0,7):C.UVGC_428_4637,(0,0,9):C.UVGC_428_4638,(0,0,15):C.UVGC_428_4639,(0,0,17):C.UVGC_428_4640,(0,0,26):C.UVGC_428_4641,(0,0,28):C.UVGC_428_4642,(0,0,29):C.UVGC_428_4643,(0,0,30):C.UVGC_428_4644,(0,0,32):C.UVGC_428_4645,(0,0,33):C.UVGC_428_4646,(0,0,34):C.UVGC_428_4647,(0,0,36):C.UVGC_428_4648,(0,0,0):C.UVGC_428_4649,(0,0,2):C.UVGC_428_4650,(0,0,4):C.UVGC_428_4651,(0,0,6):C.UVGC_428_4652,(0,0,8):C.UVGC_428_4653,(0,0,10):C.UVGC_428_4654,(0,0,11):C.UVGC_428_4655,(0,0,12):C.UVGC_428_4656,(0,0,13):C.UVGC_428_4657,(0,0,14):C.UVGC_428_4658,(0,0,16):C.UVGC_428_4659,(0,0,18):C.UVGC_428_4660,(0,0,20):C.UVGC_428_4661,(0,0,22):C.UVGC_428_4662,(0,0,23):C.UVGC_428_4663,(0,0,25):C.UVGC_428_4664,(0,0,27):C.UVGC_428_4665,(0,0,31):C.UVGC_428_4666,(0,0,35):C.UVGC_428_4667,(0,0,1):C.UVGC_428_4668,(0,0,19):C.UVGC_428_4669,(0,0,21):C.UVGC_428_4670,(0,0,24):C.UVGC_428_4671})

V_228 = CTVertex(name = 'V_228',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_419_4335,(0,0,5):C.UVGC_419_4336,(0,0,7):C.UVGC_419_4337,(0,0,9):C.UVGC_419_4338,(0,0,11):C.UVGC_419_4339,(0,0,19):C.UVGC_419_4340,(0,0,21):C.UVGC_419_4341,(0,0,22):C.UVGC_419_4342,(0,0,23):C.UVGC_419_4343,(0,0,28):C.UVGC_419_4344,(0,0,31):C.UVGC_419_4345,(0,0,33):C.UVGC_419_4346,(0,0,34):C.UVGC_419_4347,(0,0,35):C.UVGC_419_4348,(0,0,37):C.UVGC_419_4349,(0,0,38):C.UVGC_419_4350,(0,0,39):C.UVGC_419_4351,(0,0,41):C.UVGC_419_4352,(0,0,0):C.UVGC_419_4353,(0,0,2):C.UVGC_419_4354,(0,0,4):C.UVGC_419_4355,(0,0,6):C.UVGC_419_4356,(0,0,8):C.UVGC_419_4357,(0,0,10):C.UVGC_419_4358,(0,0,12):C.UVGC_419_4359,(0,0,14):C.UVGC_419_4360,(0,0,15):C.UVGC_419_4361,(0,0,17):C.UVGC_419_4362,(0,0,18):C.UVGC_419_4363,(0,0,20):C.UVGC_419_4364,(0,0,24):C.UVGC_419_4365,(0,0,25):C.UVGC_419_4366,(0,0,27):C.UVGC_419_4367,(0,0,29):C.UVGC_419_4368,(0,0,30):C.UVGC_419_4369,(0,0,32):C.UVGC_419_4370,(0,0,36):C.UVGC_419_4371,(0,0,40):C.UVGC_419_4372,(0,0,1):C.UVGC_419_4373,(0,0,13):C.UVGC_419_4374,(0,0,16):C.UVGC_419_4375,(0,0,26):C.UVGC_419_4376})

V_229 = CTVertex(name = 'V_229',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_411_4082,(0,0,8):C.UVGC_411_4083,(0,0,14):C.UVGC_411_4084,(0,0,17):C.UVGC_411_4085,(0,0,23):C.UVGC_411_4086,(0,0,27):C.UVGC_411_4087,(0,0,28):C.UVGC_411_4088,(0,0,30):C.UVGC_411_4089,(0,0,0):C.UVGC_411_4090,(0,0,2):C.UVGC_411_4091,(0,0,4):C.UVGC_411_4092,(0,0,5):C.UVGC_411_4093,(0,0,6):C.UVGC_411_4094,(0,0,7):C.UVGC_411_4095,(0,0,9):C.UVGC_411_4096,(0,0,11):C.UVGC_411_4097,(0,0,12):C.UVGC_411_4098,(0,0,13):C.UVGC_411_4099,(0,0,15):C.UVGC_411_4100,(0,0,16):C.UVGC_411_4101,(0,0,18):C.UVGC_411_4102,(0,0,20):C.UVGC_411_4103,(0,0,22):C.UVGC_411_4104,(0,0,24):C.UVGC_411_4105,(0,0,25):C.UVGC_411_4106,(0,0,26):C.UVGC_411_4107,(0,0,29):C.UVGC_411_4108,(0,0,1):C.UVGC_411_4109,(0,0,10):C.UVGC_411_4110,(0,0,19):C.UVGC_411_4111,(0,0,21):C.UVGC_411_4112})

V_230 = CTVertex(name = 'V_230',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_425_4550,(0,0,5):C.UVGC_425_4551,(0,0,7):C.UVGC_425_4552,(0,0,9):C.UVGC_425_4553,(0,0,16):C.UVGC_425_4554,(0,0,18):C.UVGC_425_4555,(0,0,28):C.UVGC_425_4556,(0,0,30):C.UVGC_425_4557,(0,0,31):C.UVGC_425_4558,(0,0,32):C.UVGC_425_4559,(0,0,34):C.UVGC_425_4560,(0,0,35):C.UVGC_425_4561,(0,0,36):C.UVGC_425_4562,(0,0,38):C.UVGC_425_4563,(0,0,0):C.UVGC_426_4587,(0,0,2):C.UVGC_425_4565,(0,0,4):C.UVGC_425_4566,(0,0,6):C.UVGC_425_4567,(0,0,8):C.UVGC_425_4568,(0,0,10):C.UVGC_425_4569,(0,0,11):C.UVGC_425_4570,(0,0,13):C.UVGC_425_4571,(0,0,14):C.UVGC_426_4588,(0,0,15):C.UVGC_425_4573,(0,0,17):C.UVGC_425_4574,(0,0,19):C.UVGC_425_4575,(0,0,22):C.UVGC_426_4589,(0,0,24):C.UVGC_426_4590,(0,0,25):C.UVGC_425_4578,(0,0,27):C.UVGC_426_4591,(0,0,29):C.UVGC_425_4580,(0,0,33):C.UVGC_425_4581,(0,0,37):C.UVGC_425_4582,(0,0,1):C.UVGC_425_4583,(0,0,12):C.UVGC_423_4541,(0,0,20):C.UVGC_423_4540,(0,0,21):C.UVGC_425_4584,(0,0,23):C.UVGC_425_4585,(0,0,26):C.UVGC_425_4586,(0,1,3):C.UVGC_423_4506,(0,1,5):C.UVGC_423_4507,(0,1,7):C.UVGC_423_4508,(0,1,9):C.UVGC_423_4509,(0,1,16):C.UVGC_423_4510,(0,1,18):C.UVGC_423_4511,(0,1,28):C.UVGC_423_4512,(0,1,30):C.UVGC_423_4513,(0,1,31):C.UVGC_423_4514,(0,1,32):C.UVGC_423_4515,(0,1,34):C.UVGC_423_4516,(0,1,35):C.UVGC_423_4517,(0,1,36):C.UVGC_423_4518,(0,1,38):C.UVGC_423_4519,(0,1,0):C.UVGC_423_4520,(0,1,2):C.UVGC_423_4521,(0,1,4):C.UVGC_423_4522,(0,1,6):C.UVGC_423_4523,(0,1,8):C.UVGC_423_4524,(0,1,10):C.UVGC_423_4525,(0,1,11):C.UVGC_423_4526,(0,1,13):C.UVGC_423_4527,(0,1,14):C.UVGC_423_4528,(0,1,15):C.UVGC_423_4529,(0,1,17):C.UVGC_423_4530,(0,1,19):C.UVGC_423_4531,(0,1,22):C.UVGC_423_4532,(0,1,24):C.UVGC_423_4533,(0,1,25):C.UVGC_423_4534,(0,1,27):C.UVGC_423_4535,(0,1,29):C.UVGC_423_4536,(0,1,33):C.UVGC_423_4537,(0,1,37):C.UVGC_423_4538,(0,1,1):C.UVGC_423_4539,(0,1,12):C.UVGC_423_4540,(0,1,20):C.UVGC_423_4541,(0,1,21):C.UVGC_423_4542,(0,1,23):C.UVGC_423_4543,(0,1,26):C.UVGC_423_4544})

V_231 = CTVertex(name = 'V_231',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_416_4248,(0,0,5):C.UVGC_416_4249,(0,0,7):C.UVGC_416_4250,(0,0,9):C.UVGC_416_4251,(0,0,11):C.UVGC_416_4252,(0,0,20):C.UVGC_416_4253,(0,0,22):C.UVGC_416_4254,(0,0,23):C.UVGC_416_4255,(0,0,24):C.UVGC_416_4256,(0,0,30):C.UVGC_416_4257,(0,0,33):C.UVGC_416_4258,(0,0,35):C.UVGC_416_4259,(0,0,36):C.UVGC_416_4260,(0,0,37):C.UVGC_416_4261,(0,0,39):C.UVGC_416_4262,(0,0,40):C.UVGC_416_4263,(0,0,41):C.UVGC_416_4264,(0,0,43):C.UVGC_416_4265,(0,0,0):C.UVGC_416_4266,(0,0,2):C.UVGC_416_4267,(0,0,4):C.UVGC_416_4268,(0,0,6):C.UVGC_416_4269,(0,0,8):C.UVGC_416_4270,(0,0,10):C.UVGC_416_4271,(0,0,12):C.UVGC_416_4272,(0,0,15):C.UVGC_416_4273,(0,0,16):C.UVGC_416_4274,(0,0,18):C.UVGC_416_4275,(0,0,19):C.UVGC_416_4276,(0,0,21):C.UVGC_416_4277,(0,0,25):C.UVGC_416_4278,(0,0,27):C.UVGC_416_4279,(0,0,29):C.UVGC_416_4280,(0,0,31):C.UVGC_416_4281,(0,0,32):C.UVGC_416_4282,(0,0,34):C.UVGC_416_4283,(0,0,38):C.UVGC_416_4284,(0,0,42):C.UVGC_416_4285,(0,0,1):C.UVGC_416_4286,(0,0,13):C.UVGC_412_4155,(0,0,14):C.UVGC_416_4287,(0,0,17):C.UVGC_416_4288,(0,0,26):C.UVGC_412_4152,(0,0,28):C.UVGC_416_4289,(0,1,3):C.UVGC_412_4113,(0,1,5):C.UVGC_412_4114,(0,1,7):C.UVGC_413_4157,(0,1,9):C.UVGC_412_4116,(0,1,11):C.UVGC_412_4117,(0,1,20):C.UVGC_413_4158,(0,1,22):C.UVGC_412_4118,(0,1,23):C.UVGC_412_4120,(0,1,24):C.UVGC_412_4121,(0,1,30):C.UVGC_412_4122,(0,1,33):C.UVGC_412_4123,(0,1,35):C.UVGC_412_4124,(0,1,36):C.UVGC_412_4125,(0,1,37):C.UVGC_412_4126,(0,1,39):C.UVGC_412_4127,(0,1,40):C.UVGC_413_4159,(0,1,41):C.UVGC_413_4160,(0,1,43):C.UVGC_412_4130,(0,1,0):C.UVGC_412_4131,(0,1,2):C.UVGC_413_4161,(0,1,4):C.UVGC_413_4162,(0,1,6):C.UVGC_412_4134,(0,1,8):C.UVGC_413_4163,(0,1,10):C.UVGC_412_4136,(0,1,12):C.UVGC_412_4137,(0,1,15):C.UVGC_413_4164,(0,1,16):C.UVGC_413_4165,(0,1,18):C.UVGC_413_4166,(0,1,19):C.UVGC_412_4141,(0,1,21):C.UVGC_413_4167,(0,1,25):C.UVGC_412_4143,(0,1,27):C.UVGC_413_4168,(0,1,29):C.UVGC_413_4169,(0,1,31):C.UVGC_413_4170,(0,1,32):C.UVGC_413_4171,(0,1,34):C.UVGC_413_4172,(0,1,38):C.UVGC_413_4173,(0,1,42):C.UVGC_412_4150,(0,1,1):C.UVGC_412_4151,(0,1,13):C.UVGC_412_4152,(0,1,14):C.UVGC_412_4153,(0,1,17):C.UVGC_412_4154,(0,1,26):C.UVGC_412_4155,(0,1,28):C.UVGC_412_4156})

V_232 = CTVertex(name = 'V_232',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_430_4686,(0,0,5):C.UVGC_430_4687,(0,0,7):C.UVGC_430_4688,(0,0,9):C.UVGC_430_4689,(0,0,11):C.UVGC_430_4690,(0,0,17):C.UVGC_430_4691,(0,0,19):C.UVGC_430_4692,(0,0,26):C.UVGC_430_4693,(0,0,30):C.UVGC_430_4694,(0,0,32):C.UVGC_430_4695,(0,0,33):C.UVGC_430_4696,(0,0,34):C.UVGC_430_4697,(0,0,36):C.UVGC_430_4698,(0,0,37):C.UVGC_420_4391,(0,0,38):C.UVGC_430_4699,(0,0,40):C.UVGC_430_4700,(0,0,0):C.UVGC_420_4394,(0,0,2):C.UVGC_420_4395,(0,0,4):C.UVGC_420_4396,(0,0,6):C.UVGC_420_4397,(0,0,8):C.UVGC_420_4398,(0,0,10):C.UVGC_420_4399,(0,0,12):C.UVGC_430_4701,(0,0,14):C.UVGC_430_4702,(0,0,15):C.UVGC_430_4703,(0,0,16):C.UVGC_420_4403,(0,0,18):C.UVGC_420_4404,(0,0,20):C.UVGC_430_4704,(0,0,23):C.UVGC_430_4705,(0,0,25):C.UVGC_420_4407,(0,0,27):C.UVGC_430_4706,(0,0,29):C.UVGC_430_4707,(0,0,31):C.UVGC_420_4410,(0,0,35):C.UVGC_420_4411,(0,0,39):C.UVGC_420_4412,(0,0,1):C.UVGC_420_4413,(0,0,13):C.UVGC_420_4417,(0,0,21):C.UVGC_420_4414,(0,0,22):C.UVGC_420_4415,(0,0,24):C.UVGC_420_4418,(0,0,28):C.UVGC_420_4416})

V_233 = CTVertex(name = 'V_233',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a] ], [ [P.a, P.G0], [P.a, P.H] ], [ [P.a, P.G0, P.W__plus__], [P.a, P.H, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.G__plus__, P.W__plus__, P.Z] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.Z], [P.G__plus__, P.H, P.Z] ], [ [P.G0], [P.H] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z], [P.H, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_431_4708,(0,0,10):C.UVGC_431_4709,(0,0,12):C.UVGC_431_4710,(0,0,14):C.UVGC_431_4711,(0,0,16):C.UVGC_431_4712,(0,0,20):C.UVGC_430_4693,(0,0,26):C.UVGC_431_4713,(0,0,28):C.UVGC_431_4714,(0,0,35):C.UVGC_431_4715,(0,0,37):C.UVGC_431_4716,(0,0,38):C.UVGC_431_4717,(0,0,39):C.UVGC_431_4718,(0,0,41):C.UVGC_431_4719,(0,0,42):C.UVGC_420_4391,(0,0,43):C.UVGC_430_4699,(0,0,45):C.UVGC_431_4720,(0,0,1):C.UVGC_431_4721,(0,0,3):C.UVGC_431_4722,(0,0,7):C.UVGC_431_4723,(0,0,9):C.UVGC_431_4724,(0,0,11):C.UVGC_431_4725,(0,0,13):C.UVGC_431_4726,(0,0,15):C.UVGC_431_4727,(0,0,17):C.UVGC_431_4728,(0,0,18):C.UVGC_431_4729,(0,0,21):C.UVGC_420_4401,(0,0,22):C.UVGC_431_4730,(0,0,24):C.UVGC_431_4731,(0,0,25):C.UVGC_420_4403,(0,0,27):C.UVGC_431_4732,(0,0,29):C.UVGC_431_4733,(0,0,30):C.UVGC_431_4734,(0,0,32):C.UVGC_431_4735,(0,0,33):C.UVGC_431_4736,(0,0,34):C.UVGC_431_4737,(0,0,36):C.UVGC_431_4738,(0,0,40):C.UVGC_431_4739,(0,0,44):C.UVGC_431_4740,(0,0,2):C.UVGC_431_4741,(0,0,4):C.UVGC_431_4742,(0,0,6):C.UVGC_431_4743,(0,0,8):C.UVGC_431_4744,(0,0,19):C.UVGC_431_4745,(0,0,23):C.UVGC_431_4746,(0,0,31):C.UVGC_431_4747,(0,0,5):C.UVGC_431_4748})

V_234 = CTVertex(name = 'V_234',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_420_4377,(0,0,5):C.UVGC_420_4378,(0,0,7):C.UVGC_420_4379,(0,0,9):C.UVGC_420_4380,(0,0,11):C.UVGC_420_4381,(0,0,19):C.UVGC_420_4382,(0,0,21):C.UVGC_420_4383,(0,0,22):C.UVGC_420_4384,(0,0,28):C.UVGC_420_4385,(0,0,31):C.UVGC_420_4386,(0,0,33):C.UVGC_420_4387,(0,0,34):C.UVGC_420_4388,(0,0,35):C.UVGC_420_4389,(0,0,37):C.UVGC_420_4390,(0,0,38):C.UVGC_420_4391,(0,0,39):C.UVGC_420_4392,(0,0,41):C.UVGC_420_4393,(0,0,0):C.UVGC_420_4394,(0,0,2):C.UVGC_420_4395,(0,0,4):C.UVGC_420_4396,(0,0,6):C.UVGC_420_4397,(0,0,8):C.UVGC_420_4398,(0,0,10):C.UVGC_420_4399,(0,0,12):C.UVGC_420_4400,(0,0,15):C.UVGC_420_4401,(0,0,17):C.UVGC_420_4402,(0,0,18):C.UVGC_420_4403,(0,0,20):C.UVGC_420_4404,(0,0,23):C.UVGC_420_4405,(0,0,25):C.UVGC_420_4406,(0,0,27):C.UVGC_420_4407,(0,0,29):C.UVGC_420_4408,(0,0,30):C.UVGC_420_4409,(0,0,32):C.UVGC_420_4410,(0,0,36):C.UVGC_420_4411,(0,0,40):C.UVGC_420_4412,(0,0,1):C.UVGC_420_4413,(0,0,13):C.UVGC_420_4414,(0,0,14):C.UVGC_420_4415,(0,0,16):C.UVGC_420_4416,(0,0,24):C.UVGC_420_4417,(0,0,26):C.UVGC_420_4418})

V_235 = CTVertex(name = 'V_235',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_415_4208,(0,0,5):C.UVGC_415_4209,(0,0,7):C.UVGC_415_4210,(0,0,9):C.UVGC_415_4211,(0,0,11):C.UVGC_415_4212,(0,0,17):C.UVGC_415_4213,(0,0,19):C.UVGC_415_4214,(0,0,20):C.UVGC_415_4215,(0,0,26):C.UVGC_415_4216,(0,0,29):C.UVGC_415_4217,(0,0,31):C.UVGC_415_4218,(0,0,32):C.UVGC_415_4219,(0,0,33):C.UVGC_415_4220,(0,0,35):C.UVGC_415_4221,(0,0,36):C.UVGC_415_4222,(0,0,37):C.UVGC_415_4223,(0,0,39):C.UVGC_415_4224,(0,0,0):C.UVGC_415_4225,(0,0,2):C.UVGC_415_4226,(0,0,4):C.UVGC_415_4227,(0,0,6):C.UVGC_415_4228,(0,0,8):C.UVGC_415_4229,(0,0,10):C.UVGC_415_4230,(0,0,12):C.UVGC_415_4231,(0,0,14):C.UVGC_415_4232,(0,0,15):C.UVGC_415_4233,(0,0,16):C.UVGC_415_4234,(0,0,18):C.UVGC_415_4235,(0,0,21):C.UVGC_415_4236,(0,0,23):C.UVGC_415_4237,(0,0,25):C.UVGC_415_4238,(0,0,27):C.UVGC_415_4239,(0,0,28):C.UVGC_415_4240,(0,0,30):C.UVGC_415_4241,(0,0,34):C.UVGC_415_4242,(0,0,38):C.UVGC_415_4243,(0,0,1):C.UVGC_415_4244,(0,0,13):C.UVGC_415_4245,(0,0,22):C.UVGC_415_4246,(0,0,24):C.UVGC_415_4247})

V_236 = CTVertex(name = 'V_236',
                 type = 'UV',
                 particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b], [P.c], [P.d], [P.e__minus__], [P.mu__minus__], [P.s], [P.t], [P.ta__minus__], [P.u] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                 couplings = {(0,1,2):C.UVGC_311_1080,(0,1,9):C.UVGC_326_1283,(0,1,11):C.UVGC_326_1284,(0,1,18):C.UVGC_326_1285,(0,1,0):C.UVGC_326_1286,(0,1,1):C.UVGC_326_1287,(0,1,3):C.UVGC_326_1288,(0,1,4):C.UVGC_326_1289,(0,1,5):C.UVGC_326_1290,(0,1,6):C.UVGC_326_1291,(0,1,7):C.UVGC_326_1292,(0,1,8):C.UVGC_326_1293,(0,1,10):C.UVGC_326_1294,(0,1,12):C.UVGC_326_1295,(0,1,13):C.UVGC_326_1296,(0,1,14):C.UVGC_326_1297,(0,1,15):C.UVGC_326_1298,(0,1,16):C.UVGC_326_1299,(0,1,17):C.UVGC_326_1300,(0,1,19):C.UVGC_326_1301,(0,2,2):C.UVGC_311_1080,(0,2,9):C.UVGC_326_1283,(0,2,11):C.UVGC_326_1284,(0,2,18):C.UVGC_326_1285,(0,2,0):C.UVGC_326_1286,(0,2,1):C.UVGC_326_1287,(0,2,3):C.UVGC_326_1288,(0,2,4):C.UVGC_326_1289,(0,2,5):C.UVGC_326_1290,(0,2,6):C.UVGC_326_1291,(0,2,7):C.UVGC_326_1292,(0,2,8):C.UVGC_326_1293,(0,2,10):C.UVGC_326_1294,(0,2,12):C.UVGC_326_1295,(0,2,13):C.UVGC_326_1296,(0,2,14):C.UVGC_326_1297,(0,2,15):C.UVGC_326_1298,(0,2,16):C.UVGC_326_1299,(0,2,17):C.UVGC_326_1300,(0,2,19):C.UVGC_326_1301,(0,0,2):C.UVGC_311_1080,(0,0,9):C.UVGC_327_1302,(0,0,11):C.UVGC_327_1303,(0,0,18):C.UVGC_327_1304,(0,0,0):C.UVGC_327_1305,(0,0,1):C.UVGC_327_1306,(0,0,3):C.UVGC_327_1307,(0,0,4):C.UVGC_327_1308,(0,0,5):C.UVGC_327_1309,(0,0,6):C.UVGC_327_1310,(0,0,7):C.UVGC_327_1311,(0,0,8):C.UVGC_327_1312,(0,0,10):C.UVGC_327_1313,(0,0,12):C.UVGC_327_1314,(0,0,13):C.UVGC_327_1315,(0,0,14):C.UVGC_327_1316,(0,0,15):C.UVGC_327_1317,(0,0,16):C.UVGC_327_1318,(0,0,17):C.UVGC_327_1319,(0,0,19):C.UVGC_327_1320})

V_237 = CTVertex(name = 'V_237',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV16, L.VVV17, L.VVV18, L.VVV19, L.VVV21, L.VVV24, L.VVV25, L.VVV26 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__], [P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_336_1575,(0,0,4):C.UVGC_336_1576,(0,0,6):C.UVGC_336_1577,(0,0,8):C.UVGC_336_1578,(0,0,17):C.UVGC_336_1579,(0,0,21):C.UVGC_336_1580,(0,0,27):C.UVGC_336_1581,(0,0,29):C.UVGC_336_1582,(0,0,30):C.UVGC_336_1583,(0,0,31):C.UVGC_336_1584,(0,0,33):C.UVGC_336_1585,(0,0,34):C.UVGC_336_1586,(0,0,35):C.UVGC_336_1587,(0,0,37):C.UVGC_336_1588,(0,0,0):C.UVGC_336_1589,(0,0,1):C.UVGC_341_1636,(0,0,3):C.UVGC_336_1591,(0,0,5):C.UVGC_336_1592,(0,0,7):C.UVGC_336_1593,(0,0,9):C.UVGC_336_1594,(0,0,10):C.UVGC_341_1637,(0,0,13):C.UVGC_336_1596,(0,0,15):C.UVGC_341_1638,(0,0,19):C.UVGC_341_1639,(0,0,22):C.UVGC_341_1640,(0,0,23):C.UVGC_336_1600,(0,0,24):C.UVGC_336_1601,(0,0,25):C.UVGC_336_1602,(0,0,26):C.UVGC_336_1603,(0,0,28):C.UVGC_336_1604,(0,0,32):C.UVGC_336_1605,(0,0,36):C.UVGC_341_1641,(0,0,12):C.UVGC_341_1642,(0,1,2):C.UVGC_317_1192,(0,1,4):C.UVGC_317_1193,(0,1,6):C.UVGC_317_1194,(0,1,8):C.UVGC_317_1195,(0,1,17):C.UVGC_317_1196,(0,1,21):C.UVGC_317_1197,(0,1,27):C.UVGC_317_1198,(0,1,29):C.UVGC_317_1199,(0,1,30):C.UVGC_317_1200,(0,1,31):C.UVGC_317_1201,(0,1,33):C.UVGC_317_1202,(0,1,34):C.UVGC_317_1203,(0,1,35):C.UVGC_317_1204,(0,1,37):C.UVGC_317_1205,(0,1,0):C.UVGC_317_1206,(0,1,1):C.UVGC_317_1207,(0,1,3):C.UVGC_317_1208,(0,1,5):C.UVGC_317_1209,(0,1,7):C.UVGC_317_1210,(0,1,9):C.UVGC_317_1211,(0,1,10):C.UVGC_317_1212,(0,1,13):C.UVGC_317_1213,(0,1,15):C.UVGC_317_1214,(0,1,19):C.UVGC_317_1215,(0,1,22):C.UVGC_317_1216,(0,1,23):C.UVGC_317_1217,(0,1,24):C.UVGC_317_1218,(0,1,25):C.UVGC_317_1219,(0,1,26):C.UVGC_317_1220,(0,1,28):C.UVGC_317_1221,(0,1,32):C.UVGC_317_1222,(0,1,36):C.UVGC_317_1223,(0,3,2):C.UVGC_317_1192,(0,3,4):C.UVGC_317_1193,(0,3,6):C.UVGC_317_1194,(0,3,8):C.UVGC_317_1195,(0,3,17):C.UVGC_317_1196,(0,3,21):C.UVGC_317_1197,(0,3,27):C.UVGC_317_1198,(0,3,29):C.UVGC_317_1199,(0,3,30):C.UVGC_317_1200,(0,3,31):C.UVGC_317_1201,(0,3,33):C.UVGC_317_1202,(0,3,34):C.UVGC_317_1203,(0,3,35):C.UVGC_317_1204,(0,3,37):C.UVGC_317_1205,(0,3,0):C.UVGC_317_1206,(0,3,1):C.UVGC_339_1622,(0,3,3):C.UVGC_317_1208,(0,3,5):C.UVGC_317_1209,(0,3,7):C.UVGC_317_1210,(0,3,9):C.UVGC_317_1211,(0,3,10):C.UVGC_339_1623,(0,3,13):C.UVGC_317_1213,(0,3,14):C.UVGC_339_1624,(0,3,16):C.UVGC_339_1625,(0,3,18):C.UVGC_339_1626,(0,3,20):C.UVGC_339_1627,(0,3,22):C.UVGC_339_1628,(0,3,23):C.UVGC_317_1217,(0,3,24):C.UVGC_317_1218,(0,3,25):C.UVGC_317_1219,(0,3,26):C.UVGC_317_1220,(0,3,28):C.UVGC_317_1221,(0,3,32):C.UVGC_317_1222,(0,3,36):C.UVGC_339_1629,(0,3,12):C.UVGC_339_1630,(0,4,2):C.UVGC_336_1575,(0,4,4):C.UVGC_336_1576,(0,4,6):C.UVGC_336_1577,(0,4,8):C.UVGC_336_1578,(0,4,17):C.UVGC_336_1579,(0,4,21):C.UVGC_336_1580,(0,4,27):C.UVGC_336_1581,(0,4,29):C.UVGC_336_1582,(0,4,30):C.UVGC_336_1583,(0,4,31):C.UVGC_336_1584,(0,4,33):C.UVGC_336_1585,(0,4,34):C.UVGC_336_1586,(0,4,35):C.UVGC_338_1615,(0,4,37):C.UVGC_336_1588,(0,4,0):C.UVGC_336_1589,(0,4,1):C.UVGC_338_1616,(0,4,3):C.UVGC_336_1591,(0,4,5):C.UVGC_336_1592,(0,4,7):C.UVGC_336_1593,(0,4,9):C.UVGC_336_1594,(0,4,10):C.UVGC_336_1595,(0,4,13):C.UVGC_336_1596,(0,4,14):C.UVGC_338_1617,(0,4,16):C.UVGC_338_1618,(0,4,18):C.UVGC_338_1619,(0,4,20):C.UVGC_338_1620,(0,4,22):C.UVGC_336_1599,(0,4,23):C.UVGC_336_1600,(0,4,24):C.UVGC_336_1601,(0,4,25):C.UVGC_336_1602,(0,4,26):C.UVGC_336_1603,(0,4,28):C.UVGC_336_1604,(0,4,32):C.UVGC_336_1605,(0,4,36):C.UVGC_338_1621,(0,4,12):C.UVGC_336_1607,(0,6,2):C.UVGC_336_1575,(0,6,4):C.UVGC_336_1576,(0,6,6):C.UVGC_336_1577,(0,6,8):C.UVGC_336_1578,(0,6,17):C.UVGC_336_1579,(0,6,21):C.UVGC_336_1580,(0,6,27):C.UVGC_336_1581,(0,6,29):C.UVGC_336_1582,(0,6,30):C.UVGC_336_1583,(0,6,31):C.UVGC_336_1584,(0,6,33):C.UVGC_336_1585,(0,6,34):C.UVGC_336_1586,(0,6,35):C.UVGC_336_1587,(0,6,37):C.UVGC_336_1588,(0,6,0):C.UVGC_336_1589,(0,6,1):C.UVGC_336_1590,(0,6,3):C.UVGC_336_1591,(0,6,5):C.UVGC_336_1592,(0,6,7):C.UVGC_336_1593,(0,6,9):C.UVGC_336_1594,(0,6,10):C.UVGC_336_1595,(0,6,13):C.UVGC_336_1596,(0,6,15):C.UVGC_336_1597,(0,6,19):C.UVGC_336_1598,(0,6,22):C.UVGC_336_1599,(0,6,23):C.UVGC_336_1600,(0,6,24):C.UVGC_336_1601,(0,6,25):C.UVGC_336_1602,(0,6,26):C.UVGC_336_1603,(0,6,28):C.UVGC_336_1604,(0,6,32):C.UVGC_336_1605,(0,6,36):C.UVGC_336_1606,(0,6,12):C.UVGC_336_1607,(0,7,2):C.UVGC_317_1192,(0,7,4):C.UVGC_317_1193,(0,7,6):C.UVGC_317_1194,(0,7,8):C.UVGC_317_1195,(0,7,17):C.UVGC_317_1196,(0,7,21):C.UVGC_317_1197,(0,7,27):C.UVGC_317_1198,(0,7,29):C.UVGC_317_1199,(0,7,30):C.UVGC_317_1200,(0,7,31):C.UVGC_317_1201,(0,7,33):C.UVGC_317_1202,(0,7,34):C.UVGC_317_1203,(0,7,35):C.UVGC_340_1631,(0,7,37):C.UVGC_317_1205,(0,7,0):C.UVGC_317_1206,(0,7,1):C.UVGC_340_1632,(0,7,3):C.UVGC_317_1208,(0,7,5):C.UVGC_317_1209,(0,7,7):C.UVGC_317_1210,(0,7,9):C.UVGC_317_1211,(0,7,10):C.UVGC_339_1623,(0,7,13):C.UVGC_317_1213,(0,7,15):C.UVGC_340_1633,(0,7,19):C.UVGC_340_1634,(0,7,22):C.UVGC_339_1628,(0,7,23):C.UVGC_317_1217,(0,7,24):C.UVGC_317_1218,(0,7,25):C.UVGC_317_1219,(0,7,26):C.UVGC_317_1220,(0,7,28):C.UVGC_317_1221,(0,7,32):C.UVGC_317_1222,(0,7,36):C.UVGC_340_1635,(0,7,12):C.UVGC_339_1630,(0,2,1):C.UVGC_337_1608,(0,2,11):C.UVGC_337_1609,(0,2,14):C.UVGC_337_1610,(0,2,16):C.UVGC_337_1611,(0,2,18):C.UVGC_337_1612,(0,2,20):C.UVGC_337_1613,(0,2,36):C.UVGC_337_1614,(0,2,12):C.UVGC_336_1607,(0,5,1):C.UVGC_137_6,(0,5,14):C.UVGC_320_1246,(0,5,16):C.UVGC_320_1247,(0,5,18):C.UVGC_320_1248,(0,5,20):C.UVGC_320_1249,(0,5,36):C.UVGC_139_8})

V_238 = CTVertex(name = 'V_238',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                 loop_particles = [ [ [P.a] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0], [P.H] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghA, P.ghWm, P.ghWp] ], [ [P.ghA, P.ghWm, P.ghWp, P.ghZ] ], [ [P.ghA, P.ghWm, P.ghZ], [P.ghA, P.ghWp, P.ghZ] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghWp, P.ghZ] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,0):C.UVGC_432_4749,(0,1,5):C.UVGC_432_4750,(0,1,7):C.UVGC_432_4751,(0,1,9):C.UVGC_432_4752,(0,1,11):C.UVGC_432_4753,(0,1,14):C.UVGC_420_4417,(0,1,20):C.UVGC_432_4754,(0,1,23):C.UVGC_432_4755,(0,1,29):C.UVGC_432_4756,(0,1,31):C.UVGC_432_4757,(0,1,32):C.UVGC_432_4758,(0,1,33):C.UVGC_432_4759,(0,1,35):C.UVGC_432_4760,(0,1,36):C.UVGC_432_4761,(0,1,37):C.UVGC_432_4762,(0,1,39):C.UVGC_432_4763,(0,1,1):C.UVGC_432_4764,(0,1,2):C.UVGC_432_4765,(0,1,4):C.UVGC_432_4766,(0,1,6):C.UVGC_432_4767,(0,1,8):C.UVGC_432_4768,(0,1,10):C.UVGC_432_4769,(0,1,12):C.UVGC_432_4770,(0,1,13):C.UVGC_432_4771,(0,1,15):C.UVGC_432_4772,(0,1,16):C.UVGC_432_4773,(0,1,22):C.UVGC_432_4774,(0,1,24):C.UVGC_432_4775,(0,1,25):C.UVGC_432_4776,(0,1,26):C.UVGC_432_4777,(0,1,27):C.UVGC_432_4778,(0,1,28):C.UVGC_432_4779,(0,1,30):C.UVGC_432_4780,(0,1,34):C.UVGC_432_4781,(0,1,38):C.UVGC_432_4782,(0,1,3):C.UVGC_432_4783,(0,1,17):C.UVGC_432_4784,(0,1,19):C.UVGC_432_4785,(0,1,21):C.UVGC_432_4786,(0,1,18):C.UVGC_432_4787,(0,2,0):C.UVGC_432_4749,(0,2,5):C.UVGC_432_4750,(0,2,7):C.UVGC_432_4751,(0,2,9):C.UVGC_432_4752,(0,2,11):C.UVGC_432_4753,(0,2,14):C.UVGC_420_4417,(0,2,20):C.UVGC_432_4754,(0,2,23):C.UVGC_432_4755,(0,2,29):C.UVGC_432_4756,(0,2,31):C.UVGC_432_4757,(0,2,32):C.UVGC_432_4758,(0,2,33):C.UVGC_432_4759,(0,2,35):C.UVGC_432_4760,(0,2,36):C.UVGC_432_4761,(0,2,37):C.UVGC_432_4762,(0,2,39):C.UVGC_432_4763,(0,2,1):C.UVGC_432_4764,(0,2,2):C.UVGC_432_4765,(0,2,4):C.UVGC_432_4766,(0,2,6):C.UVGC_432_4767,(0,2,8):C.UVGC_432_4768,(0,2,10):C.UVGC_432_4769,(0,2,12):C.UVGC_432_4770,(0,2,13):C.UVGC_432_4771,(0,2,15):C.UVGC_432_4772,(0,2,16):C.UVGC_432_4773,(0,2,22):C.UVGC_432_4774,(0,2,24):C.UVGC_432_4775,(0,2,25):C.UVGC_432_4776,(0,2,26):C.UVGC_432_4777,(0,2,27):C.UVGC_432_4778,(0,2,28):C.UVGC_432_4779,(0,2,30):C.UVGC_432_4780,(0,2,34):C.UVGC_432_4781,(0,2,38):C.UVGC_432_4782,(0,2,3):C.UVGC_432_4783,(0,2,17):C.UVGC_432_4784,(0,2,19):C.UVGC_432_4785,(0,2,21):C.UVGC_432_4786,(0,2,18):C.UVGC_432_4787,(0,0,0):C.UVGC_433_4788,(0,0,5):C.UVGC_433_4789,(0,0,7):C.UVGC_433_4790,(0,0,9):C.UVGC_433_4791,(0,0,11):C.UVGC_433_4792,(0,0,20):C.UVGC_433_4793,(0,0,23):C.UVGC_433_4794,(0,0,29):C.UVGC_433_4795,(0,0,31):C.UVGC_433_4796,(0,0,32):C.UVGC_433_4797,(0,0,33):C.UVGC_433_4798,(0,0,35):C.UVGC_433_4799,(0,0,36):C.UVGC_433_4800,(0,0,37):C.UVGC_433_4801,(0,0,39):C.UVGC_433_4802,(0,0,1):C.UVGC_433_4803,(0,0,2):C.UVGC_433_4804,(0,0,4):C.UVGC_433_4805,(0,0,6):C.UVGC_433_4806,(0,0,8):C.UVGC_433_4807,(0,0,10):C.UVGC_433_4808,(0,0,12):C.UVGC_433_4809,(0,0,13):C.UVGC_433_4810,(0,0,15):C.UVGC_433_4811,(0,0,16):C.UVGC_433_4812,(0,0,22):C.UVGC_433_4813,(0,0,24):C.UVGC_433_4814,(0,0,25):C.UVGC_433_4815,(0,0,26):C.UVGC_433_4816,(0,0,27):C.UVGC_433_4817,(0,0,28):C.UVGC_433_4818,(0,0,30):C.UVGC_433_4819,(0,0,34):C.UVGC_433_4820,(0,0,38):C.UVGC_433_4821,(0,0,3):C.UVGC_433_4822,(0,0,17):C.UVGC_432_4784,(0,0,19):C.UVGC_432_4785,(0,0,21):C.UVGC_432_4786,(0,0,18):C.UVGC_432_4787})

V_239 = CTVertex(name = 'V_239',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS8 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.Z] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.ve, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.ve, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_389_3304,(0,0,6):C.UVGC_389_3305,(0,0,8):C.UVGC_389_3306,(0,0,10):C.UVGC_389_3307,(0,0,20):C.UVGC_389_3308,(0,0,25):C.UVGC_389_3309,(0,0,27):C.UVGC_389_3310,(0,0,33):C.UVGC_389_3311,(0,0,36):C.UVGC_389_3312,(0,0,38):C.UVGC_389_3313,(0,0,39):C.UVGC_389_3314,(0,0,40):C.UVGC_389_3315,(0,0,42):C.UVGC_389_3316,(0,0,43):C.UVGC_389_3317,(0,0,46):C.UVGC_389_3318,(0,0,48):C.UVGC_389_3319,(0,0,0):C.UVGC_389_3320,(0,0,2):C.UVGC_389_3321,(0,0,3):C.UVGC_389_3322,(0,0,5):C.UVGC_389_3323,(0,0,7):C.UVGC_389_3324,(0,0,9):C.UVGC_389_3325,(0,0,11):C.UVGC_389_3326,(0,0,13):C.UVGC_389_3327,(0,0,15):C.UVGC_389_3328,(0,0,16):C.UVGC_389_3329,(0,0,18):C.UVGC_389_3330,(0,0,19):C.UVGC_389_3331,(0,0,21):C.UVGC_389_3332,(0,0,22):C.UVGC_389_3333,(0,0,23):C.UVGC_389_3334,(0,0,24):C.UVGC_389_3335,(0,0,26):C.UVGC_389_3336,(0,0,28):C.UVGC_389_3337,(0,0,29):C.UVGC_389_3338,(0,0,31):C.UVGC_389_3339,(0,0,32):C.UVGC_389_3340,(0,0,34):C.UVGC_389_3341,(0,0,35):C.UVGC_389_3342,(0,0,37):C.UVGC_389_3343,(0,0,41):C.UVGC_389_3344,(0,0,44):C.UVGC_389_3345,(0,0,45):C.UVGC_389_3346,(0,0,47):C.UVGC_389_3347,(0,0,1):C.UVGC_389_3348,(0,0,12):C.UVGC_389_3349,(0,0,14):C.UVGC_389_3350,(0,0,17):C.UVGC_389_3351,(0,0,30):C.UVGC_389_3352})

V_240 = CTVertex(name = 'V_240',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.mu__minus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.vm, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_394_3502,(0,0,6):C.UVGC_394_3503,(0,0,8):C.UVGC_394_3504,(0,0,10):C.UVGC_394_3505,(0,0,12):C.UVGC_394_3506,(0,0,19):C.UVGC_394_3507,(0,0,21):C.UVGC_394_3508,(0,0,29):C.UVGC_394_3509,(0,0,33):C.UVGC_394_3510,(0,0,38):C.UVGC_394_3511,(0,0,39):C.UVGC_394_3512,(0,0,40):C.UVGC_394_3513,(0,0,42):C.UVGC_394_3514,(0,0,43):C.UVGC_394_3515,(0,0,46):C.UVGC_394_3516,(0,0,48):C.UVGC_394_3517,(0,0,0):C.UVGC_394_3518,(0,0,2):C.UVGC_394_3519,(0,0,3):C.UVGC_394_3520,(0,0,5):C.UVGC_394_3521,(0,0,7):C.UVGC_394_3522,(0,0,9):C.UVGC_394_3523,(0,0,11):C.UVGC_394_3524,(0,0,13):C.UVGC_394_3525,(0,0,14):C.UVGC_394_3526,(0,0,15):C.UVGC_394_3527,(0,0,17):C.UVGC_394_3528,(0,0,18):C.UVGC_394_3529,(0,0,20):C.UVGC_394_3530,(0,0,22):C.UVGC_394_3531,(0,0,23):C.UVGC_394_3532,(0,0,25):C.UVGC_394_3533,(0,0,27):C.UVGC_394_3534,(0,0,28):C.UVGC_394_3535,(0,0,30):C.UVGC_394_3536,(0,0,31):C.UVGC_394_3537,(0,0,32):C.UVGC_394_3538,(0,0,34):C.UVGC_394_3539,(0,0,36):C.UVGC_394_3540,(0,0,37):C.UVGC_394_3541,(0,0,41):C.UVGC_394_3542,(0,0,44):C.UVGC_394_3543,(0,0,45):C.UVGC_394_3544,(0,0,47):C.UVGC_394_3545,(0,0,1):C.UVGC_394_3546,(0,0,16):C.UVGC_394_3547,(0,0,24):C.UVGC_394_3548,(0,0,26):C.UVGC_394_3549,(0,0,35):C.UVGC_394_3550})

V_241 = CTVertex(name = 'V_241',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ta__minus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.vt, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_399_3695,(0,0,6):C.UVGC_399_3696,(0,0,8):C.UVGC_399_3697,(0,0,10):C.UVGC_399_3698,(0,0,12):C.UVGC_399_3699,(0,0,19):C.UVGC_399_3700,(0,0,21):C.UVGC_399_3701,(0,0,29):C.UVGC_399_3702,(0,0,33):C.UVGC_399_3703,(0,0,35):C.UVGC_399_3704,(0,0,36):C.UVGC_399_3705,(0,0,37):C.UVGC_399_3706,(0,0,42):C.UVGC_399_3707,(0,0,43):C.UVGC_399_3708,(0,0,46):C.UVGC_399_3709,(0,0,48):C.UVGC_399_3710,(0,0,0):C.UVGC_399_3711,(0,0,2):C.UVGC_399_3712,(0,0,3):C.UVGC_399_3713,(0,0,5):C.UVGC_399_3714,(0,0,7):C.UVGC_399_3715,(0,0,9):C.UVGC_399_3716,(0,0,11):C.UVGC_399_3717,(0,0,13):C.UVGC_399_3718,(0,0,14):C.UVGC_399_3719,(0,0,15):C.UVGC_399_3720,(0,0,17):C.UVGC_399_3721,(0,0,18):C.UVGC_399_3722,(0,0,20):C.UVGC_399_3723,(0,0,22):C.UVGC_399_3724,(0,0,23):C.UVGC_399_3725,(0,0,25):C.UVGC_399_3726,(0,0,27):C.UVGC_399_3727,(0,0,28):C.UVGC_399_3728,(0,0,30):C.UVGC_399_3729,(0,0,31):C.UVGC_399_3730,(0,0,32):C.UVGC_399_3731,(0,0,34):C.UVGC_399_3732,(0,0,38):C.UVGC_399_3733,(0,0,40):C.UVGC_399_3734,(0,0,41):C.UVGC_399_3735,(0,0,44):C.UVGC_399_3736,(0,0,45):C.UVGC_399_3737,(0,0,47):C.UVGC_399_3738,(0,0,1):C.UVGC_399_3739,(0,0,16):C.UVGC_399_3740,(0,0,24):C.UVGC_399_3741,(0,0,26):C.UVGC_399_3742,(0,0,39):C.UVGC_399_3743})

V_242 = CTVertex(name = 'V_242',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_403_3815,(0,0,4):C.UVGC_403_3816,(0,0,6):C.UVGC_403_3817,(0,0,8):C.UVGC_403_3818,(0,0,15):C.UVGC_403_3819,(0,0,17):C.UVGC_403_3820,(0,0,23):C.UVGC_403_3821,(0,0,25):C.UVGC_403_3822,(0,0,26):C.UVGC_403_3823,(0,0,27):C.UVGC_403_3824,(0,0,29):C.UVGC_403_3825,(0,0,30):C.UVGC_403_3826,(0,0,31):C.UVGC_403_3827,(0,0,33):C.UVGC_403_3828,(0,0,0):C.UVGC_403_3829,(0,0,1):C.UVGC_403_3830,(0,0,3):C.UVGC_403_3831,(0,0,5):C.UVGC_403_3832,(0,0,7):C.UVGC_403_3833,(0,0,9):C.UVGC_403_3834,(0,0,10):C.UVGC_403_3835,(0,0,11):C.UVGC_403_3836,(0,0,13):C.UVGC_403_3837,(0,0,14):C.UVGC_403_3838,(0,0,16):C.UVGC_403_3839,(0,0,18):C.UVGC_403_3840,(0,0,19):C.UVGC_403_3841,(0,0,20):C.UVGC_403_3842,(0,0,21):C.UVGC_403_3843,(0,0,22):C.UVGC_403_3844,(0,0,24):C.UVGC_403_3845,(0,0,28):C.UVGC_403_3846,(0,0,32):C.UVGC_403_3847,(0,0,12):C.UVGC_403_3848})

V_243 = CTVertex(name = 'V_243',
                 type = 'UV',
                 particles = [ P.Z, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_408_3995,(0,0,4):C.UVGC_408_3996,(0,0,6):C.UVGC_408_3997,(0,0,8):C.UVGC_408_3998,(0,0,10):C.UVGC_408_3999,(0,0,16):C.UVGC_408_4000,(0,0,18):C.UVGC_408_4001,(0,0,19):C.UVGC_408_4002,(0,0,23):C.UVGC_408_4003,(0,0,26):C.UVGC_408_4004,(0,0,28):C.UVGC_408_4005,(0,0,29):C.UVGC_408_4006,(0,0,30):C.UVGC_408_4007,(0,0,32):C.UVGC_408_4008,(0,0,33):C.UVGC_408_4009,(0,0,34):C.UVGC_408_4010,(0,0,36):C.UVGC_408_4011,(0,0,0):C.UVGC_408_4012,(0,0,1):C.UVGC_408_4013,(0,0,3):C.UVGC_408_4014,(0,0,5):C.UVGC_408_4015,(0,0,7):C.UVGC_408_4016,(0,0,9):C.UVGC_408_4017,(0,0,11):C.UVGC_408_4018,(0,0,12):C.UVGC_408_4019,(0,0,14):C.UVGC_408_4020,(0,0,15):C.UVGC_408_4021,(0,0,17):C.UVGC_408_4022,(0,0,20):C.UVGC_408_4023,(0,0,21):C.UVGC_408_4024,(0,0,22):C.UVGC_408_4025,(0,0,24):C.UVGC_408_4026,(0,0,25):C.UVGC_408_4027,(0,0,27):C.UVGC_408_4028,(0,0,31):C.UVGC_408_4029,(0,0,35):C.UVGC_408_4030,(0,0,13):C.UVGC_408_4031,(0,1,2):C.UVGC_405_3884,(0,1,4):C.UVGC_405_3885,(0,1,6):C.UVGC_405_3886,(0,1,8):C.UVGC_405_3887,(0,1,10):C.UVGC_405_3888,(0,1,16):C.UVGC_405_3889,(0,1,18):C.UVGC_405_3890,(0,1,19):C.UVGC_405_3891,(0,1,23):C.UVGC_405_3892,(0,1,26):C.UVGC_405_3893,(0,1,28):C.UVGC_405_3894,(0,1,29):C.UVGC_405_3895,(0,1,30):C.UVGC_405_3896,(0,1,32):C.UVGC_405_3897,(0,1,33):C.UVGC_405_3898,(0,1,34):C.UVGC_405_3899,(0,1,36):C.UVGC_405_3900,(0,1,0):C.UVGC_405_3901,(0,1,1):C.UVGC_405_3902,(0,1,3):C.UVGC_405_3903,(0,1,5):C.UVGC_405_3904,(0,1,7):C.UVGC_405_3905,(0,1,9):C.UVGC_405_3906,(0,1,11):C.UVGC_405_3907,(0,1,12):C.UVGC_405_3908,(0,1,14):C.UVGC_405_3909,(0,1,15):C.UVGC_405_3910,(0,1,17):C.UVGC_405_3911,(0,1,20):C.UVGC_405_3912,(0,1,21):C.UVGC_405_3913,(0,1,22):C.UVGC_405_3914,(0,1,24):C.UVGC_405_3915,(0,1,25):C.UVGC_405_3916,(0,1,27):C.UVGC_405_3917,(0,1,31):C.UVGC_405_3918,(0,1,35):C.UVGC_405_3919,(0,1,13):C.UVGC_405_3920})

V_244 = CTVertex(name = 'V_244',
                 type = 'UV',
                 particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS5, L.VSS8 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_401_3753,(0,0,4):C.UVGC_401_3754,(0,0,6):C.UVGC_401_3755,(0,0,8):C.UVGC_401_3756,(0,0,15):C.UVGC_401_3757,(0,0,17):C.UVGC_401_3758,(0,0,23):C.UVGC_401_3759,(0,0,25):C.UVGC_401_3760,(0,0,26):C.UVGC_401_3761,(0,0,27):C.UVGC_401_3762,(0,0,29):C.UVGC_401_3763,(0,0,30):C.UVGC_335_1547,(0,0,31):C.UVGC_401_3764,(0,0,33):C.UVGC_335_1549,(0,0,0):C.UVGC_335_1551,(0,0,1):C.UVGC_401_3765,(0,0,3):C.UVGC_401_3766,(0,0,5):C.UVGC_401_3767,(0,0,7):C.UVGC_401_3768,(0,0,9):C.UVGC_401_3769,(0,0,10):C.UVGC_401_3770,(0,0,11):C.UVGC_335_1561,(0,0,13):C.UVGC_401_3771,(0,0,14):C.UVGC_335_1562,(0,0,16):C.UVGC_401_3772,(0,0,18):C.UVGC_401_3773,(0,0,19):C.UVGC_401_3774,(0,0,20):C.UVGC_401_3775,(0,0,21):C.UVGC_401_3776,(0,0,22):C.UVGC_335_1569,(0,0,24):C.UVGC_401_3777,(0,0,28):C.UVGC_401_3778,(0,0,32):C.UVGC_401_3779,(0,0,12):C.UVGC_401_3780,(0,1,2):C.UVGC_402_3781,(0,1,4):C.UVGC_402_3782,(0,1,6):C.UVGC_402_3783,(0,1,8):C.UVGC_402_3784,(0,1,15):C.UVGC_402_3785,(0,1,17):C.UVGC_402_3786,(0,1,23):C.UVGC_402_3787,(0,1,25):C.UVGC_402_3788,(0,1,26):C.UVGC_402_3789,(0,1,27):C.UVGC_402_3790,(0,1,29):C.UVGC_402_3791,(0,1,30):C.UVGC_402_3792,(0,1,31):C.UVGC_402_3793,(0,1,33):C.UVGC_402_3794,(0,1,0):C.UVGC_402_3795,(0,1,1):C.UVGC_402_3796,(0,1,3):C.UVGC_402_3797,(0,1,5):C.UVGC_402_3798,(0,1,7):C.UVGC_402_3799,(0,1,9):C.UVGC_402_3800,(0,1,10):C.UVGC_402_3801,(0,1,11):C.UVGC_402_3802,(0,1,13):C.UVGC_402_3803,(0,1,14):C.UVGC_402_3804,(0,1,16):C.UVGC_402_3805,(0,1,18):C.UVGC_402_3806,(0,1,19):C.UVGC_402_3807,(0,1,20):C.UVGC_402_3808,(0,1,21):C.UVGC_402_3809,(0,1,22):C.UVGC_402_3810,(0,1,24):C.UVGC_402_3811,(0,1,28):C.UVGC_402_3812,(0,1,32):C.UVGC_402_3813,(0,1,12):C.UVGC_402_3814})

V_245 = CTVertex(name = 'V_245',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_435_4872,(0,0,5):C.UVGC_435_4873,(0,0,7):C.UVGC_435_4874,(0,0,9):C.UVGC_435_4875,(0,0,23):C.UVGC_435_4876,(0,0,25):C.UVGC_435_4877,(0,0,34):C.UVGC_435_4878,(0,0,36):C.UVGC_435_4879,(0,0,37):C.UVGC_435_4880,(0,0,38):C.UVGC_435_4881,(0,0,40):C.UVGC_435_4882,(0,0,41):C.UVGC_435_4883,(0,0,42):C.UVGC_435_4884,(0,0,44):C.UVGC_435_4885,(0,0,0):C.UVGC_435_4886,(0,0,2):C.UVGC_435_4887,(0,0,4):C.UVGC_435_4888,(0,0,6):C.UVGC_435_4889,(0,0,8):C.UVGC_435_4890,(0,0,10):C.UVGC_435_4891,(0,0,11):C.UVGC_435_4892,(0,0,16):C.UVGC_435_4893,(0,0,19):C.UVGC_435_4894,(0,0,21):C.UVGC_435_4895,(0,0,22):C.UVGC_435_4896,(0,0,24):C.UVGC_435_4897,(0,0,26):C.UVGC_435_4898,(0,0,28):C.UVGC_435_4899,(0,0,30):C.UVGC_435_4900,(0,0,31):C.UVGC_435_4901,(0,0,33):C.UVGC_435_4902,(0,0,35):C.UVGC_435_4903,(0,0,39):C.UVGC_435_4904,(0,0,43):C.UVGC_435_4905,(0,0,1):C.UVGC_435_4906,(0,0,12):C.UVGC_435_4907,(0,0,14):C.UVGC_435_4908,(0,0,15):C.UVGC_435_4909,(0,0,17):C.UVGC_435_4910,(0,0,18):C.UVGC_435_4911,(0,0,20):C.UVGC_435_4912,(0,0,27):C.UVGC_435_4913,(0,0,29):C.UVGC_435_4914,(0,0,32):C.UVGC_435_4915,(0,0,13):C.UVGC_435_4916})

V_246 = CTVertex(name = 'V_246',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_434_4823,(0,0,5):C.UVGC_434_4824,(0,0,7):C.UVGC_434_4825,(0,0,9):C.UVGC_434_4826,(0,0,11):C.UVGC_434_4827,(0,0,23):C.UVGC_434_4828,(0,0,25):C.UVGC_434_4829,(0,0,26):C.UVGC_434_4830,(0,0,27):C.UVGC_434_4831,(0,0,34):C.UVGC_434_4832,(0,0,38):C.UVGC_434_4833,(0,0,40):C.UVGC_434_4834,(0,0,41):C.UVGC_434_4835,(0,0,42):C.UVGC_434_4836,(0,0,44):C.UVGC_434_4837,(0,0,45):C.UVGC_434_4838,(0,0,46):C.UVGC_434_4839,(0,0,48):C.UVGC_434_4840,(0,0,0):C.UVGC_434_4841,(0,0,2):C.UVGC_434_4842,(0,0,4):C.UVGC_434_4843,(0,0,6):C.UVGC_434_4844,(0,0,8):C.UVGC_434_4845,(0,0,10):C.UVGC_434_4846,(0,0,12):C.UVGC_434_4847,(0,0,17):C.UVGC_434_4848,(0,0,19):C.UVGC_434_4849,(0,0,21):C.UVGC_434_4850,(0,0,22):C.UVGC_434_4851,(0,0,24):C.UVGC_434_4852,(0,0,28):C.UVGC_434_4853,(0,0,31):C.UVGC_434_4854,(0,0,33):C.UVGC_434_4855,(0,0,35):C.UVGC_434_4856,(0,0,37):C.UVGC_434_4857,(0,0,39):C.UVGC_434_4858,(0,0,43):C.UVGC_434_4859,(0,0,47):C.UVGC_434_4860,(0,0,1):C.UVGC_434_4861,(0,0,13):C.UVGC_434_4862,(0,0,15):C.UVGC_434_4863,(0,0,16):C.UVGC_434_4864,(0,0,18):C.UVGC_434_4865,(0,0,20):C.UVGC_434_4866,(0,0,29):C.UVGC_434_4867,(0,0,30):C.UVGC_434_4868,(0,0,32):C.UVGC_434_4869,(0,0,36):C.UVGC_434_4870,(0,0,14):C.UVGC_434_4871})

V_247 = CTVertex(name = 'V_247',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_422_4461,(0,0,5):C.UVGC_422_4462,(0,0,7):C.UVGC_422_4463,(0,0,9):C.UVGC_422_4464,(0,0,11):C.UVGC_422_4465,(0,0,20):C.UVGC_422_4466,(0,0,23):C.UVGC_422_4467,(0,0,30):C.UVGC_422_4468,(0,0,34):C.UVGC_422_4469,(0,0,36):C.UVGC_422_4470,(0,0,37):C.UVGC_422_4471,(0,0,38):C.UVGC_422_4472,(0,0,40):C.UVGC_422_4473,(0,0,41):C.UVGC_422_4474,(0,0,42):C.UVGC_422_4475,(0,0,44):C.UVGC_422_4476,(0,0,0):C.UVGC_422_4477,(0,0,2):C.UVGC_422_4478,(0,0,4):C.UVGC_422_4479,(0,0,6):C.UVGC_422_4480,(0,0,8):C.UVGC_422_4481,(0,0,10):C.UVGC_422_4482,(0,0,12):C.UVGC_422_4483,(0,0,15):C.UVGC_422_4484,(0,0,17):C.UVGC_422_4485,(0,0,18):C.UVGC_422_4486,(0,0,19):C.UVGC_422_4487,(0,0,21):C.UVGC_422_4488,(0,0,22):C.UVGC_422_4489,(0,0,24):C.UVGC_422_4490,(0,0,27):C.UVGC_422_4491,(0,0,29):C.UVGC_422_4492,(0,0,31):C.UVGC_422_4493,(0,0,33):C.UVGC_422_4494,(0,0,35):C.UVGC_422_4495,(0,0,39):C.UVGC_422_4496,(0,0,43):C.UVGC_422_4497,(0,0,1):C.UVGC_422_4498,(0,0,13):C.UVGC_422_4499,(0,0,14):C.UVGC_422_4500,(0,0,16):C.UVGC_422_4501,(0,0,25):C.UVGC_422_4502,(0,0,26):C.UVGC_422_4503,(0,0,28):C.UVGC_422_4504,(0,0,32):C.UVGC_422_4505})

V_248 = CTVertex(name = 'V_248',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_435_4872,(0,0,5):C.UVGC_435_4873,(0,0,7):C.UVGC_435_4874,(0,0,9):C.UVGC_435_4875,(0,0,23):C.UVGC_435_4876,(0,0,25):C.UVGC_435_4877,(0,0,34):C.UVGC_435_4878,(0,0,36):C.UVGC_435_4879,(0,0,37):C.UVGC_435_4880,(0,0,38):C.UVGC_435_4881,(0,0,40):C.UVGC_435_4882,(0,0,41):C.UVGC_435_4883,(0,0,42):C.UVGC_435_4884,(0,0,44):C.UVGC_435_4885,(0,0,0):C.UVGC_435_4886,(0,0,2):C.UVGC_435_4887,(0,0,4):C.UVGC_435_4888,(0,0,6):C.UVGC_435_4889,(0,0,8):C.UVGC_435_4890,(0,0,10):C.UVGC_435_4891,(0,0,11):C.UVGC_435_4892,(0,0,16):C.UVGC_435_4893,(0,0,19):C.UVGC_435_4894,(0,0,21):C.UVGC_435_4895,(0,0,22):C.UVGC_435_4896,(0,0,24):C.UVGC_435_4897,(0,0,26):C.UVGC_435_4898,(0,0,28):C.UVGC_435_4899,(0,0,30):C.UVGC_435_4900,(0,0,31):C.UVGC_435_4901,(0,0,33):C.UVGC_435_4902,(0,0,35):C.UVGC_435_4903,(0,0,39):C.UVGC_435_4904,(0,0,43):C.UVGC_435_4905,(0,0,1):C.UVGC_435_4906,(0,0,12):C.UVGC_435_4907,(0,0,14):C.UVGC_435_4908,(0,0,15):C.UVGC_435_4909,(0,0,17):C.UVGC_435_4910,(0,0,18):C.UVGC_435_4911,(0,0,20):C.UVGC_435_4912,(0,0,27):C.UVGC_435_4913,(0,0,29):C.UVGC_435_4914,(0,0,32):C.UVGC_435_4915,(0,0,13):C.UVGC_435_4916})

V_249 = CTVertex(name = 'V_249',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_436_4917,(0,0,5):C.UVGC_436_4918,(0,0,7):C.UVGC_436_4919,(0,0,9):C.UVGC_436_4920,(0,0,11):C.UVGC_436_4921,(0,0,23):C.UVGC_436_4922,(0,0,25):C.UVGC_436_4923,(0,0,26):C.UVGC_436_4924,(0,0,27):C.UVGC_436_4925,(0,0,34):C.UVGC_436_4926,(0,0,38):C.UVGC_436_4927,(0,0,40):C.UVGC_436_4928,(0,0,41):C.UVGC_436_4929,(0,0,42):C.UVGC_436_4930,(0,0,44):C.UVGC_436_4931,(0,0,45):C.UVGC_436_4932,(0,0,46):C.UVGC_436_4933,(0,0,48):C.UVGC_436_4934,(0,0,0):C.UVGC_436_4935,(0,0,2):C.UVGC_436_4936,(0,0,4):C.UVGC_436_4937,(0,0,6):C.UVGC_436_4938,(0,0,8):C.UVGC_436_4939,(0,0,10):C.UVGC_436_4940,(0,0,12):C.UVGC_436_4941,(0,0,17):C.UVGC_436_4942,(0,0,19):C.UVGC_436_4943,(0,0,21):C.UVGC_436_4944,(0,0,22):C.UVGC_436_4945,(0,0,24):C.UVGC_436_4946,(0,0,28):C.UVGC_436_4947,(0,0,31):C.UVGC_436_4948,(0,0,33):C.UVGC_436_4949,(0,0,35):C.UVGC_436_4950,(0,0,37):C.UVGC_436_4951,(0,0,39):C.UVGC_436_4952,(0,0,43):C.UVGC_436_4953,(0,0,47):C.UVGC_436_4954,(0,0,1):C.UVGC_436_4955,(0,0,13):C.UVGC_436_4956,(0,0,15):C.UVGC_434_4867,(0,0,16):C.UVGC_436_4957,(0,0,18):C.UVGC_436_4958,(0,0,20):C.UVGC_436_4959,(0,0,29):C.UVGC_434_4863,(0,0,30):C.UVGC_434_4871,(0,0,32):C.UVGC_436_4960,(0,0,36):C.UVGC_436_4961,(0,0,14):C.UVGC_434_4868})

V_250 = CTVertex(name = 'V_250',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,3):C.UVGC_427_4592,(0,0,5):C.UVGC_427_4593,(0,0,7):C.UVGC_427_4594,(0,0,9):C.UVGC_427_4595,(0,0,11):C.UVGC_427_4596,(0,0,20):C.UVGC_427_4597,(0,0,23):C.UVGC_427_4598,(0,0,30):C.UVGC_427_4599,(0,0,34):C.UVGC_427_4600,(0,0,36):C.UVGC_427_4601,(0,0,37):C.UVGC_427_4602,(0,0,38):C.UVGC_427_4603,(0,0,40):C.UVGC_427_4604,(0,0,41):C.UVGC_427_4605,(0,0,42):C.UVGC_427_4606,(0,0,44):C.UVGC_427_4607,(0,0,0):C.UVGC_427_4608,(0,0,2):C.UVGC_427_4609,(0,0,4):C.UVGC_427_4610,(0,0,6):C.UVGC_427_4611,(0,0,8):C.UVGC_427_4612,(0,0,10):C.UVGC_427_4613,(0,0,12):C.UVGC_427_4614,(0,0,15):C.UVGC_427_4615,(0,0,17):C.UVGC_427_4616,(0,0,18):C.UVGC_427_4617,(0,0,19):C.UVGC_427_4618,(0,0,21):C.UVGC_427_4619,(0,0,22):C.UVGC_427_4620,(0,0,24):C.UVGC_427_4621,(0,0,27):C.UVGC_427_4622,(0,0,29):C.UVGC_427_4623,(0,0,31):C.UVGC_427_4624,(0,0,33):C.UVGC_427_4625,(0,0,35):C.UVGC_427_4626,(0,0,39):C.UVGC_427_4627,(0,0,43):C.UVGC_427_4628,(0,0,1):C.UVGC_427_4629,(0,0,13):C.UVGC_427_4630,(0,0,14):C.UVGC_422_4502,(0,0,16):C.UVGC_427_4631,(0,0,25):C.UVGC_422_4500,(0,0,26):C.UVGC_427_4632,(0,0,28):C.UVGC_427_4633,(0,0,32):C.UVGC_427_4634})

V_251 = CTVertex(name = 'V_251',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,2):C.UVGC_344_1709,(0,1,4):C.UVGC_344_1710,(0,1,6):C.UVGC_344_1711,(0,1,8):C.UVGC_344_1712,(0,1,14):C.UVGC_344_1713,(0,1,16):C.UVGC_344_1714,(0,1,22):C.UVGC_344_1715,(0,1,24):C.UVGC_344_1716,(0,1,25):C.UVGC_344_1717,(0,1,26):C.UVGC_344_1718,(0,1,28):C.UVGC_344_1719,(0,1,29):C.UVGC_344_1720,(0,1,30):C.UVGC_344_1721,(0,1,32):C.UVGC_344_1722,(0,1,0):C.UVGC_344_1723,(0,1,1):C.UVGC_344_1724,(0,1,3):C.UVGC_344_1725,(0,1,5):C.UVGC_344_1726,(0,1,7):C.UVGC_344_1727,(0,1,9):C.UVGC_344_1728,(0,1,10):C.UVGC_344_1729,(0,1,12):C.UVGC_344_1730,(0,1,13):C.UVGC_344_1731,(0,1,15):C.UVGC_344_1732,(0,1,17):C.UVGC_344_1733,(0,1,18):C.UVGC_344_1734,(0,1,19):C.UVGC_344_1735,(0,1,20):C.UVGC_344_1736,(0,1,21):C.UVGC_344_1737,(0,1,23):C.UVGC_344_1738,(0,1,27):C.UVGC_344_1739,(0,1,31):C.UVGC_344_1740,(0,1,11):C.UVGC_344_1741,(0,2,2):C.UVGC_342_1643,(0,2,4):C.UVGC_342_1644,(0,2,6):C.UVGC_342_1645,(0,2,8):C.UVGC_342_1646,(0,2,14):C.UVGC_342_1647,(0,2,16):C.UVGC_342_1648,(0,2,22):C.UVGC_342_1649,(0,2,24):C.UVGC_342_1650,(0,2,25):C.UVGC_342_1651,(0,2,26):C.UVGC_342_1652,(0,2,28):C.UVGC_342_1653,(0,2,29):C.UVGC_342_1654,(0,2,30):C.UVGC_342_1655,(0,2,32):C.UVGC_342_1656,(0,2,0):C.UVGC_342_1657,(0,2,1):C.UVGC_342_1658,(0,2,3):C.UVGC_342_1659,(0,2,5):C.UVGC_342_1660,(0,2,7):C.UVGC_342_1661,(0,2,9):C.UVGC_342_1662,(0,2,10):C.UVGC_342_1663,(0,2,12):C.UVGC_342_1664,(0,2,13):C.UVGC_342_1665,(0,2,15):C.UVGC_342_1666,(0,2,17):C.UVGC_342_1667,(0,2,18):C.UVGC_342_1668,(0,2,19):C.UVGC_342_1669,(0,2,20):C.UVGC_342_1670,(0,2,21):C.UVGC_342_1671,(0,2,23):C.UVGC_342_1672,(0,2,27):C.UVGC_342_1673,(0,2,31):C.UVGC_342_1674,(0,2,11):C.UVGC_342_1675,(0,0,2):C.UVGC_342_1643,(0,0,4):C.UVGC_342_1644,(0,0,6):C.UVGC_342_1645,(0,0,8):C.UVGC_342_1646,(0,0,14):C.UVGC_342_1647,(0,0,16):C.UVGC_342_1648,(0,0,22):C.UVGC_342_1649,(0,0,24):C.UVGC_342_1650,(0,0,25):C.UVGC_342_1651,(0,0,26):C.UVGC_342_1652,(0,0,28):C.UVGC_342_1653,(0,0,29):C.UVGC_342_1654,(0,0,30):C.UVGC_342_1655,(0,0,32):C.UVGC_342_1656,(0,0,0):C.UVGC_342_1657,(0,0,1):C.UVGC_342_1658,(0,0,3):C.UVGC_342_1659,(0,0,5):C.UVGC_342_1660,(0,0,7):C.UVGC_342_1661,(0,0,9):C.UVGC_342_1662,(0,0,10):C.UVGC_342_1663,(0,0,12):C.UVGC_342_1664,(0,0,13):C.UVGC_342_1665,(0,0,15):C.UVGC_342_1666,(0,0,17):C.UVGC_342_1667,(0,0,18):C.UVGC_342_1668,(0,0,19):C.UVGC_342_1669,(0,0,20):C.UVGC_342_1670,(0,0,21):C.UVGC_342_1671,(0,0,23):C.UVGC_342_1672,(0,0,27):C.UVGC_342_1673,(0,0,31):C.UVGC_342_1674,(0,0,11):C.UVGC_342_1675})

V_252 = CTVertex(name = 'V_252',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_409_4032,(0,0,4):C.UVGC_409_4033,(0,0,6):C.UVGC_409_4034,(0,0,8):C.UVGC_409_4035,(0,0,10):C.UVGC_409_4036,(0,0,16):C.UVGC_409_4037,(0,0,18):C.UVGC_409_4038,(0,0,22):C.UVGC_404_3853,(0,0,25):C.UVGC_409_4039,(0,0,27):C.UVGC_409_4040,(0,0,28):C.UVGC_409_4041,(0,0,29):C.UVGC_409_4042,(0,0,31):C.UVGC_409_4043,(0,0,32):C.UVGC_409_4044,(0,0,33):C.UVGC_409_4045,(0,0,35):C.UVGC_404_3863,(0,0,0):C.UVGC_404_3864,(0,0,1):C.UVGC_409_4046,(0,0,3):C.UVGC_409_4047,(0,0,5):C.UVGC_409_4048,(0,0,7):C.UVGC_409_4049,(0,0,9):C.UVGC_409_4050,(0,0,11):C.UVGC_404_3870,(0,0,12):C.UVGC_409_4051,(0,0,14):C.UVGC_409_4052,(0,0,15):C.UVGC_404_3873,(0,0,17):C.UVGC_409_4053,(0,0,19):C.UVGC_409_4054,(0,0,20):C.UVGC_409_4055,(0,0,21):C.UVGC_409_4056,(0,0,23):C.UVGC_409_4057,(0,0,24):C.UVGC_409_4058,(0,0,26):C.UVGC_409_4059,(0,0,30):C.UVGC_409_4060,(0,0,34):C.UVGC_409_4061,(0,0,13):C.UVGC_212_359})

V_253 = CTVertex(name = 'V_253',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0], [P.H] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_404_3849,(0,0,4):C.UVGC_404_3850,(0,0,6):C.UVGC_404_3851,(0,0,8):C.UVGC_404_3852,(0,0,11):C.UVGC_404_3853,(0,0,16):C.UVGC_404_3854,(0,0,18):C.UVGC_404_3855,(0,0,24):C.UVGC_404_3856,(0,0,26):C.UVGC_404_3857,(0,0,27):C.UVGC_404_3858,(0,0,28):C.UVGC_404_3859,(0,0,30):C.UVGC_404_3860,(0,0,31):C.UVGC_404_3861,(0,0,32):C.UVGC_404_3862,(0,0,34):C.UVGC_404_3863,(0,0,0):C.UVGC_404_3864,(0,0,1):C.UVGC_404_3865,(0,0,3):C.UVGC_404_3866,(0,0,5):C.UVGC_404_3867,(0,0,7):C.UVGC_404_3868,(0,0,9):C.UVGC_404_3869,(0,0,10):C.UVGC_404_3870,(0,0,12):C.UVGC_404_3871,(0,0,14):C.UVGC_404_3872,(0,0,15):C.UVGC_404_3873,(0,0,17):C.UVGC_404_3874,(0,0,19):C.UVGC_404_3875,(0,0,20):C.UVGC_404_3876,(0,0,21):C.UVGC_404_3877,(0,0,22):C.UVGC_404_3878,(0,0,23):C.UVGC_404_3879,(0,0,25):C.UVGC_404_3880,(0,0,29):C.UVGC_404_3881,(0,0,33):C.UVGC_404_3882,(0,0,13):C.UVGC_404_3883})

V_254 = CTVertex(name = 'V_254',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_410_4062,(0,0,4):C.UVGC_410_4063,(0,0,6):C.UVGC_410_4064,(0,0,8):C.UVGC_410_4065,(0,0,10):C.UVGC_410_4066,(0,0,16):C.UVGC_410_4067,(0,0,18):C.UVGC_410_4068,(0,0,19):C.UVGC_410_4069,(0,0,23):C.UVGC_410_4070,(0,0,26):C.UVGC_410_4071,(0,0,28):C.UVGC_410_4072,(0,0,29):C.UVGC_410_4073,(0,0,30):C.UVGC_410_4074,(0,0,32):C.UVGC_410_4075,(0,0,33):C.UVGC_409_4044,(0,0,34):C.UVGC_410_4076,(0,0,36):C.UVGC_410_4077,(0,0,0):C.UVGC_404_3864,(0,0,1):C.UVGC_409_4046,(0,0,3):C.UVGC_409_4047,(0,0,5):C.UVGC_409_4048,(0,0,7):C.UVGC_409_4049,(0,0,9):C.UVGC_409_4050,(0,0,11):C.UVGC_404_3870,(0,0,12):C.UVGC_410_4078,(0,0,14):C.UVGC_410_4079,(0,0,15):C.UVGC_404_3873,(0,0,17):C.UVGC_409_4053,(0,0,20):C.UVGC_409_4054,(0,0,21):C.UVGC_410_4080,(0,0,22):C.UVGC_409_4056,(0,0,24):C.UVGC_409_4057,(0,0,25):C.UVGC_410_4081,(0,0,27):C.UVGC_409_4059,(0,0,31):C.UVGC_409_4060,(0,0,35):C.UVGC_409_4061,(0,0,13):C.UVGC_212_359})

V_255 = CTVertex(name = 'V_255',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_406_3921,(0,0,4):C.UVGC_406_3922,(0,0,6):C.UVGC_406_3923,(0,0,8):C.UVGC_406_3924,(0,0,10):C.UVGC_406_3925,(0,0,16):C.UVGC_406_3926,(0,0,18):C.UVGC_406_3927,(0,0,19):C.UVGC_406_3928,(0,0,23):C.UVGC_406_3929,(0,0,26):C.UVGC_406_3930,(0,0,28):C.UVGC_406_3931,(0,0,29):C.UVGC_406_3932,(0,0,30):C.UVGC_406_3933,(0,0,32):C.UVGC_406_3934,(0,0,33):C.UVGC_406_3935,(0,0,34):C.UVGC_406_3936,(0,0,36):C.UVGC_406_3937,(0,0,0):C.UVGC_406_3938,(0,0,1):C.UVGC_406_3939,(0,0,3):C.UVGC_406_3940,(0,0,5):C.UVGC_406_3941,(0,0,7):C.UVGC_406_3942,(0,0,9):C.UVGC_406_3943,(0,0,11):C.UVGC_406_3944,(0,0,12):C.UVGC_406_3945,(0,0,14):C.UVGC_406_3946,(0,0,15):C.UVGC_406_3947,(0,0,17):C.UVGC_406_3948,(0,0,20):C.UVGC_406_3949,(0,0,21):C.UVGC_406_3950,(0,0,22):C.UVGC_406_3951,(0,0,24):C.UVGC_406_3952,(0,0,25):C.UVGC_406_3953,(0,0,27):C.UVGC_406_3954,(0,0,31):C.UVGC_406_3955,(0,0,35):C.UVGC_406_3956,(0,0,13):C.UVGC_406_3957})

V_256 = CTVertex(name = 'V_256',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV10, L.VVVV8, L.VVVV9 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.H] ], [ [P.G0], [P.H] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,2):C.UVGC_343_1676,(0,1,4):C.UVGC_343_1677,(0,1,6):C.UVGC_343_1678,(0,1,8):C.UVGC_343_1679,(0,1,15):C.UVGC_343_1680,(0,1,17):C.UVGC_343_1681,(0,1,23):C.UVGC_343_1682,(0,1,25):C.UVGC_343_1683,(0,1,26):C.UVGC_343_1684,(0,1,27):C.UVGC_343_1685,(0,1,29):C.UVGC_343_1686,(0,1,30):C.UVGC_343_1687,(0,1,31):C.UVGC_343_1688,(0,1,33):C.UVGC_343_1689,(0,1,0):C.UVGC_343_1690,(0,1,1):C.UVGC_343_1691,(0,1,3):C.UVGC_343_1692,(0,1,5):C.UVGC_343_1693,(0,1,7):C.UVGC_343_1694,(0,1,9):C.UVGC_343_1695,(0,1,10):C.UVGC_343_1696,(0,1,13):C.UVGC_343_1697,(0,1,14):C.UVGC_343_1698,(0,1,16):C.UVGC_343_1699,(0,1,18):C.UVGC_343_1700,(0,1,19):C.UVGC_343_1701,(0,1,20):C.UVGC_343_1702,(0,1,21):C.UVGC_343_1703,(0,1,22):C.UVGC_343_1704,(0,1,24):C.UVGC_343_1705,(0,1,28):C.UVGC_343_1706,(0,1,32):C.UVGC_343_1707,(0,1,11):C.UVGC_343_1708,(0,2,2):C.UVGC_343_1676,(0,2,4):C.UVGC_343_1677,(0,2,6):C.UVGC_343_1678,(0,2,8):C.UVGC_343_1679,(0,2,15):C.UVGC_343_1680,(0,2,17):C.UVGC_343_1681,(0,2,23):C.UVGC_343_1682,(0,2,25):C.UVGC_343_1683,(0,2,26):C.UVGC_343_1684,(0,2,27):C.UVGC_343_1685,(0,2,29):C.UVGC_343_1686,(0,2,30):C.UVGC_343_1687,(0,2,31):C.UVGC_343_1688,(0,2,33):C.UVGC_343_1689,(0,2,0):C.UVGC_343_1690,(0,2,1):C.UVGC_343_1691,(0,2,3):C.UVGC_343_1692,(0,2,5):C.UVGC_343_1693,(0,2,7):C.UVGC_343_1694,(0,2,9):C.UVGC_343_1695,(0,2,10):C.UVGC_343_1696,(0,2,13):C.UVGC_343_1697,(0,2,14):C.UVGC_343_1698,(0,2,16):C.UVGC_343_1699,(0,2,18):C.UVGC_343_1700,(0,2,19):C.UVGC_343_1701,(0,2,20):C.UVGC_343_1702,(0,2,21):C.UVGC_343_1703,(0,2,22):C.UVGC_343_1704,(0,2,24):C.UVGC_343_1705,(0,2,28):C.UVGC_343_1706,(0,2,32):C.UVGC_343_1707,(0,2,11):C.UVGC_343_1708,(0,0,2):C.UVGC_345_1742,(0,0,4):C.UVGC_345_1743,(0,0,6):C.UVGC_345_1744,(0,0,8):C.UVGC_345_1745,(0,0,12):C.UVGC_345_1746,(0,0,15):C.UVGC_345_1747,(0,0,17):C.UVGC_345_1748,(0,0,23):C.UVGC_345_1749,(0,0,25):C.UVGC_345_1750,(0,0,26):C.UVGC_345_1751,(0,0,27):C.UVGC_345_1752,(0,0,29):C.UVGC_345_1753,(0,0,30):C.UVGC_345_1754,(0,0,31):C.UVGC_345_1755,(0,0,33):C.UVGC_345_1756,(0,0,0):C.UVGC_345_1757,(0,0,1):C.UVGC_345_1758,(0,0,3):C.UVGC_345_1759,(0,0,5):C.UVGC_345_1760,(0,0,7):C.UVGC_345_1761,(0,0,9):C.UVGC_345_1762,(0,0,10):C.UVGC_345_1763,(0,0,13):C.UVGC_345_1764,(0,0,14):C.UVGC_345_1765,(0,0,16):C.UVGC_345_1766,(0,0,18):C.UVGC_345_1767,(0,0,19):C.UVGC_345_1768,(0,0,20):C.UVGC_345_1769,(0,0,21):C.UVGC_345_1770,(0,0,22):C.UVGC_345_1771,(0,0,24):C.UVGC_345_1772,(0,0,28):C.UVGC_345_1773,(0,0,32):C.UVGC_345_1774,(0,0,11):C.UVGC_345_1775})

V_257 = CTVertex(name = 'V_257',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_189_196,(0,0,2):C.UVGC_189_197,(0,0,3):C.UVGC_189_198,(0,0,4):C.UVGC_189_199,(0,0,12):C.UVGC_189_200,(0,0,13):C.UVGC_189_201,(0,0,14):C.UVGC_189_202,(0,0,15):C.UVGC_189_203,(0,0,16):C.UVGC_189_204,(0,0,18):C.UVGC_189_205,(0,1,1):C.UVGC_272_712,(0,1,2):C.UVGC_272_713,(0,1,3):C.UVGC_272_714,(0,1,4):C.UVGC_272_715,(0,1,8):C.UVGC_286_797,(0,1,9):C.UVGC_272_717,(0,1,12):C.UVGC_272_718,(0,1,13):C.UVGC_272_719,(0,1,14):C.UVGC_272_720,(0,1,15):C.UVGC_272_721,(0,1,16):C.UVGC_272_722,(0,1,18):C.UVGC_286_798,(0,1,0):C.UVGC_272_724,(0,1,5):C.UVGC_272_725,(0,1,6):C.UVGC_272_726,(0,1,7):C.UVGC_286_799,(0,1,10):C.UVGC_286_800,(0,1,11):C.UVGC_286_801,(0,1,17):C.UVGC_286_802,(0,2,1):C.UVGC_272_712,(0,2,2):C.UVGC_272_713,(0,2,3):C.UVGC_272_714,(0,2,4):C.UVGC_272_715,(0,2,8):C.UVGC_272_716,(0,2,9):C.UVGC_272_717,(0,2,12):C.UVGC_272_718,(0,2,13):C.UVGC_272_719,(0,2,14):C.UVGC_272_720,(0,2,15):C.UVGC_272_721,(0,2,16):C.UVGC_272_722,(0,2,18):C.UVGC_272_723,(0,2,0):C.UVGC_272_724,(0,2,5):C.UVGC_272_725,(0,2,6):C.UVGC_272_726,(0,2,7):C.UVGC_272_727,(0,2,10):C.UVGC_272_728,(0,2,11):C.UVGC_272_729,(0,2,17):C.UVGC_272_730})

V_258 = CTVertex(name = 'V_258',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.vm, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_189_196,(0,0,2):C.UVGC_189_197,(0,0,3):C.UVGC_189_198,(0,0,4):C.UVGC_189_199,(0,0,11):C.UVGC_189_200,(0,0,13):C.UVGC_189_201,(0,0,14):C.UVGC_189_202,(0,0,15):C.UVGC_189_203,(0,0,16):C.UVGC_189_204,(0,0,18):C.UVGC_189_205,(0,1,1):C.UVGC_272_712,(0,1,2):C.UVGC_272_713,(0,1,3):C.UVGC_272_714,(0,1,4):C.UVGC_272_715,(0,1,6):C.UVGC_286_797,(0,1,7):C.UVGC_272_717,(0,1,11):C.UVGC_272_718,(0,1,13):C.UVGC_272_719,(0,1,14):C.UVGC_272_720,(0,1,15):C.UVGC_272_721,(0,1,16):C.UVGC_272_722,(0,1,18):C.UVGC_286_798,(0,1,0):C.UVGC_273_731,(0,1,5):C.UVGC_273_732,(0,1,8):C.UVGC_287_803,(0,1,9):C.UVGC_286_801,(0,1,10):C.UVGC_273_734,(0,1,12):C.UVGC_287_804,(0,1,17):C.UVGC_287_805,(0,2,1):C.UVGC_272_712,(0,2,2):C.UVGC_272_713,(0,2,3):C.UVGC_272_714,(0,2,4):C.UVGC_272_715,(0,2,6):C.UVGC_272_716,(0,2,7):C.UVGC_272_717,(0,2,11):C.UVGC_272_718,(0,2,13):C.UVGC_272_719,(0,2,14):C.UVGC_272_720,(0,2,15):C.UVGC_272_721,(0,2,16):C.UVGC_272_722,(0,2,18):C.UVGC_272_723,(0,2,0):C.UVGC_273_731,(0,2,5):C.UVGC_273_732,(0,2,8):C.UVGC_273_733,(0,2,9):C.UVGC_272_729,(0,2,10):C.UVGC_273_734,(0,2,12):C.UVGC_273_735,(0,2,17):C.UVGC_273_736})

V_259 = CTVertex(name = 'V_259',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.vt, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_189_196,(0,0,2):C.UVGC_189_197,(0,0,3):C.UVGC_189_198,(0,0,4):C.UVGC_189_199,(0,0,11):C.UVGC_189_200,(0,0,12):C.UVGC_189_201,(0,0,13):C.UVGC_189_202,(0,0,14):C.UVGC_189_203,(0,0,16):C.UVGC_189_204,(0,0,18):C.UVGC_189_205,(0,1,1):C.UVGC_272_712,(0,1,2):C.UVGC_272_713,(0,1,3):C.UVGC_272_714,(0,1,4):C.UVGC_272_715,(0,1,6):C.UVGC_286_797,(0,1,7):C.UVGC_272_717,(0,1,11):C.UVGC_272_718,(0,1,12):C.UVGC_272_719,(0,1,13):C.UVGC_272_720,(0,1,14):C.UVGC_272_721,(0,1,16):C.UVGC_272_722,(0,1,18):C.UVGC_286_798,(0,1,0):C.UVGC_274_737,(0,1,5):C.UVGC_274_738,(0,1,8):C.UVGC_288_806,(0,1,9):C.UVGC_286_801,(0,1,10):C.UVGC_274_740,(0,1,15):C.UVGC_288_807,(0,1,17):C.UVGC_288_808,(0,2,1):C.UVGC_272_712,(0,2,2):C.UVGC_272_713,(0,2,3):C.UVGC_272_714,(0,2,4):C.UVGC_272_715,(0,2,6):C.UVGC_272_716,(0,2,7):C.UVGC_272_717,(0,2,11):C.UVGC_272_718,(0,2,12):C.UVGC_272_719,(0,2,13):C.UVGC_272_720,(0,2,14):C.UVGC_272_721,(0,2,16):C.UVGC_272_722,(0,2,18):C.UVGC_272_723,(0,2,0):C.UVGC_274_737,(0,2,5):C.UVGC_274_738,(0,2,8):C.UVGC_274_739,(0,2,9):C.UVGC_272_729,(0,2,10):C.UVGC_274_740,(0,2,15):C.UVGC_274_741,(0,2,17):C.UVGC_274_742})

V_260 = CTVertex(name = 'V_260',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.e__minus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.u, P.Z] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_207_341,(0,0,2):C.UVGC_207_342,(0,0,3):C.UVGC_207_343,(0,0,6):C.UVGC_207_344,(0,0,14):C.UVGC_207_345,(0,0,15):C.UVGC_207_346,(0,0,16):C.UVGC_207_347,(0,0,17):C.UVGC_207_348,(0,0,18):C.UVGC_207_349,(0,0,20):C.UVGC_207_350,(0,0,8):C.UVGC_238_484,(0,1,1):C.UVGC_269_678,(0,1,2):C.UVGC_269_679,(0,1,3):C.UVGC_269_680,(0,1,6):C.UVGC_269_681,(0,1,9):C.UVGC_283_785,(0,1,10):C.UVGC_269_683,(0,1,14):C.UVGC_269_684,(0,1,15):C.UVGC_269_685,(0,1,16):C.UVGC_269_686,(0,1,17):C.UVGC_269_687,(0,1,18):C.UVGC_269_688,(0,1,20):C.UVGC_283_786,(0,1,0):C.UVGC_271_705,(0,1,4):C.UVGC_285_794,(0,1,5):C.UVGC_285_795,(0,1,12):C.UVGC_271_708,(0,1,7):C.UVGC_271_709,(0,1,11):C.UVGC_283_789,(0,1,13):C.UVGC_271_710,(0,1,19):C.UVGC_285_796,(0,2,1):C.UVGC_269_678,(0,2,2):C.UVGC_269_679,(0,2,3):C.UVGC_269_680,(0,2,6):C.UVGC_269_681,(0,2,9):C.UVGC_269_682,(0,2,10):C.UVGC_269_683,(0,2,14):C.UVGC_269_684,(0,2,15):C.UVGC_269_685,(0,2,16):C.UVGC_269_686,(0,2,17):C.UVGC_269_687,(0,2,18):C.UVGC_269_688,(0,2,20):C.UVGC_269_689,(0,2,0):C.UVGC_271_705,(0,2,4):C.UVGC_271_706,(0,2,5):C.UVGC_271_707,(0,2,12):C.UVGC_271_708,(0,2,7):C.UVGC_271_709,(0,2,11):C.UVGC_269_696,(0,2,13):C.UVGC_271_710,(0,2,19):C.UVGC_271_711})

V_261 = CTVertex(name = 'V_261',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_207_341,(0,0,2):C.UVGC_207_342,(0,0,8):C.UVGC_207_343,(0,0,9):C.UVGC_207_344,(0,0,14):C.UVGC_207_345,(0,0,15):C.UVGC_207_346,(0,0,17):C.UVGC_207_347,(0,0,18):C.UVGC_207_348,(0,0,19):C.UVGC_207_349,(0,0,20):C.UVGC_207_350,(0,0,5):C.UVGC_207_351,(0,1,1):C.UVGC_269_678,(0,1,2):C.UVGC_269_679,(0,1,8):C.UVGC_269_680,(0,1,9):C.UVGC_269_681,(0,1,10):C.UVGC_283_785,(0,1,11):C.UVGC_269_683,(0,1,14):C.UVGC_269_684,(0,1,15):C.UVGC_269_685,(0,1,17):C.UVGC_269_686,(0,1,18):C.UVGC_269_687,(0,1,19):C.UVGC_269_688,(0,1,20):C.UVGC_283_786,(0,1,0):C.UVGC_269_690,(0,1,3):C.UVGC_269_691,(0,1,4):C.UVGC_269_692,(0,1,6):C.UVGC_269_693,(0,1,7):C.UVGC_283_787,(0,1,12):C.UVGC_283_788,(0,1,13):C.UVGC_283_789,(0,1,16):C.UVGC_283_790,(0,2,1):C.UVGC_269_678,(0,2,2):C.UVGC_269_679,(0,2,8):C.UVGC_269_680,(0,2,9):C.UVGC_269_681,(0,2,10):C.UVGC_269_682,(0,2,11):C.UVGC_269_683,(0,2,14):C.UVGC_269_684,(0,2,15):C.UVGC_269_685,(0,2,17):C.UVGC_269_686,(0,2,18):C.UVGC_269_687,(0,2,19):C.UVGC_269_688,(0,2,20):C.UVGC_269_689,(0,2,0):C.UVGC_269_690,(0,2,3):C.UVGC_269_691,(0,2,4):C.UVGC_269_692,(0,2,6):C.UVGC_269_693,(0,2,7):C.UVGC_269_694,(0,2,12):C.UVGC_269_695,(0,2,13):C.UVGC_269_696,(0,2,16):C.UVGC_269_697})

V_262 = CTVertex(name = 'V_262',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_207_341,(0,0,4):C.UVGC_207_342,(0,0,5):C.UVGC_207_343,(0,0,6):C.UVGC_207_344,(0,0,14):C.UVGC_207_345,(0,0,15):C.UVGC_207_346,(0,0,16):C.UVGC_207_347,(0,0,17):C.UVGC_207_348,(0,0,19):C.UVGC_207_349,(0,0,20):C.UVGC_207_350,(0,0,8):C.UVGC_225_427,(0,1,1):C.UVGC_269_678,(0,1,4):C.UVGC_269_679,(0,1,5):C.UVGC_269_680,(0,1,6):C.UVGC_269_681,(0,1,9):C.UVGC_283_785,(0,1,10):C.UVGC_269_683,(0,1,14):C.UVGC_269_684,(0,1,15):C.UVGC_269_685,(0,1,16):C.UVGC_269_686,(0,1,17):C.UVGC_269_687,(0,1,19):C.UVGC_269_688,(0,1,20):C.UVGC_283_786,(0,1,0):C.UVGC_270_698,(0,1,2):C.UVGC_284_791,(0,1,3):C.UVGC_284_792,(0,1,12):C.UVGC_270_701,(0,1,7):C.UVGC_270_702,(0,1,11):C.UVGC_283_789,(0,1,13):C.UVGC_270_703,(0,1,18):C.UVGC_284_793,(0,2,1):C.UVGC_269_678,(0,2,4):C.UVGC_269_679,(0,2,5):C.UVGC_269_680,(0,2,6):C.UVGC_269_681,(0,2,9):C.UVGC_269_682,(0,2,10):C.UVGC_269_683,(0,2,14):C.UVGC_269_684,(0,2,15):C.UVGC_269_685,(0,2,16):C.UVGC_269_686,(0,2,17):C.UVGC_269_687,(0,2,19):C.UVGC_269_688,(0,2,20):C.UVGC_269_689,(0,2,0):C.UVGC_270_698,(0,2,2):C.UVGC_270_699,(0,2,3):C.UVGC_270_700,(0,2,12):C.UVGC_270_701,(0,2,7):C.UVGC_270_702,(0,2,11):C.UVGC_269_696,(0,2,13):C.UVGC_270_703,(0,2,18):C.UVGC_270_704})

V_263 = CTVertex(name = 'V_263',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_187_176,(0,0,2):C.UVGC_187_177,(0,0,3):C.UVGC_187_178,(0,0,8):C.UVGC_187_179,(0,0,13):C.UVGC_187_180,(0,0,14):C.UVGC_187_181,(0,0,15):C.UVGC_187_182,(0,0,16):C.UVGC_187_183,(0,0,17):C.UVGC_187_184,(0,0,19):C.UVGC_187_185,(0,1,1):C.UVGC_266_644,(0,1,2):C.UVGC_266_645,(0,1,3):C.UVGC_266_646,(0,1,8):C.UVGC_266_647,(0,1,9):C.UVGC_279_760,(0,1,10):C.UVGC_266_649,(0,1,13):C.UVGC_266_650,(0,1,14):C.UVGC_266_651,(0,1,15):C.UVGC_266_652,(0,1,16):C.UVGC_266_653,(0,1,17):C.UVGC_266_654,(0,1,19):C.UVGC_279_761,(0,1,0):C.UVGC_268_671,(0,1,4):C.UVGC_268_672,(0,1,5):C.UVGC_268_673,(0,1,6):C.UVGC_268_674,(0,1,7):C.UVGC_281_769,(0,1,11):C.UVGC_281_770,(0,1,12):C.UVGC_279_764,(0,1,18):C.UVGC_281_771,(0,2,1):C.UVGC_266_644,(0,2,2):C.UVGC_266_645,(0,2,3):C.UVGC_266_646,(0,2,8):C.UVGC_266_647,(0,2,9):C.UVGC_266_648,(0,2,10):C.UVGC_266_649,(0,2,13):C.UVGC_266_650,(0,2,14):C.UVGC_266_651,(0,2,15):C.UVGC_266_652,(0,2,16):C.UVGC_266_653,(0,2,17):C.UVGC_266_654,(0,2,19):C.UVGC_266_655,(0,2,0):C.UVGC_268_671,(0,2,4):C.UVGC_268_672,(0,2,5):C.UVGC_268_673,(0,2,6):C.UVGC_268_674,(0,2,7):C.UVGC_268_675,(0,2,11):C.UVGC_268_676,(0,2,12):C.UVGC_266_661,(0,2,18):C.UVGC_268_677})

V_264 = CTVertex(name = 'V_264',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.b] ], [ [P.c] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.s] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_187_176,(0,0,2):C.UVGC_187_177,(0,0,5):C.UVGC_187_178,(0,0,6):C.UVGC_187_179,(0,0,13):C.UVGC_187_180,(0,0,14):C.UVGC_187_181,(0,0,16):C.UVGC_187_182,(0,0,17):C.UVGC_187_183,(0,0,18):C.UVGC_187_184,(0,0,19):C.UVGC_187_185,(0,1,1):C.UVGC_266_644,(0,1,2):C.UVGC_266_645,(0,1,5):C.UVGC_266_646,(0,1,6):C.UVGC_266_647,(0,1,8):C.UVGC_279_760,(0,1,9):C.UVGC_266_649,(0,1,13):C.UVGC_266_650,(0,1,14):C.UVGC_266_651,(0,1,16):C.UVGC_266_652,(0,1,17):C.UVGC_266_653,(0,1,18):C.UVGC_266_654,(0,1,19):C.UVGC_279_761,(0,1,0):C.UVGC_266_656,(0,1,3):C.UVGC_279_762,(0,1,4):C.UVGC_279_763,(0,1,11):C.UVGC_266_659,(0,1,7):C.UVGC_266_660,(0,1,10):C.UVGC_279_764,(0,1,12):C.UVGC_266_662,(0,1,15):C.UVGC_279_765,(0,2,1):C.UVGC_266_644,(0,2,2):C.UVGC_266_645,(0,2,5):C.UVGC_266_646,(0,2,6):C.UVGC_266_647,(0,2,8):C.UVGC_266_648,(0,2,9):C.UVGC_266_649,(0,2,13):C.UVGC_266_650,(0,2,14):C.UVGC_266_651,(0,2,16):C.UVGC_266_652,(0,2,17):C.UVGC_266_653,(0,2,18):C.UVGC_266_654,(0,2,19):C.UVGC_266_655,(0,2,0):C.UVGC_266_656,(0,2,3):C.UVGC_266_657,(0,2,4):C.UVGC_266_658,(0,2,11):C.UVGC_266_659,(0,2,7):C.UVGC_266_660,(0,2,10):C.UVGC_266_661,(0,2,12):C.UVGC_266_662,(0,2,15):C.UVGC_266_663})

V_265 = CTVertex(name = 'V_265',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.t, P.W__plus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_187_176,(0,0,6):C.UVGC_187_177,(0,0,7):C.UVGC_187_178,(0,0,8):C.UVGC_187_179,(0,0,13):C.UVGC_187_180,(0,0,14):C.UVGC_187_181,(0,0,15):C.UVGC_187_182,(0,0,16):C.UVGC_187_183,(0,0,18):C.UVGC_187_184,(0,0,19):C.UVGC_187_185,(0,1,1):C.UVGC_266_644,(0,1,6):C.UVGC_266_645,(0,1,7):C.UVGC_266_646,(0,1,8):C.UVGC_266_647,(0,1,9):C.UVGC_279_760,(0,1,10):C.UVGC_266_649,(0,1,13):C.UVGC_266_650,(0,1,14):C.UVGC_266_651,(0,1,15):C.UVGC_266_652,(0,1,16):C.UVGC_266_653,(0,1,18):C.UVGC_266_654,(0,1,19):C.UVGC_279_761,(0,1,0):C.UVGC_267_664,(0,1,2):C.UVGC_267_665,(0,1,3):C.UVGC_267_666,(0,1,4):C.UVGC_267_667,(0,1,5):C.UVGC_280_766,(0,1,11):C.UVGC_280_767,(0,1,12):C.UVGC_279_764,(0,1,17):C.UVGC_280_768,(0,2,1):C.UVGC_266_644,(0,2,6):C.UVGC_266_645,(0,2,7):C.UVGC_266_646,(0,2,8):C.UVGC_266_647,(0,2,9):C.UVGC_266_648,(0,2,10):C.UVGC_266_649,(0,2,13):C.UVGC_266_650,(0,2,14):C.UVGC_266_651,(0,2,15):C.UVGC_266_652,(0,2,16):C.UVGC_266_653,(0,2,18):C.UVGC_266_654,(0,2,19):C.UVGC_266_655,(0,2,0):C.UVGC_267_664,(0,2,2):C.UVGC_267_665,(0,2,3):C.UVGC_267_666,(0,2,4):C.UVGC_267_667,(0,2,5):C.UVGC_267_668,(0,2,11):C.UVGC_267_669,(0,2,12):C.UVGC_266_661,(0,2,17):C.UVGC_267_670})

V_266 = CTVertex(name = 'V_266',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.g] ], [ [P.G0, P.u] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.ghG] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.s] ], [ [P.t] ], [ [P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,8):C.UVGC_239_485,(0,1,1):C.UVGC_218_382,(0,1,2):C.UVGC_218_383,(0,1,3):C.UVGC_218_384,(0,1,6):C.UVGC_218_385,(0,1,9):C.UVGC_218_386,(0,1,12):C.UVGC_218_387,(0,1,13):C.UVGC_218_388,(0,1,14):C.UVGC_218_389,(0,1,0):C.UVGC_248_530,(0,1,4):C.UVGC_249_537,(0,1,5):C.UVGC_249_538,(0,1,10):C.UVGC_248_533,(0,1,7):C.UVGC_248_534,(0,1,11):C.UVGC_248_535,(0,1,15):C.UVGC_249_539,(0,2,1):C.UVGC_218_382,(0,2,2):C.UVGC_218_383,(0,2,3):C.UVGC_218_384,(0,2,6):C.UVGC_218_385,(0,2,9):C.UVGC_218_386,(0,2,12):C.UVGC_218_387,(0,2,13):C.UVGC_218_388,(0,2,14):C.UVGC_218_389,(0,2,0):C.UVGC_248_530,(0,2,4):C.UVGC_248_531,(0,2,5):C.UVGC_248_532,(0,2,10):C.UVGC_248_533,(0,2,7):C.UVGC_248_534,(0,2,11):C.UVGC_248_535,(0,2,15):C.UVGC_248_536})

V_267 = CTVertex(name = 'V_267',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.g] ], [ [P.ghG] ], [ [P.G__plus__, P.s] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,5):C.UVGC_208_352,(0,1,1):C.UVGC_218_382,(0,1,2):C.UVGC_218_383,(0,1,8):C.UVGC_218_384,(0,1,9):C.UVGC_218_385,(0,1,10):C.UVGC_218_386,(0,1,12):C.UVGC_218_387,(0,1,14):C.UVGC_218_388,(0,1,15):C.UVGC_218_389,(0,1,0):C.UVGC_218_390,(0,1,3):C.UVGC_218_391,(0,1,4):C.UVGC_218_392,(0,1,6):C.UVGC_218_393,(0,1,7):C.UVGC_219_397,(0,1,11):C.UVGC_219_398,(0,1,13):C.UVGC_219_399,(0,2,1):C.UVGC_218_382,(0,2,2):C.UVGC_218_383,(0,2,8):C.UVGC_218_384,(0,2,9):C.UVGC_218_385,(0,2,10):C.UVGC_218_386,(0,2,12):C.UVGC_218_387,(0,2,14):C.UVGC_218_388,(0,2,15):C.UVGC_218_389,(0,2,0):C.UVGC_218_390,(0,2,3):C.UVGC_218_391,(0,2,4):C.UVGC_218_392,(0,2,6):C.UVGC_218_393,(0,2,7):C.UVGC_218_394,(0,2,11):C.UVGC_218_395,(0,2,13):C.UVGC_218_396})

V_268 = CTVertex(name = 'V_268',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.G0, P.t] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.ghG] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.s] ], [ [P.t] ], [ [P.t, P.Z] ], [ [P.u] ] ],
                 couplings = {(0,0,8):C.UVGC_226_428,(0,1,1):C.UVGC_218_382,(0,1,4):C.UVGC_218_383,(0,1,5):C.UVGC_218_384,(0,1,6):C.UVGC_218_385,(0,1,9):C.UVGC_218_386,(0,1,12):C.UVGC_218_387,(0,1,13):C.UVGC_218_388,(0,1,15):C.UVGC_218_389,(0,1,0):C.UVGC_235_473,(0,1,2):C.UVGC_236_480,(0,1,3):C.UVGC_236_481,(0,1,10):C.UVGC_235_476,(0,1,7):C.UVGC_235_477,(0,1,11):C.UVGC_235_478,(0,1,14):C.UVGC_236_482,(0,2,1):C.UVGC_218_382,(0,2,4):C.UVGC_218_383,(0,2,5):C.UVGC_218_384,(0,2,6):C.UVGC_218_385,(0,2,9):C.UVGC_218_386,(0,2,12):C.UVGC_218_387,(0,2,13):C.UVGC_218_388,(0,2,15):C.UVGC_218_389,(0,2,0):C.UVGC_235_473,(0,2,2):C.UVGC_235_474,(0,2,3):C.UVGC_235_475,(0,2,10):C.UVGC_235_476,(0,2,7):C.UVGC_235_477,(0,2,11):C.UVGC_235_478,(0,2,14):C.UVGC_235_479})

V_269 = CTVertex(name = 'V_269',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.g] ], [ [P.ghG] ], [ [P.G__plus__, P.u] ], [ [P.s] ], [ [P.t] ], [ [P.u] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_218_382,(0,0,2):C.UVGC_218_383,(0,0,3):C.UVGC_218_384,(0,0,8):C.UVGC_218_385,(0,0,9):C.UVGC_218_386,(0,0,11):C.UVGC_218_387,(0,0,12):C.UVGC_218_388,(0,0,13):C.UVGC_218_389,(0,0,0):C.UVGC_243_503,(0,0,4):C.UVGC_243_504,(0,0,5):C.UVGC_243_505,(0,0,6):C.UVGC_243_506,(0,0,7):C.UVGC_244_510,(0,0,10):C.UVGC_244_511,(0,0,14):C.UVGC_244_512,(0,1,1):C.UVGC_218_382,(0,1,2):C.UVGC_218_383,(0,1,3):C.UVGC_218_384,(0,1,8):C.UVGC_218_385,(0,1,9):C.UVGC_218_386,(0,1,11):C.UVGC_218_387,(0,1,12):C.UVGC_218_388,(0,1,13):C.UVGC_218_389,(0,1,0):C.UVGC_243_503,(0,1,4):C.UVGC_243_504,(0,1,5):C.UVGC_243_505,(0,1,6):C.UVGC_243_506,(0,1,7):C.UVGC_243_507,(0,1,10):C.UVGC_243_508,(0,1,14):C.UVGC_243_509})

V_270 = CTVertex(name = 'V_270',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.b] ], [ [P.c] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d] ], [ [P.g] ], [ [P.G0, P.s] ], [ [P.ghG] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,1):C.UVGC_218_382,(0,0,2):C.UVGC_218_383,(0,0,5):C.UVGC_218_384,(0,0,6):C.UVGC_218_385,(0,0,8):C.UVGC_218_386,(0,0,11):C.UVGC_218_387,(0,0,13):C.UVGC_218_388,(0,0,14):C.UVGC_218_389,(0,0,0):C.UVGC_223_417,(0,0,3):C.UVGC_224_424,(0,0,4):C.UVGC_224_425,(0,0,9):C.UVGC_223_420,(0,0,7):C.UVGC_223_421,(0,0,10):C.UVGC_223_422,(0,0,12):C.UVGC_224_426,(0,1,1):C.UVGC_218_382,(0,1,2):C.UVGC_218_383,(0,1,5):C.UVGC_218_384,(0,1,6):C.UVGC_218_385,(0,1,8):C.UVGC_218_386,(0,1,11):C.UVGC_218_387,(0,1,13):C.UVGC_218_388,(0,1,14):C.UVGC_218_389,(0,1,0):C.UVGC_223_417,(0,1,3):C.UVGC_223_418,(0,1,4):C.UVGC_223_419,(0,1,9):C.UVGC_223_420,(0,1,7):C.UVGC_223_421,(0,1,10):C.UVGC_223_422,(0,1,12):C.UVGC_223_423})

V_271 = CTVertex(name = 'V_271',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.ghG] ], [ [P.G__plus__, P.t] ], [ [P.s] ], [ [P.t] ], [ [P.t, P.W__plus__] ], [ [P.u] ] ],
                 couplings = {(0,0,1):C.UVGC_218_382,(0,0,6):C.UVGC_218_383,(0,0,7):C.UVGC_218_384,(0,0,8):C.UVGC_218_385,(0,0,9):C.UVGC_218_386,(0,0,11):C.UVGC_218_387,(0,0,12):C.UVGC_218_388,(0,0,14):C.UVGC_218_389,(0,0,0):C.UVGC_230_446,(0,0,2):C.UVGC_230_447,(0,0,3):C.UVGC_230_448,(0,0,4):C.UVGC_230_449,(0,0,5):C.UVGC_231_453,(0,0,10):C.UVGC_231_454,(0,0,13):C.UVGC_231_455,(0,1,1):C.UVGC_218_382,(0,1,6):C.UVGC_218_383,(0,1,7):C.UVGC_218_384,(0,1,8):C.UVGC_218_385,(0,1,9):C.UVGC_218_386,(0,1,11):C.UVGC_218_387,(0,1,12):C.UVGC_218_388,(0,1,14):C.UVGC_218_389,(0,1,0):C.UVGC_230_446,(0,1,2):C.UVGC_230_447,(0,1,3):C.UVGC_230_448,(0,1,4):C.UVGC_230_449,(0,1,5):C.UVGC_230_450,(0,1,10):C.UVGC_230_451,(0,1,13):C.UVGC_230_452})

V_272 = CTVertex(name = 'V_272',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.u] ], [ [P.a, P.u, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.G__plus__], [P.d, P.G__plus__, P.H] ], [ [P.d, P.G0, P.G__plus__], [P.d, P.H, P.u], [P.G0, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.G__plus__, P.H], [P.G__plus__, P.H, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.u], [P.G__plus__, P.H, P.u] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.u, P.W__plus__, P.Z] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,9):C.UVGC_359_2217,(0,0,11):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,46):C.UVGC_359_2224,(0,0,47):C.UVGC_359_2225,(0,0,49):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_385_3153,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_385_3154,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_359_2234,(0,0,10):C.UVGC_359_2239,(0,0,12):C.UVGC_385_3155,(0,0,13):C.UVGC_385_3156,(0,0,17):C.UVGC_385_3157,(0,0,19):C.UVGC_385_3158,(0,0,20):C.UVGC_359_2242,(0,0,22):C.UVGC_385_3159,(0,0,24):C.UVGC_385_3160,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_385_3161,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_385_3162,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_385_3163,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_385_3164,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,48):C.UVGC_359_2260,(0,0,50):C.UVGC_385_3165,(0,0,52):C.UVGC_385_3166,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2264,(0,0,5):C.UVGC_359_2263,(0,0,18):C.UVGC_359_2265,(0,0,14):C.UVGC_385_3167,(0,0,21):C.UVGC_359_2267,(0,0,23):C.UVGC_359_2270,(0,0,28):C.UVGC_385_3168,(0,0,51):C.UVGC_359_2268,(0,1,15):C.UVGC_376_2743,(0,1,16):C.UVGC_376_2744})

V_273 = CTVertex(name = 'V_273',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.s] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.G__plus__], [P.c, P.G__plus__, P.H] ], [ [P.c, P.G0, P.G__plus__], [P.c, P.H, P.s], [P.G0, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.G__plus__, P.H], [P.G__plus__, P.H, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.s], [P.G__plus__, P.H, P.s] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,9):C.UVGC_359_2217,(0,0,23):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,49):C.UVGC_359_2224,(0,0,50):C.UVGC_359_2225,(0,0,52):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2230,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_359_2232,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_359_2234,(0,0,10):C.UVGC_359_2235,(0,0,11):C.UVGC_359_2236,(0,0,15):C.UVGC_359_2237,(0,0,17):C.UVGC_359_2238,(0,0,18):C.UVGC_359_2239,(0,0,20):C.UVGC_359_2240,(0,0,22):C.UVGC_359_2241,(0,0,24):C.UVGC_359_2242,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_359_2244,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_359_2247,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_359_2251,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_359_2254,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,46):C.UVGC_359_2258,(0,0,48):C.UVGC_359_2259,(0,0,51):C.UVGC_359_2260,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2263,(0,0,5):C.UVGC_359_2264,(0,0,16):C.UVGC_359_2265,(0,0,12):C.UVGC_359_2266,(0,0,19):C.UVGC_359_2267,(0,0,21):C.UVGC_359_2268,(0,0,28):C.UVGC_359_2269,(0,0,47):C.UVGC_359_2270,(0,1,13):C.UVGC_350_1806,(0,1,14):C.UVGC_350_1807})

V_274 = CTVertex(name = 'V_274',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.t] ], [ [P.a, P.t, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.G__plus__], [P.b, P.G__plus__, P.H] ], [ [P.b, P.G0, P.G__plus__], [P.b, P.H, P.t], [P.G0, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.G__plus__, P.H], [P.G__plus__, P.H, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.t], [P.G__plus__, P.H, P.t] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.t, P.W__plus__, P.Z] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,21):C.UVGC_359_2217,(0,0,23):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,46):C.UVGC_359_2224,(0,0,47):C.UVGC_359_2225,(0,0,52):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_371_2697,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_371_2698,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_371_2699,(0,0,9):C.UVGC_371_2700,(0,0,13):C.UVGC_371_2701,(0,0,15):C.UVGC_371_2702,(0,0,16):C.UVGC_359_2234,(0,0,18):C.UVGC_371_2703,(0,0,20):C.UVGC_371_2704,(0,0,22):C.UVGC_359_2239,(0,0,24):C.UVGC_359_2242,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_371_2705,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_371_2706,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_371_2707,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_371_2708,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,49):C.UVGC_371_2709,(0,0,51):C.UVGC_371_2710,(0,0,48):C.UVGC_359_2260,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2264,(0,0,5):C.UVGC_359_2263,(0,0,14):C.UVGC_359_2265,(0,0,10):C.UVGC_371_2711,(0,0,17):C.UVGC_359_2267,(0,0,19):C.UVGC_359_2270,(0,0,28):C.UVGC_371_2712,(0,0,50):C.UVGC_359_2268,(0,1,11):C.UVGC_362_2287,(0,1,12):C.UVGC_362_2288})

V_275 = CTVertex(name = 'V_275',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.u] ], [ [P.a, P.u, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.G__plus__], [P.d, P.G__plus__, P.H] ], [ [P.d, P.G0, P.G__plus__], [P.d, P.H, P.u], [P.G0, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.G__plus__, P.H], [P.G__plus__, P.H, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.u], [P.G__plus__, P.H, P.u] ], [ [P.G0, P.H] ], [ [P.G0, P.u] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.u, P.W__plus__, P.Z] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,9):C.UVGC_359_2217,(0,0,11):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,46):C.UVGC_359_2224,(0,0,47):C.UVGC_359_2225,(0,0,49):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_385_3153,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_385_3154,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_359_2234,(0,0,10):C.UVGC_359_2239,(0,0,12):C.UVGC_385_3155,(0,0,13):C.UVGC_385_3156,(0,0,17):C.UVGC_385_3157,(0,0,19):C.UVGC_385_3158,(0,0,20):C.UVGC_359_2242,(0,0,22):C.UVGC_385_3159,(0,0,24):C.UVGC_385_3160,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_385_3161,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_385_3162,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_385_3163,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_385_3164,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,48):C.UVGC_359_2260,(0,0,50):C.UVGC_385_3165,(0,0,52):C.UVGC_385_3166,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2264,(0,0,5):C.UVGC_359_2263,(0,0,18):C.UVGC_359_2265,(0,0,14):C.UVGC_385_3167,(0,0,21):C.UVGC_359_2267,(0,0,23):C.UVGC_359_2270,(0,0,28):C.UVGC_385_3168,(0,0,51):C.UVGC_359_2268,(0,1,15):C.UVGC_376_2743,(0,1,16):C.UVGC_376_2744})

V_276 = CTVertex(name = 'V_276',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.s] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.G__plus__], [P.c, P.G__plus__, P.H] ], [ [P.c, P.G0, P.G__plus__], [P.c, P.H, P.s], [P.G0, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.G__plus__, P.H], [P.G__plus__, P.H, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.s], [P.G__plus__, P.H, P.s] ], [ [P.G0, P.H] ], [ [P.G0, P.s] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,9):C.UVGC_359_2217,(0,0,23):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,49):C.UVGC_359_2224,(0,0,50):C.UVGC_359_2225,(0,0,52):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2230,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_359_2232,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_359_2234,(0,0,10):C.UVGC_359_2235,(0,0,11):C.UVGC_359_2236,(0,0,15):C.UVGC_359_2237,(0,0,17):C.UVGC_359_2238,(0,0,18):C.UVGC_359_2239,(0,0,20):C.UVGC_359_2240,(0,0,22):C.UVGC_359_2241,(0,0,24):C.UVGC_359_2242,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_359_2244,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_359_2247,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_359_2251,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_359_2254,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,46):C.UVGC_359_2258,(0,0,48):C.UVGC_359_2259,(0,0,51):C.UVGC_359_2260,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2263,(0,0,5):C.UVGC_359_2264,(0,0,16):C.UVGC_359_2265,(0,0,12):C.UVGC_359_2266,(0,0,19):C.UVGC_359_2267,(0,0,21):C.UVGC_359_2268,(0,0,28):C.UVGC_359_2269,(0,0,47):C.UVGC_359_2270,(0,1,13):C.UVGC_350_1806,(0,1,14):C.UVGC_350_1807})

V_277 = CTVertex(name = 'V_277',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.t] ], [ [P.a, P.t, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.G__plus__], [P.b, P.G__plus__, P.H] ], [ [P.b, P.G0, P.G__plus__], [P.b, P.H, P.t], [P.G0, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.G__plus__, P.H], [P.G__plus__, P.H, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.t], [P.G__plus__, P.H, P.t] ], [ [P.G0, P.H] ], [ [P.G0, P.t] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.t, P.W__plus__, P.Z] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,7):C.UVGC_359_2216,(0,0,21):C.UVGC_359_2217,(0,0,23):C.UVGC_359_2218,(0,0,25):C.UVGC_359_2219,(0,0,32):C.UVGC_359_2220,(0,0,34):C.UVGC_359_2221,(0,0,43):C.UVGC_359_2222,(0,0,45):C.UVGC_359_2223,(0,0,46):C.UVGC_359_2224,(0,0,47):C.UVGC_359_2225,(0,0,52):C.UVGC_359_2226,(0,0,53):C.UVGC_359_2227,(0,0,54):C.UVGC_359_2228,(0,0,56):C.UVGC_359_2229,(0,0,0):C.UVGC_371_2697,(0,0,3):C.UVGC_359_2231,(0,0,4):C.UVGC_371_2698,(0,0,6):C.UVGC_359_2233,(0,0,8):C.UVGC_371_2699,(0,0,9):C.UVGC_371_2700,(0,0,13):C.UVGC_371_2701,(0,0,15):C.UVGC_371_2702,(0,0,16):C.UVGC_359_2234,(0,0,18):C.UVGC_371_2703,(0,0,20):C.UVGC_371_2704,(0,0,22):C.UVGC_359_2239,(0,0,24):C.UVGC_359_2242,(0,0,26):C.UVGC_359_2243,(0,0,39):C.UVGC_371_2705,(0,0,27):C.UVGC_359_2245,(0,0,29):C.UVGC_359_2246,(0,0,30):C.UVGC_371_2706,(0,0,31):C.UVGC_359_2248,(0,0,33):C.UVGC_359_2249,(0,0,35):C.UVGC_359_2250,(0,0,36):C.UVGC_371_2707,(0,0,37):C.UVGC_359_2252,(0,0,38):C.UVGC_359_2253,(0,0,40):C.UVGC_371_2708,(0,0,41):C.UVGC_359_2255,(0,0,42):C.UVGC_359_2256,(0,0,44):C.UVGC_359_2257,(0,0,49):C.UVGC_371_2709,(0,0,51):C.UVGC_371_2710,(0,0,48):C.UVGC_359_2260,(0,0,55):C.UVGC_359_2261,(0,0,1):C.UVGC_359_2262,(0,0,2):C.UVGC_359_2264,(0,0,5):C.UVGC_359_2263,(0,0,14):C.UVGC_359_2265,(0,0,10):C.UVGC_371_2711,(0,0,17):C.UVGC_359_2267,(0,0,19):C.UVGC_359_2270,(0,0,28):C.UVGC_371_2712,(0,0,50):C.UVGC_359_2268,(0,1,11):C.UVGC_362_2287,(0,1,12):C.UVGC_362_2288})

V_278 = CTVertex(name = 'V_278',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.G__plus__], [P.e__minus__, P.G__plus__, P.H] ], [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.ve, P.W__plus__, P.Z] ], [ [P.ve, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,23):C.UVGC_359_2220,(0,0,25):C.UVGC_359_2221,(0,0,32):C.UVGC_359_2222,(0,0,34):C.UVGC_359_2223,(0,0,35):C.UVGC_359_2224,(0,0,36):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_390_3353,(0,0,2):C.UVGC_359_2231,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_390_3354,(0,0,13):C.UVGC_390_3355,(0,0,14):C.UVGC_390_3356,(0,0,15):C.UVGC_359_2243,(0,0,17):C.UVGC_390_3357,(0,0,19):C.UVGC_390_3358,(0,0,20):C.UVGC_359_2245,(0,0,21):C.UVGC_359_2246,(0,0,22):C.UVGC_359_2248,(0,0,24):C.UVGC_359_2249,(0,0,26):C.UVGC_359_2250,(0,0,27):C.UVGC_390_3359,(0,0,28):C.UVGC_359_2252,(0,0,29):C.UVGC_359_2253,(0,0,30):C.UVGC_359_2255,(0,0,31):C.UVGC_359_2256,(0,0,33):C.UVGC_359_2257,(0,0,37):C.UVGC_359_2260,(0,0,40):C.UVGC_390_3360,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,1):C.UVGC_390_3362,(0,0,12):C.UVGC_390_3363,(0,0,16):C.UVGC_390_3364,(0,0,18):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_279 = CTVertex(name = 'V_279',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.mu__minus__], [P.G__plus__, P.H, P.mu__minus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.vm, P.W__plus__, P.Z] ], [ [P.vm, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,17):C.UVGC_359_2220,(0,0,19):C.UVGC_359_2221,(0,0,28):C.UVGC_359_2222,(0,0,34):C.UVGC_359_2223,(0,0,35):C.UVGC_359_2224,(0,0,36):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2231,(0,0,1):C.UVGC_395_3551,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_359_2243,(0,0,12):C.UVGC_359_2245,(0,0,14):C.UVGC_359_2246,(0,0,15):C.UVGC_395_3552,(0,0,16):C.UVGC_359_2248,(0,0,18):C.UVGC_359_2249,(0,0,20):C.UVGC_359_2250,(0,0,21):C.UVGC_395_3553,(0,0,22):C.UVGC_395_3554,(0,0,23):C.UVGC_359_2252,(0,0,24):C.UVGC_359_2253,(0,0,25):C.UVGC_395_3555,(0,0,26):C.UVGC_359_2255,(0,0,27):C.UVGC_359_2256,(0,0,29):C.UVGC_359_2257,(0,0,31):C.UVGC_395_3556,(0,0,33):C.UVGC_395_3557,(0,0,37):C.UVGC_359_2260,(0,0,40):C.UVGC_395_3558,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,2):C.UVGC_390_3362,(0,0,13):C.UVGC_395_3559,(0,0,30):C.UVGC_390_3364,(0,0,32):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_280 = CTVertex(name = 'V_280',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.ta__minus__], [P.G__plus__, P.H, P.ta__minus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.vt, P.W__plus__, P.Z] ], [ [P.vt, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,17):C.UVGC_359_2220,(0,0,19):C.UVGC_359_2221,(0,0,28):C.UVGC_359_2222,(0,0,30):C.UVGC_359_2223,(0,0,31):C.UVGC_359_2224,(0,0,32):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2231,(0,0,1):C.UVGC_400_3744,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_359_2243,(0,0,12):C.UVGC_359_2245,(0,0,14):C.UVGC_359_2246,(0,0,15):C.UVGC_400_3745,(0,0,16):C.UVGC_359_2248,(0,0,18):C.UVGC_359_2249,(0,0,20):C.UVGC_359_2250,(0,0,21):C.UVGC_400_3746,(0,0,22):C.UVGC_400_3747,(0,0,23):C.UVGC_359_2252,(0,0,24):C.UVGC_359_2253,(0,0,25):C.UVGC_400_3748,(0,0,26):C.UVGC_359_2255,(0,0,27):C.UVGC_359_2256,(0,0,29):C.UVGC_359_2257,(0,0,33):C.UVGC_359_2260,(0,0,35):C.UVGC_400_3749,(0,0,37):C.UVGC_400_3750,(0,0,40):C.UVGC_400_3751,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,2):C.UVGC_390_3362,(0,0,13):C.UVGC_400_3752,(0,0,34):C.UVGC_390_3364,(0,0,36):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_281 = CTVertex(name = 'V_281',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.G__plus__], [P.e__minus__, P.G__plus__, P.H] ], [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.ve, P.W__plus__, P.Z] ], [ [P.ve, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,23):C.UVGC_359_2220,(0,0,25):C.UVGC_359_2221,(0,0,32):C.UVGC_359_2222,(0,0,34):C.UVGC_359_2223,(0,0,35):C.UVGC_359_2224,(0,0,36):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_390_3353,(0,0,2):C.UVGC_359_2231,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_390_3354,(0,0,13):C.UVGC_390_3355,(0,0,14):C.UVGC_390_3356,(0,0,15):C.UVGC_359_2243,(0,0,17):C.UVGC_390_3357,(0,0,19):C.UVGC_390_3358,(0,0,20):C.UVGC_359_2245,(0,0,21):C.UVGC_359_2246,(0,0,22):C.UVGC_359_2248,(0,0,24):C.UVGC_359_2249,(0,0,26):C.UVGC_359_2250,(0,0,27):C.UVGC_390_3359,(0,0,28):C.UVGC_359_2252,(0,0,29):C.UVGC_359_2253,(0,0,30):C.UVGC_359_2255,(0,0,31):C.UVGC_359_2256,(0,0,33):C.UVGC_359_2257,(0,0,37):C.UVGC_359_2260,(0,0,40):C.UVGC_390_3360,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,1):C.UVGC_390_3362,(0,0,12):C.UVGC_390_3363,(0,0,16):C.UVGC_390_3364,(0,0,18):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_282 = CTVertex(name = 'V_282',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.mu__minus__], [P.G__plus__, P.H, P.mu__minus__] ], [ [P.G0, P.H] ], [ [P.G0, P.mu__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.vm, P.W__plus__, P.Z] ], [ [P.vm, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,17):C.UVGC_359_2220,(0,0,19):C.UVGC_359_2221,(0,0,28):C.UVGC_359_2222,(0,0,34):C.UVGC_359_2223,(0,0,35):C.UVGC_359_2224,(0,0,36):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2231,(0,0,1):C.UVGC_395_3551,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_359_2243,(0,0,12):C.UVGC_359_2245,(0,0,14):C.UVGC_359_2246,(0,0,15):C.UVGC_395_3552,(0,0,16):C.UVGC_359_2248,(0,0,18):C.UVGC_359_2249,(0,0,20):C.UVGC_359_2250,(0,0,21):C.UVGC_395_3553,(0,0,22):C.UVGC_395_3554,(0,0,23):C.UVGC_359_2252,(0,0,24):C.UVGC_359_2253,(0,0,25):C.UVGC_395_3555,(0,0,26):C.UVGC_359_2255,(0,0,27):C.UVGC_359_2256,(0,0,29):C.UVGC_359_2257,(0,0,31):C.UVGC_395_3556,(0,0,33):C.UVGC_395_3557,(0,0,37):C.UVGC_359_2260,(0,0,40):C.UVGC_395_3558,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,2):C.UVGC_390_3362,(0,0,13):C.UVGC_395_3559,(0,0,30):C.UVGC_390_3364,(0,0,32):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_283 = CTVertex(name = 'V_283',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.ta__minus__], [P.G__plus__, P.H, P.ta__minus__] ], [ [P.G0, P.H] ], [ [P.G0, P.ta__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.vt, P.W__plus__, P.Z] ], [ [P.vt, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,4):C.UVGC_359_2216,(0,0,6):C.UVGC_359_2217,(0,0,8):C.UVGC_359_2218,(0,0,10):C.UVGC_359_2219,(0,0,17):C.UVGC_359_2220,(0,0,19):C.UVGC_359_2221,(0,0,28):C.UVGC_359_2222,(0,0,30):C.UVGC_359_2223,(0,0,31):C.UVGC_359_2224,(0,0,32):C.UVGC_359_2225,(0,0,38):C.UVGC_359_2226,(0,0,39):C.UVGC_359_2227,(0,0,43):C.UVGC_359_2228,(0,0,45):C.UVGC_359_2229,(0,0,0):C.UVGC_359_2231,(0,0,1):C.UVGC_400_3744,(0,0,3):C.UVGC_359_2233,(0,0,5):C.UVGC_359_2234,(0,0,7):C.UVGC_359_2239,(0,0,9):C.UVGC_359_2242,(0,0,11):C.UVGC_359_2243,(0,0,12):C.UVGC_359_2245,(0,0,14):C.UVGC_359_2246,(0,0,15):C.UVGC_400_3745,(0,0,16):C.UVGC_359_2248,(0,0,18):C.UVGC_359_2249,(0,0,20):C.UVGC_359_2250,(0,0,21):C.UVGC_400_3746,(0,0,22):C.UVGC_400_3747,(0,0,23):C.UVGC_359_2252,(0,0,24):C.UVGC_359_2253,(0,0,25):C.UVGC_400_3748,(0,0,26):C.UVGC_359_2255,(0,0,27):C.UVGC_359_2256,(0,0,29):C.UVGC_359_2257,(0,0,33):C.UVGC_359_2260,(0,0,35):C.UVGC_400_3749,(0,0,37):C.UVGC_400_3750,(0,0,40):C.UVGC_400_3751,(0,0,42):C.UVGC_390_3361,(0,0,44):C.UVGC_359_2261,(0,0,2):C.UVGC_390_3362,(0,0,13):C.UVGC_400_3752,(0,0,34):C.UVGC_390_3364,(0,0,36):C.UVGC_390_3365,(0,0,41):C.UVGC_390_3366})

V_284 = CTVertex(name = 'V_284',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.u] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.G__plus__] ], [ [P.d, P.u] ], [ [P.d, P.W__plus__] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.u] ], [ [P.G0, P.u] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.Z] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_330_1401,(0,1,5):C.UVGC_330_1402,(0,1,7):C.UVGC_330_1403,(0,1,11):C.UVGC_330_1404,(0,1,18):C.UVGC_330_1405,(0,1,20):C.UVGC_330_1406,(0,1,28):C.UVGC_330_1407,(0,1,30):C.UVGC_330_1408,(0,1,31):C.UVGC_330_1409,(0,1,32):C.UVGC_330_1410,(0,1,34):C.UVGC_330_1411,(0,1,36):C.UVGC_330_1412,(0,1,37):C.UVGC_330_1413,(0,1,39):C.UVGC_330_1414,(0,1,0):C.UVGC_330_1416,(0,1,1):C.UVGC_374_2727,(0,1,2):C.UVGC_330_1417,(0,1,4):C.UVGC_330_1418,(0,1,6):C.UVGC_330_1422,(0,1,8):C.UVGC_374_2728,(0,1,9):C.UVGC_330_1424,(0,1,10):C.UVGC_374_2729,(0,1,12):C.UVGC_330_1425,(0,1,24):C.UVGC_374_2730,(0,1,13):C.UVGC_330_1426,(0,1,14):C.UVGC_330_1427,(0,1,16):C.UVGC_374_2731,(0,1,17):C.UVGC_330_1428,(0,1,19):C.UVGC_330_1429,(0,1,21):C.UVGC_330_1430,(0,1,22):C.UVGC_330_1432,(0,1,23):C.UVGC_330_1433,(0,1,25):C.UVGC_374_2732,(0,1,26):C.UVGC_330_1434,(0,1,27):C.UVGC_330_1435,(0,1,29):C.UVGC_330_1436,(0,1,33):C.UVGC_330_1438,(0,1,35):C.UVGC_374_2733,(0,1,38):C.UVGC_330_1439,(0,1,15):C.UVGC_374_2734,(0,2,3):C.UVGC_331_1441,(0,2,5):C.UVGC_331_1442,(0,2,7):C.UVGC_331_1443,(0,2,11):C.UVGC_331_1444,(0,2,18):C.UVGC_331_1445,(0,2,20):C.UVGC_331_1446,(0,2,28):C.UVGC_331_1447,(0,2,30):C.UVGC_331_1448,(0,2,31):C.UVGC_331_1449,(0,2,32):C.UVGC_331_1450,(0,2,34):C.UVGC_331_1451,(0,2,36):C.UVGC_331_1452,(0,2,37):C.UVGC_331_1453,(0,2,39):C.UVGC_331_1454,(0,2,0):C.UVGC_331_1456,(0,2,1):C.UVGC_375_2735,(0,2,2):C.UVGC_331_1457,(0,2,4):C.UVGC_331_1458,(0,2,6):C.UVGC_331_1462,(0,2,8):C.UVGC_375_2736,(0,2,9):C.UVGC_331_1464,(0,2,10):C.UVGC_375_2737,(0,2,12):C.UVGC_331_1465,(0,2,24):C.UVGC_375_2738,(0,2,13):C.UVGC_331_1466,(0,2,14):C.UVGC_331_1467,(0,2,16):C.UVGC_375_2739,(0,2,17):C.UVGC_331_1468,(0,2,19):C.UVGC_331_1469,(0,2,21):C.UVGC_331_1470,(0,2,22):C.UVGC_331_1472,(0,2,23):C.UVGC_331_1473,(0,2,25):C.UVGC_375_2740,(0,2,26):C.UVGC_331_1474,(0,2,27):C.UVGC_331_1475,(0,2,29):C.UVGC_331_1476,(0,2,33):C.UVGC_331_1478,(0,2,35):C.UVGC_375_2741,(0,2,38):C.UVGC_331_1479,(0,2,15):C.UVGC_375_2742,(0,0,3):C.UVGC_282_772,(0,0,5):C.UVGC_282_773,(0,0,7):C.UVGC_282_774,(0,0,11):C.UVGC_282_775,(0,0,18):C.UVGC_282_776,(0,0,20):C.UVGC_282_777,(0,0,28):C.UVGC_282_778,(0,0,30):C.UVGC_282_779,(0,0,31):C.UVGC_282_780,(0,0,32):C.UVGC_282_781,(0,0,34):C.UVGC_282_782,(0,0,37):C.UVGC_282_783,(0,0,22):C.UVGC_282_784})

V_285 = CTVertex(name = 'V_285',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.H] ], [ [P.c, P.H] ], [ [P.c, P.s] ], [ [P.c, P.Z] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.W__plus__] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_330_1401,(0,1,5):C.UVGC_330_1402,(0,1,12):C.UVGC_330_1403,(0,1,14):C.UVGC_330_1404,(0,1,19):C.UVGC_330_1405,(0,1,21):C.UVGC_330_1406,(0,1,28):C.UVGC_330_1407,(0,1,30):C.UVGC_330_1408,(0,1,32):C.UVGC_330_1409,(0,1,33):C.UVGC_330_1410,(0,1,35):C.UVGC_330_1411,(0,1,36):C.UVGC_330_1412,(0,1,37):C.UVGC_330_1413,(0,1,39):C.UVGC_330_1414,(0,1,0):C.UVGC_330_1415,(0,1,1):C.UVGC_330_1416,(0,1,2):C.UVGC_330_1417,(0,1,4):C.UVGC_330_1418,(0,1,6):C.UVGC_330_1419,(0,1,7):C.UVGC_330_1420,(0,1,9):C.UVGC_330_1421,(0,1,10):C.UVGC_330_1422,(0,1,11):C.UVGC_330_1423,(0,1,13):C.UVGC_330_1424,(0,1,15):C.UVGC_330_1425,(0,1,16):C.UVGC_330_1426,(0,1,17):C.UVGC_330_1427,(0,1,18):C.UVGC_330_1428,(0,1,20):C.UVGC_330_1429,(0,1,22):C.UVGC_330_1430,(0,1,23):C.UVGC_330_1431,(0,1,24):C.UVGC_330_1432,(0,1,25):C.UVGC_330_1433,(0,1,26):C.UVGC_330_1434,(0,1,27):C.UVGC_330_1435,(0,1,29):C.UVGC_330_1436,(0,1,31):C.UVGC_330_1437,(0,1,34):C.UVGC_330_1438,(0,1,38):C.UVGC_330_1439,(0,1,8):C.UVGC_330_1440,(0,2,3):C.UVGC_331_1441,(0,2,5):C.UVGC_331_1442,(0,2,12):C.UVGC_331_1443,(0,2,14):C.UVGC_331_1444,(0,2,19):C.UVGC_331_1445,(0,2,21):C.UVGC_331_1446,(0,2,28):C.UVGC_331_1447,(0,2,30):C.UVGC_331_1448,(0,2,32):C.UVGC_331_1449,(0,2,33):C.UVGC_331_1450,(0,2,35):C.UVGC_331_1451,(0,2,36):C.UVGC_331_1452,(0,2,37):C.UVGC_331_1453,(0,2,39):C.UVGC_331_1454,(0,2,0):C.UVGC_331_1455,(0,2,1):C.UVGC_331_1456,(0,2,2):C.UVGC_331_1457,(0,2,4):C.UVGC_331_1458,(0,2,6):C.UVGC_331_1459,(0,2,7):C.UVGC_331_1460,(0,2,9):C.UVGC_331_1461,(0,2,10):C.UVGC_331_1462,(0,2,11):C.UVGC_331_1463,(0,2,13):C.UVGC_331_1464,(0,2,15):C.UVGC_331_1465,(0,2,16):C.UVGC_331_1466,(0,2,17):C.UVGC_331_1467,(0,2,18):C.UVGC_331_1468,(0,2,20):C.UVGC_331_1469,(0,2,22):C.UVGC_331_1470,(0,2,23):C.UVGC_331_1471,(0,2,24):C.UVGC_331_1472,(0,2,25):C.UVGC_331_1473,(0,2,26):C.UVGC_331_1474,(0,2,27):C.UVGC_331_1475,(0,2,29):C.UVGC_331_1476,(0,2,31):C.UVGC_331_1477,(0,2,34):C.UVGC_331_1478,(0,2,38):C.UVGC_331_1479,(0,2,8):C.UVGC_331_1480,(0,0,3):C.UVGC_282_772,(0,0,5):C.UVGC_282_773,(0,0,12):C.UVGC_282_774,(0,0,14):C.UVGC_282_775,(0,0,19):C.UVGC_282_776,(0,0,21):C.UVGC_282_777,(0,0,28):C.UVGC_282_778,(0,0,30):C.UVGC_282_779,(0,0,32):C.UVGC_282_780,(0,0,33):C.UVGC_282_781,(0,0,35):C.UVGC_282_782,(0,0,37):C.UVGC_282_783,(0,0,24):C.UVGC_282_784})

V_286 = CTVertex(name = 'V_286',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.t] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.G__plus__] ], [ [P.b, P.t] ], [ [P.b, P.W__plus__] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.t] ], [ [P.G0, P.t] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_330_1401,(0,1,7):C.UVGC_330_1402,(0,1,9):C.UVGC_330_1403,(0,1,11):C.UVGC_330_1404,(0,1,18):C.UVGC_330_1405,(0,1,20):C.UVGC_330_1406,(0,1,28):C.UVGC_330_1407,(0,1,30):C.UVGC_330_1408,(0,1,31):C.UVGC_330_1409,(0,1,32):C.UVGC_330_1410,(0,1,35):C.UVGC_330_1411,(0,1,36):C.UVGC_330_1412,(0,1,37):C.UVGC_330_1413,(0,1,39):C.UVGC_330_1414,(0,1,0):C.UVGC_330_1416,(0,1,1):C.UVGC_360_2271,(0,1,2):C.UVGC_330_1417,(0,1,4):C.UVGC_360_2272,(0,1,5):C.UVGC_330_1418,(0,1,6):C.UVGC_360_2273,(0,1,8):C.UVGC_330_1422,(0,1,10):C.UVGC_330_1424,(0,1,12):C.UVGC_330_1425,(0,1,24):C.UVGC_360_2274,(0,1,13):C.UVGC_330_1426,(0,1,14):C.UVGC_330_1427,(0,1,16):C.UVGC_360_2275,(0,1,17):C.UVGC_330_1428,(0,1,19):C.UVGC_330_1429,(0,1,21):C.UVGC_330_1430,(0,1,22):C.UVGC_330_1432,(0,1,23):C.UVGC_330_1433,(0,1,25):C.UVGC_360_2276,(0,1,26):C.UVGC_330_1434,(0,1,27):C.UVGC_330_1435,(0,1,29):C.UVGC_330_1436,(0,1,34):C.UVGC_360_2277,(0,1,33):C.UVGC_330_1438,(0,1,38):C.UVGC_330_1439,(0,1,15):C.UVGC_360_2278,(0,2,3):C.UVGC_331_1441,(0,2,7):C.UVGC_331_1442,(0,2,9):C.UVGC_331_1443,(0,2,11):C.UVGC_331_1444,(0,2,18):C.UVGC_331_1445,(0,2,20):C.UVGC_331_1446,(0,2,28):C.UVGC_331_1447,(0,2,30):C.UVGC_331_1448,(0,2,31):C.UVGC_331_1449,(0,2,32):C.UVGC_331_1450,(0,2,35):C.UVGC_331_1451,(0,2,36):C.UVGC_331_1452,(0,2,37):C.UVGC_331_1453,(0,2,39):C.UVGC_331_1454,(0,2,0):C.UVGC_331_1456,(0,2,1):C.UVGC_361_2279,(0,2,2):C.UVGC_331_1457,(0,2,4):C.UVGC_361_2280,(0,2,5):C.UVGC_331_1458,(0,2,6):C.UVGC_361_2281,(0,2,8):C.UVGC_331_1462,(0,2,10):C.UVGC_331_1464,(0,2,12):C.UVGC_331_1465,(0,2,24):C.UVGC_361_2282,(0,2,13):C.UVGC_331_1466,(0,2,14):C.UVGC_331_1467,(0,2,16):C.UVGC_361_2283,(0,2,17):C.UVGC_331_1468,(0,2,19):C.UVGC_331_1469,(0,2,21):C.UVGC_331_1470,(0,2,22):C.UVGC_331_1472,(0,2,23):C.UVGC_331_1473,(0,2,25):C.UVGC_361_2284,(0,2,26):C.UVGC_331_1474,(0,2,27):C.UVGC_331_1475,(0,2,29):C.UVGC_331_1476,(0,2,34):C.UVGC_361_2285,(0,2,33):C.UVGC_331_1478,(0,2,38):C.UVGC_331_1479,(0,2,15):C.UVGC_361_2286,(0,0,3):C.UVGC_282_772,(0,0,7):C.UVGC_282_773,(0,0,9):C.UVGC_282_774,(0,0,11):C.UVGC_282_775,(0,0,18):C.UVGC_282_776,(0,0,20):C.UVGC_282_777,(0,0,28):C.UVGC_282_778,(0,0,30):C.UVGC_282_779,(0,0,31):C.UVGC_282_780,(0,0,32):C.UVGC_282_781,(0,0,35):C.UVGC_282_782,(0,0,37):C.UVGC_282_783,(0,0,22):C.UVGC_282_784})

V_287 = CTVertex(name = 'V_287',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.H] ], [ [P.d, P.H] ], [ [P.d, P.u] ], [ [P.d, P.Z] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.u, P.W__plus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_329_1361,(0,1,5):C.UVGC_329_1362,(0,1,7):C.UVGC_329_1363,(0,1,14):C.UVGC_329_1364,(0,1,19):C.UVGC_329_1365,(0,1,21):C.UVGC_329_1366,(0,1,28):C.UVGC_329_1367,(0,1,30):C.UVGC_329_1368,(0,1,31):C.UVGC_329_1369,(0,1,32):C.UVGC_329_1370,(0,1,34):C.UVGC_329_1371,(0,1,36):C.UVGC_329_1372,(0,1,37):C.UVGC_329_1373,(0,1,39):C.UVGC_329_1374,(0,1,0):C.UVGC_333_1489,(0,1,1):C.UVGC_329_1376,(0,1,2):C.UVGC_329_1377,(0,1,4):C.UVGC_329_1381,(0,1,6):C.UVGC_329_1383,(0,1,8):C.UVGC_333_1490,(0,1,9):C.UVGC_333_1491,(0,1,11):C.UVGC_333_1492,(0,1,12):C.UVGC_329_1384,(0,1,13):C.UVGC_333_1493,(0,1,15):C.UVGC_329_1385,(0,1,16):C.UVGC_329_1386,(0,1,17):C.UVGC_329_1387,(0,1,18):C.UVGC_329_1388,(0,1,20):C.UVGC_329_1389,(0,1,22):C.UVGC_329_1390,(0,1,23):C.UVGC_333_1494,(0,1,24):C.UVGC_329_1392,(0,1,25):C.UVGC_329_1393,(0,1,26):C.UVGC_329_1394,(0,1,27):C.UVGC_329_1395,(0,1,29):C.UVGC_329_1396,(0,1,33):C.UVGC_329_1398,(0,1,35):C.UVGC_333_1495,(0,1,38):C.UVGC_329_1399,(0,1,10):C.UVGC_333_1496,(0,2,3):C.UVGC_328_1321,(0,2,5):C.UVGC_328_1322,(0,2,7):C.UVGC_328_1323,(0,2,14):C.UVGC_328_1324,(0,2,19):C.UVGC_328_1325,(0,2,21):C.UVGC_328_1326,(0,2,28):C.UVGC_328_1327,(0,2,30):C.UVGC_328_1328,(0,2,31):C.UVGC_328_1329,(0,2,32):C.UVGC_328_1330,(0,2,34):C.UVGC_328_1331,(0,2,36):C.UVGC_328_1332,(0,2,37):C.UVGC_328_1333,(0,2,39):C.UVGC_328_1334,(0,2,0):C.UVGC_332_1481,(0,2,1):C.UVGC_328_1336,(0,2,2):C.UVGC_328_1337,(0,2,4):C.UVGC_328_1341,(0,2,6):C.UVGC_328_1343,(0,2,8):C.UVGC_332_1482,(0,2,9):C.UVGC_332_1483,(0,2,11):C.UVGC_332_1484,(0,2,12):C.UVGC_328_1344,(0,2,13):C.UVGC_332_1485,(0,2,15):C.UVGC_328_1345,(0,2,16):C.UVGC_328_1346,(0,2,17):C.UVGC_328_1347,(0,2,18):C.UVGC_328_1348,(0,2,20):C.UVGC_328_1349,(0,2,22):C.UVGC_328_1350,(0,2,23):C.UVGC_332_1486,(0,2,24):C.UVGC_328_1352,(0,2,25):C.UVGC_328_1353,(0,2,26):C.UVGC_328_1354,(0,2,27):C.UVGC_328_1355,(0,2,29):C.UVGC_328_1356,(0,2,33):C.UVGC_328_1358,(0,2,35):C.UVGC_332_1487,(0,2,38):C.UVGC_328_1359,(0,2,10):C.UVGC_332_1488,(0,0,3):C.UVGC_275_743,(0,0,5):C.UVGC_275_744,(0,0,7):C.UVGC_275_745,(0,0,14):C.UVGC_275_746,(0,0,19):C.UVGC_275_747,(0,0,21):C.UVGC_275_748,(0,0,28):C.UVGC_275_749,(0,0,30):C.UVGC_275_750,(0,0,31):C.UVGC_275_751,(0,0,32):C.UVGC_275_752,(0,0,34):C.UVGC_275_753,(0,0,37):C.UVGC_275_754,(0,0,24):C.UVGC_275_755})

V_288 = CTVertex(name = 'V_288',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.s] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.G__plus__] ], [ [P.c, P.s] ], [ [P.c, P.W__plus__] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.s] ], [ [P.G0, P.s] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.s, P.Z] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_329_1361,(0,1,5):C.UVGC_329_1362,(0,1,9):C.UVGC_329_1363,(0,1,11):C.UVGC_329_1364,(0,1,18):C.UVGC_329_1365,(0,1,20):C.UVGC_329_1366,(0,1,28):C.UVGC_329_1367,(0,1,30):C.UVGC_329_1368,(0,1,32):C.UVGC_329_1369,(0,1,33):C.UVGC_329_1370,(0,1,35):C.UVGC_329_1371,(0,1,36):C.UVGC_329_1372,(0,1,37):C.UVGC_329_1373,(0,1,39):C.UVGC_329_1374,(0,1,0):C.UVGC_329_1376,(0,1,1):C.UVGC_349_1798,(0,1,2):C.UVGC_329_1377,(0,1,4):C.UVGC_329_1381,(0,1,6):C.UVGC_349_1799,(0,1,7):C.UVGC_329_1383,(0,1,8):C.UVGC_349_1800,(0,1,10):C.UVGC_329_1384,(0,1,12):C.UVGC_329_1385,(0,1,24):C.UVGC_349_1801,(0,1,13):C.UVGC_329_1386,(0,1,14):C.UVGC_329_1387,(0,1,16):C.UVGC_349_1802,(0,1,17):C.UVGC_329_1388,(0,1,19):C.UVGC_329_1389,(0,1,21):C.UVGC_329_1390,(0,1,22):C.UVGC_329_1392,(0,1,23):C.UVGC_329_1393,(0,1,25):C.UVGC_349_1803,(0,1,26):C.UVGC_329_1394,(0,1,27):C.UVGC_329_1395,(0,1,29):C.UVGC_329_1396,(0,1,31):C.UVGC_349_1804,(0,1,34):C.UVGC_329_1398,(0,1,38):C.UVGC_329_1399,(0,1,15):C.UVGC_349_1805,(0,2,3):C.UVGC_328_1321,(0,2,5):C.UVGC_328_1322,(0,2,9):C.UVGC_328_1323,(0,2,11):C.UVGC_328_1324,(0,2,18):C.UVGC_328_1325,(0,2,20):C.UVGC_328_1326,(0,2,28):C.UVGC_328_1327,(0,2,30):C.UVGC_328_1328,(0,2,32):C.UVGC_328_1329,(0,2,33):C.UVGC_328_1330,(0,2,35):C.UVGC_328_1331,(0,2,36):C.UVGC_328_1332,(0,2,37):C.UVGC_328_1333,(0,2,39):C.UVGC_328_1334,(0,2,0):C.UVGC_328_1336,(0,2,1):C.UVGC_348_1790,(0,2,2):C.UVGC_328_1337,(0,2,4):C.UVGC_328_1341,(0,2,6):C.UVGC_348_1791,(0,2,7):C.UVGC_328_1343,(0,2,8):C.UVGC_348_1792,(0,2,10):C.UVGC_328_1344,(0,2,12):C.UVGC_328_1345,(0,2,24):C.UVGC_348_1793,(0,2,13):C.UVGC_328_1346,(0,2,14):C.UVGC_328_1347,(0,2,16):C.UVGC_348_1794,(0,2,17):C.UVGC_328_1348,(0,2,19):C.UVGC_328_1349,(0,2,21):C.UVGC_328_1350,(0,2,22):C.UVGC_328_1352,(0,2,23):C.UVGC_328_1353,(0,2,25):C.UVGC_348_1795,(0,2,26):C.UVGC_328_1354,(0,2,27):C.UVGC_328_1355,(0,2,29):C.UVGC_328_1356,(0,2,31):C.UVGC_348_1796,(0,2,34):C.UVGC_328_1358,(0,2,38):C.UVGC_328_1359,(0,2,15):C.UVGC_348_1797,(0,0,3):C.UVGC_275_743,(0,0,5):C.UVGC_275_744,(0,0,9):C.UVGC_275_745,(0,0,11):C.UVGC_275_746,(0,0,18):C.UVGC_275_747,(0,0,20):C.UVGC_275_748,(0,0,28):C.UVGC_275_749,(0,0,30):C.UVGC_275_750,(0,0,32):C.UVGC_275_751,(0,0,33):C.UVGC_275_752,(0,0,35):C.UVGC_275_753,(0,0,37):C.UVGC_275_754,(0,0,22):C.UVGC_275_755})

V_289 = CTVertex(name = 'V_289',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.H] ], [ [P.b, P.H] ], [ [P.b, P.t] ], [ [P.b, P.Z] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.t, P.W__plus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_329_1361,(0,1,10):C.UVGC_329_1362,(0,1,12):C.UVGC_329_1363,(0,1,14):C.UVGC_329_1364,(0,1,19):C.UVGC_329_1365,(0,1,21):C.UVGC_329_1366,(0,1,28):C.UVGC_329_1367,(0,1,30):C.UVGC_329_1368,(0,1,31):C.UVGC_329_1369,(0,1,32):C.UVGC_329_1370,(0,1,35):C.UVGC_329_1371,(0,1,36):C.UVGC_329_1372,(0,1,37):C.UVGC_329_1373,(0,1,39):C.UVGC_329_1374,(0,1,0):C.UVGC_329_1375,(0,1,1):C.UVGC_329_1376,(0,1,2):C.UVGC_329_1377,(0,1,4):C.UVGC_329_1378,(0,1,5):C.UVGC_329_1379,(0,1,7):C.UVGC_329_1380,(0,1,8):C.UVGC_329_1381,(0,1,9):C.UVGC_329_1382,(0,1,11):C.UVGC_329_1383,(0,1,13):C.UVGC_329_1384,(0,1,15):C.UVGC_329_1385,(0,1,16):C.UVGC_329_1386,(0,1,17):C.UVGC_329_1387,(0,1,18):C.UVGC_329_1388,(0,1,20):C.UVGC_329_1389,(0,1,22):C.UVGC_329_1390,(0,1,23):C.UVGC_329_1391,(0,1,24):C.UVGC_329_1392,(0,1,25):C.UVGC_329_1393,(0,1,26):C.UVGC_329_1394,(0,1,27):C.UVGC_329_1395,(0,1,29):C.UVGC_329_1396,(0,1,34):C.UVGC_329_1397,(0,1,33):C.UVGC_329_1398,(0,1,38):C.UVGC_329_1399,(0,1,6):C.UVGC_329_1400,(0,2,3):C.UVGC_328_1321,(0,2,10):C.UVGC_328_1322,(0,2,12):C.UVGC_328_1323,(0,2,14):C.UVGC_328_1324,(0,2,19):C.UVGC_328_1325,(0,2,21):C.UVGC_328_1326,(0,2,28):C.UVGC_328_1327,(0,2,30):C.UVGC_328_1328,(0,2,31):C.UVGC_328_1329,(0,2,32):C.UVGC_328_1330,(0,2,35):C.UVGC_328_1331,(0,2,36):C.UVGC_328_1332,(0,2,37):C.UVGC_328_1333,(0,2,39):C.UVGC_328_1334,(0,2,0):C.UVGC_328_1335,(0,2,1):C.UVGC_328_1336,(0,2,2):C.UVGC_328_1337,(0,2,4):C.UVGC_328_1338,(0,2,5):C.UVGC_328_1339,(0,2,7):C.UVGC_328_1340,(0,2,8):C.UVGC_328_1341,(0,2,9):C.UVGC_328_1342,(0,2,11):C.UVGC_328_1343,(0,2,13):C.UVGC_328_1344,(0,2,15):C.UVGC_328_1345,(0,2,16):C.UVGC_328_1346,(0,2,17):C.UVGC_328_1347,(0,2,18):C.UVGC_328_1348,(0,2,20):C.UVGC_328_1349,(0,2,22):C.UVGC_328_1350,(0,2,23):C.UVGC_328_1351,(0,2,24):C.UVGC_328_1352,(0,2,25):C.UVGC_328_1353,(0,2,26):C.UVGC_328_1354,(0,2,27):C.UVGC_328_1355,(0,2,29):C.UVGC_328_1356,(0,2,34):C.UVGC_328_1357,(0,2,33):C.UVGC_328_1358,(0,2,38):C.UVGC_328_1359,(0,2,6):C.UVGC_328_1360,(0,0,3):C.UVGC_275_743,(0,0,10):C.UVGC_275_744,(0,0,12):C.UVGC_275_745,(0,0,14):C.UVGC_275_746,(0,0,19):C.UVGC_275_747,(0,0,21):C.UVGC_275_748,(0,0,28):C.UVGC_275_749,(0,0,30):C.UVGC_275_750,(0,0,31):C.UVGC_275_751,(0,0,32):C.UVGC_275_752,(0,0,35):C.UVGC_275_753,(0,0,37):C.UVGC_275_754,(0,0,24):C.UVGC_275_755})

V_290 = CTVertex(name = 'V_290',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.W__plus__] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_307_1005,(0,0,4):C.UVGC_307_1006,(0,0,6):C.UVGC_307_1007,(0,0,8):C.UVGC_307_1008,(0,0,15):C.UVGC_307_1009,(0,0,17):C.UVGC_307_1010,(0,0,23):C.UVGC_307_1011,(0,0,25):C.UVGC_307_1012,(0,0,26):C.UVGC_307_1013,(0,0,27):C.UVGC_307_1014,(0,0,29):C.UVGC_307_1015,(0,0,30):C.UVGC_307_1016,(0,0,32):C.UVGC_307_1017,(0,0,34):C.UVGC_307_1018,(0,0,0):C.UVGC_307_1019,(0,0,1):C.UVGC_307_1020,(0,0,3):C.UVGC_307_1021,(0,0,5):C.UVGC_307_1022,(0,0,7):C.UVGC_307_1023,(0,0,9):C.UVGC_307_1024,(0,0,10):C.UVGC_307_1025,(0,0,11):C.UVGC_307_1026,(0,0,12):C.UVGC_307_1027,(0,0,13):C.UVGC_307_1028,(0,0,14):C.UVGC_307_1029,(0,0,16):C.UVGC_307_1030,(0,0,18):C.UVGC_307_1031,(0,0,19):C.UVGC_307_1032,(0,0,20):C.UVGC_307_1033,(0,0,21):C.UVGC_307_1034,(0,0,22):C.UVGC_307_1035,(0,0,24):C.UVGC_307_1036,(0,0,28):C.UVGC_307_1037,(0,0,31):C.UVGC_307_1038,(0,0,33):C.UVGC_307_1039})

V_291 = CTVertex(name = 'V_291',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.mu__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_307_1005,(0,0,4):C.UVGC_307_1006,(0,0,6):C.UVGC_307_1007,(0,0,8):C.UVGC_307_1008,(0,0,13):C.UVGC_307_1009,(0,0,15):C.UVGC_307_1010,(0,0,22):C.UVGC_307_1011,(0,0,25):C.UVGC_307_1012,(0,0,26):C.UVGC_307_1013,(0,0,27):C.UVGC_307_1014,(0,0,29):C.UVGC_307_1015,(0,0,30):C.UVGC_307_1016,(0,0,32):C.UVGC_307_1017,(0,0,34):C.UVGC_307_1018,(0,0,0):C.UVGC_307_1019,(0,0,1):C.UVGC_307_1020,(0,0,3):C.UVGC_307_1021,(0,0,5):C.UVGC_307_1022,(0,0,7):C.UVGC_307_1023,(0,0,9):C.UVGC_307_1025,(0,0,10):C.UVGC_307_1027,(0,0,11):C.UVGC_307_1028,(0,0,12):C.UVGC_307_1029,(0,0,14):C.UVGC_307_1030,(0,0,16):C.UVGC_307_1031,(0,0,17):C.UVGC_308_1040,(0,0,18):C.UVGC_307_1032,(0,0,19):C.UVGC_307_1033,(0,0,20):C.UVGC_307_1034,(0,0,21):C.UVGC_307_1035,(0,0,23):C.UVGC_307_1036,(0,0,24):C.UVGC_308_1041,(0,0,28):C.UVGC_307_1037,(0,0,31):C.UVGC_307_1038,(0,0,33):C.UVGC_307_1039})

V_292 = CTVertex(name = 'V_292',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ta__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.Z] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_307_1005,(0,0,4):C.UVGC_307_1006,(0,0,6):C.UVGC_307_1007,(0,0,8):C.UVGC_307_1008,(0,0,13):C.UVGC_307_1009,(0,0,15):C.UVGC_307_1010,(0,0,22):C.UVGC_307_1011,(0,0,24):C.UVGC_307_1012,(0,0,25):C.UVGC_307_1013,(0,0,26):C.UVGC_307_1014,(0,0,29):C.UVGC_307_1015,(0,0,30):C.UVGC_307_1016,(0,0,32):C.UVGC_307_1017,(0,0,34):C.UVGC_307_1018,(0,0,0):C.UVGC_307_1019,(0,0,1):C.UVGC_307_1020,(0,0,3):C.UVGC_307_1021,(0,0,5):C.UVGC_307_1022,(0,0,7):C.UVGC_307_1023,(0,0,9):C.UVGC_307_1025,(0,0,10):C.UVGC_307_1027,(0,0,11):C.UVGC_307_1028,(0,0,12):C.UVGC_307_1029,(0,0,14):C.UVGC_307_1030,(0,0,16):C.UVGC_307_1031,(0,0,17):C.UVGC_309_1042,(0,0,18):C.UVGC_307_1032,(0,0,19):C.UVGC_307_1033,(0,0,20):C.UVGC_307_1034,(0,0,21):C.UVGC_307_1035,(0,0,23):C.UVGC_307_1036,(0,0,27):C.UVGC_307_1037,(0,0,28):C.UVGC_309_1043,(0,0,31):C.UVGC_307_1038,(0,0,33):C.UVGC_307_1039})

V_293 = CTVertex(name = 'V_293',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.H] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.Z] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.ve] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.ve, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_335_1536,(0,1,5):C.UVGC_335_1537,(0,1,7):C.UVGC_335_1538,(0,1,9):C.UVGC_335_1539,(0,1,18):C.UVGC_335_1540,(0,1,20):C.UVGC_335_1541,(0,1,27):C.UVGC_335_1542,(0,1,29):C.UVGC_335_1543,(0,1,30):C.UVGC_335_1544,(0,1,31):C.UVGC_335_1545,(0,1,33):C.UVGC_335_1546,(0,1,34):C.UVGC_335_1547,(0,1,36):C.UVGC_335_1548,(0,1,38):C.UVGC_335_1549,(0,1,0):C.UVGC_335_1550,(0,1,1):C.UVGC_335_1551,(0,1,2):C.UVGC_335_1552,(0,1,4):C.UVGC_335_1553,(0,1,6):C.UVGC_335_1554,(0,1,8):C.UVGC_335_1555,(0,1,10):C.UVGC_335_1556,(0,1,12):C.UVGC_335_1557,(0,1,13):C.UVGC_335_1558,(0,1,14):C.UVGC_335_1559,(0,1,15):C.UVGC_335_1560,(0,1,16):C.UVGC_335_1561,(0,1,17):C.UVGC_335_1562,(0,1,19):C.UVGC_335_1563,(0,1,21):C.UVGC_335_1564,(0,1,22):C.UVGC_335_1565,(0,1,23):C.UVGC_335_1566,(0,1,24):C.UVGC_335_1567,(0,1,25):C.UVGC_335_1568,(0,1,26):C.UVGC_335_1569,(0,1,28):C.UVGC_335_1570,(0,1,32):C.UVGC_335_1571,(0,1,35):C.UVGC_335_1572,(0,1,37):C.UVGC_335_1573,(0,1,11):C.UVGC_335_1574,(0,2,3):C.UVGC_334_1497,(0,2,5):C.UVGC_334_1498,(0,2,7):C.UVGC_334_1499,(0,2,9):C.UVGC_334_1500,(0,2,18):C.UVGC_334_1501,(0,2,20):C.UVGC_334_1502,(0,2,27):C.UVGC_334_1503,(0,2,29):C.UVGC_334_1504,(0,2,30):C.UVGC_334_1505,(0,2,31):C.UVGC_334_1506,(0,2,33):C.UVGC_334_1507,(0,2,34):C.UVGC_334_1508,(0,2,36):C.UVGC_334_1509,(0,2,38):C.UVGC_334_1510,(0,2,0):C.UVGC_334_1511,(0,2,1):C.UVGC_334_1512,(0,2,2):C.UVGC_334_1513,(0,2,4):C.UVGC_334_1514,(0,2,6):C.UVGC_334_1515,(0,2,8):C.UVGC_334_1516,(0,2,10):C.UVGC_334_1517,(0,2,12):C.UVGC_334_1518,(0,2,13):C.UVGC_334_1519,(0,2,14):C.UVGC_334_1520,(0,2,15):C.UVGC_334_1521,(0,2,16):C.UVGC_334_1522,(0,2,17):C.UVGC_334_1523,(0,2,19):C.UVGC_334_1524,(0,2,21):C.UVGC_334_1525,(0,2,22):C.UVGC_334_1526,(0,2,23):C.UVGC_334_1527,(0,2,24):C.UVGC_334_1528,(0,2,25):C.UVGC_334_1529,(0,2,26):C.UVGC_334_1530,(0,2,28):C.UVGC_334_1531,(0,2,32):C.UVGC_334_1532,(0,2,35):C.UVGC_334_1533,(0,2,37):C.UVGC_334_1534,(0,2,11):C.UVGC_334_1535,(0,0,3):C.UVGC_289_809,(0,0,5):C.UVGC_289_810,(0,0,7):C.UVGC_289_811,(0,0,9):C.UVGC_289_812,(0,0,18):C.UVGC_289_813,(0,0,20):C.UVGC_289_814,(0,0,27):C.UVGC_289_815,(0,0,29):C.UVGC_289_816,(0,0,30):C.UVGC_289_817,(0,0,31):C.UVGC_289_818,(0,0,33):C.UVGC_289_819,(0,0,36):C.UVGC_289_820,(0,0,23):C.UVGC_289_821})

V_294 = CTVertex(name = 'V_294',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.mu__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vm] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vm, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_335_1536,(0,1,5):C.UVGC_335_1537,(0,1,7):C.UVGC_335_1538,(0,1,9):C.UVGC_335_1539,(0,1,16):C.UVGC_335_1540,(0,1,18):C.UVGC_335_1541,(0,1,26):C.UVGC_335_1542,(0,1,29):C.UVGC_335_1543,(0,1,30):C.UVGC_335_1544,(0,1,31):C.UVGC_335_1545,(0,1,33):C.UVGC_335_1546,(0,1,34):C.UVGC_335_1547,(0,1,36):C.UVGC_335_1548,(0,1,38):C.UVGC_335_1549,(0,1,0):C.UVGC_335_1551,(0,1,1):C.UVGC_347_1783,(0,1,2):C.UVGC_335_1552,(0,1,4):C.UVGC_335_1553,(0,1,6):C.UVGC_335_1554,(0,1,8):C.UVGC_335_1555,(0,1,10):C.UVGC_335_1558,(0,1,11):C.UVGC_335_1560,(0,1,12):C.UVGC_335_1561,(0,1,14):C.UVGC_347_1784,(0,1,15):C.UVGC_335_1562,(0,1,17):C.UVGC_335_1563,(0,1,19):C.UVGC_335_1564,(0,1,20):C.UVGC_347_1785,(0,1,21):C.UVGC_335_1566,(0,1,22):C.UVGC_335_1567,(0,1,23):C.UVGC_347_1786,(0,1,24):C.UVGC_335_1568,(0,1,25):C.UVGC_335_1569,(0,1,27):C.UVGC_335_1570,(0,1,28):C.UVGC_347_1787,(0,1,32):C.UVGC_335_1571,(0,1,35):C.UVGC_347_1788,(0,1,37):C.UVGC_335_1573,(0,1,13):C.UVGC_347_1789,(0,2,3):C.UVGC_334_1497,(0,2,5):C.UVGC_334_1498,(0,2,7):C.UVGC_334_1499,(0,2,9):C.UVGC_334_1500,(0,2,16):C.UVGC_334_1501,(0,2,18):C.UVGC_334_1502,(0,2,26):C.UVGC_334_1503,(0,2,29):C.UVGC_334_1504,(0,2,30):C.UVGC_334_1505,(0,2,31):C.UVGC_334_1506,(0,2,33):C.UVGC_334_1507,(0,2,34):C.UVGC_334_1508,(0,2,36):C.UVGC_334_1509,(0,2,38):C.UVGC_334_1510,(0,2,0):C.UVGC_334_1512,(0,2,1):C.UVGC_346_1776,(0,2,2):C.UVGC_334_1513,(0,2,4):C.UVGC_334_1514,(0,2,6):C.UVGC_334_1515,(0,2,8):C.UVGC_334_1516,(0,2,10):C.UVGC_334_1519,(0,2,11):C.UVGC_334_1521,(0,2,12):C.UVGC_334_1522,(0,2,14):C.UVGC_346_1777,(0,2,15):C.UVGC_334_1523,(0,2,17):C.UVGC_334_1524,(0,2,19):C.UVGC_334_1525,(0,2,20):C.UVGC_346_1778,(0,2,21):C.UVGC_334_1527,(0,2,22):C.UVGC_334_1528,(0,2,23):C.UVGC_346_1779,(0,2,24):C.UVGC_334_1529,(0,2,25):C.UVGC_334_1530,(0,2,27):C.UVGC_334_1531,(0,2,28):C.UVGC_346_1780,(0,2,32):C.UVGC_334_1532,(0,2,35):C.UVGC_346_1781,(0,2,37):C.UVGC_334_1534,(0,2,13):C.UVGC_346_1782,(0,0,3):C.UVGC_289_809,(0,0,5):C.UVGC_289_810,(0,0,7):C.UVGC_289_811,(0,0,9):C.UVGC_289_812,(0,0,16):C.UVGC_289_813,(0,0,18):C.UVGC_289_814,(0,0,26):C.UVGC_289_815,(0,0,29):C.UVGC_289_816,(0,0,30):C.UVGC_289_817,(0,0,31):C.UVGC_289_818,(0,0,33):C.UVGC_289_819,(0,0,36):C.UVGC_289_820,(0,0,21):C.UVGC_289_821})

V_295 = CTVertex(name = 'V_295',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV4, L.FFV5, L.FFV6 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.ta__minus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.H] ], [ [P.G0, P.H, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.vt] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.vt, P.W__plus__] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,1,3):C.UVGC_335_1536,(0,1,5):C.UVGC_335_1537,(0,1,7):C.UVGC_335_1538,(0,1,9):C.UVGC_335_1539,(0,1,16):C.UVGC_335_1540,(0,1,18):C.UVGC_335_1541,(0,1,26):C.UVGC_335_1542,(0,1,28):C.UVGC_335_1543,(0,1,29):C.UVGC_335_1544,(0,1,30):C.UVGC_335_1545,(0,1,33):C.UVGC_335_1546,(0,1,34):C.UVGC_335_1547,(0,1,36):C.UVGC_335_1548,(0,1,38):C.UVGC_335_1549,(0,1,0):C.UVGC_335_1551,(0,1,1):C.UVGC_373_2720,(0,1,2):C.UVGC_335_1552,(0,1,4):C.UVGC_335_1553,(0,1,6):C.UVGC_335_1554,(0,1,8):C.UVGC_335_1555,(0,1,10):C.UVGC_335_1558,(0,1,11):C.UVGC_335_1560,(0,1,12):C.UVGC_335_1561,(0,1,14):C.UVGC_373_2721,(0,1,15):C.UVGC_335_1562,(0,1,17):C.UVGC_335_1563,(0,1,19):C.UVGC_335_1564,(0,1,20):C.UVGC_373_2722,(0,1,21):C.UVGC_335_1566,(0,1,22):C.UVGC_335_1567,(0,1,23):C.UVGC_373_2723,(0,1,24):C.UVGC_335_1568,(0,1,25):C.UVGC_335_1569,(0,1,27):C.UVGC_335_1570,(0,1,31):C.UVGC_335_1571,(0,1,32):C.UVGC_373_2724,(0,1,35):C.UVGC_373_2725,(0,1,37):C.UVGC_335_1573,(0,1,13):C.UVGC_373_2726,(0,2,3):C.UVGC_334_1497,(0,2,5):C.UVGC_334_1498,(0,2,7):C.UVGC_334_1499,(0,2,9):C.UVGC_334_1500,(0,2,16):C.UVGC_334_1501,(0,2,18):C.UVGC_334_1502,(0,2,26):C.UVGC_334_1503,(0,2,28):C.UVGC_334_1504,(0,2,29):C.UVGC_334_1505,(0,2,30):C.UVGC_334_1506,(0,2,33):C.UVGC_334_1507,(0,2,34):C.UVGC_334_1508,(0,2,36):C.UVGC_334_1509,(0,2,38):C.UVGC_334_1510,(0,2,0):C.UVGC_334_1512,(0,2,1):C.UVGC_372_2713,(0,2,2):C.UVGC_334_1513,(0,2,4):C.UVGC_334_1514,(0,2,6):C.UVGC_334_1515,(0,2,8):C.UVGC_334_1516,(0,2,10):C.UVGC_334_1519,(0,2,11):C.UVGC_334_1521,(0,2,12):C.UVGC_334_1522,(0,2,14):C.UVGC_372_2714,(0,2,15):C.UVGC_334_1523,(0,2,17):C.UVGC_334_1524,(0,2,19):C.UVGC_334_1525,(0,2,20):C.UVGC_372_2715,(0,2,21):C.UVGC_334_1527,(0,2,22):C.UVGC_334_1528,(0,2,23):C.UVGC_372_2716,(0,2,24):C.UVGC_334_1529,(0,2,25):C.UVGC_334_1530,(0,2,27):C.UVGC_334_1531,(0,2,31):C.UVGC_334_1532,(0,2,32):C.UVGC_372_2717,(0,2,35):C.UVGC_372_2718,(0,2,37):C.UVGC_334_1534,(0,2,13):C.UVGC_372_2719,(0,0,3):C.UVGC_289_809,(0,0,5):C.UVGC_289_810,(0,0,7):C.UVGC_289_811,(0,0,9):C.UVGC_289_812,(0,0,16):C.UVGC_289_813,(0,0,18):C.UVGC_289_814,(0,0,26):C.UVGC_289_815,(0,0,28):C.UVGC_289_816,(0,0,29):C.UVGC_289_817,(0,0,30):C.UVGC_289_818,(0,0,33):C.UVGC_289_819,(0,0,36):C.UVGC_289_820,(0,0,21):C.UVGC_289_821})

V_296 = CTVertex(name = 'V_296',
                 type = 'UV',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S2 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.H] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_205_324,(0,0,1):C.UVGC_205_325,(0,0,2):C.UVGC_205_326,(0,0,3):C.UVGC_205_327,(0,0,4):C.UVGC_205_328,(0,0,5):C.UVGC_205_329,(0,0,6):C.UVGC_205_330,(0,0,7):C.UVGC_205_331,(0,0,8):C.UVGC_205_332,(0,0,9):C.UVGC_205_333,(0,0,10):C.UVGC_205_334,(0,0,11):C.UVGC_205_335,(0,0,12):C.UVGC_205_336,(0,0,13):C.UVGC_205_337,(0,0,14):C.UVGC_205_338,(0,0,15):C.UVGC_205_339})

V_297 = CTVertex(name = 'V_297',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_251_546,(0,2,1):C.UVGC_251_547,(0,2,3):C.UVGC_251_548,(0,2,4):C.UVGC_251_549,(0,2,5):C.UVGC_251_550,(0,2,6):C.UVGC_251_551,(0,4,0):C.UVGC_251_546,(0,4,1):C.UVGC_251_547,(0,4,3):C.UVGC_251_548,(0,4,4):C.UVGC_251_549,(0,4,5):C.UVGC_251_550,(0,4,6):C.UVGC_251_551,(0,3,0):C.UVGC_250_540,(0,3,1):C.UVGC_250_541,(0,3,3):C.UVGC_250_542,(0,3,4):C.UVGC_252_552,(0,3,5):C.UVGC_252_553,(0,3,6):C.UVGC_252_554,(0,0,0):C.UVGC_250_540,(0,0,1):C.UVGC_250_541,(0,0,3):C.UVGC_250_542,(0,0,4):C.UVGC_250_543,(0,0,5):C.UVGC_250_544,(0,0,6):C.UVGC_250_545,(0,1,2):C.UVGC_210_354})

V_298 = CTVertex(name = 'V_298',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_253_555,(0,0,1):C.UVGC_253_556,(0,0,2):C.UVGC_253_557})

V_299 = CTVertex(name = 'V_299',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_255_564,(0,2,1):C.UVGC_255_565,(0,2,3):C.UVGC_255_566,(0,2,4):C.UVGC_255_567,(0,2,5):C.UVGC_255_568,(0,2,6):C.UVGC_255_569,(0,4,0):C.UVGC_255_564,(0,4,1):C.UVGC_255_565,(0,4,3):C.UVGC_255_566,(0,4,4):C.UVGC_255_567,(0,4,5):C.UVGC_255_568,(0,4,6):C.UVGC_255_569,(0,3,0):C.UVGC_254_558,(0,3,1):C.UVGC_254_559,(0,3,3):C.UVGC_256_570,(0,3,4):C.UVGC_254_561,(0,3,5):C.UVGC_256_571,(0,3,6):C.UVGC_256_572,(0,0,0):C.UVGC_254_558,(0,0,1):C.UVGC_254_559,(0,0,3):C.UVGC_254_560,(0,0,4):C.UVGC_254_561,(0,0,5):C.UVGC_254_562,(0,0,6):C.UVGC_254_563,(0,1,2):C.UVGC_213_363})

V_300 = CTVertex(name = 'V_300',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_257_573,(0,0,1):C.UVGC_257_574,(0,0,2):C.UVGC_253_557})

V_301 = CTVertex(name = 'V_301',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_259_581,(0,2,1):C.UVGC_259_582,(0,2,3):C.UVGC_259_583,(0,2,4):C.UVGC_259_584,(0,2,5):C.UVGC_259_585,(0,2,6):C.UVGC_259_586,(0,4,0):C.UVGC_259_581,(0,4,1):C.UVGC_259_582,(0,4,3):C.UVGC_259_583,(0,4,4):C.UVGC_259_584,(0,4,5):C.UVGC_259_585,(0,4,6):C.UVGC_259_586,(0,3,0):C.UVGC_258_575,(0,3,1):C.UVGC_258_576,(0,3,3):C.UVGC_260_587,(0,3,4):C.UVGC_258_578,(0,3,5):C.UVGC_260_588,(0,3,6):C.UVGC_260_589,(0,0,0):C.UVGC_258_575,(0,0,1):C.UVGC_258_576,(0,0,3):C.UVGC_258_577,(0,0,4):C.UVGC_258_578,(0,0,5):C.UVGC_258_579,(0,0,6):C.UVGC_258_580,(0,1,2):C.UVGC_237_483})

V_302 = CTVertex(name = 'V_302',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF8 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_261_590,(0,0,1):C.UVGC_261_591,(0,0,2):C.UVGC_253_557})

V_303 = CTVertex(name = 'V_303',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,2,0):C.UVGC_245_513,(0,2,1):C.UVGC_245_514,(0,2,2):C.UVGC_245_515,(0,2,4):C.UVGC_245_516,(0,2,3):C.UVGC_245_517,(0,2,5):C.UVGC_245_518,(0,2,6):C.UVGC_245_519,(0,4,0):C.UVGC_245_513,(0,4,1):C.UVGC_245_514,(0,4,2):C.UVGC_245_515,(0,4,4):C.UVGC_245_516,(0,4,3):C.UVGC_245_517,(0,4,5):C.UVGC_245_518,(0,4,6):C.UVGC_245_519,(0,3,0):C.UVGC_246_520,(0,3,1):C.UVGC_247_527,(0,3,2):C.UVGC_247_528,(0,3,4):C.UVGC_246_523,(0,3,3):C.UVGC_246_524,(0,3,5):C.UVGC_246_525,(0,3,6):C.UVGC_247_529,(0,0,0):C.UVGC_246_520,(0,0,1):C.UVGC_246_521,(0,0,2):C.UVGC_246_522,(0,0,4):C.UVGC_246_523,(0,0,3):C.UVGC_246_524,(0,0,5):C.UVGC_246_525,(0,0,6):C.UVGC_246_526,(0,1,5):C.UVGC_142_11})

V_304 = CTVertex(name = 'V_304',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_240_486,(0,2,1):C.UVGC_240_487,(0,2,2):C.UVGC_240_488,(0,2,3):C.UVGC_240_489,(0,2,4):C.UVGC_240_490,(0,2,5):C.UVGC_240_491,(0,2,6):C.UVGC_240_492,(0,4,0):C.UVGC_240_486,(0,4,1):C.UVGC_240_487,(0,4,2):C.UVGC_240_488,(0,4,3):C.UVGC_240_489,(0,4,4):C.UVGC_240_490,(0,4,5):C.UVGC_240_491,(0,4,6):C.UVGC_240_492,(0,3,0):C.UVGC_241_493,(0,3,1):C.UVGC_241_494,(0,3,2):C.UVGC_241_495,(0,3,3):C.UVGC_241_496,(0,3,4):C.UVGC_242_500,(0,3,5):C.UVGC_242_501,(0,3,6):C.UVGC_242_502,(0,0,0):C.UVGC_241_493,(0,0,1):C.UVGC_241_494,(0,0,2):C.UVGC_241_495,(0,0,3):C.UVGC_241_496,(0,0,4):C.UVGC_241_497,(0,0,5):C.UVGC_241_498,(0,0,6):C.UVGC_241_499,(0,1,3):C.UVGC_209_353})

V_305 = CTVertex(name = 'V_305',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_216_372,(0,2,1):C.UVGC_216_373,(0,2,2):C.UVGC_216_374,(0,2,3):C.UVGC_216_375,(0,2,4):C.UVGC_216_376,(0,2,5):C.UVGC_216_377,(0,2,6):C.UVGC_216_378,(0,4,0):C.UVGC_216_372,(0,4,1):C.UVGC_216_373,(0,4,2):C.UVGC_216_374,(0,4,3):C.UVGC_216_375,(0,4,4):C.UVGC_216_376,(0,4,5):C.UVGC_216_377,(0,4,6):C.UVGC_216_378,(0,3,0):C.UVGC_215_365,(0,3,1):C.UVGC_215_366,(0,3,2):C.UVGC_215_367,(0,3,3):C.UVGC_215_368,(0,3,4):C.UVGC_217_379,(0,3,5):C.UVGC_217_380,(0,3,6):C.UVGC_217_381,(0,0,0):C.UVGC_215_365,(0,0,1):C.UVGC_215_366,(0,0,2):C.UVGC_215_367,(0,0,3):C.UVGC_215_368,(0,0,4):C.UVGC_215_369,(0,0,5):C.UVGC_215_370,(0,0,6):C.UVGC_215_371,(0,1,3):C.UVGC_140_9})

V_306 = CTVertex(name = 'V_306',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,2,0):C.UVGC_221_407,(0,2,1):C.UVGC_221_408,(0,2,2):C.UVGC_221_409,(0,2,4):C.UVGC_221_410,(0,2,3):C.UVGC_221_411,(0,2,5):C.UVGC_221_412,(0,2,6):C.UVGC_221_413,(0,4,0):C.UVGC_221_407,(0,4,1):C.UVGC_221_408,(0,4,2):C.UVGC_221_409,(0,4,4):C.UVGC_221_410,(0,4,3):C.UVGC_221_411,(0,4,5):C.UVGC_221_412,(0,4,6):C.UVGC_221_413,(0,3,0):C.UVGC_220_400,(0,3,1):C.UVGC_222_414,(0,3,2):C.UVGC_222_415,(0,3,4):C.UVGC_220_403,(0,3,3):C.UVGC_220_404,(0,3,5):C.UVGC_220_405,(0,3,6):C.UVGC_222_416,(0,0,0):C.UVGC_220_400,(0,0,1):C.UVGC_220_401,(0,0,2):C.UVGC_220_402,(0,0,4):C.UVGC_220_403,(0,0,3):C.UVGC_220_404,(0,0,5):C.UVGC_220_405,(0,0,6):C.UVGC_220_406,(0,1,5):C.UVGC_214_364})

V_307 = CTVertex(name = 'V_307',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,2,0):C.UVGC_234_466,(0,2,1):C.UVGC_234_467,(0,2,2):C.UVGC_234_468,(0,2,4):C.UVGC_234_469,(0,2,3):C.UVGC_234_470,(0,2,5):C.UVGC_234_471,(0,2,6):C.UVGC_234_472,(0,4,0):C.UVGC_234_466,(0,4,1):C.UVGC_234_467,(0,4,2):C.UVGC_234_468,(0,4,4):C.UVGC_234_469,(0,4,3):C.UVGC_234_470,(0,4,5):C.UVGC_234_471,(0,4,6):C.UVGC_234_472,(0,3,0):C.UVGC_232_456,(0,3,1):C.UVGC_233_463,(0,3,2):C.UVGC_233_464,(0,3,4):C.UVGC_232_459,(0,3,3):C.UVGC_232_460,(0,3,5):C.UVGC_232_461,(0,3,6):C.UVGC_233_465,(0,0,0):C.UVGC_232_456,(0,0,1):C.UVGC_232_457,(0,0,2):C.UVGC_232_458,(0,0,4):C.UVGC_232_459,(0,0,3):C.UVGC_232_460,(0,0,5):C.UVGC_232_461,(0,0,6):C.UVGC_232_462,(0,1,5):C.UVGC_141_10})

V_308 = CTVertex(name = 'V_308',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF10, L.FF6, L.FF7, L.FF8, L.FF9 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_228_436,(0,2,1):C.UVGC_228_437,(0,2,2):C.UVGC_228_438,(0,2,3):C.UVGC_228_439,(0,2,4):C.UVGC_228_440,(0,2,5):C.UVGC_228_441,(0,2,6):C.UVGC_228_442,(0,4,0):C.UVGC_228_436,(0,4,1):C.UVGC_228_437,(0,4,2):C.UVGC_228_438,(0,4,3):C.UVGC_228_439,(0,4,4):C.UVGC_228_440,(0,4,5):C.UVGC_228_441,(0,4,6):C.UVGC_228_442,(0,3,0):C.UVGC_227_429,(0,3,1):C.UVGC_227_430,(0,3,2):C.UVGC_227_431,(0,3,3):C.UVGC_227_432,(0,3,4):C.UVGC_229_443,(0,3,5):C.UVGC_229_444,(0,3,6):C.UVGC_229_445,(0,0,0):C.UVGC_227_429,(0,0,1):C.UVGC_227_430,(0,0,2):C.UVGC_227_431,(0,0,3):C.UVGC_227_432,(0,0,4):C.UVGC_227_433,(0,0,5):C.UVGC_227_434,(0,0,6):C.UVGC_227_435,(0,1,3):C.UVGC_206_340})

V_309 = CTVertex(name = 'V_309',
                 type = 'UV',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS6 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0] ], [ [P.G0, P.Z] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_298_860,(0,0,1):C.UVGC_298_861,(0,0,2):C.UVGC_298_862,(0,0,3):C.UVGC_298_863,(0,0,4):C.UVGC_298_864,(0,0,6):C.UVGC_298_865,(0,0,7):C.UVGC_298_866,(0,0,8):C.UVGC_298_867,(0,0,10):C.UVGC_298_868,(0,0,11):C.UVGC_298_869,(0,0,12):C.UVGC_298_870,(0,0,13):C.UVGC_298_871,(0,0,14):C.UVGC_298_872,(0,0,15):C.UVGC_298_873,(0,0,16):C.UVGC_298_874,(0,0,17):C.UVGC_298_875,(0,0,5):C.UVGC_298_876,(0,0,9):C.UVGC_298_877,(0,1,0):C.UVGC_297_842,(0,1,1):C.UVGC_297_843,(0,1,2):C.UVGC_297_844,(0,1,3):C.UVGC_297_845,(0,1,4):C.UVGC_297_846,(0,1,6):C.UVGC_297_847,(0,1,7):C.UVGC_297_848,(0,1,8):C.UVGC_297_849,(0,1,10):C.UVGC_297_850,(0,1,11):C.UVGC_297_851,(0,1,12):C.UVGC_297_852,(0,1,13):C.UVGC_297_853,(0,1,14):C.UVGC_297_854,(0,1,15):C.UVGC_297_855,(0,1,16):C.UVGC_297_856,(0,1,17):C.UVGC_297_857,(0,1,5):C.UVGC_297_858,(0,1,9):C.UVGC_297_859})

V_310 = CTVertex(name = 'V_310',
                 type = 'UV',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS6 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0] ], [ [P.G0, P.H] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_302_923,(0,0,1):C.UVGC_302_924,(0,0,2):C.UVGC_302_925,(0,0,3):C.UVGC_302_926,(0,0,4):C.UVGC_302_927,(0,0,6):C.UVGC_302_928,(0,0,7):C.UVGC_302_929,(0,0,8):C.UVGC_302_930,(0,0,10):C.UVGC_302_931,(0,0,12):C.UVGC_302_932,(0,0,13):C.UVGC_302_933,(0,0,14):C.UVGC_302_934,(0,0,15):C.UVGC_302_935,(0,0,16):C.UVGC_302_936,(0,0,17):C.UVGC_302_937,(0,0,18):C.UVGC_302_938,(0,0,5):C.UVGC_302_939,(0,0,9):C.UVGC_302_940,(0,0,11):C.UVGC_302_941,(0,1,0):C.UVGC_301_910,(0,1,1):C.UVGC_301_911,(0,1,2):C.UVGC_301_912,(0,1,3):C.UVGC_301_913,(0,1,6):C.UVGC_301_914,(0,1,12):C.UVGC_301_915,(0,1,13):C.UVGC_301_916,(0,1,14):C.UVGC_301_917,(0,1,15):C.UVGC_301_918,(0,1,16):C.UVGC_301_919,(0,1,5):C.UVGC_301_920,(0,1,9):C.UVGC_301_921,(0,1,11):C.UVGC_301_922})

V_311 = CTVertex(name = 'V_311',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS5 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b] ], [ [P.b, P.t] ], [ [P.c] ], [ [P.c, P.s] ], [ [P.d] ], [ [P.d, P.u] ], [ [P.e__minus__] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.W__plus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.ta__minus__, P.vt] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,2):C.UVGC_314_1128,(0,0,4):C.UVGC_314_1129,(0,0,6):C.UVGC_314_1130,(0,0,8):C.UVGC_314_1131,(0,0,10):C.UVGC_314_1132,(0,0,12):C.UVGC_314_1133,(0,0,14):C.UVGC_302_929,(0,0,15):C.UVGC_314_1134,(0,0,18):C.UVGC_302_931,(0,0,20):C.UVGC_314_1135,(0,0,22):C.UVGC_314_1136,(0,0,23):C.UVGC_314_1137,(0,0,24):C.UVGC_314_1138,(0,0,26):C.UVGC_314_1139,(0,0,27):C.UVGC_302_937,(0,0,29):C.UVGC_314_1140,(0,0,0):C.UVGC_314_1141,(0,0,1):C.UVGC_314_1142,(0,0,3):C.UVGC_314_1143,(0,0,5):C.UVGC_314_1144,(0,0,7):C.UVGC_314_1145,(0,0,9):C.UVGC_314_1146,(0,0,11):C.UVGC_314_1147,(0,0,13):C.UVGC_314_1148,(0,0,16):C.UVGC_302_939,(0,0,17):C.UVGC_314_1149,(0,0,19):C.UVGC_314_1150,(0,0,21):C.UVGC_314_1151,(0,0,25):C.UVGC_314_1152,(0,0,28):C.UVGC_314_1153,(0,1,1):C.UVGC_304_960,(0,1,3):C.UVGC_304_961,(0,1,5):C.UVGC_304_962,(0,1,7):C.UVGC_304_963,(0,1,9):C.UVGC_304_964,(0,1,11):C.UVGC_304_965,(0,1,13):C.UVGC_304_966,(0,1,16):C.UVGC_304_967,(0,1,17):C.UVGC_304_968,(0,1,19):C.UVGC_304_969,(0,1,21):C.UVGC_304_970,(0,1,25):C.UVGC_304_971,(0,1,28):C.UVGC_304_972})

V_312 = CTVertex(name = 'V_312',
                 type = 'UV',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,0):C.UVGC_265_631,(0,1,1):C.UVGC_265_632,(0,1,2):C.UVGC_265_633,(0,1,3):C.UVGC_265_634,(0,1,4):C.UVGC_265_635,(0,1,5):C.UVGC_265_636,(0,1,7):C.UVGC_265_637,(0,1,8):C.UVGC_265_638,(0,1,9):C.UVGC_265_639,(0,1,10):C.UVGC_265_640,(0,1,11):C.UVGC_265_641,(0,1,12):C.UVGC_265_642,(0,1,6):C.UVGC_265_643,(0,2,4):C.UVGC_291_825,(0,2,12):C.UVGC_291_826,(0,2,6):C.UVGC_291_827,(0,0,0):C.UVGC_264_618,(0,0,1):C.UVGC_264_619,(0,0,2):C.UVGC_264_620,(0,0,3):C.UVGC_264_621,(0,0,4):C.UVGC_264_622,(0,0,5):C.UVGC_264_623,(0,0,7):C.UVGC_264_624,(0,0,8):C.UVGC_264_625,(0,0,9):C.UVGC_264_626,(0,0,10):C.UVGC_264_627,(0,0,11):C.UVGC_264_628,(0,0,12):C.UVGC_264_629,(0,0,6):C.UVGC_264_630})

V_313 = CTVertex(name = 'V_313',
                 type = 'UV',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,0):C.UVGC_263_605,(0,1,1):C.UVGC_263_606,(0,1,2):C.UVGC_263_607,(0,1,3):C.UVGC_263_608,(0,1,4):C.UVGC_263_609,(0,1,5):C.UVGC_263_610,(0,1,7):C.UVGC_263_611,(0,1,8):C.UVGC_263_612,(0,1,9):C.UVGC_263_613,(0,1,10):C.UVGC_263_614,(0,1,11):C.UVGC_263_615,(0,1,12):C.UVGC_263_616,(0,1,6):C.UVGC_263_617,(0,2,4):C.UVGC_290_822,(0,2,12):C.UVGC_290_823,(0,2,6):C.UVGC_290_824,(0,0,0):C.UVGC_262_592,(0,0,1):C.UVGC_262_593,(0,0,2):C.UVGC_262_594,(0,0,3):C.UVGC_262_595,(0,0,4):C.UVGC_262_596,(0,0,5):C.UVGC_262_597,(0,0,7):C.UVGC_262_598,(0,0,8):C.UVGC_262_599,(0,0,9):C.UVGC_262_600,(0,0,10):C.UVGC_262_601,(0,0,11):C.UVGC_262_602,(0,0,12):C.UVGC_262_603,(0,0,6):C.UVGC_262_604})

V_314 = CTVertex(name = 'V_314',
                 type = 'UV',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV10, L.VV7, L.VV8 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0] ], [ [P.G0, P.H] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,1,0):C.UVGC_300_894,(0,1,1):C.UVGC_300_895,(0,1,2):C.UVGC_300_896,(0,1,3):C.UVGC_300_897,(0,1,6):C.UVGC_300_898,(0,1,7):C.UVGC_300_899,(0,1,11):C.UVGC_300_900,(0,1,12):C.UVGC_300_901,(0,1,13):C.UVGC_300_902,(0,1,14):C.UVGC_300_903,(0,1,15):C.UVGC_300_904,(0,1,16):C.UVGC_300_905,(0,1,17):C.UVGC_300_906,(0,1,5):C.UVGC_300_907,(0,1,8):C.UVGC_300_908,(0,1,10):C.UVGC_300_909,(0,2,0):C.UVGC_303_942,(0,2,1):C.UVGC_303_943,(0,2,2):C.UVGC_303_944,(0,2,3):C.UVGC_303_945,(0,2,4):C.UVGC_303_946,(0,2,6):C.UVGC_303_947,(0,2,7):C.UVGC_303_948,(0,2,9):C.UVGC_303_949,(0,2,11):C.UVGC_303_950,(0,2,12):C.UVGC_303_951,(0,2,13):C.UVGC_303_952,(0,2,14):C.UVGC_303_953,(0,2,15):C.UVGC_303_954,(0,2,16):C.UVGC_303_955,(0,2,17):C.UVGC_303_956,(0,2,5):C.UVGC_303_957,(0,2,8):C.UVGC_303_958,(0,2,10):C.UVGC_303_959,(0,0,0):C.UVGC_299_878,(0,0,1):C.UVGC_299_879,(0,0,2):C.UVGC_299_880,(0,0,3):C.UVGC_299_881,(0,0,6):C.UVGC_299_882,(0,0,7):C.UVGC_299_883,(0,0,11):C.UVGC_299_884,(0,0,12):C.UVGC_299_885,(0,0,13):C.UVGC_299_886,(0,0,14):C.UVGC_299_887,(0,0,15):C.UVGC_299_888,(0,0,16):C.UVGC_299_889,(0,0,17):C.UVGC_299_890,(0,0,5):C.UVGC_299_891,(0,0,8):C.UVGC_299_892,(0,0,10):C.UVGC_299_893})

V_315 = CTVertex(name = 'V_315',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV6, L.VV8, L.VV9 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0] ], [ [P.G0, P.G__plus__] ], [ [P.ghA, P.ghWm], [P.ghA, P.ghWp] ], [ [P.ghWm, P.ghZ], [P.ghWp, P.ghZ] ], [ [P.G__plus__] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.Z] ], [ [P.H] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_313_1113,(0,0,1):C.UVGC_313_1114,(0,0,2):C.UVGC_313_1115,(0,0,3):C.UVGC_313_1116,(0,0,4):C.UVGC_313_1117,(0,0,5):C.UVGC_313_1118,(0,0,7):C.UVGC_313_1119,(0,0,8):C.UVGC_313_1120,(0,0,9):C.UVGC_313_1121,(0,0,11):C.UVGC_313_1122,(0,0,12):C.UVGC_313_1123,(0,0,14):C.UVGC_313_1124,(0,0,15):C.UVGC_313_1125,(0,0,16):C.UVGC_313_1126,(0,0,18):C.UVGC_313_1127,(0,1,6):C.UVGC_315_1154,(0,1,10):C.UVGC_315_1155,(0,1,13):C.UVGC_315_1156,(0,1,17):C.UVGC_315_1157,(0,1,19):C.UVGC_315_1158,(0,1,0):C.UVGC_315_1159,(0,1,1):C.UVGC_315_1160,(0,1,2):C.UVGC_315_1161,(0,1,3):C.UVGC_315_1162,(0,1,4):C.UVGC_315_1163,(0,1,5):C.UVGC_315_1164,(0,1,7):C.UVGC_315_1165,(0,1,8):C.UVGC_315_1166,(0,1,9):C.UVGC_315_1167,(0,1,11):C.UVGC_315_1168,(0,1,12):C.UVGC_315_1169,(0,1,14):C.UVGC_315_1170,(0,1,15):C.UVGC_315_1171,(0,1,16):C.UVGC_315_1172,(0,1,18):C.UVGC_315_1173,(0,2,0):C.UVGC_312_1098,(0,2,1):C.UVGC_312_1099,(0,2,2):C.UVGC_312_1100,(0,2,3):C.UVGC_312_1101,(0,2,4):C.UVGC_312_1102,(0,2,5):C.UVGC_312_1103,(0,2,7):C.UVGC_312_1104,(0,2,8):C.UVGC_312_1105,(0,2,9):C.UVGC_312_1106,(0,2,11):C.UVGC_312_1107,(0,2,12):C.UVGC_312_1108,(0,2,14):C.UVGC_312_1109,(0,2,15):C.UVGC_312_1110,(0,2,16):C.UVGC_312_1111,(0,2,18):C.UVGC_312_1112})

V_316 = CTVertex(name = 'V_316',
                 type = 'UV',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV10, L.VV7 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.ghG] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,1,0):C.UVGC_167_58,(0,1,1):C.UVGC_167_59,(0,1,2):C.UVGC_167_60,(0,1,3):C.UVGC_167_61,(0,1,4):C.UVGC_167_62,(0,1,5):C.UVGC_167_63,(0,1,6):C.UVGC_167_64,(0,1,7):C.UVGC_167_65,(0,0,0):C.UVGC_168_66,(0,0,1):C.UVGC_168_67,(0,0,2):C.UVGC_168_68,(0,0,5):C.UVGC_168_69,(0,0,6):C.UVGC_168_70,(0,0,7):C.UVGC_168_71})

V_317 = CTVertex(name = 'V_317',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_276_756,(0,0,3):C.UVGC_276_757,(0,0,0):C.UVGC_276_758,(0,0,2):C.UVGC_276_759})

V_318 = CTVertex(name = 'V_318',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_276_756,(0,0,3):C.UVGC_276_757,(0,0,1):C.UVGC_276_759,(0,0,2):C.UVGC_276_758})

V_319 = CTVertex(name = 'V_319',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV5 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_276_756,(0,0,3):C.UVGC_276_757,(0,0,1):C.UVGC_276_759,(0,0,2):C.UVGC_276_758})

V_320 = CTVertex(name = 'V_320',
                 type = 'UV',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_293_831,(0,0,2):C.UVGC_293_832,(0,0,1):C.UVGC_293_833})

V_321 = CTVertex(name = 'V_321',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_292_828,(0,0,2):C.UVGC_292_829,(0,0,1):C.UVGC_292_830})

V_322 = CTVertex(name = 'V_322',
                 type = 'UV',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS7 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_294_834,(0,0,2):C.UVGC_294_835,(0,0,1):C.UVGC_294_836})

V_323 = CTVertex(name = 'V_323',
                 type = 'UV',
                 particles = [ P.a, P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV12 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_201_316,(0,0,1):C.UVGC_201_317})

V_324 = CTVertex(name = 'V_324',
                 type = 'UV',
                 particles = [ P.a, P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV12 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_202_318,(0,0,1):C.UVGC_202_319})

V_325 = CTVertex(name = 'V_325',
                 type = 'UV',
                 particles = [ P.a, P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV12 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_203_320,(0,0,1):C.UVGC_203_321})

V_326 = CTVertex(name = 'V_326',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV12 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_204_322,(0,0,1):C.UVGC_204_323})

V_327 = CTVertex(name = 'V_327',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV12 ],
                 loop_particles = [ [ [P.G0], [P.H] ], [ [P.G0, P.H] ], [ [P.ghWm], [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_212_359,(0,0,2):C.UVGC_212_360,(0,0,3):C.UVGC_212_361,(0,0,1):C.UVGC_212_362})

V_328 = CTVertex(name = 'V_328',
                 type = 'UV',
                 particles = [ P.a, P.a, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_296_840,(0,0,0):C.UVGC_296_841})

V_329 = CTVertex(name = 'V_329',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_295_837,(0,0,2):C.UVGC_295_838,(0,0,1):C.UVGC_295_839})

V_330 = CTVertex(name = 'V_330',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,1):C.UVGC_296_840,(0,0,0):C.UVGC_296_841})

V_331 = CTVertex(name = 'V_331',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.ghWm], [P.ghWp] ], [ [P.G__plus__, P.W__plus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.UVGC_295_837,(0,0,2):C.UVGC_295_838,(0,0,1):C.UVGC_295_839})

V_332 = CTVertex(name = 'V_332',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G0] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_429_4672,(0,0,2):C.UVGC_429_4673,(0,0,4):C.UVGC_429_4674,(0,0,7):C.UVGC_429_4675,(0,0,9):C.UVGC_429_4676,(0,0,10):C.UVGC_429_4677,(0,0,13):C.UVGC_420_4416,(0,0,15):C.UVGC_429_4678,(0,0,1):C.UVGC_429_4679,(0,0,3):C.UVGC_429_4680,(0,0,5):C.UVGC_429_4681,(0,0,6):C.UVGC_420_4415,(0,0,8):C.UVGC_429_4682,(0,0,11):C.UVGC_429_4683,(0,0,12):C.UVGC_429_4684,(0,0,14):C.UVGC_429_4685})

V_333 = CTVertex(name = 'V_333',
                 type = 'UV',
                 particles = [ P.W__plus__, P.W__plus__, P.G__minus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.a, P.G0] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ] ],
                 couplings = {(0,0,0):C.UVGC_429_4672,(0,0,2):C.UVGC_429_4673,(0,0,4):C.UVGC_429_4674,(0,0,7):C.UVGC_429_4675,(0,0,9):C.UVGC_429_4676,(0,0,10):C.UVGC_429_4677,(0,0,13):C.UVGC_420_4416,(0,0,15):C.UVGC_429_4678,(0,0,1):C.UVGC_429_4679,(0,0,3):C.UVGC_429_4680,(0,0,5):C.UVGC_429_4681,(0,0,6):C.UVGC_420_4415,(0,0,8):C.UVGC_429_4682,(0,0,11):C.UVGC_429_4683,(0,0,12):C.UVGC_429_4684,(0,0,14):C.UVGC_429_4685})

V_334 = CTVertex(name = 'V_334',
                 type = 'UV',
                 particles = [ P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS4, L.SS5 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_163_50,(0,0,1):C.UVGC_163_51,(0,1,0):C.UVGC_150_24,(0,1,1):C.UVGC_150_25})

V_335 = CTVertex(name = 'V_335',
                 type = 'UV',
                 particles = [ P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVV22, L.VVV28, L.VVV29 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_128_1,(0,0,2):C.UVGC_136_5,(0,1,1):C.UVGC_128_1})

V_336 = CTVertex(name = 'V_336',
                 type = 'UV',
                 particles = [ P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV22, L.VVV28, L.VVV29 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_129_2,(0,0,2):C.UVGC_137_6,(0,1,1):C.UVGC_129_2})

V_337 = CTVertex(name = 'V_337',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV22, L.VVV27, L.VVV29 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_130_3,(0,0,2):C.UVGC_138_7,(0,1,1):C.UVGC_130_3})

V_338 = CTVertex(name = 'V_338',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV22, L.VVV28, L.VVV29 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,0):C.UVGC_131_4,(0,0,2):C.UVGC_139_8,(0,1,1):C.UVGC_131_4})

V_339 = CTVertex(name = 'V_339',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_166_56,(0,0,1):C.UVGC_166_57})

V_340 = CTVertex(name = 'V_340',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_165_54,(0,0,1):C.UVGC_165_55})

V_341 = CTVertex(name = 'V_341',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_164_52,(0,0,1):C.UVGC_164_53})

V_342 = CTVertex(name = 'V_342',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVS2 ],
                 loop_particles = [ [ [P.ghA, P.ghWm] ], [ [P.ghA, P.ghWp] ], [ [P.ghWm, P.ghZ] ], [ [P.ghWp, P.ghZ] ] ],
                 couplings = {(0,0,0):C.UVGC_211_355,(0,0,1):C.UVGC_211_356,(0,0,2):C.UVGC_211_357,(0,0,3):C.UVGC_211_358})

V_343 = CTVertex(name = 'V_343',
                 type = 'UV',
                 particles = [ P.G0, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_160_44,(0,0,1):C.UVGC_160_45})

V_344 = CTVertex(name = 'V_344',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_161_46,(0,0,1):C.UVGC_161_47})

V_345 = CTVertex(name = 'V_345',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS2 ],
                 loop_particles = [ [ [P.ghWm] ], [ [P.ghWp] ] ],
                 couplings = {(0,0,0):C.UVGC_162_48,(0,0,1):C.UVGC_162_49})

