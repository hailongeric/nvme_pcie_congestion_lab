#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(){

    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr)); 
    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_addr.s_addr = inet_addr("10.177.74.243");  
    serv_addr.sin_port = htons(25000); 

    if(connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))<0){
        puts("connect error\n");
    }
   

    char *buffer = malloc(1024*1024);
    for(int i=0;i<100000000;i++){
        int ret = read(sock, buffer, 1024*1024);
        //printf("[+]: num: %d recv size: %d \n",i,ret);
    }
    
    close(sock);
    return 0;
}