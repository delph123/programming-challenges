#ifndef __MATHUTIL_H
#define __MATHUTIL_H

// math lib configuration
#define CML_NO_DEFAULT_EXPR_TRAITS
#define CML_VECTOR_UNROLL_LIMIT 25
#define CML_VECTOR_DOT_UNROLL_LIMIT 25
#define CML_NO_2D_UNROLLER
#define CML_DEFAULT_ARRAY_LAYOUT cml::row_major
#define CML_ALWAYS_PROMOTE_TO_DEFAULT_LAYOUT
#define CML_DEFAULT_ARRAY_ALLOC std::allocator<void>
//#define CML_AUTOMATIC_VECTOR_RESIZE_ON_ASSIGNMENT
#define CML_CHECK_VECTOR_EXPR_SIZES
//#define CML_AUTOMATIC_MATRIX_RESIZE_ON_ASSIGNMENT
#define CML_CHECK_MATRIX_EXPR_SIZES

#include <stdlib.h>
#include <stdexcept>
#include <ostream>
#include "cml\cml_cml.h"

using namespace cml;

inline float DegToRad( float angle )
{
	return ( angle / 180.0f ) * constants<float>::pi();
}

inline float RadToDeg( float angle )
{
	return ( angle / constants<float>::pi() ) * 180.0f;
}

inline float ModAngle( float angle )
{
	while ( angle >= constants<float>::two_pi() )
	{
		angle -= constants<float>::two_pi();
	}
	
	while ( angle < 0.0f )
	{
		angle += constants<float>::two_pi();
	}
	
	return angle;
}

template< typename T >
void Swap( T& a, T& b )
{
	T temp = a;
	a = b;
	b = temp;
}

template< typename T >
bool Between( const T val, const T min, const T max )
{
	return ( val >= min && val <= max );
}

template< typename T >
bool Near( const T a, const T b, const T epsilon = (T)0.00001 )
{
	return ( Abs( a-b ) < epsilon );
}

template< typename T >
T Clamp( const T val, const T& min, const T& max )
{
	if( val > max )
	{
		return max;
	}
	
	if( val < min )
	{
		return min;
	}
	
	return val;
}

template< typename T >
T Max( const T a, const T b )
{
	if( a > b )
	{
		return a;
	}
	else
	{
		return b;
	}
}


template< typename T >
T Min( const T a, const T b )
{
	if( a > b )
	{
		return b;
	}
	else
	{
		return a;
	}
}

template< typename T >
T Min( const T a, const T b, const T c )
{
	return Min( Min( a, b ), c );
}

template< typename T >
T Max( const T a, const T b, const T c )
{
	return Max( Max( a, b ), c );
}

template< typename T >
T Abs( const T val )
{
	if( val < (T)0 )
	{
		return -val;
	}
	else
	{
		return val;
	}
}

template< typename T >
T Sgn( const T val )
{
	if( val < (T)0 )
	{
		return (T)-1;
	}
	else
	{
		return (T)1;
	}
}

template< typename t_Output, typename t_Input >
t_Output LinearMap( const t_Output& a, const t_Output& b, const t_Input& value, const t_Input& min, const t_Input& max )
{
	return ( ( ( value - min ) / ( max - min ) ) * ( b - a ) ) + a;
}

template< typename t_Output, typename t_Input >
t_Output LinearMapClamp( const t_Output& a, const t_Output& b, const t_Input& value, const t_Input& min, const t_Input& max )
{
	return Clamp( LinearMap( a, b, value, min, max ), Min( a, b ), Max( a, b ) );
}

template< typename T >
T Lerp ( const T& a, const T& b, float t )
{
	return ( b * t ) + ( a * ( 1.0f - t ) );
}

#endif // __MATHUTIL_H

