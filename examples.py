#!/usr/bin/env python3
"""
Comprehensive examples demonstrating the Bioinformatics Data Converter capabilities
"""

import pandas as pd
from pathlib import Path
from convertor import (
    convert_single_file,
    convert_multiple_files,
    save_results,
)
from interactive_converter import (
    auto_suggest_mapping,
    auto_detect_omics_type,
    process_large_file,
    suggest_chunk_size,
    create_omics_column_patterns,
)


def example_1_basic_conversion():
    """Example 1: Basic conversion with auto-detection"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Conversion with Auto-Detection")
    print("="*80)
    
    # Convert genomics data
    result = convert_single_file(
        filename="test_data/genomics_gwas.tsv",
        verbose=True
    )
    
    print(f"\nResult preview:")
    print(result.head())
    
    return result


def example_2_auto_suggest_api():
    """Example 2: Using auto-suggest with Python API"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Auto-Suggest with Python API")
    print("="*80)
    
    # Read data
    df = pd.read_csv("test_data/transcriptomics_rnaseq.csv")
    
    print(f"Original columns: {df.columns.tolist()}")
    
    # Detect omics type
    omics_type = auto_detect_omics_type(df)
    print(f"\nDetected omics type: {omics_type}")
    
    # Auto-suggest mappings
    suggested = auto_suggest_mapping(df)
    print(f"\nSuggested mappings:")
    for orig, std in suggested.items():
        print(f"  {orig} -> {std}")
    
    # Apply mappings
    result_df = pd.DataFrame()
    for orig, std in suggested.items():
        result_df[std] = df[orig]
    
    print(f"\nResult preview:")
    print(result_df.head())
    
    return result_df


def example_3_batch_conversion():
    """Example 3: Batch conversion of multiple files"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Batch Conversion of Multiple Files")
    print("="*80)
    
    # List of files to convert
    file_list = [
        "test_data/genomics_gwas.tsv",
        "test_data/transcriptomics_rnaseq.csv",
        "test_data/proteomics_data.tsv",
    ]
    
    # Convert all files
    results = convert_multiple_files(
        file_list=file_list,
        keep_unmatched=False,
        verbose=True
    )
    
    # Show summary
    print(f"\n" + "-"*80)
    print("Conversion Summary:")
    for filename, df in results.items():
        print(f"  {Path(filename).name}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return results


def example_4_large_file_simulation():
    """Example 4: Simulate large file processing"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Large File Processing (Simulated)")
    print("="*80)
    
    # Create a simulated large file
    print("Creating simulated large dataset...")
    large_df = pd.read_csv("test_data/genomics_gwas.tsv", sep="\t")
    
    # Replicate to make it larger (simulate 500K rows)
    large_df = pd.concat([large_df] * 100000, ignore_index=True)
    
    # Save to temporary file
    temp_file = "/tmp/large_genomics_data.tsv"
    large_df.to_csv(temp_file, sep="\t", index=False)
    
    print(f"Created temporary file with {len(large_df):,} rows")
    
    # Suggest chunk size
    chunk_size = suggest_chunk_size(temp_file, available_memory_gb=4.0)
    if chunk_size:
        print(f"Suggested chunk size: {chunk_size:,} rows")
    else:
        print("File is small enough to process without chunking")
        chunk_size = 100000  # Use default for this example
    
    # Prepare mapping
    sample_df = pd.read_csv(temp_file, sep="\t", nrows=1000)
    mapping = auto_suggest_mapping(sample_df)
    
    print("\nProcessing large file with chunking...")
    output_file = "/tmp/large_output.tsv"
    
    # Process with chunks
    process_large_file(
        filename=temp_file,
        output_file=output_file,
        column_mapping=mapping,
        chunksize=chunk_size or 100000,
        verbose=True,
        sep="\t"
    )
    
    # Verify output
    result_sample = pd.read_csv(output_file, sep="\t", nrows=5)
    print("\nOutput sample:")
    print(result_sample)
    
    return output_file


