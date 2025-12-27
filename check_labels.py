import os
import re
from collections import defaultdict, Counter
import json

def check_txt_labels_in_directory(directory="."):
    """
    检查指定目录下所有txt文件的标签长度并生成排行榜
    
    Args:
        directory: 要检查的目录路径，默认为当前目录
    """
    
    # 支持的扩展名
    supported_extensions = {'.txt'}
    
    # 存储结果
    results = {
        'file_stats': [],  # 每个文件的统计信息
        'token_count_summary': defaultdict(int),  # token数量统计
        'label_frequency': Counter(),  # 标签出现频率
        'longest_labels': []  # 最长的标签
    }
    
    print(f"正在扫描目录: {os.path.abspath(directory)}\n")
    
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # 只处理txt文件
        if not (os.path.isfile(filepath) and filename.lower().endswith('.txt')):
            continue
        
        print(f"处理文件: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 如果文件为空，跳过
            if not content:
                print(f"  文件为空\n")
                continue
            
            # 使用多种分隔符拆分标签
            # 常见的分隔符：逗号、分号、竖线、空格
            delimiters = [',', ';', '|', '\n', '\t']
            
            # 尝试不同的分隔符
            labels = []
            for delimiter in delimiters:
                if delimiter in content:
                    labels = [label.strip() for label in content.split(delimiter) if label.strip()]
                    break
            
            # 如果没有找到分隔符，尝试按空格分割
            if not labels:
                labels = [content.strip()]
            
            # 计算各种统计信息
            label_count = len(labels)
            word_count = sum(len(label.split()) for label in labels)
            char_count = sum(len(label) for label in labels)
            
            # 估算token数量（简单估算，假设每个单词大约1-2个token）
            estimated_tokens = word_count * 1.5
            
            # 保存文件统计信息
            file_stat = {
                'filename': filename,
                'full_path': filepath,
                'raw_content': content,
                'cleaned_labels': labels,
                'label_count': label_count,
                'word_count': word_count,
                'char_count': char_count,
                'estimated_tokens': estimated_tokens,
                'has_long_labels': any(len(label) > 50 for label in labels),  # 标记长标签
                'longest_label': max(labels, key=len) if labels else ""
            }
            
            results['file_stats'].append(file_stat)
            
            # 更新汇总统计
            token_range = "未知"
            if estimated_tokens <= 20:
                token_range = "0-20 tokens"
            elif estimated_tokens <= 40:
                token_range = "21-40 tokens"
            elif estimated_tokens <= 60:
                token_range = "41-60 tokens"
            elif estimated_tokens <= 77:
                token_range = "61-77 tokens"
            else:
                token_range = "超过77 tokens"
            
            results['token_count_summary'][token_range] += 1
            
            # 统计标签频率
            for label in labels:
                results['label_frequency'][label] += 1
            
            # 记录特别长的标签
            for label in labels:
                if len(label) > 50:  # 超过50字符认为是长标签
                    results['longest_labels'].append({
                        'filename': filename,
                        'label': label,
                        'length': len(label)
                    })
            
            print(f"  标签数量: {label_count}")
            print(f"  单词数量: {word_count}")
            print(f"  字符数量: {char_count}")
            print(f"  估计token数: {estimated_tokens:.1f}")
            print(f"  是否可能超长: {'是' if estimated_tokens > 77 else '否'}\n")
            
        except Exception as e:
            print(f"  处理文件时出错: {e}\n")
            continue
    
    return results

def print_leaderboard(results):
    """打印排行榜"""
    
    if not results['file_stats']:
        print("未找到任何txt文件！")
        return
    
    print("=" * 80)
    print("TXT标签文件排行榜")
    print("=" * 80)
    
    # 1. 按标签数量排名
    print("\n按标签数量排名:")
    print("-" * 40)
    sorted_by_labels = sorted(results['file_stats'], 
                             key=lambda x: x['label_count'], 
                             reverse=True)
    
    for i, stat in enumerate(sorted_by_labels[:10], 1):
        status = "可能超长" if stat['estimated_tokens'] > 77 else ""
        print(f"{i:2d}. {stat['filename']:30} 标签数: {stat['label_count']:3d}  "
              f"Tokens: {stat['estimated_tokens']:5.1f} {status}")
    
    # 2. 按估计token数排名
    print("\n按估计Token数排名:")
    print("-" * 40)
    sorted_by_tokens = sorted(results['file_stats'], 
                             key=lambda x: x['estimated_tokens'], 
                             reverse=True)
    
    for i, stat in enumerate(sorted_by_tokens[:10], 1):
        status = "可能超长" if stat['estimated_tokens'] > 77 else ""
        print(f"{i:2d}. {stat['filename']:30}  "
              f"Tokens: {stat['estimated_tokens']:5.1f}  "
              f"标签数: {stat['label_count']:3d} {status}")
    
    # 3. Token数量分布统计
    print("\nToken数量分布:")
    print("-" * 40)
    for range_name, count in sorted(results['token_count_summary'].items()):
        percentage = (count / len(results['file_stats'])) * 100
        bar = "*" * int(percentage / 2)
        print(f"{range_name:20s}: {count:3d} 个文件 {percentage:5.1f}% {bar}")
    
    # 4. 最长的标签
    if results['longest_labels']:
        print("\n最长的标签:")
        print("-" * 40)
        sorted_long_labels = sorted(results['longest_labels'], 
                                   key=lambda x: x['length'], 
                                   reverse=True)
        for i, item in enumerate(sorted_long_labels[:5], 1):
            label_preview = item['label'][:60] + "..." if len(item['label']) > 60 else item['label']
            print(f"{i:2d}. {item['filename']:20} 长度: {item['length']:3d}")
            print(f"    标签: {label_preview}")
            print()
    
    # 5. 潜在问题文件
    print("\n潜在问题文件 (可能超过77 tokens):")
    print("-" * 40)
    problematic_files = [stat for stat in results['file_stats'] 
                        if stat['estimated_tokens'] > 77]
    
    if problematic_files:
        for stat in problematic_files:
            print(f"文件: {stat['filename']}")
            print(f"  Token数: {stat['estimated_tokens']:.1f}")
            print(f"  标签数: {stat['label_count']}")
            print(f"  最长标签: {stat['longest_label'][:50]}..." if len(stat['longest_label']) > 50 
                  else f"  最长标签: {stat['longest_label']}")
            print()
    else:
        print("没有发现可能超长的文件")
    
    # 6. 最常出现的标签
    print("\n最常出现的标签:")
    print("-" * 40)
    common_labels = results['label_frequency'].most_common(10)
    for i, (label, count) in enumerate(common_labels, 1):
        label_preview = label[:40] + "..." if len(label) > 40 else label
        print(f"{i:2d}. {label_preview:43} 出现次数: {count:3d}")

def generate_feature_prompt(results, top_n=20, min_frequency=2):
    """
    生成特征提示词，将所有标签按出现频率排序，生成可用于训练的特征词
    
    Args:
        results: 分析结果
        top_n: 取前多少个特征词
        min_frequency: 最小出现频率，低于此值的不计入
    """
    if not results['label_frequency']:
        print("没有找到任何标签！")
        return ""
    
    # 获取所有标签，按频率排序
    all_labels_freq = results['label_frequency'].most_common()
    
    print("\n" + "=" * 80)
    print("特征提示词生成器")
    print("=" * 80)
    
    # 统计信息
    total_unique_labels = len(all_labels_freq)
    print(f"总共出现 {sum(results['label_frequency'].values())} 次标签")
    print(f"其中不重复的标签有 {total_unique_labels} 个")
    
    # 筛选出出现频率较高的标签
    frequent_labels = [(label, freq) for label, freq in all_labels_freq if freq >= min_frequency]
    
    if not frequent_labels:
        print(f"没有找到出现频率 >= {min_frequency} 的标签")
        return ""
    
    print(f"出现频率 >= {min_frequency} 的标签有 {len(frequent_labels)} 个")
    
    # 生成特征提示词
    print(f"\n生成的特征提示词 (前{min(top_n, len(frequent_labels))}个):")
    print("-" * 40)
    
    # 创建特征词列表
    feature_words = []
    for i, (label, freq) in enumerate(frequent_labels[:top_n], 1):
        feature_words.append(label)
        print(f"{i:3d}. {label:<40} (出现次数: {freq})")
    
    # 将特征词组合成提示词
    feature_prompt = ", ".join(feature_words)
    
    # 估计token数量
    estimated_tokens = sum(len(word.split()) for word in feature_words) * 1.5
    
    print(f"\n组合后的特征提示词:")
    print("-" * 40)
    print(feature_prompt)
    print(f"\n提示词长度统计:")
    print(f"  标签数量: {len(feature_words)}")
    print(f"  字符数量: {len(feature_prompt)}")
    print(f"  单词数量: {sum(len(word.split()) for word in feature_words)}")
    print(f"  估计Token数: {estimated_tokens:.1f}")
    print(f"  是否超过限制: {'是' if estimated_tokens > 77 else '否'}")
    
    # 将特征提示词保存到文件
    output_file = "feature_prompt.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 生成的特征提示词\n")
        f.write(f"# 基于 {len(results['file_stats'])} 个文件中的标签统计\n")
        f.write(f"# 包含 {len(feature_words)} 个特征词，出现频率 >= {min_frequency}\n")
        f.write(f"# 估计Token数: {estimated_tokens:.1f}\n")
        f.write("\n" + "="*50 + "\n\n")
        f.write(feature_prompt)
        f.write("\n\n" + "="*50 + "\n")
        f.write("\n# 特征词列表:\n")
        for i, (label, freq) in enumerate(frequent_labels[:top_n], 1):
            f.write(f"{i:3d}. {label} (出现次数: {freq})\n")
    
    print(f"\n特征提示词已保存到: {output_file}")
    
    return feature_prompt

