# bioconverter 完整使用指南

## 概述

bioconverter 是一个通用的生物信息学数据转换工具，支持基因组学、转录组学、蛋白质组学和代谢组学等多组学数据格式的标准化转换。

**PyPI 包地址**: https://pypi.org/project/bioconverter/  
**GitHub 仓库**: https://github.com/Jeblqr/bioConv

---

## 一、Python 安装与使用

### 1.1 安装

#### 从 PyPI 安装（推荐）

```bash
pip install bioconverter
```

#### 从 GitHub 安装最新版本

```bash
pip install git+https://github.com/Jeblqr/bioConv.git
```

#### 验证安装

```bash
python -c "import convertor; print('bioconverter installed successfully')"
```

### 1.2 命令行接口（CLI）使用

安装后，可以通过 `bioconverter` 命令或 `python -m cli` 使用 CLI。

#### 基本用法

```bash
# 查看帮助
bioconverter --help

# 自动检测并转换（推荐）
bioconverter -i input_data.tsv -o output_data.tsv

# 仅显示文件信息，不进行转换
bioconverter -i input_data.tsv --info-only

# 显示所有支持的列名模式
bioconverter --show-patterns
```

#### 自动列映射（Auto-suggest）

```bash
# 使用自动建议的列映射
bioconverter -i gwas_data.tsv -o standardized_gwas.tsv --auto-suggest

# 带详细输出
bioconverter -i gwas_data.tsv -o output.tsv --auto-suggest --verbose

# 保留未匹配的列
bioconverter -i data.tsv -o output.tsv --auto-suggest --keep-unmatched
```

#### 交互式列映射

```bash
# 交互式逐列映射（推荐用于首次使用）
bioconverter -i custom_format.txt -o output.tsv --interactive

# 批量交互式映射（一次性输入所有映射）
bioconverter -i data.csv -o output.tsv --batch-interactive
```

#### 手动指定列映射

```bash
# 使用命令行参数指定映射
bioconverter -i input.txt -o output.tsv --map "CHR=chr,POS=pos,P=pval,BETA=beta"

# 从 CSV 文件读取映射
bioconverter -i input.txt -o output.tsv --map-file mapping.csv
```

#### 处理大文件

```bash
# 自动分块处理大文件（>100MB）
bioconverter -i large_file.tsv.gz -o output.tsv --auto-suggest

# 手动指定分块大小
bioconverter -i large_file.tsv -o output.tsv --chunk-size 50000

# 指定可用内存（GB）
bioconverter -i large_file.tsv -o output.tsv --memory 8
```

#### 输出格式选项

```bash
# 输出为 CSV
bioconverter -i input.tsv -o output.csv --output-format csv

# 输出为 Parquet（需要 pyarrow）
bioconverter -i input.tsv -o output.parquet --output-format parquet

# 禁用输出压缩
bioconverter -i input.tsv -o output.tsv --no-compression

# 默认输出为 gzip 压缩的 TSV
bioconverter -i input.tsv -o output.tsv.gz
```

#### 生成转换报告

```bash
# 生成转换报告（默认开启）
bioconverter -i input.tsv -o output.tsv --generate-report

# 指定报告保存目录
bioconverter -i input.tsv -o output.tsv --report-dir ./reports/
```

#### 处理 VCF 文件

```bash
# 自动检测 VCF 格式
bioconverter -i variants.vcf.gz -o standardized_variants.tsv

# 显式指定为 VCF
bioconverter -i data.txt -o output.tsv --vcf
```

#### 完整示例

```bash
# 基因组学 GWAS 数据转换
bioconverter -i gwas_summary.tsv -o standardized_gwas.tsv \
  --auto-suggest \
  --verbose \
  --generate-report \
  --report-dir ./reports/

# 转录组学 RNA-seq 数据
bioconverter -i deseq2_results.csv -o standardized_rnaseq.tsv \
  --auto-suggest \
  --keep-unmatched

# 大文件处理（5GB 数据）
bioconverter -i huge_dataset.tsv.gz -o output.tsv \
  --chunk-size 100000 \
  --memory 16 \
  --verbose
```

