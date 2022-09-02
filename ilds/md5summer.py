import os
import json
import hashlib

from .file import get_file_md5


def create_md5(dir_path, save_md5=None):
    """
    创建 md5summer md5 验证
    """
    if not os.path.isdir(dir_path):
        raise FileExistsError(f'{dir_path} 不是目录文件')

    if save_md5 is None:
        save_md5 = dir_path + '.md5'

    err_list = []

    with open(save_md5, 'w', encoding='gb2312') as out_md5:
        print('\n处理路径：\n%s\n' % (dir_path))
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for _filename in filenames:
                _file = os.path.join(dirpath, _filename)
                md5_file = _file.replace(dir_path, '').replace('\\', '/').strip('/')

                try:
                    line = f"{get_file_md5(_file)} *{md5_file}\n"
                    # print(line.strip())
                    out_md5.write(line)
                except Exception as e:
                    err_list.append(f"{md5_file} {e}")

    if err_list:
        with open(save_md5 + '.err', 'w', encoding='utf-8') as out_f:
            out_f.write('\n'.join(err_list))


def checking_md5(file, dir_path=None):
    """
    检验文件的 md5 信息
    """

    if dir_path is None:
        # dir_path = os.path.splitext(file)[0]
        dir_path = os.path.dirname(file)

    if not os.path.isdir(dir_path):
        raise FileExistsError(f'{dir_path} 不是目录文件')

    check_out = []

    print('文件路径：\n%s\n' % (dir_path))
    with open(file, 'r') as in_f:
        for line in in_f:
            _list = line.strip().split(' *')
            if len(_list[0]) == 32:
                # print(_list)
                _file = os.path.join(dir_path, _list[1])
                md5 = _list[0]
                if os.path.exists(_file):
                    # print(file, md5)
                    if get_file_md5(_file) != md5:
                        check_out.append({'file': _list[1], 'info': '验证失败', 'md5': md5})
                else:
                    # print(_list[1], '文件没有找到')
                    check_out.append({'file': _list[1], 'info': '文件没有找到'})
    if check_out:
        with open(file + '_检验失败.json', 'w', encoding='utf-8') as f:
            json.dump(check_out, f, ensure_ascii=False, indent=2)


def save_tar(json_file, dir_path=None):
    """
    验证失败的文件保存到压缩包
    """
    import tarfile

    err_list = []

    if dir_path is None:
        # dir_path = os.path.splitext(file)[0]
        dir_path = os.path.dirname(json_file)

    if not os.path.isdir(dir_path):
        raise FileExistsError(f'{dir_path} 不是目录文件')

    tar = tarfile.open(os.path.splitext(json_file)[0] + '_tar.tar', 'w')

    with open(json_file, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        for data in data_list:
            _file = os.path.join(dir_path, data['file'])
            try:
                tar.add(_file)
            except Exception as e:
                err_list.append({'file': data['file'], 'info': str(e)})
            # print(_file)

    tar.close()

    if err_list:
        with open(json_file + '.err.json', 'w', encoding='utf-8') as out_f:
            json.dump(err_list, out_f, ensure_ascii=False, indent=2)


def main():
    import sys
    import argparse
    # https://docs.python.org/zh-cn/3/library/argparse.html

    description = '创建md5summer的简单命令行界面。'
    parser = argparse.ArgumentParser(prog='lds_md5summer', description=description, epilog='谢谢使用！')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('file', help='输入文件名或路径')
    parser.add_argument('-o', '--out_file', help='导出md5文件的名字', default=None)

    if len(sys.argv) == 1:
        parser.exit(1, parser.format_help())

    # 创建互斥的参数，互斥组内的参数不可同时出现
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--check', action='store_true', default=False,
                       help='检验文件的md5信息')
    group.add_argument('-t', '--tar', action='store_true', default=False,
                       help='验证失败的文件保存到压缩包')

    args = parser.parse_args()

    # print('程序的名称', sys.argv[0], parser.prog, args, )

    if args.check:
        checking_md5(args.file, dir_path=args.out_file)
    elif args.tar:
        save_tar(args.file, dir_path=None)
    else:
        create_md5(args.file, args.out_file)


if __name__ == '__main__':
    import time

    start = time.time()

    main()

    print(f'运行时间 {time.time() - start:.3f} 秒', )
