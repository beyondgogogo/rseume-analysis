from datetime import datetime

# 用于生成时间戳
def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")