### 1.3 Python API 使用

#### 基本转换

```python
from convertor import convert_single_file

# 简单转换（自动检测格式）
result = convert_single_file(
    filename="input_data.tsv",
    verbose=True
)

# 保存结果
result.to_csv("output.tsv", sep='\t', index=False)
```

#### 批量转换多个文件

```python
from convertor import convert_multiple_files
import glob

# 批量转换目录中所有文件
files = glob.glob("data/*.tsv") + glob.glob("data/*.csv")
results = convert_multiple_files(
    file_list=files,
    keep_unmatched=False,
    verbose=True
)

# 查看结果
for filename, df in results.items():
    print(f"{filename}: {df.shape[0]} rows, {df.shape[1]} columns")

# 合并所有结果
import pandas as pd
combined = pd.concat(results.values(), ignore_index=True)
combined.to_csv("combined_output.tsv", sep='\t', index=False)
```

#### 自动建议与交互式映射

```python
from interactive_converter import (
    auto_suggest_mapping,
    auto_detect_omics_type,
    interactive_column_mapping
)
import pandas as pd

# 读取数据样本
df = pd.read_csv("input_data.csv", nrows=1000)

# 自动检测组学类型
omics_type = auto_detect_omics_type(df)
print(f"Detected omics type: {omics_type}")

# 自动建议列映射
suggested = auto_suggest_mapping(df)
print("Suggested mappings:")
for orig, std in suggested.items():
    print(f"  {orig} -> {std}")

# 交互式确认/修改映射（在终端运行）
mapping = interactive_column_mapping(df, suggested_mapping=suggested)
```

#### 处理大文件（分块）

```python
from interactive_converter import process_large_file, suggest_chunk_size

# 自动建议分块大小
chunk_size = suggest_chunk_size("large_file.tsv", available_memory_gb=8.0)
print(f"Suggested chunk size: {chunk_size}")

# 分块处理
process_large_file(
    filename="large_file.tsv.gz",
    output_file="output.tsv",
    column_mapping={"CHR": "chr", "POS": "pos", "P": "pval"},
    chunksize=chunk_size,
    verbose=True,
    sep='\t'
)
```

#### 获取支持的列名模式

```python
from convertor import create_genetic_column_patterns

# 获取所有支持的模式
patterns = create_genetic_column_patterns()

# 查看基因组学相关模式
print("Genomics patterns:")
for std_name, pattern in patterns.items():
    if 'chr' in std_name or 'pos' in std_name or 'pval' in std_name:
        print(f"  {std_name}: {pattern.pattern}")
```

#### 自定义列映射

```python
from convertor import convert_single_file

# 手动指定列映射
custom_mapping = {
    "Chromosome": "chr",
    "Position": "pos",
    "P-value": "pval",
    "Effect": "beta",
    "StdErr": "se"
}

result = convert_single_file(
    filename="custom_format.txt",
    column_mapping=custom_mapping,
    keep_unmatched=True,  # 保留未映射的列
    verbose=True
)
```

#### 生成转换报告

```python
from conversion_report import ConversionReport

# 创建报告对象
report = ConversionReport()

# 设置输入信息
report.set_input_info(
    filename="input.tsv",
    columns=["CHR", "POS", "SNP", "P"],
    rows=10000,
    file_size_mb=5.2,
    omics_type="genomics"
)

# 设置输出信息
report.set_output_info(
    filename="output.tsv",
    columns=["chr", "pos", "rsid", "pval"]
)

# 设置列映射
report.set_column_mapping(
    mapping={"CHR": "chr", "POS": "pos", "SNP": "rsid", "P": "pval"},
    unmapped=[]
)

# 设置处理信息
report.set_processing_info()

# 保存报告
report.save_report(report_dir="./reports/", prefix="conversion")
```

#### 完整示例：端到端工作流

