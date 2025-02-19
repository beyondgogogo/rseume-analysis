import logging
import os
import pandas as pd
import PyPDF2
import glm
from utils import generate_timestamp
import re

# 设置日志
logging.basicConfig(level=logging.DEBUG)


class ResumeService:

    # 提取PDF文件中的文本
    def extract_text_from_pdf(self, file):
        try:
            logging.info(f"开始提取PDF文本：{file.name if hasattr(file, 'name') else '未命名文件'}")
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                    logging.debug(f"成功提取第 {page_num + 1} 页的文本")
                else:
                    logging.warning(f"第 {page_num + 1} 页未提取到文本")
            if not text:
                logging.error("提取的文本为空，请检查PDF文件是否有效或格式正确。")
                raise ValueError("提取的PDF文本为空")
            logging.info("成功提取PDF文本")
            return text
        except Exception as e:
            logging.error(f"提取PDF文本时发生错误：{str(e)}")
            raise Exception(f"提取PDF文本时发生错误：{str(e)}")

    # 调用GLM模型进行简历分块
    def split_resume_with_glm(self, extracted_text):
        try:
            logging.info("开始调用GLM模型分块简历内容")
            prompt = f"请将以下简历内容分成几个部分，包括但不限于：个人基本信息、教育经历、实习经历、工作经历、项目经历、相关技能等。\n\n{extracted_text}"

            # 调用GLM模型并返回分块结果
            result = glm.chat_with_ai("user", prompt)
            logging.info("简历内容分块成功")
            # 进行格式检查
            if not result or not isinstance(result, str):
                logging.error("返回的简历分块内容无效或格式不正确")
                raise ValueError("GLM返回的简历分块内容无效")
            return result
        except Exception as e:
            logging.error(f"调用GLM模型分块简历内容时发生错误：{str(e)}")
            raise Exception(f"调用GLM模型分块简历内容时发生错误：{str(e)}")

    # 清理简历内容中的Markdown标记
    def clean_markdown(self, content):
        # 移除 Markdown 标题（###）
        content = re.sub(r'###\s+', '', content)
        # 移除 Markdown 列表项（-）
        content = re.sub(r'-\s+', '', content)
        return content.strip()

    # 保存每个简历部分为单独的txt文件
    def save_resume_to_txt(self, resume_id, resume_parts):
        try:
            # 创建以时间戳命名的文件夹
            folder_name = f"resume_{resume_id}"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                logging.info(f"创建文件夹：{folder_name}")
            else:
                logging.warning(f"文件夹 {folder_name} 已存在")

            # 分块后的简历数据应该是按部分和条目分开的
            resume_data = resume_parts.split("\n")
            current_section = ""
            current_content = []

            # 用于将简历部分按标题和内容结构化
            section_titles = ["个人基本信息", "教育经历", "实习经历", "实习经历", "项目经历", "相关技能"]

            for part in resume_data:
                part = part.strip()

                # 如果发现一个新部分的标题
                for title in section_titles:
                    if part.startswith(f"### {title}"):  # 匹配到标题
                        if current_section:  # 如果当前部分有内容
                            # 清理Markdown格式并保存
                            cleaned_content = self.clean_markdown("\n".join(current_content))
                            file_name = os.path.join(folder_name, f"{current_section}.txt")
                            with open(file_name, "w", encoding="utf-8") as f:
                                f.write(cleaned_content)
                            logging.debug(f"已保存文件：{file_name}")

                        current_section = title  # 更新当前部分标题
                        current_content = [part]  # 将标题作为内容的一部分
                        logging.debug(f"检测到新部分标题：{current_section}")
                        break
                else:
                    # 如果不是部分标题，则为内容条目
                    if part:  # 非空条目
                        current_content.append(part)

            # 最后一个部分的内容
            if current_section:
                cleaned_content = self.clean_markdown("\n".join(current_content))
                file_name = os.path.join(folder_name, f"{current_section}.txt")
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(cleaned_content)
                logging.debug(f"已保存文件：{file_name}")

            logging.info(f"简历内容成功保存到文件夹：{folder_name}")
            return folder_name
        except Exception as e:
            logging.error(f"保存简历到txt文件时发生错误：{str(e)}")
            raise Exception(f"保存简历到txt文件时发生错误：{str(e)}")

    # 处理简历的主流程
    def process_resume(self, file):
        try:
            logging.info("开始处理简历流程")

            # 提取PDF文件中的文本
            extracted_text = self.extract_text_from_pdf(file)

            # 调用GLM模型进行简历分块
            resume_parts = self.split_resume_with_glm(extracted_text)

            # 生成当前时间戳作为简历号
            resume_id = generate_timestamp()
            logging.info(f"生成的简历ID为：{resume_id}")

            # 保存简历内容到txt文件夹中
            folder_name = self.save_resume_to_txt(resume_id, resume_parts)

            # 返回简历号（时间戳）和生成的文件夹名
            logging.info("简历处理成功")
            return {"message": f"简历上传并处理成功，简历号：{resume_id}", "folder": folder_name}
        except Exception as e:
            logging.error(f"处理简历时发生错误：{str(e)}")
            return {"message": f"处理简历时发生错误：{str(e)}"}
