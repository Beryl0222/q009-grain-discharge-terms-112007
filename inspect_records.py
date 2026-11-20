"""读入资料包并列出可供检查的记录。"""

import argparse
import json
from pathlib import Path


def load_records(path):
    """读取 UTF-8 资料并检查记录编号。"""
    with Path(path).open(encoding="utf-8") as stream:
        groups = json.load(stream)
    if not isinstance(groups, dict) or not groups:
        raise ValueError("资料应包含非空的记录类别")
    for kind, records in groups.items():
        if not isinstance(records, list):
            raise ValueError(f"{kind} 应为记录数组")
        ids = set()
        for row in records:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError(f"{kind} 中存在没有编号的记录")
            if row["id"] in ids:
                raise ValueError(f"{kind} 中编号重复 {row['id']}")
            ids.add(row["id"])
    return groups


def main():
    parser = argparse.ArgumentParser(description="浏览合成原始资料")
    parser.add_argument("path", type=Path, help="资料文件路径")
    parser.add_argument("--list", action="store_true", help="列出记录类别与数量")
    args = parser.parse_args()
    records = load_records(args.path)
    if args.list:
        for kind, group in records.items():
            print(f"{kind}　{len(group)} 条")
    else:
        print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