```python
import pandas as pd
from convertor import convert_single_file
from interactive_converter import auto_suggest_mapping, auto_detect_omics_type
from conversion_report import ConversionReport

# 1. 读取样本数据
df_sample = pd.read_csv("input_data.tsv", sep='\t', nrows=100)

# 2. 自动检测数据类型
omics_type = auto_detect_omics_type(df_sample)
print(f"Detected: {omics_type}")

# 3. 获取建议映射
mapping = auto_suggest_mapping(df_sample)
print("Suggested mappings:", mapping)

# 4. 执行转换
result = convert_single_file(
    filename="input_data.tsv",
    column_mapping=mapping,
    verbose=True
)

# 5. 保存结果
output_file = "standardized_output.tsv"
result.to_csv(output_file, sep='\t', index=False)

print(f"Conversion complete: {result.shape[0]} rows, {result.shape[1]} columns")
print(f"Output saved to: {output_file}")
```

---

## 二、R 包安装与使用

### 2.1 安装

#### 从 GitHub 安装（推荐）

```r
# 安装 remotes 包（如果尚未安装）
if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes")
}

# 从 GitHub 安装 bioconverter
remotes::install_github("Jeblqr/bioConv")
```

#### 安装依赖

bioconverter R 包需要以下依赖：

1. **R 包依赖**：`reticulate`、`tibble`、`readr`
2. **Python 依赖**：Python (>= 3.8) 和 `bioconverter` Python 包

```r
# 安装 R 包依赖
install.packages(c("reticulate", "tibble", "readr"))

# 安装 Python bioconverter 包
reticulate::py_install("bioconverter", pip = TRUE)
```

#### 配置 Python 环境（可选）

如果你有特定的 Python 环境（如 conda/virtualenv），需要在使用前配置：

```r
library(reticulate)

# 方式 1: 使用特定 Python
use_python("/path/to/python", required = TRUE)

# 方式 2: 使用 conda 环境
use_condaenv("your-env-name", required = TRUE)

# 方式 3: 使用 virtualenv
use_virtualenv("path/to/venv", required = TRUE)
```

### 2.2 R 包使用

#### 加载包

```r
library(bioconverter)
```

#### 基本转换

```r
# 转换单个文件（自动检测格式和列映射）
result <- convert_file(
  input_file = "gwas_data.tsv",
  output_file = "standardized_gwas.tsv",
  verbose = TRUE
)

# 查看结果
print(head(result))
print(dim(result))
```

#### 手动指定列映射

```r
# 使用命名列表指定映射
custom_mapping <- list(
  CHR = "chr",
  POS = "pos",
  SNP = "rsid",
  P = "pval",
  BETA = "beta",
  SE = "se"
)

result <- convert_file(
  input_file = "custom_data.txt",
  output_file = "output.tsv",
  column_mapping = custom_mapping,
  keep_unmatched = FALSE,
  verbose = TRUE
)
```

#### 自动建议列映射

```r
# 获取自动建议的列映射
suggestions <- auto_suggest_mapping("input_data.tsv", n_rows = 1000)

# 查看建议
print(suggestions)

# 使用建议进行转换
result <- convert_file(
  input_file = "input_data.tsv",
  output_file = "output.tsv",
  column_mapping = suggestions,
  verbose = FALSE
)
```

#### 获取支持的列名模式

```r
# 获取所有支持的列名模式
patterns <- get_column_patterns()

# 查看不同组学类型的模式
print(patterns$genomics)
print(patterns$transcriptomics)
print(patterns$proteomics)
print(patterns$metabolomics)
```

#### 生成转换报告

```r
# 转换时自动生成报告
result <- convert_file(
  input_file = "input.tsv",
  output_file = "output.tsv",
  generate_report = TRUE,
  report_dir = "./reports/",
  verbose = TRUE
)

# 手动生成报告
generate_conversion_report(
  input_file = "input.tsv",
  output_file = "output.tsv",
  original_columns = c("CHR", "POS", "P"),
  final_columns = c("chr", "pos", "pval"),
  column_mapping = list(CHR = "chr", POS = "pos", P = "pval"),
  report_dir = "./reports/",
  omics_type = "genomics"
)
```

