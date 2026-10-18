# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sat 17 Oct 2026 23:24:25


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_495_1166,(0,0,1):C.R2GC_495_1167,(0,0,2):C.R2GC_495_1168,(0,0,3):C.R2GC_495_1169,(0,0,7):C.R2GC_495_1170,(0,0,8):C.R2GC_495_1171,(0,0,9):C.R2GC_495_1172,(0,0,10):C.R2GC_495_1173,(0,0,11):C.R2GC_495_1174,(0,0,12):C.R2GC_495_1175,(0,0,13):C.R2GC_495_1176,(0,0,5):C.R2GC_495_1177,(0,0,6):C.R2GC_495_1178,(0,0,4):C.R2GC_495_1179})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,21):C.R2GC_495_1175,(0,0,23):C.R2GC_496_1180,(0,0,0):C.R2GC_496_1181,(0,0,2):C.R2GC_182_76,(0,0,3):C.R2GC_496_1182,(0,0,4):C.R2GC_496_1183,(0,0,5):C.R2GC_496_1184,(0,0,6):C.R2GC_496_1185,(0,0,7):C.R2GC_496_1186,(0,0,8):C.R2GC_496_1187,(0,0,9):C.R2GC_496_1188,(0,0,10):C.R2GC_495_1169,(0,0,11):C.R2GC_496_1189,(0,0,15):C.R2GC_496_1190,(0,0,16):C.R2GC_496_1191,(0,0,17):C.R2GC_495_1170,(0,0,18):C.R2GC_496_1192,(0,0,19):C.R2GC_496_1193,(0,0,20):C.R2GC_495_1173,(0,0,22):C.R2GC_496_1194,(0,0,1):C.R2GC_496_1195,(0,0,12):C.R2GC_496_1196,(0,0,13):C.R2GC_496_1197,(0,0,14):C.R2GC_496_1198})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_497_1199,(0,0,1):C.R2GC_497_1200,(0,0,2):C.R2GC_497_1201,(0,0,3):C.R2GC_497_1202,(0,0,6):C.R2GC_497_1203,(0,0,7):C.R2GC_497_1204,(0,0,8):C.R2GC_497_1205,(0,0,9):C.R2GC_497_1206,(0,0,10):C.R2GC_497_1207,(0,0,11):C.R2GC_497_1208,(0,0,12):C.R2GC_497_1209,(0,0,4):C.R2GC_497_1210,(0,0,5):C.R2GC_497_1211})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.a, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS2 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
               couplings = {(0,0,0):C.R2GC_240_295,(0,0,1):C.R2GC_240_296,(0,0,2):C.R2GC_240_297,(0,0,3):C.R2GC_240_298,(0,0,4):C.R2GC_240_299,(0,0,5):C.R2GC_240_300,(0,0,6):C.R2GC_240_301,(0,0,7):C.R2GC_240_302,(0,0,8):C.R2GC_240_303,(0,0,9):C.R2GC_240_304,(0,0,10):C.R2GC_240_305,(0,0,11):C.R2GC_240_306,(0,0,12):C.R2GC_240_307,(0,0,13):C.R2GC_240_308,(0,0,14):C.R2GC_240_309})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV1 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_321_545,(0,0,1):C.R2GC_321_546})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.a, P.W__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVS1 ],
               loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
               couplings = {(0,0,1):C.R2GC_500_1245,(0,0,2):C.R2GC_500_1246,(0,0,3):C.R2GC_500_1247,(0,0,4):C.R2GC_500_1248,(0,0,5):C.R2GC_500_1249,(0,0,6):C.R2GC_500_1250,(0,0,7):C.R2GC_500_1251,(0,0,8):C.R2GC_500_1252,(0,0,10):C.R2GC_500_1253,(0,0,11):C.R2GC_500_1254,(0,0,12):C.R2GC_500_1255,(0,0,13):C.R2GC_500_1256,(0,0,0):C.R2GC_500_1257,(0,0,9):C.R2GC_500_1258})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.W__minus__, P.G0, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VSS2 ],
               loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
               couplings = {(0,0,1):C.R2GC_402_710,(0,0,2):C.R2GC_402_711,(0,0,3):C.R2GC_402_712,(0,0,4):C.R2GC_402_713,(0,0,5):C.R2GC_402_714,(0,0,6):C.R2GC_402_715,(0,0,7):C.R2GC_402_716,(0,0,8):C.R2GC_402_717,(0,0,14):C.R2GC_402_718,(0,0,15):C.R2GC_402_719,(0,0,16):C.R2GC_402_720,(0,0,17):C.R2GC_402_721,(0,0,0):C.R2GC_402_722,(0,0,9):C.R2GC_402_723,(0,0,10):C.R2GC_402_724,(0,0,11):C.R2GC_402_725,(0,0,12):C.R2GC_402_726,(0,0,13):C.R2GC_402_727})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.W__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.VSS2 ],
               loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
               couplings = {(0,0,1):C.R2GC_404_744,(0,0,2):C.R2GC_404_745,(0,0,3):C.R2GC_404_746,(0,0,4):C.R2GC_404_747,(0,0,5):C.R2GC_404_748,(0,0,6):C.R2GC_404_749,(0,0,7):C.R2GC_404_750,(0,0,8):C.R2GC_404_751,(0,0,14):C.R2GC_404_752,(0,0,15):C.R2GC_404_753,(0,0,16):C.R2GC_404_754,(0,0,17):C.R2GC_404_755,(0,0,0):C.R2GC_404_756,(0,0,9):C.R2GC_404_757,(0,0,10):C.R2GC_404_758,(0,0,11):C.R2GC_404_759,(0,0,12):C.R2GC_404_760,(0,0,13):C.R2GC_404_761})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.a, P.W__minus__, P.W__plus__ ],
               color = [ '1' ],
               lorentz = [ L.VVV1 ],
               loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_319_533,(0,0,1):C.R2GC_319_534,(0,0,2):C.R2GC_319_535,(0,0,3):C.R2GC_319_536,(0,0,4):C.R2GC_319_537,(0,0,5):C.R2GC_319_538,(0,0,6):C.R2GC_319_539,(0,0,7):C.R2GC_319_540,(0,0,8):C.R2GC_319_541,(0,0,9):C.R2GC_319_542,(0,0,10):C.R2GC_319_543,(0,0,11):C.R2GC_319_544})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_500_1256,(0,0,2):C.R2GC_501_1259,(0,0,3):C.R2GC_501_1260,(0,0,4):C.R2GC_501_1261,(0,0,5):C.R2GC_501_1262,(0,0,6):C.R2GC_501_1263,(0,0,7):C.R2GC_501_1264,(0,0,8):C.R2GC_501_1265,(0,0,10):C.R2GC_501_1266,(0,0,11):C.R2GC_501_1267,(0,0,12):C.R2GC_501_1268,(0,0,13):C.R2GC_500_1245,(0,0,0):C.R2GC_501_1269,(0,0,9):C.R2GC_501_1270})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_403_728,(0,0,2):C.R2GC_403_729,(0,0,3):C.R2GC_403_730,(0,0,4):C.R2GC_403_731,(0,0,5):C.R2GC_403_732,(0,0,6):C.R2GC_403_733,(0,0,7):C.R2GC_403_734,(0,0,8):C.R2GC_403_735,(0,0,14):C.R2GC_403_736,(0,0,15):C.R2GC_403_737,(0,0,16):C.R2GC_403_738,(0,0,17):C.R2GC_403_739,(0,0,0):C.R2GC_403_740,(0,0,9):C.R2GC_402_724,(0,0,10):C.R2GC_402_723,(0,0,11):C.R2GC_403_741,(0,0,12):C.R2GC_403_742,(0,0,13):C.R2GC_403_743})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_404_744,(0,0,2):C.R2GC_404_745,(0,0,3):C.R2GC_404_746,(0,0,4):C.R2GC_405_762,(0,0,5):C.R2GC_404_748,(0,0,6):C.R2GC_405_763,(0,0,7):C.R2GC_404_750,(0,0,8):C.R2GC_404_751,(0,0,14):C.R2GC_404_752,(0,0,15):C.R2GC_405_764,(0,0,16):C.R2GC_404_754,(0,0,17):C.R2GC_404_755,(0,0,0):C.R2GC_404_756,(0,0,9):C.R2GC_404_757,(0,0,10):C.R2GC_404_758,(0,0,11):C.R2GC_404_759,(0,0,12):C.R2GC_404_760,(0,0,13):C.R2GC_404_761})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,15):C.R2GC_499_1228,(0,0,17):C.R2GC_499_1229,(0,0,1):C.R2GC_499_1230,(0,0,2):C.R2GC_499_1231,(0,0,3):C.R2GC_499_1232,(0,0,4):C.R2GC_499_1233,(0,0,5):C.R2GC_499_1234,(0,0,6):C.R2GC_499_1235,(0,0,7):C.R2GC_499_1236,(0,0,8):C.R2GC_499_1237,(0,0,9):C.R2GC_499_1238,(0,0,11):C.R2GC_499_1239,(0,0,12):C.R2GC_499_1240,(0,0,13):C.R2GC_499_1241,(0,0,14):C.R2GC_499_1242,(0,0,16):C.R2GC_499_1243,(0,0,0):C.R2GC_499_1244,(0,0,10):C.R2GC_496_1195})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVV1 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_423_832,(0,0,1):C.R2GC_423_833,(0,0,2):C.R2GC_423_834,(0,0,3):C.R2GC_423_835,(0,0,4):C.R2GC_423_836,(0,0,5):C.R2GC_423_837,(0,0,6):C.R2GC_423_838,(0,0,7):C.R2GC_423_839,(0,0,8):C.R2GC_423_840,(0,0,9):C.R2GC_423_841,(0,0,10):C.R2GC_423_842,(0,0,11):C.R2GC_423_843})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_601_1893,(0,0,1):C.R2GC_601_1894,(0,0,2):C.R2GC_601_1895,(0,0,6):C.R2GC_601_1896,(0,0,3):C.R2GC_601_1897,(0,0,4):C.R2GC_601_1898,(0,0,5):C.R2GC_601_1899,(0,0,7):C.R2GC_601_1900,(0,0,9):C.R2GC_601_1901,(0,1,0):C.R2GC_603_1911,(0,1,1):C.R2GC_603_1912,(0,1,2):C.R2GC_603_1913,(0,1,6):C.R2GC_603_1914,(0,1,3):C.R2GC_603_1915,(0,1,5):C.R2GC_603_1916,(0,1,7):C.R2GC_603_1917,(0,1,8):C.R2GC_603_1918,(0,1,9):C.R2GC_603_1919})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.c__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.d, P.G__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0], [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_600_1884,(0,0,1):C.R2GC_600_1885,(0,0,2):C.R2GC_600_1886,(0,0,3):C.R2GC_600_1887,(0,0,4):C.R2GC_600_1888,(0,0,5):C.R2GC_600_1889,(0,0,7):C.R2GC_600_1890,(0,0,8):C.R2GC_600_1891,(0,0,9):C.R2GC_600_1892,(0,1,0):C.R2GC_602_1902,(0,1,1):C.R2GC_602_1903,(0,1,2):C.R2GC_602_1904,(0,1,3):C.R2GC_602_1905,(0,1,4):C.R2GC_602_1906,(0,1,5):C.R2GC_602_1907,(0,1,6):C.R2GC_602_1908,(0,1,7):C.R2GC_602_1909,(0,1,9):C.R2GC_602_1910})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.t__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.d, P.G0, P.t], [P.d, P.H, P.t] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_615_2005,(0,0,1):C.R2GC_615_2006,(0,0,2):C.R2GC_615_2007,(0,0,6):C.R2GC_615_2008,(0,0,3):C.R2GC_615_2009,(0,0,4):C.R2GC_615_2010,(0,0,5):C.R2GC_615_2011,(0,0,7):C.R2GC_615_2012,(0,0,9):C.R2GC_615_2013,(0,1,0):C.R2GC_620_2050,(0,1,1):C.R2GC_620_2051,(0,1,2):C.R2GC_620_2052,(0,1,6):C.R2GC_620_2053,(0,1,3):C.R2GC_620_2054,(0,1,5):C.R2GC_620_2055,(0,1,7):C.R2GC_620_2056,(0,1,8):C.R2GC_620_2057,(0,1,9):C.R2GC_620_2058})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.u__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.s, P.u] ], [ [P.G0, P.s, P.u], [P.H, P.s, P.u] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.g, P.s, P.u] ], [ [P.s, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_607_1943,(0,0,1):C.R2GC_607_1944,(0,0,2):C.R2GC_607_1945,(0,0,8):C.R2GC_607_1946,(0,0,3):C.R2GC_607_1947,(0,0,4):C.R2GC_607_1948,(0,0,6):C.R2GC_607_1949,(0,0,7):C.R2GC_607_1950,(0,0,9):C.R2GC_607_1951,(0,1,0):C.R2GC_609_1961,(0,1,1):C.R2GC_609_1962,(0,1,2):C.R2GC_609_1963,(0,1,8):C.R2GC_609_1964,(0,1,3):C.R2GC_609_1965,(0,1,5):C.R2GC_609_1966,(0,1,6):C.R2GC_609_1967,(0,1,7):C.R2GC_609_1968,(0,1,9):C.R2GC_609_1969})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_606_1934,(0,0,1):C.R2GC_606_1935,(0,0,2):C.R2GC_606_1936,(0,0,6):C.R2GC_606_1937,(0,0,3):C.R2GC_606_1938,(0,0,5):C.R2GC_606_1939,(0,0,7):C.R2GC_606_1940,(0,0,8):C.R2GC_606_1941,(0,0,9):C.R2GC_606_1942,(0,1,0):C.R2GC_608_1952,(0,1,1):C.R2GC_608_1953,(0,1,2):C.R2GC_608_1954,(0,1,6):C.R2GC_608_1955,(0,1,3):C.R2GC_608_1956,(0,1,4):C.R2GC_608_1957,(0,1,5):C.R2GC_608_1958,(0,1,7):C.R2GC_608_1959,(0,1,9):C.R2GC_608_1960})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.t__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.s, P.t] ], [ [P.G0, P.s, P.t], [P.H, P.s, P.t] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.g, P.s, P.t] ], [ [P.s, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_616_2014,(0,0,1):C.R2GC_616_2015,(0,0,2):C.R2GC_616_2016,(0,0,8):C.R2GC_616_2017,(0,0,3):C.R2GC_616_2018,(0,0,4):C.R2GC_616_2019,(0,0,6):C.R2GC_616_2020,(0,0,7):C.R2GC_616_2021,(0,0,9):C.R2GC_616_2022,(0,1,0):C.R2GC_621_2059,(0,1,1):C.R2GC_621_2060,(0,1,2):C.R2GC_621_2061,(0,1,8):C.R2GC_621_2062,(0,1,3):C.R2GC_621_2063,(0,1,5):C.R2GC_621_2064,(0,1,6):C.R2GC_621_2065,(0,1,7):C.R2GC_621_2066,(0,1,9):C.R2GC_621_2067})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.u__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.b, P.G0, P.u], [P.b, P.H, P.u] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_618_2032,(0,0,1):C.R2GC_618_2033,(0,0,2):C.R2GC_618_2034,(0,0,6):C.R2GC_618_2035,(0,0,3):C.R2GC_618_2036,(0,0,4):C.R2GC_618_2037,(0,0,5):C.R2GC_618_2038,(0,0,7):C.R2GC_618_2039,(0,0,9):C.R2GC_618_2040,(0,1,0):C.R2GC_623_2077,(0,1,1):C.R2GC_623_2078,(0,1,2):C.R2GC_623_2079,(0,1,6):C.R2GC_623_2080,(0,1,3):C.R2GC_623_2081,(0,1,5):C.R2GC_623_2082,(0,1,7):C.R2GC_623_2083,(0,1,8):C.R2GC_623_2084,(0,1,9):C.R2GC_623_2085})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.c__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.c, P.G__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0], [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_617_2023,(0,0,1):C.R2GC_617_2024,(0,0,2):C.R2GC_617_2025,(0,0,3):C.R2GC_617_2026,(0,0,4):C.R2GC_617_2027,(0,0,5):C.R2GC_617_2028,(0,0,6):C.R2GC_617_2029,(0,0,7):C.R2GC_617_2030,(0,0,9):C.R2GC_617_2031,(0,1,0):C.R2GC_622_2068,(0,1,1):C.R2GC_622_2069,(0,1,2):C.R2GC_622_2070,(0,1,3):C.R2GC_622_2071,(0,1,4):C.R2GC_622_2072,(0,1,5):C.R2GC_622_2073,(0,1,7):C.R2GC_622_2074,(0,1,8):C.R2GC_622_2075,(0,1,9):C.R2GC_622_2076})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_619_2041,(0,0,1):C.R2GC_619_2042,(0,0,2):C.R2GC_619_2043,(0,0,6):C.R2GC_619_2044,(0,0,3):C.R2GC_619_2045,(0,0,4):C.R2GC_619_2046,(0,0,5):C.R2GC_619_2047,(0,0,7):C.R2GC_619_2048,(0,0,9):C.R2GC_619_2049,(0,1,0):C.R2GC_624_2086,(0,1,1):C.R2GC_624_2087,(0,1,2):C.R2GC_624_2088,(0,1,6):C.R2GC_624_2089,(0,1,3):C.R2GC_624_2090,(0,1,5):C.R2GC_624_2091,(0,1,7):C.R2GC_624_2092,(0,1,8):C.R2GC_624_2093,(0,1,9):C.R2GC_624_2094})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_211_214,(0,0,1):C.R2GC_211_215,(0,0,3):C.R2GC_211_216,(0,0,4):C.R2GC_210_206,(0,0,5):C.R2GC_210_205,(0,0,7):C.R2GC_211_217,(0,0,8):C.R2GC_211_218,(0,0,10):C.R2GC_211_219,(0,0,2):C.R2GC_211_220,(0,0,6):C.R2GC_211_221,(0,0,9):C.R2GC_211_222,(0,0,11):C.R2GC_211_223,(0,1,0):C.R2GC_210_202,(0,1,1):C.R2GC_210_203,(0,1,3):C.R2GC_210_204,(0,1,4):C.R2GC_210_205,(0,1,5):C.R2GC_210_206,(0,1,7):C.R2GC_210_207,(0,1,8):C.R2GC_210_208,(0,1,10):C.R2GC_210_209,(0,1,2):C.R2GC_210_210,(0,1,6):C.R2GC_210_211,(0,1,9):C.R2GC_210_212,(0,1,11):C.R2GC_210_213})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_213_236,(0,0,1):C.R2GC_213_237,(0,0,8):C.R2GC_213_238,(0,0,3):C.R2GC_212_230,(0,0,4):C.R2GC_213_239,(0,0,6):C.R2GC_213_240,(0,0,9):C.R2GC_212_227,(0,0,11):C.R2GC_213_241,(0,0,2):C.R2GC_213_242,(0,0,5):C.R2GC_213_243,(0,0,7):C.R2GC_213_244,(0,0,10):C.R2GC_213_245,(0,1,0):C.R2GC_212_224,(0,1,1):C.R2GC_212_225,(0,1,8):C.R2GC_212_226,(0,1,3):C.R2GC_212_227,(0,1,4):C.R2GC_212_228,(0,1,6):C.R2GC_212_229,(0,1,9):C.R2GC_212_230,(0,1,11):C.R2GC_212_231,(0,1,2):C.R2GC_212_232,(0,1,5):C.R2GC_212_233,(0,1,7):C.R2GC_212_234,(0,1,10):C.R2GC_212_235})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_505_1292,(0,0,1):C.R2GC_505_1293,(0,0,2):C.R2GC_505_1294,(0,0,3):C.R2GC_505_1295,(0,0,5):C.R2GC_505_1296,(0,0,6):C.R2GC_505_1297,(0,0,8):C.R2GC_505_1298,(0,0,10):C.R2GC_505_1299,(0,0,4):C.R2GC_505_1300,(0,0,7):C.R2GC_505_1301,(0,0,9):C.R2GC_505_1302,(0,0,11):C.R2GC_505_1303})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_517_1365,(0,0,1):C.R2GC_517_1366,(0,0,3):C.R2GC_517_1367,(0,0,4):C.R2GC_517_1368,(0,0,6):C.R2GC_517_1369,(0,0,7):C.R2GC_517_1370,(0,0,8):C.R2GC_517_1371,(0,0,10):C.R2GC_517_1372,(0,0,2):C.R2GC_517_1373,(0,0,5):C.R2GC_517_1374,(0,0,9):C.R2GC_517_1375,(0,0,11):C.R2GC_517_1376,(0,1,0):C.R2GC_517_1365,(0,1,1):C.R2GC_517_1366,(0,1,3):C.R2GC_517_1367,(0,1,4):C.R2GC_517_1368,(0,1,6):C.R2GC_517_1369,(0,1,7):C.R2GC_517_1370,(0,1,8):C.R2GC_517_1371,(0,1,10):C.R2GC_517_1372,(0,1,2):C.R2GC_518_1377,(0,1,5):C.R2GC_517_1374,(0,1,9):C.R2GC_518_1378,(0,1,11):C.R2GC_517_1376})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_550_1561,(0,0,1):C.R2GC_550_1562,(0,0,9):C.R2GC_550_1563,(0,0,3):C.R2GC_550_1564,(0,0,5):C.R2GC_550_1565,(0,0,7):C.R2GC_550_1566,(0,0,10):C.R2GC_550_1567,(0,0,11):C.R2GC_550_1568,(0,0,2):C.R2GC_550_1569,(0,0,4):C.R2GC_550_1570,(0,0,6):C.R2GC_550_1571,(0,0,8):C.R2GC_550_1572,(0,1,0):C.R2GC_550_1561,(0,1,1):C.R2GC_550_1562,(0,1,9):C.R2GC_550_1563,(0,1,3):C.R2GC_550_1564,(0,1,5):C.R2GC_551_1573,(0,1,7):C.R2GC_550_1566,(0,1,10):C.R2GC_550_1567,(0,1,11):C.R2GC_550_1568,(0,1,2):C.R2GC_550_1569,(0,1,4):C.R2GC_550_1570,(0,1,6):C.R2GC_551_1574,(0,1,8):C.R2GC_550_1572})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_214_246,(0,0,1):C.R2GC_214_247,(0,0,2):C.R2GC_214_248,(0,0,4):C.R2GC_214_249,(0,0,5):C.R2GC_214_250,(0,0,6):C.R2GC_214_251,(0,0,8):C.R2GC_214_252,(0,0,10):C.R2GC_214_253,(0,0,3):C.R2GC_214_254,(0,0,7):C.R2GC_214_255,(0,0,9):C.R2GC_214_256,(0,0,11):C.R2GC_214_257})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_595_1843,(0,0,1):C.R2GC_595_1844,(0,0,2):C.R2GC_595_1845,(0,0,6):C.R2GC_595_1846,(0,0,3):C.R2GC_595_1847,(0,0,5):C.R2GC_595_1848,(0,0,7):C.R2GC_595_1849,(0,0,8):C.R2GC_595_1850,(0,0,9):C.R2GC_595_1851,(0,1,0):C.R2GC_547_1534,(0,1,1):C.R2GC_547_1535,(0,1,2):C.R2GC_547_1536,(0,1,6):C.R2GC_547_1537,(0,1,3):C.R2GC_547_1538,(0,1,4):C.R2GC_547_1539,(0,1,5):C.R2GC_547_1540,(0,1,7):C.R2GC_547_1541,(0,1,9):C.R2GC_547_1542})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.s__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.s, P.u] ], [ [P.G0, P.s, P.u], [P.H, P.s, P.u] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.g, P.s, P.u] ], [ [P.s, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_596_1852,(0,0,1):C.R2GC_596_1853,(0,0,2):C.R2GC_596_1854,(0,0,8):C.R2GC_596_1855,(0,0,3):C.R2GC_596_1856,(0,0,5):C.R2GC_596_1857,(0,0,6):C.R2GC_596_1858,(0,0,7):C.R2GC_596_1859,(0,0,9):C.R2GC_596_1860,(0,1,0):C.R2GC_553_1575,(0,1,1):C.R2GC_553_1576,(0,1,2):C.R2GC_553_1577,(0,1,8):C.R2GC_553_1578,(0,1,3):C.R2GC_553_1579,(0,1,4):C.R2GC_553_1580,(0,1,6):C.R2GC_553_1581,(0,1,7):C.R2GC_553_1582,(0,1,9):C.R2GC_553_1583})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.b__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.b, P.G0, P.u], [P.b, P.H, P.u] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_597_1861,(0,0,1):C.R2GC_597_1862,(0,0,2):C.R2GC_597_1863,(0,0,6):C.R2GC_597_1864,(0,0,3):C.R2GC_597_1865,(0,0,5):C.R2GC_597_1866,(0,0,7):C.R2GC_597_1867,(0,0,8):C.R2GC_597_1868,(0,0,9):C.R2GC_597_1869,(0,1,0):C.R2GC_544_1507,(0,1,1):C.R2GC_544_1508,(0,1,2):C.R2GC_544_1509,(0,1,6):C.R2GC_544_1510,(0,1,3):C.R2GC_544_1511,(0,1,4):C.R2GC_544_1512,(0,1,5):C.R2GC_544_1513,(0,1,7):C.R2GC_544_1514,(0,1,9):C.R2GC_544_1515})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.d__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.d, P.G__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0], [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_587_1777,(0,0,1):C.R2GC_587_1778,(0,0,2):C.R2GC_587_1779,(0,0,3):C.R2GC_587_1780,(0,0,4):C.R2GC_587_1781,(0,0,5):C.R2GC_587_1782,(0,0,6):C.R2GC_587_1783,(0,0,7):C.R2GC_587_1784,(0,0,9):C.R2GC_587_1785,(0,1,0):C.R2GC_548_1543,(0,1,1):C.R2GC_548_1544,(0,1,2):C.R2GC_548_1545,(0,1,3):C.R2GC_548_1546,(0,1,4):C.R2GC_548_1547,(0,1,5):C.R2GC_548_1548,(0,1,7):C.R2GC_548_1549,(0,1,8):C.R2GC_548_1550,(0,1,9):C.R2GC_548_1551})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_588_1786,(0,0,1):C.R2GC_588_1787,(0,0,2):C.R2GC_588_1788,(0,0,6):C.R2GC_588_1789,(0,0,3):C.R2GC_588_1790,(0,0,4):C.R2GC_588_1791,(0,0,5):C.R2GC_588_1792,(0,0,7):C.R2GC_588_1793,(0,0,9):C.R2GC_588_1794,(0,1,0):C.R2GC_554_1584,(0,1,1):C.R2GC_554_1585,(0,1,2):C.R2GC_554_1586,(0,1,6):C.R2GC_554_1587,(0,1,3):C.R2GC_554_1588,(0,1,5):C.R2GC_554_1589,(0,1,7):C.R2GC_554_1590,(0,1,8):C.R2GC_554_1591,(0,1,9):C.R2GC_554_1592})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.b__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.c, P.G__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0], [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_589_1795,(0,0,1):C.R2GC_589_1796,(0,0,2):C.R2GC_589_1797,(0,0,3):C.R2GC_589_1798,(0,0,4):C.R2GC_589_1799,(0,0,5):C.R2GC_589_1800,(0,0,7):C.R2GC_589_1801,(0,0,8):C.R2GC_589_1802,(0,0,9):C.R2GC_589_1803,(0,1,0):C.R2GC_545_1516,(0,1,1):C.R2GC_545_1517,(0,1,2):C.R2GC_545_1518,(0,1,3):C.R2GC_545_1519,(0,1,4):C.R2GC_545_1520,(0,1,5):C.R2GC_545_1521,(0,1,6):C.R2GC_545_1522,(0,1,7):C.R2GC_545_1523,(0,1,9):C.R2GC_545_1524})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.d__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.d, P.G0, P.t], [P.d, P.H, P.t] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_590_1804,(0,0,1):C.R2GC_590_1805,(0,0,2):C.R2GC_590_1806,(0,0,6):C.R2GC_590_1807,(0,0,3):C.R2GC_590_1808,(0,0,5):C.R2GC_590_1809,(0,0,7):C.R2GC_590_1810,(0,0,8):C.R2GC_590_1811,(0,0,9):C.R2GC_590_1812,(0,1,0):C.R2GC_549_1552,(0,1,1):C.R2GC_549_1553,(0,1,2):C.R2GC_549_1554,(0,1,6):C.R2GC_549_1555,(0,1,3):C.R2GC_549_1556,(0,1,4):C.R2GC_549_1557,(0,1,5):C.R2GC_549_1558,(0,1,7):C.R2GC_549_1559,(0,1,9):C.R2GC_549_1560})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.s__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.s, P.t] ], [ [P.G0, P.s, P.t], [P.H, P.s, P.t] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.g, P.s, P.t] ], [ [P.s, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_591_1813,(0,0,1):C.R2GC_591_1814,(0,0,2):C.R2GC_591_1815,(0,0,8):C.R2GC_591_1816,(0,0,3):C.R2GC_591_1817,(0,0,5):C.R2GC_591_1818,(0,0,6):C.R2GC_591_1819,(0,0,7):C.R2GC_591_1820,(0,0,9):C.R2GC_591_1821,(0,1,0):C.R2GC_555_1593,(0,1,1):C.R2GC_555_1594,(0,1,2):C.R2GC_555_1595,(0,1,8):C.R2GC_555_1596,(0,1,3):C.R2GC_555_1597,(0,1,4):C.R2GC_555_1598,(0,1,6):C.R2GC_555_1599,(0,1,7):C.R2GC_555_1600,(0,1,9):C.R2GC_555_1601})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_592_1822,(0,0,1):C.R2GC_592_1823,(0,0,2):C.R2GC_592_1824,(0,0,6):C.R2GC_592_1825,(0,0,3):C.R2GC_592_1826,(0,0,5):C.R2GC_592_1827,(0,0,7):C.R2GC_592_1828,(0,0,8):C.R2GC_592_1829,(0,0,9):C.R2GC_592_1830,(0,1,0):C.R2GC_546_1525,(0,1,1):C.R2GC_546_1526,(0,1,2):C.R2GC_546_1527,(0,1,6):C.R2GC_546_1528,(0,1,3):C.R2GC_546_1529,(0,1,4):C.R2GC_546_1530,(0,1,5):C.R2GC_546_1531,(0,1,7):C.R2GC_546_1532,(0,1,9):C.R2GC_546_1533})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_521_1384,(0,0,1):C.R2GC_521_1385,(0,0,2):C.R2GC_521_1386,(0,0,3):C.R2GC_521_1387,(0,0,4):C.R2GC_521_1388})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_525_1400,(0,0,1):C.R2GC_525_1401,(0,0,2):C.R2GC_525_1402,(0,0,3):C.R2GC_525_1403,(0,0,4):C.R2GC_525_1404})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_568_1670,(0,0,1):C.R2GC_568_1671,(0,0,2):C.R2GC_568_1672,(0,0,3):C.R2GC_568_1673,(0,0,4):C.R2GC_568_1674})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_523_1389,(0,0,1):C.R2GC_523_1390,(0,0,2):C.R2GC_523_1391,(0,0,4):C.R2GC_523_1392,(0,0,3):C.R2GC_523_1393,(0,0,5):C.R2GC_523_1394})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_527_1405,(0,0,1):C.R2GC_527_1406,(0,0,3):C.R2GC_527_1407,(0,0,5):C.R2GC_527_1408,(0,0,2):C.R2GC_527_1409,(0,0,4):C.R2GC_527_1410})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_570_1675,(0,0,1):C.R2GC_570_1676,(0,0,3):C.R2GC_570_1677,(0,0,5):C.R2GC_570_1678,(0,0,2):C.R2GC_570_1679,(0,0,4):C.R2GC_570_1680})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_216_270,(0,0,1):C.R2GC_216_271,(0,0,3):C.R2GC_216_272,(0,0,4):C.R2GC_216_273,(0,0,2):C.R2GC_216_274,(0,0,5):C.R2GC_216_275})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_217_276,(0,0,1):C.R2GC_217_277,(0,0,4):C.R2GC_217_278,(0,0,5):C.R2GC_217_279,(0,0,2):C.R2GC_217_280,(0,0,3):C.R2GC_217_281})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_218_282,(0,0,1):C.R2GC_218_283,(0,0,4):C.R2GC_218_284,(0,0,5):C.R2GC_218_285,(0,0,2):C.R2GC_218_286,(0,0,3):C.R2GC_218_287})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_520_1379,(0,0,1):C.R2GC_520_1380,(0,0,2):C.R2GC_520_1381,(0,0,3):C.R2GC_520_1382,(0,0,4):C.R2GC_520_1383})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_524_1395,(0,0,1):C.R2GC_524_1396,(0,0,2):C.R2GC_524_1397,(0,0,3):C.R2GC_524_1398,(0,0,4):C.R2GC_524_1399})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_567_1665,(0,0,1):C.R2GC_567_1666,(0,0,2):C.R2GC_567_1667,(0,0,3):C.R2GC_567_1668,(0,0,4):C.R2GC_567_1669})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_593_1831,(0,0,1):C.R2GC_593_1832,(0,0,3):C.R2GC_593_1833,(0,0,8):C.R2GC_593_1834,(0,0,5):C.R2GC_593_1835,(0,0,6):C.R2GC_593_1836,(0,0,9):C.R2GC_593_1837,(0,0,11):C.R2GC_593_1838,(0,0,2):C.R2GC_593_1839,(0,0,4):C.R2GC_593_1840,(0,0,7):C.R2GC_593_1841,(0,0,10):C.R2GC_593_1842})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_195_146,(0,0,1):C.R2GC_195_147,(0,0,3):C.R2GC_195_148,(0,0,4):C.R2GC_194_138,(0,0,5):C.R2GC_194_137,(0,0,7):C.R2GC_195_149,(0,0,8):C.R2GC_195_150,(0,0,10):C.R2GC_195_151,(0,0,2):C.R2GC_195_152,(0,0,6):C.R2GC_195_153,(0,0,9):C.R2GC_195_154,(0,0,11):C.R2GC_195_155,(0,1,0):C.R2GC_194_134,(0,1,1):C.R2GC_194_135,(0,1,3):C.R2GC_194_136,(0,1,4):C.R2GC_194_137,(0,1,5):C.R2GC_194_138,(0,1,7):C.R2GC_194_139,(0,1,8):C.R2GC_194_140,(0,1,10):C.R2GC_194_141,(0,1,2):C.R2GC_194_142,(0,1,6):C.R2GC_194_143,(0,1,9):C.R2GC_194_144,(0,1,11):C.R2GC_194_145})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_202_168,(0,0,1):C.R2GC_202_169,(0,0,3):C.R2GC_202_170,(0,0,8):C.R2GC_202_171,(0,0,5):C.R2GC_202_172,(0,0,6):C.R2GC_202_173,(0,0,9):C.R2GC_202_174,(0,0,11):C.R2GC_202_175,(0,0,2):C.R2GC_202_176,(0,0,4):C.R2GC_202_177,(0,0,7):C.R2GC_202_178,(0,0,10):C.R2GC_202_179,(0,1,0):C.R2GC_203_180,(0,1,1):C.R2GC_203_181,(0,1,3):C.R2GC_203_182,(0,1,8):C.R2GC_203_183,(0,1,5):C.R2GC_202_174,(0,1,6):C.R2GC_203_184,(0,1,9):C.R2GC_202_172,(0,1,11):C.R2GC_203_185,(0,1,2):C.R2GC_203_186,(0,1,4):C.R2GC_203_187,(0,1,7):C.R2GC_203_188,(0,1,10):C.R2GC_203_189})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_215_258,(0,0,1):C.R2GC_215_259,(0,0,3):C.R2GC_215_260,(0,0,9):C.R2GC_215_261,(0,0,5):C.R2GC_215_262,(0,0,7):C.R2GC_215_263,(0,0,10):C.R2GC_215_264,(0,0,11):C.R2GC_215_265,(0,0,2):C.R2GC_215_266,(0,0,4):C.R2GC_215_267,(0,0,6):C.R2GC_215_268,(0,0,8):C.R2GC_215_269})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_507_1304,(0,0,1):C.R2GC_507_1305,(0,0,3):C.R2GC_507_1306,(0,0,4):C.R2GC_507_1307,(0,0,6):C.R2GC_507_1308,(0,0,7):C.R2GC_507_1309,(0,0,8):C.R2GC_507_1310,(0,0,10):C.R2GC_507_1311,(0,0,2):C.R2GC_507_1312,(0,0,5):C.R2GC_507_1313,(0,0,9):C.R2GC_508_1316,(0,0,11):C.R2GC_507_1315,(0,1,0):C.R2GC_507_1304,(0,1,1):C.R2GC_507_1305,(0,1,3):C.R2GC_507_1306,(0,1,4):C.R2GC_507_1307,(0,1,6):C.R2GC_507_1308,(0,1,7):C.R2GC_507_1309,(0,1,8):C.R2GC_507_1310,(0,1,10):C.R2GC_507_1311,(0,1,2):C.R2GC_507_1312,(0,1,5):C.R2GC_507_1313,(0,1,9):C.R2GC_507_1314,(0,1,11):C.R2GC_507_1315})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_565_1650,(0,0,1):C.R2GC_565_1651,(0,0,3):C.R2GC_565_1652,(0,0,9):C.R2GC_565_1653,(0,0,5):C.R2GC_565_1654,(0,0,7):C.R2GC_566_1662,(0,0,10):C.R2GC_565_1656,(0,0,11):C.R2GC_565_1657,(0,0,2):C.R2GC_565_1658,(0,0,4):C.R2GC_566_1663,(0,0,6):C.R2GC_565_1660,(0,0,8):C.R2GC_566_1664,(0,1,0):C.R2GC_565_1650,(0,1,1):C.R2GC_565_1651,(0,1,3):C.R2GC_565_1652,(0,1,9):C.R2GC_565_1653,(0,1,5):C.R2GC_565_1654,(0,1,7):C.R2GC_565_1655,(0,1,10):C.R2GC_565_1656,(0,1,11):C.R2GC_565_1657,(0,1,2):C.R2GC_565_1658,(0,1,4):C.R2GC_565_1659,(0,1,6):C.R2GC_565_1660,(0,1,8):C.R2GC_565_1661})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.Z, P.G0, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_459_952,(0,0,1):C.R2GC_459_953,(0,0,2):C.R2GC_459_954,(0,0,3):C.R2GC_459_955,(0,0,6):C.R2GC_459_956,(0,0,7):C.R2GC_459_957,(0,0,8):C.R2GC_459_958,(0,0,9):C.R2GC_459_959,(0,0,10):C.R2GC_459_960,(0,0,5):C.R2GC_459_961,(0,0,4):C.R2GC_459_962,(0,1,0):C.R2GC_483_1092,(0,1,1):C.R2GC_483_1093,(0,1,2):C.R2GC_483_1094,(0,1,3):C.R2GC_483_1095,(0,1,6):C.R2GC_483_1096,(0,1,7):C.R2GC_483_1097,(0,1,8):C.R2GC_483_1098,(0,1,9):C.R2GC_483_1099,(0,1,10):C.R2GC_483_1100,(0,1,5):C.R2GC_483_1101,(0,1,4):C.R2GC_483_1102})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_476_1053,(0,0,1):C.R2GC_476_1054,(0,0,2):C.R2GC_476_1055,(0,0,3):C.R2GC_476_1056,(0,0,4):C.R2GC_476_1057,(0,0,5):C.R2GC_476_1058,(0,0,6):C.R2GC_476_1059,(0,0,7):C.R2GC_476_1060,(0,0,8):C.R2GC_476_1061,(0,0,10):C.R2GC_476_1062,(0,0,11):C.R2GC_476_1063,(0,0,12):C.R2GC_476_1064,(0,0,13):C.R2GC_476_1065,(0,0,14):C.R2GC_476_1066,(0,0,15):C.R2GC_476_1067,(0,0,9):C.R2GC_476_1068,(0,1,0):C.R2GC_469_1026,(0,1,1):C.R2GC_469_1027,(0,1,2):C.R2GC_469_1028,(0,1,3):C.R2GC_469_1029,(0,1,4):C.R2GC_469_1030,(0,1,5):C.R2GC_469_1031,(0,1,6):C.R2GC_469_1032,(0,1,7):C.R2GC_469_1033,(0,1,8):C.R2GC_469_1034,(0,1,10):C.R2GC_469_1035,(0,1,11):C.R2GC_469_1036,(0,1,12):C.R2GC_469_1037,(0,1,13):C.R2GC_469_1038,(0,1,14):C.R2GC_469_1039,(0,1,15):C.R2GC_469_1040,(0,1,9):C.R2GC_469_1041})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_493_1138,(0,0,2):C.R2GC_493_1139,(0,0,3):C.R2GC_493_1140,(0,0,4):C.R2GC_493_1141,(0,0,5):C.R2GC_493_1142,(0,0,6):C.R2GC_493_1143,(0,0,7):C.R2GC_493_1144,(0,0,8):C.R2GC_493_1145,(0,0,10):C.R2GC_493_1146,(0,0,12):C.R2GC_493_1147,(0,0,13):C.R2GC_493_1148,(0,0,14):C.R2GC_493_1149,(0,0,0):C.R2GC_493_1150,(0,0,9):C.R2GC_493_1151,(0,0,11):C.R2GC_493_1152})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_493_1149,(0,0,2):C.R2GC_494_1153,(0,0,3):C.R2GC_494_1154,(0,0,4):C.R2GC_494_1155,(0,0,5):C.R2GC_494_1156,(0,0,6):C.R2GC_494_1157,(0,0,7):C.R2GC_494_1158,(0,0,8):C.R2GC_494_1159,(0,0,10):C.R2GC_494_1160,(0,0,12):C.R2GC_494_1161,(0,0,13):C.R2GC_494_1162,(0,0,14):C.R2GC_493_1138,(0,0,0):C.R2GC_494_1163,(0,0,9):C.R2GC_494_1164,(0,0,11):C.R2GC_494_1165})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_503_1281,(0,0,1):C.R2GC_503_1282,(0,0,2):C.R2GC_503_1283,(0,0,3):C.R2GC_503_1284,(0,0,5):C.R2GC_503_1285,(0,0,6):C.R2GC_503_1286,(0,0,7):C.R2GC_503_1287,(0,0,8):C.R2GC_503_1288,(0,0,9):C.R2GC_503_1289,(0,0,10):C.R2GC_503_1290,(0,0,4):C.R2GC_503_1291})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_234_288,(0,0,1):C.R2GC_234_289,(0,0,2):C.R2GC_237_293,(0,0,3):C.R2GC_237_294,(0,1,0):C.R2GC_234_288,(0,1,1):C.R2GC_234_289,(0,1,2):C.R2GC_234_290})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_234_288,(0,0,1):C.R2GC_235_291,(0,0,2):C.R2GC_237_293,(0,0,3):C.R2GC_237_294,(0,1,0):C.R2GC_234_288,(0,1,1):C.R2GC_235_291,(0,1,2):C.R2GC_234_290})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_234_288,(0,0,1):C.R2GC_236_292,(0,0,2):C.R2GC_237_293,(0,0,3):C.R2GC_237_294,(0,1,0):C.R2GC_234_288,(0,1,1):C.R2GC_236_292,(0,1,2):C.R2GC_234_290})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,5):C.R2GC_174_60,(0,1,0):C.R2GC_249_335,(0,1,1):C.R2GC_313_524,(0,1,2):C.R2GC_313_525,(0,1,3):C.R2GC_313_526,(0,1,4):C.R2GC_313_527,(0,1,7):C.R2GC_249_338,(0,1,6):C.R2GC_313_528,(0,1,8):C.R2GC_313_529,(0,1,9):C.R2GC_249_340,(0,2,0):C.R2GC_249_335,(0,2,1):C.R2GC_315_530,(0,2,3):C.R2GC_315_531,(0,2,7):C.R2GC_249_338,(0,2,6):C.R2GC_315_532,(0,2,9):C.R2GC_251_347})

