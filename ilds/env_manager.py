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


def get_current_version(package_name):
    """
    获取库的当前安装版本
    """
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None


class EnvManager:
    def __init__(self):
        self.mirrors = {
            "阿里": "https://mirrors.aliyun.com/pypi/simple/",
            "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "PyPI": None,
        }
        self.update_list = []
        settings = load_settings()
        self.is_save_requirements = settings.get("is_save_requirements", True)
        self.selected_mirror_name = settings.get("selected_mirror_name", "PyPI")
        self.mirror_url = self.mirrors.get(self.selected_mirror_name, None)
        self.python_path = sys.executable

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
        try:
            command = [self.python_path, "-m", "pip", "install", "-r", requirements_file]

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
        print(f"{'更新' if self.is_save_requirements else '检查更新'}文件: {requirements_file}")
        start = time.time()

        with open(requirements_file, 'r') as file:
            lines = file.readlines()

        update_count = 0
        requirements_lines = []
        self.update_list = []

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                requirements_lines.append(line)
                continue

            try:
                req = pkg_resources.Requirement.parse(stripped_line)
                package_name = req.project_name
                # req_version = req.specs[0][1]

                # 获取 Python 版本限制
                if ';' in line:
                    python_version_part = line.split(';')[1].strip()
                else:
                    python_version_part = None

                # 获取安装版本
                installed_version = get_current_version(package_name)

                latest_version = get_latest_version(package_name)

                if latest_version and (not installed_version or installed_version != latest_version):
                    if python_version_part is None:
                        new_line = f"{package_name}=={latest_version}\n"
                    else:
                        new_line = f"{package_name}=={latest_version} ; {python_version_part}\n"
                    requirements_lines.append(new_line)
                    self.update_list.append({'installed_version': installed_version, 'latest_version': latest_version, 'package_name': package_name,
                                             'python_version_part': python_version_part, })
                    print(f"{package_name}: {installed_version} -> {latest_version}")
                    update_count += 1
                else:
                    requirements_lines.append(line)

            except ValueError:
                requirements_lines.append(line)

        print(f'使用时间 {second_to_time_str(time.time() - start)}', )

        if self.is_save_requirements:
            with open(requirements_file, 'w') as f:
                f.writelines(requirements_lines)

        if self.is_save_requirements and update_count:
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

        try:
            command = [self.python_path, "-m", "pip", "install", f"{package_name}=={version}"]

            if self.mirror_url is None:
                info = ""
            else:
                command.extend(["-i", self.mirror_url])
                info = f"(使用镜像源: {self.mirror_url})"

            subprocess.check_call(command)
            print(f"已将 {package_name} 更新到 {version}{info}")
        except subprocess.CalledProcessError as e:
            print(f"更新 {package_name} 时出错: {e}")

    def install_update(self):
        while True:
            print("更新内容:")
            for idx, data in enumerate(self.update_list, start=1):
                print(f"{idx}: {data['package_name']} {data['installed_version']} -> {data['latest_version']}")
            selected = input("请输入要更新到环境中的更新内容编号或按回车返回主菜单：").strip()
            if selected.isdigit() and 1 <= int(selected) <= len(self.update_list):
                data = self.update_list[int(selected) - 1]
                chosen_line = f"{data['package_name']}=={data['latest_version']}"
                print(f"正在更新选择的库: {chosen_line.strip()}")
                self.update_selected_package(chosen_line)
            else:
                print("返回主菜单。")
                break

    def manual_install_package(self):
        """
        安装库
        """
        package_name = input("请输入要安装的库（可以指定版本，例如 `ilds==1.0.0`，或者只输入库名安装最新版本）：").strip()
        if not package_name:
            print("库名称不能为空。")
            return

        try:
            command = [self.python_path, "-m", "pip", "install", package_name]

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
        print('-' * 70)
        print(f'Python: {self.python_path}')
        print(f"保存文件: {'是' if self.is_save_requirements else '否'}\t镜像源: {self.selected_mirror_name}")
        print('-' * 70)

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

    def upgrade_pip(self):
        """
        Upgrade pip to the latest version.
        """
        current_version = get_current_version('pip')
        latest_version = get_latest_version('pip')

        if not latest_version:
            print("无法获取 pip 的最新版本，稍后再试。")
            return

        if current_version == latest_version:
            print(f"pip 已经是最新版本: {current_version}")
            return

        try:
            command = [self.python_path, "-m", "pip", "install", "--upgrade", "pip"]

            if self.mirror_url is None:
                info = ""
            else:
                command.extend(["-i", self.mirror_url])
                info = f"(使用镜像源: {self.mirror_url})"

            subprocess.check_call(command)
            print(f"pip 已经升级 {info} {current_version} -> {latest_version}")
        except subprocess.CalledProcessError as e:
            print(f"升级 pip 时出错: {e}")

    def main(self):
        while True:
            self.display_settings()
            print("选择一个选项:")

            requirements_files = self.list_requirements_files()

            for index, filename in enumerate(requirements_files, start=1):
                print(f"{index} - {'更新' if self.is_save_requirements else '检查更新'} {filename}")

            print(f"{len(requirements_files) + 1} - 输入要{'更新' if self.is_save_requirements else '检查更新'}的 requirements 文件")
            print(f"{len(requirements_files) + 2} - 安装库")
            print(f"{len(requirements_files) + 3} - 升级 pip (在PyCharm中会运行失败)")
            print(f"{len(requirements_files) + 4} - 安装待更新的库【{len(self.update_list)}】")
            print(f"{len(requirements_files) + 5} - 设置菜单")
            print("e - 退出")

            choice = input("请输入您的选择：").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(requirements_files):
                filename = requirements_files[int(choice) - 1]
                self.update_requirements_file(filename)
            elif choice == str(len(requirements_files) + 1):
                filename = input(f"请输入要{'更新' if self.is_save_requirements else '检查更新'}的 requirements 文件：").strip()
                if filename:
                    self.update_requirements_file(filename)
                else:
                    print("文件不能为空，请重新输入。")
            elif choice == str(len(requirements_files) + 2):
                self.manual_install_package()
            elif choice == str(len(requirements_files) + 3):
                self.upgrade_pip()
            elif choice == str(len(requirements_files) + 4):
                if self.update_list:
                    self.install_update()
                else:
                    print('没有待更新内容！')
            elif choice == str(len(requirements_files) + 5):
                self.settings_menu()
            elif choice == 'e':
                break
            else:
                print("无效输入，请重新输入！")


def main():
    env_manager = EnvManager()
    env_manager.main()


if __name__ == '__main__':
    main()
