//
//  Buffer.h
//  Utils
//
//  Created by Filip Kovac on 19/10/2016.
//  Copyright © 2016 Filip Kovac. All rights reserved.
//

#pragma once

#include "stdafx.h"

namespace NumericOptimization { namespace Utils {

	/*
		Basic static array wrapper class ( no run-time index guarding, for performance sake )
	*/
	template < class T, class Allocator = MemoryAllocator<T> > class Buffer {
	public:

		Buffer() {
			m_size = 0;
			m_pItems = nullptr;
		};

		Buffer( __in const size_t length ) {
			m_pItems = nullptr;
			Allocate( length );
		};

		Buffer( __in const Buffer<T>& other ) {
			m_size = other.m_size;
			m_pItems = nullptr;

			Allocate( m_size );
			ShallowCopy<T>( other.m_pItems, m_size, m_pItems );
		};

		~Buffer() {
			if ( m_pItems != nullptr ) {
				Allocator::Release( m_pItems );
			}
		};

		/*
			Allocates array of given size
		*/
		void Allocate( __in const size_t length ) {
			T *temp = m_pItems;
			if ( temp != nullptr )
			{
				Allocator::Release( temp );
			}

			m_pItems = Allocator::Allocate( length );
			m_size = length;
		}

		void Set( __in const size_t count, __in_ecount( count ) const T *pSrc ) {
			if ( pSrc == nullptr ) {
				throw InvalidArgumentException<T>( GET_VARIABLE_NAME( pSrc ) );
			}

			Allocate( count );
			ShallowCopy<T>( pSrc, count, m_pItems );
		}

		void Set( __in const Buffer<T> &src ) {
			Set( src.Length(), src.Ptr() );
		}

		void Fill( __in const T val ) {
			T *pDst = m_pItems;
			for ( size_t i = 0; i < m_size; i++ ) {
				*pDst = val;
				pDst++;
			}
		}

		inline T* Ptr() const { 
			return m_pItems; 
		}

		inline size_t Length() const { 
			return m_size; 
		}

		T& operator[] ( size_t pos ) const {
			_ASSERT_EXPR( pos < m_size, L"Index is out of range" );
			return *( m_pItems + pos );
		}

	protected:

		size_t	m_size;
		T*		m_pItems;

	};

} }