#### 使用 Python CLI（推荐用于交互式映射）

R 不适合交互式命令行输入，对于需要交互式列映射的场景，建议使用 Python CLI：

```r
# 获取使用 Python CLI 的提示
convert_with_mapping("input_data.tsv")

# 或者直接在 R 中调用 system 命令
system("bioconverter -i input_data.tsv -o output.tsv --interactive")
```

#### 完整示例

```r
library(bioconverter)
library(dplyr)

# 1. 转换基因组学数据
gwas_result <- convert_file(
  input_file = "gwas_summary.tsv",
  output_file = "standardized_gwas.tsv",
  verbose = TRUE,
  generate_report = TRUE
)

# 2. 查看结果
print(head(gwas_result))
print(paste("Dimensions:", nrow(gwas_result), "rows,", ncol(gwas_result), "columns"))

# 3. 进行后续分析
significant_variants <- gwas_result %>%
  filter(pval < 5e-8) %>%
  arrange(pval)

print(paste("Found", nrow(significant_variants), "significant variants"))

# 4. 转换转录组学数据
rnaseq_result <- convert_file(
  input_file = "deseq2_results.csv",
  output_file = "standardized_rnaseq.tsv",
  verbose = FALSE
)

# 5. 合并多个数据集（如果适用）
# 注意：只有在列结构兼容时才能合并
```

#### 批量转换

```r
# 批量转换多个文件
library(purrr)

files <- c("file1.tsv", "file2.csv", "file3.txt")

results <- map(files, ~{
  convert_file(
    input_file = .x,
    output_file = paste0("standardized_", basename(.x)),
    verbose = FALSE
  )
})

# 查看所有结果
walk2(files, results, ~{
  cat(sprintf("%s: %d rows, %d cols\n", .x, nrow(.y), ncol(.y)))
})
```

---

## 三、支持的数据类型和标准列名

### 3.1 基因组学（Genomics）

**标准列名**：

- `chr` - 染色体
- `pos` - 位置
- `rsid` - SNP/变异位点标识符
- `ref` - 参考等位基因
- `alt` - 替代/效应等位基因
- `pval` - P 值
- `beta` - 效应大小
- `se` - 标准误
- `or` - 比值比
- `frq` - 等位基因频率
- `n` - 样本数
- `info` - 插补质量

**支持的输入格式**：

- GWAS 汇总统计
- VCF 文件
- SNP 数据
- 关联研究结果

### 3.2 转录组学（Transcriptomics）

**标准列名**：

- `gene_id` - 基因标识符（如 ENSG）
- `gene_name` - 基因符号
- `transcript_id` - 转录本标识符
- `expression` - 表达值
- `fpkm` - FPKM 值
- `tpm` - TPM 值
- `counts` - 读数计数
- `log2fc` - Log2 倍数变化
- `padj` - 校正后 P 值

**支持的输入格式**：

- RNA-seq 计数数据
- FPKM/TPM 表达值
- 差异表达分析结果（DESeq2, edgeR 等）
- 基因表达矩阵

### 3.3 蛋白质组学（Proteomics）

**标准列名**：

- `protein_id` - 蛋白质标识符
- `protein_name` - 蛋白质名称
- `peptide` - 肽段序列
- `abundance` - 蛋白质丰度
- `intensity` - 信号强度
- `ratio` - 倍数变化比率

**支持的输入格式**：

- 蛋白质丰度数据
- 肽段强度测量
- 定量蛋白质组学结果（MaxQuant 等）

### 3.4 代谢组学（Metabolomics）

**标准列名**：

- `metabolite_id` - 代谢物标识符
- `metabolite_name` - 代谢物名称
- `mz` - 质荷比
- `rt` - 保留时间
- `concentration` - 浓度
- `peak_area` - 峰面积

