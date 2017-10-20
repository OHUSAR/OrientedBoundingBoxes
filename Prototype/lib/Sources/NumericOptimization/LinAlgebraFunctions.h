#pragma once

namespace NumericOptimization { namespace Math { namespace LinearAlgebra {

	template < typename Scalar >
	Vector< Scalar, 2 > GetOrthogonal( __in const Vector< Scalar, 2 >& A ) {
		return Vector< Scalar, 2 >( { A[1], -A[0] } );
	};

	template < typename Scalar >
	Vector< Scalar, 2 > IntersectLines( 
		__in const Vector< Scalar, 2 >& dirA, 
		__in const Vector< Scalar, 2 >& ptA, 
		__in const Vector< Scalar, 2 >& dirB,
		__in const Vector< Scalar, 2 >& ptB 
	) {
		Vector< Scalar, 2> ptA2 = ptA + dirA;
		Vector< Scalar, 2> ptB2 = ptB + dirB;

		float dxA = ptA[0] - ptA2[0];
		float dxB = ptB[0] - ptB2[0];
		float dyA = ptA[1] - ptA2[1];
		float dyB = ptB[1] - ptB2[1];

		float det = ( dxA ) * ( dyB ) - ( dyA ) * ( dxB );
		if ( det != 0 ) {
			float fctA = ptA[0] * ptA2[1] - ptA[1] * ptA2[0];
			float fctB = ptB[0] * ptB2[1] - ptB[1] * ptB2[0];

			return Vector2<>( {
				( ( fctA ) * ( dxB ) - ( dxA ) * ( fctB ) ) / det,
				( ( fctA ) * ( dyB ) - ( dyA ) * ( fctB ) ) / det,
			} );
		}

		throw InvalidArgumentException( GET_VARIABLE_NAME( dirA ), "Lines are parallel" );
	}

} } }
