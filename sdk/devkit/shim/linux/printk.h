#ifndef _LINUX_PRINTK_H
#define _LINUX_PRINTK_H
/* devkit 替身：把内核日志转成单测可断言的记录函数。 */

void ksuhook_test_log(const char *fmt, ...) __attribute__((format(printf, 1, 2)));
#define pr_info(fmt, ...) ksuhook_test_log(fmt, ##__VA_ARGS__)
#define pr_err(fmt, ...) ksuhook_test_log(fmt, ##__VA_ARGS__)
#define pr_warn(fmt, ...) ksuhook_test_log(fmt, ##__VA_ARGS__)
#define pr_debug(fmt, ...) ksuhook_test_log(fmt, ##__VA_ARGS__)

#endif