def export_results(results, output_file="label_analysis.json"):
    """导出结果到JSON文件"""
    # 清理数据，移除原始内容以减少文件大小
    export_data = {
        'file_stats': [],
        'summary': {
            'total_files': len(results['file_stats']),
            'total_labels': sum(stat['label_count'] for stat in results['file_stats']),
            'token_distribution': dict(results['token_count_summary']),
            'problematic_files': len([stat for stat in results['file_stats'] 
                                    if stat['estimated_tokens'] > 77])
        },
        'most_common_labels': results['label_frequency'].most_common(20),
        'longest_labels': results['longest_labels'][:20]
    }
    
    # 添加文件统计（不包含原始内容）
    for stat in results['file_stats']:
        file_stat = {
            'filename': stat['filename'],
            'label_count': stat['label_count'],
            'word_count': stat['word_count'],
            'char_count': stat['char_count'],
            'estimated_tokens': stat['estimated_tokens'],
            'has_long_labels': stat['has_long_labels'],
            'longest_label': stat['longest_label'][:100]  # 只保存前100个字符
        }
        export_data['file_stats'].append(file_stat)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细分析结果已导出到: {output_file}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检查TXT标签文件长度并生成特征提示词')
    parser.add_argument('--dir', default='.', help='要检查的目录，默认为当前目录')
    parser.add_argument('--export', action='store_true', help='导出结果到JSON文件')
    parser.add_argument('--feature', action='store_true', help='生成特征提示词')
    parser.add_argument('--top', type=int, default=20, help='特征提示词取前多少个标签，默认20')
    parser.add_argument('--min-freq', type=int, default=2, help='最小出现频率，默认2')
    parser.add_argument('--limit', type=int, default=0, help='限制检查的文件数量，0表示不限制')
    
    args = parser.parse_args()
    
    print("TXT标签文件检查工具")
    print("=" * 50)
    
    # 检查目录是否存在
    if not os.path.exists(args.dir):
        print(f"错误: 目录 '{args.dir}' 不存在！")
        return
    
    # 运行检查
    results = check_txt_labels_in_directory(args.dir)
    
    if not results['file_stats']:
        print(f"在目录 '{args.dir}' 中未找到任何txt文件！")
        return
    
    # 打印排行榜
    print_leaderboard(results)
    
    # 生成特征提示词
    if args.feature:
        generate_feature_prompt(results, top_n=args.top, min_frequency=args.min_freq)
    
    # 导出结果
    if args.export:
        export_results(results)
    
    # 输出总结
    print("\n" + "=" * 50)
    print("检查完成！")
    print(f"扫描目录: {os.path.abspath(args.dir)}")
    print(f"处理文件: {len(results['file_stats'])} 个")
    print(f"总标签数: {sum(stat['label_count'] for stat in results['file_stats'])} 个")
    print(f"不重复标签: {len(results['label_frequency'])} 个")
    
    problematic = len([stat for stat in results['file_stats'] 
                      if stat['estimated_tokens'] > 77])
    if problematic > 0:
        print(f"可能超长的文件: {problematic} 个")
        print("注意: 这些文件的标签可能超过SDXL模型的77 tokens限制")
    else:
        print("所有文件的标签长度都在安全范围内")

if __name__ == "__main__":
    main()
