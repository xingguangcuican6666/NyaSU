#ifndef _LINUX_ATOMIC_H
#define _LINUX_ATOMIC_H
/* devkit 替身：单线程单测下用普通变量即可。 */
#include <linux/types.h>

typedef struct { long counter; } atomic_long_t;
typedef struct { int counter; } atomic_t;

#define atomic_long_inc(a) (__atomic_add_fetch(&(a)->counter, 1, __ATOMIC_RELAXED))
#define atomic_long_read(a) (__atomic_load_n(&(a)->counter, __ATOMIC_RELAXED))
#define atomic_inc(a) (__atomic_add_fetch(&(a)->counter, 1, __ATOMIC_RELAXED))
#define atomic_read(a) (__atomic_load_n(&(a)->counter, __ATOMIC_RELAXED))

#endif
