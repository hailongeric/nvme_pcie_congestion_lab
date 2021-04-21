#include<stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define N 2000000

static inline uint64_t rdtscp()
{
    uint64_t rax,rdx;
    asm volatile ( "rdtscp\n" : "=a" (rax), "=d" (rdx)::"%rcx","memory");
    return (rdx << 32) | rax;
}


int main(int args, char *argv[]){



    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("10.177.74.243");
    server_addr.sin_port = htons(25000);
    bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
    listen(sock, 1);
    struct sockaddr_in client_addr;
    socklen_t client_addr_size = sizeof(client_addr);
    int client_sock = accept(sock, (struct sockaddr*)&client_addr, &client_addr_size);
    char *str = malloc(1024*1024*10);
    memset(str,'A',1024*1024*10);
    //size = 1460 <one packetage size>;

    int size =1024;
    if(args > 1){
        size = atoi(argv[1]);
    }


    uint64_t T1, T2, T3, gap_sum=0;;
    for(int i =0 ;i<N;i++){
        T1 = rdtscp();
        write(client_sock, str,size);

        T2 = rdtscp();
        uint64_t gap = T2-T1;
        gap_sum+=gap;

        while(1){
            T3 = rdtscp();
            if(T3-T2 >= 9*gap)
                break;
        }
    }
    printf("GAP %f\n", ((gap_sum*1.0)/N)/3600000000);

    close(client_sock);
    close(sock);
    return 0;

}
