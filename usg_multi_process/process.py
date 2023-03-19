import subprocess
import socket
from multiprocessing import Queue, Process
# 2023-03-20 Useop Gim(c) GNU3.0 Affero
# Verison 1.0 


class ParallerProcess:
    """
    This class object controls the process and server
    """

    def __init__(self,
                 ip: str,
                 port: str,
                 timeout: str,
                 pName: str,
                 args: str,
                 runType: str,
                 name: str
                 ) -> None:
        """
        Set the configuration for process

        Args:
            ip(str): IP address for server and client
            port(str): Port address for server and client
            timeout(str): timeout for server and client
            pName(str): process name
            args(str): arguments
            runType(str): Type for running process
        """
        self.ip = ip
        self.port = int(port)
        self.timeout = int(timeout)
        self.pName = pName
        self.args = args
        self.runType = runType
        self.server_socket = None
        self.recv_data = None
        self.connected_socket = None
        self.p = None
        self.send_q = Queue()
        self.recv_q = Queue()
        self.command = ' '.join([
            self.pName,
            self.args,
            '--ip', self.ip,
            '--port', port,
            '--timeout', timeout])
        self.name = name
        print(f"[PROCESS]{self.name} : PROCESS init")

    def _start_server(self) -> None:
        """
        Start server for process
        """
        print(f"[PROCESS]{self.name} : SERVER start")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)

    def _start_process(self) -> None:
        """
        Running subprocess
        """
        print(f"[PROCESS]{self.name} : PROCESS start with config {self.command}")
        subprocess.Popen(
                        args=self.command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, 
                        shell=True,
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
        
    def _start_multi_processing(self) -> None:
        self.p = Process(target=self._start_process)
        self.p.daemon = True
        self.p.start()

    def _connect_server(self) -> None:
        """
        Connecting server and process
        """
        print(f"[PROCESS]{self.name} : Connection start")
        self.connected_socket, _ = self.server_socket.accept()

    def _recv_client(self) -> bool:
        """
        Receiving message from client

        Returns
            If an error occurs, a value of true will be returned
        """
        if self.connected_socket is not None:
            self.recv_data = None
            try:
                self.recv_data = self.connected_socket.recv(1024)
                print(f"[SERVER]{self.name} : recv data [{self.recv_data}]")
                return False
            except:
                # disconnecting client
                print(f"[SERVER]{self.name} : client recv connection is closed.")
                self.connected_socket = None
                return True

    def _send_client(self, send_data: str) -> bool:
        """
        Sending message to client

        Args
            send_data(str): data for sending to process
        Returns
            If an error occurs, a value of true will be returned
        """
        if self.connected_socket is not None:
            try:
                self.connected_socket.sendall(send_data.encode())
                print(f"[SERVER]{self.name} : send data [{send_data}]")
                return False
            except:
                # disconnecting client
                print(f"[SERVER]{self.name} : client send connection is closed.")
                self.connected_socket.close()
                return True

    def _close_process(self) -> None:
        """
        Closing server socket
        """
        print(f"[PROCESS]{self.name} : close")
        self.recv_q = Queue()
        self.send_q = Queue()
        if self.p is not None:
            self.p.terminate()
            self.p = None
        
        print(f"[PROCESS]{self.name} : close done")

    def _reset(self):
        """
        Reset process and server
        """
        print(f"[PROCESS]{self.name} : reset")
        self._start_multi_processing()
        self._connect_server()
        print(f"[PROCESS]{self.name} : reset done")

    def start(self):
        """
        Running PROCESS and SERVER
        """
        print(f"[PROCESS]{self.name} : start")
        self._start_server()
        self._close_process()
        self._reset()
        while True:
            if self._recv_client():
                self._close_process()
                self._reset()
            else:
                print(f'[PROCESS]{self.name} : recv')
                self.recv_q.put(self.recv_data)
            while self.send_q.empty(): 
                pass
            print(f'[PROCESS]{self.name} : send')
            send_data = self.send_q.get()
            self._send_client(send_data)
