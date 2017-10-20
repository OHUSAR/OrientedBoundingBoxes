#pragma once

namespace BoundingBoxes {

	class AxisAlignedBoundingBox
	{
	public:
		static void Get( __in const uint pointCount, __in_ecount( pointCount ) const Vector2<>* pPoints, __out_ecount( 4 ) Vector2<>* pAABB );

	protected:

		enum AABB_VERTEX_INDICES {
			MIN_PT = 0,
			MAX_PT = 1
		};

	};

}