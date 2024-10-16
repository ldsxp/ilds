import os
import sys
import time
import json
import subprocess
import pkg_resources

from ilds.time import second_to_time_str

import requests

SETTINGS_FILE = 'env_settings.json'


def load_settings():
    """
    加载设置文件，如果不存在则使用默认设置
    """
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print('打开设置文件出错', e)

    return {"is_save_requirements": True, "selected_mirror": "0", }


def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_latest_version(package_name):
    """
    获取 PyPI 上库的最新版本
    """
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['info']['version']
        else:
            return None
    except Exception as e:
        print(f"获取 {package_name} 最新版本时出错: {e}")
        return None


class EnvManager:
    def __init__(self):
        self.mirrors = {
            "阿里": "https://mirrors.aliyun.com/pypi/simple/",
            "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "PyPI": None,
        }
        self.update_lines = []
        settings = load_settings()
        self.is_save_requirements = settings.get("is_save_requirements", True)
        self.selected_mirror_name = settings.get("selected_mirror_name", "PyPI")
        self.mirror_url = self.mirrors.get(self.selected_mirror_name, None)

    def choose_mirror(self):
        """
        镜像源菜单选择
        """
        print("请选择您想使用的源:")
        mirror_names = list(self.mirrors.keys())

        for idx, name in enumerate(mirror_names, start=1):
            url = self.mirrors[name]
            print(f"{idx}: {name}" + (f" ({url})" if url else ""))

        choice = input("请输入你的选择: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(mirror_names):
            self.selected_mirror_name = mirror_names[int(choice) - 1]
            self.mirror_url = self.mirrors[self.selected_mirror_name]
        else:
            print("无效选择, 使用默认源。")
            self.selected_mirror_name = "PyPI"
            self.mirror_url = self.mirrors.get(self.selected_mirror_name, None)

        settings = load_settings()
        settings["selected_mirror_name"] = self.selected_mirror_name
        save_settings(settings)

    def update_environment(self, requirements_file):
        """
        使用 pip 根据更新后的 requirements 文件更新当前环境
        支持使用自定义的国内源
        """
        python_path = sys.executable
        print(f"当前运行的 Python 解释器路径: {python_path}")

        try:
            command = [python_path, "-m", "pip", "install", "-r", requirements_file]

            if self.mirror_url is None:
                info = ""
            else:
                command.extend(["-i", self.mirror_url])
                info = f"(使用镜像源: {self.mirror_url})"

            subprocess.check_call(command)
            print(f"已根据 {requirements_file} 更新当前环境中的库{info}")
        except subprocess.CalledProcessError as e:
            print(f"更新环境时出错: {e}")

    def update_requirements_file(self, requirements_file):
        """
        更新 requirements.txt 中库的版本到最新版
        """
        print(f"更新文件: {requirements_file}")
        start = time.time()

        with open(requirements_file, 'r') as file:
            lines = file.readlines()

        update_count = 0
        requirements_lines = []
        self.update_lines = []

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                requirements_lines.append(line)
                continue

            try:
                req = pkg_resources.Requirement.parse(stripped_line)
                package_name = req.project_name

                installed_version = None
                try:
                    installed_version = pkg_resources.get_distribution(package_name).version
                except pkg_resources.DistributionNotFound:
                    pass

                latest_version = get_latest_version(package_name)

                if latest_version and (not installed_version or installed_version != latest_version):
                    new_line = f"{package_name}=={latest_version}\n"
                    requirements_lines.append(new_line)
                    self.update_lines.append(new_line)
                    print(f"更新 {package_name}: {installed_version} -> {latest_version}")
                    update_count += 1
                else:
                    requirements_lines.append(line)

            except ValueError:
                requirements_lines.append(line)

        print(f'使用时间 {second_to_time_str(time.time() - start)}', )

        if self.is_save_requirements:
            with open(requirements_file, 'w') as f:
                f.writelines(requirements_lines)

        if update_count:
            update = input(f"有 {update_count} 个需要更新的库\n输入任意字符按回车更新。直接按回车忽略更新，只保存到 {requirements_file} 文件中:")
            if update:
                self.update_environment(requirements_file)
        else:
            print('没有库需要更新')

    def list_requirements_files(self):
        files = os.listdir('.')
        requirements_files = [f for f in files if 'requirements' in f and f.lower().endswith('.txt')]
        return requirements_files

    def update_selected_package(self, package_line):
        """
        更新选择的库到当前环境
        """
        package_name, version = package_line.split('==')
        python_path = sys.executable

        try:
            command = [python_path, "-m", "pip", "install", f"{package_name}=={version}"]

            if self.mirror_url is None:
                info = ""
            else:
                command.extend(["-i", self.mirror_url])
                info = f"(使用镜像源: {self.mirror_url})"

            subprocess.check_call(command)
            print(f"已将 {package_name} 更新到 {version}{info}")
        except subprocess.CalledProcessError as e:
            print(f"更新 {package_name} 时出错: {e}")

    def manual_install_package(self):
        """
        手动安装库
        """
        package_name = input("请输入要安装的库（可以指定版本，例如 `ilds==1.0.0`，或者只输入库名安装最新版本）：").strip()
        if not package_name:
            print("库名称不能为空。")
            return

        python_path = sys.executable

        try:
            command = [python_path, "-m", "pip", "install", package_name]

            if self.mirror_url is None:
                info = ""
            else:
                command.extend(["-i", self.mirror_url])
                info = f"(使用镜像源: {self.mirror_url})"

            subprocess.check_call(command)
            print(f"已安装 {package_name}{info}")
        except subprocess.CalledProcessError as e:
            print(f"安装 {package_name} 时出错: {e}")

    def display_settings(self):
        print(f"保存文件: {'是' if self.is_save_requirements else '否'}, 镜像源: {self.selected_mirror_name}")

    def settings_menu(self):

        while True:
            print("设置菜单:")
            print(f"1 - 设置保存 requirements 文件为 {'否' if self.is_save_requirements else '是'}")
            print("2 - 选择镜像源")
            print("b - 返回主菜单")

            choice = input("请输入您的选择: ").strip()

            settings = load_settings()

            if choice == "1":
                self.is_save_requirements = not self.is_save_requirements
                print(f"设置保存 requirements 文件 已设置为: {'是' if self.is_save_requirements else '否'}")
                settings["is_save_requirements"] = self.is_save_requirements
                save_settings(settings)
            elif choice == "2":
                self.choose_mirror()
            elif choice == "b":
                break
            else:
                print("无效的选择，请重新选择。")

    def main(self):
        while True:
            self.display_settings()
            print("选择一个选项:")

            requirements_files = self.list_requirements_files()

            for index, filename in enumerate(requirements_files, start=1):
                print(f"{index} - 更新 {filename}")

            print(f"{len(requirements_files) + 1} - 手动输入要更新的文件")
            print(f"{len(requirements_files) + 2} - 手动安装库")

            # 如果更新内容存在，添加一个选项
            if self.update_lines:
                print(f"{len(requirements_files) + 3} - 选择更新内容并更新到环境")

            print(f"{len(requirements_files) + 4} - 设置菜单")
            print("e - 退出")

            choice = input("请输入您的选择：").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(requirements_files):
                filename = requirements_files[int(choice) - 1]
                self.update_requirements_file(filename)
            elif choice == str(len(requirements_files) + 1):
                filename = input("请输入要更新的文件：").strip()
                if filename:
                    self.update_requirements_file(filename)
                else:
                    print("文件不能为空，请重新输入。")
            elif choice == str(len(requirements_files) + 2):
                self.manual_install_package()
            elif self.update_lines and choice == str(len(requirements_files) + 3):
                print("更新内容:")
                for idx, line in enumerate(self.update_lines, start=1):
                    print(f"{idx}: {line.strip()}")
                selected = input("请输入要更新到环境中的更新内容编号或按回车返回：").strip()
                if selected.isdigit() and 1 <= int(selected) <= len(self.update_lines):
                    chosen_line = self.update_lines[int(selected) - 1]
                    print(f"正在更新选择的库: {chosen_line.strip()}")
                    self.update_selected_package(chosen_line)
                else:
                    print("返回主菜单。")
            elif choice == str(len(requirements_files) + 4):
                self.settings_menu()
            elif choice == 'e':
                break
            else:
                print("无效输入，请重新输入。")


def main():
    env_manager = EnvManager()
    env_manager.main()


if __name__ == '__main__':
    main()
