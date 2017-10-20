#include "stdafx.h"
#include "BasicDefs.h"
#include "AxisAlignedBoundingBox.h"

namespace BoundingBoxes {

	void AxisAlignedBoundingBox::Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pPoints, __out_ecount( 2 ) Vector2<>* pAABB ) {
		pAABB[AABB_VERTEX_INDICES::MIN_PT][0] = FLT_MAX;
		pAABB[AABB_VERTEX_INDICES::MIN_PT][1] = FLT_MAX;
		
		pAABB[AABB_VERTEX_INDICES::MAX_PT][0] = -FLT_MAX;
		pAABB[AABB_VERTEX_INDICES::MAX_PT][1] = -FLT_MAX;

		for ( uint i = 0; i < pointCount; i++ )
		{
			const Vector2<>& pt = pPoints[i];
			if ( pt[0] > pAABB[AABB_VERTEX_INDICES::MAX_PT][0] ) {
				pAABB[AABB_VERTEX_INDICES::MAX_PT][0] = pt[0];
			}

			if ( pt[0] < pAABB[AABB_VERTEX_INDICES::MIN_PT][0] ) {
				pAABB[AABB_VERTEX_INDICES::MIN_PT][0] = pt[0];
			}

			if ( pt[1] > pAABB[AABB_VERTEX_INDICES::MAX_PT][1] ) {
				pAABB[AABB_VERTEX_INDICES::MAX_PT][1] = pt[1];
			}

			if ( pt[1] < pAABB[AABB_VERTEX_INDICES::MIN_PT][1] ) {
				pAABB[AABB_VERTEX_INDICES::MIN_PT][1] = pt[1];
			}
		}
	}

}