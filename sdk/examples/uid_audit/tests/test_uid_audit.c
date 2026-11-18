/* 模块单测：由 `ksuhook dev` 编译运行。
 *
 * 这里只验证载荷自己的逻辑，不需要内核，也不需要编整颗 GKI。
 */

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <linux/sched.h>
#include <linux/uidgid.h>

#include "uid_audit.h"

void ksuhook_test_log(const char *fmt, ...);

#define MAX_LOGS 32
static char logs[MAX_LOGS][256];
static int log_count;

void ksuhook_test_log(const char *fmt, ...)
{
    va_list ap;
    if (log_count >= MAX_LOGS)
        return;
    va_start(ap, fmt);
    vsnprintf(logs[log_count], sizeof(logs[0]), fmt, ap);
    va_end(ap);
    log_count++;
}

static struct task_struct test_current = {.pid = 4242, .tgid = 4242};
struct task_struct *ksuhook_current = &test_current;

static int failures;

#define CHECK(cond, msg)                                                                           \
    do {                                                                                           \
        if (!(cond)) {                                                                             \
            fprintf(stderr, "FAIL: %s\n", msg);                                                    \
            failures++;                                                                            \
        }                                                                                          \
    } while (0)

int main(void)
{
    /* 相同 uid：不记录 */
    CHECK(uid_audit_on_setresuid(1000, 1000) == 0, "returns 0 as pass-through");
    CHECK(log_count == 0, "no log when uid unchanged");

    /* uid 变化：记录一次 */
    CHECK(uid_audit_on_setresuid(1000, 2000) == 0, "still returns 0");
    CHECK(log_count == 1, "one log after uid change");
    CHECK(strstr(logs[0], "1000 -> 2000") != NULL, "log contains both uids");

    /* 再变一次：累计计数递增 */
    uid_audit_on_setresuid(2000, 0);
    CHECK(log_count == 2, "second change logged");
    CHECK(strstr(logs[1], "total 2") != NULL, "counter accumulates");

    if (failures) {
        fprintf(stderr, "%d check(s) failed\n", failures);
        return 1;
    }
    printf("uid_audit: all checks passed\n");
    return 0;
}
