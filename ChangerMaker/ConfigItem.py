from abc import abstractclassmethod
import json
class ConfigItem :
    def __init__(self,mode="w") -> None:
        self._dict = json.load("setting.json")
    
    def run():
        btsid = input("输入BTSID：")
        # 替换配置文件中的BTSID
        item = input("选择参数")
    

class Item(abstractclassmethod()):
    def __init__(self) -> None:
        super().__init__()
        self._distName  
        self._name 
        self._value 
        self.btsid 

class F1U(Item):
    def __init__(self,btsid) -> None:
        super().__init__()
        self._distName = btsid+"/TNLSVC-1/TNL-2/IPNO-1/IPRT-1"
        self._name = 