**支持的输入格式**：

- 代谢物浓度
- LC-MS/GC-MS 峰数据
- 代谢物鉴定结果

### 3.5 样本信息（Sample Information）

**标准列名**：

- `sample_id` - 样本标识符
- `condition` - 实验条件
- `timepoint` - 时间点
- `replicate` - 重复编号
- `batch` - 批次标识符

---

## 四、常见问题与解决方案

### 4.1 Python 相关

**Q: 导入 bioconverter 时出错？**

A: 确保已安装：

```bash
pip install bioconverter
python -c "import convertor"
```

**Q: 如何处理非常大的文件（>10GB）？**

A: 使用分块处理：

```bash
bioconverter -i huge_file.tsv -o output.tsv --chunk-size 50000 --memory 16
```

**Q: 如何处理自定义分隔符？**

A: 使用 `--sep` 参数：

```bash
bioconverter -i data.txt -o output.tsv --sep "|"
```

### 4.2 R 相关

**Q: R 中找不到 Python 模块？**

A: 配置 Python 环境：

```r
library(reticulate)
use_python("/path/to/python", required = TRUE)
py_install("bioconverter", pip = TRUE)
```

**Q: reticulate 报错？**

A: 确保安装了正确版本：

```r
install.packages("reticulate")
library(reticulate)
py_config()  # 查看 Python 配置
```

**Q: 如何在 R 中使用交互式映射？**

A: 建议使用 Python CLI：

```r
system("bioconverter -i input.tsv -o output.tsv --interactive")
```

### 4.3 通用问题

**Q: 如何查看支持的所有列名模式？**

A:

```bash
bioconverter --show-patterns
```

或在 Python 中：

```python
from convertor import create_genetic_column_patterns
patterns = create_genetic_column_patterns()
for name in sorted(patterns.keys()):
    print(name)
```

**Q: 转换后的数据丢失了某些列？**

A: 使用 `--keep-unmatched` 保留未匹配的列：

```bash
bioconverter -i input.tsv -o output.tsv --keep-unmatched
```

**Q: 如何自定义列映射？**

A: 使用 `--map` 参数或在代码中指定 `column_mapping`。

---

## 五、高级用法

### 5.1 创建自定义列模式

```python
import re
from convertor import convert_single_file

# 定义自定义模式
custom_patterns = {
    'my_field': re.compile(r'^(my_field|custom_name)$', re.IGNORECASE)
}

# 使用自定义模式
result = convert_single_file(
    filename="data.tsv",
    custom_patterns=custom_patterns
)
```

### 5.2 Pipeline 集成

```bash
#!/bin/bash
# 批量处理 pipeline

for file in data/*.tsv; do
  output="processed/$(basename $file)"
  bioconverter -i "$file" -o "$output" --auto-suggest --verbose
done

echo "All files processed!"
```

### 5.3 与其他工具集成

```python
# 与 Pandas pipeline 集成
import pandas as pd
from convertor import convert_single_file

# 转换
df = convert_single_file("input.tsv")

# 后续分析
df_filtered = df[df['pval'] < 0.05]
df_filtered = df_filtered.sort_values('pval')

# 进一步处理
result = df_filtered.groupby('chr').agg({
    'pval': 'min',
    'beta': 'mean'
})

print(result)
```

---

## 六、性能说明

- **小文件（<100MB）**：内存中处理，非常快速
- **中等文件（100MB-1GB）**：自动分块（200K 行/块）
- **大文件（1-10GB）**：自动分块（100K 行/块）
- **超大文件（>10GB）**：自动分块（50K 行/块）

内存使用默认优化为不超过 4GB（可配置）。

---

## 七、获取帮助

- **GitHub Issues**: https://github.com/Jeblqr/bioConv/issues
- **PyPI 主页**: https://pypi.org/project/bioconverter/
- **文档**: 查看仓库 README.md

---

## 八、许可证

MIT License - 可自由用于学术研究和商业应用。
