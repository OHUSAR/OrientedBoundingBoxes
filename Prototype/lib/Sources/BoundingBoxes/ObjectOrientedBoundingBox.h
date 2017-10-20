#pragma once

namespace BoundingBoxes {

	class ObjectOrientedBoundingBox
	{
	public:
		
		static void Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pOOBB );

	protected:

		enum SIDE_INDICES {
			LEFT = 0,
			BOTTOM = 1,
			RIGHT = 2,
			TOP = 3
		};

	protected:

		static void GetOrientedEdges( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( pointCount ) Vector2<>* pEdges );

		static void GetExtremePointIndices( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) int* pIndices );

		static void GetBox( __in_ecount( 2 ) const Vector2<>* pCaliperDirs, __in_ecount( 4 ) const int* pEdgeIndices, __in const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pBox, __out float& area );

		
		// Remove when on git :)
		static void GetProto( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pOOBB );

		static void GetBoxProto( __in_ecount( 4 ) const Vector2<>* pCaliperDirs, __in_ecount( 4 ) const int* pEdgeIndices, __in const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pBox, __out float& area );
	};

}
