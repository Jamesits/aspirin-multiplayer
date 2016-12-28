#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include "NaiveSocketLibrary/NaiveSocketLibrary.h"

#define PORT1 48000
#define PORT2 48001

SOCKET sListen1;
SOCKADDR *conn1;
SOCKET sListen2;
SOCKADDR *conn2;

void t1() {
    SOCKADDR_IN clientAddr;
    memset(&clientAddr, 0, sizeof(clientAddr));

    char message[1024] = {0};
    socklen_t address_len = NSLEndpointV4SocketLen;
    int recvBytes = recvfrom(sListen1, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
    if(recvBytes <= 0) return;
    printf("Received from 1: %s\n", message);
    sendto(sListen2, message, recvBytes, 0, (struct sockaddr*)&clientAddr, address_len);
}

void t2() {
    SOCKADDR_IN clientAddr;
    memset(&clientAddr, 0, sizeof(clientAddr));

    char message[1024] = {0};
    socklen_t address_len = NSLEndpointV4SocketLen;
    int recvBytes = recvfrom(sListen2, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
    if(recvBytes <= 0) return;
    printf("Received from 2: %s\n", message);
    sendto(sListen1, message, recvBytes, 0, (struct sockaddr*)&clientAddr, address_len);
}

int main(int argc, char *argv[])
{
   	NSLInit();
	sListen1 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	conn1 = NSLEndpointV4("0.0.0.0", PORT1);
	NSLBindV4(sListen1, conn1);
    sListen2 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	conn2 = NSLEndpointV4("0.0.0.0", PORT2);
	NSLBindV4(sListen2, conn2);
	printf("Server started, press ^C to quit...\n");

	pthread_t p1, p2;

    while (1){
        pthread_create(&p1, NULL, NULL, NULL);
        pthread_create(&p2, NULL, NULL, NULL);

        pthread_join(p1, NULL);
        pthread_join(p2, NULL);
    }

    NSLCloseSocket(sListen1);
    NSLCloseSocket(sListen2);
    free(conn1);
    free(conn2);
    NSLEnd();
    return 0;
}
