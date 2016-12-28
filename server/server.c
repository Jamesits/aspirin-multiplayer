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
SOCKADDR_IN broadcastAddr1;
SOCKADDR_IN broadcastAddr2;

void *t1(void *a) {
    while (1) {
        SOCKADDR_IN clientAddr;
        memset(&clientAddr, 0, sizeof(clientAddr));

        char message[1024] = {0};
        socklen_t address_len = NSLEndpointV4SocketLen;
        int recvBytes = recvfrom(sListen1, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
        if(recvBytes <= 0) continue;
        printf("Received from 1: %s\n", message);
        sendto(sListen1, message, recvBytes, 0, (struct sockaddr*)&broadcastAddr1, address_len);
        sendto(sListen2, message, recvBytes, 0, (struct sockaddr*)&broadcastAddr2, address_len);
    }
    return 0;
}

void *t2(void *a) {
    while (1) {
        SOCKADDR_IN clientAddr;
        memset(&clientAddr, 0, sizeof(clientAddr));

        char message[1024] = {0};
        socklen_t address_len = NSLEndpointV4SocketLen;
        int recvBytes = recvfrom(sListen2, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
        if(recvBytes <= 0) continue;
        printf("Received from 2: %s\n", message);
        sendto(sListen1, message, recvBytes, 0, (struct sockaddr*)&broadcastAddr1, address_len);
        sendto(sListen2, message, recvBytes, 0, (struct sockaddr*)&broadcastAddr2, address_len);
    }
    return 0;
}

int main(int argc, char *argv[])
{
    char loopch=0;
    memset(&broadcastAddr1, 0, sizeof(broadcastAddr1));
    broadcastAddr1.sin_family = AF_INET;
    broadcastAddr1.sin_addr.s_addr = inet_addr("255.255.255.255");
    broadcastAddr1.sin_port = htons(PORT1);
    memset(&broadcastAddr2, 0, sizeof(broadcastAddr2));
    broadcastAddr2.sin_family = AF_INET;
    broadcastAddr2.sin_addr.s_addr = inet_addr("255.255.255.255");
    broadcastAddr2.sin_port = htons(PORT2);
   	NSLInit();
	sListen1 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	conn1 = NSLEndpointV4("0.0.0.0", PORT1);
    setsockopt(sListen1, IPPROTO_IP, IP_MULTICAST_LOOP, (char *)&loopch, sizeof(loopch));
	NSLBindV4(sListen1, conn1);
    sListen2 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	conn2 = NSLEndpointV4("0.0.0.0", PORT2);
    setsockopt(sListen2, IPPROTO_IP, IP_MULTICAST_LOOP, (char *)&loopch, sizeof(loopch));
	NSLBindV4(sListen2, conn2);
	printf("Server started, press ^C to quit...\n");

	pthread_t p1, p2;

    while (1){
        pthread_create(&p1, NULL, t1, NULL);
        pthread_create(&p2, NULL, t2, NULL);

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
