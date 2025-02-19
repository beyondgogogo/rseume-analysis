from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

# 导入服务
from service.resume_service import ResumeService
from service.resume_labeling_service import *

app = Flask(__name__)

# 初始化服务
resume_service = ResumeService()
resumeLabelingService = ResumeLabelingService()
# 设置日志
logging.basicConfig(level=logging.DEBUG)

# 数据库连接
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='resume',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# 插入标签数据
def insert_resume_and_labels(resume_id, labels, label_type):
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    # 插入简历-先不存简历，因为后续简历会有较大变动
    #cursor.execute('INSERT INTO resumes (resume_id) VALUES (%s)', (resume_id,))
    #resume_db_id = cursor.lastrowid

    # 插入标签
    for label in labels:
        cursor.execute('INSERT INTO labels (label_type, label_value) VALUES (%s, %s)', (label_type, label))
        label_db_id = cursor.lastrowid

        # 插入简历与标签的关联
        cursor.execute('INSERT INTO resume_labels (resume_id, label_id) VALUES (%s, %s)', (resume_id, label_db_id))

    connection.commit()
    cursor.close()
    connection.close()

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:
        # 获取上传的文件
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # 使用 ResumeService 处理简历
        result = resume_service.process_resume(file)

        # 返回处理结果
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error uploading resume: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 获取基本信息标签接口
@app.route('/get_basic_labels', methods=['GET'])
def get_basic_labels():
    try:
        # 获取简历编号（resume_id）参数
        resume_id = request.args.get('resume_id')
        if not resume_id:
            return jsonify({"error": "No resume_id provided"}), 400

        # 使用 BasicLabelsService 获取基本信息标签
        result = resumeLabelingService.get_basic_labels(resume_id)

        # 存储标签到数据库
        insert_resume_and_labels(resume_id, result['labels'], 'basic')

        # 返回结果
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error getting basic labels for resume {resume_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 获取教育经历标签接口
@app.route('/get_education_labels', methods=['GET'])
def get_education_labels():
    try:
        # 获取简历编号（resume_id）参数
        resume_id = request.args.get('resume_id')
        if not resume_id:
            return jsonify({"error": "No resume_id provided"}), 400

        # 使用 EducationLabelsService 获取教育经历标签
        result = resumeLabelingService.get_education_labels(resume_id)

        # 存储标签到数据库
        insert_resume_and_labels(resume_id, result['labels'], 'education')

        # 返回结果
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error getting education labels for resume {resume_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 获取技能标签接口
@app.route('/get_skills_labels', methods=['GET'])
def get_skills_labels():
    try:
        # 获取简历编号（resume_id）参数
        resume_id = request.args.get('resume_id')
        if not resume_id:
            return jsonify({"error": "No resume_id provided"}), 400

        # 使用 SkillsLabelsService 获取技能标签
        result = resumeLabelingService.get_skills_labels(resume_id)

        # 存储标签到数据库
        insert_resume_and_labels(resume_id, result['labels'], 'skills')

        # 返回结果
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error getting skills labels for resume {resume_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 获取工作经历标签接口
@app.route('/get_work_experience_labels', methods=['GET'])
def get_work_experience_labels():
    try:
        # 获取简历编号（resume_id）参数
        resume_id = request.args.get('resume_id')
        if not resume_id:
            return jsonify({"error": "No resume_id provided"}), 400

        # 使用 WorkExperienceLabelsService 获取工作经历标签
        result = resumeLabelingService.get_work_experience_labels(resume_id)

        # 存储标签到数据库
        insert_resume_and_labels(resume_id, result['labels'], 'work_experience')

        # 返回结果
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error getting work experience labels for resume {resume_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
