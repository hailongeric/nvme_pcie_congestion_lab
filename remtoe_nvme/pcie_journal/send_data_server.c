#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#define N 5000000
int times_gap = 2;

static inline uint64_t rdtscp()
{
    uint64_t rax,rdx;
    asm volatile ( "rdtscp\n" : "=a" (rax), "=d" (rdx)::"%rcx","memory");
    return (rdx << 32) | rax;
}

int main(int args, char *argv[])
{

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1)
    {
        printf("socket error!\n");
        exit(1);
    }
    
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("10.177.74.236");
    server_addr.sin_port = htons(25000);
    int len;
    len = sizeof(struct sockaddr_in);

    char *str = malloc(1024 * 1024 * 10);
    memset(str, 'A', 1024 * 1024 * 10);


    int size = 6550;
    if (args > 1)
    {
        size = atoi(argv[1]);
    }
    if (args > 2)
    {
        times_gap = atoi(argv[2]);
    }
    printf("send sise -> %d\ntimes_gap -> %d\n",size,times_gap);

    uint64_t T1, T2, T3, gap_sum=0;

    for (int i = 0; i < N; i++)
    {
        T1 = rdtscp();
        sendto(sock, str, size, 0, (struct sockaddr *)&server_addr, len);
        T2 = rdtscp();
        uint64_t gap = T2-T1;

        gap_sum+=gap;
        // volatile uint64_t m =0;
        // for (volatile int j = 0; j < 100000; j++)
        // {
        //     m++;
        // }
        while(1){
            T3 = rdtscp();
            if(T3-T2 >= times_gap*gap)
                break;
        }
    }

    printf("Gap: %lf  -> time: %lf \nfree cpu is 2*Gap\n", (gap_sum*1.0)/N, ((gap_sum*1.0)/N)/3600000000);

    close(sock);
    return 0;
}
