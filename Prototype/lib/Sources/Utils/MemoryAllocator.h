//
//  MemoryAllocator.h
//  Utils
//
//  Created by Filip Kovac on 07/10/2016.
//  Copyright © 2016 Filip Kovac. All rights reserved.
//

#pragma once

#include <stdlib.h>
#include "Exception.h"

namespace NumericOptimization { namespace Utils {

	namespace Internal {

	#pragma push_macro("new")
	#pragma push_macro("delete")

	#undef new
	#undef delete

	template < typename T > class MemoryAllocatorImplementation {
	private:
		struct AllocationHelper {
			T o;

			void* operator new ( size_t size )
			{
				return malloc ( size );
			}

			void* operator new[]( size_t size )
			{
				return malloc ( size );
			}

			void operator delete ( void *ptr )
			{
				free ( ptr );
			}

			void operator delete[]( void *ptr )
			{
				free ( ptr );
			}
		};

	public:

		static T* Allocate ( size_t size )
		{
			T* pMem = (T*)( new AllocationHelper[size] );
			if ( !pMem ) {
				throw Exceptions::OutOfMemoryException( size * sizeof( T ) );
			}

			return pMem;
		};

		static T* AllocateItem ()
		{
			T* pMem = (T*)( new AllocationHelper );
			if ( !pMem ) {
				throw Exceptions::OutOfMemoryException( sizeof( T ) );
			}

			return pMem;
		}

		static void Release ( T* buffer )
		{
			delete[] ( AllocationHelper * )( buffer );
		}

		static void ReleaseItem ( T* pItem )
		{
			delete (AllocationHelper *)( pItem );
		}

	};

	#pragma pop_macro("new")
	#pragma pop_macro("delete")

	}

	template < typename T > class MemoryAllocator : public Internal::MemoryAllocatorImplementation< T > {};
} }
