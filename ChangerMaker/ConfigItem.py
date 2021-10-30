from abc import abstractclassmethod
import json
class ConfigItem :
    def __init__(self,mode="w") -> None:
        self._dict = json.load("setting.json")
    
    def run():
        input("选择参数")
    

class Item(abstractclassmethod()):
    def __init__(self) -> None:
        super().__init__()
        self._distName  
        self._name 
        self._value 

class F1U(Item):
    def __init__(self) -> None:
        super().__init__()
        self._distName = 