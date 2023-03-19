<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"><img src="https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white"><img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

[![My Skills](https://skillicons.dev/icons?i=python,cpp,linux,docker,aws,gcp)](https://skillicons.dev)

# :basketball: USG_Massive



This package is for paraller Asynchronized python multi process 
This project is for the massive running program for cloud service

## :heart_eyes: Requirements
python 3.9.0 <=

## :snowflake:  Futureworks
1. docker image automatical installation [80%] 
2. aws, gcp for command [50%]
3. manager for assive multiprocessing [10%]
4. GUI data analysis system [0%]

## :art: How to install

download usg_multi_process python package and usg_socket.h

## :saxophone: In python example 

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
