import glm
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# 设置 OpenAI API 密钥
# openai.api_key = 'your-openai-api-key'  # 在此处替换为你的 API 密钥

def explain_job_with_ai1(job_name, index):
    """
    使用第一个 AI 函数（chatwithai）解释职业名称的意义。
    :param job_name: 职业名称
    :param index: 职业的索引
    :return: (索引, 职业名称, 职业解释)
    """
    prompt = f"请解释以下职业的含义：{job_name}\n\n请按照以下格式返回解释：\n职业：<职业名称>\n解释：<职业解释>"
    explanation = glm.chat_with_ai('user', prompt)
    return index, job_name, explanation

def explain_job_with_ai2(job_name, index):
    """
    使用第二个 AI 函数（chatwithai2）解释职业名称的意义。
    :param job_name: 职业名称
    :param index: 职业的索引
    :return: (索引, 职业名称, 职业解释)
    """
    prompt = f"请解释以下职业的含义：{job_name}\n\n请按照以下格式返回解释：\n职业：<职业名称>\n解释：<职业解释>"
    explanation = glm.chat_with_ai2('user', prompt)
    return index, job_name, explanation

def process_job_list(input_file_path, output_file_path):
    """
    处理职业清单文件并为每个职业生成解释，并保存为 CSV 文件。
    :param input_file_path: 输入文件路径（清单）
    :param output_file_path: 输出文件路径（CSV文件，包含解释）
    """
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        job_names = infile.readlines()

    # 使用 tqdm 显示进度条
    total_jobs = len(job_names)
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['职业', '解释'])  # 写入表头

        # 使用 ThreadPoolExecutor 并行化任务
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for i in range(total_jobs):
                job = job_names[i].strip()
                if job:
                    # 交替使用 chatwithai 和 chatwithai2
                    if i % 2 == 0:
                        futures.append(executor.submit(explain_job_with_ai1, job, i))
                    else:
                        futures.append(executor.submit(explain_job_with_ai2, job, i))

            # 等待所有线程完成，并按原始顺序处理结果
            results = []
            for future in tqdm(futures, desc="正在处理职业", unit="个职业"):
                results.append(future.result())  # 获取每个任务的结果

            # 按照索引对结果排序，确保顺序正确
            results.sort(key=lambda x: x[0])

            # 解析并写入 CSV 文件
            for index, job_name, explanation in results:
                # 解析返回的格式化结果
                job_name_clean = ""
                explanation_text = ""
                for line in explanation.split('\n'):
                    if line.startswith("职业："):
                        job_name_clean = line.replace("职业：", "").strip()
                    elif line.startswith("解释："):
                        explanation_text = line.replace("解释：", "").strip()

                # 写入 CSV 文件
                csv_writer.writerow([job_name_clean, explanation_text])

    print(f"解释已保存到 {output_file_path}")

# 示例：设置输入和输出文件路径
input_file_path = '../其他资料/职业清单.txt'  # 输入的职业清单文件路径
output_file_path = '../其他资料/职业清单解释.csv'  # 输出的职业解释 CSV 文件路径

# 调用函数处理文本
process_job_list(input_file_path, output_file_path)
