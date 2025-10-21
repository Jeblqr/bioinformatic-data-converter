"""
遗传学数据转换工具使用示例
"""

import pandas as pd
from convertor import (
    convert_single_file,
    convert_from_metadata,
    convert_multiple_files,
    save_results,
    create_genetic_column_patterns,
)
import re


# ========================================
# 示例 1: 转换单个文件
# ========================================
def example_single_file():
    """转换单个文件的示例"""
    print("=" * 80)
    print("Example 1: Convert single file")
    print("=" * 80)

    result = convert_single_file(
        filename="/path/to/your/file.tsv.gz",
        metadata={"trait": "AGA", "n": 119185},
        verbose=True,
    )

    print(f"\nResult shape: {result.shape}")
    print(f"Result columns: {result.columns.tolist()}")
    print(result.head())


# ========================================
# 示例 2: 从元数据表批量转换
# ========================================
def example_from_metadata():
    """从元数据表批量转换的示例（你的用例）"""
    print("=" * 80)
    print("Example 2: Convert from metadata DataFrame")
    print("=" * 80)

    # 定义trait metadata
    trait_meta = pd.DataFrame(
        {
            "trait": ["AGA", "AGA", "AGA", "AGA", "AGA", "ANX"],
            "file": [
                "/home/qrluo/data/data/aga_metabolism/data/raw/AGA/finn-b-L12_ALOPECANDRO.vcf.gz",
                "/home/qrluo/data/data/aga_metabolism/data/raw/AGA/GCST90043616_buildGRCh37.tsv.gz",
                "/home/qrluo/data/data/aga_metabolism/data/raw/AGA/GCST90043617_buildGRCh37.tsv.gz",
                "/home/qrluo/data/data/aga_metabolism/data/raw/AGA/GCST90043618_buildGRCh37.tsv.gz",
                "/home/qrluo/data/data/aga_metabolism/data/raw/AGA/GCST90043619_buildGRCh37.tsv.gz",
                "/home/qrluo/data/data/aga_metabolism/data/raw/ANX/finn-b-F5_ALLANXIOUS.vcf.gz",
            ],
            "N": [119185, 207036, 207036, 207036, 207036, 210623],
        }
    )

    # 转换所有文件
    results = convert_from_metadata(
        metadata_df=trait_meta,
        file_column="file",
        metadata_columns=["trait", "N"],  # 将这些列作为元数据添加到结果中
        verbose=True,
    )

    # 查看结果
    for filename, df in results.items():
        print(f"\n{'='*80}")
        print(f"File: {filename}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(df.head(3))

    # 保存结果
    save_results(
        result_dict=results,
        output_dir="/home/qrluo/data/data/aga_metabolism/data/processed",
        file_prefix="std",
        output_format="tsv",
        compression="gzip",
    )

    return results


# ========================================
# 示例 3: 批量转换文件列表
# ========================================
def example_multiple_files():
    """批量转换文件列表的示例"""
    print("=" * 80)
    print("Example 3: Convert multiple files")
    print("=" * 80)

    file_list = [
        "/path/to/file1.tsv.gz",
        "/path/to/file2.tsv.gz",
        "/path/to/file3.vcf.gz",
    ]

    # 为每个文件指定元数据
    metadata = {
        "/path/to/file1.tsv.gz": {"trait": "AGA", "n": 119185},
        "/path/to/file2.tsv.gz": {"trait": "AGA", "n": 207036},
        "/path/to/file3.vcf.gz": {"trait": "ANX", "n": 210623},
    }

    results = convert_multiple_files(
        file_list=file_list, metadata=metadata, verbose=True
    )

    return results


# ========================================
# 示例 4: 使用自定义列名映射
# ========================================
def example_custom_mapping():
    """使用自定义列名映射的示例"""
    print("=" * 80)
    print("Example 4: Custom column mapping")
    print("=" * 80)

    # 手动指定某个文件的列名映射
    column_mapping = {
        "/path/to/special_file.tsv": {
            "SNP_ID": "rsid",
            "CHROM": "chr",
            "POS": "pos",
            "EFFECT": "beta",
            "P_VALUE": "pval",
        }
    }

    result = convert_single_file(
        filename="/path/to/special_file.tsv",
        column_mapping=column_mapping["/path/to/special_file.tsv"],
        verbose=True,
    )

    return result


# ========================================
# 示例 5: 添加自定义模式
# ========================================
def example_custom_patterns():
    """添加自定义正则表达式模式的示例"""
    print("=" * 80)
    print("Example 5: Custom regex patterns")
    print("=" * 80)

    # 添加自定义的列名识别模式
    custom_patterns = {
        "gene": re.compile(
            r"^(gene|gene_name|gene_symbol|nearest_gene)$", re.IGNORECASE
        ),
        "consequence": re.compile(
            r"^(consequence|csq|annotation|variant_class)$", re.IGNORECASE
        ),
    }

    result = convert_single_file(
        filename="/path/to/annotated_file.tsv",
        custom_patterns=custom_patterns,
        keep_unmatched=True,  # 保留未匹配的列
        verbose=True,
    )

    return result


# ========================================
# 示例 6: 合并多个文件的结果
# ========================================
def example_combine_results():
    """合并多个文件结果的示例"""
    print("=" * 80)
    print("Example 6: Combine results from multiple files")
    print("=" * 80)

    # 假设已经转换了多个文件
    results = convert_multiple_files(
        file_list=["/path/to/file1.tsv", "/path/to/file2.tsv"],
        metadata={
            "/path/to/file1.tsv": {"study": "study1"},
            "/path/to/file2.tsv": {"study": "study2"},
        },
    )

    # 合并所有结果
    combined_df = pd.concat(results.values(), ignore_index=True)

    print(f"Combined shape: {combined_df.shape}")
    print(f"Studies: {combined_df['study'].unique()}")

    return combined_df


# ========================================
# 示例 7: 查看支持的列名模式
# ========================================
def example_show_patterns():
    """显示所有支持的列名模式"""
    print("=" * 80)
    print("Example 7: Show all supported column name patterns")
    print("=" * 80)

    patterns = create_genetic_column_patterns()

    for field, pattern in patterns.items():
        # 从正则表达式中提取匹配的选项
        pattern_str = pattern.pattern
        # 移除正则符号
        pattern_str = (
            pattern_str.replace("^", "")
            .replace("$", "")
            .replace("(", "")
            .replace(")", "")
        )
        options = pattern_str.split("|")

        print(f"\n{field.upper()}:")
        print(f"  Recognized column names: {', '.join(options)}")


# ========================================
# 主函数
# ========================================
if __name__ == "__main__":
    # 运行你的用例
    example_from_metadata()

    # 或者运行其他示例
    # example_single_file()
    # example_custom_mapping()
    # example_custom_patterns()
    # example_show_patterns()
