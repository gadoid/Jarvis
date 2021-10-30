from typing import overload
import xmltodict
import json


class FileResolver():
    @staticmethod
    def xmlMaker(json_type):
        print("Change the Json file to Xml")
        try :
            if isinstance(json_type,dict):
                return  xmltodict.unparse(json_type,pretty=True,encoding="UTF-8")
            else :
                return xmltodict.unparse(json.loads(json_type),pretty=True,encoding='UTF-8')
        except FileNotFoundError as fo :
            print("the File Not Found")

    @staticmethod
    def jsonMaker(xml_type):
        print("Change the XML file to Json")
        try :
            if isinstance(xml_type,dict):
                return json.dumps(xml_type)
            else :
                return json.dumps(xmltodict.parse(xml_type),indent=1)
        except FileNotFoundError as fo :
            print("the File Not Found")

    
    @staticmethod
    def dictMaker(filepath):
        if isinstance(filepath,dict):
            return filepath
        type = filepath.split(".")[-1]
        with open (filepath,"r") as fileobject :
            file = fileobject.read()
        if type.lower() == "xml":
            print(f"Change the XML file \"{filepath}\" to Dict")
            return xmltodict.parse(file)
        elif type.lower() == "json":
            print(f"Change the Json file  \"{filepath}\" to Dict")
            return json.loads(file)


