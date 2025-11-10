#!/bin/bash
#
# Bash Example: Using bioconverter CLI for data conversion
#
# This example demonstrates how to use bioconverter from the command line.

set -e  # Exit on error

echo "============================================================="
echo "bioconverter Bash/CLI Examples"
echo "============================================================="
echo ""

# Example 1: Basic conversion with auto-detection
echo "============================================================="
echo "Example 1: Basic Conversion with Auto-detection"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/genomics_gwas.tsv -o output_bash_1.tsv"
echo ""

bioconverter -i test_data/genomics_gwas.tsv -o output_bash_1.tsv

echo ""
echo "✓ Output saved to: output_bash_1.tsv"
echo ""


# Example 2: Auto-suggest mapping with verbose output
echo "============================================================="
echo "Example 2: Auto-suggest Mapping (Verbose)"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/transcriptomics_rnaseq.csv -o output_bash_2.tsv --auto-suggest --verbose"
echo ""

bioconverter -i test_data/transcriptomics_rnaseq.csv \
  -o output_bash_2.tsv \
  --auto-suggest \
  --verbose

echo ""
echo "✓ Output saved to: output_bash_2.tsv"
echo ""


# Example 3: Keep unmatched columns
echo "============================================================="
echo "Example 3: Keep Unmatched Columns"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/proteomics_data.tsv -o output_bash_3.tsv --keep-unmatched"
echo ""

bioconverter -i test_data/proteomics_data.tsv \
  -o output_bash_3.tsv \
  --keep-unmatched

echo ""
echo "✓ Output saved to: output_bash_3.tsv"
echo ""


# Example 4: Manual column mapping
echo "============================================================="
echo "Example 4: Manual Column Mapping"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/genomics_gwas.tsv -o output_bash_4.tsv --map 'chr=chr,pos=pos,pval=pval'"
echo ""

bioconverter -i test_data/genomics_gwas.tsv \
  -o output_bash_4.tsv \
  --map "chr=chr,pos=pos,pval=pval"

echo ""
echo "✓ Output saved to: output_bash_4.tsv"
echo ""


# Example 5: Generate report
echo "============================================================="
echo "Example 5: Generate Conversion Report"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/metabolomics_data.csv -o output_bash_5.tsv --generate-report --report-dir ./reports/"
echo ""

bioconverter -i test_data/metabolomics_data.csv \
  -o output_bash_5.tsv \
  --generate-report \
  --report-dir ./reports/

echo ""
echo "✓ Output saved to: output_bash_5.tsv"
echo "✓ Report saved to: ./reports/"
echo ""


# Example 6: Show file information only (no conversion)
echo "============================================================="
echo "Example 6: Show File Information (No Conversion)"
echo "============================================================="
echo ""
echo "Command: bioconverter -i test_data/genomics_gwas.tsv --info-only"
echo ""

bioconverter -i test_data/genomics_gwas.tsv --info-only

echo ""


# Example 7: Show all supported column patterns
echo "============================================================="
echo "Example 7: Show Supported Column Patterns"
echo "============================================================="
echo ""
echo "Command: bioconverter --show-patterns | head -20"
echo ""

bioconverter --show-patterns | head -20

echo ""
echo "... (truncated, use 'bioconverter --show-patterns' to see all)"
echo ""


# Example 8: Process compressed file
echo "============================================================="
echo "Example 8: Process Compressed File"
echo "============================================================="
echo ""

# First, create a compressed test file if it doesn't exist
if [ ! -f test_data/genomics_gwas.tsv.gz ]; then
  echo "Creating compressed test file..."
  gzip -c test_data/genomics_gwas.tsv > test_data/genomics_gwas.tsv.gz
fi

echo "Command: bioconverter -i test_data/genomics_gwas.tsv.gz -o output_bash_8.tsv"
echo ""

bioconverter -i test_data/genomics_gwas.tsv.gz \
  -o output_bash_8.tsv

echo ""
echo "✓ Compressed file processed and saved to: output_bash_8.tsv"
echo ""


# Example 9: Output to different formats
echo "============================================================="
echo "Example 9: Output to Different Formats"
echo "============================================================="
echo ""

# CSV output
echo "Command: bioconverter -i test_data/genomics_gwas.tsv -o output_bash_9.csv --output-format csv"
echo ""

bioconverter -i test_data/genomics_gwas.tsv \
  -o output_bash_9.csv \
  --output-format csv

echo "✓ CSV output saved to: output_bash_9.csv"
echo ""


# Example 10: Batch processing with shell loop
echo "============================================================="
echo "Example 10: Batch Processing Multiple Files"
echo "============================================================="
echo ""

echo "Processing all TSV files in test_data/..."
echo ""

for file in test_data/*.tsv; do
  if [ -f "$file" ]; then
    basename=$(basename "$file" .tsv)
    output="output_batch_${basename}.tsv"
    
    echo "Processing: $file -> $output"
    
    bioconverter -i "$file" -o "$output" --auto-suggest --verbose=false 2>/dev/null || true
  fi
done

echo ""
echo "✓ Batch processing complete"
echo ""


# Example 11: Pipeline integration
echo "============================================================="
echo "Example 11: Pipeline Integration"
echo "============================================================="
echo ""
echo "Creating a data processing pipeline..."
echo ""

# Step 1: Convert
echo "Step 1: Convert data"
bioconverter -i test_data/genomics_gwas.tsv -o pipeline_step1.tsv --auto-suggest

# Step 2: Filter (using awk as example)
echo "Step 2: Filter significant results (p < 0.05)"
awk -F'\t' 'NR==1 || ($4 < 0.05)' pipeline_step1.tsv > pipeline_step2.tsv

# Step 3: Count results
echo "Step 3: Count results"
total_lines=$(wc -l < pipeline_step1.tsv)
sig_lines=$(wc -l < pipeline_step2.tsv)

echo ""
echo "  Total variants: $((total_lines - 1))"
echo "  Significant variants: $((sig_lines - 1))"
echo ""
echo "✓ Pipeline complete"
echo "✓ Final output: pipeline_step2.tsv"
echo ""


# Summary
echo "============================================================="
echo "All examples completed successfully!"
echo "============================================================="
echo ""
echo "Generated output files:"
ls -lh output_bash_*.tsv output_batch_*.tsv pipeline_*.tsv 2>/dev/null || echo "  (some files may not exist if test data was missing)"
echo ""
echo "Note: Some examples may fail if test data files don't exist."
echo "This is normal if running outside the test environment."
echo ""
