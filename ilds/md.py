# -*- coding: utf-8 -*-
#
# ---------------------------------------
#   程序：md.py
#   版本：0.3
#   作者：lds
#   日期：2019-01-02
#   语言：Python 3.X
#   说明：处理 markdown 的函数集合
"""
20190102 html_to_md 添加按序号重命名图片文件
20190319 添加 md_to_html，转换 markdown 为 html 文件
"""
# ---------------------------------------

import os
import re
import shutil

import chardet
import requests
import html2text
import mistune

# 匹配图像链接的正则表达式 # *([^\n]+?) *#* *(?:\n+|$)   ![图像](../images/00038.jpeg)
IMG_LINK_COMPILE = re.compile(r'!\[.*?\]\((.*?)\)')

TEMPLATES = '''
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title></title>
    </head>
    <body>

HTML_TEMPLATES

    </body>
</html>'''


def html_to_md(html_file, save_file=None, end=False, rename_img=False, img_start_index=0):
    """
    转换 html 为 markdown

    例子：
    save_file = html_to_md(html_file)
    print('转换html：%s 为 markdown：%s' % (html_file, save_file))

    :param html_file: 要转换的文件
    # :param save_to:
    # :param img_fun: 本来打算用来修复图片链接，但是有问题所以暂停使用
    :param save_file: 保存文件名（默认是）
    :param end:
    :param rename_img: 重命名 md 文件中的图片为序号(如：000001.jpg)
    :param img_start_index: 开始重命名图片的序号
    :return:
    """

    # html = open(html_file, 'r', encoding='utf-8').read()
    # with open(html_file, 'r', encoding='utf-8') as html:
    with open(html_file, 'rb') as fp:
        # import chardet
        # 先能识别文件的编码方式，然后根据此编码方式进行对文件编码，获取文件内容。 """
        html_data = fp.read()
        result = chardet.detect(html_data)
        file_content = html_data.decode(encoding=result['encoding'])

        text_maker = html2text.HTML2Text()
        text_maker.body_width = 0
        # text_maker.ignore_links = True # 忽略链接
        # text_maker.kypass_tables = False # 循环表
        text_maker.kypass_tables = True

        text = text_maker.handle(file_content)  # html.read()

        # 处理表格有多余空行的问题
        text = re.sub('\n\n\| \n\n', '|', text)  # 替换 | 符号的换行
        text = re.sub('\n  \n', '\n', text)  # 替换两个换行为一个
        # print(text)

        file_path, file_name = os.path.split(html_file)  # 分离 文件路径 文件名+扩展名
        # print(file_path, file_name)

        # 默认文件名
        if save_file is None:
            f_name, _ = os.path.splitext(html_file)
            save_file = f_name + ".md"
        else:
            f_name, _ = os.path.splitext(save_file)

        save_to = os.path.dirname(save_file)

        # 处理图片文件
        link_result = IMG_LINK_COMPILE.findall(text)
        if link_result:
            # print(f_line, link_result)
            # c = 0
            # continue
            for result in link_result:
                # print(result)

                # if img_fun is not None:
                #     result = img_fun(result)

                # 图片名称
                image_name = os.path.split(result)[1]
                if rename_img:
                    _ext = os.path.splitext(image_name)[1]
                    if _ext:
                        image_name = "%06d%s" % (img_start_index, _ext)
                    else:
                        image_name = "%06d.jpg" % (img_start_index)
                # 图片文件
                file = os.path.join(file_path, result)

                # 图片存放路径
                save_dir_name = os.path.split(f_name)[-1]
                save_img_path = os.path.join(save_to, 'img', save_dir_name)
                if not os.path.exists(save_img_path):
                    os.makedirs(save_img_path)

                save_img = os.path.join(save_img_path, image_name)
                # print('保存路径：', save_img_path, '图片：', save_img)

                if os.path.exists(file):
                    # print('文件已经存在', file)
                    shutil.copy(file, save_img)
                else:
                    try:
                        res = requests.get(result, verify=False)
                        with open(save_img, 'wb') as f:
                            f.write(res.content)
                        # print('下载图片：', result, '保存路径：', save_img)
                    except Exception as e:
                        print('文件', file, e)

                new_image = f'./img/{save_dir_name}/{image_name}'
                text = text.replace(result, new_image)
                # print(new_image)
                img_start_index += 1

        with open(save_file, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
            # 在结尾添加文件名
            if end:
                output_file.write('\n\n\n')
                output_file.write(file_name)

    # print('转换html：%s 为 markdown：%s' % (html_file, save_file))
    # print(save_file)
    return save_file


def md_to_html(md_file, save_file=None):
    """
    转换 markdown 为 html 文件
    """

    with open(md_file, 'r', encoding='utf-8') as text:
        renderer = mistune.Renderer(escape=True, hard_wrap=True)
        # 使用渲染器
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(text.read())

        html = TEMPLATES.replace('HTML_TEMPLATES', html)

        # 如果没有指定保存文件名，那么让我们返回转换好的html内容
        if save_file is None:
            # save_file = md_file + ".html"
            return html

        with open(save_file, 'w', encoding='utf-8') as output_file:
            output_file.write(html)

    # print(save_file)
    return save_file


def doc():
    """
    打印模块说明文档
    """
    doc_text = """
    """
    doc_text += '\n'
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=html_to_md)
    doc_text += '{fun.__name__}{fun.__doc__}\n'.format(fun=md_to_html)

    print(doc_text)


if __name__ == '__main__':
    # 记录运行时间 --------------------------------------------------
    from time import time, sleep

    start_time = t1 = time()

    doc()

    print('运行时间 %.2f 秒' % (time() - start_time))
