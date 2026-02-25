"""
主题管理工具 - 管理themes.yaml文件
"""

import sys
import yaml
from pathlib import Path
from typing import List

# 设置控制台编码为UTF-8（Windows）
# 注意：只在作为主脚本运行时重定向，避免在被导入时冲突
if sys.platform == "win32" and __name__ == "__main__":
    import io

    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if not isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def load_themes(themes_file: Path) -> List[str]:
    """从themes.yaml加载themes"""
    if not themes_file.exists():
        return []

    try:
        with open(themes_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                return []
            return data.get("themes", [])
    except Exception as e:
        print(f"⚠️  读取themes.yaml失败: {e}")
        return []


def save_themes(themes_file: Path, themes: List[str]):
    """保存themes到themes.yaml"""
    themes_file.parent.mkdir(parents=True, exist_ok=True)

    data = {"themes": themes}

    try:
        with open(themes_file, "w", encoding="utf-8") as f:
            yaml.dump(
                data, f, allow_unicode=True, default_flow_style=False, sort_keys=False
            )
        print(f"✅ themes已保存到: {themes_file}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def add_theme(themes_file: Path, theme: str) -> bool:
    """添加theme"""
    themes = load_themes(themes_file)

    if theme in themes:
        print(f"⚠️  theme '{theme}' 已存在")
        return False

    themes.append(theme)
    return save_themes(themes_file, themes)


def remove_theme(themes_file: Path, theme: str) -> bool:
    """删除theme"""
    themes = load_themes(themes_file)

    if theme not in themes:
        print(f"⚠️  theme '{theme}' 不存在")
        return False

    themes.remove(theme)
    return save_themes(themes_file, themes)


def list_themes(themes_file: Path):
    """列出所有themes"""
    themes = load_themes(themes_file)

    if not themes:
        print("📋 当前没有themes")
        return

    print(f"📋 当前themes ({len(themes)}个):")
    print("-" * 70)
    for i, theme in enumerate(themes, 1):
        print(f"  {i}. {theme}")
    print("-" * 70)


def interactive_theme_management(base_dir: Path):
    """交互式主题管理"""
    themes_file = base_dir / "themes.yaml"

    while True:
        print("\n" + "=" * 70)
        print("主题管理")
        print("=" * 70)
        list_themes(themes_file)

        print("\n请选择操作：")
        print("  1. 添加theme")
        print("  2. 删除theme")
        print("  3. 查看themes")
        print("  0. 退出")

        choice = input("\n请选择 (0-3): ").strip()

        if choice == "0":
            break
        elif choice == "1":
            theme = input("请输入要添加的theme: ").strip()
            if theme:
                if add_theme(themes_file, theme):
                    print(f"✅ 已添加theme: {theme}")
        elif choice == "2":
            theme = input("请输入要删除的theme: ").strip()
            if theme:
                confirm = input(f"确认删除 '{theme}'? (y/n): ").strip().lower()
                if confirm in ["y", "yes", "是"]:
                    if remove_theme(themes_file, theme):
                        print(f"✅ 已删除theme: {theme}")
        elif choice == "3":
            list_themes(themes_file)
        else:
            print("⚠️  无效选择，请重试")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="主题管理工具")
    parser.add_argument("--add", type=str, help="添加theme")
    parser.add_argument("--remove", type=str, help="删除theme")
    parser.add_argument("--list", action="store_true", help="列出所有themes")
    parser.add_argument("--interactive", action="store_true", help="交互式管理")
    parser.add_argument(
        "--base-dir", type=str, help="基础目录路径（默认为脚本所在目录）"
    )

    args = parser.parse_args()

    base_dir = Path(args.base_dir) if args.base_dir else Path(__file__).parent
    themes_file = base_dir / "themes.yaml"

    if args.list:
        list_themes(themes_file)
    elif args.add:
        add_theme(themes_file, args.add)
    elif args.remove:
        remove_theme(themes_file, args.remove)
    elif args.interactive:
        interactive_theme_management(base_dir)
    else:
        # 默认交互式
        interactive_theme_management(base_dir)
