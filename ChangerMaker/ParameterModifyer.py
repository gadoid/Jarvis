from typing import List, Text
from FileResolver import * ;
import os ;
import time ;
import ast
from collections import OrderedDict

class ParameterModifyer():
    def __init__(self,filename,fixpalist="config.json") -> None:
        self._dict = FileResolver.dictMaker(filename)
        # 读取SCF文件，转换为python字典
        self._fixparameterlist = FileResolver.dictMaker(fixpalist)
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
        return self._fixparameterlist
        # 获取配置文件

    # [@distName : {name:value,name:value},{@distName : {name:value}}

    def parameterModifier(self,fixParameterlist=None,MergeOption=False,Merfile=None):
        """ 依照配置对传入的文件进行参数修改
        "shouxiang.jiao@nokia-sbell.com"
        """
        if MergeOption :
            self._dict = Merfile
        if not fixParameterlist : 
            fixParameterlist = self._fixparameterlist
        for element in fixParameterlist :
            #遍历配置文件
            for distName,kv in element.items():
                if isinstance(kv,dict):
                    for k,v in kv.items() :
                        # 分别获取路径名，参数名和对应的值
                        targetDict = self.findDistName(self._dict,distName)
                        # 传入路径名，返回对应路径名的字典（或者ID）
                        targetDict = self.findName(targetDict,k)
                        # 传入方法名，返回对应路径下，对应名称的字典
                        targetDict['#text'] = v
                        # 完成赋值                   
                elif isinstance(kv,list):
                    for num in range (0,len(kv)) :
                        for k,v in kv[num].items() :
                            # 分别获取路径名，参数名和对应的值
                            targetDict = self.findDistName(self._dict,distName)
                            # 传入路径名，返回对应路径名的字典（或者ID）
                            print(targetDict)
                            targetDict = self.findName(targetDict,k,True,num)
                            # 传入方法名，返回对应路径下，对应名称的字典
                            print(targetDict)
                            targetDict['#text'] = v
                        

                    # 完成赋值                   
        print("参数修改完毕")
        return self._dict

    def ParmeterMerge(self,SCF1,SCF2,SCFTemplate="SCFTemplate",size="SCF1",MergeOption=True):
        Dict1 = FileResolver.dictMaker(SCF1)
        Dict2 = FileResolver.dictMaker(SCF2)
        #Dict3 = FileResolver.dictMaker(SCFTemplate)
        if size == "SCF1" :
            SCF = self.ParameterModifyerFollowSCF1(SCF1,SCF2)
        elif size == "SCF2" :
            SCF = self.ParameterModifyerFollowSCF2(SCF1,SCF2)
        elif size == "Max" :
            SCF = self.ParameterModifyerMaxSize(SCF1,SCF2)
        elif size == "Min" :
            SCF = self.ParameterModifyerMinSize(SCF1,SCF2)
        else :
            return print("Wrong Size Option")
        if MergeOption:
            SCF_XML = FileResolver.xmlMaker(SCF)
            name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")+".xml"
            with open(name,"w") as SCF :
                SCF.write(SCF_XML)
            print("\"%s\"文件保存在%s"%(name,os.getcwd()))
        elif not MergeOption :
            return SCF

    def ParameterModifyerFollowSCF1(self,SCF1,SCF2):
        SCF1 = FileResolver.dictMaker(SCF1)
        SCF2 = FileResolver.dictMaker(SCF2)
        SCF1Class = SCF1["raml"]["cmData"]["managedObject"]
        classKey = []
        for distName in SCF1Class :
            classKey.append(distName["@distName"])
        SCF2Class = SCF2["raml"]["cmData"]["managedObject"]
        for element in SCF2Class :
            if element["@distName"] not in classKey :
                SCF1Class.append(element)
        return SCF1
                
    def ParameterModifyerFollowSCF2(self,SCF1,SCF2):
        SCF1 = FileResolver.dictMaker(SCF1)
        SCF2 = FileResolver.dictMaker(SCF2)
        SCF2Class = SCF2["raml"]["cmData"]["managedObject"]
        classKey = []
        for distName in SCF2Class :
            classKey.append(distName["@distName"])
        SCF1Class = SCF1["raml"]["cmData"]["managedObject"]
        for element in SCF1Class :
            if element["@distName"] not in classKey :
                SCF2Class.append(element)
        return SCF2        

    def ParameterModifyerMaxSize(self):
        pass
        # create scf from template 
        # get parameter from both scf 

    def ParameterModifyerMinSize(self):
        pass
        # create scf from template
        # get paramter follow the template 
                
    def btsIdFormat(self,*args):
        btsid = self.getBtsId(args[0])
        cbtsid = self.getBtsId(args[1])
        with open(args[1],"r") as scf :
            sct = scf.read().replace(cbtsid,btsid)
        with open(args[1],"w") as scf:
            scf.write(sct)
        
    def getBtsId(self,SCF=None):
        if not SCF :
            SCF =self._dict
        try:
            btsid = FileResolver.dictMaker(SCF)["raml"]["cmData"]["managedObject"][0]["@distName"]
        except KeyError as ke :
            print("请检查文件%s"%(SCF))
        return btsid

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
            for i in range (0,len(parameterDict['p'])):
                if parameterDict['p'][i]['@name'] == Name:
                    return parameterDict['p'][i]
        elif 'list' in parameterDict.keys():
            NameDict = parameterDict['list']['item']
            if ListOption:
                NameDict = parameterDict['list']['item'][num]['p']
                for i in range (0,len(NameDict)):
                    print(NameDict[i])
                    print("__________")
                    print(Name)
                    if NameDict[i]['@name'] == Name:
                        return NameDict[i]
            elif not ListOption:
                NameDict = parameterDict['list']['item']['p']
                for i in range (0,len(NameDict)):
                    if NameDict[i]['@name'] == Name:
                        return NameDict[i]
            print(ListOption)
            print(NameDict)

    def ParmeterIntersection(self,SCF1,SCF2,SCFTemplate="SCFTemplate",size="SCF1",MergeOption=True):
        Dict1 = FileResolver.dictMaker(SCF1)
        Dict2 = FileResolver.dictMaker(SCF2)
        #Dict3 = FileResolver.dictMaker(SCFTemplate)
        if size == "SCF1" :
            SCF = self.ParameterModifyerFollowSCF1(SCF1,SCF2)
        elif size == "SCF2" :
            SCF = self.ParameterModifyerFollowSCF2(SCF1,SCF2)
        elif size == "Max" :
            SCF = self.ParameterModifyerMaxSize(SCF1,SCF2)
        elif size == "Min" :
            SCF = self.ParameterModifyerMinSize(SCF1,SCF2)
        else :
            return print("Wrong Size Option")
        if MergeOption:
            SCF_XML = FileResolver.xmlMaker(SCF)
            name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")+".xml"
            with open(name,"w") as SCF :
                SCF.write(SCF_XML)
            print("\"%s\"文件保存在%s"%(name,os.getcwd()))
        elif not MergeOption :
            return SCF

    #def parameterAdd(self,)


if __name__  == "__main__" :
    os.chdir("G:\Jarvis\Jarvis\ChangerMaker")
    test = ParameterModifyer("global_configs_streams_0.250_master_CU_CNF_NSA_SCF_TDD_eCPRI_ASOD_AEUB_CU_TL102 (1).xml")
    # test.btsIdFormat("test.xml","test1.xml")
    test.parameterModifier(test.getplist())
    
    #test.ParmeterMerge("global_configs_streams_0.250_master_CU_CNF_NSA_SCF_TDD_eCPRI_ASOD_AEUB_CU_TL102 (1).xml","test1.xml")
    os.chdir(os.getcwd())
    print(os.getcwd())
    with open ("result.json","w") as ob :
        ob.write(json.dumps(test.getdict()))