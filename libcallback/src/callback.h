#ifndef CBACK_H
#define CBACK_H

typedef struct _CBackSenderKey CBackSenderKey;
typedef struct _CBackHandlerKey CBackHandlerKey;

enum CBackParamType
{
	CBACK_PARAM_VOIDP,
	CBACK_PARAM_STRING,
	CBACK_PARAM_CHAR,
	CBACK_PARAM_INT,
	CBACK_PARAM_UINT,
	CBACK_PARAM_LONGNUM
};

typedef union CBackParamValue
{
	void *ptr;
	char *str;
	char ch;
	int num;
	unsigned int unum;
	long longnum;
} CBackParamValue_t;

struct CBackParam
{
	const char *name;
	int type;
	CBackParamValue_t value;
};

/**
 * @brief Callback handler
 */
typedef void (*CBackHandler)( void *sender,
	unsigned int num_params,
	const struct CBackParam *params,
	void *user_data );
/**
 * @brief Callback for notification of a destroyed handler key
 */
typedef (*CBackHandlerDestroyNotify)( CBackHandlerKey *handler_key,
	void *user_data );

/**
 * @brief Call this before using the signal system.
 */
void cback_init();

/**
 * @brief Create a new sender which cann be emitted by sender.
 * @param sender Instance sending the signal.
 * @param num_params Number of parameters sent to signal handlers.
 * @param param_types Array of param_types, num_params long.
 * @return SenderKey used to emit the signal.  Do not free this.
 *
 * You can create multiple senders per unique passed sender value,
 * this is only used as a param passed to all connected handlerst
 */
CBackSenderKey *cback_sender_new( void *sender );

/**
 * @brief Delete a sender.
 * 
 * This will free all CBackHandlerKey's, so make sure handlers
 * with no destroy_notify handlers no longer have references to
 * thier handler keys.
 */
void cback_sender_delete( CBackSenderKey *sender_key );

/**
 * @brief Connect handler to signal.
 *
 * The returned CBackHandlerKey is used to disconnect
 * the callback.  The destroy_notify is used to notify the
 * owner of the CBackHandlerKey when it has been deleted
 * by a call to cback_sender_free.
 */
CBackHandlerKey *cback_handler_connect( CBackSenderKey *sender_key,
	CBackHandler handler,
	void *user_data,
	CBackHandlerDestroyNotify destry_notify );

/**
 * @brief Disconnect handler.
 *
 * This will free the handler_key as well as cause the
 * callback to no longer be called.  The destroy_notify
 * will be called before the handler_key is free'd.
 */
void cback_handler_disconnect( CBackHandlerKey *handler_key );

/**
 * @brief emit signal
 */ 
int cback_sender_emit( CBackSenderKey *sender_key,
	unsigned int num_params,
	const struct CBackParam *params );

/**
 * @bref Call this to free signal system.
 *
 * All CBackSenderKey structs will become invalid after calling this.
 */
void cback_deinit();

#endif

