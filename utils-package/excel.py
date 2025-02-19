import xlrd

def extract_second_column_to_txt_xls(xls_file, txt_file):
    try:
        # 打开 .xls 文件
        workbook = xlrd.open_workbook(xls_file)
        sheet = workbook.sheet_by_index(0)  # 获取第一个工作表

        # 打开文本文件写入
        with open(txt_file, 'w', encoding='utf-8') as file:
            for row_idx in range(sheet.nrows):  # 遍历所有行
                cell_value = sheet.cell_value(row_idx, 1)  # 获取第二列的值 (索引1)
                if cell_value:  # 跳过空值
                    file.write(f"{cell_value}\n")
        print(f"成功提取第二列内容到 {txt_file}")
    except Exception as e:
        print(f"发生错误: {e}")

# 调用示例
xls_file_path = "../其他资料/W020190117549670267429.xls"  # 替换为你的.xls文件路径
txt_file_path = "../其他资料/证书大全.txt"  # 替换为你希望保存的txt文件路径
extract_second_column_to_txt_xls(xls_file_path, txt_file_path)
