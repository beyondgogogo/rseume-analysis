import glm
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


# 设置 OpenAI API 密钥
# openai.api_key = 'your-openai-api-key'  # 在此处替换为你的 API 密钥

def explain_certificates_with_ai(cert_name, index):
    """
    使用 AI 扩展证书及其相关证书信息。
    :param cert_name: 证书名称
    :param index: 证书的索引
    :return: (索引, 证书名称, 扩展的证书信息)
    """
    # 生成给定证书的扩展提示
    prompt = f"请根据这个证书，拓展出相关的证书，返回证书名称、权威性和解释：{cert_name}\n\n请按照以下格式返回每个证书的信息：\n证书名称：<证书名称>\n权威性：<权威性>\n解释：<证书解释>"

    # 向 AI 提交请求，获取相关证书
    explanation = glm.chat_with_ai('user', prompt)  # 调用你需要的 AI 函数

    print(explanation)

    # 假设 AI 返回的格式是证书信息按行分隔
    return index, cert_name, explanation


def process_certificates(cert_file_path, output_file_path):
    """
    处理证书文件并为每个证书生成扩展解释，并保存为 CSV 文件。
    :param cert_file_path: 输入文件路径（证书清单）
    :param output_file_path: 输出文件路径（CSV文件，包含解释）
    """
    with open(cert_file_path, 'r', encoding='utf-8') as infile:
        certificate_names = infile.readlines()

    # 使用 tqdm 显示进度条
    total_certificates = len(certificate_names)
    processed_count = 0  # 用于统计已处理的证书数量

    with open(output_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['证书', '类型', '权威性', '解释'])  # 写入表头

        # 使用 ThreadPoolExecutor 并行处理证书
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for index, cert_name in enumerate(certificate_names):
                cert_name = cert_name.strip()  # 去掉换行符

                if cert_name:  # 排除空行
                    futures.append(executor.submit(explain_certificates_with_ai, cert_name, index))

            # 获取并写入扩展证书的解释
            for future in tqdm(futures, total=total_certificates, desc="处理中"):
                index, cert_name, explanation = future.result()

                # 假设 explanation 格式是多个证书信息按换行符分隔
                # 解析 AI 返回的扩展信息
                related_certificates = explanation.split("\n")
                for related_cert in related_certificates:
                    parts = related_cert.split("\n")
                    if len(parts) < 3:
                        continue

                    cert_name_exp = parts[0].split("：")[1] if "证书名称：" in parts[0] else ""
                    authority = parts[1].split("：")[1] if "权威性：" in parts[1] else ""
                    description = parts[2].split("：")[1] if "解释：" in parts[2] else ""

                    # 将扩展后的证书信息写入 CSV
                    csv_writer.writerow([cert_name_exp, cert_name, authority, description])
                    processed_count += 1

                    # 每处理10条数据保存一次
                    if processed_count % 10 == 0:
                        csvfile.flush()  # 确保写入文件

    print(f"扩展解释已保存到 {output_file_path}")


# 示例：设置输入和输出文件路径
cert_file_path = '../其他资料/证书大全new.txt'  # 证书清单文件路径
output_file_path = '../其他资料/证书清单解释.csv'  # 输出的证书解释 CSV 文件路径

# 调用函数处理文本
process_certificates(cert_file_path, output_file_path)
