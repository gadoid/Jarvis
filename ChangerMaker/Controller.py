from FileResolver import FileResolver
from ParameterModifyer import ParameterModifyer
import os 
import time
class Controller():
    def __init__(self) -> None:
        pass


    def createScfFromQT(self,configfile=None):
        # get QT scf from QT git
        #file = None 
        #a = ParameterModifyer(file).parameterModifier(fixParameterlist=configfile)
        name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")
        with open(name,"w") as SCF :
            SCF.write(FileResolver.xmlMaker(ParameterModifyer("test.xml").parameterModifier(fixParameterlist=configfile)))
        print("\"%s\"文件保存在%s"%(name,os.getcwd()))
    
    def createScfLocal(self,configfile=None):
        # get QT scf from QT git
        #file = None 
        #a = ParameterModifyer(file).parameterModifier(fixParameterlist=configfile)
        name = "SCF_"+time.strftime("%Y_%m_%d_%H_%M_%S")
        with open(name,"w") as SCF :
            SCF.write(FileResolver.xmlMaker(ParameterModifyer("test.xml").parameterModifier(fixParameterlist=configfile)))
        print("\"%s\"文件保存在%s"%(name,os.getcwd()))

    

print(Controller().createScfFromQT())