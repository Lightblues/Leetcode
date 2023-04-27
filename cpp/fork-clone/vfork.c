#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <unistd.h>

/*
如果fork简单的vfork()的做法更加火爆，内核连子进程的虚拟地址空间结构也不创建了，直接共享了父进程的虚拟空间，当然了，这种做法就顺水推舟的共享了父进程的物理空间
 */

int main(void)
{
    int count = 1;
    int child;

    // child = vfork( );

    printf("Before create son, the father's count is:%d\n", count);

    if ((child = vfork()) < 0)
    {
        perror("fork error : ");
    }
    else if (child == 0) //  fork return 0 in the child process because child can get hid PID by getpid( )
    {
        printf("This is son, his count is: %d (%p). and his pid is: %d\n", ++count, &count, getpid());
        exit(0);
    }
    else //  the PID of the child process is returned in the parent’s thread of execution
    {
        printf("After son, This is father, his count is: %d (%p), his pid is: %d\n", ++count, &count, getpid());
        exit(0);
    }

    return EXIT_SUCCESS;
}