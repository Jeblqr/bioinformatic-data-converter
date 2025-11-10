#!/usr/bin/env python3
"""
Python Example: Using bioconverter for data conversion

This example demonstrates how to use bioconverter in Python scripts.
"""

import pandas as pd
from bioconverter.convertor import convert_single_file, convert_multiple_files
from bioconverter.interactive_converter import (
    auto_suggest_mapping,
    auto_detect_omics_type,
    process_large_file
)
from bioconverter.conversion_report import ConversionReport

def example_basic_conversion():
    """Example 1: Basic single file conversion"""
    print("=" * 60)
    print("Example 1: Basic Single File Conversion")
    print("=" * 60)
    
    # Convert a single file with automatic format detection
    result = convert_single_file(
        filename="test_data/genomics_gwas.tsv",
        verbose=True
    )
    
    print(f"\nResult shape: {result.shape}")
    print(f"Columns: {list(result.columns)}")
    print("\nFirst few rows:")
    print(result.head())
    
    # Save the result
    result.to_csv("output_gwas.tsv", sep='\t', index=False)
    print("\n✓ Output saved to: output_gwas.tsv")


def example_auto_suggest():
    """Example 2: Auto-suggest column mapping"""
    print("\n" + "=" * 60)
    print("Example 2: Auto-suggest Column Mapping")
    print("=" * 60)
    
    # Read sample data
    df = pd.read_csv("test_data/transcriptomics_rnaseq.csv", nrows=100)
    
    # Auto-detect omics type
    omics_type = auto_detect_omics_type(df)
    print(f"\nDetected omics type: {omics_type}")
    
    # Get suggested mappings
    mapping = auto_suggest_mapping(df)
    print("\nSuggested column mappings:")
    for original, standard in mapping.items():
        print(f"  {original:20s} -> {standard}")
    
    # Apply the mapping
    result = convert_single_file(
        filename="test_data/transcriptomics_rnaseq.csv",
        column_mapping=mapping,
        verbose=False
    )
    
    print(f"\n✓ Conversion complete: {result.shape[0]} rows, {result.shape[1]} columns")


def example_custom_mapping():
    """Example 3: Custom column mapping"""
    print("\n" + "=" * 60)
    print("Example 3: Custom Column Mapping")
    print("=" * 60)
    
    # Define custom mapping
    custom_mapping = {
        "Chromosome": "chr",
        "Position": "pos",
        "P_value": "pval",
        "Effect_size": "beta",
        "Standard_error": "se"
    }
    
    print("\nCustom mapping:")
    for k, v in custom_mapping.items():
        print(f"  {k} -> {v}")
    
    # Apply custom mapping (simulated with existing file)
    result = convert_single_file(
        filename="test_data/genomics_gwas.tsv",
        column_mapping=custom_mapping,
        keep_unmatched=True,
        verbose=True
    )
    
    print(f"\n✓ Result columns: {list(result.columns)}")


def example_batch_conversion():
    """Example 4: Batch convert multiple files"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Conversion")
    print("=" * 60)
    
    # List of files to convert
    files = [
        "test_data/genomics_gwas.tsv",
        "test_data/transcriptomics_rnaseq.csv",
        "test_data/proteomics_data.tsv"
    ]
    
    print(f"\nConverting {len(files)} files...")
    
    # Batch convert
    results = convert_multiple_files(
        file_list=files,
        keep_unmatched=False,
        verbose=False
    )
    
    # Display results
    print("\nConversion results:")
    for filename, df in results.items():
        print(f"  {filename:40s} -> {df.shape[0]:6d} rows, {df.shape[1]:2d} cols")
    
    # Save all results
    for filename, df in results.items():
        output_name = f"standardized_{filename.split('/')[-1]}"
        df.to_csv(output_name, sep='\t', index=False)
        print(f"  ✓ Saved: {output_name}")


def example_large_file():
    """Example 5: Process large file with chunking"""
    print("\n" + "=" * 60)
    print("Example 5: Large File Processing (Simulated)")
    print("=" * 60)
    
    # For demonstration, we'll process a small file with chunking
    print("\nProcessing file with chunking (chunk_size=1000)...")
    
    process_large_file(
        filename="test_data/genomics_gwas.tsv",
        output_file="output_large.tsv",
        column_mapping=None,  # Auto-detect
        chunksize=1000,
        verbose=True,
        sep='\t'
    )
    
    print("\n✓ Large file processed and saved to: output_large.tsv")


def example_with_report():
    """Example 6: Generate conversion report"""
    print("\n" + "=" * 60)
    print("Example 6: Generate Conversion Report")
    print("=" * 60)
    
    # Convert with reporting
    input_file = "test_data/metabolomics_data.csv"
    
    # Read original data for reporting
    df_orig = pd.read_csv(input_file)
    
    # Convert
    result = convert_single_file(
        filename=input_file,
        verbose=True
    )
    
    # Create report
    report = ConversionReport()
    
    # Set input info
    report.set_input_info(
        filename=input_file,
        columns=list(df_orig.columns),
        rows=len(df_orig),
        file_size_mb=0.1,
        omics_type="metabolomics"
    )
    
    # Set output info
    report.set_output_info(
        filename="output_metabolomics.tsv",
        columns=list(result.columns)
    )
    
    # Set mapping info
    mapping = auto_suggest_mapping(df_orig)
    report.set_column_mapping(
        mapping=mapping,
        unmapped=[]
    )
    
    # Set processing info
    report.set_processing_info()
    
    # Save report
    report.save_report(report_dir="./reports/", prefix="metabolomics_conversion")
    
    print("\n✓ Report saved to: ./reports/metabolomics_conversion_report.txt")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("bioconverter Python Examples")
    print("=" * 60)
    
    try:
        example_basic_conversion()
        example_auto_suggest()
        example_custom_mapping()
        example_batch_conversion()
        example_large_file()
        example_with_report()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully! ✓")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n⚠ Note: Some test files may not exist: {e}")
        print("This is normal if running outside the test environment.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