V_66 = CTVertex(name = 'V_66',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_249_335,(0,0,1):C.R2GC_249_336,(0,0,2):C.R2GC_249_337,(0,0,3):C.R2GC_249_338,(0,0,4):C.R2GC_249_339,(0,0,5):C.R2GC_249_340,(0,0,6):C.R2GC_249_341,(0,0,7):C.R2GC_249_342,(0,0,8):C.R2GC_249_343,(0,0,9):C.R2GC_249_344,(0,1,0):C.R2GC_249_335,(0,1,1):C.R2GC_251_346,(0,1,3):C.R2GC_249_338,(0,1,4):C.R2GC_249_339,(0,1,5):C.R2GC_251_347,(0,1,6):C.R2GC_251_348,(0,1,8):C.R2GC_251_349})

V_67 = CTVertex(name = 'V_67',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_249_335,(0,0,1):C.R2GC_293_466,(0,0,2):C.R2GC_293_467,(0,0,3):C.R2GC_293_468,(0,0,4):C.R2GC_293_469,(0,0,7):C.R2GC_249_338,(0,0,5):C.R2GC_293_470,(0,0,6):C.R2GC_293_471,(0,0,8):C.R2GC_293_472,(0,0,9):C.R2GC_249_340,(0,1,0):C.R2GC_249_335,(0,1,1):C.R2GC_295_473,(0,1,3):C.R2GC_295_474,(0,1,7):C.R2GC_249_338,(0,1,5):C.R2GC_293_470,(0,1,6):C.R2GC_295_475,(0,1,9):C.R2GC_251_347})

