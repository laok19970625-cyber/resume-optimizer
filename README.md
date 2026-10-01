# AI 简历优化器

读入简历文本，优化表达（动词开头 + 量化成果），或按目标岗位做匹配度分析。

## 特性
- `optimize`：简历描述优化
- `match`：岗位匹配度评估 + 差距分析 + 优化建议
- 保持事实不编造

## 快速开始
```bash
export LLM_API_KEY="你的Key"
python main.py optimize resume.txt
python main.py match resume.txt job.txt
```

## 应用场景
- 求职简历打磨
- 岗位匹配自测
- 职业规划咨询

## License
MIT
