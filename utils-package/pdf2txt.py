import re

import PyPDF2


def pdf_to_text(pdf_path, txt_path):
    # 打开PDF文件
    with open(pdf_path, 'rb') as pdf_file:
        # 创建PDF阅读器对象
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # 获取PDF页数
        num_pages = len(pdf_reader.pages)

        # 打开文本文件来写入提取的文本
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # 逐页读取PDF内容
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # 按行处理文本
                if text:  # 如果提取的文本不为空
                    lines = text.split('\n')
                    for line in lines:
                        # 使用正则表达式去掉行首的数字和可能的空格
                        cleaned_line = re.sub(r'^\d+\s*', '', line)
                        txt_file.write(cleaned_line)
                        txt_file.write("\n")  # 每行之间添加换行符

    print(f"PDF内容已成功保存到 {txt_path}")


# 使用示例
pdf_path = '../其他资料/国家职业分类.pdf'  # 你的PDF文件路径
txt_path = '../其他资料/国家职业分类.txt'  # 输出的TXT文件路径
pdf_to_text(pdf_path, txt_path)