V_68 = CTVertex(name = 'V_68',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_245_318,(0,0,1):C.R2GC_261_374,(0,0,2):C.R2GC_261_375,(0,0,3):C.R2GC_245_319,(0,0,4):C.R2GC_261_376,(0,0,5):C.R2GC_245_321,(0,0,6):C.R2GC_261_377,(0,0,7):C.R2GC_261_378,(0,0,8):C.R2GC_261_379,(0,0,9):C.R2GC_261_380,(0,1,0):C.R2GC_245_318,(0,1,1):C.R2GC_263_381,(0,1,3):C.R2GC_245_319,(0,1,4):C.R2GC_261_376,(0,1,5):C.R2GC_247_329,(0,1,6):C.R2GC_263_382,(0,1,7):C.R2GC_263_383})

V_69 = CTVertex(name = 'V_69',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_245_318,(0,0,1):C.R2GC_281_432,(0,0,2):C.R2GC_281_433,(0,0,6):C.R2GC_245_319,(0,0,3):C.R2GC_281_434,(0,0,4):C.R2GC_281_435,(0,0,5):C.R2GC_281_436,(0,0,7):C.R2GC_245_321,(0,0,8):C.R2GC_281_437,(0,0,9):C.R2GC_281_438,(0,1,0):C.R2GC_245_318,(0,1,1):C.R2GC_283_439,(0,1,6):C.R2GC_245_319,(0,1,3):C.R2GC_281_434,(0,1,4):C.R2GC_283_440,(0,1,5):C.R2GC_283_441,(0,1,7):C.R2GC_247_329})

V_70 = CTVertex(name = 'V_70',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_245_318,(0,0,1):C.R2GC_245_319,(0,0,2):C.R2GC_245_320,(0,0,3):C.R2GC_245_321,(0,0,4):C.R2GC_245_322,(0,0,5):C.R2GC_245_323,(0,0,6):C.R2GC_245_324,(0,0,7):C.R2GC_245_325,(0,0,8):C.R2GC_245_326,(0,0,9):C.R2GC_245_327,(0,1,0):C.R2GC_245_318,(0,1,1):C.R2GC_245_319,(0,1,2):C.R2GC_245_320,(0,1,3):C.R2GC_247_329,(0,1,4):C.R2GC_247_330,(0,1,6):C.R2GC_247_331,(0,1,7):C.R2GC_247_332})

V_71 = CTVertex(name = 'V_71',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_175_61,(0,0,7):C.R2GC_175_62,(0,0,5):C.R2GC_175_63,(0,1,1):C.R2GC_323_559,(0,1,2):C.R2GC_322_555,(0,1,3):C.R2GC_331_593,(0,1,4):C.R2GC_330_591,(0,1,6):C.R2GC_341_636,(0,1,8):C.R2GC_340_634,(0,1,9):C.R2GC_324_561,(0,2,1):C.R2GC_322_553,(0,2,3):C.R2GC_330_589,(0,2,6):C.R2GC_340_632,(0,2,9):C.R2GC_325_566})

V_72 = CTVertex(name = 'V_72',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_175_61,(0,0,1):C.R2GC_323_557,(0,0,2):C.R2GC_322_551,(0,0,3):C.R2GC_175_62,(0,0,4):C.R2GC_324_560,(0,0,5):C.R2GC_324_561,(0,0,6):C.R2GC_324_562,(0,0,7):C.R2GC_324_563,(0,0,8):C.R2GC_324_564,(0,0,9):C.R2GC_324_565,(0,1,0):C.R2GC_175_61,(0,1,1):C.R2GC_322_550,(0,1,3):C.R2GC_175_62,(0,1,4):C.R2GC_324_560,(0,1,5):C.R2GC_325_566,(0,1,6):C.R2GC_325_567,(0,1,8):C.R2GC_325_568})

V_73 = CTVertex(name = 'V_73',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_175_61,(0,0,1):C.R2GC_323_558,(0,0,2):C.R2GC_322_554,(0,0,3):C.R2GC_331_592,(0,0,4):C.R2GC_330_590,(0,0,7):C.R2GC_175_62,(0,0,5):C.R2GC_346_655,(0,0,6):C.R2GC_341_635,(0,0,8):C.R2GC_340_633,(0,0,9):C.R2GC_324_561,(0,1,0):C.R2GC_175_61,(0,1,1):C.R2GC_322_552,(0,1,3):C.R2GC_330_588,(0,1,7):C.R2GC_175_62,(0,1,5):C.R2GC_346_655,(0,1,6):C.R2GC_340_631,(0,1,9):C.R2GC_325_566})

V_74 = CTVertex(name = 'V_74',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_322_547,(0,0,1):C.R2GC_325_567,(0,0,2):C.R2GC_324_563,(0,0,3):C.R2GC_175_62,(0,0,4):C.R2GC_330_587,(0,0,5):C.R2GC_322_549,(0,0,6):C.R2GC_330_588,(0,0,7):C.R2GC_330_589,(0,0,8):C.R2GC_330_590,(0,0,9):C.R2GC_330_591,(0,1,0):C.R2GC_322_547,(0,1,1):C.R2GC_324_562,(0,1,3):C.R2GC_175_62,(0,1,4):C.R2GC_330_587,(0,1,5):C.R2GC_323_556,(0,1,6):C.R2GC_331_592,(0,1,7):C.R2GC_331_593})

V_75 = CTVertex(name = 'V_75',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_322_547,(0,0,1):C.R2GC_325_568,(0,0,2):C.R2GC_324_565,(0,0,6):C.R2GC_175_62,(0,0,3):C.R2GC_340_630,(0,0,4):C.R2GC_340_631,(0,0,5):C.R2GC_340_632,(0,0,7):C.R2GC_322_549,(0,0,8):C.R2GC_340_633,(0,0,9):C.R2GC_340_634,(0,1,0):C.R2GC_322_547,(0,1,1):C.R2GC_324_564,(0,1,6):C.R2GC_175_62,(0,1,3):C.R2GC_340_630,(0,1,4):C.R2GC_341_635,(0,1,5):C.R2GC_341_636,(0,1,7):C.R2GC_323_556})

V_76 = CTVertex(name = 'V_76',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_322_547,(0,0,1):C.R2GC_175_62,(0,0,2):C.R2GC_322_548,(0,0,3):C.R2GC_322_549,(0,0,4):C.R2GC_322_550,(0,0,5):C.R2GC_322_551,(0,0,6):C.R2GC_322_552,(0,0,7):C.R2GC_322_553,(0,0,8):C.R2GC_322_554,(0,0,9):C.R2GC_322_555,(0,1,0):C.R2GC_322_547,(0,1,1):C.R2GC_175_62,(0,1,2):C.R2GC_322_548,(0,1,3):C.R2GC_323_556,(0,1,4):C.R2GC_323_557,(0,1,6):C.R2GC_323_558,(0,1,7):C.R2GC_323_559})

