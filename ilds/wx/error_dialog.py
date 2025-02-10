import wx
import subprocess
import platform
import os


class ErrorDialog(wx.Dialog):
    def __init__(self, parent, error_message, title="错误", error_label='错误信息', log_file_path=None):
        super().__init__(parent, title=title, size=(869, 969),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.error_message = error_message
        self.log_file_path = log_file_path

        panel = wx.Panel(self)

        # 创建用于显示错误信息的多行文本框
        error_text_ctrl = wx.TextCtrl(panel, value=self.error_message,
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # 创建关闭按钮
        close_button = wx.Button(panel, id=wx.ID_OK, label="关闭")

        # 创建布局管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        if error_label:
            error_label = wx.StaticText(panel, label=error_label)
            sizer.Add(error_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(error_text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        # 创建按钮用于打开错误日志文件
        if self.log_file_path and os.path.isfile(self.log_file_path):
            path_label = wx.StaticText(panel, label=f"文件：{self.log_file_path}")
            sizer.Add(path_label, 0, wx.ALL | wx.CENTER, 5)
            open_log_button = wx.Button(panel, label="打开错误日志")
            open_log_button.Bind(wx.EVT_BUTTON, self.on_open_log)
            sizer.Add(open_log_button, 0, wx.ALL | wx.CENTER, 5)

        sizer.Add(close_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

    def on_open_log(self, event):
        try:
            system_platform = platform.system()

            if system_platform == "Windows":
                os.startfile(self.log_file_path)
            elif system_platform == "Darwin":
                subprocess.run(["open", self.log_file_path], check=True)
            else:
                subprocess.run(["xdg-open", self.log_file_path], check=True)

        except Exception as e:
            print(f"Exception: {str(e)}")
            wx.MessageBox(f"无法打开日志文件: {str(e)}", "错误", wx.ICON_ERROR)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="wxPython 错误对话框示例")

        # 模拟错误信息和日志文件路径
        error_message = "示例错误信息" * 100
        log_file_path = r""

        # 创建并显示错误对话框
        error_dialog = ErrorDialog(self.frame, error_message=error_message, title="错误", error_label='错误信息', log_file_path=log_file_path)
        error_dialog.ShowModal()
        error_dialog.Destroy()

        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
