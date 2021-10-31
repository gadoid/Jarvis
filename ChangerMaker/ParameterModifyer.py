from typing import List, Text
from FileResolver import * ;
import os ;
import time ;
import ast
import re
from collections import OrderedDict
from JarvisToolsBox import JarvisToolsBox

class ParameterModifyer():
    def __init__(self,filename,fixpalist="tttt.json") -> None:
        self._dict = FileResolver.dictMaker(filename)
        # 读取SCF文件，转换为python字典
        self._configDict = FileResolver.dictMaker(fixpalist)
        # 读取配置文件，转换为python字典

    def getdict(self):
        """ 获取字典的封装函数
        "shouxiang.jiao@nokia-sbell.com"
        """
        return self._dict 
        # 获取SCF 文件
    
    def getplist(self):
        """ 获取配置文件的封装函数
        "shouxiang.jiao@nokia-sbell.com"
        """
        return self._configDict
        # 获取配置文件

    # [@distName : {name:value,name:value},{@distName : {name:value}}

    def parameterModifier(self,configDict=None,MergeOption=False,Merfile=None):
        """ 依照配置对传入的文件进行参数修改
        "shouxiang.jiao@nokia-sbell.com"
        """
        if MergeOption :
            self._dict = Merfile
        if not configDict : 
            configDict = self._configDict
        #for element in configDict :
            #遍历配置文件
        for distName,kv in configDict.items():
            if isinstance(kv,dict):
                for k,v in kv.items() :
                    # 分别获取路径名，参数名和对应的值
                    targetDict = self.findDistName(self._dict,distName)
                    if not targetDict :
                        choice = input("未找到distName："+distName+"是否添加？")
                        if choice.lower() == "y" :
                            self.distNameAdd(distName)
                        else :
                            print("未添加参数"+distName+":"+k)
                            continue 
                    # 传入路径名，返回对应路径名的字典（或者ID）
                    if not targetDict:
                        continue
                    targetDict = self.findName(targetDict,k)
                    # 传入方法名，返回对应路径下，对应名称的字典
                    if targetDict :
                        targetDict['#text'] = v
                    else :
                        print("未找到参数"+k)
                    # 完成赋值                   
            elif isinstance(kv,list):
                for num in range (0,len(kv)) :
                    for k,v in kv[num].items() :
                        # 分别获取路径名，参数名和对应的值
                        targetDict = self.findDistName(self._dict,distName)
                        # 传入路径名，返回对应路径名的字典（或者ID）
                        if not targetDict :
                            continue
                        targetDict = self.findName(targetDict,k,True,num)
                        # 传入方法名，返回对应路径下，对应名称的字典
                        if targetDict:
                            targetDict['#text'] = v
                        else :
                            print("未找到参数"+k)
                    

                    # 完成赋值                   
        print("参数修改完毕")
        return self._dict

    def parameterGetter(self,configDict="cuness.json",MergeOption=False,Merfile=None):
        """ 依照配置对传入的文件进行参数修改
        "shouxiang.jiao@nokia-sbell.com"
        """
        if MergeOption :
            self._dict = Merfile
        if not configDict : 
            configDict = self._configDict
        if isinstance(configDict,str):
            configDict = FileResolver.dictMaker(configDict)
        for element in configDict :
            #遍历配置文件
            for distName,kv in element.items():
                if isinstance(kv,dict):
                    for k in kv.keys() :
                        # 分别获取路径名，参数名和对应的值
                        targetDict = self.findDistName(self._dict,distName)
                        if not targetDict :
                            choice = input("未找到distName："+distName+"是否添加？")
                            if choice.lower() == "y" :
                                self.distNameAdd(distName)
                            else :
                                print("未添加参数"+distName+":"+k)
                                continue 
                        # 传入路径名，返回对应路径名的字典（或者ID）
                        targetDict = self.findName(targetDict,k)
                        # 传入方法名，返回对应路径下，对应名称的字典
                        #print(element[distName][k])
                        if targetDict:
                            element[distName][k] = targetDict['#text']
                        else :
                            print("未找到参数"+k)
                        # 完成赋值                   
                elif isinstance(kv,list):
                    for num in range (0,len(kv)) :
                        for k in kv[num].keys() :
                            # 分别获取路径名，参数名和对应的值
                            targetDict = self.findDistName(self._dict,distName)
                            # 传入路径名，返回对应路径名的字典（或者ID）
                            targetDict = self.findName(targetDict,k,True,num)
                            # 传入方法名，返回对应路径下，对应名称的字典
                        if  targetDict:
                            element[distName][k] = targetDict['#text']
                        else :
                            print("未找到参数"+k)
                with open("testsetting.json","w") as fileobject :
                    fileobject.write(json.dumps(configDict))
                print("值查询完毕，已保存在config.json 中")
                return configDict


    # def ParmeterMerge(self,SCF1,SCF2,SCFTemplate="SCFTemplate",size="SCF1",MergeOption=True):
    #     Dict1 = FileResolver.dictMaker(SCF1)
    #     Dict2 = FileResolver.dictMaker(SCF2)
    #     #Dict3 = FileResolver.dictMaker(SCFTemplate)
    #     if size == "SCF1" :
    #         SCF = self.ParameterModifyerFollowSCF1(SCF1,SCF2)
    #     elif size == "SCF2" :
    #         SCF = self.ParameterModifyerFollowSCF2(SCF1,SCF2)
    #     elif size == "Max" :
    #         SCF = self.ParameterModifyerMaxSize(SCF1,SCF2)
    #     elif size == "Min" :
    #         SCF = self.ParameterModifyerMinSize(SCF1,SCF2)
    #     else :
    #         return print("Wrong Size Option")
    #     if MergeOption:
    #         SCF_XML = FileResolver.xmlMaker(SCF)
    #         name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")+".xml"
    #         with open(name,"w") as SCF :
    #             SCF.write(SCF_XML)
    #         print("\"%s\"文件保存在%s"%(name,os.getcwd()))
    #     elif not MergeOption :
    #         return SCF

    # def ParameterModifyerFollowSCF1(self,SCF1,SCF2):
    #     SCF1 = FileResolver.dictMaker(SCF1)
    #     SCF2 = FileResolver.dictMaker(SCF2)
    #     SCF1Class = SCF1["raml"]["cmData"]["managedObject"]
    #     classKey = []
    #     for distName in SCF1Class :
    #         classKey.append(distName["@distName"])
    #     SCF2Class = SCF2["raml"]["cmData"]["managedObject"]
    #     for element in SCF2Class :
    #         if element["@distName"] not in classKey :
    #             SCF1Class.append(element)
    #     return SCF1
                
    # def ParameterModifyerFollowSCF2(self,SCF1,SCF2):
    #     SCF1 = FileResolver.dictMaker(SCF1)
    #     SCF2 = FileResolver.dictMaker(SCF2)
    #     SCF2Class = SCF2["raml"]["cmData"]["managedObject"]
    #     classKey = []
    #     for distName in SCF2Class :
    #         classKey.append(distName["@distName"])
    #     SCF1Class = SCF1["raml"]["cmData"]["managedObject"]
    #     for element in SCF1Class :
    #         if element["@distName"] not in classKey :
    #             SCF2Class.append(element)
    #     return SCF2        

    def ParameterModifyerMaxSize(self):
        pass
        # create scf from template 
        # get parameter from both scf 

    def ParameterModifyerMinSize(self):
        pass
        # create scf from template
        # get paramter follow the template 
                
    # def btsIdFormat(self,*args):
    #     btsid = self.getBtsId(args[0])
    #     cbtsid = self.getBtsId(args[1])
    #     with open(args[1],"r") as scf :
    #         sct = scf.read().replace(cbtsid,btsid)
    #     with open(args[1],"w") as scf:
    #         scf.write(sct)
        
    # def getBtsId(self,SCF=None):
    #     if not SCF :
    #         SCF =self._dict
    #     try:
    #         btsid = FileResolver.dictMaker(SCF)["raml"]["cmData"]["managedObject"][0]["@distName"]
    #     except KeyError as ke :
    #         print("请检查文件%s"%(SCF))
    #     return btsid

    def findDistName(self,parameterDict,distName,RDict=True):
        try:
            DistNameDict = parameterDict["raml"]["cmData"]["managedObject"]
        except KeyError:
            print("请检查 SCF 文件")
        #SelectDict = a["raml"]["cmData"]["managedObject"]
        # for i in range (0,len(SelectDict)):
        #     if SelectDict[i]["@distName"] == distName :
        #         return i
        for i in range (0,len(DistNameDict)):
            if DistNameDict[i]["@distName"] == distName :
                if RDict :
                    return DistNameDict[i]
                else :
                    return i 
        print("未找到对应的distName%s"%(distName))
        return 0 

    def findName(self,parameterDict,Name,ListOption=False,num=0,RDict=True):
        # SelectDicit = a["raml"]["cmData"]["managedObject"][distNameId]
        # if 'p' in SelectDicit.keys():
        #     for i in range (0,len(SelectDicit['p'])):
        #         if SelectDicit['p'][i]['@name'] == Name:
        #             return i 
        # elif 'list' in SelectDicit.keys():
        #     SelectDicit = SelectDicit['list']['item']['p']
        #     for i in range (0,len(SelectDicit)):
        #         if SelectDicit[i]['@name'] == Name:
        #             return i 
        if 'p' in parameterDict.keys():
            if isinstance(parameterDict['p'],list):
                for i in range (0,len(parameterDict['p'])):
                    if parameterDict['p'][i]['@name'] == Name:
                        return parameterDict['p'][i]
            elif isinstance(parameterDict['p'],dict):
                if parameterDict['p']['@name'] == Name:
                        return parameterDict['p']
            else :
                print("未找到对应参数")
                return 0
        elif 'list' in parameterDict.keys():
            NameDict = parameterDict['list']['item']
            if ListOption:
                NameDict = parameterDict['list']['item'][num]['p']
                if isinstance(NameDict,list):
                    for i in range (0,len(NameDict)):
                        if NameDict[i]['@name'] == Name:
                            return NameDict[i]
                elif isinstance(NameDict,dict):
                    if NameDict['@name'] == Name:
                            return NameDict
            elif not ListOption:
                NameDict = parameterDict['list']['item']['p']
                if isinstance(NameDict,list):
                    for i in range (0,len(NameDict)):
                        if NameDict[i]['@name'] == Name:
                            return NameDict[i]
                elif isinstance(NameDict,dict):
                    if NameDict['@name'] == Name :
                            return NameDict

            else :
                print("未找到对应参数")
                return 0

    # def ParmeterIntersection(self,SCF1,SCF2,SCFTemplate="SCFTemplate",size="SCF1",MergeOption=True):
    #     Dict1 = FileResolver.dictMaker(SCF1)
    #     Dict2 = FileResolver.dictMaker(SCF2)
    #     #Dict3 = FileResolver.dictMaker(SCFTemplate)
    #     if size == "SCF1" :
    #         SCF = self.ParameterModifyerFollowSCF1(SCF1,SCF2)
    #     elif size == "SCF2" :
    #         SCF = self.ParameterModifyerFollowSCF2(SCF1,SCF2)
    #     elif size == "Max" :
    #         SCF = self.ParameterModifyerMaxSize(SCF1,SCF2)
    #     elif size == "Min" :
    #         SCF = self.ParameterModifyerMinSize(SCF1,SCF2)
    #     else :
    #         return print("Wrong Size Option")
    #     if MergeOption:
    #         SCF_XML = FileResolver.xmlMaker(SCF)
    #         name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")+".xml"
    #         with open(name,"w") as SCF :
    #             SCF.write(SCF_XML)
    #         print("\"%s\"文件保存在%s"%(name,os.getcwd()))
    #     elif not MergeOption :
    #         return SCF

    def distNameAdd(self,distName,SCF=None):
        classname = "@"+self.getClassName(distName)
        if SCF :
            return FileResolver.dictMaker(SCF).update({"@class":classname,"@distName":distName,
            "@operation": "create","version":SCF["raml"]["cmData"]["managedObject"][0]["@version"]})
        return self._dict.update({"@class":classname,"@distName":distName,
            "@operation": "create","version":self._dict["raml"]["cmData"]["managedObject"][0]["@version"]})
            
    def NameAdd(self,dict_type,name,value,SCF=None):
        dict_type[name] = value 
        return dict_type
    
    def getClassName(self,distName):
        num = re.search(r'[0-9]{1,}',distName).group()
        with open ("setting.json","r") as fileobject :
            content = json.loads(fileobject.read())
        return content[distName]

    # @staticmethod
    # def btsIdChange(file,newMrbtsId):
    #     if isinstance(newMrbtsId,int):
    #         num = str(newMrbtsId)
    #     elif isinstance(newMrbtsId,str):
    #         num = re.search(r'[0-9]{1,}',newMrbtsId).group()
    #     else :
    #         print("ID信息类型错误，请检查")
    #         return
    #     with open(file,"r") as scf :
    #         sct = scf.read()
    #         id = re.search(r'MRBTS[\-][0-9]{1,}',sct)
    #         if id :
    #             sct = sct.replace(id.group(),"MRBTS-"+num)
    #             print("MRBTSID已修改为"+num)
    #         else :
    #             print("MRBTSID匹配失败")
    #         id = re.search(r'NRBTS[\-][0-9]{1,}',sct)
    #         if id :
    #             sct = sct.replace(id.group(),"NRBTS-"+num)
    #             print("NRBTSID已修改为"+num)
    #         else :
    #             print("NRBTSID匹配失败")
    #     with open(file,"w") as scf:
    #         scf.write(sct)
    
    def createDistClassPair(self,SCF=None):
        if SCF :
            dict = FileResolver.dictMaker(SCF)
        else :
            dict = self._dict
        PairDict= {}
        for ele in dict["raml"]["cmData"]["managedObject"]:
            PairDict[ele["@distName"]] =  ele["@class"]
        with open ("setting.json","w") as fileobejct :
            fileobejct.write(json.dumps(PairDict))
        print("setting文件已生成")

if __name__  == "__main__" :
    os.chdir("G:\Jarvis\Jarvis\ChangerMaker")
    JarvisToolsBox.changeBtsId("test2.xml","tttt.json")
    JarvisToolsBox.changeBtsId("test1.xml","tttt.json")
    JarvisToolsBox.ParameterMerageF2toF1("test2.xml","test1.xml")

    test = ParameterModifyer("test2.xml")

    #test.createDistClassPair(os.getcwd()+"\\test.xml")
    # test.btsIdFormat("test.xml","test1.xml")
    c = test.parameterModifier(test.getplist())
    with open("result.xml","w") as fileobject :
        fileobject.write(FileResolver.xmlMaker(c))
    #test.parameterGetter()
    #test.ParmeterMerge("global_configs_streams_0.250_master_CU_CNF_NSA_SCF_TDD_eCPRI_ASOD_AEUB_CU_TL102 (1).xml","test1.xml")
    # with open ("result.json","w") as ob :
    #     ob.write(json.dumps(test.getdict()))
    #ParameterModifyer.btsIdChange("config.json",76)