from colorama import Fore, Back, Style


def prompt_list(in_list, title='选择内容：', text='输入序号：'):
    """
    命令行选择列表内容的交互提示
    选择列表内容，输入 e 返回 None
    """
    print(Fore.BLUE + title)
    for i, v in enumerate(in_list):
        print(Fore.RED + f'({i}):', Fore.GREEN + str(v))
    _ret = None
    while True:
        input_str = input(Fore.YELLOW + text)
        # print(input_str, type(input_str), int(input_str))
        if input_str == 'e':
            break
        try:
            _ret = in_list[int(input_str)]
            break
        except:
            continue
    print(Style.RESET_ALL)
    return _ret


def confirm_yes_no(title='是否确认继续...', text='输入 y 确认，其他任意字符表示取消'):
    """
    命令行选择列表内容的交互提示
    输入 y 返回 True，其他任意字符 返回 False
    """
    print(Fore.RED + title)
    print(Fore.YELLOW + text)
    input_str = input(Fore.BLUE + '请输入选择：')
    ret = False
    if input_str.lower() == 'y':
        ret = True

    print(Style.RESET_ALL)
    return ret


def doc():
    """
    打印模块说明文档
    """
    doc_text = """"""
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=prompt_list)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=confirm_yes_no)

    print(doc_text)


if __name__ == '__main__':

    my_list = [1111, 3333]
    ret = prompt_list(my_list)
    if ret is None:
        print('没有选择内容直接退出了')
    else:
        print('选择了', ret)

    ret = confirm_yes_no()
    if ret:
        print('选择了确认')
    else:
        print('选择了取消')
