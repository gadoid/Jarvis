from os import stat
import re;
import json
import os 
import time
import copy
from FileResolver import FileResolver


class JarvisToolsBox():
    @staticmethod
    def getBtsId(file,num=False):
        """
        Static method , Give a file return the file's MRBTS,NRBTS ID 
        Default return the file's MRBTS,NRBTS ID 
        set the num to Ture , return the fils's MRBTS,NRBTS ID number
        """
        with open (file,'r') as fileobject :
            content =fileobject.read()
        result1 = re.search(r'MRBTS[\-][0-9]{1,}',content)
        result2 = re.search(r'NRBTS[\-][0-9]{1,}',content)
        if result1 :
            mrbtsid = result1.group()
        else :
            mrbtsid = None
        if result2 :
            nrbtsid = result2.group()
        else : 
            nrbtsid = None
        if num :
            return re.search(r'[0-9]{1,}',mrbtsid).group()
        return mrbtsid,nrbtsid

    @staticmethod
    def changeBtsId(file1,file2):
        """
        change the file2's MRBTS,NRBTS Id to the file1 
        """
        counter = 0
        mbts1,nbts1 = JarvisToolsBox.getBtsId(file1)
        mbts2,nbts2 = JarvisToolsBox.getBtsId(file2)
        with open (file1,"r") as fileobject :
            FileContent = fileobject.read()
        if mbts2 :
            if mbts1 :
                FileContent = FileContent.replace(mbts1,mbts2)
                print("已修改"+file1+" NRBTS-ID为"+mbts2)
                counter += 1
            else :
                print("未修改MRBTS ID ,请检查"+file1+"是否存在MRBTS ID ！")
        else :
            print("未修改MRBTS ID ,请检查"+file2+"是否存在MRBTS ID ！")

        if nbts2 :
            if nbts1:
                FileContent = FileContent.replace(nbts1,nbts2)
                print("已修改"+file1+" NRBTS-ID为"+nbts2)
                counter += 1
            else :
                print("未修改NRBTS ID,请检查"+file1+"是否存在NRBTS ID ！")
        else :
                print("未修改NRBTS ID,请检查"+file2+"是否存在NRBTS ID ！")
        if counter :
            with open (file1,'w') as fileobject :
                fileobject.write(FileContent)
        else :
            print("未对"+file1+"进行修改")

    @staticmethod
    def GetDistName():
        pass

    @staticmethod
    def ParameterMerageF2toF1(file1,file2,backup=False,new=False):
        if backup :
            os.system(f"copy {file1} {file1+'bak'}") 
            print("已备份文件"+file1)
        with open (file1,"r") as fileobject :
            file1content =FileResolver.dictMaker(file1)
        with open (file2,"r") as fileobject :
            file2content =FileResolver.dictMaker(file2)
        file1Dict = file1content["raml"]["cmData"]["managedObject"]
        distNameList = []
        for distName in file1Dict :
            distNameList.append(distName["@distName"])
        file2Dict = file2content["raml"]["cmData"]["managedObject"]
        for element in file2Dict :
            if element["@distName"] not in distNameList :
                file1Dict.append(element)
        file1content = FileResolver.xmlMaker(file1content)
        if new :
            name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")+".xml"
            with open(name,"w") as fileobject :
                fileobject.write(file1content)
            print("\"%s\"文件保存在%s"%(name,os.getcwd()))
        elif not new :
            with open(file1,"w") as fileobject :
                fileobject.write(file1content)
            print("已根据"+file2+"对"+file1+"进行了添加")
    
    @staticmethod
    def fitId(file1,file2):
        file1content = FileResolver.dictMaker(file1)
        file2content = FileResolver.dictMaker(file2)
        file1Dict = file1content["raml"]["cmData"]["managedObject"]
        file2Dict = file2content["raml"]["cmData"]["managedObject"]
        dist1NameList = [i["@distName"] for i in file1Dict]
        dist2NameList = [i["@distName"] for i in file2Dict]
        for i in dist1NameList :
            r = re.search(i,FileResolver.stringMaker(file2))
            if not r : 
                print(i.split("/"))
            

    @staticmethod
    def ParmeterMerge(file1,file2,SCFTemplate="SCFTemplate",mode="file1",backup=False,new=True):
        #Dict3 = FileResolver.dictMaker(SCFTemplate)
        if mode == "file1" :
            newfile = JarvisToolsBox.ParameterMerageF2toF1(file1,file2,backup,new)
        elif mode == "file2" :
            newfile = JarvisToolsBox.ParameterMerageF2toF1(file2,file1,backup,new)
        # elif mode == "Max" :
        #     newfile = self.ParameterModifyerMaxSize(file1,file2)
        # elif mode == "Min" :
        #     newfile = self.ParameterModifyerMinSize(file1,file2)
        else :
            return print("Wrong Mode Option")

    @staticmethod
    def configJsonGenerte(file):
        filedict = FileResolver.dictMaker(file)
        listdict = {}
        ConfigList = filedict["raml"]["cmData"]["managedObject"]
        for item in ConfigList :
            print(item["@distName"])
            listdict[item["@distName"]] = JarvisToolsBox.findConfiglist(item)
        with open ("config.json","w") as ob :
            ob.write(FileResolver.jsonMaker(listdict))
        print(os.getcwd())
    
    @staticmethod
    def findConfiglist(parameterDict,ListOption=False,num=0,RDict=True):
        distDict = {}

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
            if isinstance(parameterDict['p'],dict):
                distDict[parameterDict['p']['@name']] = parameterDict['p']['#text']
            elif isinstance(parameterDict['p'],list):
                for item in parameterDict['p']:
                    distDict[item['@name']] = item['#text']
        elif 'list' in parameterDict.keys():
            NameDict = parameterDict['list']
            if isinstance(NameDict,list):
                for num0 in range (0,len(NameDict)):
                    NameDict = parameterDict['list'][num0]
                    if isinstance(NameDict,list):
                        for num in range (0,len(NameDict)):
                            if isinstance(NameDict,list):
                                NameDict = parameterDict['list'][num0]['item'][num]['p']
                                print(NameDict)
                                for item in NameDict:
                                    print(item)
                                    print("22222222222222222222222")
                                    distDict[item['@name']] = item['#text']
                            elif isinstance(NameDict,dict):
                                for item in NameDict.items():
                                    print(item)
                                    print("22222222222222222222222")
                                    distDict[item['@name']] = item['#text']
                    elif isinstance(NameDict,list):
                        NameDict = parameterDict['list']['item']['p']
                        for item in NameDict.items():
                            print(item)
                            print("333333333333333333333")
                            distDict[item['@name']] = item['#text']
            elif isinstance(NameDict,dict):
                NameDict = parameterDict['list']['item']
                if isinstance(NameDict,list):
                    itemlist = []
                    for num in range (0,len(NameDict)):
                        NameDict = parameterDict['list']['item'][num]['p']
                        if isinstance(NameDict,list):
                            for item in NameDict:
                                print(item)
                                print("22222222222222222222222")
                                distDict[item['@name']] = item['#text']
                        elif isinstance(NameDict,dict):
                            for item in NameDict.items():
                                print(item)
                                print("22222222222222222222222")
                                distDict[item['@name']] = item['#text']
                        itemlist.append(copy.deepcopy(distDict))
                    distDict = itemlist
                elif isinstance(NameDict,list):
                    NameDict = parameterDict['list']['item']['p']
                    for item in NameDict.items():
                        print(item)
                        print("333333333333333333333")
                        distDict[item['@name']] = item['#text']
        return distDict


if __name__ == "__main__" :
    #JarvisToolsBox.changeBtsId("result.json","config.json")
    #JarvisToolsBox.ParmeterMerge("test.xml","test1.xml",backup=True,new=True)
    # JarvisToolsBox.changeBtsId("test2.xml","test.xml")
    # JarvisToolsBox.fitId("test.xml","test2.xml")
    # JarvisToolsBox.fitId("test2.xml","test1.xml")
    JarvisToolsBox.configJsonGenerte("test2.xml")