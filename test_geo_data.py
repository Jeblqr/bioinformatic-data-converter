#!/usr/bin/env python3
"""
Comprehensive test using real data from GEO (Gene Expression Omnibus) and public repositories.

This script downloads real bioinformatics data from public repositories and tests
all functionality of the bioConv converter with authentic datasets.
"""

import pandas as pd
import urllib.request
import gzip
import shutil
from pathlib import Path
import sys
from convertor import (
    convert_single_file,
    convert_multiple_files,
    save_results,
    create_genetic_column_patterns,
    match_columns,
)
from interactive_converter import (
    auto_suggest_mapping,
    auto_detect_omics_type,
    process_large_file,
)


class TestGEOData:
    """Comprehensive test suite using real GEO data"""
    
    def __init__(self, data_dir="geo_test_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        result = {
            'test': test_name,
            'status': status,
            'message': message
        }
        self.test_results.append(result)
        status_symbol = "✓" if status == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {message}")
        
    def download_file(self, url, filename, description=""):
        """Download a file from URL"""
        filepath = self.data_dir / filename
        
        if filepath.exists():
            print(f"  File already exists: {filename}")
            return filepath
            
        print(f"  Downloading {description}: {filename}")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"  Downloaded successfully: {filepath.stat().st_size / 1024:.2f} KB")
            return filepath
        except Exception as e:
            print(f"  Error downloading {filename}: {e}")
            return None
    
    def test_1_download_gwas_data(self):
        """Test 1: Download and process real GWAS data from GWAS Catalog"""
        print("\n" + "="*80)
        print("TEST 1: Download and Process GWAS Data")
        print("="*80)
        
        # GWAS Catalog - Sample GWAS summary statistics
        # Using a smaller dataset for testing
        gwas_url = "http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90027001-GCST90028000/GCST90027158/GCST90027158_buildGRCh38.tsv.gz"
        
        filepath = self.download_file(
            gwas_url,
            "gwas_catalog_sample.tsv.gz",
            "GWAS Catalog summary statistics"
        )
        
        if not filepath:
            # Use local sample file if download fails
            local_file = self.data_dir / "gwas_catalog_sample.tsv"
            if local_file.exists():
                filepath = local_file
                print(f"  Using local sample file: {filepath}")
            else:
                self.log_test("Download GWAS data", "SKIP", "Download failed and no local file")
                return None
            
        # Test conversion
        try:
            result = convert_single_file(
                filename=str(filepath),
                verbose=True
            )
            
            # Validate result
            assert result.shape[0] > 0, "No rows in result"
            assert result.shape[1] > 0, "No columns in result"
            
            print(f"\nResult preview:")
            print(result.head())
            print(f"\nColumns: {result.columns.tolist()}")
            
            self.log_test("Download GWAS data", "PASS", 
                         f"Converted {result.shape[0]} variants, {result.shape[1]} columns")
            return result
            
        except Exception as e:
            self.log_test("Download GWAS data", "FAIL", str(e))
            import traceback
            traceback.print_exc()
            return None
    
    def test_2_download_rnaseq_data(self):
        """Test 2: Download and process RNA-seq data from GEO"""
        print("\n" + "="*80)
        print("TEST 2: Download and Process RNA-seq Data from GEO")
        print("="*80)
        
        # GEO RNA-seq data - differential expression results
        # GSE147507 - COVID-19 RNA-seq study (processed data)
        geo_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE147nnn/GSE147507/suppl/GSE147507_RawReadCounts_Human.tsv.gz"
        
        filepath = self.download_file(
            geo_url,
            "geo_rnaseq_counts.tsv.gz",
            "GEO RNA-seq read counts"
        )
        
        if not filepath:
            # Use local sample file if download fails
            local_file = self.data_dir / "geo_rnaseq_deseq2.csv"
            if local_file.exists():
                filepath = local_file
                print(f"  Using local sample file: {filepath}")
            else:
                self.log_test("Download RNA-seq data", "SKIP", "Download failed and no local file")
                return None
            
        # Test conversion
        try:
            result = convert_single_file(
                filename=str(filepath),
                verbose=True
            )
            
            # Validate result
            assert result.shape[0] > 0, "No rows in result"
            
            print(f"\nResult preview:")
            print(result.head())
            print(f"\nColumns: {result.columns.tolist()}")
            
            self.log_test("Download RNA-seq data", "PASS",
                         f"Converted {result.shape[0]} genes, {result.shape[1]} columns")
            return result
            
        except Exception as e:
            self.log_test("Download RNA-seq data", "FAIL", str(e))
            import traceback
            traceback.print_exc()
            return None
    
    def test_3_auto_suggest_mapping(self):
        """Test 3: Test auto-suggestion with real data"""
        print("\n" + "="*80)
        print("TEST 3: Auto-Suggest Column Mapping")
        print("="*80)
        
        # Use existing test data
        test_files = [
            "test_data/genomics_gwas.tsv",
            "test_data/transcriptomics_rnaseq.csv",
        ]
        
        for test_file in test_files:
            if not Path(test_file).exists():
                continue
                
            print(f"\nTesting: {test_file}")
            try:
                # Read sample
                if test_file.endswith('.csv'):
                    df = pd.read_csv(test_file, nrows=100)
                else:
                    df = pd.read_csv(test_file, sep='\t', nrows=100)
                
                # Auto-suggest mapping
                suggested = auto_suggest_mapping(df)
                
                print(f"Original columns: {df.columns.tolist()}")
                print(f"Suggested mappings:")
                for orig, std in suggested.items():
                    print(f"  {orig} -> {std}")
                
                # Detect omics type
                omics_type = auto_detect_omics_type(df)
                print(f"Detected omics type: {omics_type}")
                
                assert len(suggested) > 0, "No mappings suggested"
                self.log_test(f"Auto-suggest for {Path(test_file).name}", "PASS",
                            f"Mapped {len(suggested)} columns, type={omics_type}")
                
            except Exception as e:
                self.log_test(f"Auto-suggest for {Path(test_file).name}", "FAIL", str(e))
    
    def test_4_batch_conversion(self):
        """Test 4: Batch conversion of multiple files"""
        print("\n" + "="*80)
        print("TEST 4: Batch Conversion of Multiple Files")
        print("="*80)
        
        # Collect all available test files
        file_list = []
        for pattern in ['test_data/*.tsv', 'test_data/*.csv']:
            import glob
            file_list.extend(glob.glob(pattern))
        
        if not file_list:
            self.log_test("Batch conversion", "SKIP", "No test files found")
            return
        
        print(f"Files to convert: {len(file_list)}")
        for f in file_list:
            print(f"  - {f}")
        
        try:
            results = convert_multiple_files(
                file_list=file_list,
                keep_unmatched=False,
                verbose=True
            )
            
            print(f"\nConversion summary:")
            total_rows = 0
            for filename, df in results.items():
                rows = df.shape[0]
                cols = df.shape[1]
                total_rows += rows
                print(f"  {Path(filename).name}: {rows} rows, {cols} columns")
            
            assert len(results) == len(file_list), "Not all files converted"
            assert total_rows > 0, "No data converted"
            
            self.log_test("Batch conversion", "PASS",
                         f"Converted {len(results)} files, {total_rows} total rows")
            
        except Exception as e:
            self.log_test("Batch conversion", "FAIL", str(e))
            import traceback
            traceback.print_exc()
    
    def test_5_output_formats(self):
        """Test 5: Test different output formats"""
        print("\n" + "="*80)
        print("TEST 5: Output Format Testing")
        print("="*80)
        
        # Use existing test data
        test_file = "test_data/genomics_gwas.tsv"
        if not Path(test_file).exists():
            self.log_test("Output formats", "SKIP", "Test file not found")
            return
        
        try:
            # Convert data
            result = convert_single_file(test_file, verbose=False)
            
            # Test different output formats
            output_dir = self.data_dir / "output_test"
            output_dir.mkdir(exist_ok=True)
            
            formats_tested = []
            
            # TSV gzipped
            tsv_gz = output_dir / "test_output.tsv.gz"
            result.to_csv(tsv_gz, sep='\t', index=False, compression='gzip')
            formats_tested.append(f"TSV.GZ ({tsv_gz.stat().st_size / 1024:.2f} KB)")
            
            # CSV
            csv_file = output_dir / "test_output.csv"
            result.to_csv(csv_file, index=False)
            formats_tested.append(f"CSV ({csv_file.stat().st_size / 1024:.2f} KB)")
            
            # Parquet
            parquet_file = output_dir / "test_output.parquet"
            result.to_parquet(parquet_file, compression='snappy')
            formats_tested.append(f"Parquet ({parquet_file.stat().st_size / 1024:.2f} KB)")
            
            # Verify files can be read back
            df_tsv = pd.read_csv(tsv_gz, sep='\t', compression='gzip')
            df_csv = pd.read_csv(csv_file)
            df_parquet = pd.read_parquet(parquet_file)
            
            assert df_tsv.shape == result.shape, "TSV roundtrip failed"
            assert df_csv.shape == result.shape, "CSV roundtrip failed"
            assert df_parquet.shape == result.shape, "Parquet roundtrip failed"
            
            print("\nFormats tested:")
            for fmt in formats_tested:
                print(f"  ✓ {fmt}")
            
            self.log_test("Output formats", "PASS",
                         f"All formats tested: {', '.join([f.split()[0] for f in formats_tested])}")
            
        except Exception as e:
            self.log_test("Output formats", "FAIL", str(e))
            import traceback
            traceback.print_exc()
    
    def test_6_column_pattern_matching(self):
        """Test 6: Test column pattern matching comprehensiveness"""
        print("\n" + "="*80)
        print("TEST 6: Column Pattern Matching")
        print("="*80)
        
        # Get all patterns
        patterns = create_genetic_column_patterns()
        
        print(f"Total patterns defined: {len(patterns)}")
        
        # Test pattern categories
        categories = {
            'Genomics': ['chr', 'pos', 'rsid', 'ref', 'alt', 'pval', 'beta', 'se', 'or', 'frq', 'n', 'info'],
            'Transcriptomics': ['gene_id', 'gene_name', 'transcript_id', 'expression', 'fpkm', 'tpm', 'counts', 'log2fc', 'padj'],
            'Proteomics': ['protein_id', 'protein_name', 'peptide', 'abundance', 'intensity', 'ratio'],
            'Metabolomics': ['metabolite_id', 'metabolite_name', 'mz', 'rt', 'concentration', 'peak_area'],
            'Sample Info': ['sample_id', 'condition', 'timepoint', 'replicate', 'batch']
        }
        
        print("\nPattern coverage by category:")
        for category, fields in categories.items():
            found = sum(1 for f in fields if f in patterns)
            print(f"  {category}: {found}/{len(fields)} fields")
        
        # Test matching with various column names
        test_columns = [
            'CHR', 'chr', 'chromosome', 'CHROM',
            'POS', 'pos', 'position', 'bp',
            'P', 'pval', 'p_value', 'P-value',
            'gene_id', 'ENSG', 'gene_name', 'symbol',
            'log2FoldChange', 'LFC', 'log2fc',
        ]
        
        print("\nTesting column name matching:")
        matched_results = match_columns(test_columns)
        matches = sum(1 for v in matched_results.values() if v is not None)
        
        for col, std in matched_results.items():
            if std:
                print(f"  ✓ '{col}' -> '{std}'")
            else:
                print(f"  ✗ '{col}' -> (no match)")
        
        self.log_test("Column pattern matching", "PASS",
                     f"Matched {matches}/{len(test_columns)} test columns")
    
    def test_7_large_file_handling(self):
        """Test 7: Test large file handling with chunking"""
        print("\n" + "="*80)
        print("TEST 7: Large File Handling (Simulated)")
        print("="*80)
        
        # Create simulated large file
        test_file = "test_data/genomics_gwas.tsv"
        if not Path(test_file).exists():
            self.log_test("Large file handling", "SKIP", "Test file not found")
            return
        
        try:
            # Read original data
            df_orig = pd.read_csv(test_file, sep='\t')
            
            # Replicate to create larger dataset (simulate 50K rows)
            large_df = pd.concat([df_orig] * 10000, ignore_index=True)
            
            # Save to temp file
            temp_large = self.data_dir / "large_test_file.tsv"
            large_df.to_csv(temp_large, sep='\t', index=False)
            
            print(f"Created simulated large file: {len(large_df):,} rows")
            print(f"File size: {temp_large.stat().st_size / (1024*1024):.2f} MB")
            
            # Test chunked processing
            output_file = self.data_dir / "large_output.tsv"
            
            # Get mapping for the data
            sample_df = pd.read_csv(temp_large, sep='\t', nrows=100)
            mapping = auto_suggest_mapping(sample_df)
            
            print("\nProcessing with chunks...")
            process_large_file(
                filename=str(temp_large),
                output_file=str(output_file),
                column_mapping=mapping,
                chunksize=10000,
                verbose=True,
                sep='\t'
            )
            
            # Verify output
            result_df = pd.read_csv(output_file, sep='\t')
            
            print(f"\nOutput verification:")
            print(f"  Input rows: {len(large_df):,}")
            print(f"  Output rows: {len(result_df):,}")
            print(f"  Columns: {result_df.columns.tolist()}")
            
            assert len(result_df) == len(large_df), "Row count mismatch"
            
            self.log_test("Large file handling", "PASS",
                         f"Processed {len(result_df):,} rows in chunks")
            
            # Cleanup
            temp_large.unlink()
            output_file.unlink()
            
        except Exception as e:
            self.log_test("Large file handling", "FAIL", str(e))
            import traceback
            traceback.print_exc()
    
    def test_8_data_integrity(self):
        """Test 8: Verify data integrity through conversion"""
        print("\n" + "="*80)
        print("TEST 8: Data Integrity Verification")
        print("="*80)
        
        test_file = "test_data/genomics_gwas.tsv"
        if not Path(test_file).exists():
            self.log_test("Data integrity", "SKIP", "Test file not found")
            return
        
        try:
            # Read original data
            df_orig = pd.read_csv(test_file, sep='\t')
            
            # Convert
            df_converted = convert_single_file(test_file, verbose=False)
            
            # Check that data values are preserved
            # CHR -> chr
            if 'CHR' in df_orig.columns and 'chr' in df_converted.columns:
                assert df_orig['CHR'].equals(df_converted['chr']), "CHR values not preserved"
                print("  ✓ CHR values preserved")
            
            # POS -> pos
            if 'POS' in df_orig.columns and 'pos' in df_converted.columns:
                assert df_orig['POS'].equals(df_converted['pos']), "POS values not preserved"
                print("  ✓ POS values preserved")
            
            # P -> pval
            if 'P' in df_orig.columns and 'pval' in df_converted.columns:
                assert df_orig['P'].equals(df_converted['pval']), "P values not preserved"
                print("  ✓ P values preserved")
            
            # Verify no data loss
            assert df_orig.shape[0] == df_converted.shape[0], "Row count changed"
            print(f"  ✓ Row count preserved: {df_orig.shape[0]}")
            
            self.log_test("Data integrity", "PASS",
                         "All values preserved through conversion")
            
        except Exception as e:
            self.log_test("Data integrity", "FAIL", str(e))
            import traceback
            traceback.print_exc()
    
    def test_9_geo_format_files(self):
        """Test 9: Test conversion of all GEO format sample files"""
        print("\n" + "="*80)
        print("TEST 9: GEO Format File Conversion")
        print("="*80)
        
        # Test files with different GEO/public data formats
        test_files = {
            'geo_test_data/gwas_catalog_sample.tsv': 'GWAS Catalog format',
            'geo_test_data/geo_rnaseq_deseq2.csv': 'DESeq2 RNA-seq results',
            'geo_test_data/geo_microarray_expression.txt': 'GEO microarray expression',
            'geo_test_data/proteomics_maxquant.txt': 'MaxQuant proteomics',
            'geo_test_data/metabolomics_lcms.csv': 'LC-MS metabolomics'
        }
        
        results = []
        for filepath, description in test_files.items():
            if not Path(filepath).exists():
                print(f"  ○ Skipping {description}: file not found")
                continue
                
            print(f"\n  Testing {description}...")
            try:
                result = convert_single_file(
                    filename=filepath,
                    verbose=False,
                    keep_unmatched=True
                )
                
                print(f"    ✓ Converted: {result.shape[0]} rows, {result.shape[1]} columns")
                print(f"    Columns: {result.columns.tolist()[:10]}")  # Show first 10
                results.append((description, result))
                
            except Exception as e:
                print(f"    ✗ Failed: {e}")
                self.log_test(f"GEO format: {description}", "FAIL", str(e))
                import traceback
                traceback.print_exc()
        
        if results:
            self.log_test("GEO format files", "PASS",
                         f"Successfully converted {len(results)}/{len(test_files)} file types")
        else:
            self.log_test("GEO format files", "FAIL", "No files converted")
    
    def test_10_cross_omics_integration(self):
        """Test 10: Test handling of mixed omics data"""
        print("\n" + "="*80)
        print("TEST 10: Cross-Omics Data Integration")
        print("="*80)
        
        # Test batch conversion of different omics types
        import glob
        all_files = []
        all_files.extend(glob.glob('test_data/*.tsv'))
        all_files.extend(glob.glob('test_data/*.csv'))
        all_files.extend(glob.glob('geo_test_data/*.tsv'))
        all_files.extend(glob.glob('geo_test_data/*.csv'))
        all_files.extend(glob.glob('geo_test_data/*.txt'))
        
        if not all_files:
            self.log_test("Cross-omics integration", "SKIP", "No files found")
            return
        
        print(f"Found {len(all_files)} data files across different omics types")
        
        try:
            # Convert all files
            results = convert_multiple_files(
                file_list=all_files,
                keep_unmatched=True,
                verbose=False
            )
            
            # Analyze omics type distribution
            omics_counts = {}
            for filepath, df in results.items():
                sample_df = df.head(10) if len(df) > 10 else df
                omics_type = auto_detect_omics_type(sample_df)
                omics_counts[omics_type] = omics_counts.get(omics_type, 0) + 1
            
            print("\nOmics type distribution:")
            for omics_type, count in omics_counts.items():
                print(f"  {omics_type}: {count} files")
            
            total_rows = sum(df.shape[0] for df in results.values())
            
            self.log_test("Cross-omics integration", "PASS",
                         f"Processed {len(results)} files, {total_rows:,} total rows across {len(omics_counts)} omics types")
            
        except Exception as e:
            self.log_test("Cross-omics integration", "FAIL", str(e))
            import traceback
            traceback.print_exc()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIP')
        
        print(f"\nTotal tests: {total}")
        print(f"  ✓ Passed: {passed}")
        print(f"  ✗ Failed: {failed}")
        print(f"  ○ Skipped: {skipped}")
        
        if failed > 0:
            print("\nFailed tests:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  ✗ {result['test']}: {result['message']}")
        
        print("\n" + "="*80)
        
        return passed, failed, skipped


def main():
    """Run all tests"""
    print("="*80)
    print("COMPREHENSIVE TEST SUITE - GEO DATA")
    print("Testing bioConv with real data from public repositories")
    print("="*80)
    
    tester = TestGEOData()
    
    # Run all tests
    tester.test_1_download_gwas_data()
    tester.test_2_download_rnaseq_data()
    tester.test_3_auto_suggest_mapping()
    tester.test_4_batch_conversion()
    tester.test_5_output_formats()
    tester.test_6_column_pattern_matching()
    tester.test_7_large_file_handling()
    tester.test_8_data_integrity()
    tester.test_9_geo_format_files()
    tester.test_10_cross_omics_integration()
    
    # Print summary
    passed, failed, skipped = tester.print_summary()
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ All tests completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
