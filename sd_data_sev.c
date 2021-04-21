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
#include<string.h>
#include <signal.h>

#define N 5000000
int times_gap = 2;
uint64_t T1, T2, T3, gap_sum=0,gap;

char secret[380] = "10101010101010101010100000000000000010100000010010011000011001001001011100000000010101010001111101110011010001110110011001001101110000010010100011011111000"; //001100101001111110000010110001001010000010010100011101101010011111001000011111011100010001101111111000110111011001011110101110000010001000110101000000111101101100101011110100111011101111110111101";


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
    //setsockopt(sock, IPv4, int option_name,     const void*option_value, socklen_t option_len);
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
    int per_size = 1024;

    int size = 6550;
    if (args > 1)
    {
        size = atoi(argv[1]);
    }
    if (args > 2)
    {
        times_gap = atoi(argv[2]);
    }
    if (args > 3)
    {
        per_size = atoi(argv[3]);
    }
    printf("send sise -> %d\ntimes_gap -> %d\n",size,times_gap);

    signal(SIGINT, sighandler);

    


    T1 = rdtscp();
    for(int jj = 0; jj< size;jj++){
        sendto(sock, str, 1472, 0, (struct sockaddr *)&server_addr, len);
    }
    T2 = rdtscp(); 
    
    gap = T2-T1;
    printf("%lld\n",gap); 
    fflush(stdout);
    int len_s = strlen(secret);
    T3 = rdtscp(); 
    for (int i = 0; i < N; i++)
    {
        char tmp = secret[i%len_s];
        if(tmp == '1'){
            T1 = rdtscp();
            for(int jj = 0; jj< size;jj++){
                sendto(sock, str, per_size, 0, (struct sockaddr *)&server_addr, len);
            }
            T2 = rdtscp();
            
        }else if(tmp == '0'){
            T1 = rdtscp();
            for(int jj = 0; jj< 1;jj++){
                sendto(sock, str, 1472, 0, (struct sockaddr *)&server_addr, len);
            }
            T2 = rdtscp();
            //gap = ((T2-T1) +gap)/2;
            // gap = T2-T1;
            // while(1){
            //     T3 = rdtscp();
            //     if(T3-T2 >= times_gap*gap)
            //         break;
            // }
        }
        T2 = rdtscp();
        while(1){
                T3 = rdtscp();
                
                if(T3-T2 >= times_gap*gap){
                    break;
                }
        }
        //  T2 = rdtscp();
        // while(1){
        //     T3 = rdtscp();
        //     if(T3-T2 >= times_gap*gap)
        //         break;
        // }
        
    }
    close(sock);
    return 0;
}
