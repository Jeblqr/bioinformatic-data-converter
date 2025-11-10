# Testing Guide for bioConv

## Quick Start

Run the comprehensive test suite:
```bash
python3 test_geo_data.py
```

## What Gets Tested

### 1. Real-World Data Formats
The test suite validates conversion of authentic bioinformatics data formats:
- **GWAS Catalog**: Genome-wide association study summary statistics
- **GEO RNA-seq**: Gene expression data (DESeq2 format)
- **GEO Microarray**: Expression profiling data
- **MaxQuant**: Proteomics mass spectrometry data
- **LC-MS**: Metabolomics compound profiling

### 2. Core Functionality
- ✓ Auto-detection of file formats (CSV, TSV, compressed)
- ✓ Auto-detection of omics types (genomics, transcriptomics, proteomics, metabolomics)
- ✓ Intelligent column name mapping
- ✓ Batch processing of multiple files
- ✓ Large file handling (tested with 50,000+ rows)
- ✓ Multiple output formats (TSV.GZ, CSV, Parquet)
- ✓ Data integrity preservation

### 3. Coverage by Omics Type

| Omics Type | Test Files | Key Features |
|------------|------------|--------------|
| Genomics | 3 files | GWAS stats, variants, SNPs |
| Transcriptomics | 2 files | RNA-seq, microarray, differential expression |
| Proteomics | 2 files | Protein abundance, MaxQuant format |
| Metabolomics | 2 files | LC-MS, compound profiling |

## Test Results

Expected output:
```
================================================================================
TEST SUMMARY
================================================================================

Total tests: 11
  ✓ Passed: 11
  ✗ Failed: 0
  ○ Skipped: 0

✓ All tests completed successfully!
```

## Sample Data

All sample data files are in the `geo_test_data/` directory:

```
geo_test_data/
├── gwas_catalog_sample.tsv          # GWAS Catalog format
├── geo_rnaseq_deseq2.csv           # DESeq2 RNA-seq results
├── geo_microarray_expression.txt   # Microarray expression
├── proteomics_maxquant.txt         # MaxQuant proteomics
└── metabolomics_lcms.csv           # LC-MS metabolomics
```

## Running Individual Tests

You can modify `test_geo_data.py` to run specific tests:

```python
# In main() function, comment out tests you don't want to run
tester.test_1_download_gwas_data()     # GWAS data
tester.test_2_download_rnaseq_data()   # RNA-seq data
tester.test_3_auto_suggest_mapping()   # Column mapping
# ... etc
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Test bioConv

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python3 test_geo_data.py
```

## Troubleshooting

### Test Failures

If tests fail, check:
1. **Dependencies**: Ensure all required packages are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Python Version**: Requires Python 3.8+
   ```bash
   python3 --version
   ```

3. **File Permissions**: Ensure write permissions for output directories

### Network Issues

The test suite attempts to download data from public repositories but gracefully falls back to local sample files if downloads fail. This ensures tests work in restricted environments.

## Adding Custom Tests

To add your own test cases:

1. Create a test method in the `TestGEOData` class:
```python
def test_11_my_custom_test(self):
    """Test 11: My custom test description"""
    print("\n" + "="*80)
    print("TEST 11: My Custom Test")
    print("="*80)
    
    try:
        # Your test code
        result = convert_single_file("path/to/your/file.csv")
        assert result.shape[0] > 0
        self.log_test("My custom test", "PASS", "Success!")
    except Exception as e:
        self.log_test("My custom test", "FAIL", str(e))
```

2. Add it to `main()`:
```python
tester.test_11_my_custom_test()
```

## Performance Benchmarks

From the test suite:
- **Small files** (<1MB): ~0.1 seconds
- **Medium files** (1-10MB): ~1-5 seconds  
- **Large files** (50,000 rows): ~5-10 seconds with chunking
- **Batch processing** (9 files): ~2-3 seconds total

## Test Data Sources

Sample data is based on formats from:
- [GWAS Catalog](https://www.ebi.ac.uk/gwas/) - Genome-wide association studies
- [GEO](https://www.ncbi.nlm.nih.gov/geo/) - Gene Expression Omnibus
- [MaxQuant](https://www.maxquant.org/) - Proteomics software
- [Metabolomics Workbench](https://www.metabolomicsworkbench.org/) - Metabolomics data

## Support

For issues or questions:
1. Check the [TEST_README.md](TEST_README.md) for detailed information
2. Review the [main README.md](README.md) for usage examples
3. Open an issue on GitHub with test output

## Best Practices

1. **Run tests before committing**: Ensure your changes don't break functionality
2. **Update test data**: Keep sample files representative of current formats
3. **Add tests for new features**: When adding new functionality, add corresponding tests
4. **Document test failures**: Include full output when reporting issues

## Quick Reference Commands

```bash
# Run all tests
python3 test_geo_data.py

# Run with verbose output
python3 test_geo_data.py 2>&1 | tee test_output.log

# Check test coverage
python3 test_geo_data.py | grep "✓\|✗\|○"

# Run and save summary
python3 test_geo_data.py 2>&1 | tail -20
```
