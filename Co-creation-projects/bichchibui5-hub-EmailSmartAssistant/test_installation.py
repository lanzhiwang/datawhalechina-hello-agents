#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装测试脚本
Installation Test Script

用于验证所有依赖是否正确安装
"""

import sys
from rich.console import Console
from rich.table import Table

console = Console()


def test_imports():
    """测试所有必要的库导入"""
    test_results = []

    # 核心库测试
    libraries = [
        ("imaplib", "邮件IMAP协议"),
        ("smtplib", "邮件SMTP协议"),
        ("email", "邮件处理"),
        ("json", "JSON处理"),
        ("pandas", "数据处理"),
        ("numpy", "数值计算"),
        ("jieba", "中文分词"),
        ("textblob", "文本处理"),
        ("langdetect", "语言检测"),
        ("sklearn", "机器学习"),
        ("dateparser", "日期解析"),
        ("arrow", "时间处理"),
        ("jinja2", "模板引擎"),
        ("matplotlib", "图表绘制"),
        ("seaborn", "统计图表"),
        ("tqdm", "进度条"),
        ("rich", "终端美化"),
    ]

    for lib_name, description in libraries:
        try:
            __import__(lib_name)
            test_results.append((lib_name, description, "✅ 成功", "green"))
        except ImportError as e:
            test_results.append((lib_name, description, f"❌ 失败: {str(e)}", "red"))

    return test_results


def test_files():
    """测试必要文件是否存在"""
    import os

    files_to_check = [
        ("config/email_config.json", "邮箱配置文件"),
        ("templates/reply_templates.json", "回复模板文件"),
        ("EmailSmartAssistant.ipynb", "主程序Notebook"),
        ("requirements.txt", "依赖列表"),
        ("README.md", "说明文档"),
    ]

    file_results = []
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            file_results.append((file_path, description, "✅ 存在", "green"))
        else:
            file_results.append((file_path, description, "❌ 缺失", "red"))

    return file_results


def main():
    """主测试函数"""
    console.print("🧪 智能邮件助手 - 安装测试", style="bold blue")
    console.print("=" * 50)

    # 测试Python版本
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    console.print(f"Python版本: {python_version}", style="cyan")

    if sys.version_info < (3, 7):
        console.print("⚠️  建议使用Python 3.7或更高版本", style="yellow")

    console.print()

    # 测试库导入
    console.print("📚 测试库导入...", style="bold")
    import_results = test_imports()

    table = Table(title="库导入测试结果")
    table.add_column("库名称", style="cyan")
    table.add_column("描述", style="white")
    table.add_column("状态", style="white")

    success_count = 0
    for lib_name, description, status, color in import_results:
        table.add_row(lib_name, description, status)
        if "成功" in status:
            success_count += 1

    console.print(table)
    console.print(
        f"导入成功: {success_count}/{len(import_results)}",
        style="green" if success_count == len(import_results) else "yellow",
    )

    console.print()

    # 测试文件存在
    console.print("📁 测试文件完整性...", style="bold")
    file_results = test_files()

    file_table = Table(title="文件完整性测试")
    file_table.add_column("文件路径", style="cyan")
    file_table.add_column("描述", style="white")
    file_table.add_column("状态", style="white")

    file_success = 0
    for file_path, description, status, color in file_results:
        file_table.add_row(file_path, description, status)
        if "存在" in status:
            file_success += 1

    console.print(file_table)
    console.print(
        f"文件完整: {file_success}/{len(file_results)}",
        style="green" if file_success == len(file_results) else "yellow",
    )

    console.print()

    # 总结
    if success_count == len(import_results) and file_success == len(file_results):
        console.print("🎉 所有测试通过！可以开始使用智能邮件助手。", style="bold green")
        console.print(
            "💡 下一步：运行 'jupyter notebook EmailSmartAssistant.ipynb'", style="blue"
        )
    else:
        console.print("⚠️  存在问题，请检查上述失败项目。", style="bold yellow")
        if success_count < len(import_results):
            console.print(
                "📦 安装缺失的库：pip install -r requirements.txt", style="cyan"
            )


if __name__ == "__main__":
    main()
