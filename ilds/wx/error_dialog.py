import os
import platform
import subprocess

import wx
import wx.adv


class MessageDialog(wx.Dialog):
    def __init__(self, parent, message, title="信息", label='信息', file_path=None):
        super().__init__(parent, title=title, size=(869, 969),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.message = message
        self.file_path = file_path

        panel = wx.Panel(self)

        # 创建用于显示信息的多行文本框
        message_text_ctrl = wx.TextCtrl(panel, value=self.message,
                                        style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # 创建按钮
        close_button = wx.Button(panel, id=wx.ID_OK, label="关闭")

        # 创建布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        if label:
            label_text = wx.StaticText(panel, label=label)
            main_sizer.Add(label_text, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(message_text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # 用于按钮的水平布局
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 创建按钮用于打开文件（如果提供了文件路径）
        if self.file_path and os.path.isfile(self.file_path):
            path_label = wx.StaticText(panel, label=f"文件：{self.file_path}")
            main_sizer.Add(path_label, 0, wx.ALL | wx.CENTER, 5)

            open_file_button = wx.Button(panel, label="打开文件")
            open_file_button.Bind(wx.EVT_BUTTON, self.on_open_file)
            button_sizer.Add(open_file_button, 0, wx.ALL, 5)

            open_dir_button = wx.Button(panel, label="打开文件所在目录")
            open_dir_button.Bind(wx.EVT_BUTTON, self.on_open_directory)
            button_sizer.Add(open_dir_button, 0, wx.ALL, 5)

        button_sizer.Add(close_button, 0, wx.ALL, 5)

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(main_sizer)

    def on_open_file(self, event):
        try:
            system_platform = platform.system()
            if system_platform == "Windows":
                os.startfile(self.file_path)
            elif system_platform == "Darwin":
                subprocess.run(["open", self.file_path], check=True)
            else:
                subprocess.run(["xdg-open", self.file_path], check=True)

        except Exception as e:
            print(f"Exception: {str(e)}")
            wx.MessageBox(f"无法打开文件: {str(e)}", "错误", wx.ICON_ERROR)

    def on_open_directory(self, event):
        try:
            directory = os.path.dirname(self.file_path)
            system_platform = platform.system()

            if system_platform == "Windows":
                os.startfile(directory)
            elif system_platform == "Darwin":
                subprocess.run(["open", directory], check=True)
            else:
                subprocess.run(["xdg-open", directory], check=True)

        except Exception as e:
            print(f"Exception: {str(e)}")
            wx.MessageBox(f"无法打开目录: {str(e)}", "错误", wx.ICON_ERROR)


class MultiErrorDialog(wx.Dialog):
    def __init__(self, parent, errors, title="错误"):
        super().__init__(parent, title=f'{title} [{len(errors)}]', size=(869, 969),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        # 使用滚动窗口
        scroll_win = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.HSCROLL)
        scroll_win.SetScrollRate(5, 5)

        # 创建布局管理器
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 为每个错误信息创建一组控件
        for error in errors:
            error_label = error.get('error_label', '错误信息')
            error_message = error.get('error_message', '')
            error_file_path = error.get('error_file_path', None)

            # 创建错误信息的标签
            error_label_ctrl = wx.StaticText(scroll_win, label=error_label)
            sizer.Add(error_label_ctrl, 0, wx.ALL | wx.CENTER, 5)

            # 创建用于显示错误信息的多行文本框
            error_text_ctrl = wx.TextCtrl(scroll_win, value=error_message,
                                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
            error_text_ctrl.SetMinSize((400, 150))  # 设置最小尺寸
            sizer.Add(error_text_ctrl, 0, wx.EXPAND | wx.ALL, 5)

            # 当提供日志文件路径且文件存在时，创建超链接控件
            if error_file_path and os.path.isfile(error_file_path):
                hyperlink = wx.adv.HyperlinkCtrl(scroll_win, label=error_file_path, url="")
                hyperlink.Bind(wx.adv.EVT_HYPERLINK, lambda event, path=error_file_path: self.on_open_log(event, path))
                sizer.Add(hyperlink, 0, wx.ALL | wx.CENTER, 5)

        # 设置滚动窗口的布局
        scroll_win.SetSizer(sizer)
        scroll_win.FitInside()  # 调整滚动区域大小
        scroll_win.Layout()

        # 创建对话框的外部布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(scroll_win, 1, wx.EXPAND | wx.ALL, 5)

        # 创建关闭按钮
        close_button = wx.Button(self, id=wx.ID_OK, label="关闭")
        main_sizer.Add(close_button, 0, wx.ALL | wx.CENTER, 5)

        # 应用整体布局
        self.SetSizer(main_sizer)

    def on_open_log(self, event, error_file_path):
        try:
            system_platform = platform.system()

            if system_platform == "Windows":
                os.startfile(error_file_path)
            elif system_platform == "Darwin":
                subprocess.run(["open", error_file_path], check=True)
            else:
                subprocess.run(["xdg-open", error_file_path], check=True)

        except Exception as e:
            print(f"Exception: {str(e)}")
            wx.MessageBox(f"无法打开日志文件: {str(e)}", "错误", wx.ICON_ERROR)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython 错误对话框示例")

        # 模拟错误信息和日志文件路径
        error_message = "示例错误信息" * 100
        error_file_path = r""

        # 创建并显示错误对话框
        error_dialog = MessageDialog(self.frame, message=error_message, title='信息', label='普通信息', file_path=error_file_path)
        error_dialog.ShowModal()
        error_dialog.Destroy()

        return True


class MyMultiApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython 错误对话框示例")

        # 模拟多个错误信息，使用字典格式
        errors = [
            {"error_message": "示例错误信息 1", "error_label": "错误信息 1", "error_file_path": r"path\to\log1.txt"},
            {"error_message": "示例错误信息 2", "error_label": "错误信息 2", "error_file_path": r"path\to\log2.txt"},
            {"error_message": "示例错误信息 3", "error_label": "错误信息 3", "error_file_path": r"path\to\log3.txt"},
            # 添加更多的错误信息来测试滚动
            {"error_message": "示例错误信息 4", "error_label": "错误信息 4", "error_file_path": r"path\to\log4.txt"},
            {"error_message": "示例错误信息 5", "error_label": "错误信息 5", "error_file_path": r"path\to\log5.txt"},
        ]

        # 创建并显示错误对话框
        if len(errors) == 1:
            error_dialog = MessageDialog(self.frame, message=errors[0]['error_message'], title='错误', label=errors[0]['error_label'],
                                         file_path=errors[0]['error_file_path'])
        else:
            error_dialog = MultiErrorDialog(self.frame, errors=errors)

        error_dialog.ShowModal()
        error_dialog.Destroy()

        return True


if __name__ == "__main__":
    # app = MyApp(False)
    app = MyMultiApp(False)
    app.MainLoop()
