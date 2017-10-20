#pragma once

namespace BoundingBoxes { namespace ConvexHull {

	class SimplePolygonConvexHull
	{
	public:
		
		static void Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pPoints, __inout uint& convexHullLength, __out_ecount( convexHullLength ) Vector2<>* pConvexHull );

	protected:

		static bool IsLeftTurn( __in const Vector2<>& pt1, __in const Vector2<>& pt2, __in const Vector2<>& pt3 );

	};

} }