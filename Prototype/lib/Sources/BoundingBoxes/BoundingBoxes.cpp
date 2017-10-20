// BoundingBoxes.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include <iostream>

#include "BasicDefs.h"
#include "SimplePolygonConvexHull.h"
#include "AxisAlignedBoundingBox.h"
#include "ObjectOrientedBoundingBox.h"

using namespace BoundingBoxes;
using namespace BoundingBoxes::ConvexHull;


int main()
{
	Vector2<> pts[] = {
		/*
		Vector2<>( { 35, 174   } ),
		Vector2<>( { 45, 140   } ),
		Vector2<>( { 30, 110   } ),
		Vector2<>( { 40, 103   } ),
		Vector2<>( { 74, 133   } ),
		Vector2<>( { 106, 110  } ),
		Vector2<>( { 72, 90    } ),
		Vector2<>( { 77, 39    } ),
		Vector2<>( { 105, 45   } ),
		Vector2<>( { 147, 11   } ),
		Vector2<>( { 140, 39   } ),
		Vector2<>( { 98, 74    } ),
		Vector2<>( { 125, 102  } ),
		Vector2<>( { 135, 63   } ),
		Vector2<>( { 155, 45   } ),
		Vector2<>( { 150, 86   } ),
		Vector2<>( { 200, 110  } ),
		Vector2<>( { 160, 125  } ),
		Vector2<>( { 157, 155  } ),
		Vector2<>( { 128, 123  } ),
		Vector2<>( { 91, 141   } ),
		Vector2<>( { 89, 154   } ),
		Vector2<>( { 66, 157   } ),
		*/

		Vector2<> ( { 65.9091033935547f,	-37.7272720336914f	} ),
		Vector2<> ( { 105.909103393555f,	12.27272605896f		} ),
		Vector2<> ( { -4.09089660644531f,	42.2727279663086f	} ),
		Vector2<> ( { 65.9091033935547f,	52.2727279663086f	} ),
		Vector2<> ( { 5.90910339355469f,	72.2727279663086f	} ),
		Vector2<> ( { -44.0908966064453f,	62.2727279663086f	} ),
		Vector2<> ( { -74.0908966064453f,	2.27272605895996f	} ),
		Vector2<> ( { -34.0908966064453f,	32.2727279663086f	} ),
		Vector2<> ( { -34.0908966064453f,	52.2727279663086f	} ),
		Vector2<> ( { -14.0908966064453f,	42.2727279663086f	} ),
		Vector2<> ( { -24.0908966064453f,	-7.72727394104004f	} ),
		Vector2<> ( { -84.0908966064453f,	-17.72727394104f	} ),
		Vector2<> ( { -64.0908966064453f,	-47.7272720336914f	} ),
		Vector2<> ( { -14.0908966064453f,	-27.72727394104f	} ),
		Vector2<> ( { 15.9091033935547f,	22.27272605896f		} ),
		Vector2<> ( { 25.9091033935547f,	2.27272605895996f	} ),
		Vector2<> ( { -4.09089660644531f,	-37.7272720336914f	} ),
		Vector2<> ( { 5.90910339355469f,	-7.72727394104004f	} ),
		Vector2<> ( { -24.0908966064453f,	-47.7272720336914f	} ),
		Vector2<> ( { 15.9091033935547f,	-67.7272720336914f	} ),
		Vector2<> ( { 55.9091033935547f,	-27.72727394104f	} ),
		Vector2<> ( { 55.9091033935547f,	-67.7272720336914f	} ),
	};

	const uint ptsCount = (uint)_countof( pts );

	uint convexHullLength = ptsCount;
	Buffer< Vector2<> > convexHull( convexHullLength );
	
	SimplePolygonConvexHull::Get( ptsCount, pts, convexHullLength, convexHull.Ptr() );
	for ( uint i = 0; i < convexHullLength / 2; i++ ) {
		Vector2<> tmp = convexHull[i];
		convexHull[i] = convexHull[convexHullLength - i - 1];
		convexHull[convexHullLength - i - 1] = tmp;
	}

	Timer timer;
	TimeGroup& tg = timer.GetTimeGroup( "Test" );

	Vector2<> aabb[2];
	tg.Start();
	AxisAlignedBoundingBox::Get( convexHullLength, convexHull.Ptr(), aabb );
	tg.SaveElapsed();

	Vector2<> oobb2[4];
	tg.Start();
	ObjectOrientedBoundingBox::Get( convexHullLength, convexHull.Ptr(), oobb2 );
	tg.SaveElapsed();

	printf( "Convex hull length: %u\nConvex hull: [", convexHullLength );
	for ( uint i = 0; i < convexHullLength; i++ ) {
		printf( " %f, %f, ", convexHull[i][0], convexHull[i][1] );
	}
	printf( "]\n" );

	printf( "Axis aligned bounding box: [ %f, %f ], [ %f, %f ]\n", aabb[0][0], aabb[0][1], aabb[1][0], aabb[1][1] );

	printf( "Oriented bounding box 2: [ %f, %f , %f, %f , %f, %f , %f, %f ]\n", oobb2[0][0], oobb2[0][1], oobb2[1][0], oobb2[1][1], oobb2[2][0], oobb2[2][1], oobb2[3][0], oobb2[3][1] );


	printf( "Times: AABB: %fms, OOBB: %fms\n", tg.durations[0], tg.durations[1] );

	int a = 0;
	std::cin >> a;

    return 0;

	/*
	
	157.000000, 155.00000
	200.000000, 110.00000
	147.000000, 11.000000
	77.000000, 39.000000 
	30.000000, 110.000000
	35.000000, 174.000000
	

	120.269318, 230.445969
	229.419189, 65.559509 
	111.215866, -12.688238
	2.065835, 152.198456 

	*/
}

