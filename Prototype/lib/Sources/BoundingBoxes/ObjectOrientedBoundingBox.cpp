#include "stdafx.h"
#include "BasicDefs.h"
#include "ObjectOrientedBoundingBox.h"

namespace BoundingBoxes {

	void ObjectOrientedBoundingBox::Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pOOBB ) {
		Buffer< Vector2<> > edges( pointCount );

		float minArea = FLT_MAX;
		float tmpArea = FLT_MAX;
		Vector2<> tmpBox[4];

		int edgeIndices[4];
		float angles[4];
		Vector2<> caliperDirs[2] = {
			Vector2<>( { 0, -1 } ),
			Vector2<>( { 1, 0 } )
		};

		GetOrientedEdges( pointCount, pConvexHull, edges.Ptr() );
		GetExtremePointIndices( pointCount, pConvexHull, edgeIndices );

		for ( uint i = 0; i < pointCount; i++ ) {
			angles[SIDE_INDICES::LEFT]		= caliperDirs[SIDE_INDICES::LEFT]	* edges[ edgeIndices[ SIDE_INDICES::LEFT ] ];
			angles[SIDE_INDICES::BOTTOM]	= caliperDirs[SIDE_INDICES::BOTTOM] * edges[ edgeIndices[ SIDE_INDICES::BOTTOM ] ];
			angles[SIDE_INDICES::RIGHT]		= caliperDirs[SIDE_INDICES::LEFT]	* edges[ edgeIndices[ SIDE_INDICES::RIGHT ] ];
			angles[SIDE_INDICES::TOP]		= caliperDirs[SIDE_INDICES::BOTTOM] * edges[ edgeIndices[ SIDE_INDICES::TOP ] ];
		
			for ( uint j = 0; j < 4; j++ ) {
				angles[j] *= angles[j];
			}

			uint minAngleIx = 0;
			for ( uint j = 1; j < 4; j++ ) {
				if ( angles[j] > angles[minAngleIx] ) {
					minAngleIx = j;
				}
			}

			uint minCaliperIx = minAngleIx % 2;

			caliperDirs[minCaliperIx] = edges[edgeIndices[minAngleIx]];
			caliperDirs[( minCaliperIx + 1 ) % 2] = GetOrthogonal( caliperDirs[minCaliperIx] );
			edgeIndices[minAngleIx] = ( edgeIndices[minAngleIx] + 1 ) % pointCount;

			GetBox( caliperDirs, edgeIndices, pConvexHull, tmpBox, tmpArea );
			// printf( "obbb2_%u = [ %f, %f , %f, %f , %f, %f, %f, %f ]\n", i, tmpBox[0][0], tmpBox[0][1], tmpBox[1][0], tmpBox[1][1], tmpBox[2][0], tmpBox[2][1], tmpBox[3][0], tmpBox[3][1] );

			if ( tmpArea < minArea ) {
				minArea = tmpArea;
				memcpy( pOOBB, tmpBox, 4 * sizeof( Vector2<> ) );
			}
		}
	}

	inline void ObjectOrientedBoundingBox::GetOrientedEdges( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( pointCount ) Vector2<>* pEdges ) {
		for ( uint i = 0; i < pointCount - 1; i++ ) {
			pEdges[i] = pConvexHull[i + 1] - pConvexHull[i];
			pEdges[i].Normalize();
		}

		pEdges[pointCount - 1] = pConvexHull[0] - pConvexHull[pointCount - 1];
		pEdges[pointCount - 1].Normalize();
	}

	inline void ObjectOrientedBoundingBox::GetExtremePointIndices( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) int* pIndices ) {
		Vector2<> maxPt( { -FLT_MAX, -FLT_MAX } );
		Vector2<> minPt( { FLT_MAX, FLT_MAX } );

		for ( int i = 0; i < (int)pointCount; i++ ) {
			const Vector2<>& pt = pConvexHull[i];
			if ( pt[0] < minPt[0] ) {
				minPt[0] = pt[0];
				pIndices[SIDE_INDICES::LEFT] = i;
			}

			if ( pt[0] > maxPt[0] ) {
				maxPt[0] = pt[0];
				pIndices[SIDE_INDICES::RIGHT] = i;
			}

			if ( pt[1] < minPt[1] ) {
				minPt[1] = pt[1];
				pIndices[SIDE_INDICES::BOTTOM] = i;
			}

			if ( pt[1] > maxPt[1] ) {
				maxPt[1] = pt[1];
				pIndices[SIDE_INDICES::TOP] = i;
			}
		}
	}

	inline void ObjectOrientedBoundingBox::GetBox( __in_ecount( 2 ) const Vector2<>* pCaliperDirs, __in_ecount( 4 ) const int* pEdgeIndices, __in const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pBox, __out float& area ) {
		pBox[SIDE_INDICES::LEFT] = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::LEFT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::TOP]] );
		pBox[SIDE_INDICES::BOTTOM] = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::LEFT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::BOTTOM]] );
		pBox[SIDE_INDICES::RIGHT] = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::RIGHT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::BOTTOM]] );
		pBox[SIDE_INDICES::TOP] = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::RIGHT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::TOP]] );

		area = pBox[SIDE_INDICES::LEFT].Distance( pBox[SIDE_INDICES::BOTTOM] ) * pBox[SIDE_INDICES::LEFT].Distance( pBox[SIDE_INDICES::TOP] );
	}

	// -------------------------------
	//	Prototype
	// -------------------------------
	void ObjectOrientedBoundingBox::GetProto( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pOOBB ) {
		Buffer< Vector2<> > edges( pointCount );
		GetOrientedEdges( pointCount, pConvexHull, edges.Ptr() );

		int edgeIndices[4];
		GetExtremePointIndices( pointCount, pConvexHull, edgeIndices );

		Vector2<> caliperDirs[4] = {
			Vector2<>( { 0, -1 } ),
			Vector2<>( { 1, 0 } ),
			Vector2<>( { 0, 1 } ),
			Vector2<>( { -1, 0 } ),
		};

		float maxArea = FLT_MAX;

		for ( uint i = 0; i < pointCount; i++ ) {
			float angles[4] = {
				caliperDirs[SIDE_INDICES::LEFT] * edges[edgeIndices[SIDE_INDICES::LEFT]]	,
				caliperDirs[SIDE_INDICES::BOTTOM] * edges[edgeIndices[SIDE_INDICES::BOTTOM]],
				caliperDirs[SIDE_INDICES::RIGHT] * edges[edgeIndices[SIDE_INDICES::RIGHT]]	,
				caliperDirs[SIDE_INDICES::TOP] * edges[edgeIndices[SIDE_INDICES::TOP]]		,
			};

			uint minAngleIx = 0;
			for ( uint j = 1; j < 4; j++ ) {
				if ( angles[j] * angles[j] > angles[minAngleIx] * angles[minAngleIx] ) {
					minAngleIx = j;
				}
			}

			caliperDirs[minAngleIx] = edges[edgeIndices[minAngleIx]];
			caliperDirs[( minAngleIx + 1 ) % 4] = GetOrthogonal( caliperDirs[minAngleIx] );
			caliperDirs[( minAngleIx + 2 ) % 4] = -caliperDirs[minAngleIx];
			caliperDirs[( minAngleIx + 3 ) % 4] = -GetOrthogonal( caliperDirs[minAngleIx] );
			
			edgeIndices[minAngleIx] = ( edgeIndices[minAngleIx] + 1 ) % pointCount;

			Vector2<> box[4];
			float area = 0;
			GetBox( caliperDirs, edgeIndices, pConvexHull, box, area );

			// printf( "obbb%u = [ %f, %f , %f, %f , %f, %f, %f, %f ]\n", i, box[0][0], box[0][1], box[1][0], box[1][1], box[2][0], box[2][1], box[3][0], box[3][1] );

			if ( area < maxArea ) {
				maxArea = area;
				memcpy( pOOBB, box, 4 * sizeof( Vector2<> ) );
			}
		}
	}

	void ObjectOrientedBoundingBox::GetBoxProto( __in_ecount( 4 ) const Vector2<>* pCaliperDirs, __in_ecount( 4 ) const int* pEdgeIndices, __in const Vector2<>* pConvexHull, __out_ecount( 4 ) Vector2<>* pBox, __out float& area )	{
		Vector2<> ptUpLeft = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::LEFT]], pCaliperDirs[SIDE_INDICES::TOP], pConvexHull[pEdgeIndices[SIDE_INDICES::TOP]] );
		Vector2<> ptUpRight = IntersectLines( pCaliperDirs[SIDE_INDICES::RIGHT], pConvexHull[pEdgeIndices[SIDE_INDICES::RIGHT]], pCaliperDirs[SIDE_INDICES::TOP], pConvexHull[pEdgeIndices[SIDE_INDICES::TOP]] );
		Vector2<> ptBotLeft = IntersectLines( pCaliperDirs[SIDE_INDICES::LEFT], pConvexHull[pEdgeIndices[SIDE_INDICES::LEFT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::BOTTOM]] );
		Vector2<> ptBotRight = IntersectLines( pCaliperDirs[SIDE_INDICES::RIGHT], pConvexHull[pEdgeIndices[SIDE_INDICES::RIGHT]], pCaliperDirs[SIDE_INDICES::BOTTOM], pConvexHull[pEdgeIndices[SIDE_INDICES::BOTTOM]] );

		float sideLength = ptUpLeft.Distance( ptBotLeft );
		float baseLength = ptUpLeft.Distance( ptUpRight );

		area = sideLength * baseLength;
		pBox[SIDE_INDICES::LEFT] = ptUpLeft;
		pBox[SIDE_INDICES::BOTTOM] = ptBotLeft;
		pBox[SIDE_INDICES::RIGHT] = ptBotRight;
		pBox[SIDE_INDICES::TOP] = ptUpRight;
	}

}