def example_5_custom_patterns():
    """Example 5: Using custom column patterns"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Custom Column Patterns")
    print("="*80)
    
    import re
    
    # Create custom patterns for specialized fields
    custom_patterns = {
        'custom_id': re.compile(r'^(myid|custom_identifier|special_id)$', re.IGNORECASE),
        'custom_score': re.compile(r'^(score|my_score|ranking)$', re.IGNORECASE),
    }
    
    print("Custom patterns defined:")
    for field, pattern in custom_patterns.items():
        print(f"  {field}: {pattern.pattern}")
    
    # Note: In real usage, you would apply these patterns during conversion
    # For demonstration, we'll just show the concept
    
    return custom_patterns


def example_6_output_formats():
    """Example 6: Different output formats"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Different Output Formats")
    print("="*80)
    
    # Convert data
    result = convert_single_file(
        filename="test_data/genomics_gwas.tsv",
        verbose=False
    )
    
    # Save in different formats
    output_dir = Path("/tmp/format_examples")
    output_dir.mkdir(exist_ok=True)
    
    # TSV (default, compressed)
    tsv_file = output_dir / "output.tsv.gz"
    result.to_csv(tsv_file, sep="\t", index=False, compression="gzip")
    print(f"Saved TSV (gzipped): {tsv_file}")
    
    # CSV (uncompressed)
    csv_file = output_dir / "output.csv"
    result.to_csv(csv_file, index=False)
    print(f"Saved CSV: {csv_file}")
    
    # Parquet (columnar format)
    parquet_file = output_dir / "output.parquet"
    result.to_parquet(parquet_file, compression="snappy")
    print(f"Saved Parquet: {parquet_file}")
    
    # Show file sizes
    print("\nFile sizes:")
    for f in [tsv_file, csv_file, parquet_file]:
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name}: {size_kb:.2f} KB")
    
    return output_dir


def example_7_metadata_integration():
    """Example 7: Adding metadata to converted data"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Metadata Integration")
    print("="*80)
    
    # Create metadata DataFrame
    metadata = pd.DataFrame({
        'file': [
            'test_data/genomics_gwas.tsv',
            'test_data/transcriptomics_rnaseq.csv',
        ],
        'study': ['GWAS_Study_2024', 'RNAseq_Study_2024'],
        'tissue': ['Blood', 'Brain'],
        'n_samples': [10000, 50]
    })
    
    print("Metadata table:")
    print(metadata)
    
    # Convert files with metadata
    from convertor import convert_from_metadata
    
    results = convert_from_metadata(
        metadata_df=metadata,
        file_column='file',
        metadata_columns=['study', 'tissue', 'n_samples'],
        verbose=False
    )
    
    # Show results with metadata
    print("\n" + "-"*80)
    for filename, df in results.items():
        print(f"\nFile: {Path(filename).name}")
        print(df.head(3))
    
    return results


def example_8_keep_unmatched_columns():
    """Example 8: Preserving unmapped columns"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Keep Unmatched Columns")
    print("="*80)
    
    # Create data with some non-standard columns
    test_df = pd.DataFrame({
        'CHR': [1, 2, 3],
        'POS': [1000, 2000, 3000],
        'SNP': ['rs1', 'rs2', 'rs3'],
        'P': [0.001, 0.01, 0.1],
        'CustomField1': ['A', 'B', 'C'],
        'CustomField2': [1.5, 2.5, 3.5]
    })
    
    temp_file = "/tmp/test_with_custom.tsv"
    test_df.to_csv(temp_file, sep="\t", index=False)
    
    print("Original data:")
    print(test_df)
    
    # Convert without keeping unmatched
    result1 = convert_single_file(
        filename=temp_file,
        keep_unmatched=False,
        verbose=False
    )
    
    print(f"\nWithout keep_unmatched: {result1.columns.tolist()}")
    
    # Convert with keeping unmatched
    result2 = convert_single_file(
        filename=temp_file,
        keep_unmatched=True,
        verbose=False
    )
    
    print(f"With keep_unmatched: {result2.columns.tolist()}")
    
    return result1, result2


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("BIOINFORMATICS DATA CONVERTER - USAGE EXAMPLES")
    print("="*80)
    
    # Run examples
    try:
        example_1_basic_conversion()
    except Exception as e:
        print(f"Example 1 error: {e}")
    
    try:
        example_2_auto_suggest_api()
    except Exception as e:
        print(f"Example 2 error: {e}")
    
    try:
        example_3_batch_conversion()
    except Exception as e:
        print(f"Example 3 error: {e}")
    
    try:
        example_4_large_file_simulation()
    except Exception as e:
        print(f"Example 4 error: {e}")
    
    try:
        example_5_custom_patterns()
    except Exception as e:
        print(f"Example 5 error: {e}")
    
    try:
        example_6_output_formats()
    except Exception as e:
        print(f"Example 6 error: {e}")
    
    try:
        example_7_metadata_integration()
    except Exception as e:
        print(f"Example 7 error: {e}")
    
    try:
        example_8_keep_unmatched_columns()
    except Exception as e:
        print(f"Example 8 error: {e}")
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)


if __name__ == "__main__":
    main()
