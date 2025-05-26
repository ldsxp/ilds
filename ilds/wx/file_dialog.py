import os
import wx

# 对话框扩展名过滤器
WILDCARD = ("Microsoft Office Excel (*.xls)|*.xls|"
            "Python source (*.py)|*.py|"
            "Compiled Python (*.pyc)|*.pyc|"
            "SPAM files (*.spam)|*.spam|"
            "Egg file (*.egg)|*.egg|"
            "All files (*.*)|*.*")


def show_file_dialog(dialog_class, parent, message, default_dir, default_file, dialog_wildcard, style, set_value):
    """
    文件对话框通用函数
    """
    dlg = dialog_class(parent,
                       message=message,
                       defaultDir=default_dir,
                       defaultFile=default_file,
                       wildcard=dialog_wildcard,
                       style=style)

    result = None

    if dlg.ShowModal() == wx.ID_OK:
        if style & wx.FD_MULTIPLE:
            result = dlg.GetPaths()
        else:
            result = dlg.GetPath()

        if set_value is not None:
            if isinstance(result, list):
                set_value('|'.join(result))
            else:
                set_value(result)

    dlg.Destroy()
    return result


def open_file_dialog(parent, message='打开文件 ...', default_dir=None, default_file='', dialog_wildcard=WILDCARD,
                     style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW,
                     set_value=None):
    """
    打开文件对话框
    """
    if default_dir is None:
        default_dir = os.getcwd()

    return show_file_dialog(wx.FileDialog, parent, message, default_dir, default_file, dialog_wildcard, style, set_value)


def save_file_dialog(parent, message='保存文件 ...', default_dir=None, default_file='', dialog_wildcard=WILDCARD,
                     style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, set_value=None):
    """
    保存文件对话框
    """
    if default_dir is None:
        default_dir = os.getcwd()

    return show_file_dialog(wx.FileDialog, parent, message, default_dir, default_file, dialog_wildcard, style, set_value)


def dir_dialog(parent, message='选择文件夹', default_path='', style=wx.DD_DEFAULT_STYLE, set_value=None, **kwargs):
    """
    选择文件夹对话框
    """
    dlg = wx.DirDialog(parent, message, defaultPath=default_path, style=style, **kwargs)
    file_path = None

    if dlg.ShowModal() == wx.ID_OK:
        file_path = dlg.GetPath()

        if set_value is not None:
            set_value(file_path)

    dlg.Destroy()
    return file_path
