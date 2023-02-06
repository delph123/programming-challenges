#ifndef __ASSERT_H
#define __ASSERT_H

#define CTAssert( _condition ) { char error[(_condition)?1:-1]; error[0] = 0; }

extern char assert_buf[];
void AssertTrap( const char* p_msg, const char* p_file, int line, const char* p_func );

void InitLog( const char* exename );

#define Assert( _x ) \
	if( !( _x ) ) \
	{ \
		AssertTrap( #_x, __FILE__, __LINE__, __PRETTY_FUNCTION__ ); \
	}

#define MsgAssert( _x, ... ) \
	if( !( _x ) ) \
	{ \
		sprintf( assert_buf, __VA_ARGS__ ); \
		AssertTrap( assert_buf, __FILE__, __LINE__, __PRETTY_FUNCTION__ ); \
	}
	
void DbgMessage( const char* p_msg, ... );
void DbgMessageType( const char* p_type, const char* p_msg, ... );

#define DUMPB( _f ) DbgMessage( "%s: %s", #_f, _f?"true":"false" );
#define DUMPF( _f ) DbgMessage( "%s: %f", #_f, _f );
#define DUMPS( _f ) DbgMessage( "%s: %s", #_f, _f );
#define DUMPI( _f ) DbgMessage( "%s: %d", #_f, _f );
#define DUMPP( _f ) DbgMessage( "%s: %p", #_f, (void*)_f );
#define DUMPV( _f ) DbgMessage( "%s: (%0.4f, %0.4f)", #_f, _f[0], _f[1] );
#define DEMARK DbgMessage( "%s: %d", __PRETTY_FUNCTION__, __LINE__ );

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#define DbgPush( _x, ... )							DbgMessageType( "Push", #_x, ##__VA_ARGS__ );
#define DbgPop()									DbgMessageType( "Pop", "" );
#define DbgTurn( _x )								DbgMessageType( "StartTurn", "[[%s]]", (_x)->ToString().c_str() );
#define DbgGameState( _x )							DbgMessageType( "AddGameState", "[[%s]]", (_x)->ToString().c_str() );
#define DbgPHighlight( _p, _r, _g, _b )				DbgMessageType( "PlanetHighlight", "%d, %d, %d, %d", _p, _r, _g, _b );
#define DbgPMessage( _p, _r, _g, _b, _x, ... )		DbgMessageType( "PlanetComment", "%d, %d, %d, %d, [[" _x "]]", _p, _r, _g, _b, ##__VA_ARGS__ );
#define DbgPLine( _p1, _p2, _r, _g, _b )			DbgMessageType( "PlanetLine", "%d, %d, %d, %d, %d", _p1, _p2, _r, _g, _b );
#define DbgLine( _v1, _v2, _r, _g, _b )				DbgMessageType( "Line", "%f, %f, %f, %f, %d, %d, %d", _v1[0], _v1[1], _v2[0], _v2[1], _r, _g, _b );

class CDebugPop
{
	bool pop;
public:
	CDebugPop( bool do_pop )	{ pop = do_pop; }
	~CDebugPop()			{ if( pop ) DbgPop(); }
};

#define DbgScope( _x, ... )							DbgPush( _x, ##__VA_ARGS__ ); CDebugPop __d__( true );
#define DbgScopeB( _cond, _x, ... )					if( (_cond) ) { DbgPush( _x, ##__VA_ARGS__ ); } CDebugPop __d__( (_cond) );

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#endif //__ASSERT_H
