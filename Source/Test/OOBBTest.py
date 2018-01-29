import unittest

from Core.BasicDefs import *
from Core.SimulationObjects import SimulationPolygon


class OOBBTest( unittest.TestCase ):
    def testExampleOOBB(self):
        vertices = [
            vector([65.9091033935547, -37.7272720336914]),
            vector([105.909103393555, 12.27272605896	] ),
            vector( [  -4.09089660644531,	42.2727279663086	] ),
            vector( [  65.9091033935547,	52.2727279663086	] ),
            vector( [  5.90910339355469,	72.2727279663086	] ),
            vector( [  -44.0908966064453,	62.2727279663086	] ),
            vector( [  -74.0908966064453,	2.27272605895996	] ),
            vector( [  -34.0908966064453,	32.2727279663086	] ),
            vector( [  -34.0908966064453,	52.2727279663086	] ),
            vector( [  -14.0908966064453,	42.2727279663086	] ),
            vector( [  -24.0908966064453,	-7.72727394104004	] ),
            vector( [  -84.0908966064453,	-17.72727394104	] ),
            vector( [  -64.0908966064453,	-47.7272720336914	] ),
            vector( [  -14.0908966064453,	-27.72727394104	] ),
            vector( [  15.9091033935547,	22.27272605896		] ),
            vector( [  25.9091033935547,	2.27272605895996	] ),
            vector( [  -4.09089660644531,	-37.7272720336914	] ),
            vector( [  5.90910339355469,	-7.72727394104004	] ),
            vector( [  -24.0908966064453,	-47.7272720336914	] ),
            vector( [  15.9091033935547,	-67.7272720336914	] ),
            vector( [  55.9091033935547,	-27.72727394104	] ),
            vector( [  55.9091033935547,	-67.7272720336914	] )
        ]

        so = SimulationPolygon( vertices )
        result = so.bvh.boundingVolumes[0].GetVertices()
        expected_result = [
            [-92, -33],
            [47, -103],
            [ 113,   28],
            [-26,  98],
        ]
        for i, v in enumerate(result):
            a, b = [int(x) for x in v]
            self.assertEqual(expected_result[i][0], a)
            self.assertEqual(expected_result[i][1], b)
