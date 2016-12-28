#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "NaiveSocketLibrary/NaiveSocketLibrary.h"

#define PORT1 48000
#define PORT2 48001

int main(int argc, char *argv[])
{
   	NSLInit();
	SOCKET sListen1 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	SOCKADDR *conn1 = NSLEndpointV4("0.0.0.0", PORT1);
	NSLBindV4(sListen1, conn1);
    SOCKET sListen2 = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	SOCKADDR *conn2 = NSLEndpointV4("0.0.0.0", PORT2);
	NSLBindV4(sListen2, conn2);
	printf("Server started, press ^C to quit...\n");

	while(true)
	{
		{
            SOCKADDR_IN clientAddr;
    		memset(&clientAddr, 0, sizeof(clientAddr));

    		char message[1024] = {0};
    		socklen_t address_len = NSLEndpointV4SocketLen;
    		int recvBytes = recvfrom(sListen1, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
    		if(recvBytes <= 0) break;
    		printf("Received from 1: %s\n", message);
    		sendto(sListen2, message, recvBytes, 0, (struct sockaddr*)&clientAddr, address_len);
        }
        {
            SOCKADDR_IN clientAddr;
    		memset(&clientAddr, 0, sizeof(clientAddr));

    		char message[1024] = {0};
    		socklen_t address_len = NSLEndpointV4SocketLen;
    		int recvBytes = recvfrom(sListen2, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
    		if(recvBytes <= 0) break;
    		printf("Received from 2: %s\n", message);
    		sendto(sListen1, message, recvBytes, 0, (struct sockaddr*)&clientAddr, address_len);
        }
	}

   NSLCloseSocket(sListen);
   free(conn);
   NSLEnd();
   return 0;
}