V_77 = CTVertex(name = 'V_77',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_409_769,(0,0,1):C.R2GC_409_770,(0,0,2):C.R2GC_409_771,(0,0,4):C.R2GC_409_772,(0,0,6):C.R2GC_409_773,(0,0,7):C.R2GC_409_774,(0,0,8):C.R2GC_409_775,(0,1,3):C.R2GC_206_194,(0,1,5):C.R2GC_206_195})

V_78 = CTVertex(name = 'V_78',
                type = 'R2',
                particles = [ P.s__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s, P.u] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.G0, P.s, P.u] ], [ [P.g, P.s, P.u] ], [ [P.H, P.s, P.u] ], [ [P.s, P.u, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_410_776,(0,0,1):C.R2GC_410_777,(0,0,2):C.R2GC_410_778,(0,0,4):C.R2GC_410_779,(0,0,6):C.R2GC_410_780,(0,0,7):C.R2GC_410_781,(0,0,8):C.R2GC_410_782,(0,1,3):C.R2GC_208_198,(0,1,5):C.R2GC_208_199})

V_79 = CTVertex(name = 'V_79',
                type = 'R2',
                particles = [ P.b__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.u] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.b, P.G0, P.u] ], [ [P.b, P.g, P.u] ], [ [P.b, P.H, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_411_783,(0,0,1):C.R2GC_411_784,(0,0,2):C.R2GC_411_785,(0,0,4):C.R2GC_411_786,(0,0,6):C.R2GC_411_787,(0,0,7):C.R2GC_411_788,(0,0,8):C.R2GC_411_789,(0,1,3):C.R2GC_204_190,(0,1,5):C.R2GC_204_191})

V_80 = CTVertex(name = 'V_80',
                type = 'R2',
                particles = [ P.d__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.d, P.W__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0] ], [ [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.d, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_412_790,(0,0,1):C.R2GC_412_791,(0,0,2):C.R2GC_412_792,(0,0,3):C.R2GC_412_793,(0,0,6):C.R2GC_412_794,(0,0,7):C.R2GC_412_795,(0,0,8):C.R2GC_412_796,(0,1,4):C.R2GC_190_126,(0,1,5):C.R2GC_190_127})

V_81 = CTVertex(name = 'V_81',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_413_797,(0,0,1):C.R2GC_413_798,(0,0,2):C.R2GC_413_799,(0,0,4):C.R2GC_413_800,(0,0,6):C.R2GC_413_801,(0,0,7):C.R2GC_413_802,(0,0,8):C.R2GC_413_803,(0,1,3):C.R2GC_192_130,(0,1,5):C.R2GC_192_131})

V_82 = CTVertex(name = 'V_82',
                type = 'R2',
                particles = [ P.b__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.c, P.W__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0] ], [ [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.c, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_414_804,(0,0,1):C.R2GC_414_805,(0,0,2):C.R2GC_414_806,(0,0,3):C.R2GC_414_807,(0,0,6):C.R2GC_414_808,(0,0,7):C.R2GC_414_809,(0,0,8):C.R2GC_414_810,(0,1,4):C.R2GC_188_122,(0,1,5):C.R2GC_188_123})

V_83 = CTVertex(name = 'V_83',
                type = 'R2',
                particles = [ P.d__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.t] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.d, P.G0, P.t] ], [ [P.d, P.g, P.t] ], [ [P.d, P.H, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_415_811,(0,0,1):C.R2GC_415_812,(0,0,2):C.R2GC_415_813,(0,0,4):C.R2GC_415_814,(0,0,6):C.R2GC_415_815,(0,0,7):C.R2GC_415_816,(0,0,8):C.R2GC_415_817,(0,1,3):C.R2GC_198_160,(0,1,5):C.R2GC_198_161})

V_84 = CTVertex(name = 'V_84',
                type = 'R2',
                particles = [ P.s__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s, P.t] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.G0, P.s, P.t] ], [ [P.g, P.s, P.t] ], [ [P.H, P.s, P.t] ], [ [P.s, P.t, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_416_818,(0,0,1):C.R2GC_416_819,(0,0,2):C.R2GC_416_820,(0,0,4):C.R2GC_416_821,(0,0,6):C.R2GC_416_822,(0,0,7):C.R2GC_416_823,(0,0,8):C.R2GC_416_824,(0,1,3):C.R2GC_200_164,(0,1,5):C.R2GC_200_165})

V_85 = CTVertex(name = 'V_85',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_417_825,(0,0,1):C.R2GC_417_826,(0,0,2):C.R2GC_417_827,(0,0,4):C.R2GC_417_828,(0,0,6):C.R2GC_417_829,(0,0,7):C.R2GC_417_830,(0,0,8):C.R2GC_417_831,(0,1,3):C.R2GC_196_156,(0,1,5):C.R2GC_196_157})

V_86 = CTVertex(name = 'V_86',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_599_1877,(0,0,1):C.R2GC_599_1878,(0,0,2):C.R2GC_599_1879,(0,0,4):C.R2GC_599_1880,(0,0,6):C.R2GC_599_1881,(0,0,7):C.R2GC_599_1882,(0,0,8):C.R2GC_599_1883,(0,1,3):C.R2GC_207_196,(0,1,5):C.R2GC_207_197})

V_87 = CTVertex(name = 'V_87',
                type = 'R2',
                particles = [ P.c__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.d, P.W__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0] ], [ [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.d, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_598_1870,(0,0,1):C.R2GC_598_1871,(0,0,2):C.R2GC_598_1872,(0,0,3):C.R2GC_598_1873,(0,0,6):C.R2GC_598_1874,(0,0,7):C.R2GC_598_1875,(0,0,8):C.R2GC_598_1876,(0,1,4):C.R2GC_191_128,(0,1,5):C.R2GC_191_129})

V_88 = CTVertex(name = 'V_88',
                type = 'R2',
                particles = [ P.t__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.t] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.d, P.G0, P.t] ], [ [P.d, P.g, P.t] ], [ [P.d, P.H, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_610_1970,(0,0,1):C.R2GC_610_1971,(0,0,2):C.R2GC_610_1972,(0,0,4):C.R2GC_610_1973,(0,0,6):C.R2GC_610_1974,(0,0,7):C.R2GC_610_1975,(0,0,8):C.R2GC_610_1976,(0,1,3):C.R2GC_199_162,(0,1,5):C.R2GC_199_163})

V_89 = CTVertex(name = 'V_89',
                type = 'R2',
                particles = [ P.u__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s, P.u] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.G0, P.s, P.u] ], [ [P.g, P.s, P.u] ], [ [P.H, P.s, P.u] ], [ [P.s, P.u, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_605_1927,(0,0,1):C.R2GC_605_1928,(0,0,2):C.R2GC_605_1929,(0,0,4):C.R2GC_605_1930,(0,0,6):C.R2GC_605_1931,(0,0,7):C.R2GC_605_1932,(0,0,8):C.R2GC_605_1933,(0,1,3):C.R2GC_209_200,(0,1,5):C.R2GC_209_201})

V_90 = CTVertex(name = 'V_90',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_604_1920,(0,0,1):C.R2GC_604_1921,(0,0,2):C.R2GC_604_1922,(0,0,4):C.R2GC_604_1923,(0,0,6):C.R2GC_604_1924,(0,0,7):C.R2GC_604_1925,(0,0,8):C.R2GC_604_1926,(0,1,3):C.R2GC_193_132,(0,1,5):C.R2GC_193_133})

V_91 = CTVertex(name = 'V_91',
                type = 'R2',
                particles = [ P.t__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s, P.t] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.G0, P.s, P.t] ], [ [P.g, P.s, P.t] ], [ [P.H, P.s, P.t] ], [ [P.s, P.t, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_611_1977,(0,0,1):C.R2GC_611_1978,(0,0,2):C.R2GC_611_1979,(0,0,4):C.R2GC_611_1980,(0,0,6):C.R2GC_611_1981,(0,0,7):C.R2GC_611_1982,(0,0,8):C.R2GC_611_1983,(0,1,3):C.R2GC_201_166,(0,1,5):C.R2GC_201_167})

V_92 = CTVertex(name = 'V_92',
                type = 'R2',
                particles = [ P.u__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.u] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.b, P.G0, P.u] ], [ [P.b, P.g, P.u] ], [ [P.b, P.H, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_613_1991,(0,0,1):C.R2GC_613_1992,(0,0,2):C.R2GC_613_1993,(0,0,4):C.R2GC_613_1994,(0,0,6):C.R2GC_613_1995,(0,0,7):C.R2GC_613_1996,(0,0,8):C.R2GC_613_1997,(0,1,3):C.R2GC_205_192,(0,1,5):C.R2GC_205_193})

V_93 = CTVertex(name = 'V_93',
                type = 'R2',
                particles = [ P.c__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.c, P.W__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0] ], [ [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.c, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_612_1984,(0,0,1):C.R2GC_612_1985,(0,0,2):C.R2GC_612_1986,(0,0,3):C.R2GC_612_1987,(0,0,6):C.R2GC_612_1988,(0,0,7):C.R2GC_612_1989,(0,0,8):C.R2GC_612_1990,(0,1,4):C.R2GC_189_124,(0,1,5):C.R2GC_189_125})

V_94 = CTVertex(name = 'V_94',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_614_1998,(0,0,1):C.R2GC_614_1999,(0,0,2):C.R2GC_614_2000,(0,0,4):C.R2GC_614_2001,(0,0,6):C.R2GC_614_2002,(0,0,7):C.R2GC_614_2003,(0,0,8):C.R2GC_614_2004,(0,1,3):C.R2GC_197_158,(0,1,5):C.R2GC_197_159})

V_95 = CTVertex(name = 'V_95',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_96 = CTVertex(name = 'V_96',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_97 = CTVertex(name = 'V_97',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_98 = CTVertex(name = 'V_98',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_99 = CTVertex(name = 'V_99',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_100 = CTVertex(name = 'V_100',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_406_765,(0,0,1):C.R2GC_406_766,(0,0,2):C.R2GC_406_767,(0,0,3):C.R2GC_406_768})

V_101 = CTVertex(name = 'V_101',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_461_973,(0,0,1):C.R2GC_465_1004,(0,0,2):C.R2GC_465_1005,(0,0,3):C.R2GC_465_1006,(0,0,4):C.R2GC_465_1007,(0,0,7):C.R2GC_461_976,(0,0,5):C.R2GC_465_1008,(0,0,6):C.R2GC_465_1009,(0,0,8):C.R2GC_465_1010,(0,0,9):C.R2GC_461_978,(0,1,0):C.R2GC_477_1069,(0,1,1):C.R2GC_479_1080,(0,1,3):C.R2GC_479_1081,(0,1,7):C.R2GC_477_1071,(0,1,5):C.R2GC_479_1082,(0,1,6):C.R2GC_479_1083,(0,1,9):C.R2GC_477_1073})

V_102 = CTVertex(name = 'V_102',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_461_973,(0,0,1):C.R2GC_461_974,(0,0,2):C.R2GC_461_975,(0,0,3):C.R2GC_461_976,(0,0,4):C.R2GC_461_977,(0,0,5):C.R2GC_461_978,(0,0,6):C.R2GC_461_979,(0,0,7):C.R2GC_461_980,(0,0,8):C.R2GC_461_981,(0,0,9):C.R2GC_461_982,(0,1,0):C.R2GC_477_1069,(0,1,1):C.R2GC_477_1070,(0,1,3):C.R2GC_477_1071,(0,1,4):C.R2GC_477_1072,(0,1,5):C.R2GC_477_1073,(0,1,6):C.R2GC_477_1074,(0,1,8):C.R2GC_477_1075})

V_103 = CTVertex(name = 'V_103',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_461_973,(0,0,1):C.R2GC_464_997,(0,0,2):C.R2GC_464_998,(0,0,3):C.R2GC_464_999,(0,0,4):C.R2GC_464_1000,(0,0,7):C.R2GC_461_976,(0,0,5):C.R2GC_464_1001,(0,0,6):C.R2GC_464_1002,(0,0,8):C.R2GC_464_1003,(0,0,9):C.R2GC_461_978,(0,1,0):C.R2GC_477_1069,(0,1,1):C.R2GC_478_1076,(0,1,3):C.R2GC_478_1077,(0,1,7):C.R2GC_477_1071,(0,1,5):C.R2GC_478_1078,(0,1,6):C.R2GC_478_1079,(0,1,9):C.R2GC_477_1073})

V_104 = CTVertex(name = 'V_104',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_460_963,(0,0,1):C.R2GC_462_983,(0,0,2):C.R2GC_462_984,(0,0,3):C.R2GC_460_964,(0,0,4):C.R2GC_462_985,(0,0,5):C.R2GC_460_966,(0,0,6):C.R2GC_462_986,(0,0,7):C.R2GC_462_987,(0,0,8):C.R2GC_462_988,(0,0,9):C.R2GC_462_989,(0,1,0):C.R2GC_466_1011,(0,1,1):C.R2GC_467_1018,(0,1,3):C.R2GC_466_1012,(0,1,4):C.R2GC_467_1019,(0,1,5):C.R2GC_466_1014,(0,1,6):C.R2GC_467_1020,(0,1,7):C.R2GC_467_1021})

V_105 = CTVertex(name = 'V_105',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_460_963,(0,0,1):C.R2GC_463_990,(0,0,2):C.R2GC_463_991,(0,0,6):C.R2GC_460_964,(0,0,3):C.R2GC_463_992,(0,0,4):C.R2GC_463_993,(0,0,5):C.R2GC_463_994,(0,0,7):C.R2GC_460_966,(0,0,8):C.R2GC_463_995,(0,0,9):C.R2GC_463_996,(0,1,0):C.R2GC_466_1011,(0,1,1):C.R2GC_468_1022,(0,1,6):C.R2GC_466_1012,(0,1,3):C.R2GC_468_1023,(0,1,4):C.R2GC_468_1024,(0,1,5):C.R2GC_468_1025,(0,1,7):C.R2GC_466_1014})

V_106 = CTVertex(name = 'V_106',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_460_963,(0,0,1):C.R2GC_460_964,(0,0,2):C.R2GC_460_965,(0,0,3):C.R2GC_460_966,(0,0,4):C.R2GC_460_967,(0,0,5):C.R2GC_460_968,(0,0,6):C.R2GC_460_969,(0,0,7):C.R2GC_460_970,(0,0,8):C.R2GC_460_971,(0,0,9):C.R2GC_460_972,(0,1,0):C.R2GC_466_1011,(0,1,1):C.R2GC_466_1012,(0,1,2):C.R2GC_466_1013,(0,1,3):C.R2GC_466_1014,(0,1,4):C.R2GC_466_1015,(0,1,6):C.R2GC_466_1016,(0,1,7):C.R2GC_466_1017})

V_107 = CTVertex(name = 'V_107',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_470_1042,(0,0,1):C.R2GC_470_1043,(0,0,2):C.R2GC_470_1044})

V_108 = CTVertex(name = 'V_108',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_471_1045,(0,0,1):C.R2GC_470_1043,(0,0,2):C.R2GC_470_1044})

V_109 = CTVertex(name = 'V_109',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_472_1046,(0,0,1):C.R2GC_470_1043,(0,0,2):C.R2GC_470_1044})

V_110 = CTVertex(name = 'V_110',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_473_1047,(0,0,1):C.R2GC_473_1048,(0,0,2):C.R2GC_473_1049,(0,0,4):C.R2GC_473_1050,(0,1,0):C.R2GC_480_1084,(0,1,1):C.R2GC_480_1085,(0,1,2):C.R2GC_480_1086,(0,1,3):C.R2GC_480_1087})

V_111 = CTVertex(name = 'V_111',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_473_1047,(0,0,1):C.R2GC_474_1051,(0,0,3):C.R2GC_473_1049,(0,0,4):C.R2GC_473_1050,(0,1,0):C.R2GC_480_1084,(0,1,1):C.R2GC_481_1088,(0,1,2):C.R2GC_481_1089,(0,1,3):C.R2GC_480_1086})

V_112 = CTVertex(name = 'V_112',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_473_1047,(0,0,1):C.R2GC_475_1052,(0,0,3):C.R2GC_473_1049,(0,0,4):C.R2GC_473_1050,(0,1,0):C.R2GC_480_1084,(0,1,1):C.R2GC_482_1090,(0,1,2):C.R2GC_482_1091,(0,1,3):C.R2GC_480_1086})

V_113 = CTVertex(name = 'V_113',
                 type = 'R2',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S1 ],
                 loop_particles = [ [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_173_58,(0,0,1):C.R2GC_173_59})

V_114 = CTVertex(name = 'V_114',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_241_310,(0,1,1):C.R2GC_241_311,(0,3,0):C.R2GC_241_310,(0,3,1):C.R2GC_241_311,(0,2,1):C.R2GC_176_64,(0,2,2):C.R2GC_176_65,(0,4,1):C.R2GC_156_8,(0,0,0):C.R2GC_154_6})

V_115 = CTVertex(name = 'V_115',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_176_65,(0,0,1):C.R2GC_177_66})

V_116 = CTVertex(name = 'V_116',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_242_312,(0,1,1):C.R2GC_242_313,(0,3,0):C.R2GC_242_312,(0,3,1):C.R2GC_242_313,(0,2,1):C.R2GC_176_64,(0,2,2):C.R2GC_176_65,(0,4,1):C.R2GC_156_8,(0,0,0):C.R2GC_154_6})

