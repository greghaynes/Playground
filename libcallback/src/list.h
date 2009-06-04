#ifndef CBACK_LIST_H
#define CBACK_LIST_H

/*
 * This is used  to allow for generic list operation functions.
 */
struct DoublyList
{
	struct DoublyList *next;
	struct DoublyList *prev;
};

/**
 * Will set node pointers to point to node.
 */
void doubly_list_init( struct DoublyList *node );

/**
 * Removes node from the chain it is in.
 */
void doubly_list_unlink( struct DoublyList *node );

/**
 * Insert node into chain after the node chain.
 * Node will be unlinked before being inserted.
 */
void doubly_list_insert_after( struct DoublyList *chain,
	struct DoublyList *node );

void doubly_list_foreach( struct DoublyList *chain,
	void(*handler)(struct DoublyList*) );

#endif

