#pragma once

#include <string>
#include <sstream>

namespace NumericOptimization { namespace Utils { namespace Exceptions {

	namespace Internal {

		template < typename ... Args >
		std::string StringFormat( __in_z const char* pFormat, Args ... args ) {
			size_t formattedSize = snprintf( nullptr, 0, pFormat, args ... ) + 1;
			char* tmpBuffer = new char[formattedSize];

			snprintf( tmpBuffer, formattedSize, pFormat, args ... );
			std::string result( tmpBuffer, tmpBuffer + formattedSize - 1 );

			delete[] tmpBuffer;
			return result;
		};

	}

	namespace ExceptionReasons {
		static const char* DIMENSIONS_MISMATCH = "Dimensions do not match";
		
		static const char* DIVISION_BY_ZERO = "Division by zero";

		static const char* BAD_LOGARITHM_INPUT = "log' can't be calculated for x <= 0";

		static const char* BAD_SQRT_INPUT = "sqrt' can't be calculated for x < 0";

		static const char* BAD_CBRT_INPUT = "cbrt' can't be calculated for x == 0";

		static const char* LINE_FITTING_NO_INPUT = "There are no points to fit line to";

		static const char* NULLPTR = "Was nullptr";

		static const char* INVALID_FILE = "Invalid filename given";

		static const char* GPU_NOT_SYNCED = "Object data are not synchornized with GPU";

		static const char* MATRIX_SINGULAR = "Is singular or nearly singular";

	};

	class Exception {
	
	public:
	
		Exception() noexcept {};
	
		explicit Exception( __in_z const char* pMessage ) : m_message( pMessage ) {};

		explicit Exception( __in const std::string& message ) : m_message( message ) {};
	
		Exception( __in const Exception& src ) : m_message( src.m_message ) {};
	
		virtual ~Exception() {};
	
	
		Exception& operator= ( __in const Exception& src ) {
			m_message = src.m_message;
		};
	
		virtual const char* what() {
			return m_message.c_str();
		};
	
		virtual std::string& GetErrorMessage() {
			return m_message;
		}
	
	protected:
	
		std::string m_message;
	
	};
	
	
	class IndexOutOfRangeException : public Exception {
	
	public:

		IndexOutOfRangeException() : Exception( "Index is out of range " ) {};
	
		explicit IndexOutOfRangeException( __in const size_t ixActual, __in const size_t ixMax ) :
			Exception( Internal::StringFormat( "Index %zu is out of range. Greatest valid index is %zu", ixActual, ixMax ) ) {};

		explicit IndexOutOfRangeException( __in const unsigned int ixActual, __in const unsigned int ixMax ) :
			Exception( Internal::StringFormat( "Index %u is out of range. Greatest valid index is %u", ixActual, ixMax ) ) {};
	
		explicit IndexOutOfRangeException( __in const int ixActual, __in const int ixMax ) :
			Exception( Internal::StringFormat( "Index %d is out of range. Greatest valid index is %d", ixActual, ixMax ) ) {};
	
		explicit IndexOutOfRangeException( __in const size_t ix1, __in const size_t ix2, __in const size_t ixMax1, __in const size_t ixMax2 ) :
			Exception( Internal::StringFormat( "Index [%zu, %zu] is out of range. Greatest valid index is [%zu, %zu]", ix1, ix2, ixMax1, ixMax2 ) ) {};

		explicit IndexOutOfRangeException( __in const unsigned int ix1, __in const unsigned int ix2, __in const unsigned int ixMax1, __in const unsigned int ixMax2 ) :
			Exception( Internal::StringFormat( "Index [%u, %u] is out of range. Greatest valid index is [%u, %u]", ix1, ix2, ixMax1, ixMax2 ) ) {};
	
		explicit IndexOutOfRangeException( __in const int ix1, __in const int ix2, __in const int ixMax1, __in const int ixMax2 ) :
			Exception( Internal::StringFormat( "Index [%d, %d] is out of range. Greatest valid index is [%d, %d]", ix1, ix2, ixMax1, ixMax2 ) ) {};
	
	};
	
	
	class OutOfMemoryException : public Exception {
	
	public:
	
		OutOfMemoryException() : Exception( "Application ran out of memory" ) {};
	
		explicit OutOfMemoryException( __in const size_t byteCount ) :
			Exception( Internal::StringFormat( "Application ran out of memory while allocating %u Bytes", byteCount ) ) {};
	
	};

	class InvalidArgumentException : public Exception {
		
	public:

		InvalidArgumentException() : Exception( "One or more argumets are invalid" ) {};

		explicit InvalidArgumentException( __in_z const char* pVarString ) :
			Exception( Internal::StringFormat( "Argument [%s] is invalid", pVarString ) ) {};

		explicit InvalidArgumentException( __in_z const char* pVarString, __in_z const char* pReason ) :
			Exception( Internal::StringFormat( "Argument [%s] is invalid. Reason: %s", pVarString, pReason ) ) {};

		template < typename T >
		explicit InvalidArgumentException( __in_z const char *pVarString, __in T* pVal ) {
			std::stringstream stream;
			stream.sync_with_stdio( false );

			stream << "Argument [" << typeid( T ).name() << " " << pVarString;
			if ( pVal ) {
				stream << " = " << *pVal;
			}
			stream << " (at 0x" << pVal << ") ] is invalid";
			m_message = stream.str();
		}

	};

	class InvalidDimensionsException : public Exception {

	public:

		InvalidDimensionsException() : Exception( "Dimensions are invalid" ) {};

		explicit InvalidDimensionsException( __in const size_t actualX, __in const size_t actualY, __in const size_t expectedX, __in const size_t expectedY ) :
			Exception( Internal::StringFormat( "Dimensions [%u, %u] are invalid, expected [%u, %u]", actualX, actualY, expectedX, expectedY ) ) {};

		explicit InvalidDimensionsException( __in_z const char* pVarString, __in const size_t actualX, __in const size_t actualY, __in const size_t expectedX, __in const size_t expectedY ) :
			Exception( Internal::StringFormat( "%s has invalid dimensions [%u, %u], expected [%u, %u]", pVarString, actualX, actualY, expectedX, expectedY ) ) {};

		explicit InvalidDimensionsException( __in_z const char* pVarString ) :
			Exception( Internal::StringFormat( "%s has invalid dimensions", pVarString ) ) {};

	};

	class WrongStateException : public Exception {
		
	public:

		WrongStateException() : Exception( "Object is in wrong state" ) {};

		explicit WrongStateException( __in const char* pVarString ) :
			Exception( Internal::StringFormat( "%s is in wrong state", pVarString ) ) {};

		explicit WrongStateException( __in const char* pVarString, __in const char* pReasonStr ) :
			Exception( Internal::StringFormat( "%s is in wrong state. Reason: %s", pVarString, pReasonStr ) ) {};

		template < typename T >
		explicit WrongStateException( __in T* pVar, __in const char* pVarString ) :
			Exception( Internal::StringFormat( "%s %s is in wrong state", typeid(T).name(), pVarString ) ) 
		{
			UNREFERENCED_PARAMETER( pVar );
		};

		template < typename T >
		explicit WrongStateException( __in T* pVar, __in const char* pVarString, __in const char* pReasonStr ) :
			Exception( Internal::StringFormat( "Object is in wrong state\nType:%s\nVariable name:%s\nReason: %s", typeid( T ).name(), pVarString, pReasonStr ) ) 
		{
			UNREFERENCED_PARAMETER( pVar );
		};

	};

} } }