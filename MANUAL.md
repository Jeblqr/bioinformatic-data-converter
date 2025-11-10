# Bioconverter User Manual

**Version:** 0.1.0  
**Last Updated:** 2024-11-10

A comprehensive guide for using the Bioinformatics Data Converter in both Python and R.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Python Usage](#python-usage)
5. [R Usage](#r-usage)
6. [Column Mapping](#column-mapping)
7. [Large File Processing](#large-file-processing)
8. [Conversion Reports](#conversion-reports)
9. [API Reference](#api-reference)
10. [Examples by Data Type](#examples-by-data-type)
11. [Troubleshooting](#troubleshooting)

---

## 1. Installation

### Python Installation

#### From Source (Development)
```bash
git clone https://github.com/Jeblqr/bioinformatic-data-converter.git
cd bioinformatic-data-converter
pip install -e .
```

#### From PyPI (Once Published)
```bash
pip install bioconverter
```

#### Dependencies
- Python >= 3.8
- pandas >= 2.0.0
- numpy >= 1.24.0
- pyarrow >= 12.0.0

### R Installation

#### From Source (Development)
```r
# Install devtools if not already installed
install.packages("devtools")

# Install from GitHub
devtools::install_github("Jeblqr/bioinformatic-data-converter")
```

#### From CRAN (Once Published)
```r
install.packages("bioconverter")
```

#### Dependencies
- R >= 3.6.0
- reticulate >= 1.20
- readr >= 2.0.0
- dplyr >= 1.0.0
- tibble >= 3.0.0
- jsonlite >= 1.7.0

**Note:** The R package uses `reticulate` to interface with the Python implementation.

---

## 2. Quick Start

### Python Quick Start

```python
# Command-line interface
bioconverter -i input.tsv -o output.tsv --auto-suggest

# Python API
from convertor import convert_single_file

result = convert_single_file(
    filename="gwas_data.tsv",
    verbose=True
)
```

### R Quick Start

```r
library(bioconverter)

# Convert a file
result <- convert_file(
  input_file = "gwas_data.tsv",
  output_file = "standardized_gwas.tsv"
)

# View the result
head(result)
```

---

## 3. Core Concepts

### Supported Omics Types

1. **Genomics**: GWAS summary statistics, VCF files, SNP data
2. **Transcriptomics**: RNA-seq counts, differential expression, FPKM/TPM
3. **Proteomics**: Protein abundance, peptide intensity
4. **Metabolomics**: Metabolite concentrations, LC-MS/GC-MS data

### Standardized Fields

| Category | Fields |
|----------|--------|
| **Genomics** | chr, pos, rsid, ref, alt, pval, beta, se, or, frq, n, info |
| **Transcriptomics** | gene_id, gene_name, transcript_id, expression, fpkm, tpm, counts, log2fc, padj |
| **Proteomics** | protein_id, protein_name, peptide, abundance, intensity, ratio |
| **Metabolomics** | metabolite_id, metabolite_name, mz, rt, concentration, peak_area |
| **Sample Info** | sample_id, condition, timepoint, replicate, batch |

### Processing Modes

1. **Auto-suggest**: Automatic column mapping based on patterns
2. **Interactive**: Step-by-step user-guided mapping
3. **Batch Interactive**: All mappings entered at once
4. **Manual**: Explicit column specification

---

## 4. Python Usage

### 4.1 Command-Line Interface

#### Basic Conversion
```bash
# Show file information only
bioconverter -i data.tsv --info-only

# Auto-suggest mappings
bioconverter -i data.tsv -o output.tsv --auto-suggest

# Interactive mapping
bioconverter -i data.tsv -o output.tsv --interactive

# Manual mapping
bioconverter -i data.txt -o output.tsv --map "CHR=chr,POS=pos,P=pval"
```

#### Advanced Options
```bash
# Large file with chunking
bioconverter -i large_file.tsv.gz -o output.tsv --chunk-size 100000

# Keep unmapped columns
bioconverter -i data.tsv -o output.tsv --auto-suggest --keep-unmatched

# Different output format
bioconverter -i data.csv -o output.parquet --auto-suggest --output-format parquet

# Show all supported patterns
bioconverter --show-patterns
```

### 4.2 Python API

#### Simple Conversion
```python
from convertor import convert_single_file

# Convert with auto-detection
result = convert_single_file(
    filename="gwas_data.tsv",
    verbose=True
)

print(result.head())
```

#### With Column Mapping
```python
from convertor import convert_single_file

# Manual column mapping
mapping = {
    "CHR": "chr",
    "POS": "pos",
    "SNP": "rsid",
    "P": "pval"
}

result = convert_single_file(
    filename="data.txt",
    column_mapping=mapping,
    keep_unmatched=True,
    verbose=True
)
```

#### Auto-Suggest Mapping
```python
import pandas as pd
from interactive_converter import auto_suggest_mapping

# Read sample data
df = pd.read_csv("data.tsv", sep="\t", nrows=1000)

# Get suggestions
suggested = auto_suggest_mapping(df)
print("Suggested mappings:", suggested)

# Use suggestions
from convertor import standardize_columns
result = standardize_columns(df, column_mapping=suggested)
```

#### Large File Processing
```python
from interactive_converter import process_large_file, suggest_chunk_size

# Get suggested chunk size
chunk_size = suggest_chunk_size("large_file.tsv", available_memory_gb=8.0)

# Process with chunking
mapping = {"CHR": "chr", "POS": "pos", "P": "pval"}

process_large_file(
    filename="large_file.tsv",
    output_file="output.tsv",
    column_mapping=mapping,
    chunksize=chunk_size,
    verbose=True,
    sep="\t"
)
```

#### Generate Conversion Report
```python
from conversion_report import ConversionReport

# Create report
report = ConversionReport()

# Set information
report.set_input_info(
    filename="input.tsv",
    columns=original_columns,
    rows=n_rows,
    file_size_mb=file_size,
    omics_type="genomics"
)

report.set_column_mapping(mapping, unmapped_columns)
report.set_processing_info()

# Save reports
report.save_report("./reports", "my_conversion")

# Print summary
report.print_summary()
```

---

## 5. R Usage

### 5.1 Basic Conversion

```r
library(bioconverter)

# Simple conversion with auto-suggestion
result <- convert_file(
  input_file = "gwas_data.tsv",
  output_file = "standardized_gwas.tsv"
)

# View results
head(result)
dim(result)
```

### 5.2 With Manual Mapping

```r
# Define column mapping
my_mapping <- list(
  CHR = "chr",
  POS = "pos",
  SNP = "rsid",
  P = "pval",
  BETA = "beta"
)

# Convert with custom mapping
result <- convert_file(
  input_file = "data.txt",
  output_file = "output.tsv",
  column_mapping = my_mapping,
  keep_unmatched = TRUE
)
```

### 5.3 Auto-Suggest Mappings

```r
# Get automatic suggestions
suggestions <- auto_suggest_mapping("my_data.tsv")

# Review suggestions
print(suggestions)

# Use suggestions for conversion
result <- convert_file(
  input_file = "my_data.tsv",
  output_file = "output.tsv",
  column_mapping = suggestions
)
```

### 5.4 View Supported Patterns

```r
# Get all supported column patterns
patterns <- get_column_patterns()

# View by category
print(patterns$genomics)
print(patterns$transcriptomics)
print(patterns$proteomics)
print(patterns$metabolomics)
```

### 5.5 Generate Reports

```r
# Conversion with report generation
result <- convert_file(
  input_file = "data.tsv",
  output_file = "output.tsv",
  generate_report = TRUE,
  report_dir = "./reports"
)

# Reports will be saved as:
# - ./reports/conversion_report.txt
# - ./reports/conversion_report.json
# - ./reports/conversion_report_mapping.csv
```

---

## 6. Column Mapping

### 6.1 Understanding Column Patterns

The converter recognizes over 135 column name variations. Examples:

**Genomics:**
- Chromosome: `chr`, `chromosome`, `chrom`, `CHR`, `#CHROM`
- Position: `pos`, `position`, `bp`, `POS`, `base_position`
- P-value: `p`, `pval`, `p_value`, `pvalue`, `P`, `P_VALUE`

**Transcriptomics:**
- Gene ID: `gene_id`, `geneid`, `ensembl_id`, `ENSG`
- Gene Name: `gene_name`, `gene_symbol`, `symbol`, `gene`
- Log2FC: `log2fc`, `log2_fold_change`, `log2foldchange`, `lfc`

### 6.2 Custom Patterns (Python Only)

```python
import re
from convertor import convert_single_file

# Define custom patterns
custom_patterns = {
    'my_field': re.compile(r'^(myfield|my_field|custom)$', re.IGNORECASE)
}

# Use in conversion
result = convert_single_file(
    filename="data.tsv",
    custom_patterns=custom_patterns
)
```

### 6.3 Interactive Mapping (Python CLI)

```bash
# Start interactive mode
bioconverter -i data.tsv -o output.tsv --interactive

# Follow prompts:
# For each column, enter the standard name or press Enter to skip
# CHR -> chr
# POS -> pos
# P_VALUE -> pval
# ...

# Preview and confirm before processing
```

---

## 7. Large File Processing

### 7.1 Chunked Processing (Python)

```python
from interactive_converter import process_large_file, suggest_chunk_size

# Automatic chunk size suggestion
chunk_size = suggest_chunk_size("huge_file.tsv", available_memory_gb=4.0)

print(f"Suggested chunk size: {chunk_size}")

# Process with chunking
mapping = {"CHR": "chr", "POS": "pos"}

process_large_file(
    filename="huge_file.tsv",
    output_file="output.tsv",
    column_mapping=mapping,
    chunksize=chunk_size or 100000,
    verbose=True,
    sep="\t"
)
```

### 7.2 Memory Management

| File Size | Suggested Chunk Size | Memory Usage |
|-----------|---------------------|--------------|
| <500MB | No chunking | ~2x file size |
| 500MB-2GB | 200K rows | ~500MB |
| 2-10GB | 100K rows | ~250MB |
| >10GB | 50K rows | ~150MB |

### 7.3 Progress Tracking

For large files, the converter displays progress:
```
Processing large file: huge_data.tsv
Chunk size: 100000 rows
  Processed 100,000 rows...
  Processed 200,000 rows...
  ...
  Complete! Total rows processed: 5,000,000
```

---

## 8. Conversion Reports

### 8.1 Report Contents

Each conversion generates three report files:

1. **Text Report** (`conversion_report.txt`): Human-readable summary
2. **JSON Report** (`conversion_report.json`): Machine-readable data
3. **Mapping CSV** (`conversion_report_mapping.csv`): Column mapping table

### 8.2 Text Report Example

```
================================================================================
BIOINFORMATICS DATA CONVERSION REPORT
================================================================================

Generated: 2024-11-10 09:45:00

INPUT INFORMATION
--------------------------------------------------------------------------------
File: gwas_data.tsv
File Size: 125.50 MB
Detected Type: genomics
Rows: 1,234,567
Original Columns: 9

PROCESSING INFORMATION
--------------------------------------------------------------------------------
Method: in-memory

COLUMN MAPPING
--------------------------------------------------------------------------------
Columns Mapped: 9
Columns Unmapped: 0

Mapped Columns:
  CHR                            -> chr
  POS                            -> pos
  SNP                            -> rsid
  ...

OUTPUT INFORMATION
--------------------------------------------------------------------------------
File: standardized_gwas.tsv
Final Columns: 9
Rows Written: 1,234,567
```

### 8.3 Using Reports (Python)

```python
import json
import pandas as pd

# Read JSON report
with open("conversion_report.json") as f:
    report_data = json.load(f)

print(f"Input file: {report_data['input']['file']}")
print(f"Omics type: {report_data['input']['omics_type']}")
print(f"Mapped columns: {report_data['mapping']['mapping_count']}")

# Read mapping CSV
mapping_df = pd.read_csv("conversion_report_mapping.csv")
print(mapping_df)
```

### 8.4 Using Reports (R)

```r
library(jsonlite)
library(readr)

# Read JSON report
report <- fromJSON("conversion_report.json")

cat("Input file:", report$input$file, "\n")
cat("Omics type:", report$input$omics_type, "\n")
cat("Rows processed:", report$input$rows, "\n")

# Read mapping CSV
mapping <- read_csv("conversion_report_mapping.csv")
print(mapping)
```

---

## 9. API Reference

### 9.1 Python Functions

#### `convert_single_file()`
Convert a single file with auto-detection.

**Parameters:**
- `filename` (str): Input file path
- `sep` (str, optional): Column separator
- `compression` (str, optional): Compression format
- `column_mapping` (dict, optional): Manual column mapping
- `custom_patterns` (dict, optional): Custom regex patterns
- `metadata` (dict, optional): Metadata to add
- `keep_unmatched` (bool): Keep unmapped columns
- `verbose` (bool): Print detailed information

**Returns:** pandas DataFrame

#### `process_large_file()`
Process large files with chunking.

**Parameters:**
- `filename` (str): Input file path
- `output_file` (str): Output file path
- `column_mapping` (dict): Column mapping
- `chunksize` (int): Rows per chunk
- `verbose` (bool): Show progress
- `**read_kwargs`: Additional read arguments

#### `auto_suggest_mapping()`
Automatically suggest column mappings.

**Parameters:**
- `df` (DataFrame): Input DataFrame
- `custom_patterns` (dict, optional): Custom patterns

**Returns:** dict of suggested mappings

### 9.2 R Functions

#### `convert_file()`
Main conversion function for R.

**Arguments:**
- `input_file`: Path to input file
- `output_file`: Path to output file
- `auto_suggest`: Use automatic mapping (default: TRUE)
- `column_mapping`: Named list of mappings
- `keep_unmatched`: Keep unmapped columns (default: FALSE)
- `verbose`: Print information (default: TRUE)
- `generate_report`: Create conversion report (default: TRUE)
- `report_dir`: Directory for reports

**Returns:** tibble

#### `get_column_patterns()`
Get supported column patterns.

**Returns:** List of pattern categories

#### `auto_suggest_mapping()`
Get automatic mapping suggestions.

**Arguments:**
- `input_file`: Path to input file
- `n_rows`: Rows to analyze (default: 1000)

**Returns:** Named list of suggestions

---

## 10. Examples by Data Type

### 10.1 Genomics (GWAS)

**Python:**
```python
result = convert_single_file(
    filename="gwas_summary_stats.tsv.gz",
    verbose=True
)
# Auto-detects: chr, pos, rsid, pval, beta, se, etc.
```

**R:**
```r
result <- convert_file(
  input_file = "gwas_summary_stats.tsv.gz",
  output_file = "standardized_gwas.tsv"
)
```

### 10.2 Transcriptomics (RNA-seq)

**Python:**
```python
result = convert_single_file(
    filename="deseq2_results.csv",
    verbose=True
)
# Auto-detects: gene_id, gene_name, log2fc, pval, padj
```

**R:**
```r
result <- convert_file(
  input_file = "deseq2_results.csv",
  output_file = "standardized_rnaseq.tsv"
)
```

### 10.3 Proteomics

**Python:**
```python
result = convert_single_file(
    filename="protein_abundance.tsv",
    verbose=True
)
# Auto-detects: protein_id, protein_name, abundance, intensity
```

**R:**
```r
result <- convert_file(
  input_file = "protein_abundance.tsv",
  output_file = "standardized_proteomics.tsv"
)
```

### 10.4 Metabolomics

**Python:**
```python
result = convert_single_file(
    filename="lcms_results.csv",
    verbose=True
)
# Auto-detects: metabolite_name, mz, rt, peak_area, concentration
```

**R:**
```r
result <- convert_file(
  input_file = "lcms_results.csv",
  output_file = "standardized_metabolomics.tsv"
)
```

---

## 11. Troubleshooting

### Common Issues

#### Issue: "Module not found" error in R
**Solution:**
```r
# Install reticulate if not present
install.packages("reticulate")

# Install Python package
reticulate::py_install("bioconverter", pip = TRUE)
```

#### Issue: Memory error with large files
**Solution:**
```python
# Use chunked processing
from interactive_converter import process_large_file

process_large_file(
    filename="large_file.tsv",
    output_file="output.tsv",
    column_mapping=mapping,
    chunksize=50000  # Reduce chunk size
)
```

#### Issue: No columns auto-mapped
**Solution:**
```bash
# View supported patterns
bioconverter --show-patterns

# Use manual mapping
bioconverter -i data.txt -o output.tsv --map "OLD_NAME=new_name"
```

#### Issue: VCF file not parsing correctly
**Solution:**
```python
# Explicitly specify VCF format
from convertor import read_vcf_file

df = read_vcf_file("file.vcf.gz", compression="gzip")
```

### Getting Help

- **GitHub Issues**: https://github.com/Jeblqr/bioinformatic-data-converter/issues
- **Documentation**: Check README.md and IMPLEMENTATION_SUMMARY.md
- **Examples**: See examples.py and demo.sh

---

## Appendix: Complete Pattern Reference

### Genomics Patterns
- **chr**: chr, chromosome, chrom, #chr, #chrom, #CHROM, seqname
- **pos**: pos, position, bp, base_pair, base_position, ps, POS, start, end
- **rsid**: rsid, snp, snpid, snp_id, variant_id, varid, id, ID, marker, rs
- **ref**: ref, reference, ref_allele, reference_allele, REF, a2, allele2
- **alt**: alt, alternate, alt_allele, ALT, a1, allele1, effect_allele
- **pval**: p, pval, p_value, pvalue, p-value, P, pval_nominal
- **beta**: beta, b, effect, coef, coefficient, effect_size, BETA, slope
- **se**: se, stderr, standard_error, std_err, SE
- **or**: or, odds_ratio, oddsratio, OR
- **frq**: frq, freq, frequency, maf, af, eaf, allele_freq, AF
- **n**: n, n_samples, sample_size, nsize, ns, N
- **info**: info, imputation_quality, r2, rsq, INFO

### Transcriptomics Patterns
- **gene_id**: gene_id, geneid, ensembl_id, ensembl, ensg
- **gene_name**: gene_name, genename, gene_symbol, symbol, gene
- **transcript_id**: transcript_id, transcriptid, enst
- **expression**: expression, expr, value
- **fpkm**: fpkm, rpkm
- **tpm**: tpm, transcripts_per_million
- **counts**: counts, read_count, reads
- **log2fc**: log2fc, log2_fold_change, log2foldchange, lfc
- **padj**: padj, adj_pval, adjusted_pvalue, fdr, qval, q_value

### Proteomics Patterns
- **protein_id**: protein_id, proteinid, uniprot, uniprot_id
- **protein_name**: protein_name, proteinname, protein
- **peptide**: peptide, peptide_sequence, sequence
- **abundance**: abundance, protein_abundance
- **intensity**: intensity, signal, signal_intensity
- **ratio**: ratio, fold_change, fc

### Metabolomics Patterns
- **metabolite_id**: metabolite_id, metaboliteid, compound_id, hmdb, hmdb_id
- **metabolite_name**: metabolite_name, metabolite, compound, compound_name
- **mz**: mz, m/z, mass, mass_to_charge
- **rt**: rt, retention_time, retentiontime
- **concentration**: concentration, conc, amount
- **peak_area**: peak_area, area, peak_intensity

---

**End of Manual**
