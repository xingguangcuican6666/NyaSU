#ifndef UID_AUDIT_H
#define UID_AUDIT_H

#include <linux/uidgid.h>

/* hooks.toml 里声明的 entry；单独成头文件，便于 tests/ 直接 include。 */
int uid_audit_on_setresuid(uid_t old_uid, uid_t new_uid);

#endif
