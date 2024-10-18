import os
import shutil
import subprocess
import sys
from datetime import datetime

# 打包程序使用的自定义变量，每个打包程序都不同！
CONFIG = {
    "ENV_PATH": r"D:\Envs\lds",
    "FILE_DIR": r"D:\git_ldsxp\GUI",
    "GUI_SCRIPT_NAME": "EXE GUI",
    "CMD_ARG": [],  # 添加自定义的命令行参数，以列表的形式添加
    "COPY_FILE_LIST": ["main.ico", "说明.md"],  # 需要复制的文件列表
}

VERSION = "1.0.0"


def format_timedelta(timedelta):
    total_seconds = int(timedelta.total_seconds())
    if total_seconds < 60:
        return f"{total_seconds}秒"
    minutes, seconds = divmod(total_seconds, 60)
    if minutes < 60:
        return f"{minutes}分钟 {seconds}秒"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}小时 {minutes}分钟 {seconds}秒"


class Packager:
    def __init__(self, config=None):
        if config is None:
            self.config = CONFIG
        else:
            self.config = config
        self.debug = False
        self.python_scripts = os.path.join(self.config['FILE_DIR'], f"{self.config['GUI_SCRIPT_NAME']}.py")
        self.icon_path = os.path.join(self.config['FILE_DIR'], "main.ico")

    def check_env(self):
        if not os.path.exists(self.config['ENV_PATH']):
            print(f"打包工具 {VERSION} 版\n")
            print(f"虚拟环境（{self.config['ENV_PATH']}）不存在。\n")
            print("将退出命令行工具！！！\n")
            input("按回车退出...")
            sys.exit()

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_requirements(self):
        start_time = datetime.now()
        requirements_file = os.path.join(self.config['FILE_DIR'], "requirements_dev.txt")
        pip_executable = os.path.join(self.config['ENV_PATH'], "Scripts", "pip.exe")
        source_choice = input("是否使用清华源安装依赖包？(y/N)：").strip().lower()
        if source_choice == 'y':
            subprocess.run([pip_executable, "install", "-r", requirements_file, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/"], check=True)
        else:
            subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)
        end_time = datetime.now()
        print(f"依赖包更新完成 使用时间: {format_timedelta(end_time - start_time)}")
        input("按回车继续...")

    def start_build(self, gui, ):
        start_time = datetime.now()
        self.clean_directories()
        pyinstaller_executable = os.path.join(self.config['ENV_PATH'], "Scripts", "pyinstaller.exe")
        pyinstaller_cmd = [
            pyinstaller_executable,
            "--clean",
            gui,
            "--noupx",
            self.python_scripts,
            "-p", self.config['FILE_DIR'],
            *self.config['CMD_ARG']
        ]
        if os.path.exists(self.icon_path):
            pyinstaller_cmd.extend(["--icon", self.icon_path])
        if self.debug:
            print(pyinstaller_cmd)
        subprocess.run(pyinstaller_cmd, check=True)
        if self.config['COPY_FILE_LIST']:
            self.copy_additional_files()
        end_time = datetime.now()
        print(f"打包完成{'' if gui == '--windowed' else '(命令行)'} 使用时间: {format_timedelta(end_time - start_time)}")
        input("按回车返回菜单...")

    def clean_directories(self):
        for dir_name in ["dist", "build", ]:
            file_path = os.path.join(self.config['FILE_DIR'], dir_name)
            if os.path.exists(file_path):
                shutil.rmtree(file_path)

    def copy_additional_files(self):
        dist_gui_dir = os.path.join(self.config['FILE_DIR'], "dist", self.config['GUI_SCRIPT_NAME'])
        for file_name in self.config['COPY_FILE_LIST']:
            src = os.path.join(self.config['FILE_DIR'], file_name)
            if os.path.exists(src):
                dst = os.path.join(dist_gui_dir, file_name)
                shutil.copy(src, dst)
            else:
                print(f"文件 {file_name} 不存在，跳过复制。")

    def main(self):
        self.check_env()
        while True:
            self.clear_console()
            print(f"打包工具 {VERSION}")
            python_executable = os.path.join(self.config['ENV_PATH'], "Scripts", "python.exe")
            print(python_executable)
            print("Python version:")
            subprocess.run([python_executable, "-V"])
            print("\n   选项   菜 单\n")
            print("   [1]    打包程序\n")
            print("   [2]    打包程序（命令行）\n")
            print("   [3]    更新依赖\n")
            print("   输入其他任意内容退出...\n")
            choice = input("请输入 [] 内的选项，按回车：").strip()

            if choice == "1":
                gui = "--windowed"
                self.start_build(gui)
            elif choice == "2":
                gui = "--console"
                self.start_build(gui)
            elif choice == "3":
                self.update_requirements()
            else:
                print("选择无效，程序退出。")
                break
        print("程序结束。")


def main(config=None):
    packager = Packager(config)
    packager.main()


if __name__ == "__main__":
    main(config=None)
