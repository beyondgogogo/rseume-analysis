import logging
import os
import glm

# 设置日志
logging.basicConfig(level=logging.DEBUG)


class ResumeLabelingService:

    def __init__(self):
        # 设置标签文件路径
        self.label_paths = {
            "basic": "labels/basic_labels.txt",
            "education": "labels/education_labels.txt",
            "skills": "labels/skills_labels.txt",
            "work_experience": "labels/work_experience_labels.txt"
        }

    # 读取标签文件
    def _read_labels(self, label_type):
        try:
            label_file = self.label_paths.get(label_type)
            if not os.path.exists(label_file):
                logging.error(f"标签文件 {label_file} 不存在")
                return None

            with open(label_file, "r", encoding="utf-8") as f:
                labels_content = f.read().strip()

            if not labels_content:
                logging.error(f"标签文件 {label_file} 内容为空")
                return None

            return labels_content
        except Exception as e:
            logging.error(f"读取标签文件 {label_type} 时发生错误：{str(e)}")
            return None

    # 构造prompt并调用GLM模型
    def _generate_labels(self, resume_id, content, label_type):
        try:
            # 获取标签列表
            labels_content = self._read_labels(label_type)
            if not labels_content:
                return {"message": f"标签文件 {label_type} 不存在或为空"}

            # 构造prompt
            prompt = f"请根据以下内容为我打标签。以下是一些标签，您只需从这些标签中挑选相关的内容，不要添加其他标签。\n\n{content}\n\n【以下是标签列表：】\n{labels_content}\n\n请根据内容和标签为我生成相应的标签。只返回标签，不需要其他解释。"

            # 调用GLM模型为简历生成标签
            logging.info(f"开始为简历 {resume_id} 的{label_type}生成标签")
            labels = glm.chat_with_ai("user", prompt)

            # 处理返回结果，确保只返回标签
            if labels:
                label_list = [label.strip() for label in labels.strip().split("\n") if label.strip()]
                return {"message": f"{label_type}标签生成成功", "labels": label_list}
            else:
                logging.error(f"{label_type}标签生成失败")
                return {"message": f"{label_type}标签生成失败"}

        except Exception as e:
            logging.error(f"生成{label_type}标签时发生错误：{str(e)}")
            return {"message": f"生成{label_type}标签时发生错误：{str(e)}"}

    # 提取基本信息标签
    def get_basic_labels(self, resume_id):
        try:
            folder_name = f"resume_{resume_id}"
            basic_file_path = os.path.join(folder_name, "个人基本信息.txt")

            if not os.path.exists(basic_file_path):
                logging.error(f"基本信息文件 {basic_file_path} 不存在")
                return {"message": f"基本信息文件 {basic_file_path} 不存在"}

            with open(basic_file_path, "r", encoding="utf-8") as f:
                basic_content = f.read().strip()
            if not basic_content:
                logging.error("基本信息内容为空")
                return {"message": "基本信息内容为空"}

            # 调用GLM生成基本信息标签
            return self._generate_labels(resume_id, basic_content, "basic")

        except Exception as e:
            logging.error(f"获取基本信息标签时发生错误：{str(e)}")
            return {"message": f"获取基本信息标签时发生错误：{str(e)}"}

    # 提取教育经历标签
    def get_education_labels(self, resume_id):
        try:
            folder_name = f"resume_{resume_id}"
            edu_file_path = os.path.join(folder_name, "教育经历.txt")

            if not os.path.exists(edu_file_path):
                logging.error(f"教育经历文件 {edu_file_path} 不存在")
                return {"message": f"教育经历文件 {edu_file_path} 不存在"}

            with open(edu_file_path, "r", encoding="utf-8") as f:
                education_content = f.read().strip()
            if not education_content:
                logging.error("教育经历内容为空")
                return {"message": "教育经历内容为空"}

            # 调用GLM生成教育经历标签
            return self._generate_labels(resume_id, education_content, "education")

        except Exception as e:
            logging.error(f"获取教育经历标签时发生错误：{str(e)}")
            return {"message": f"获取教育经历标签时发生错误：{str(e)}"}

    # 提取技能标签
    def get_skills_labels(self, resume_id):
        try:
            folder_name = f"resume_{resume_id}"
            skills_file_path = os.path.join(folder_name, "相关技能.txt")

            if not os.path.exists(skills_file_path):
                logging.error(f"技能文件 {skills_file_path} 不存在")
                return {"message": f"技能文件 {skills_file_path} 不存在"}

            with open(skills_file_path, "r", encoding="utf-8") as f:
                skills_content = f.read().strip()
            if not skills_content:
                logging.error("技能内容为空")
                return {"message": "技能内容为空"}

            # 调用GLM生成技能标签
            return self._generate_labels(resume_id, skills_content, "skills")

        except Exception as e:
            logging.error(f"获取技能标签时发生错误：{str(e)}")
            return {"message": f"获取技能标签时发生错误：{str(e)}"}

    # 提取工作经验和实习经历标签
    def get_work_experience_labels(self, resume_id):
        try:
            folder_name = f"resume_{resume_id}"
            work_file_path = os.path.join(folder_name, "工作经历.txt")
            internship_file_path = os.path.join(folder_name, "实习经历.txt")

            # 初始化工作经历内容为空
            work_experience_content = ""

            # 如果工作经历文件存在，则读取内容
            if os.path.exists(work_file_path):
                with open(work_file_path, "r", encoding="utf-8") as f:
                    work_experience_content = f.read().strip()
                if not work_experience_content:
                    logging.error("工作经历文件内容为空")
                    return {"message": "工作经历内容为空"}
            else:
                logging.info(f"工作经历文件 {work_file_path} 不存在")

            # 如果实习经历文件存在，则读取内容并附加
            if os.path.exists(internship_file_path):
                with open(internship_file_path, "r", encoding="utf-8") as f:
                    internship_content = f.read().strip()
                if internship_content:
                    work_experience_content += "\n" + internship_content
            else:
                logging.info(f"实习经历文件 {internship_file_path} 不存在")

            # 如果工作经历内容为空，则返回相应的提示
            if not work_experience_content:
                logging.error("工作经历和实习经历文件均为空")
                return {"message": "工作经历和实习经历文件均为空"}

            # 调用GLM生成工作经历和实习经历标签
            return self._generate_labels(resume_id, work_experience_content, "work_experience")

        except Exception as e:
            logging.error(f"获取工作经历和实习经历标签时发生错误：{str(e)}")
            return {"message": f"获取工作经历和实习经历标签时发生错误：{str(e)}"}


        except Exception as e:
            logging.error(f"获取工作经历标签时发生错误：{str(e)}")
            return {"message": f"获取工作经历标签时发生错误：{str(e)}"}

