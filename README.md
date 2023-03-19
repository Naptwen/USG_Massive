# USG_Massive
Paraller Asynchronized python multi process examples

In python example
```python
from parallerprocessing.core import Core
import copy

def main():
    config1 = {
        'ip': '127.0.0.1',
        'port': '4444',
        'timeout': '5',
        'pName': 'main.exe',
        'args': '',
        'runType': 'subprocess'
    }
    config2 = copy.deepcopy(config1)
    config3 = copy.deepcopy(config1)
    config2['port'] = '4455'
    config3['port'] = '5555'

    mycore = Core()
    mycore.append(name='test1', process_config=config1)
    mycore.append(name='test2', process_config=config2)
    mycore.append(name='test3', process_config=config3)
    mycore.start()

    for i in range(0, 100):
        mycore.push(trg='test1', send_data='test is test1')
        mycore.pull(trg="test1")

        mycore.push(trg='test2', send_data='test is test2')
        mycore.pull(trg="test2")

        mycore.push(trg='test3', send_data='test is test3')
        mycore.pull(trg="test3")
```
