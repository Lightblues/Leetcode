#include <stdio.h>
#include <malloc.h>

#include <sched.h>
#include <signal.h>

#include <sys/types.h>
#include <unistd.h>

#define FIBER_STACK 8192
int a;
void *stack;

/*
int clone(int (fn)(void ), void *child_stack, int flags, void *arg);

下面的例子是创建一个线程（子进程共享了父进程虚存空间，没有自己独立的虚存空间不能称其为进程）。父进程被挂起当子线程释放虚存资源后再继续执行。
 */

int do_something()
{
    printf("This is son, the pid is:%d, the a is: %d\n", getpid(), ++a);
    free(stack); //这里我也不清楚，如果这里不释放，不知道子线程死亡后，该内存是否会释放，知情者可以告诉下,谢谢
    exit(1);
}

int main()
{
    void *stack;
    a = 1;
    stack = malloc(FIBER_STACK); //为子进程申请系统堆栈

    if (!stack)
    {
        printf("The stack failed\n");
        exit(0);
    }
    printf("creating son thread!!!\n");

    clone(&do_something, (char *)stack + FIBER_STACK, CLONE_VM | CLONE_VFORK, 0); //创建子线程

    printf("This is father, my pid is: %d, the a is: %d\n", getpid(), a);
    exit(1);
}