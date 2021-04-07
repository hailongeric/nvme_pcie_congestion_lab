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

    socklen_t len;
    len = sizeof(struct sockaddr_in);

    char *str = malloc(1024 * 1024 * 10);
    memset(str, 'A', 1024 * 1024 * 10);


    int size = 1024;
    if (args > 1)
    {
        size = atoi(argv[2]);
    }

    int k = 0;

    for (int i = 0; i < 1000000; i++)
    {
        sendto(sock, str, 6550, 0, (struct sockaddr *)&server_addr, len);
        k++;
         volatile uint64_t m =0;
        // if(k==20){
            for (volatile int j = 0; j < 100000; j++)
            {
                m++;
            }
        //     printf("%d\n", m);
        //     k=0;
        // }
    }

    close(sock);
    return 0;
}