V_117 = CTVertex(name = 'V_117',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_176_65,(0,0,1):C.R2GC_177_66})

V_118 = CTVertex(name = 'V_118',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_243_314,(0,1,1):C.R2GC_243_315,(0,3,0):C.R2GC_243_314,(0,3,1):C.R2GC_243_315,(0,2,1):C.R2GC_176_64,(0,2,2):C.R2GC_176_65,(0,4,1):C.R2GC_156_8,(0,0,0):C.R2GC_154_6})

V_119 = CTVertex(name = 'V_119',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_176_65,(0,0,1):C.R2GC_177_66})

V_120 = CTVertex(name = 'V_120',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_387_707,(0,0,3):C.R2GC_387_708,(0,0,5):C.R2GC_387_709,(0,2,0):C.R2GC_387_707,(0,2,3):C.R2GC_387_708,(0,2,5):C.R2GC_387_709,(0,1,0):C.R2GC_248_333,(0,1,1):C.R2GC_187_114,(0,1,2):C.R2GC_187_118,(0,1,3):C.R2GC_244_316,(0,1,4):C.R2GC_187_121,(0,1,5):C.R2GC_248_334,(0,3,0):C.R2GC_248_333,(0,3,3):C.R2GC_244_316,(0,3,5):C.R2GC_250_345})

V_121 = CTVertex(name = 'V_121',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_364_698,(0,0,2):C.R2GC_364_699,(0,0,3):C.R2GC_364_700,(0,2,0):C.R2GC_364_698,(0,2,2):C.R2GC_364_699,(0,2,3):C.R2GC_364_700,(0,1,0):C.R2GC_153_5,(0,1,1):C.R2GC_187_115,(0,1,2):C.R2GC_244_316,(0,1,3):C.R2GC_244_317,(0,1,4):C.R2GC_187_117,(0,1,5):C.R2GC_187_118,(0,3,0):C.R2GC_153_5,(0,3,2):C.R2GC_244_316,(0,3,3):C.R2GC_246_328})

V_122 = CTVertex(name = 'V_122',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_273_411,(0,0,1):C.R2GC_273_412,(0,0,2):C.R2GC_273_413})

V_123 = CTVertex(name = 'V_123',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_252_350,(0,0,1):C.R2GC_252_351,(0,0,2):C.R2GC_252_352})

V_124 = CTVertex(name = 'V_124',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_272_408,(0,0,1):C.R2GC_272_409,(0,0,2):C.R2GC_272_410})

V_125 = CTVertex(name = 'V_125',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.W__plus__] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_373_701,(0,0,2):C.R2GC_373_702,(0,0,3):C.R2GC_373_703,(0,2,0):C.R2GC_373_701,(0,2,2):C.R2GC_373_702,(0,2,3):C.R2GC_373_703,(0,1,0):C.R2GC_153_5,(0,1,1):C.R2GC_187_116,(0,1,2):C.R2GC_244_316,(0,1,3):C.R2GC_244_317,(0,1,4):C.R2GC_187_120,(0,1,5):C.R2GC_187_121,(0,3,0):C.R2GC_153_5,(0,3,2):C.R2GC_244_316,(0,3,3):C.R2GC_246_328})

V_126 = CTVertex(name = 'V_126',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_264_384,(0,0,1):C.R2GC_264_385,(0,0,2):C.R2GC_264_386})

V_127 = CTVertex(name = 'V_127',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_253_353,(0,0,1):C.R2GC_253_354,(0,0,2):C.R2GC_253_355})

V_128 = CTVertex(name = 'V_128',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_265_387,(0,0,1):C.R2GC_265_388,(0,0,2):C.R2GC_265_389})

V_129 = CTVertex(name = 'V_129',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_358_692,(0,1,1):C.R2GC_358_693,(0,1,2):C.R2GC_358_694,(0,3,0):C.R2GC_358_692,(0,3,1):C.R2GC_358_693,(0,3,2):C.R2GC_358_694,(0,2,1):C.R2GC_244_316,(0,2,2):C.R2GC_244_317,(0,2,3):C.R2GC_187_112,(0,2,4):C.R2GC_187_113,(0,2,5):C.R2GC_187_114,(0,4,1):C.R2GC_244_316,(0,4,2):C.R2GC_246_328,(0,0,0):C.R2GC_153_5})

V_130 = CTVertex(name = 'V_130',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_359_695,(0,0,2):C.R2GC_359_696,(0,0,3):C.R2GC_359_697,(0,2,0):C.R2GC_359_695,(0,2,2):C.R2GC_359_696,(0,2,3):C.R2GC_359_697,(0,1,0):C.R2GC_248_333,(0,1,1):C.R2GC_187_112,(0,1,2):C.R2GC_244_316,(0,1,3):C.R2GC_248_334,(0,1,4):C.R2GC_187_115,(0,1,5):C.R2GC_187_116,(0,3,0):C.R2GC_248_333,(0,3,2):C.R2GC_244_316,(0,3,3):C.R2GC_250_345})

V_131 = CTVertex(name = 'V_131',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_378_704,(0,0,3):C.R2GC_378_705,(0,0,5):C.R2GC_378_706,(0,2,0):C.R2GC_378_704,(0,2,3):C.R2GC_378_705,(0,2,5):C.R2GC_378_706,(0,3,0):C.R2GC_248_333,(0,3,3):C.R2GC_244_316,(0,3,5):C.R2GC_250_345,(0,1,0):C.R2GC_248_333,(0,1,1):C.R2GC_187_113,(0,1,2):C.R2GC_187_117,(0,1,3):C.R2GC_244_316,(0,1,4):C.R2GC_187_120,(0,1,5):C.R2GC_248_334})

V_132 = CTVertex(name = 'V_132',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_296_476,(0,0,1):C.R2GC_296_477,(0,0,2):C.R2GC_296_478})

V_133 = CTVertex(name = 'V_133',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_304_500,(0,0,1):C.R2GC_304_501,(0,0,2):C.R2GC_304_502})

V_134 = CTVertex(name = 'V_134',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_297_479,(0,0,1):C.R2GC_297_480,(0,0,2):C.R2GC_297_481})

V_135 = CTVertex(name = 'V_135',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_285_445,(0,0,1):C.R2GC_285_446,(0,0,2):C.R2GC_285_447})

V_136 = CTVertex(name = 'V_136',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_305_503,(0,0,1):C.R2GC_305_504,(0,0,2):C.R2GC_305_505})

V_137 = CTVertex(name = 'V_137',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_284_442,(0,0,1):C.R2GC_284_443,(0,0,2):C.R2GC_284_444})

V_138 = CTVertex(name = 'V_138',
                 type = 'R2',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_490_1103,(0,0,1):C.R2GC_490_1104,(0,0,2):C.R2GC_490_1105,(0,0,3):C.R2GC_490_1106,(0,0,6):C.R2GC_490_1107,(0,0,7):C.R2GC_490_1108,(0,0,8):C.R2GC_490_1109,(0,0,9):C.R2GC_490_1110,(0,0,10):C.R2GC_490_1111,(0,0,11):C.R2GC_492_1135,(0,0,12):C.R2GC_492_1136,(0,0,4):C.R2GC_492_1137,(0,0,5):C.R2GC_490_1114,(0,1,0):C.R2GC_184_89,(0,1,1):C.R2GC_184_90,(0,1,2):C.R2GC_184_91,(0,1,3):C.R2GC_184_92,(0,1,6):C.R2GC_184_93,(0,1,7):C.R2GC_184_94,(0,1,8):C.R2GC_184_95,(0,1,9):C.R2GC_184_96,(0,1,10):C.R2GC_184_97,(0,1,4):C.R2GC_184_98,(0,1,5):C.R2GC_184_99})

V_139 = CTVertex(name = 'V_139',
                 type = 'R2',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_490_1103,(0,0,1):C.R2GC_490_1104,(0,0,2):C.R2GC_490_1105,(0,0,3):C.R2GC_490_1106,(0,0,6):C.R2GC_490_1107,(0,0,7):C.R2GC_490_1108,(0,0,8):C.R2GC_490_1109,(0,0,9):C.R2GC_490_1110,(0,0,10):C.R2GC_490_1111,(0,0,11):C.R2GC_490_1112,(0,0,12):C.R2GC_490_1113,(0,0,4):C.R2GC_490_1114,(0,0,5):C.R2GC_490_1115,(0,1,0):C.R2GC_184_89,(0,1,1):C.R2GC_184_90,(0,1,2):C.R2GC_184_91,(0,1,3):C.R2GC_184_92,(0,1,6):C.R2GC_184_93,(0,1,7):C.R2GC_184_94,(0,1,8):C.R2GC_184_95,(0,1,9):C.R2GC_184_96,(0,1,10):C.R2GC_184_97,(0,1,4):C.R2GC_184_99,(0,1,5):C.R2GC_184_98})

V_140 = CTVertex(name = 'V_140',
                 type = 'R2',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,18):C.R2GC_490_1112,(0,0,20):C.R2GC_491_1116,(0,0,0):C.R2GC_491_1117,(0,0,1):C.R2GC_491_1118,(0,0,2):C.R2GC_491_1119,(0,0,3):C.R2GC_491_1120,(0,0,4):C.R2GC_491_1121,(0,0,5):C.R2GC_491_1122,(0,0,6):C.R2GC_491_1123,(0,0,7):C.R2GC_491_1124,(0,0,8):C.R2GC_491_1125,(0,0,9):C.R2GC_491_1126,(0,0,10):C.R2GC_491_1127,(0,0,12):C.R2GC_491_1128,(0,0,13):C.R2GC_491_1129,(0,0,14):C.R2GC_491_1130,(0,0,15):C.R2GC_491_1131,(0,0,16):C.R2GC_491_1132,(0,0,17):C.R2GC_491_1133,(0,0,19):C.R2GC_491_1134,(0,1,0):C.R2GC_185_100,(0,1,2):C.R2GC_185_101,(0,1,3):C.R2GC_185_102,(0,1,4):C.R2GC_185_103,(0,1,5):C.R2GC_185_104,(0,1,6):C.R2GC_185_105,(0,1,7):C.R2GC_185_106,(0,1,8):C.R2GC_185_107,(0,1,9):C.R2GC_184_92,(0,1,11):C.R2GC_185_108,(0,1,12):C.R2GC_185_109,(0,1,14):C.R2GC_184_93,(0,1,15):C.R2GC_185_110,(0,1,16):C.R2GC_185_111,(0,1,17):C.R2GC_184_96})

V_141 = CTVertex(name = 'V_141',
                 type = 'R2',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,12):C.R2GC_150_2,(0,1,0):C.R2GC_169_29,(0,1,2):C.R2GC_169_30,(0,1,4):C.R2GC_169_31,(0,1,5):C.R2GC_169_32,(0,1,7):C.R2GC_169_33,(0,1,8):C.R2GC_169_34,(0,1,9):C.R2GC_169_35,(0,1,10):C.R2GC_169_36,(0,1,11):C.R2GC_169_37,(0,1,12):C.R2GC_169_38,(0,2,1):C.R2GC_168_27,(0,2,3):C.R2GC_168_28,(0,2,6):C.R2GC_150_2,(0,2,12):C.R2GC_154_6})

V_142 = CTVertex(name = 'V_142',
                 type = 'R2',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,12):C.R2GC_152_4,(0,1,0):C.R2GC_172_48,(0,1,2):C.R2GC_172_49,(0,1,4):C.R2GC_172_50,(0,1,5):C.R2GC_172_51,(0,1,7):C.R2GC_172_52,(0,1,8):C.R2GC_172_53,(0,1,9):C.R2GC_172_54,(0,1,10):C.R2GC_172_55,(0,1,11):C.R2GC_172_56,(0,1,12):C.R2GC_172_57,(0,2,1):C.R2GC_171_44,(0,2,3):C.R2GC_171_45,(0,2,6):C.R2GC_171_46,(0,2,12):C.R2GC_171_47})

V_143 = CTVertex(name = 'V_143',
                 type = 'R2',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,13):C.R2GC_151_3,(0,1,0):C.R2GC_502_1271,(0,1,2):C.R2GC_502_1272,(0,1,4):C.R2GC_502_1273,(0,1,5):C.R2GC_502_1274,(0,1,7):C.R2GC_502_1275,(0,1,8):C.R2GC_502_1276,(0,1,9):C.R2GC_502_1277,(0,1,10):C.R2GC_502_1278,(0,1,11):C.R2GC_502_1279,(0,1,13):C.R2GC_502_1280,(0,2,1):C.R2GC_170_39,(0,2,3):C.R2GC_170_40,(0,2,6):C.R2GC_170_41,(0,2,12):C.R2GC_170_42,(0,2,13):C.R2GC_170_43})

V_144 = CTVertex(name = 'V_144',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV3 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_150_2,(0,0,15):C.R2GC_151_3,(0,1,14):C.R2GC_498_1212,(0,1,16):C.R2GC_498_1213,(0,1,0):C.R2GC_498_1214,(0,1,1):C.R2GC_498_1215,(0,1,2):C.R2GC_498_1216,(0,1,3):C.R2GC_498_1217,(0,1,4):C.R2GC_498_1218,(0,1,5):C.R2GC_498_1219,(0,1,6):C.R2GC_498_1220,(0,1,7):C.R2GC_498_1221,(0,1,8):C.R2GC_498_1222,(0,1,10):C.R2GC_498_1223,(0,1,11):C.R2GC_498_1224,(0,1,12):C.R2GC_498_1225,(0,1,13):C.R2GC_498_1226,(0,1,15):C.R2GC_498_1227,(0,2,0):C.R2GC_154_6,(0,2,1):C.R2GC_187_112,(0,2,2):C.R2GC_187_113,(0,2,3):C.R2GC_187_114,(0,2,4):C.R2GC_187_115,(0,2,5):C.R2GC_187_116,(0,2,6):C.R2GC_187_117,(0,2,7):C.R2GC_187_118,(0,2,9):C.R2GC_187_119,(0,2,11):C.R2GC_187_120,(0,2,12):C.R2GC_187_121,(0,2,15):C.R2GC_170_43})

V_145 = CTVertex(name = 'V_145',
                 type = 'R2',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,4):C.R2GC_149_1,(0,1,0):C.R2GC_166_15,(0,1,2):C.R2GC_166_16,(0,1,3):C.R2GC_166_17,(0,1,5):C.R2GC_166_18,(0,1,6):C.R2GC_166_19,(0,1,7):C.R2GC_166_20,(0,2,1):C.R2GC_165_13,(0,2,4):C.R2GC_165_14})

V_146 = CTVertex(name = 'V_146',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_541_1489,(0,0,2):C.R2GC_541_1490,(0,0,4):C.R2GC_541_1491,(0,0,1):C.R2GC_541_1492,(0,0,3):C.R2GC_541_1493,(0,0,5):C.R2GC_541_1494,(0,1,0):C.R2GC_537_1465,(0,1,2):C.R2GC_537_1466,(0,1,4):C.R2GC_537_1467,(0,1,1):C.R2GC_537_1468,(0,1,3):C.R2GC_537_1469,(0,1,5):C.R2GC_537_1470})

V_147 = CTVertex(name = 'V_147',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_511_1329,(0,0,2):C.R2GC_511_1330,(0,0,4):C.R2GC_511_1331,(0,0,1):C.R2GC_511_1332,(0,0,3):C.R2GC_511_1333,(0,0,5):C.R2GC_511_1334,(0,1,0):C.R2GC_515_1353,(0,1,2):C.R2GC_515_1354,(0,1,4):C.R2GC_515_1355,(0,1,1):C.R2GC_515_1356,(0,1,3):C.R2GC_515_1357,(0,1,5):C.R2GC_515_1358})

V_148 = CTVertex(name = 'V_148',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_538_1471,(0,0,2):C.R2GC_538_1472,(0,0,4):C.R2GC_538_1473,(0,0,1):C.R2GC_538_1474,(0,0,3):C.R2GC_538_1475,(0,0,5):C.R2GC_538_1476,(0,1,0):C.R2GC_542_1495,(0,1,2):C.R2GC_542_1496,(0,1,4):C.R2GC_542_1497,(0,1,1):C.R2GC_542_1498,(0,1,3):C.R2GC_542_1499,(0,1,5):C.R2GC_542_1500})

V_149 = CTVertex(name = 'V_149',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_530_1423,(0,0,2):C.R2GC_530_1424,(0,0,4):C.R2GC_530_1425,(0,0,1):C.R2GC_530_1426,(0,0,3):C.R2GC_530_1427,(0,0,5):C.R2GC_530_1428,(0,1,0):C.R2GC_534_1447,(0,1,2):C.R2GC_534_1448,(0,1,4):C.R2GC_534_1449,(0,1,1):C.R2GC_534_1450,(0,1,3):C.R2GC_534_1451,(0,1,5):C.R2GC_534_1452})

V_150 = CTVertex(name = 'V_150',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_514_1347,(0,0,2):C.R2GC_514_1348,(0,0,4):C.R2GC_514_1349,(0,0,1):C.R2GC_514_1350,(0,0,3):C.R2GC_514_1351,(0,0,5):C.R2GC_514_1352,(0,1,0):C.R2GC_510_1323,(0,1,2):C.R2GC_510_1324,(0,1,4):C.R2GC_510_1325,(0,1,1):C.R2GC_510_1326,(0,1,3):C.R2GC_510_1327,(0,1,5):C.R2GC_510_1328})

