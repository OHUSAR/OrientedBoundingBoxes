#pragma once

#include "stdafxMath.h"
#include "DynamicMatrix.h" 

namespace NumericOptimization { namespace Math { namespace LinearAlgebra {

	// -------------------------------------------------------------------------------------------------------
	//    Unary Operators
	// -------------------------------------------------------------------------------------------------------
	template < typename Scalar >
	inline Matrix<Scalar, MatrixBase::Dynamic> operator- ( __in const Matrix<Scalar, MatrixBase::Dynamic>& A ) {
		Matrix<Scalar, MatrixBase::Dynamic> B( A );
		B *= Scalar( -1 );
		return B;
	};

	// -------------------------------------------------------------------------------------------------------
	//    Scalar Binary Operators
	// -------------------------------------------------------------------------------------------------------

	// -------------------------------------------------------------------------------------------------------
	//    Matrix Binary Operators
	// -------------------------------------------------------------------------------------------------------
	template < typename Scalar >
	inline Matrix<Scalar, MatrixBase::Dynamic> operator+ ( __in const Matrix<Scalar, MatrixBase::Dynamic>& A, __in const Matrix<Scalar, MatrixBase::Dynamic>& B ) {
		if ( !A.HasEqualDimensions( B ) ) {
			throw InvalidDimensionsException( GET_VARIABLE_NAME( B ) );
		}

		Matrix<Scalar, MatrixBase::Dynamic> C( A );
		C += B;
		return C;
	};

	template < typename Scalar >
	inline Matrix<Scalar, MatrixBase::Dynamic> operator- ( __in const Matrix<Scalar, MatrixBase::Dynamic>& A, __in const Matrix<Scalar, MatrixBase::Dynamic>& B ) {
		if ( !A.HasEqualDimensions( B ) ) {
			throw InvalidDimensionsException( GET_VARIABLE_NAME( B ) );
		}

		Matrix<Scalar, MatrixBase::Dynamic> C( A );
		C -= B;
		return C;
	};

	template < typename Scalar >
	inline Matrix<Scalar, MatrixBase::Dynamic> operator* ( __in const Matrix<Scalar, MatrixBase::Dynamic>& A, __in const Matrix<Scalar, MatrixBase::Dynamic>& B ) {

		uint Arows = 0, ACols = 0;
		uint BRows = 0, BCols = 0;

		A.GetDimensions( Arows, ACols );
		B.GetDimensions( BRows, BCols );

		if ( !A.CheckMultiplicationDimensions( B ) ) {
			throw InvalidDimensionsException( BRows, BCols, ACols, BCols );
		}

		Matrix<Scalar, MatrixBase::Dynamic> C( Arows, BCols );

		Scalar* pDst = C.Elements();
		Scalar* pASrc = A.Elements();
		Scalar* pBSrc = B.Elements();

		for ( uint i = 0; i < Arows; i++ ) {
			for ( uint j = 0; j < BCols; j++ ) {
				Scalar tmp = Scalar( 0 );
				for ( uint k = 0; k < ACols; k++ ) {
					tmp += ( *( pASrc + i * ACols + k ) ) * ( *( pBSrc + k * BCols + j ) );
				}
				*( pDst + i * BCols + j ) = tmp;
			}
		}

		return C;
	};

} } }