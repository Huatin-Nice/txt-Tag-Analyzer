# txt-Tag-Analyzer
这是一个用于分析TXT格式标签文件的Python工具，针对AI图像训练（如Stable Diffusion、SDXL等）的标签管理需求。它可以统计标签频率、检查长度限制、生成特征提示词，帮助你优化训练数据。

TXT标签分析工具
这是一个用于分析TXT格式标签文件的Python工具，特别针对AI图像训练（如Stable Diffusion、SDXL等）的标签管理需求。它可以统计标签频率、检查长度限制、生成特征提示词，帮助你优化训练数据。
功能特性
📊 标签统计分析：统计所有标签的出现频率
📏 长度检查：检测可能超过SDXL模型77 tokens限制的标签
🏆 排行榜功能：按标签数量、token数量等多维度排名
🔍 问题识别：自动识别过长标签和问题文件
🎯 特征提取：生成高频特征提示词
📁 数据导出：支持JSON格式导出分析结果
🔧 批量处理：支持批量处理目录下所有txt文件
应用场景
AI图像训练数据集预处理
标签质量检查和优化
特征提取和提示词工程
数据集分析和整理

安装要求
# 需要Python 3.6+
# 安装依赖
pip install -r requirements.txt
依赖库
Python标准库（无需额外安装）：
os
re
collections
json
argparse
快速开始
基本使用
# 检查当前目录下的所有txt文件
python check_labels.py

# 检查指定目录
python check_labels.py --dir ./your_dataset

# 检查并生成特征提示词
python check_labels.py --feature

# 检查并导出JSON结果
python check_labels.py --feature --export
完整参数说明
python check_labels.py [选项]

选项:
  -h, --help            显示帮助信息
  --dir DIR             要检查的目录路径，默认为当前目录
  --feature             生成特征提示词
  --top N               特征提示词取前N个标签，默认20
  --min-freq M          最小出现频率，默认2
  --export              导出结果到JSON文件
  --limit LIMIT         限制检查的文件数量，0表示不限制
使用示例
示例1：基本检查
python check_labels.py --dir ./training_data
输出：
TXT标签文件检查工具
==================================================
正在扫描目录: /path/to/training_data
处理文件: image1.txt
  标签数量: 5
  单词数量: 12
  字符数量: 85
  估计token数: 18.0
  是否可能超长: 否
...
示例2：生成特征提示词
python check_labels.py --dir ./character_data --feature --top 15 --min-freq 3
这将：
分析 ./character_data目录下的所有txt文件
统计标签出现频率
提取出现频率≥3次的前15个标签
生成特征提示词并保存到 feature_prompt.txt
示例3：完整分析并导出
python check_labels.py --dir ./dataset --feature --export --min-freq 1
输出文件
1. 控制台输出
文件排行榜（按标签数、token数排序）
Token数量分布统计
最长的标签列表
潜在问题文件警告
最常出现的标签
生成的特征提示词
2. 生成的文件
feature_prompt.txt（使用 --feature参数时生成）
包含按频率排序的特征提示词，格式如下：
# 生成的特征提示词
# 基于 150 个文件中的标签统计
# 包含 20 个特征词，出现频率 >= 2
# 估计Token数: 45.3

==================================================

masterpiece, best quality, 1girl, solo, looking at viewer, ...

==================================================

# 特征词列表:
  1. masterpiece (出现次数: 45)
  2. best quality (出现次数: 42)
  3. 1girl (出现次数: 38)
  ...
label_analysis.json（使用 --export参数时生成）
包含详细的统计分析数据：
{
  "file_stats": [...],
  "summary": {
    "total_files": 150,
    "total_labels": 1250,
    "token_distribution": {...},
    "problematic_files": 3
  },
  "most_common_labels": [...],
  "longest_labels": [...]
}
功能详解
1. 标签解析
自动识别多种分隔符：, ; | \n \t
自动去除标签前后空格
支持中英文混合标签
2. Token估算
使用简单的估算方法：token数 ≈ 单词数 × 1.5
标记可能超过77 tokens的文件
提供安全范围建议
3. 特征提示词生成
统计所有标签的出现频率
可配置最小出现频率阈值
可配置提取的标签数量
自动组合成标准提示词格式
4. 问题检测
识别过长标签（>50字符）
标记可能超限的文件
提供详细的错误信息
实际应用案例
案例1：数据集清洗
# 检查训练数据集，找出问题文件
python check_labels.py --dir ./训练数据 --export

# 根据输出结果，可以：
# 1. 手动修改过长的标签
# 2. 删除或拆分过长的文件
# 3. 重新组织标签结构
案例2：角色特征提取
# 从角色图片集中提取共同特征
python check_labels.py --dir ./角色图片 --feature --top 30 --min-freq 5

# 生成的特征提示词可用于：
# 1. 训练LoRA模型时的核心提示词
# 2. 创建角色的标准描述模板
# 3. 优化训练数据的标签质量
案例3：数据集分析
# 完整分析数据集结构
python check_labels.py --dir ./dataset --feature --export --min-freq 1

# 通过分析结果可以了解：
# 1. 标签的平均长度和分布
# 2. 最常见的标签组合
# 3. 数据集的质量状况
# 4. 需要优化的方向
注意事项
1. Token估算限制
当前使用简单的估算方法（单词数×1.5）
对于SDXL，实际token数可能因tokenizer不同而有差异
77 tokens是SDXL模型的标准限制
2. 文件格式要求
仅支持UTF-8编码的txt文件
每行或每个标签用指定分隔符分隔
不支持二进制文件或其他格式
3. 性能考虑
处理大量文件时可能需要较长时间
建议先在小样本上测试
结果文件可能较大，注意磁盘空间
故障排除
常见问题1：编码错误
# 如果出现编码错误，可以：
# 1. 检查文件编码是否为UTF-8
# 2. 使用文本编辑器转换编码
# 3. 或修改代码使用其他编码
常见问题2：内存不足
# 处理大型数据集时：
# 1. 使用 --limit 参数限制文件数量
# 2. 分批次处理
# 3. 不导出JSON结果
常见问题3：分隔符识别错误
# 如果标签分割不正确：
# 1. 检查文件使用的分隔符
# 2. 可以修改代码中的delimiters列表
# 3. 统一文件格式
