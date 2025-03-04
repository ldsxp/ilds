import wx
import datetime


class StatusBarMixin:
    """
    添加自定义的状态栏的 Mixin 类
    """

    def __init__(self, num_fields=3, field_widths=None):
        self.num_fields = num_fields
        self.field_widths = field_widths if field_widths else [-1] * num_fields

        # 创建具有自定义字段数量的状态栏
        self.status_bar = self.CreateStatusBar(self.num_fields)

        # 设置每个字段的比例宽度
        self.status_bar.SetStatusWidths(self.field_widths)

    def get_field_clicked(self, event):
        """返回被点击的字段索引或 -1。如果点击区域不在任何字段上则返回 -1。"""
        pos = event.GetPosition()
        for i in range(self.status_bar.GetFieldsCount()):
            rect = self.status_bar.GetFieldRect(i)
            if rect.Contains(pos):
                return i
        return -1

    def is_event_in_status_bar_field(self, event, status_bar, field_index):
        """
        检查事件是否发生在状态栏的指定字段中
        """
        return status_bar.GetFieldRect(field_index).Contains(event.GetPosition())


class StatusBar(StatusBarMixin):
    def __init__(self, num_fields=3, field_widths=None):
        StatusBarMixin.__init__(self, num_fields, field_widths)

        # 绑定鼠标事件，我们在同时支持左键单击和双击的时候，经常不能正确获取双击数据，所以我们要选择一个使用
        self.status_bar.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.status_bar.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.status_bar.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

        # 定时器，用于状态栏时间更新
        self.timer = wx.Timer(self)
        # 设置定时器，每秒更新一次
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(1000)

    def on_left_down(self, event):
        # 处理左键单击
        field = self.get_field_clicked(event)
        if field != -1:
            wx.MessageBox(f"左键单击在状态栏的第 {field + 1} 列", "信息", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("左键单击在状态栏的未知位置", "信息", wx.OK | wx.ICON_WARNING)
        event.Skip()

    def on_left_dclick(self, event):
        # 处理左键双击
        field = self.get_field_clicked(event)
        if field != -1:
            wx.MessageBox(f"左键双击在状态栏的第 {field + 1} 列", "信息", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("左键双击在状态栏的未知位置", "信息", wx.OK | wx.ICON_WARNING)
        event.Skip()

    def on_right_down(self, event):
        # 处理右键单击
        field = self.get_field_clicked(event)
        if field != -1:
            menu = wx.Menu()

            open_file_menu = wx.MenuItem(menu, wx.ID_ANY, '打开文件', )
            menu.Append(open_file_menu)
            self.Bind(wx.EVT_MENU, self.OnOpenFile, open_file_menu)

            self.PopupMenu(menu)
            menu.Destroy()
        else:
            wx.MessageBox("右键单击在状态栏的未知位置", "信息", wx.OK | wx.ICON_WARNING)
        event.Skip()

    def update_status(self):
        """更新状态栏，下面是根据字段数量显示时间分为若干部分（小时、分钟和秒）的例子"""
        now = datetime.datetime.now()
        if self.num_fields > 0:
            self.SetStatusText(f'小时: {now.hour:02}', 0)
        if self.num_fields > 1:
            self.SetStatusText(f'分钟: {now.minute:02}', 1)
        if self.num_fields > 2:
            self.SetStatusText(f'秒: {now.second:02}', 2)
        # 进行额外字段的其他配置
        for i in range(3, self.num_fields):
            self.SetStatusText(f'字段 {i + 1}', i)

    def on_timer(self, event):
        """定时更新状态栏"""
        self.update_status()

    def OnOpenFile(self, event):
        print('选择打开文件')
        event.Skip()


class MyFrame(wx.Frame, StatusBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 使用自定义字段数量和宽度初始化状态栏 Mixin
        # 提供字段数量和宽度
        num_fields = 4
        field_widths = [-2, -1, -1, -2]
        StatusBar.__init__(self, num_fields=num_fields, field_widths=field_widths)

        panel = wx.Panel(self)


class MyApp(wx.App):
    def OnInit(self):
        # 在这里，可以自定义状态栏的字段数量和宽度
        frame = MyFrame(None, title="自定义状态栏", size=(400, 150), )
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
