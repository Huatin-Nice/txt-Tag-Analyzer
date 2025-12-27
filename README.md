# txt-Tag-Analyzer
这是一个用于分析TXT格式标签文件的Python工具，针对AI图像训练（如Stable Diffusion、SDXL等）的标签管理需求。它可以统计标签频率、检查长度限制、生成特征提示词，帮助你优化训练数据。

# TXT Tag Analyzer

一个专门用于分析和处理AI训练标签文件的Python工具。快速检查标签长度、统计频率、生成特征提示词，优化你的数据集。

## ✨ 功能特性
 
  📊 **智能分析** - 自动统计标签频率和分布
  📏 **长度检查** - 检测超出模型限制的标签（如SDXL的77 tokens限制）
  🎯 **特征提取** - 生成高频特征提示词用于训练
  📁 **批量处理** - 支持整个目录的文件分析
  🚨 **问题识别** - 自动发现过长标签和问题文件
  💾 **数据导出** - 支持JSON格式导出完整分析结果
  ⚡ **快速高效** - 纯Python实现，无额外依赖
## 🚀 快速开始

### 安装

无需安装，只需Python 3.6+：

```bash
git clone https://github.com/yourusername/txt-tag-analyzer.git
cd txt-tag-analyzer
```

### 基本使用

```bash
# 检查当前目录
python check_labels.py

# 检查指定目录
python check_labels.py --dir ./your_dataset

# 生成特征提示词
python check_labels.py --feature

# 完整分析并导出
python check_labels.py --feature --export
```

## 📖 使用示例

### 示例1：数据集质量检查

```bash
# 检查数据集，找出可能的问题
python check_labels.py --dir ./training_data
```

### 示例2：提取角色特征

```bash
# 提取前20个最常见特征
python check_labels.py --dir ./character_images --feature --top 20

# 提取频率≥3的特征
python check_labels.py --dir ./character_images --feature --min-freq 3
```

### 示例3：完整分析报告

```bash
# 生成详细分析报告
python check_labels.py --dir ./dataset --feature --export --min-freq 2
```

## 📊 输出示例

```markdown
TXT Tag Analyzer
==================================================
正在扫描目录: /path/to/dataset
处理文件: image_001.txt
  标签数量: 8
  单词数量: 15
  字符数量: 102
  估计token数: 22.5
  是否可能超长: 否

特征提示词生成器
==================================================
总共出现 1250 次标签
其中不重复的标签有 156 个
出现频率 >= 2 的标签有 45 个

生成的特征提示词 (前20个):
----------------------------------------
  1. masterpiece                       (出现次数: 45)
  2. best quality                      (出现次数: 42)
  3. 1girl                             (出现次数: 38)
  ...

特征提示词已保存到: feature_prompt.txt
```

## 🔧 参数说明

| 参数         | 说明                  | 默认值      |
| ------------ | --------------------- | ----------- |
| `--dir`      | 要分析的目录路径      | 当前目录    |
| `--feature`  | 生成特征提示词        | False       |
| `--top`      | 特征提示词取前N个标签 | 20          |
| `--min-freq` | 最小出现频率          | 2           |
| `--export`   | 导出JSON结果          | False       |
| `--limit`    | 限制处理文件数量      | 0（无限制） |

## 📁 输出文件

### 控制台输出
  文件排行榜（标签数、token数）
  Token分布统计 
  最长标签列表 
  问题文件警告
  高频标签统计
### 生成文件
  **feature_prompt.txt** - 生成的特征提示词 
  **label_analysis.json** - 完整分析数据（JSON格式）
  
## 🔍 应用场景

### 🎨 AI训练数据准备 
  检查标签是否符合模型要求
  优化标签长度和质量
  提取数据集共性特征
### 📈 数据集分析
  统计标签分布和频率
  识别数据集中常见特征
  发现标签质量问题
### 🔧 工作流集成
  自动化数据清洗流程
  训练前数据质量检查
  特征工程和提示词优化
## 🛠️ 技术细节

### 支持的格式
  UTF-8编码的txt文件
  多种分隔符：`, ; | \n \t`
  支持中英文混合标签

### Token估算
  简单估算：`token数 ≈ 单词数 × 1.5`
  标记可能超过77 tokens的文件
  提供安全范围建议

## 📄 许可证

MIT License - 详见 LICENSE文件

## 🤝 贡献

欢迎贡献！请查看 CONTRIBUTING.md了解详细信息。
   Fork 本仓库
   创建功能分支 (`git checkout -b feature/AmazingFeature`)
   提交更改 (`git commit -m 'Add some AmazingFeature'`)
   推送分支 (`git push origin feature/AmazingFeature`)
   开启 Pull Request

## 📝 更新日志

### v1.0.0
  初始版本发布
  基础标签分析功能
  特征提示词生成 
  结果导出功能
