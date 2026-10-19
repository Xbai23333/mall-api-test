
import sys
from datetime import datetime
from pathlib import Path

import pytest


def main():
    # 获取项目根目录
    project_root = Path(__file__).resolve().parent

    # 创建测试报告目录
    report_dir = project_root / "reports"
    report_dir.mkdir(exist_ok=True)

    # 生成带时间戳的报告名称
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"report_{timestamp}.html"

    print("=" * 50)
    print("Mall 商城接口自动化测试")
    print(f"测试报告：{report_path}")
    print("=" * 50)

    # 执行pytest测试
    exit_code = pytest.main([
        str(project_root / "tests"),
        "-v",
        f"--html={report_path}",
        "--self-contained-html"
    ])

    # 将测试执行状态返回给系统
    return int(exit_code)


if __name__ == "__main__":
    sys.exit(main())
