#ifndef LIST_H
#define LIST_H

#include "list.h"

void doubly_list_init( struct DoublyList *node )
{
	node->next = node;
	node->prev = node;
}

void doubly_list_unlink( struct DoublyList *node )
{
	// Were already unlinked
	if( node->prev == node )
		return;
	// Remove from chain
	node->prev->next = node->next;
	node->next->prev = node->prev;
	// Reset our pointers
	node->next = node;
	node->prev = node;
}

void doubly_list_insert_after( struct DoublyList *chain,
	struct DoublyList *node )
{
	doubly_list_unlink( node );
	node->next = chain->next;
	node->prev = chain;
	chain->next->prev = node;
	chain->next = node;
}

void doubly_list_foreach( struct DoublyList *chain,
	void(*handler)(struct DoublyList*) )
{
	struct DoublyList *itr = chain, *next = chain;
	do
	{
		// Allows for unlinking in handler
		next = itr->next;
		handler( itr );
		itr = next;
	} while( itr != chain );
}

#endif

