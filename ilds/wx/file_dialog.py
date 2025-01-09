import os
import sys

import wx

# 对话框扩展名过滤器
WILDCARD = "Microsoft Office Excel (*.xls)|*.xls|" \
           "Python source (*.py)|*.py|" \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|" \
           "Egg file (*.egg)|*.egg|" \
           "All files (*.*)|*.*"


def open_file_dialog(parent,
                     message='打开文件 ...',
                     default_dir=os.getcwd(),
                     default_file='',
                     dialog_wildcard=WILDCARD,
                     style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW,
                     set_value=None
                     ):
    """
    打开文件对话框，因为打开文件可以选择多个文件，所以我们返回列表，没有内容返回空列表

    :param parent:
    :param message:
    :param default_dir:
    :param default_file:
    :param dialog_wildcard:
    :param style:
    :param set_value: 要设置变量的函数，例如：textCtrl.SetValue
    :return:
    """

    paths = None

    dlg = wx.FileDialog(parent,
                        message=message,
                        defaultDir=default_dir,
                        defaultFile=default_file,
                        wildcard=dialog_wildcard,
                        style=style
                        )

    # 显示对话框，并处理对话框选择结果
    if dlg.ShowModal() == wx.ID_OK:
        # 检查对话框风格是否支持多文件
        if style & wx.FD_MULTIPLE:
            # 返回多个文件的路径列表
            paths = dlg.GetPaths()
        else:
            # 返回单个文件路径
            paths = dlg.GetPath()

    # 销毁对话框。 不要这样做，直到你完成它！
    # 否则可能会发生意外！
    dlg.Destroy()

    if paths and set_value is not None:
        if isinstance(paths, list):
            set_value('|'.join(paths))
        else:
            set_value(paths)

    return paths


def save_file_dialog(parent,
                     message='保存文件 ...',
                     default_dir=os.getcwd(),
                     default_file='',
                     dialog_wildcard=WILDCARD,
                     style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                     set_value=None):
    """
    保存文件对话框

    :param parent:
    :param message:
    :param default_dir:
    :param default_file:
    :param dialog_wildcard:
    :param style:
    :param set_value: 要设置变量的函数，例如：textCtrl.SetValue
    :return:
    """

    file = None
    dlg = wx.FileDialog(
        parent, message=message,
        defaultDir=default_dir,
        defaultFile=default_file,
        wildcard=dialog_wildcard,
        style=style
    )

    # 设置默认过滤器。 默认情况下将使用列表中的第一个过滤器。
    # dlg.SetFilterIndex(2)

    # # 显示对话框，并处理对话框选择结果
    if dlg.ShowModal() == wx.ID_OK:
        file = dlg.GetPath()

    # 销毁对话框
    dlg.Destroy()

    if file and set_value is not None:
        set_value(file)

    return file


def dir_dialog(parent,
               message='选择文件夹',
               default_path='',
               style=wx.DD_DEFAULT_STYLE,
               # pos=None,
               # size=None,
               # name=None,
               set_value=None,
               **kwargs
               ):
    """
    选择文件夹对话框

    :param parent:
    :param message:
    :param default_path: 默认路径
    :param style: 多个风格用 | 分割 wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_CHANGE_DIR
    :param set_value: 要设置变量的函数，例如：textCtrl.SetValue
    :return:
    """
    file_path = None
    dlg = wx.DirDialog(parent, message, defaultPath=default_path, style=style, **kwargs)

    # 显示对话框，并处理对话框选择结果
    if dlg.ShowModal() == wx.ID_OK:
        file_path = dlg.GetPath()

    # 销毁对话框
    dlg.Destroy()

    if file_path and set_value is not None:
        set_value(file_path)

    return file_path
