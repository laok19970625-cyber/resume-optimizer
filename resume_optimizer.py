"""AI 简历优化器：读入简历文本 -> LLM 优化表达 -> 按目标岗位定向改写。"""

from __future__ import annotations

import json
import os
import urllib.request


class LLMClient:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.api_base = (api_base or os.environ.get("LLM_API_BASE", "https://open.bigmodel.cn/api/paas/v4")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "glm-4-flash")

    def chat(self, messages, temperature=0.4):
        if not self.api_key:
            raise RuntimeError("未配置 LLM_API_KEY，请设置环境变量后重试。")
        url = f"{self.api_base}/chat/completions"
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]


OPTIMIZE_PROMPT = (
    "你是一名资深 HR 与简历专家。请优化下面的简历描述，要求：\n"
    "1) 用动词开头、量化成果（数字、百分比）。\n"
    "2) 语言专业、简洁，去除空话套话。\n"
    "3) 保持事实，不编造经历。\n"
    "4) 直接输出优化后的文本，不要解释。"
)


def optimize_resume(resume_text: str, llm: LLMClient | None = None) -> str:
    llm = llm or LLMClient()
    messages = [
        {"role": "system", "content": OPTIMIZE_PROMPT},
        {"role": "user", "content": resume_text},
    ]
    return llm.chat(messages)


MATCH_PROMPT = (
    "你是一名职业规划顾问。请根据目标岗位要求，分析候选人的简历，"
    "输出：1) 匹配度评估（百分比） 2) 优势 3) 差距与改进建议 4) 简历优化重点。"
    "用中文，条理清晰。"
)


def match_job(resume_text: str, job_desc: str, llm: LLMClient | None = None) -> str:
    llm = llm or LLMClient()
    messages = [
        {"role": "system", "content": MATCH_PROMPT},
        {"role": "user", "content": f"目标岗位要求：\n{job_desc}\n\n候选人简历：\n{resume_text}"},
    ]
    return llm.chat(messages)
