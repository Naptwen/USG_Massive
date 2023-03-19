import time
from usg_multi_process.process import ParallerProcess
import psutil
import threading
import time
# 2023-03-20 Useop Gim(c) GNU3.0 Affero
# Verison 1.0 

class Core:
    """
    This class object controls the mutiple process
    """

    def __init__(self):
        self.processes = dict()

    def append(self, name: str, process_config):
        """
        Add process configuration
        """
        print(f"[Core] Process append! {len(self.processes)}")
        self.processes[name] = ParallerProcess(**process_config, name = name)

    def start(self):
        """
        Start process list
        """
        print(f"[Core] start! {len(self.processes)}")
        self._kill_all()
        for _key, _process in self.processes.items():
            print(f'[Core] Process {_key} is start')
            t = threading.Thread(target=_process.start)
            t.daemon = True
            t.start()
            time.sleep(2)# Waiting until the process is running

    def push(self, trg:str, send_data):
        """
        Add send data for specific process
        Args:
            trg(str): Process name
        """
        print(f"[Core] push {trg}")
        try:
            self.processes[trg].send_q.put_nowait(send_data)
        except Exception as error:
            print(f"[Core] push {trg} timeout!")
            pass
        
    def pull(self, trg:str):
        """
        Receive data from specific process
        Args:
            trg(str): Process name
        """
        print(f"[Core] pull {trg}")
        try:
            return self.processes[trg].recv_q.get(timeout=self.processes[trg].timeout)            
        except Exception as error:
            print(error)
            return None

    def _kill_all(self):
        """
        Kill all processes whose process name are as same as on the process config list
        """
        print(f"[Core] Kill process start! {len(self.processes)}")
        for _process in self.processes.values():
            for _running_process in psutil.process_iter():
                if _running_process.name() == _process.pName.lower():
                    _running_process.kill()
                    print(f"[Core] {_process.pName} process is killed!")

