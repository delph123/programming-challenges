
#include "SSAssert.h"

#define DBG_MSG_SZ (10*1024)
char debug_msg_buf[DBG_MSG_SZ];
char assert_buf[DBG_MSG_SZ];

#ifdef DEBUG_OUTPUT
#include <fstream>
std::ofstream debug_file;
#endif

void InitLog( const char* exename )
{
#	ifdef DEBUG_OUTPUT
	debug_file.open( ( std::string( exename ) + "_log.txt" ).c_str() );
#	endif
}

void DbgMessage( const char* p_msg, ... )
{	
#	ifdef DEBUG_OUTPUT
	va_list arglist;
    va_start( arglist, p_msg );
    vsnprintf(debug_msg_buf, DBG_MSG_SZ, p_msg, arglist );
    va_end( arglist );
	debug_file << "Comment([[" << debug_msg_buf << "]])\n";
	debug_file.flush();
#	endif
}

void DbgMessageType( const char* p_type, const char* p_msg, ... )
{	
#	ifdef DEBUG_OUTPUT
	va_list arglist;
    va_start( arglist, p_msg );
    vsnprintf(debug_msg_buf, DBG_MSG_SZ, p_msg, arglist );
    va_end( arglist );
	debug_file << p_type << "(" << debug_msg_buf << ")\n";
	debug_file.flush();
#	endif
}

void AssertTrap( const char* p_msg, const char* p_file, int line, const char* p_func )
{
#	ifdef DEBUG_OUTPUT
	DbgMessage( "Assert: %s (%d:%s)", p_msg, line, p_file );
	_exit( 1 );
#	endif
}
