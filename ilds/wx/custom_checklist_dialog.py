import wx


class CustomCheckListDialog(wx.Dialog):
    """
    此类是一个自定义的多选对话框，该对话框可以显示项目列表，允许用户选择一个或多个项目。并支持添加和删除项目
    """

    def __init__(self, parent, title, choices, default_selections=None):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.original_choices = choices[:]  # 保存初始状态
        self.choices = choices[:]  # 工作列表
        self.default_selections = default_selections or []
        self.deleted_items = []  # 删除的项目
        self.added_items = []  # 新增的项目
        self.is_modified = False  # 标记列表是否被修改
        self.InitUI()
        self.SetSize((400, 500))
        self.Centre()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.checklist = wx.CheckListBox(self, choices=self.choices)
        self.checklist.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckItem)
        self.checklist.Bind(wx.EVT_LISTBOX_DCLICK, self.OnEditCheckedItem)
        vbox.Add(self.checklist, 1, wx.EXPAND | wx.ALL, 10)

        self.checklist.SetCheckedItems(self.default_selections)

        button_hbox = wx.BoxSizer(wx.HORIZONTAL)

        add_button = wx.Button(self, label='添加项目')
        add_button.Bind(wx.EVT_BUTTON, self.OnAddItem)
        button_hbox.Add(add_button, 1, wx.EXPAND | wx.RIGHT, 5)

        remove_button = wx.Button(self, label='删除选中项目')
        remove_button.Bind(wx.EVT_BUTTON, self.OnRemoveCheckedItems)
        button_hbox.Add(remove_button, 1, wx.EXPAND | wx.LEFT, 5)

        select_all_button = wx.Button(self, label='全选')
        select_all_button.Bind(wx.EVT_BUTTON, self.OnSelectAll)
        button_hbox.Add(select_all_button, 1, wx.EXPAND | wx.LEFT, 5)

        deselect_all_button = wx.Button(self, label='取消选择')
        deselect_all_button.Bind(wx.EVT_BUTTON, self.OnDeselectAll)
        button_hbox.Add(deselect_all_button, 1, wx.EXPAND | wx.LEFT, 5)

        vbox.Add(button_hbox, 0, wx.EXPAND | wx.ALL, 10)

        self.selected_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        self.selected_text_ctrl.SetMinSize((-1, 100))
        vbox.Add(self.selected_text_ctrl, 2, wx.EXPAND | wx.ALL, 10)

        ok_button = wx.Button(self, wx.ID_OK, label='确定')
        cancel_button = wx.Button(self, wx.ID_CANCEL, label='取消')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(ok_button, 1, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(cancel_button, 1, wx.EXPAND | wx.LEFT, 5)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)
        self.UpdateSelectedText()

    def OnAddItem(self, event):
        new_item = wx.GetTextFromUser("输入新项目", "添加项目")
        if new_item:
            self.checklist.Append(new_item)
            self.choices.append(new_item)
            self.added_items.append(new_item)  # 记录新增项目
            self.is_modified = True  # 标记列表已被修改

    def OnEditCheckedItem(self, event):
        index = self.checklist.GetSelection()
        if index == wx.NOT_FOUND:
            return

        current_value = self.choices[index]
        new_value = wx.GetTextFromUser(f"编辑内容: {current_value}", "编辑选中项目", current_value)
        if new_value and new_value != current_value:
            self.checklist.SetString(index, new_value)
            self.choices[index] = new_value
            self.is_modified = True  # 标记列表已被修改
            self.UpdateSelectedText()

    def OnRemoveCheckedItems(self, event):
        checked_indices = [i for i in range(len(self.choices)) if self.checklist.IsChecked(i)]
        for index in reversed(checked_indices):
            self.deleted_items.append(self.choices[index])
            self.checklist.Delete(index)
            del self.choices[index]
        if checked_indices:
            self.is_modified = True  # 标记列表已被修改
        self.UpdateSelectedText()

    def OnSelectAll(self, event):
        self.checklist.SetCheckedItems(list(range(len(self.choices))))
        self.UpdateSelectedText()

    def OnDeselectAll(self, event):
        self.checklist.SetCheckedItems([])
        self.UpdateSelectedText()

    def OnCheckItem(self, event):
        # 因为勾选不改变列表内容，不在这里标记 is_modified
        self.UpdateSelectedText()

    def UpdateSelectedText(self):
        checked_items = self.GetCheckedItems()
        if checked_items:
            self.selected_text_ctrl.SetValue(f"选中（{len(checked_items)}个）: {', '.join(checked_items)}")
        else:
            self.selected_text_ctrl.SetValue("没有选择项目")

    def GetCheckedItems(self):
        return [self.choices[i] for i in range(len(self.choices)) if self.checklist.IsChecked(i)]

    def GetDeletedItems(self):
        return self.deleted_items

    def GetAddedItems(self):
        return self.added_items

    def IsModified(self):
        return self.is_modified

    def GetRemainingItems(self):
        return self.choices


if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            choices = ["项目 {}".format(i) for i in range(1, 101)]  # 增加更多项目以测试滚动条
            default_selections = [0, 2]
            dialog = CustomCheckListDialog(None, "选择项目", choices, default_selections)

            if dialog.ShowModal() == wx.ID_OK:
                selected_items = dialog.GetCheckedItems()
                deleted_items = dialog.GetDeletedItems()
                added_items = dialog.GetAddedItems()
                remaining_items = dialog.GetRemainingItems()
                is_modified = dialog.IsModified()

                print("选中的项目:", selected_items)
                print("删除的项目:", deleted_items)
                print("新增的项目:", added_items)
                print("剩余的项目:", remaining_items)
                print("列表是否修改:", is_modified)
            dialog.Destroy()

            return True  # 返回 True 以继续运行应用程序的事件循环，如果像本示例一样只有一个对话框，返回 False 也是合理的，因为关闭对话框程序也结束了


    app = MyApp()
    app.MainLoop()
