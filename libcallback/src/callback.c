#include "callback.h"
#include "list.h"

#include <stdlib.h>

typedef struct _CBackSystem CBackSystem;

struct _CBackHandlerKey
{
	struct DoublyList list;
	CBackHandler handler;
	void *user_data;
	CBackHandlerDestroyNotify destroy_notify;
};

struct _CBackSenderKey
{
	struct DoublyList list;
	CBackHandlerKey *handlers;
	void *sender;
};

struct _CBackSystem
{
	CBackSenderKey *senders;
};

CBackSystem *cback_instance()
{
	static CBackSystem *system = 0;
	if( !system )
	{
		system = (CBackSystem*)malloc(sizeof(struct _CBackSystem));
		system->senders = 0;
	}
	return system;
}

void cback_system_insert_sender( CBackSenderKey *ins_sender )
{
	CBackSystem *system = cback_instance();
	CBackSenderKey *sender;
	if( system->senders )
		doubly_list_insert_after( &system->senders->list,
			&ins_sender->list );
	else
		system->senders = ins_sender;
}

CBackHandlerKey *cback_handler_key_new()
{
	CBackHandlerKey *key;
	key = (CBackHandlerKey*)malloc(sizeof(struct _CBackHandlerKey));
	key->handler = 0;
	key->user_data = 0;
	key->destroy_notify = 0;
	doubly_list_init( &key->list );
	return key;
}

void cback_handler_key_free( CBackHandlerKey *handler_node )
{
	// Call the destroy notify
	if( handler_node->destroy_notify )
	{
		handler_node->destroy_notify( handler_node,
			handler_node->user_data );
	}
	free( handler_node );
}

void cback_handler_free_node( struct DoublyList *node )
{
	doubly_list_unlink( node );
	cback_handler_key_free( (CBackHandlerKey*)node );
}

CBackSenderKey *cback_sender_key_new()
{
	CBackSenderKey *key;
	key = (CBackSenderKey*)malloc(sizeof(struct _CBackSenderKey));
	key->handlers = 0;
	key->sender = 0;
	doubly_list_init( &key->list );
	return key;
}

/**
 * The node should already be unlinked when calling
 * this method.
 */
void cback_sender_key_free( CBackSenderKey *node )
{
	if( node->handlers )
		doubly_list_foreach( &node->handlers->list,
			cback_handler_free_node );

	free( node );
}

void cback_sender_free_node( struct DoublyList *node )
{
	doubly_list_unlink( node );
	cback_sender_key_free( (CBackSenderKey*)node );
}

void cback_init()
{
	cback_instance();
}

CBackSenderKey *cback_sender_new( void *sender )
{
	CBackSenderKey *key;
	key = cback_sender_key_new();
	
	cback_system_insert_sender( key );

	key->handlers = 0;
	key->sender = sender;
	
	return key;
}

void cback_sender_delete( CBackSenderKey *sender_key )
{
	doubly_list_unlink( &sender_key->list );
	cback_sender_key_free( sender_key );
}

CBackHandlerKey *cback_handler_connect( CBackSenderKey *sender_key,
	CBackHandler handler,
	void *user_data,
	CBackHandlerDestroyNotify destroy_notify )
{
	CBackHandlerKey *key = cback_handler_key_new();
	key->handler = handler;
	key->user_data = user_data;
	key->destroy_notify = destroy_notify;
	
	if( !sender_key->handlers )
		sender_key->handlers = key;
	else
		doubly_list_insert_after( &sender_key->handlers->list,
			&key->list );
}

void cback_handler_disconnect( CBackHandlerKey *handler_key )
{
	doubly_list_unlink( &handler_key->list );
	cback_handler_key_free( handler_key );
}

int cback_sender_emit( CBackSenderKey *sender_key,
	unsigned int num_params,
	const struct CBackParam *params )
{
	CBackHandlerKey *handler;
	handler = sender_key->handlers;
	if( !handler )
		return;
	do
	{
		handler->handler( sender_key->sender,
			num_params,
			params,
			handler->user_data );
		handler = (CBackHandlerKey*)handler->list.next;
	} while( handler != sender_key->handlers );
	return 0;
}

void cback_deinit()
{
	CBackSystem *system = cback_instance();
	doubly_list_foreach( &system->senders->list,
		cback_sender_free_node );
	free( system );
}

