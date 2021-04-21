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
#include <signal.h>

long long recv_size = 0, gap_sum=0;

static inline uint64_t rdtscp()
{
    uint64_t rax,rdx;
    asm volatile ( "rdtscp\n" : "=a" (rax), "=d" (rdx)::"%rcx","memory");
    return (rdx << 32) | rax;
}

void sighandler(int signum)
{
   printf("recv data size: %lld\nuse_time : %f\n",recv_size,(gap_sum*1.0)/3600000000);
   exit(0);
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
    //server_addr.sin_addr.s_addr = inet_addr("10.177.74.236");
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(25000);
    bzero(server_addr.sin_zero, 8);

    int len;
    len = sizeof(struct sockaddr_in);

    if(bind(sock,(struct sockaddr *)&server_addr,sizeof(server_addr))<0){
        printf("bind error\n");
    }

    struct sockaddr_in client_addr;
    memset(&client_addr, 0, sizeof(client_addr));
    
    char *str = malloc(1024 * 1024 * 10);
    


    
    uint64_t T1, T2=0;
    signal(SIGINT, sighandler);

    while(1){
        int size = 0;
        size = recvfrom(sock, str, 65500, 0, (struct sockaddr *)&client_addr, &len);
        if(size > 0){
            T1 = rdtscp();

            if(T2){
                recv_size += size;
                gap_sum += (T1-T2);
            }
        }
        T2 = rdtscp();
    }

    close(sock);
    return 0;
}