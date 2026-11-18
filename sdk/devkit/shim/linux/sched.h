#ifndef _LINUX_SCHED_H
#define _LINUX_SCHED_H
/* devkit 替身：只提供模块常用的字段，其余请在模块 tests/ 里桩接。 */
#include <linux/types.h>
#include <linux/uidgid.h>

struct task_struct {
    int pid;
    int tgid;
    uid_t uid;
    uid_t euid;
};

extern struct task_struct *ksuhook_current;
#define current ksuhook_current

#endif
