from openpyxl import load_workbook

from _.不对外公开 import *
from ilds.excel import SheetImageLoader, parse_id
from ilds.file import validate_title

wb = load_workbook(excel_file)
print(excel_file)

# sheet = wb['Sheet1']
sheet = wb['0赞起结抖音破万赞前三名奖励288以报备为准冲冲冲（收集结果）']

# 将工作表放入加载器
image_loader = SheetImageLoader(excel_file, wb, sheet)
# image_loader.is_wps = True
print(f'is_wps {image_loader.is_wps}')

# 并从指定单元格获取 Pillow 图像
cell = 'I3'
# cell = '=_xlfn.DISPIMG("ID_BED31091C6EF438D80F4DF82AFDDB362",1)'
print(parse_id(cell))
image_raw = image_loader.get(cell, is_print=True)

save_file = f'{validate_title(cell)}.png'
print(f'save_file:{save_file}')
image_loader.save_image(cell, save_file)

# 检查单元格中是否有图像
if image_loader.image_in('I4'):
    print("有图片!")

image_loader.close()
