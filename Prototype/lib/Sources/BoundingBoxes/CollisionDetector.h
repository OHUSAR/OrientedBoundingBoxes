#pragma once
#pragma once

namespace BoundingBoxes { namespace Collisions {

	struct CollisionObject {
		uint vertexCount;
		Vector2<>* pVertices;
		Vector2<>* pEdgeNormals;
	};

	class CollisionDetector
	{
	public:

		void GetEdgeNormals( __inout CollisionObject& obj ) const {
			const uint lastVertIx = obj.vertexCount - 1;
			for ( uint i = 0; i < lastVertIx; i++ ) {
				obj.pEdgeNormals[i] = GetOrthogonal( (Vector2<>)(obj.pVertices[i + 1] - obj.pVertices[i]) );
				obj.pEdgeNormals[i].Normalize();
			}

			obj.pEdgeNormals[lastVertIx] = GetOrthogonal( ( Vector2<> )( obj.pVertices[0] - obj.pVertices[lastVertIx] ) );
			obj.pEdgeNormals[lastVertIx].Normalize();
		}

		bool DetectCollision( __in const CollisionObject& objA, __in const CollisionObject& objB ) const {
			Projection<> projA;
			Projection<> projB;
			for ( uint axisI = 0; axisI < objA.vertexCount; axisI++ ) {
				GetProjection( objA, objA.pEdgeNormals[axisI], projA );
				GetProjection( objB, objA.pEdgeNormals[axisI], projB );

				if ( !projA.Overlaps( projB ) ) {
					return false;
				}
			}

			for ( uint axisI = 0; axisI < objB.vertexCount; axisI++ ) {
				GetProjection( objA, objB.pEdgeNormals[axisI], projA );
				GetProjection( objB, objB.pEdgeNormals[axisI], projB );

				if ( !projA.Overlaps( projB ) ) {
					return false;
				}
			}

			return true;
		}

	protected:

		template < typename Scalar = float >
		struct Projection {
			Scalar minPt;
			Scalar maxPt;

			bool Overlaps( __in  const Projection& other ) const {
				return !( ( other.minPt >= maxPt ) || ( other.maxPt <= minPt ) );
			}
		};

	protected:

		void GetProjection( __in const CollisionObject& obj, __in const Vector2<>& axis, __out Projection<>& proj ) const {
			proj.minPt = axis * obj.pVertices[0];
			proj.maxPt = proj.minPt;
			for ( uint vertI = 1; vertI < obj.vertexCount; vertI++ ) {
				float dot = axis * obj.pVertices[vertI];
				if ( dot > proj.maxPt ) {
					proj.maxPt = dot;
				} else if ( dot < proj.minPt ) {
					proj.minPt = dot;
				}
			}
		}

	};

} }