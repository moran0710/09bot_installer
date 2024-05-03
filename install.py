import os
from rich.console import Console
import subprocess
import sys

console = Console(color_system="auto")


def stop():
    input("出现灾难性错误，按回车键退出程序")
    exit(1)


# 初始化虚拟环境路径
if sys.platform == "win32":
    python_path = r".\.venv\Scripts\python.exe"
elif sys.platform == "linux":
    python_path = r".venv/bin/python3"

bot_path = os.path.join(".", "bot09")

console.print(
    """=======================================================
||                  09Bot 一键安装脚本             ||
||                  Powered By MoranDCCX           ||
||                 基于Nonebot2 开发               ||
||                 开发交流群：798523753           ||
=======================================================""", style="#66ccff", justify="center")

# 环境检测部分
console.print("正在进行Python环境检测")
# python环境检测
result = subprocess.getstatusoutput("python --version")
if result[0] != 0:
    console.print("[red][ERROR] 出现错误：此环境没有安装python，请安装python版本>=3.9后再试[/]")
    stop()
elif int(result[1][7:].split('.')[0]) == 2 or int(result[1][7:].split('.')[1]) < 9:
    console.print("[red][ERROR] Python版本过低，请升级到3.9版本及以上再试[/]")
else:
    console.print("[Success] Python环境正常", style="#7CFC00")

# git检测
try:
    from git import Repo
except ImportError:
    console.print("[ERROR] 出现错误：此环境没有安装git，请安装git后再试\nLinux用户可以使用yum install git或者apt-get install git命令安装\nWindows用户可前往网上下载git安装包")
    stop()

# 虚拟环境检测
console.print("正在检测虚拟环境")
if not os.path.exists(".venv"):
    print("虚拟环境不存在 正在新建")
    subprocess.getstatusoutput("pip install virtualenv")
    subprocess.getstatusoutput("virtualenv .venv")
console.print("[Success] 虚拟环境环境正常", style="#7CFC00")

# clone
console.print("""
请选择下载方式：
1.从github下载(速度慢，更新及时）
2.从gitee下载（速度快，更新可能不及时）
""")
mode = input("请输入模式编号\n")
while True:
    if mode == "1":
        download_url = ("https://github.com/moran0710/Bot09.git", "git@github.com:moran0710/Bot09.git")
        break
    elif mode == "2":
        download_url = ("https://gitee.com/mocstudio/bot09.git", "git@gitee.com:mocstudio/bot09.git")
        break
    else:
        console.print("输入错误，请重新输入")
try:
    with console.status("[blue]正在克隆bot09本体 下载模式：https...[/]"):
        Repo.clone_from(download_url[0], bot_path)
except Exception as e:
    try:
        os.mkdir("bot09")
        with console.status("[red]模式https出现错误 切换下载模式ssh下载中..."):
            Repo.clone_from(download_url[1], bot_path)
    except Exception as e:
        console.print(f"[red]出现异常！")
        console.print(e)
        stop()
console.print("[Success] 存储库下载完成！", style="#7CFC00")

with console.status("开始安装依赖...."):
    result = subprocess.getstatusoutput(f"{python_path} -m pip install -r {os.path.join(bot_path, 'requirement.txt')}")
    if result[0] != 0:
        console.print(f"[red]出现异常！")
        console.print(result[1])
        stop()

console.print("[Success] 依赖安装完成！", style="#7CFC00")

with console.status("正在释放启动脚本...."):
    if sys.platform == "win32":
        bat = (
            r"""@echo off
cd bot09
..\.venv\Scripts\python.exe bot.py
"""
        )
        mode = "bat"
    elif sys.platform == "linux":
        bat = r"""chmod +x ./bot09/lagrange/Lagrange.Linux64
cd bot09
../.venv/bin/python3 runbot.py
"""
        mode = "sh"
    with open(os.path.join(".", "runbot" + "." + mode), "w") as f:
        f.write(bat)

console.print(
    """
已经完成09Bot的安装！
Windows用户可以运行runbot.bat开启机器人
Windows命令提示符一键执行指令：runbot.bat
Linux用户请运行runbot.sh
Linux终端一键执行指令：bash runbot.sh
"""
)
