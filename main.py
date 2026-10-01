"""命令行入口：简历优化 / 岗位匹配。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from resume_optimizer import LLMClient, match_job, optimize_resume  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("用法：")
        print("  python main.py optimize <简历文件>")
        print("  python main.py match <简历文件> <岗位描述文件>")
        return

    cmd = sys.argv[1]
    try:
        if cmd == "optimize":
            resume = Path(sys.argv[2]).read_text(encoding="utf-8")
            print("=== 优化后简历 ===")
            print(optimize_resume(resume, LLMClient()))
        elif cmd == "match":
            resume = Path(sys.argv[2]).read_text(encoding="utf-8")
            jd = Path(sys.argv[3]).read_text(encoding="utf-8")
            print("=== 岗位匹配分析 ===")
            print(match_job(resume, jd, LLMClient()))
        else:
            print(f"未知命令：{cmd}")
    except RuntimeError as e:
        print(f"[错误] {e}")


if __name__ == "__main__":
    main()
