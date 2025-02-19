import logging
import os
import glm

# 设置日志
logging.basicConfig(level=logging.DEBUG)


class EducationLabelsService:

    # 提取教育经历标签
    def get_education_labels(self, resume_id):
        try:
            # 根据简历ID找到对应的文件夹路径
            folder_name = f"resume_{resume_id}"
            if not os.path.exists(folder_name):
                logging.error(f"简历文件夹 {folder_name} 不存在")
                return {"message": f"简历文件夹 {folder_name} 不存在"}

            # 找到教育经历文件并读取内容
            edu_file_path = os.path.join(folder_name, "教育经历.txt")
            if not os.path.exists(edu_file_path):
                logging.error(f"教育经历文件 {edu_file_path} 不存在")
                return {"message": f"教育经历文件 {edu_file_path} 不存在"}

            # 读取教育经历内容
            with open(edu_file_path, "r", encoding="utf-8") as f:
                education_content = f.read().strip()
            if not education_content:
                logging.error("教育经历内容为空")
                return {"message": "教育经历内容为空"}

            # 读取教育标签文件（education_labels.txt）
            labels_file_path = "labels/education_labels.txt"
            if not os.path.exists(labels_file_path):
                logging.error(f"标签文件 {labels_file_path} 不存在")
                return {"message": f"标签文件 {labels_file_path} 不存在"}

            # 读取标签内容
            with open(labels_file_path, "r", encoding="utf-8") as f:
                labels_content = f.read().strip()
            if not labels_content:
                logging.error("标签文件内容为空")
                return {"message": "标签文件内容为空"}

            # 构造prompt，将教育标签内容加到prompt中，并明确要求返回标签
            prompt = f"请根据以下教育经历为我打标签。以下是一些标签，您只需从这些标签中挑选相关的内容，不要添加其他标签。\n\n{education_content}\n\n【以下是标签列表：】\n{labels_content}\n\n请根据教育经历和标签为我生成相应的标签。只返回标签，不需要其他解释。"

            # 调用GLM模型为教育经历生成标签
            logging.info(f"开始为简历 {resume_id} 的教育经历生成标签")
            labels = glm.chat_with_ai("user", prompt)

            # 处理返回结果，确保只返回标签
            if labels:
                # 确保返回的标签是以逗号分隔的列表，去掉多余的符号和空白字符
                label_list = [label.strip() for label in labels.strip().split("\n") if label.strip()]
                return {"message": "标签生成成功", "labels": label_list}
            else:
                logging.error("未能生成标签")
                return {"message": "未能生成标签"}

        except Exception as e:
            logging.error(f"获取教育经历标签时发生错误：{str(e)}")
            return {"message": f"获取教育经历标签时发生错误：{str(e)}"}
