/* UID Audit 载荷：只观察，不改行为。
 *
 * 签名与 ksu_handle_setresuid(uid_t old_uid, uid_t new_uid) 一致，返回 int。
 * 返回 0 表示"没有意见"：ksuhook 生成的包装会继续执行原函数。
 */

#include <linux/atomic.h>
#include <linux/printk.h>
#include <linux/sched.h>
#include <linux/types.h>
#include <linux/uidgid.h>

#include "uid_audit.h"

static atomic_long_t uid_audit_changes;

int uid_audit_on_setresuid(uid_t old_uid, uid_t new_uid)
{
    long total;

    if (old_uid == new_uid)
        return 0;

    total = atomic_long_inc(&uid_audit_changes);
    pr_info("uid_audit: %u -> %u (total %ld)\n", old_uid, new_uid, total);
    return 0;
}