V_151 = CTVertex(name = 'V_151',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_533_1441,(0,0,2):C.R2GC_533_1442,(0,0,4):C.R2GC_533_1443,(0,0,1):C.R2GC_533_1444,(0,0,3):C.R2GC_533_1445,(0,0,5):C.R2GC_533_1446,(0,1,0):C.R2GC_529_1417,(0,1,2):C.R2GC_529_1418,(0,1,4):C.R2GC_529_1419,(0,1,1):C.R2GC_529_1420,(0,1,3):C.R2GC_529_1421,(0,1,5):C.R2GC_529_1422})

V_152 = CTVertex(name = 'V_152',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_573_1693,(0,0,2):C.R2GC_573_1694,(0,0,4):C.R2GC_573_1695,(0,0,1):C.R2GC_573_1696,(0,0,3):C.R2GC_573_1697,(0,0,5):C.R2GC_573_1698,(0,1,0):C.R2GC_577_1717,(0,1,2):C.R2GC_577_1718,(0,1,4):C.R2GC_577_1719,(0,1,1):C.R2GC_577_1720,(0,1,3):C.R2GC_577_1721,(0,1,5):C.R2GC_577_1722})

V_153 = CTVertex(name = 'V_153',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_581_1741,(0,0,2):C.R2GC_581_1742,(0,0,4):C.R2GC_581_1743,(0,0,1):C.R2GC_581_1744,(0,0,3):C.R2GC_581_1745,(0,0,5):C.R2GC_581_1746,(0,1,0):C.R2GC_585_1765,(0,1,2):C.R2GC_585_1766,(0,1,4):C.R2GC_585_1767,(0,1,1):C.R2GC_585_1768,(0,1,3):C.R2GC_585_1769,(0,1,5):C.R2GC_585_1770})

V_154 = CTVertex(name = 'V_154',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_576_1711,(0,0,2):C.R2GC_576_1712,(0,0,4):C.R2GC_576_1713,(0,0,1):C.R2GC_576_1714,(0,0,3):C.R2GC_576_1715,(0,0,5):C.R2GC_576_1716,(0,1,0):C.R2GC_572_1687,(0,1,2):C.R2GC_572_1688,(0,1,4):C.R2GC_572_1689,(0,1,1):C.R2GC_572_1690,(0,1,3):C.R2GC_572_1691,(0,1,5):C.R2GC_572_1692})

V_155 = CTVertex(name = 'V_155',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_561_1632,(0,0,2):C.R2GC_561_1633,(0,0,4):C.R2GC_561_1634,(0,0,1):C.R2GC_561_1635,(0,0,3):C.R2GC_561_1636,(0,0,5):C.R2GC_561_1637,(0,1,0):C.R2GC_557_1608,(0,1,2):C.R2GC_557_1609,(0,1,4):C.R2GC_557_1610,(0,1,1):C.R2GC_557_1611,(0,1,3):C.R2GC_557_1612,(0,1,5):C.R2GC_557_1613})

V_156 = CTVertex(name = 'V_156',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_584_1759,(0,0,2):C.R2GC_584_1760,(0,0,4):C.R2GC_584_1761,(0,0,1):C.R2GC_584_1762,(0,0,3):C.R2GC_584_1763,(0,0,5):C.R2GC_584_1764,(0,1,0):C.R2GC_580_1735,(0,1,2):C.R2GC_580_1736,(0,1,4):C.R2GC_580_1737,(0,1,1):C.R2GC_580_1738,(0,1,3):C.R2GC_580_1739,(0,1,5):C.R2GC_580_1740})

V_157 = CTVertex(name = 'V_157',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_558_1614,(0,0,2):C.R2GC_558_1615,(0,0,4):C.R2GC_558_1616,(0,0,1):C.R2GC_558_1617,(0,0,3):C.R2GC_558_1618,(0,0,5):C.R2GC_558_1619,(0,1,0):C.R2GC_562_1638,(0,1,2):C.R2GC_562_1639,(0,1,4):C.R2GC_562_1640,(0,1,1):C.R2GC_562_1641,(0,1,3):C.R2GC_562_1642,(0,1,5):C.R2GC_562_1643})

V_158 = CTVertex(name = 'V_158',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_540_1483,(0,0,2):C.R2GC_540_1484,(0,0,4):C.R2GC_540_1485,(0,0,1):C.R2GC_540_1486,(0,0,3):C.R2GC_540_1487,(0,0,5):C.R2GC_540_1488,(0,1,0):C.R2GC_539_1477,(0,1,2):C.R2GC_539_1478,(0,1,4):C.R2GC_539_1479,(0,1,1):C.R2GC_539_1480,(0,1,3):C.R2GC_539_1481,(0,1,5):C.R2GC_539_1482})

V_159 = CTVertex(name = 'V_159',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_509_1317,(0,0,2):C.R2GC_509_1318,(0,0,4):C.R2GC_509_1319,(0,0,1):C.R2GC_509_1320,(0,0,3):C.R2GC_509_1321,(0,0,5):C.R2GC_509_1322,(0,1,0):C.R2GC_516_1359,(0,1,2):C.R2GC_516_1360,(0,1,4):C.R2GC_516_1361,(0,1,1):C.R2GC_516_1362,(0,1,3):C.R2GC_516_1363,(0,1,5):C.R2GC_516_1364})

V_160 = CTVertex(name = 'V_160',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_536_1459,(0,0,2):C.R2GC_536_1460,(0,0,4):C.R2GC_536_1461,(0,0,1):C.R2GC_536_1462,(0,0,3):C.R2GC_536_1463,(0,0,5):C.R2GC_536_1464,(0,1,0):C.R2GC_543_1501,(0,1,2):C.R2GC_543_1502,(0,1,4):C.R2GC_543_1503,(0,1,1):C.R2GC_543_1504,(0,1,3):C.R2GC_543_1505,(0,1,5):C.R2GC_543_1506})

V_161 = CTVertex(name = 'V_161',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_528_1411,(0,0,2):C.R2GC_528_1412,(0,0,4):C.R2GC_528_1413,(0,0,1):C.R2GC_528_1414,(0,0,3):C.R2GC_528_1415,(0,0,5):C.R2GC_528_1416,(0,1,0):C.R2GC_535_1453,(0,1,2):C.R2GC_535_1454,(0,1,4):C.R2GC_535_1455,(0,1,1):C.R2GC_535_1456,(0,1,3):C.R2GC_535_1457,(0,1,5):C.R2GC_535_1458})

V_162 = CTVertex(name = 'V_162',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_513_1341,(0,0,2):C.R2GC_513_1342,(0,0,4):C.R2GC_513_1343,(0,0,1):C.R2GC_513_1344,(0,0,3):C.R2GC_513_1345,(0,0,5):C.R2GC_513_1346,(0,1,0):C.R2GC_512_1335,(0,1,2):C.R2GC_512_1336,(0,1,4):C.R2GC_512_1337,(0,1,1):C.R2GC_512_1338,(0,1,3):C.R2GC_512_1339,(0,1,5):C.R2GC_512_1340})

V_163 = CTVertex(name = 'V_163',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_532_1435,(0,0,2):C.R2GC_532_1436,(0,0,4):C.R2GC_532_1437,(0,0,1):C.R2GC_532_1438,(0,0,3):C.R2GC_532_1439,(0,0,5):C.R2GC_532_1440,(0,1,0):C.R2GC_531_1429,(0,1,2):C.R2GC_531_1430,(0,1,4):C.R2GC_531_1431,(0,1,1):C.R2GC_531_1432,(0,1,3):C.R2GC_531_1433,(0,1,5):C.R2GC_531_1434})

V_164 = CTVertex(name = 'V_164',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_574_1699,(0,0,2):C.R2GC_574_1700,(0,0,4):C.R2GC_574_1701,(0,0,1):C.R2GC_574_1702,(0,0,3):C.R2GC_574_1703,(0,0,5):C.R2GC_574_1704,(0,1,0):C.R2GC_575_1705,(0,1,2):C.R2GC_575_1706,(0,1,4):C.R2GC_575_1707,(0,1,1):C.R2GC_575_1708,(0,1,3):C.R2GC_575_1709,(0,1,5):C.R2GC_575_1710})

V_165 = CTVertex(name = 'V_165',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_582_1747,(0,0,2):C.R2GC_582_1748,(0,0,4):C.R2GC_582_1749,(0,0,1):C.R2GC_582_1750,(0,0,3):C.R2GC_582_1751,(0,0,5):C.R2GC_582_1752,(0,1,0):C.R2GC_583_1753,(0,1,2):C.R2GC_583_1754,(0,1,4):C.R2GC_583_1755,(0,1,1):C.R2GC_583_1756,(0,1,3):C.R2GC_583_1757,(0,1,5):C.R2GC_583_1758})

V_166 = CTVertex(name = 'V_166',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_578_1723,(0,0,2):C.R2GC_578_1724,(0,0,4):C.R2GC_578_1725,(0,0,1):C.R2GC_578_1726,(0,0,3):C.R2GC_578_1727,(0,0,5):C.R2GC_578_1728,(0,1,0):C.R2GC_571_1681,(0,1,2):C.R2GC_571_1682,(0,1,4):C.R2GC_571_1683,(0,1,1):C.R2GC_571_1684,(0,1,3):C.R2GC_571_1685,(0,1,5):C.R2GC_571_1686})

V_167 = CTVertex(name = 'V_167',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_563_1644,(0,0,2):C.R2GC_563_1645,(0,0,4):C.R2GC_563_1646,(0,0,1):C.R2GC_563_1647,(0,0,3):C.R2GC_563_1648,(0,0,5):C.R2GC_563_1649,(0,1,0):C.R2GC_556_1602,(0,1,2):C.R2GC_556_1603,(0,1,4):C.R2GC_556_1604,(0,1,1):C.R2GC_556_1605,(0,1,3):C.R2GC_556_1606,(0,1,5):C.R2GC_556_1607})

V_168 = CTVertex(name = 'V_168',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_586_1771,(0,0,2):C.R2GC_586_1772,(0,0,4):C.R2GC_586_1773,(0,0,1):C.R2GC_586_1774,(0,0,3):C.R2GC_586_1775,(0,0,5):C.R2GC_586_1776,(0,1,0):C.R2GC_579_1729,(0,1,2):C.R2GC_579_1730,(0,1,4):C.R2GC_579_1731,(0,1,1):C.R2GC_579_1732,(0,1,3):C.R2GC_579_1733,(0,1,5):C.R2GC_579_1734})

V_169 = CTVertex(name = 'V_169',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_559_1620,(0,0,2):C.R2GC_559_1621,(0,0,4):C.R2GC_559_1622,(0,0,1):C.R2GC_559_1623,(0,0,3):C.R2GC_559_1624,(0,0,5):C.R2GC_559_1625,(0,1,0):C.R2GC_560_1626,(0,1,2):C.R2GC_560_1627,(0,1,4):C.R2GC_560_1628,(0,1,1):C.R2GC_560_1629,(0,1,3):C.R2GC_560_1630,(0,1,5):C.R2GC_560_1631})

V_170 = CTVertex(name = 'V_170',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_155_7})

V_171 = CTVertex(name = 'V_171',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_158_9})

V_172 = CTVertex(name = 'V_172',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_161_10})

V_173 = CTVertex(name = 'V_173',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_274_414,(0,0,1):C.R2GC_274_415,(0,0,2):C.R2GC_274_416,(0,0,3):C.R2GC_274_417,(0,0,4):C.R2GC_274_418,(0,0,5):C.R2GC_274_419,(0,1,0):C.R2GC_278_426,(0,1,2):C.R2GC_278_427,(0,1,3):C.R2GC_278_428})

V_174 = CTVertex(name = 'V_174',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_255_362,(0,0,1):C.R2GC_255_363,(0,0,2):C.R2GC_255_364,(0,0,3):C.R2GC_255_365,(0,0,4):C.R2GC_255_366,(0,0,5):C.R2GC_255_367,(0,1,0):C.R2GC_259_371,(0,1,2):C.R2GC_259_372,(0,1,3):C.R2GC_259_373})

V_175 = CTVertex(name = 'V_175',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_275_420,(0,0,1):C.R2GC_275_421,(0,0,2):C.R2GC_275_422,(0,0,3):C.R2GC_275_423,(0,0,4):C.R2GC_275_424,(0,0,5):C.R2GC_275_425,(0,1,0):C.R2GC_279_429,(0,1,2):C.R2GC_279_430,(0,1,3):C.R2GC_279_431})

V_176 = CTVertex(name = 'V_176',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_254_356,(0,0,1):C.R2GC_254_357,(0,0,2):C.R2GC_254_358,(0,0,3):C.R2GC_254_359,(0,0,4):C.R2GC_254_360,(0,0,5):C.R2GC_254_361,(0,1,0):C.R2GC_258_368,(0,1,2):C.R2GC_258_369,(0,1,3):C.R2GC_258_370})

V_177 = CTVertex(name = 'V_177',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_267_396,(0,0,1):C.R2GC_267_397,(0,0,2):C.R2GC_267_398,(0,0,3):C.R2GC_267_399,(0,0,4):C.R2GC_267_400,(0,0,5):C.R2GC_267_401,(0,1,0):C.R2GC_271_405,(0,1,2):C.R2GC_271_406,(0,1,3):C.R2GC_271_407})

V_178 = CTVertex(name = 'V_178',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_266_390,(0,0,1):C.R2GC_266_391,(0,0,2):C.R2GC_266_392,(0,0,3):C.R2GC_266_393,(0,0,4):C.R2GC_266_394,(0,0,5):C.R2GC_266_395,(0,1,0):C.R2GC_270_402,(0,1,2):C.R2GC_270_403,(0,1,3):C.R2GC_270_404})

V_179 = CTVertex(name = 'V_179',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_298_482,(0,0,1):C.R2GC_298_483,(0,0,2):C.R2GC_298_484,(0,0,3):C.R2GC_298_485,(0,0,4):C.R2GC_298_486,(0,0,5):C.R2GC_298_487,(0,1,0):C.R2GC_302_494,(0,1,2):C.R2GC_302_495,(0,1,4):C.R2GC_302_496})

V_180 = CTVertex(name = 'V_180',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_306_506,(0,0,1):C.R2GC_306_507,(0,0,2):C.R2GC_306_508,(0,0,3):C.R2GC_306_509,(0,0,4):C.R2GC_306_510,(0,0,5):C.R2GC_306_511,(0,1,0):C.R2GC_310_518,(0,1,2):C.R2GC_310_519,(0,1,4):C.R2GC_310_520})

V_181 = CTVertex(name = 'V_181',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_299_488,(0,0,1):C.R2GC_299_489,(0,0,2):C.R2GC_299_490,(0,0,3):C.R2GC_299_491,(0,0,4):C.R2GC_299_492,(0,0,5):C.R2GC_299_493,(0,1,0):C.R2GC_303_497,(0,1,2):C.R2GC_303_498,(0,1,4):C.R2GC_303_499})

V_182 = CTVertex(name = 'V_182',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_307_512,(0,0,1):C.R2GC_307_513,(0,0,2):C.R2GC_307_514,(0,0,3):C.R2GC_307_515,(0,0,4):C.R2GC_307_516,(0,0,5):C.R2GC_307_517,(0,1,0):C.R2GC_311_521,(0,1,2):C.R2GC_311_522,(0,1,4):C.R2GC_311_523})

V_183 = CTVertex(name = 'V_183',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_287_454,(0,0,1):C.R2GC_287_455,(0,0,2):C.R2GC_287_456,(0,0,3):C.R2GC_287_457,(0,0,4):C.R2GC_287_458,(0,0,5):C.R2GC_287_459,(0,1,0):C.R2GC_291_463,(0,1,2):C.R2GC_291_464,(0,1,4):C.R2GC_291_465})

V_184 = CTVertex(name = 'V_184',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_286_448,(0,0,1):C.R2GC_286_449,(0,0,2):C.R2GC_286_450,(0,0,3):C.R2GC_286_451,(0,0,4):C.R2GC_286_452,(0,0,5):C.R2GC_286_453,(0,1,0):C.R2GC_290_460,(0,1,2):C.R2GC_290_461,(0,1,4):C.R2GC_290_462})

V_185 = CTVertex(name = 'V_185',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_442_880,(0,0,1):C.R2GC_442_881,(0,0,2):C.R2GC_442_882,(0,0,3):C.R2GC_442_883,(0,0,4):C.R2GC_442_884,(0,0,5):C.R2GC_442_885,(0,1,0):C.R2GC_445_895,(0,1,2):C.R2GC_445_896,(0,1,3):C.R2GC_445_897})

V_186 = CTVertex(name = 'V_186',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_435_850,(0,0,1):C.R2GC_435_851,(0,0,2):C.R2GC_435_852,(0,0,3):C.R2GC_435_853,(0,0,4):C.R2GC_435_854,(0,0,5):C.R2GC_435_855,(0,1,0):C.R2GC_436_856,(0,1,2):C.R2GC_436_857,(0,1,3):C.R2GC_436_858})

V_187 = CTVertex(name = 'V_187',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_443_886,(0,0,1):C.R2GC_443_887,(0,0,2):C.R2GC_443_888,(0,0,3):C.R2GC_443_889,(0,0,4):C.R2GC_443_890,(0,0,5):C.R2GC_443_891,(0,1,0):C.R2GC_444_892,(0,1,2):C.R2GC_444_893,(0,1,3):C.R2GC_444_894})

