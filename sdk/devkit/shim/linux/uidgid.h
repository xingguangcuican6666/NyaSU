#ifndef _LINUX_UIDGID_H
#define _LINUX_UIDGID_H
/* devkit 替身 */
#include <linux/types.h>

typedef unsigned int uid_t;
typedef unsigned int gid_t;
typedef struct { uid_t val; } kuid_t;

#define GLOBAL_ROOT_UID ((uid_t)0)

static inline uid_t __kuid_val(kuid_t uid) { return uid.val; }

#endif
