import os
import sys
import json
import subprocess
import pkg_resources
from urllib import request


def get_latest_version(package_name):
    """
    获取 PyPI 上库的最新版本
    """
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    try:
        with request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return data['info']['version']
            else:
                return None
    except Exception as e:
        print(f"获取 {package_name} 最新版本时出错: {e}")
        return None


class RequirementsUpdater:
    def __init__(self):
        self.mirrors = {
            "1": ("阿里", "https://mirrors.aliyun.com/pypi/simple/"),
            "2": ("清华大学", "https://pypi.tuna.tsinghua.edu.cn/simple/"),
            "0": ("默认 PyPI 源", None),
            "e": ("退出更新", ''),
        }

    def choose_mirror(self):
        """
        镜像源菜单选择
        """
        print("请选择您想使用的源:")
        for key, (name, url) in self.mirrors.items():
            print(f"{key}: {name}" + (f" ({url})" if url else ""))

        choice = input("请输入你的选择: ").strip()
        return self.mirrors.get(choice, (None, None))[1]

    def update_environment(self, requirements_file):
        """
        使用 pip 根据更新后的 requirements 文件更新当前环境
        支持使用自定义的国内源
        """
        python_path = sys.executable
        print(f"当前运行的 Python 解释器路径: {python_path}")
        mirror_url = self.choose_mirror()

        try:
            command = [python_path, "-m", "pip", "install", "-r", requirements_file]

            if mirror_url is None:
                info = ""
            elif not mirror_url:
                return
            else:
                command.extend(["-i", mirror_url])
                info = f"(使用镜像源: {mirror_url})"

            subprocess.check_call(command)
            print(f"已根据 {requirements_file} 更新当前环境中的库{info}")
        except subprocess.CalledProcessError as e:
            print(f"更新环境时出错: {e}")

    def update_requirements_file(self, requirements_file):
        """
        更新 requirements.txt 中库的版本到最新版
        """
        print(f"更新文件: {requirements_file}")

        with open(requirements_file, 'r') as file:
            lines = file.readlines()

        update_lines = []
        update_count = 0

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                update_lines.append(line)
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
                    update_lines.append(new_line)
                    print(f"更新 {package_name}: {installed_version} -> {latest_version}")
                    update_count += 1
                else:
                    update_lines.append(line)

            except ValueError:
                update_lines.append(line)

        with open(requirements_file, 'w') as f:
            f.writelines(update_lines)

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

    def main(self):
        while True:
            print("选择要更新的文件:")

            requirements_files = self.list_requirements_files()

            for index, filename in enumerate(requirements_files, start=1):
                print(f"{index} - 更新 {filename}")

            print(f"{len(requirements_files) + 1} - 手动输入要更新的文件")
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
            elif choice == 'e':
                break
            else:
                print("无效输入，请重新输入。")


def main():
    updater = RequirementsUpdater()
    updater.main()


if __name__ == '__main__':
    main()
