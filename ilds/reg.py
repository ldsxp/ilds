import winreg


def save_to_registry(sub_key, name, value):
    # 打开或创建一个注册表项
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, sub_key)

    # 设置值
    if isinstance(value, int):
        # 如果是整数，使用 REG_DWORD
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
    elif isinstance(value, str):
        # 如果是字符串，使用 REG_SZ
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
    elif isinstance(value, bytes):
        # 如果是字节数组，使用 REG_BINARY
        winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, value)
    else:
        # 如果是其他类型，抛出异常
        raise ValueError(f"不支持的类型: 在键 '{name}' 的值 '{value}' 是不支持的类型 {type(value)}")

    # 关闭注册表项
    winreg.CloseKey(key)


def read_from_registry(sub_key, name):
    # 打开注册表项
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key)

    # 读取注册表项的值
    value, value_type = winreg.QueryValueEx(key, name)

    winreg.CloseKey(key)

    # 根据注册表值类型，处理数据
    if value_type == winreg.REG_SZ:
        return value  # 字符串
    elif value_type == winreg.REG_DWORD:
        return int(value)  # DWORD 整数
    elif value_type == winreg.REG_BINARY:
        return bytes(value)  # 二进制数据
    else:
        ValueError(f"不支持的注册表类型: {name} (类型: {value_type})")


def save_dict_to_registry(sub_key, settings):
    # 打开或创建一个注册表项
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, sub_key)

    # 写入字典中的每个键值对
    for name, value in settings.items():
        if isinstance(value, int):
            # 如果是整数，使用 REG_DWORD
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
        elif isinstance(value, str):
            # 如果是字符串，使用 REG_SZ
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        elif isinstance(value, bytes):
            # 如果是字节数组，使用 REG_BINARY
            winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, value)
        else:
            # 如果是其他类型，抛出异常
            raise ValueError(f"不支持的类型: 在键 '{name}' 的值 '{value}' 是不支持的类型 {type(value)}")

    winreg.CloseKey(key)


def read_dict_from_registry(sub_key):
    registry_dict = {}

    # 打开注册表项
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key)

    # 获取项下的值数量
    num_values = winreg.QueryInfoKey(key)[1]

    # 读取每个值
    for i in range(num_values):
        name, value, value_type = winreg.EnumValue(key, i)

        # 根据注册表值类型，处理数据
        if value_type == winreg.REG_SZ:
            registry_dict[name] = value  # 字符串
        elif value_type == winreg.REG_DWORD:
            registry_dict[name] = int(value)  # DWORD 整数
        elif value_type == winreg.REG_BINARY:
            registry_dict[name] = bytes(value)  # 二进制数据
        else:
            ValueError(f"不支持的注册表类型: {name} (类型: {value_type})")

    winreg.CloseKey(key)

    return registry_dict


if __name__ == '__main__':
    from ilds.time import Timer

    with Timer() as timer:
        ...

        # # 保存字典内容到注册表
        # settings_dict = {
        #     "Setting1": "value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1value1",
        #     "Setting2": 123333,  # 整数值
        #     "Setting3": b'\x00\x01\x02\x03',  # 字节数据
        # }
        # try:
        #     save_dict_to_registry(sub_key=r'Software\MyApp\Settings', settings=settings_dict)
        # except WindowsError as e:
        #     print(f'注册表操作发生错误: {e}')
        #
        # # 读取注册表中的数据
        # print('读取注册表字典', read_dict_from_registry(sub_key=r'Software\MyApp\Settings'))

        # save_to_registry(sub_key=r'Software\MyApp\Settings', name='MySetting', value=r'开发测试')
        # print('读取注册表', read_from_registry(sub_key=r'Software\MyApp\Settings', name='MySetting'))
