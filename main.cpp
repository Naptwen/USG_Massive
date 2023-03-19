#include "usg_socket.h"

int main(int argv, char** argc)
{
    std::string ipAddr = "127.0.0.1";
    std::string port = "5555";
    long timeout = 1;
#ifdef _WIN32
    for(int i = 0; i < argv; ++i)
    {
        if(_strcmpi(argc[i],"--ip") == 0)
           ipAddr = argc[i + 1];
        else if(_strcmpi(argc[i],"--port") == 0)
           port = argc[i + 1];
        else if(_strcmpi(argc[i],"--timeout") == 0)
           timeout = std::stoi(argc[i + 1]);
    }
#else
    for(int i = 0; i < argv; ++i)
    {
        if(strcasecmp(argc[i],"--ip") == 0)
           ipAddr = argc[i + 1];
        else if(strcasecmp(argc[i],"--port") == 0)
           port = argc[i + 1];
        else if(strcasecmp(argc[i],"--timeout") == 0)
           timeout = std::stoi(argc[i + 1]);
    }
#endif
    printf("[Client] IP : [%s]\n[Client] PORT : [%s]\n[Client] TIMEOUT : [%d]\n", ipAddr.c_str(), port.c_str(), timeout);
    auto clientSocket = Socket(ipAddr.c_str(), port.c_str(), timeout);
    if(clientSocket.init())
        return 1;
    for(int i = 0; i < 4; ++i)
    {
        clientSocket.send_client("hello world!");
        clientSocket.recv_client();
    }
    return 0;
}