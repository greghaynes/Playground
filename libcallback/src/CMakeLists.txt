project(libcallback)

set(callback_SRCS
	callback.c
	list.c)

set(callback_HDRS
	callback.h
	list.h)

add_library(callback SHARED ${callback_SRCS})

set_target_properties(callback
	PROPERTIES
	VERSION 0.1
	SOVERSION 1)

install(TARGETS callback
	DESTINATION lib)

INSTALL(FILES ${callback_HDRS}
	DESTINATION include/libcallback-1.0/libcallback)

