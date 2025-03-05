import os
import platform
import subprocess

import wx
import wx.adv


class MessageDialog(wx.Dialog):
    def __init__(self, parent, message, title="信息", label='信息', file_path=None, scroll_to_bottom=True):
        super().__init__(parent, title=title, size=(869, 969),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.message = message
        self.file_path = file_path

        panel = wx.Panel(self)

        # 创建用于显示信息的多行文本框
        self.message_text_ctrl = wx.TextCtrl(panel, value=self.message,
                                             style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # 如果 scroll_to_bottom 为 True, 滚动到最底部
        if scroll_to_bottom:
            self.scroll_to_bottom()

        # 创建按钮
        close_button = wx.Button(panel, id=wx.ID_OK, label="关闭")

        # 创建布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        if label:
            label_text = wx.StaticText(panel, label=label)
            main_sizer.Add(label_text, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(self.message_text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

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

    def scroll_to_bottom(self):
        # 设置光标位置到文本末尾
        self.message_text_ctrl.SetInsertionPointEnd()
        # 滚动文本框到光标位置
        self.message_text_ctrl.ShowPosition(self.message_text_ctrl.GetLastPosition())

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


class MultiMessageDialog(wx.Dialog):
    def __init__(self, parent, messages, title="信息", scroll_to_bottom=True):
        super().__init__(parent, title=f'{title} [{len(messages)}]', size=(869, 969),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        # 使用滚动窗口
        scroll_win = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.HSCROLL)
        scroll_win.SetScrollRate(5, 5)

        # 创建布局管理器
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 为每条信息创建一组控件
        for message in messages:
            label = message.get('label', '信息')
            message_text = message.get('message', '')
            file_path = message.get('file_path', None)

            # 创建信息的标签
            label_ctrl = wx.StaticText(scroll_win, label=label)
            sizer.Add(label_ctrl, 0, wx.ALL | wx.CENTER, 5)

            # 创建用于显示信息的多行文本框
            message_text_ctrl = wx.TextCtrl(scroll_win, value=message_text,
                                            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
            message_text_ctrl.SetMinSize((400, 150))  # 设置最小尺寸
            sizer.Add(message_text_ctrl, 0, wx.EXPAND | wx.ALL, 5)

            # 滚动到文本框底部
            if scroll_to_bottom:
                message_text_ctrl.ShowPosition(message_text_ctrl.GetLastPosition())

            # 当提供文件路径且文件存在时，创建超链接控件
            if file_path and os.path.isfile(file_path):
                hyperlink = wx.adv.HyperlinkCtrl(scroll_win, label=file_path, url="")
                hyperlink.Bind(wx.adv.EVT_HYPERLINK, lambda event, path=file_path: self.on_open_file(event, path))
                sizer.Add(hyperlink, 0, wx.ALL | wx.CENTER, 5)

                # 创建一个打开目录的按钮
                open_dir_button = wx.Button(scroll_win, label="打开文件所在目录")
                open_dir_button.Bind(wx.EVT_BUTTON, lambda event, path=file_path: self.on_open_directory(event, path))
                sizer.Add(open_dir_button, 0, wx.ALL | wx.CENTER, 5)

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

    def on_open_file(self, event, file_path):
        try:
            system_platform = platform.system()

            if system_platform == "Windows":
                os.startfile(file_path)
            elif system_platform == "Darwin":
                subprocess.run(["open", file_path], check=True)
            else:
                subprocess.run(["xdg-open", file_path], check=True)

        except Exception as e:
            print(f"Exception: {str(e)}")
            wx.MessageBox(f"无法打开文件: {str(e)}", "错误", wx.ICON_ERROR)

    def on_open_directory(self, event, file_path):
        try:
            directory = os.path.dirname(file_path)
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


class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython 错误对话框示例")

        # 模拟错误信息和日志文件路径
        error_message = "示例错误信息" * 100 + "示例错误信息\n" * 100
        error_file_path = r""

        # 创建并显示错误对话框
        error_dialog = MessageDialog(self.frame, message=error_message, title='信息', label='普通信息', file_path=error_file_path, scroll_to_bottom=True)
        error_dialog.ShowModal()
        error_dialog.Destroy()

        return True


class MyMultiApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython 错误对话框示例")

        # 模拟多个错误信息，使用字典格式
        errors = [
            {"message": "示例错误信息 1\n" * 100, "label": "错误信息 1", "file_path": r"path\to\log1.txt"},
            {"message": "示例错误信息 2\n" * 100, "label": "错误信息 2", "file_path": r"path\to\log2.txt"},
            {"message": "示例错误信息 3\n" * 100, "label": "错误信息 3", "file_path": r"path\to\log3.txt"},
            # 添加更多的错误信息来测试滚动
            {"message": "示例错误信息 4\n" * 100, "label": "错误信息 4", "file_path": r"path\to\log4.txt"},
            {"message": "示例错误信息 5\n" * 100, "label": "错误信息 5", "file_path": r"path\to\log5.txt"},
        ]

        # 创建并显示错误对话框
        if len(errors) == 1:
            error_dialog = MessageDialog(self.frame, message=errors[0]['error_message'], title='错误', label=errors[0]['error_label'],
                                         file_path=errors[0]['error_file_path'])
        else:
            error_dialog = MultiMessageDialog(self.frame, messages=errors)

        error_dialog.ShowModal()
        error_dialog.Destroy()

        return True


if __name__ == "__main__":
    # app = MyApp(False)
    app = MyMultiApp(False)
    app.MainLoop()
