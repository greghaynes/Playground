#include "callback.h"

#include <stdio.h>

void say_hello( void *sender,
	unsigned int n_params,
	const struct CBackParam *params,
	void *user_data )
{
	printf( "Hello, world!\n" );
	fflush(stdout);
}

int main( int argc, char **argv )
{
	CBackSenderKey *sender;
	CBackHandlerKey *handler;

	cback_init();
	sender = cback_sender_new( NULL );
	handler = cback_handler_connect( sender,
		say_hello,
		NULL, NULL );
	cback_sender_emit( sender, 0, NULL );
	cback_deinit();
	return 0;
}