V_188 = CTVertex(name = 'V_188',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_434_844,(0,0,1):C.R2GC_434_845,(0,0,2):C.R2GC_434_846,(0,0,3):C.R2GC_434_847,(0,0,4):C.R2GC_434_848,(0,0,5):C.R2GC_434_849,(0,1,0):C.R2GC_437_859,(0,1,2):C.R2GC_437_860,(0,1,3):C.R2GC_437_861})

V_189 = CTVertex(name = 'V_189',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_439_868,(0,0,1):C.R2GC_439_869,(0,0,2):C.R2GC_439_870,(0,0,3):C.R2GC_439_871,(0,0,4):C.R2GC_439_872,(0,0,5):C.R2GC_439_873,(0,1,0):C.R2GC_440_874,(0,1,2):C.R2GC_440_875,(0,1,3):C.R2GC_440_876})

V_190 = CTVertex(name = 'V_190',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_438_862,(0,0,1):C.R2GC_438_863,(0,0,2):C.R2GC_438_864,(0,0,3):C.R2GC_438_865,(0,0,4):C.R2GC_438_866,(0,0,5):C.R2GC_438_867,(0,1,0):C.R2GC_441_877,(0,1,2):C.R2GC_441_878,(0,1,3):C.R2GC_441_879})

V_191 = CTVertex(name = 'V_191',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_451_922,(0,0,1):C.R2GC_451_923,(0,0,2):C.R2GC_451_924,(0,0,3):C.R2GC_451_925,(0,0,4):C.R2GC_451_926,(0,0,5):C.R2GC_451_927,(0,1,0):C.R2GC_453_931,(0,1,2):C.R2GC_453_932,(0,1,4):C.R2GC_453_933})

V_192 = CTVertex(name = 'V_192',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_455_940,(0,0,1):C.R2GC_455_941,(0,0,2):C.R2GC_455_942,(0,0,3):C.R2GC_455_943,(0,0,4):C.R2GC_455_944,(0,0,5):C.R2GC_455_945,(0,1,0):C.R2GC_457_949,(0,1,2):C.R2GC_457_950,(0,1,4):C.R2GC_457_951})

V_193 = CTVertex(name = 'V_193',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_450_916,(0,0,1):C.R2GC_450_917,(0,0,2):C.R2GC_450_918,(0,0,3):C.R2GC_450_919,(0,0,4):C.R2GC_450_920,(0,0,5):C.R2GC_450_921,(0,1,0):C.R2GC_452_928,(0,1,2):C.R2GC_452_929,(0,1,4):C.R2GC_452_930})

V_194 = CTVertex(name = 'V_194',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_454_934,(0,0,1):C.R2GC_454_935,(0,0,2):C.R2GC_454_936,(0,0,3):C.R2GC_454_937,(0,0,4):C.R2GC_454_938,(0,0,5):C.R2GC_454_939,(0,1,0):C.R2GC_456_946,(0,1,2):C.R2GC_456_947,(0,1,4):C.R2GC_456_948})

V_195 = CTVertex(name = 'V_195',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_446_898,(0,0,1):C.R2GC_446_899,(0,0,2):C.R2GC_446_900,(0,0,3):C.R2GC_446_901,(0,0,4):C.R2GC_446_902,(0,0,5):C.R2GC_446_903,(0,1,0):C.R2GC_448_910,(0,1,2):C.R2GC_448_911,(0,1,4):C.R2GC_448_912})

V_196 = CTVertex(name = 'V_196',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_447_904,(0,0,1):C.R2GC_447_905,(0,0,2):C.R2GC_447_906,(0,0,3):C.R2GC_447_907,(0,0,4):C.R2GC_447_908,(0,0,5):C.R2GC_447_909,(0,1,0):C.R2GC_449_913,(0,1,2):C.R2GC_449_914,(0,1,4):C.R2GC_449_915})

V_197 = CTVertex(name = 'V_197',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_337_618,(0,0,1):C.R2GC_337_619,(0,0,2):C.R2GC_337_620,(0,0,3):C.R2GC_337_621,(0,0,4):C.R2GC_337_622,(0,0,5):C.R2GC_337_623,(0,1,0):C.R2GC_339_627,(0,1,2):C.R2GC_339_628,(0,1,3):C.R2GC_339_629})

V_198 = CTVertex(name = 'V_198',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_326_569,(0,0,1):C.R2GC_326_570,(0,0,2):C.R2GC_326_571,(0,0,3):C.R2GC_326_572,(0,0,4):C.R2GC_326_573,(0,0,5):C.R2GC_326_574,(0,1,0):C.R2GC_328_581,(0,1,2):C.R2GC_328_582,(0,1,3):C.R2GC_328_583})

V_199 = CTVertex(name = 'V_199',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_336_612,(0,0,1):C.R2GC_336_613,(0,0,2):C.R2GC_336_614,(0,0,3):C.R2GC_336_615,(0,0,4):C.R2GC_336_616,(0,0,5):C.R2GC_336_617,(0,1,0):C.R2GC_338_624,(0,1,2):C.R2GC_338_625,(0,1,3):C.R2GC_338_626})

V_200 = CTVertex(name = 'V_200',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_332_594,(0,0,1):C.R2GC_332_595,(0,0,2):C.R2GC_332_596,(0,0,3):C.R2GC_332_597,(0,0,4):C.R2GC_332_598,(0,0,5):C.R2GC_332_599,(0,1,0):C.R2GC_334_606,(0,1,2):C.R2GC_334_607,(0,1,3):C.R2GC_334_608})

V_201 = CTVertex(name = 'V_201',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_327_575,(0,0,1):C.R2GC_327_576,(0,0,2):C.R2GC_327_577,(0,0,3):C.R2GC_327_578,(0,0,4):C.R2GC_327_579,(0,0,5):C.R2GC_327_580,(0,1,0):C.R2GC_329_584,(0,1,2):C.R2GC_329_585,(0,1,3):C.R2GC_329_586})

V_202 = CTVertex(name = 'V_202',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_333_600,(0,0,1):C.R2GC_333_601,(0,0,2):C.R2GC_333_602,(0,0,3):C.R2GC_333_603,(0,0,4):C.R2GC_333_604,(0,0,5):C.R2GC_333_605,(0,1,0):C.R2GC_335_609,(0,1,2):C.R2GC_335_610,(0,1,3):C.R2GC_335_611})

V_203 = CTVertex(name = 'V_203',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_348_656,(0,0,1):C.R2GC_348_657,(0,0,2):C.R2GC_348_658,(0,0,3):C.R2GC_348_659,(0,0,4):C.R2GC_348_660,(0,0,5):C.R2GC_348_661,(0,1,0):C.R2GC_350_668,(0,1,2):C.R2GC_350_669,(0,1,4):C.R2GC_350_670})

V_204 = CTVertex(name = 'V_204',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_352_674,(0,0,1):C.R2GC_352_675,(0,0,2):C.R2GC_352_676,(0,0,3):C.R2GC_352_677,(0,0,4):C.R2GC_352_678,(0,0,5):C.R2GC_352_679,(0,1,0):C.R2GC_354_686,(0,1,2):C.R2GC_354_687,(0,1,4):C.R2GC_354_688})

V_205 = CTVertex(name = 'V_205',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_349_662,(0,0,1):C.R2GC_349_663,(0,0,2):C.R2GC_349_664,(0,0,3):C.R2GC_349_665,(0,0,4):C.R2GC_349_666,(0,0,5):C.R2GC_349_667,(0,1,0):C.R2GC_351_671,(0,1,2):C.R2GC_351_672,(0,1,4):C.R2GC_351_673})

V_206 = CTVertex(name = 'V_206',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_343_643,(0,0,1):C.R2GC_343_644,(0,0,2):C.R2GC_343_645,(0,0,3):C.R2GC_343_646,(0,0,4):C.R2GC_343_647,(0,0,5):C.R2GC_343_648,(0,1,0):C.R2GC_345_652,(0,1,2):C.R2GC_345_653,(0,1,4):C.R2GC_345_654})

V_207 = CTVertex(name = 'V_207',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_353_680,(0,0,1):C.R2GC_353_681,(0,0,2):C.R2GC_353_682,(0,0,3):C.R2GC_353_683,(0,0,4):C.R2GC_353_684,(0,0,5):C.R2GC_353_685,(0,1,0):C.R2GC_355_689,(0,1,2):C.R2GC_355_690,(0,1,4):C.R2GC_355_691})

V_208 = CTVertex(name = 'V_208',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_342_637,(0,0,1):C.R2GC_342_638,(0,0,2):C.R2GC_342_639,(0,0,3):C.R2GC_342_640,(0,0,4):C.R2GC_342_641,(0,0,5):C.R2GC_342_642,(0,1,0):C.R2GC_344_649,(0,1,2):C.R2GC_344_650,(0,1,4):C.R2GC_344_651})

V_209 = CTVertex(name = 'V_209',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_182_67,(0,0,1):C.R2GC_182_68,(0,0,2):C.R2GC_182_69,(0,0,3):C.R2GC_182_70,(0,0,5):C.R2GC_182_71,(0,0,6):C.R2GC_182_72,(0,0,7):C.R2GC_182_73,(0,0,8):C.R2GC_182_74,(0,0,9):C.R2GC_182_75,(0,0,10):C.R2GC_182_76,(0,0,4):C.R2GC_182_77})

V_210 = CTVertex(name = 'V_210',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_183_78,(0,0,1):C.R2GC_183_79,(0,0,2):C.R2GC_183_80,(0,0,3):C.R2GC_183_81,(0,0,5):C.R2GC_183_82,(0,0,6):C.R2GC_183_83,(0,0,7):C.R2GC_183_84,(0,0,8):C.R2GC_183_85,(0,0,9):C.R2GC_183_86,(0,0,10):C.R2GC_183_87,(0,0,4):C.R2GC_183_88})

V_211 = CTVertex(name = 'V_211',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_167_21,(0,0,1):C.R2GC_167_22,(0,0,2):C.R2GC_167_23,(0,0,3):C.R2GC_167_24,(0,0,4):C.R2GC_167_25,(0,0,5):C.R2GC_167_26})

V_212 = CTVertex(name = 'V_212',
                 type = 'R2',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_164_12,(0,1,0):C.R2GC_163_11})

V_213 = CTVertex(name = 'V_213',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_395_169})

V_214 = CTVertex(name = 'V_214',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_393_167})

V_215 = CTVertex(name = 'V_215',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_394_168})

V_216 = CTVertex(name = 'V_216',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_393_167})

V_217 = CTVertex(name = 'V_217',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_393_167})

V_218 = CTVertex(name = 'V_218',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_395_169})

V_219 = CTVertex(name = 'V_219',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_495_258})

V_220 = CTVertex(name = 'V_220',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_495_258})

V_221 = CTVertex(name = 'V_221',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_497_259})

V_222 = CTVertex(name = 'V_222',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_221_3})

V_223 = CTVertex(name = 'V_223',
                 type = 'UV',
                 particles = [ P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_1})

V_224 = CTVertex(name = 'V_224',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_317_92})

V_225 = CTVertex(name = 'V_225',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_318_93})

V_226 = CTVertex(name = 'V_226',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_389_163})

V_227 = CTVertex(name = 'V_227',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_317_92})

V_228 = CTVertex(name = 'V_228',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_430_201})

V_229 = CTVertex(name = 'V_229',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_429_200})

V_230 = CTVertex(name = 'V_230',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_220_2})

V_231 = CTVertex(name = 'V_231',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_421_192})

V_232 = CTVertex(name = 'V_232',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_486_250})

V_233 = CTVertex(name = 'V_233',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_425_196})

V_234 = CTVertex(name = 'V_234',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_388_162})

V_235 = CTVertex(name = 'V_235',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_318_93})

V_236 = CTVertex(name = 'V_236',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_428_199})

V_237 = CTVertex(name = 'V_237',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_429_200})

V_238 = CTVertex(name = 'V_238',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_1})

V_239 = CTVertex(name = 'V_239',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_424_195})

V_240 = CTVertex(name = 'V_240',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_485_249})

V_241 = CTVertex(name = 'V_241',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_422_193})

V_242 = CTVertex(name = 'V_242',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_432_203})

V_243 = CTVertex(name = 'V_243',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_425_196})

V_244 = CTVertex(name = 'V_244',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_431_202})

V_245 = CTVertex(name = 'V_245',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_422_193})

V_246 = CTVertex(name = 'V_246',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_487_251})

V_247 = CTVertex(name = 'V_247',
                 type = 'UV',
                 particles = [ P.ghG, P.ghG__tilde__, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_223_5})

V_248 = CTVertex(name = 'V_248',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_223_5})

V_249 = CTVertex(name = 'V_249',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g, P.g ],
                 color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
                 lorentz = [ L.VVVV3, L.VVVV6, L.VVVV7 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(1,1,0):C.UVGC_224_6,(0,0,0):C.UVGC_224_6,(2,2,0):C.UVGC_224_6})

V_250 = CTVertex(name = 'V_250',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_419_190})

V_251 = CTVertex(name = 'V_251',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_420_191})

V_252 = CTVertex(name = 'V_252',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_500_262})

V_253 = CTVertex(name = 'V_253',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_402_176})

V_254 = CTVertex(name = 'V_254',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_404_178})

V_255 = CTVertex(name = 'V_255',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_319_94})

V_256 = CTVertex(name = 'V_256',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_419_190})

V_257 = CTVertex(name = 'V_257',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_418_189})

V_258 = CTVertex(name = 'V_258',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_501_263})

V_259 = CTVertex(name = 'V_259',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_403_177})

V_260 = CTVertex(name = 'V_260',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_404_178})

V_261 = CTVertex(name = 'V_261',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_396_170})

V_262 = CTVertex(name = 'V_262',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_396_170})

V_263 = CTVertex(name = 'V_263',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_396_170})

V_264 = CTVertex(name = 'V_264',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_499_261})

V_265 = CTVertex(name = 'V_265',
                 type = 'UV',
                 particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_320_95})

V_266 = CTVertex(name = 'V_266',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_423_194})

V_267 = CTVertex(name = 'V_267',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_397_171})

V_268 = CTVertex(name = 'V_268',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_601_359,(0,1,0):C.UVGC_603_361})

V_269 = CTVertex(name = 'V_269',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_600_358,(0,1,0):C.UVGC_602_360})

V_270 = CTVertex(name = 'V_270',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_615_373,(0,1,0):C.UVGC_620_378})

V_271 = CTVertex(name = 'V_271',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_607_365,(0,1,0):C.UVGC_609_367})

V_272 = CTVertex(name = 'V_272',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_606_364,(0,1,0):C.UVGC_608_366})

V_273 = CTVertex(name = 'V_273',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_616_374,(0,1,0):C.UVGC_621_379})

V_274 = CTVertex(name = 'V_274',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_618_376,(0,1,0):C.UVGC_623_381})

V_275 = CTVertex(name = 'V_275',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_617_375,(0,1,0):C.UVGC_622_380})

V_276 = CTVertex(name = 'V_276',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_619_377,(0,1,0):C.UVGC_624_382})

V_277 = CTVertex(name = 'V_277',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_519_279})

V_278 = CTVertex(name = 'V_278',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_552_311})

V_279 = CTVertex(name = 'V_279',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_505_267})

V_280 = CTVertex(name = 'V_280',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_517_278,(0,1,0):C.UVGC_517_278})

V_281 = CTVertex(name = 'V_281',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_550_310,(0,1,0):C.UVGC_550_310})

V_282 = CTVertex(name = 'V_282',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_504_266,(0,1,0):C.UVGC_504_266})

V_283 = CTVertex(name = 'V_283',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_595_353,(0,1,0):C.UVGC_547_307})

V_284 = CTVertex(name = 'V_284',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_596_354,(0,1,0):C.UVGC_553_312})

V_285 = CTVertex(name = 'V_285',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_597_355,(0,1,0):C.UVGC_544_304})

V_286 = CTVertex(name = 'V_286',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_587_345,(0,1,0):C.UVGC_548_308})

V_287 = CTVertex(name = 'V_287',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_588_346,(0,1,0):C.UVGC_554_313})

V_288 = CTVertex(name = 'V_288',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_589_347,(0,1,0):C.UVGC_545_305})

V_289 = CTVertex(name = 'V_289',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_590_348,(0,1,0):C.UVGC_549_309})

V_290 = CTVertex(name = 'V_290',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_591_349,(0,1,0):C.UVGC_555_314})

V_291 = CTVertex(name = 'V_291',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_592_350,(0,1,0):C.UVGC_546_306})

V_292 = CTVertex(name = 'V_292',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_521_281})

V_293 = CTVertex(name = 'V_293',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_525_285})

V_294 = CTVertex(name = 'V_294',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_568_326})

V_295 = CTVertex(name = 'V_295',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_523_283})

V_296 = CTVertex(name = 'V_296',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_527_287})

V_297 = CTVertex(name = 'V_297',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_570_328})

V_298 = CTVertex(name = 'V_298',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_522_282,(0,1,0):C.UVGC_522_282})

V_299 = CTVertex(name = 'V_299',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_526_286,(0,1,0):C.UVGC_526_286})

V_300 = CTVertex(name = 'V_300',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_569_327,(0,1,0):C.UVGC_569_327})

V_301 = CTVertex(name = 'V_301',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_520_280})

V_302 = CTVertex(name = 'V_302',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_524_284})

V_303 = CTVertex(name = 'V_303',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_567_325})

V_304 = CTVertex(name = 'V_304',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_593_351})

V_305 = CTVertex(name = 'V_305',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_506_268})

V_306 = CTVertex(name = 'V_306',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_564_323})

