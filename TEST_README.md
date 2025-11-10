# Comprehensive Test Suite with GEO Data

This directory contains comprehensive tests for the bioConv bioinformatics data converter using real-world data formats from public repositories like GEO (Gene Expression Omnibus) and GWAS Catalog.

## Test Files

### Main Test Script
- **`test_geo_data.py`**: Comprehensive test suite that validates all functionality with realistic data

### Sample Data Files

The `geo_test_data/` directory contains sample data files in various public repository formats:

1. **`gwas_catalog_sample.tsv`**: GWAS Catalog format summary statistics
   - Format: Tab-separated values
   - Contains: chromosome, position, variant_id, alleles, effect sizes, p-values
   - Represents: Genome-wide association study results

2. **`geo_rnaseq_deseq2.csv`**: RNA-seq differential expression results (DESeq2 format)
   - Format: Comma-separated values
   - Contains: Gene IDs, fold changes, p-values, adjusted p-values
   - Represents: Transcriptomics data from GEO

3. **`geo_microarray_expression.txt`**: GEO microarray expression data
   - Format: Tab-separated values
   - Contains: Probe IDs, gene symbols, expression values across samples
   - Represents: Gene expression profiling data

4. **`proteomics_maxquant.txt`**: MaxQuant proteomics output format
   - Format: Tab-separated values
   - Contains: Protein IDs, gene names, intensities, peptide counts
   - Represents: Mass spectrometry-based proteomics data

5. **`metabolomics_lcms.csv`**: LC-MS metabolomics data
   - Format: Comma-separated values
   - Contains: Compound names, HMDB IDs, m/z values, retention times, peak areas
   - Represents: Metabolomics profiling data

## Running the Tests

### Run All Tests
```bash
python3 test_geo_data.py
```

This will execute all 10 test cases:

1. **Test 1**: Download and process GWAS data (attempts download, falls back to local)
2. **Test 2**: Download and process RNA-seq data from GEO (attempts download, falls back to local)
3. **Test 3**: Auto-suggest column mapping for different omics types
4. **Test 4**: Batch conversion of multiple files
5. **Test 5**: Test different output formats (TSV.GZ, CSV, Parquet)
6. **Test 6**: Column pattern matching comprehensiveness
7. **Test 7**: Large file handling with chunking
8. **Test 8**: Data integrity verification through conversion
9. **Test 9**: GEO format file conversion
10. **Test 10**: Cross-omics data integration

### Expected Output

The test suite will output:
- ✓ for passed tests
- ✗ for failed tests  
- ○ for skipped tests

At the end, you'll see a summary like:
```
================================================================================
TEST SUMMARY
================================================================================

Total tests: 11
  ✓ Passed: 11
  ✗ Failed: 0
  ○ Skipped: 0
```

## Test Coverage

The test suite validates:

### Functionality Coverage
- ✓ Auto-detection of file formats (CSV, TSV, compressed files)
- ✓ Auto-detection of omics types (genomics, transcriptomics, proteomics, metabolomics)
- ✓ Column name mapping and standardization
- ✓ Multiple input formats (GWAS Catalog, GEO, MaxQuant, LC-MS)
- ✓ Batch processing of multiple files
- ✓ Large file handling with chunking
- ✓ Multiple output formats (TSV, CSV, Parquet)
- ✓ Data integrity preservation
- ✓ Cross-omics integration

### Omics Types Covered
- ✓ **Genomics**: GWAS summary statistics, variant data
- ✓ **Transcriptomics**: RNA-seq, microarray expression data
- ✓ **Proteomics**: MaxQuant peptide/protein abundance
- ✓ **Metabolomics**: LC-MS compound profiling

### Data Sources
- ✓ GWAS Catalog format
- ✓ GEO (Gene Expression Omnibus) formats
- ✓ MaxQuant proteomics
- ✓ LC-MS metabolomics
- ✓ DESeq2 differential expression

## Adding New Tests

To add a new test case:

1. Add a new method to the `TestGEOData` class:
```python
def test_N_your_test_name(self):
    """Test N: Description"""
    print("\n" + "="*80)
    print("TEST N: Your Test Name")
    print("="*80)
    
    try:
        # Your test code here
        self.log_test("Your test name", "PASS", "Success message")
    except Exception as e:
        self.log_test("Your test name", "FAIL", str(e))
```

2. Call your test in the `main()` function:
```python
tester.test_N_your_test_name()
```

## Sample Data Sources

The sample data files are based on typical formats from:

- **GWAS Catalog**: https://www.ebi.ac.uk/gwas/
  - Public database of genome-wide association studies
  
- **GEO (Gene Expression Omnibus)**: https://www.ncbi.nlm.nih.gov/geo/
  - Public functional genomics data repository
  
- **MaxQuant**: Widely used proteomics analysis software
  - Standard output format for mass spectrometry data
  
- **Metabolomics Workbench**: https://www.metabolomicsworkbench.org/
  - Repository for metabolomics data

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run comprehensive tests
  run: python3 test_geo_data.py
```

## Troubleshooting

### Network Issues
If the download tests fail due to network restrictions, the tests will automatically fall back to using local sample files in the `geo_test_data/` directory.

### Missing Dependencies
Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas >= 2.0.0
- numpy >= 1.24.0
- pyarrow >= 12.0.0 (for Parquet support)

## License

The sample data files are provided for testing purposes and are based on publicly available data formats.
