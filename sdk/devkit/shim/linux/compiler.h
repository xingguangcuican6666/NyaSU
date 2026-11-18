#ifndef _LINUX_COMPILER_H
#define _LINUX_COMPILER_H
/* devkit 替身 */
#define __init
#define __exit
#define __user
#define __kernel
#define __always_inline inline __attribute__((always_inline))
#define likely(x) __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)

#endif
