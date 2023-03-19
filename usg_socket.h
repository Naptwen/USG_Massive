#include <stdlib.h>
#include <iostream>
#include <cstring>
#include <sstream>
#include <sys/types.h>
#include <stdio.h>
#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#pragma comment(lib, "Ws2_32.lib") 
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>
#endif

#define BUFFERSIZE 1024

class Socket
{
private:
    const char* _ip_addr = "127.0.0.1";
    const char* _port = "5555";
    const long _time = 1;
public:
    Socket(
        const char* ip_addr, 
        const char* port, 
        const long timeout = 1) : 
            _ip_addr(ip_addr), _port(port), _time(timeout) {}
#ifdef _WIN32
    SOCKET hSock;
    bool init()
    {
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2,2), &wsaData);
        struct sockaddr_in servAddr;
        char recvmsg[BUFFERSIZE];
        // Create Socket
        hSock = socket(PF_INET, SOCK_STREAM, 0);

        if(hSock ==SOCKET_ERROR)
        {
            printf("[Client] socket create error! %s::%s\n", _ip_addr, _port);
        }

        memset(&servAddr, 0, sizeof(servAddr));
        servAddr.sin_family = AF_INET;
        servAddr.sin_addr.s_addr = inet_addr(this->_ip_addr);
        servAddr.sin_port = htons(std::stoi(this->_port));

        //Address check
        if (servAddr.sin_addr.s_addr == INADDR_NONE)
        {
            printf("[Client] address error! %s::%s\n", _ip_addr, _port);
            return true;
        }

        //Socket connectioning
        if(connect(hSock, (SOCKADDR*)& servAddr, sizeof(servAddr)) == SOCKET_ERROR)
        {
            printf("[Client] connection error! %s::%s\n", _ip_addr, _port);
            closesocket(hSock);
            return true;
        }        
        printf("[Client] connected : [%d] %s::%s\n", hSock, _ip_addr, _port);
        return false;            
    }
    void send_client(const char* sendmsg)
    {
        printf("[Client] send message : [%s]\n", sendmsg);
        send(hSock, sendmsg, strlen(sendmsg) + 1, 0);
    }
    void recv_client()
    {
        char recvmsg[BUFFERSIZE];
        auto recvLen = recv(hSock, recvmsg, BUFFERSIZE - 1, 0);
        if(recvLen <= 0)
        {
            if(WSAGetLastError() == WSAETIMEDOUT)
                printf("[Client] recv timeout : %s::%s\n", _ip_addr, _port);
            else
                printf("[Client] recv error : %s::%s\n", _ip_addr, _port);
            close_client();
            return;
        }
        recvmsg[recvLen] = '\0';
        printf("[Client] recv message : [%s]\n", recvmsg);
    }
    void close_client()
    {
        WSACleanup();
        closesocket(hSock);
    }
#elif defined(__linux__)
    int hSock;
    void init()
    {
        struct sockaddr_in servAddr;
        char recvmsg[BUFFERSIZE];
        // 소켓 생성
        hSock = socket(PF_INET, SOCK_STREAM, 0);
        memset(&servAddr, 0, sizeof(servAddr));
        servAddr.sin_family = AF_INET;
        inet_pton(AF_INET, this->_ip_addr, &servAddr.sin_addr);
        servAddr.sin_port = htons(std::stoi(this->_port));
        //Address 확인
        if (servAddr.sin_addr.s_addr == INADDR_NONE)
            return true;

        //소켓 타임아웃 설정
        struct timeval tv;
        tv.tv_sec = this->_time;
        tv.tv_usec = 0;
        setsockopt(hSock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

        // 소켓 주소 할당
        if(connect(hSock, (SOCKADDR*)& servAddr, sizeof(servAddr)) == SOCKET_ERROR)
        {
            printf("[Client] connection error! %s::%s\n", _ip_addr, _port);
            closesocket(hSock);
            return true;
        }        
    }
    
    void send_client(char sendmsg[BUFFERSIZE])
    {
        write(hSock, sendmsg, sizeof(sendmsg));
    }

    void recv_client()
    {
        char recvmsg[BUFFERSIZE];
        auto recvLen = read(hSock, recvmsg, BUFFERSIZE - 1);
        if(recvLen <= 0)
        {
            if(errno == EAGAIN)
                printf("[Client] recv timeout : %s::%s\n", _ip_addr, _port);
            else
                printf("[Client] recv error : %s::%s\n", _ip_addr, _port);
            close_client();
        }
        recvmsg[recvLen] = '\0';
        printf("[Client] recv message : [%s]\n", recvmsg);
    }

    void close_client()
    {
        close(hStock);
    }
#endif
};