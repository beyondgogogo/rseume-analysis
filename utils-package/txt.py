import re


def extract_jobs_from_file(input_file_path, output_file_path):
    try:
        # 尝试读取文件内容，使用GBK编码以支持中文文件
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # 如果读取为空，尝试其他编码格式
        if not text:
            print("文件读取为空，尝试使用GBK编码...")
            with open(input_file_path, 'r', encoding='gbk') as file:
                text = file.read()

        # 输出读取的部分文本，查看格式
        print("读取到的文本：")
        print(text[:500])  # 只打印前500个字符进行调试

        # 使用正则表达式匹配每个职业名称
        job_pattern = re.compile(r'-\d{2}-\d{2}-\d{2}([^\n]*)')  # 匹配“数字-数字-数字”后面跟着的内容

        # 查找所有匹配的职业名称
        job_names = re.findall(job_pattern, text)

        # 如果没有找到职业名称，打印提示
        if not job_names:
            print("未能提取到职业名称，可能是正则表达式需要调整。")
        else:
            # 写入文件，每行一个职业名称
            with open(output_file_path, 'w', encoding='utf-8') as file:
                for job in job_names:
                    # 清理职业名称前后的空格
                    cleaned_job = job.strip()

                    # 使用正则去除非汉字字符
                    cleaned_job = re.sub(r'[^\u4e00-\u9fa5]', '', cleaned_job)

                    if cleaned_job:  # 如果清理后的职业名称不为空
                        file.write(cleaned_job + '\n')

            print(f"提取的职业名称已保存到 {output_file_path}")

    except Exception as e:
        print(f"读取文件或处理过程中发生错误：{e}")


# 示例：设置输入和输出文件路径
input_file_path = '../其他资料/国家职业分类.txt'  # 输入的文本文件路径
output_file_path = '../其他资料/职业清单.txt'  # 输出的职业清单文件路径

# 调用函数处理文本
extract_jobs_from_file(input_file_path, output_file_path)