V_307 = CTVertex(name = 'V_307',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_594_352,(0,1,0):C.UVGC_594_352})

V_308 = CTVertex(name = 'V_308',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_507_269,(0,1,0):C.UVGC_507_269})

V_309 = CTVertex(name = 'V_309',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_565_324,(0,1,0):C.UVGC_565_324})

V_310 = CTVertex(name = 'V_310',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_484_248})

V_311 = CTVertex(name = 'V_311',
                 type = 'UV',
                 particles = [ P.Z, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_459_230,(0,1,0):C.UVGC_483_247})

V_312 = CTVertex(name = 'V_312',
                 type = 'UV',
                 particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_473_242,(0,1,0):C.UVGC_469_240})

V_313 = CTVertex(name = 'V_313',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_391_165})

V_314 = CTVertex(name = 'V_314',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_392_166})

V_315 = CTVertex(name = 'V_315',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_493_256})

V_316 = CTVertex(name = 'V_316',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_391_165})

V_317 = CTVertex(name = 'V_317',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_390_164})

V_318 = CTVertex(name = 'V_318',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_494_257})

V_319 = CTVertex(name = 'V_319',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_427_198,(0,1,0):C.UVGC_426_197,(0,2,0):C.UVGC_426_197})

V_320 = CTVertex(name = 'V_320',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_488_252})

V_321 = CTVertex(name = 'V_321',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_489_253})

V_322 = CTVertex(name = 'V_322',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_488_252})

V_323 = CTVertex(name = 'V_323',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_503_265})

V_324 = CTVertex(name = 'V_324',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_398_172,(0,1,0):C.UVGC_398_172,(0,2,0):C.UVGC_399_173})

V_325 = CTVertex(name = 'V_325',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_1,(0,1,0):C.UVGC_219_1})

V_326 = CTVertex(name = 'V_326',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_1,(0,1,0):C.UVGC_219_1})

V_327 = CTVertex(name = 'V_327',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_1,(0,1,0):C.UVGC_219_1})

V_328 = CTVertex(name = 'V_328',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_313_88,(0,1,0):C.UVGC_315_90})

V_329 = CTVertex(name = 'V_329',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_249_24,(0,1,0):C.UVGC_251_26})

V_330 = CTVertex(name = 'V_330',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_293_68,(0,1,0):C.UVGC_295_70})

V_331 = CTVertex(name = 'V_331',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_261_36,(0,1,0):C.UVGC_263_38})

V_332 = CTVertex(name = 'V_332',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_281_56,(0,1,0):C.UVGC_283_58})

V_333 = CTVertex(name = 'V_333',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_245_20,(0,1,0):C.UVGC_247_22})

V_334 = CTVertex(name = 'V_334',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_356_130,(0,1,0):C.UVGC_357_131})

V_335 = CTVertex(name = 'V_335',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_324_98,(0,1,0):C.UVGC_325_99})

V_336 = CTVertex(name = 'V_336',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_346_120,(0,1,0):C.UVGC_347_121})

V_337 = CTVertex(name = 'V_337',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_330_104,(0,1,0):C.UVGC_331_105})

V_338 = CTVertex(name = 'V_338',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_340_114,(0,1,0):C.UVGC_341_115})

V_339 = CTVertex(name = 'V_339',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_322_96,(0,1,0):C.UVGC_323_97})

V_340 = CTVertex(name = 'V_340',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_409_180})

V_341 = CTVertex(name = 'V_341',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_410_181})

V_342 = CTVertex(name = 'V_342',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_411_182})

V_343 = CTVertex(name = 'V_343',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_412_183})

V_344 = CTVertex(name = 'V_344',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_413_184})

V_345 = CTVertex(name = 'V_345',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_414_185})

V_346 = CTVertex(name = 'V_346',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_415_186})

V_347 = CTVertex(name = 'V_347',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_416_187})

V_348 = CTVertex(name = 'V_348',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_417_188})

V_349 = CTVertex(name = 'V_349',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_599_357})

V_350 = CTVertex(name = 'V_350',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_598_356})

V_351 = CTVertex(name = 'V_351',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_610_368})

V_352 = CTVertex(name = 'V_352',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_605_363})

V_353 = CTVertex(name = 'V_353',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_604_362})

V_354 = CTVertex(name = 'V_354',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_611_369})

V_355 = CTVertex(name = 'V_355',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_613_371})

V_356 = CTVertex(name = 'V_356',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_612_370})

V_357 = CTVertex(name = 'V_357',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_614_372})

V_358 = CTVertex(name = 'V_358',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_359 = CTVertex(name = 'V_359',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_360 = CTVertex(name = 'V_360',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_361 = CTVertex(name = 'V_361',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_362 = CTVertex(name = 'V_362',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_363 = CTVertex(name = 'V_363',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_179})

V_364 = CTVertex(name = 'V_364',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_465_236,(0,1,0):C.UVGC_479_245})

V_365 = CTVertex(name = 'V_365',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_461_232,(0,1,0):C.UVGC_477_243})

V_366 = CTVertex(name = 'V_366',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_464_235,(0,1,0):C.UVGC_478_244})

V_367 = CTVertex(name = 'V_367',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_462_233,(0,1,0):C.UVGC_467_238})

V_368 = CTVertex(name = 'V_368',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_463_234,(0,1,0):C.UVGC_468_239})

V_369 = CTVertex(name = 'V_369',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_460_231,(0,1,0):C.UVGC_466_237})

V_370 = CTVertex(name = 'V_370',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_470_241})

V_371 = CTVertex(name = 'V_371',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_470_241})

V_372 = CTVertex(name = 'V_372',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_470_241})

V_373 = CTVertex(name = 'V_373',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_473_242,(0,1,0):C.UVGC_480_246})

V_374 = CTVertex(name = 'V_374',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_473_242,(0,1,0):C.UVGC_480_246})

V_375 = CTVertex(name = 'V_375',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_473_242,(0,1,0):C.UVGC_480_246})

V_376 = CTVertex(name = 'V_376',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_241_16,(0,2,0):C.UVGC_241_16,(0,0,0):C.UVGC_228_10})

V_377 = CTVertex(name = 'V_377',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_242_17,(0,2,0):C.UVGC_242_17,(0,0,0):C.UVGC_229_11})

V_378 = CTVertex(name = 'V_378',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_243_18,(0,2,0):C.UVGC_243_18,(0,0,0):C.UVGC_232_14})

V_379 = CTVertex(name = 'V_379',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_387_161,(0,3,0):C.UVGC_387_161,(0,2,0):C.UVGC_312_87,(0,4,0):C.UVGC_314_89,(0,0,0):C.UVGC_233_15})

V_380 = CTVertex(name = 'V_380',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_364_138,(0,3,0):C.UVGC_364_138,(0,2,0):C.UVGC_260_35,(0,4,0):C.UVGC_262_37,(0,0,0):C.UVGC_227_9})

V_381 = CTVertex(name = 'V_381',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_273_48,(0,0,0):C.UVGC_370_144,(0,2,0):C.UVGC_372_146,(0,3,0):C.UVGC_277_52})

V_382 = CTVertex(name = 'V_382',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_252_27,(0,0,0):C.UVGC_362_136,(0,2,0):C.UVGC_360_134,(0,3,0):C.UVGC_256_31})

V_383 = CTVertex(name = 'V_383',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_272_47,(0,0,0):C.UVGC_371_145,(0,2,0):C.UVGC_369_143,(0,3,0):C.UVGC_276_51})

V_384 = CTVertex(name = 'V_384',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_373_147,(0,3,0):C.UVGC_373_147,(0,2,0):C.UVGC_280_55,(0,4,0):C.UVGC_282_57,(0,0,0):C.UVGC_230_12})

V_385 = CTVertex(name = 'V_385',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_264_39,(0,0,0):C.UVGC_367_141,(0,2,0):C.UVGC_365_139,(0,3,0):C.UVGC_268_43})

V_386 = CTVertex(name = 'V_386',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_253_28,(0,0,0):C.UVGC_361_135,(0,2,0):C.UVGC_363_137,(0,3,0):C.UVGC_257_32})

V_387 = CTVertex(name = 'V_387',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_265_40,(0,0,0):C.UVGC_366_140,(0,2,0):C.UVGC_368_142,(0,3,0):C.UVGC_269_44})

V_388 = CTVertex(name = 'V_388',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_358_132,(0,3,0):C.UVGC_358_132,(0,2,0):C.UVGC_244_19,(0,4,0):C.UVGC_246_21,(0,0,0):C.UVGC_225_7})

V_389 = CTVertex(name = 'V_389',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_359_133,(0,3,0):C.UVGC_359_133,(0,2,0):C.UVGC_248_23,(0,4,0):C.UVGC_250_25,(0,0,0):C.UVGC_226_8})

V_390 = CTVertex(name = 'V_390',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_378_152,(0,3,0):C.UVGC_378_152,(0,4,0):C.UVGC_294_69,(0,2,0):C.UVGC_292_67,(0,0,0):C.UVGC_231_13})

V_391 = CTVertex(name = 'V_391',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_296_71,(0,0,0):C.UVGC_381_155,(0,2,0):C.UVGC_379_153,(0,3,0):C.UVGC_300_75})

V_392 = CTVertex(name = 'V_392',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_304_79,(0,0,0):C.UVGC_385_159,(0,2,0):C.UVGC_383_157,(0,3,0):C.UVGC_308_83})

V_393 = CTVertex(name = 'V_393',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_297_72,(0,0,0):C.UVGC_380_154,(0,2,0):C.UVGC_382_156,(0,3,0):C.UVGC_301_76})

V_394 = CTVertex(name = 'V_394',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_285_60,(0,0,0):C.UVGC_375_149,(0,2,0):C.UVGC_377_151,(0,3,0):C.UVGC_289_64})

V_395 = CTVertex(name = 'V_395',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_305_80,(0,0,0):C.UVGC_384_158,(0,2,0):C.UVGC_386_160,(0,3,0):C.UVGC_309_84})

V_396 = CTVertex(name = 'V_396',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_284_59,(0,0,0):C.UVGC_376_150,(0,2,0):C.UVGC_374_148,(0,3,0):C.UVGC_288_63})

V_397 = CTVertex(name = 'V_397',
                 type = 'UV',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_492_255})

V_398 = CTVertex(name = 'V_398',
                 type = 'UV',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_490_254})

V_399 = CTVertex(name = 'V_399',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_490_254})

V_400 = CTVertex(name = 'V_400',
                 type = 'UV',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_502_264})

V_401 = CTVertex(name = 'V_401',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_316_91,(0,1,0):C.UVGC_498_260,(0,2,0):C.UVGC_222_4})

V_402 = CTVertex(name = 'V_402',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_541_301,(0,1,0):C.UVGC_537_297})

V_403 = CTVertex(name = 'V_403',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_511_272,(0,1,0):C.UVGC_515_276})

V_404 = CTVertex(name = 'V_404',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_538_298,(0,1,0):C.UVGC_542_302})

V_405 = CTVertex(name = 'V_405',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_530_290,(0,1,0):C.UVGC_534_294})

V_406 = CTVertex(name = 'V_406',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_514_275,(0,1,0):C.UVGC_510_271})

V_407 = CTVertex(name = 'V_407',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_533_293,(0,1,0):C.UVGC_529_289})

V_408 = CTVertex(name = 'V_408',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_573_331,(0,1,0):C.UVGC_577_335})

V_409 = CTVertex(name = 'V_409',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_581_339,(0,1,0):C.UVGC_585_343})

V_410 = CTVertex(name = 'V_410',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_576_334,(0,1,0):C.UVGC_572_330})

V_411 = CTVertex(name = 'V_411',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_561_320,(0,1,0):C.UVGC_557_316})

V_412 = CTVertex(name = 'V_412',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_584_342,(0,1,0):C.UVGC_580_338})

V_413 = CTVertex(name = 'V_413',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_558_317,(0,1,0):C.UVGC_562_321})

V_414 = CTVertex(name = 'V_414',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_540_300,(0,1,0):C.UVGC_539_299})

V_415 = CTVertex(name = 'V_415',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_509_270,(0,1,0):C.UVGC_516_277})

V_416 = CTVertex(name = 'V_416',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_536_296,(0,1,0):C.UVGC_543_303})

V_417 = CTVertex(name = 'V_417',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_528_288,(0,1,0):C.UVGC_535_295})

V_418 = CTVertex(name = 'V_418',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_513_274,(0,1,0):C.UVGC_512_273})

V_419 = CTVertex(name = 'V_419',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_532_292,(0,1,0):C.UVGC_531_291})

V_420 = CTVertex(name = 'V_420',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_574_332,(0,1,0):C.UVGC_575_333})

V_421 = CTVertex(name = 'V_421',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_582_340,(0,1,0):C.UVGC_583_341})

V_422 = CTVertex(name = 'V_422',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_578_336,(0,1,0):C.UVGC_571_329})

V_423 = CTVertex(name = 'V_423',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_563_322,(0,1,0):C.UVGC_556_315})

V_424 = CTVertex(name = 'V_424',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_586_344,(0,1,0):C.UVGC_579_337})

V_425 = CTVertex(name = 'V_425',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_559_318,(0,1,0):C.UVGC_560_319})

V_426 = CTVertex(name = 'V_426',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_274_49,(0,1,0):C.UVGC_278_53})

V_427 = CTVertex(name = 'V_427',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_255_30,(0,1,0):C.UVGC_259_34})

V_428 = CTVertex(name = 'V_428',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_275_50,(0,1,0):C.UVGC_279_54})

V_429 = CTVertex(name = 'V_429',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_254_29,(0,1,0):C.UVGC_258_33})

V_430 = CTVertex(name = 'V_430',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_267_42,(0,1,0):C.UVGC_271_46})

V_431 = CTVertex(name = 'V_431',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_266_41,(0,1,0):C.UVGC_270_45})

V_432 = CTVertex(name = 'V_432',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_298_73,(0,1,0):C.UVGC_302_77})

V_433 = CTVertex(name = 'V_433',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_306_81,(0,1,0):C.UVGC_310_85})

V_434 = CTVertex(name = 'V_434',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_299_74,(0,1,0):C.UVGC_303_78})

V_435 = CTVertex(name = 'V_435',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_307_82,(0,1,0):C.UVGC_311_86})

V_436 = CTVertex(name = 'V_436',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_287_62,(0,1,0):C.UVGC_291_66})

V_437 = CTVertex(name = 'V_437',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_286_61,(0,1,0):C.UVGC_290_65})

V_438 = CTVertex(name = 'V_438',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_442_213,(0,1,0):C.UVGC_445_216})

V_439 = CTVertex(name = 'V_439',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_435_206,(0,1,0):C.UVGC_436_207})

V_440 = CTVertex(name = 'V_440',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_443_214,(0,1,0):C.UVGC_444_215})

V_441 = CTVertex(name = 'V_441',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_434_205,(0,1,0):C.UVGC_437_208})

V_442 = CTVertex(name = 'V_442',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_439_210,(0,1,0):C.UVGC_440_211})

V_443 = CTVertex(name = 'V_443',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_438_209,(0,1,0):C.UVGC_441_212})

V_444 = CTVertex(name = 'V_444',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_451_222,(0,1,0):C.UVGC_453_224})

V_445 = CTVertex(name = 'V_445',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_455_226,(0,1,0):C.UVGC_457_228})

V_446 = CTVertex(name = 'V_446',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_450_221,(0,1,0):C.UVGC_452_223})

V_447 = CTVertex(name = 'V_447',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_454_225,(0,1,0):C.UVGC_456_227})

V_448 = CTVertex(name = 'V_448',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_446_217,(0,1,0):C.UVGC_448_219})

V_449 = CTVertex(name = 'V_449',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_447_218,(0,1,0):C.UVGC_449_220})

V_450 = CTVertex(name = 'V_450',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_337_111,(0,1,0):C.UVGC_339_113})

V_451 = CTVertex(name = 'V_451',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_326_100,(0,1,0):C.UVGC_328_102})

V_452 = CTVertex(name = 'V_452',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_336_110,(0,1,0):C.UVGC_338_112})

V_453 = CTVertex(name = 'V_453',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_332_106,(0,1,0):C.UVGC_334_108})

V_454 = CTVertex(name = 'V_454',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_327_101,(0,1,0):C.UVGC_329_103})

V_455 = CTVertex(name = 'V_455',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_333_107,(0,1,0):C.UVGC_335_109})

V_456 = CTVertex(name = 'V_456',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_348_122,(0,1,0):C.UVGC_350_124})

V_457 = CTVertex(name = 'V_457',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_352_126,(0,1,0):C.UVGC_354_128})

V_458 = CTVertex(name = 'V_458',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_349_123,(0,1,0):C.UVGC_351_125})

V_459 = CTVertex(name = 'V_459',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_343_117,(0,1,0):C.UVGC_345_119})

V_460 = CTVertex(name = 'V_460',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_353_127,(0,1,0):C.UVGC_355_129})

V_461 = CTVertex(name = 'V_461',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_342_116,(0,1,0):C.UVGC_344_118})

V_462 = CTVertex(name = 'V_462',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_401_175})

V_463 = CTVertex(name = 'V_463',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_401_175})

V_464 = CTVertex(name = 'V_464',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_458_229})

V_465 = CTVertex(name = 'V_465',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_400_174})

V_466 = CTVertex(name = 'V_466',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_400_174})

V_467 = CTVertex(name = 'V_467',
                 type = 'UV',
                 particles = [ P.Z, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_433_204})
