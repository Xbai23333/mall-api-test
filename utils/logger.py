import logging
import os
from datetime import datetime


def setup_logger():
    # 创建日志文件夹
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名
    log_file = os.path.join(
        log_dir,
        f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # 创建日志记录器
    logger = logging.getLogger("mall_api_test")
    logger.setLevel(logging.INFO)

    # 避免重复添加日志处理器
    if logger.handlers:
        return logger

    # 设置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # 输出日志到文件
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 输出日志到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()