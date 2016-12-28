#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "NaiveSocketLibrary/NaiveSocketLibrary.h"

#define PORT 0xa591

int main(int argc, char *argv[])
{
   	NSLInit();
	SOCKET sListen = NSLSocket(AF_INET, SOCK_DGRAM, 0);
	SOCKADDR *conn = NSLEndpointV4("0.0.0.0", PORT);
	NSLBindV4(sListen, conn);
	printf("Server started, press ^C to quit...\n");

	while(true)
	{
		SOCKADDR_IN clientAddr;
		memset(&clientAddr, 0, sizeof(clientAddr));

		char message[1024] = {0};
		socklen_t address_len = NSLEndpointV4SocketLen;
		int recvBytes = recvfrom(sListen, message, sizeof(message), 0, (struct sockaddr*)&clientAddr, &address_len);
		if(recvBytes <= 0)
		{
			// non-blocking receive will return a -1
			break;
		}
		printf("Received: %s\n", message);
		sendto(sListen, message, recvBytes, 0, (struct sockaddr*)&clientAddr, address_len);
	}

   NSLCloseSocket(sListen);
   free(conn);
   NSLEnd();
   return 0;
}
