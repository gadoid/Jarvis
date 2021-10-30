class Jarvis():
    def __init__(self) -> None:
        pass
        self.logo()
        self.run()

    def run(self):
        while True:
            self.option()

    def logo(self):
        print("""
   ___                  _     
  |_  |                (_)    
    | | __ _ _ ____   ___ ___ 
    | |/ _` |  __\\ \\ / / / __|
/\\__/ / (_| | |   \\ V /| \\__ \\
\\____/ \\__,_|_|    \\_/ |_|___/
                              
  Simple - Smart - Efficiency                             
        """)
    
    def option(self):
        print("""
        选择功能 ：
        1. 配置SCF文件
        2. 配置环境配置文件
        3. 命令行记录工具
        4. 配置文件格式化
        5. 后台功能
        6. feature模板
        """)
        message = input("请选择 ： ")

    def configJsonCreate(self):
        

# Jarvis
# +pull scf from qt check the difference client
# （检查并拉去最新的qt scf 文件 比较不同）
# +modify scf from configfile （qt/input）client
#   (由配置文件来修改scf 文件，同时接收拉取和输入选项)
# +config the configfile client
# （配置文件配置）
# +环境参数获取 client+server
# （从页面或表格中提取环境信息，分析对应的ip）
# +wa notifyer / wa executor client+server
# （WA提示和WA执行）socket
# +command logger client + server
# （命令记录工具）
# +format maker
# （提供配置文件的格式化）client
# +env check
# （提供环境状态统计表） server


if __name__ == "__main__":
    Jarvis()