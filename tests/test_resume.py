"""简历优化器单元测试。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from resume_optimizer import LLMClient, match_job, optimize_resume  # noqa: E402


class FakeLLM(LLMClient):
    def chat(self, messages, temperature=0.4):
        return "[结果] " + messages[-1]["content"][:30]


class TestResume(unittest.TestCase):
    def test_optimize(self):
        r = optimize_resume("负责网站开发，做了很多功能", FakeLLM())
        self.assertIn("[结果]", r)

    def test_match(self):
        r = match_job("会Python", "需要Python工程师", FakeLLM())
        self.assertIn("[结果]", r)


if __name__ == "__main__":
    unittest.main(verbosity=2)
