#include "stdafx.h"
#include "BasicDefs.h"
#include "SimplePolygonConvexHull.h"

#include <deque>

namespace BoundingBoxes { namespace ConvexHull {

	void SimplePolygonConvexHull::Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pPoints, __inout uint& convexHullLength, __out_ecount( convexHullLength ) Vector2<>* pConvexHull ) {
		if ( pointCount < 3 ) {
			throw InvalidArgumentException( GET_VARIABLE_NAME( pointCount ), "must be greater than 3" );
		}

		std::deque< Vector2<> > convexHull;

		if ( IsLeftTurn( pPoints[0], pPoints[1], pPoints[2] ) ) {
			convexHull.push_back( pPoints[0] );
			convexHull.push_back( pPoints[1] );
		} else {
			convexHull.push_back( pPoints[1] );
			convexHull.push_back( pPoints[0] );
		}
		convexHull.push_back( pPoints[2] );
		convexHull.push_front( pPoints[2] );

		for ( uint i = 3; i < pointCount; i++ ) {
			const Vector2<>& currentPoint = pPoints[i];

			size_t ixEnd = convexHull.size() - 1;

			if ( !IsLeftTurn( convexHull[0], convexHull[1], currentPoint ) || !IsLeftTurn( convexHull[ixEnd - 1], convexHull[ixEnd], currentPoint ) ) {
				while ( !IsLeftTurn( convexHull[0], convexHull[1], currentPoint ) ) {
					convexHull.pop_front();
				}
				convexHull.push_front( currentPoint );
				
				ixEnd = convexHull.size() - 1;

				while ( !IsLeftTurn( convexHull[ixEnd - 1], convexHull[ixEnd], currentPoint ) ) {
					convexHull.pop_back();
					ixEnd--;
				}
				convexHull.push_back( currentPoint );
			}
		}

		if ( convexHullLength < ( convexHull.size() - 1 ) ) {
			throw InvalidArgumentException( GET_VARIABLE_NAME( convexHullLength ), "is too small" );
		}

		convexHullLength = static_cast<uint>( convexHull.size() - 1 );
		std::copy( convexHull.begin(), convexHull.end() - 1, pConvexHull );
	}
	
	bool SimplePolygonConvexHull::IsLeftTurn( __in const Vector2<>& a, __in const Vector2<>& b, __in const Vector2<>& c ) {
		return (
			( ( b[0] - a[0] ) * ( c[1] - a[1] )  ) - ( ( c[0] - a[0] ) * ( b[1] - a[1] ) ) 
		) < 0;
	}

} }